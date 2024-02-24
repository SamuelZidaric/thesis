import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

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

# Convert 'Status/Reaction Time' to a new column indicating reversal (1), no reversal (0), or exclude (-1 for "Already Reversing" and "No movement")
all_data['Reversal Status'] = np.where(all_data['Status/Reaction Time'] == 'No Reversal', 0,
                                       np.where((all_data['Status/Reaction Time'] == 'Already Reversing') | 
                                                (all_data['Status/Reaction Time'] == 'No movement'), -1, 1))

# Exclude "Already Reversing" from calculations
filtered_data = all_data[all_data['Reversal Status'] != -1]

# Calculate the probability of reversal for each activation, excluding "Already Reversing"
reversal_probability = filtered_data.groupby('Activation')['Reversal Status'].mean().reset_index()

# Calculate the count of observations (excluding "Already Reversing") for each activation
counts_per_activation = filtered_data.groupby('Activation').size()

# Visualization with Seaborn: Bar plot of reversal probabilities by Activation
plt.figure(figsize=(12, 8))
barplot = sns.barplot(x='Activation', y='Reversal Status', data=reversal_probability, color='darkblue')
plt.title('Probability of Reversal per Activation (ATR-positives)')
plt.xlabel('Activation Number')
plt.ylabel('Probability of Reversal')
plt.ylim(0, 1)  # Set the y-axis to go from 0 to 1
plt.grid(True)
plt.xticks(rotation=45)  # Rotate labels if they overlap

# Calculate the total sample size
total_sample_size = counts_per_activation.sum()

# Create a legend or annotation for the total sample size
# Here we add it as an annotation to the plot
plt.text(0.95, 0.95, f'Total sample size = {total_sample_size}', transform=plt.gcf().transFigure, 
         ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))
plt.tight_layout()
plt.show()
