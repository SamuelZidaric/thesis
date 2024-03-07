import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Your main path
main_path = 'Z:/neurobiology/zimmer/zidaric/data/int_neg/data/'

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

# Assuming the group logic is based on a predefined sequence of group values
subdivision_values = [60, 0, 40, 10, 80, 20, 40, 10, 60, 20, 80, 0, 40, 60, 80, 20, 10, 0, 60, 40, 20, 80, 0, 10, 60, 40, 80, 0, 10, 20]
# Repeat the subdivision values to cover all rows in the dataset
extended_subdivision_values = subdivision_values * ((len(all_data) // len(subdivision_values)) + 2)
all_data['Group'] = extended_subdivision_values[:len(all_data)]
# Convert 'Status/Reaction Time' to 'No Reversal', 'Valid Reversals', and 'Already Reversing' categories
all_data['Status'] = np.where(all_data['Status/Reaction Time'] == 'No Reversal', 'No Reversal',
                              np.where(all_data['Status/Reaction Time'] == 'Already Reversing', 'Already Reversing', 'Valid Reversals'))

# Now, for visualization, we can count the frequencies of each status within each group
# This example assumes you have a 'Group' column. Adjust accordingly if your data needs a different approach

# Count the frequency of each status within each group
status_counts = all_data.groupby('Group')['Status'].value_counts(normalize=True).unstack(fill_value=0)

# Plotting the frequencies of 'Valid Reversals', 'No Reversal', and 'Already Reversing'
ax = status_counts[['Valid Reversals', 'No Reversal', 'Already Reversing']].plot(kind='bar', stacked=True, figsize=(14, 8), color=['green', 'red', 'yellow'], legend=True)
plt.title('Frequency of Reversal Status by Group')
plt.xlabel('LED Power')
plt.ylabel('Frequency')

# Annotate percentages on each bar
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    if height > 0:  # Only display labels for bars with height
        ax.text(x + width/2, 
                y + height/2, 
                f'{height:.0%}', 
                horizontalalignment='center', 
                verticalalignment='center')

plt.legend(['Valid Reversals', 'No Reversal', 'Already Reversing'], loc='upper right')
plt.grid(axis='y', alpha=0.75)
plt.show()


