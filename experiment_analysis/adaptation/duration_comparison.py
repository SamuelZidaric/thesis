import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from scipy.stats import ttest_ind

# Corrected paths for the two groups
group_1_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'
group_2_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli/data/'

# Generate lists of file paths for each group
rev_duration_paths_list1 = glob.glob(os.path.join(group_1_path, 'w*/*Ch0/rev_duration_all.xlsx'))
rev_duration_paths_list2 = glob.glob(os.path.join(group_2_path, 'w*/*Ch0/rev_duration_all.xlsx'))

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Function to process files and append to DataFrame
def process_files(paths_list, group_label):
    reversal_durations = []

    for file_path in paths_list:
        df = pd.read_excel(file_path)
        df['Numeric Durations'] = pd.to_numeric(df['Duration (seconds)'], errors='coerce')
        df = df.dropna(subset=['Numeric Durations'])  # Keep only valid numeric reaction times
        df['Group'] = group_label  # Assign group label
        reversal_durations.append(df[['Numeric Durations', 'Group']])

    return pd.concat(reversal_durations)

# Process data for each group
group_1_data = process_files(rev_duration_paths_list1, 'ATR+')
group_2_data = process_files(rev_duration_paths_list2, 'ATR-')

# Process each group and append to the all_data DataFrame
all_data = pd.concat([group_1_data, group_2_data], ignore_index=True)

# Statistical Comparison
stat, p_value = ttest_ind(
    all_data[all_data['Group'] == 'ATR+']['Numeric Durations'], 
    all_data[all_data['Group'] == 'ATR-']['Numeric Durations'],
    equal_var=False
)

plt.figure(figsize=(12, 8))
boxplot = sns.boxplot(x='Group', y='Numeric Durations', data=all_data, palette='Set2', showfliers=False)
sns.stripplot(x='Group', y='Numeric Durations', data=all_data, color='black', alpha=0.5, jitter=True)

# Calculate the sample size for each group
sample_sizes = all_data.groupby('Group').size().reset_index(name='Sample Size')

# Annotate with the sample sizes
for i, (group, sample_size) in enumerate(zip(sample_sizes['Group'], sample_sizes['Sample Size'])):
    x_position = i
    y_position = all_data['Numeric Durations'].quantile(0.75) + (all_data['Numeric Durations'].quantile(0.75) * 5.3)  # Adjust this based on your data
    plt.text(x_position, y_position, f'N={sample_size}', 
             horizontalalignment='center', size='medium', color='black', weight='semibold',
             bbox=dict(facecolor='white', alpha=0.5))

plt.title('Comparison of Reversal Durations Between Groups')
plt.xlabel('Experimental Group')
plt.ylabel('Reversal Timeframe (seconds)')
plt.ylim(all_data['Numeric Durations'].min(), all_data['Numeric Durations'].max() * 1.1)  # Adjust ylim to fit annotations
plt.tight_layout()
plt.show()