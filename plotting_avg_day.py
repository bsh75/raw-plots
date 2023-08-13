import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator
import numpy as np

def plot_average_day_by_month(input_folder, output_folder, month_range):
    files = os.listdir(input_folder)
    
    for filename in files:
        print(filename)
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)
            
            # Convert 'Datetime' column to datetime64 dtype
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            
            # Filter data based on specified month range
            start_month, end_month = month_range
            df = df[(df['Datetime'].dt.month >= start_month) & (df['Datetime'].dt.month <= end_month)]
            
            # Group data by time of day
            df['Time'] = df['Datetime'].dt.time
            mean_by_time = df.groupby('Time')['RPS Price'].mean()
            std_by_time = df.groupby('Time')['RPS Price'].std()
            
            # Calculate upper and lower bounds for std dev lines
            upper_bound = mean_by_time + std_by_time
            lower_bound = mean_by_time - std_by_time
            
            # Convert time objects to numerical values
            time_values = np.arange(len(mean_by_time))
            
            plt.figure(figsize=(10, 6))
            plt.plot(time_values, mean_by_time.values, label='Average RPS Price')
            plt.plot(time_values, upper_bound.values, label='Upper Bound (1 Std Dev)')
            plt.plot(time_values, lower_bound.values, label='Lower Bound (1 Std Dev)')
            
            plt.xlabel('Time of Day')
            plt.ylabel('Average RPS Price')
            plt.title(f'Average Day Over Time for {os.path.basename(file_path)}')
            plt.legend()
            
            plt.xticks(time_values, mean_by_time.index, rotation=45)  # Use time labels for x-axis
            
            plt.tight_layout()
            
            # Save the plot as an image file
            output_filename = os.path.splitext(filename)[0] + f'_avg_day_plot.png'
            output_filepath = os.path.join(output_folder, output_filename)
            plt.savefig(output_filepath)
            
            plt.close()  # Close the figure after saving

input_folder = 'avg_by_region'
output_folder = 'avg_day_by_month_plots'
month_range = (8, 8)  # Specify the desired month range here

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

plot_average_day_by_month(input_folder, output_folder, month_range)
