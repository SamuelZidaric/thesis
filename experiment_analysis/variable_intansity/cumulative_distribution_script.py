
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Your main path
main_path = 'Z:/neurobiology/zimmer/zidaric/data/uli_pip/int_pos/data/'

# Glob pattern to match the file structure you mentioned
rev_reaction_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Loop through each file path in the list
for file_path in rev_reaction_paths_list:
    # Read the current Excel file
    temp_data = pd.read_excel(file_path)
    
    # Filter out activations beyond the 30th, if the 'Activation' column exists
    if 'Activation' in temp_data.columns:
        temp_data = temp_data[temp_data['Activation'] <= 30]

    # For example, extracting a part of the file_path as an identifier
    temp_data['Identifier'] = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
    
    # Append the data from the current file to the all_data DataFrame
    all_data = pd.concat([all_data, temp_data], ignore_index=True)

# Assuming the structure and content of 'all_data' matches what we've worked with:
# Calculate the group for each activation as before (using the specific order provided)
group_values = [60, 0, 40, 10, 80, 20, 40, 10, 60, 20, 80, 0, 40, 60, 80, 20, 10, 0, 60, 40, 20, 80, 0, 10, 60, 40, 80, 0, 10, 20]
all_data['Group'] = all_data['Activation'].apply(lambda x: group_values[x-1] if x <= 30 else None)

# Plotting the cumulative distribution as requested
def plot_cumulative_distribution(data):
    groups = data['Group'].unique()
    mean_values = data.groupby('Group').size().values / len(data)  # Frequency of each group
    
    sorted_indices = np.argsort(groups)
    sorted_groups = groups[sorted_indices]
    sorted_mean_values = mean_values[sorted_indices]
    
    cumulative_values = np.cumsum(sorted_mean_values)
    cumulative_distribution = cumulative_values / cumulative_values[-1]
    
    plt.figure(figsize=(14, 8))
    plt.plot(sorted_groups, cumulative_distribution, marker='o', linestyle='-', color='blue')
    plt.title('Cumulative Distribution of Mean Status Frequencies by Subgroups of ATR+')
    plt.xlabel('Group')
    plt.ylabel('Cumulative Frequency (%)')
    plt.grid(True)
    plt.show()

# Example usage with the current 'all_data'
plot_cumulative_distribution(all_data[all_data['Status/Reaction Time'] != 'Already Reversing'])
