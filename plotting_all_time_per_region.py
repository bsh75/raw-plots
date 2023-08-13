import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, AutoDateLocator

def plot_and_save_average_region_data(file_path, moving_average_window, output_folder):
    df = pd.read_csv(file_path)
    
    # Convert 'Datetime' column to datetime64 dtype and set it as index
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)
    
    # Apply moving average filter
    df['Smoothed RPS Price'] = df['RPS Price'].rolling(window=moving_average_window, min_periods=1, center=True).mean()
    
    # Calculate variance
    df['Variance'] = df['RPS Price'].rolling(window=moving_average_window, min_periods=1, center=True).var()
    
    # Calculate 2nd standard deviation lines
    df['Std_Dev_Pos'] = df['Smoothed RPS Price'] + 2 * np.sqrt(df['Variance'])
    df['Std_Dev_Neg'] = df['Smoothed RPS Price'] - 2 * np.sqrt(df['Variance'])
    
    # Create a folder for each region
    region_folder = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0])
    os.makedirs(region_folder, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Smoothed RPS Price'], label=f'Smoothed RPS Price (Window={moving_average_window})')
    plt.plot(df.index, df['Std_Dev_Pos'], label=f'2nd Std Dev Above')
    plt.plot(df.index, df['Std_Dev_Neg'], label=f'2nd Std Dev Below')

    plt.xlabel('Date')
    plt.title(f'RPS Price Over Time and Variance for {os.path.basename(file_path)}')
    plt.legend()

    # Set date locator and formatter for x-axis
    date_locator = AutoDateLocator(maxticks=10)
    date_formatter = DateFormatter('%Y-%m-%d')  # Format as 'YYYY-MM-DD'

    plt.gca().xaxis.set_major_locator(date_locator)
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.xticks(rotation=45)

    # Set the x-axis limits
    plt.xlim(df.index.min(), df.index.max())

    plt.tight_layout()

    # Save the plot as an image file
    plot_filename = os.path.join(region_folder, f'plot_{moving_average_window}_avg.png')
    plt.savefig(plot_filename)

    # Save the data used in the plot as a CSV
    data_filename = os.path.join(region_folder, f'data_{moving_average_window}_avg.csv')
    df.to_csv(data_filename)

    plt.show()

data_folder = 'avg_by_region'
output_folder = 'plots_and_data'
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_folder, filename)
        plot_and_save_average_region_data(file_path, moving_average_window=100, output_folder=output_folder)
