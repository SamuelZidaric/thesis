import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from scipy.stats import linregress

# Your main path
main_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'

# Glob pattern to match the file structure you mentioned
rev_reaction_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Loop through each file path in the list
for file_path in rev_reaction_paths_list:
    # Read the current Excel file
    temp_data = pd.read_excel(file_path)
    
    # Optionally, filter out activations beyond a certain threshold if needed
    if 'Activation' in temp_data.columns:
        temp_data = temp_data[temp_data['Activation'] <= 56]  # Example threshold
    
    # Add an identifier column to distinguish between datasets
    identifier = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
    temp_data['Identifier'] = identifier
    
    # Append the filtered data to the all_data DataFrame
    all_data = pd.concat([all_data, temp_data], ignore_index=True)

# Convert 'Status/Reaction Time' to numeric, coercing errors to NaN
all_data['Numeric Reaction Time'] = pd.to_numeric(all_data['Status/Reaction Time'], errors='coerce')

# Ensure 'Activation' is numeric
all_data['Activation'] = pd.to_numeric(all_data['Activation'], errors='coerce')
all_data.dropna(subset=['Activation', 'Numeric Reaction Time'], inplace=True)

# Group by 'Activation' and calculate medians
median_data = all_data.groupby('Activation').agg({'Numeric Reaction Time': 'median'}).reset_index()

# Calculate regression line based on median values
slope, intercept, r_value, p_value, std_err = linregress(median_data['Activation'], median_data['Numeric Reaction Time'])

# Plot the original data
plt.figure(figsize=(12, 8))
plt.scatter(all_data['Activation'], all_data['Numeric Reaction Time'], alpha=0.5)

# Plot the median-based regression line
x = np.array([min(all_data['Activation']), max(all_data['Activation'])])
y = intercept + slope * x
plt.plot(x, y, color='darkred', label=f'Median Regression Line\nSlope: {slope:.2f}, Intercept: {intercept:.2f}')

# Add plot labels and legend
plt.title('Reaction Times by Activation Number in ATR+ group')
plt.xlabel('Activation Number')
plt.ylabel('Reaction Time (seconds)')
plt.legend()
plt.grid(True)

# Calculate the total sample size
total_sample_size = all_data['Numeric Reaction Time'].count()

# Add a textbox with the total sample size
plt.text(0.94, 0.95, f'n = {total_sample_size}', transform=plt.gcf().transFigure, 
         ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))

plt.tight_layout()
plt.show()
