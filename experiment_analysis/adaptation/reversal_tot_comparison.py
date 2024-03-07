import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Corrected paths for the two groups
group_1_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'
group_2_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli/data/'

def process_data(file_paths, group_label):
    total_valid_reversals = 0
    sample_size = 0  # Initialize sample size counter
    for file_path in file_paths:
        df = pd.read_excel(file_path)
        # Convert 'Status/Reaction Time' to numeric, storing NaN for non-numeric values
        df['Numeric Reaction Time'] = pd.to_numeric(df['Status/Reaction Time'], errors='coerce')
        
        # Filter the DataFrame to exclude 'No Reversal', 'No movement', and 'Already Reversing'
        filtered_df = df[~df['Status/Reaction Time'].isin(['No Reversal', 'Already Reversing', 'No movement'])]
        
        # Update total valid reversals count
        total_valid_reversals += filtered_df['Numeric Reaction Time'].notna().sum()
        
        # Update sample size to count only rows considered as attempts (excluding the specified statuses)
        sample_size += len(filtered_df)
    
    return pd.DataFrame({'Group': [group_label], 
                         'Total Valid Reversals': [total_valid_reversals], 
                         'Sample Size': [sample_size]})

# Generate lists of file paths for each group
rev_reaction_paths_list1 = glob.glob(os.path.join(group_1_path, 'w*/*Ch0/rev_reaction.xlsx'))
rev_reaction_paths_list2 = glob.glob(os.path.join(group_2_path, 'w*/*Ch0/rev_reaction.xlsx'))

# Process data for each group
group_1_data = process_data(rev_reaction_paths_list1, 'ATR+')
group_2_data = process_data(rev_reaction_paths_list2, 'ATR-')

# Combine data from both groups
combined_data = pd.concat([group_1_data, group_2_data], ignore_index=True)

plt.figure(figsize=(12, 8))  # Adjust the figure size as needed
barplot = sns.barplot(x='Group', y='Total Valid Reversals', data=combined_data, palette = 'Set1')

# Annotate bars with the sample size, adjusting the position for better visibility
for index, row in combined_data.iterrows():
    # Adjust these values as needed for optimal placement
    height = row['Total Valid Reversals']
    sample_size_text = f'n = {row["Sample Size"]}'
    x_position = index
    y_position = height + 0.05 * max(combined_data['Total Valid Reversals'])  # Adjust this for separation

    plt.text(x_position, y_position, sample_size_text, color='black', ha="center", va='bottom', weight='semibold', bbox=dict(facecolor='white', alpha=0.5))

plt.title('Comparison of Total Induced Reversals Between ATR+ and ATR- Groups')
plt.ylabel('Total Induced Reversals')
plt.xlabel('Experimental Group')
plt.xticks(rotation=45)  # Adjust or remove rotation based on your preference
plt.ylim(0, 1.2 * max(combined_data['Total Valid Reversals']))  # Extend y-axis limit for text space
plt.tight_layout()
plt.show()
