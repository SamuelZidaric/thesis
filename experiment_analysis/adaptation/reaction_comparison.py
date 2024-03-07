import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Corrected paths for the two groups
group_1_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'
group_2_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli/data/'

# Generate lists of file paths for each group
rev_reaction_paths_list1 = glob.glob(os.path.join(group_1_path, 'w*/*Ch0/rev_reaction.xlsx'))
rev_reaction_paths_list2 = glob.glob(os.path.join(group_2_path, 'w*/*Ch0/rev_reaction.xlsx'))

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

def gather_reaction_times(file_paths, group_label):
    reaction_times = []  # List to hold reaction times and group labels
    
    for file_path in file_paths:
        df = pd.read_excel(file_path)
        # Convert 'Status/Reaction Time' to numeric, storing NaN for non-numeric values
        df['Numeric Reaction Time'] = pd.to_numeric(df['Status/Reaction Time'], errors='coerce')
        df = df.dropna(subset=['Numeric Reaction Time'])  # Keep only valid numeric reaction times
        df['Group'] = group_label  # Assign group label
        reaction_times.append(df[['Numeric Reaction Time', 'Group']])
    
    return pd.concat(reaction_times)

# Gather reaction times for each group
group_1_data = gather_reaction_times(rev_reaction_paths_list1, 'ATR+')
group_2_data = gather_reaction_times(rev_reaction_paths_list2, 'ATR-')

# Combine reaction times from both groups
all_reaction_times = pd.concat([group_1_data, group_2_data], ignore_index=True)

# Ensure only valid numeric reaction times are included for this comparison
valid_reaction_times = all_reaction_times.dropna(subset=['Numeric Reaction Time'])

plt.figure(figsize=(12, 8))

# Create a boxplot
boxplot = sns.boxplot(x='Group', y='Numeric Reaction Time', data=all_reaction_times, palette='Set2', showfliers=False)

# Overlay a strip plot to show individual data points
sns.stripplot(x='Group', y='Numeric Reaction Time', data=all_reaction_times, color='black', alpha=0.5, jitter=True)

# Calculate the sample size for each group
sample_sizes = all_reaction_times.groupby('Group').size().reset_index(name='Sample Size')

# Annotate the boxplot with the sample sizes
for i, (group, sample_size) in enumerate(zip(sample_sizes['Group'], sample_sizes['Sample Size'])):
    # Positioning the text annotation above the boxplot
    plt.text(i, all_reaction_times['Numeric Reaction Time'].max() + 0.07, f'n = {sample_size}', 
             horizontalalignment='center', size=10, color='black', weight='semibold', bbox=dict(facecolor='white', alpha=0.5))

plt.title('Comparison of Reaction Times Between ATR+ and ATR- Groups')
plt.ylabel('Reaction Time (seconds)')
plt.xlabel('Experimental Group')
plt.ylim(0, 2.2)  # Adjust ylim to fit annotations

plt.tight_layout()
plt.show()
