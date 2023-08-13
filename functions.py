import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_data(file_path):
    # Specify column names for the DataFrame
    column_names = ['exit_point', 'region', 'RPS', 'date', 'time_index', 'rps_price']
    
    # Read the CSV file into a DataFrame, skip the first row (header)
    df = pd.read_csv(file_path, skiprows=1, names=column_names)
    
    # Filter out rows with non-date values in the 'date' column
    df = df[df['date'].str.contains(r'^\d{2}/\d{2}/\d{4}$', na=False)]
    
    # Convert 'time_index' to integer
    df['datetime'] = pd.to_datetime(df['date'], format='%d/%m/%Y') + pd.to_timedelta((df['time_index'] - 1) * 30, unit='minutes')
    
    return df


# def save_grouped_data_to_excel(grouped_data):
#     writer = pd.ExcelWriter('grouped_data.xlsx', engine='xlsxwriter')
    
#     for region, region_data in grouped_data.items():
#         if not region_data:
#             continue
        
#         datetime_values, rps_price_values = zip(*region_data)
#         data_dict = {
#             'Datetime': datetime_values,
#             'RPS Price': rps_price_values
#         }
        
#         df = pd.DataFrame(data_dict)
#         sheet_name = f'Grouped Data - {region}'
#         df.to_excel(writer, sheet_name=sheet_name, index=False)
    
#     writer.save()

def save_grouped_data_to_excel(grouped_data):
    output_folder = 'sorted_data'
    os.makedirs(output_folder, exist_ok=True)
    
    output_path = os.path.join(output_folder, 'grouped_data.xlsx')
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for region, region_data in grouped_data.items():
            if not region_data:
                continue

            datetime_values, rps_price_values = zip(*region_data)
            data_dict = {
                'Datetime': datetime_values,
                'RPS Price': rps_price_values
            }

            df = pd.DataFrame(data_dict)

            # Truncate or modify the region name to fit within Excel's character limit
            sheet_name = f'Region - {region[:25]}' if len(region) > 25 else f'Region - {region}'
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Grouped data saved to '{output_path}'")


def save_grouped_data_to_csv(grouped_data, folder_name):
    folder_name = 'sorted_data'
    os.makedirs(folder_name, exist_ok=True)
    
    for region, region_data in grouped_data.items():
        if not region_data:
            continue
        
        datetime_values, rps_price_values = zip(*region_data)
        data_dict = {
            'Datetime': datetime_values,
            'RPS Price': rps_price_values
        }
        
        df = pd.DataFrame(data_dict)
        filename = os.path.join(folder_name, f'grouped_data_{region}.csv')
        df.to_csv(filename, index=False)


def average_region_data(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Extract region from the filename (e.g., 'grouped_data_('WATA', 'WTK0331').csv')
            region = filename.split("'")[1]
            
            df = pd.read_csv(file_path)
            averaged_df = df.groupby('Datetime')['RPS Price'].mean().reset_index()
            
            output_filename = os.path.join(output_folder, f'averaged_{region}.csv')
            averaged_df.to_csv(output_filename, index=False)


def group_data(df):
    grouped_data = df.groupby(['region', 'exit_point', 'time_index'])
    grouped_data_dict = {}

    for group_keys, group in grouped_data:
        region, exit_point, time_index = group_keys
        if (region, exit_point) not in grouped_data_dict:
            grouped_data_dict[(region, exit_point)] = []
        
        grouped_data_dict[(region, exit_point)].extend(list(zip(group['datetime'], group['rps_price'])))
    
    return grouped_data_dict

def apply_mean_filter(data, window_size):
    smoothed_data_dict = {}
    for (region, exit_point), data in data.items():
        data.sort(key=lambda x: x[0])  # Sort data by datetime
        
        datetime_values, rps_price_values = zip(*data)
        smoothed_rps_price_values = np.convolve(rps_price_values, np.ones(window_size)/window_size, mode='same')
        smoothed_data_dict[(region, exit_point)] = list(zip(datetime_values, smoothed_rps_price_values))
    
    return smoothed_data_dict

def plot_exitpoint_vs_time(data, exit_point):
    plt.figure()
    plt.title(f'Exit Point: {exit_point} - RPS Price Trends')
    
    for region, exit_point_data in data.items():
        if exit_point_data:
            datetime_values, smoothed_rps_price_values = zip(*exit_point_data)
            plt.plot(datetime_values, smoothed_rps_price_values, label=f'Region: {region}')

    plt.xlabel('Datetime')
    plt.ylabel('Smoothed RPS Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_region_over_time(data, region):
    plt.figure()
    plt.title(f'Region: {region} - RPS Price Trends')
    
    for exit_point, region_data in data.items():
        if region_data:
            datetime_values, smoothed_rps_price_values = zip(*region_data)
            plt.plot(datetime_values, smoothed_rps_price_values, label=f'Exit Point: {exit_point}')

    plt.xlabel('Datetime')
    plt.ylabel('Smoothed RPS Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()