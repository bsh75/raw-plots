import os
import pandas as pd
from functions import *

input_folder_path = 'data'
files = os.listdir(input_folder_path)
# print(files)
# Initialize an empty dictionary to store the grouped data
grouped_data_dict = {}

print(files)
# Iterate through each CSV file in the folder
for filename in files:
    print(filename)
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder_path, filename)
        df = read_data(file_path)
        grouped_data = group_data(df)
        # print(grouped_data)
        for key, value in grouped_data.items():
            if key not in grouped_data_dict:
                grouped_data_dict[key] = []
            grouped_data_dict[key].extend(value)

# print(grouped_data_dict)
save_grouped_data_to_csv(grouped_data_dict, folder_name='sorted_data')

average_region_data(folder_path='sorted_data', output_folder='avg_by_region')