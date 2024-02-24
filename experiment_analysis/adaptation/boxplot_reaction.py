import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Your main path
main_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli/data/'

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

# Convert 'Status/Reaction Time' to numeric, coercing errors to NaN (this will filter out non-numeric values)
all_data['Numeric Reaction Time'] = pd.to_numeric(all_data['Status/Reaction Time'], errors='coerce')

# Filter out rows without a valid numeric reaction time
filtered_data = all_data.dropna(subset=['Numeric Reaction Time'])

# Calculate the total sample size
total_sample_size = filtered_data['Identifier'].count()

# Visualization with Seaborn: Box plot and strip plot of reaction times by Identifier
plt.figure(figsize=(12, 8))
sns.boxplot(x='Identifier', y='Numeric Reaction Time', data=filtered_data, color='lightgray', showfliers=False)
sns.stripplot(x='Identifier', y='Numeric Reaction Time', data=filtered_data, size=4, color='darkblue', alpha=0.5)
plt.title('Distribution of Reaction Times by Individual Worm')
plt.xlabel('Worms')
plt.ylabel('Reaction Time (seconds)')
plt.grid(True)
plt.xticks(rotation=45)  # Rotate labels if they overlap
# Add a textbox with the total sample size
plt.text(0.95, 0.95, f'Total sample size = {total_sample_size}', transform=plt.gcf().transFigure, 
         ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))
plt.tight_layout()
plt.show()
