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

def gather_already_reversing_instances(file_paths, group_label):
    reversing_instances = []  # List to hold 'Already reversing' instances and group labels
    
    for file_path in file_paths:
        df = pd.read_excel(file_path)
        # Assuming 'Already reversing' is a category in 'Status/Reaction Time'
        already_reversing = df[df['Status/Reaction Time'] == 'Already Reversing']
        already_reversing['Group'] = group_label  # Assign group label
        reversing_instances.append(already_reversing[['Status/Reaction Time', 'Group']])
    
    return pd.concat(reversing_instances)

# Gather 'Already reversing' instances for each group
group_1_reversing = gather_already_reversing_instances(rev_reaction_paths_list1, 'ATR+')
group_2_reversing = gather_already_reversing_instances(rev_reaction_paths_list2, 'ATR-')

# Combine instances from both groups
all_reversing_instances = pd.concat([group_1_reversing, group_2_reversing], ignore_index=True)

plt.figure(figsize=(12, 8))

# Create the countplot
countplot = sns.countplot(x='Group', data=all_reversing_instances, palette='Set2')

# Get the current axis of the plot
ax = plt.gca()

# Calculate the count for each group
group_counts = all_reversing_instances['Group'].value_counts().reset_index(name='Count')
group_counts.columns = ['Group', 'Count']
group_counts = group_counts.sort_values(by='Group')  # Sort to ensure the order matches the plot

# Annotate the countplot with the counts
for p, count in zip(ax.patches, group_counts['Count']):
    # The bar's width and position can be used to place text properly
    x_position = p.get_x() + p.get_width() / 2
    y_position = p.get_height() + 3  # Small offset above the bar
    ax.text(x_position, y_position, f'n = {count}', 
            ha='center', va='bottom', color='black', weight='semibold')

plt.title('Comparison of "Already Reversing" Instances Between ATR+ and ATR- Groups')
plt.ylabel('Count')
plt.xlabel('Experimental Group')
plt.ylim(0, max(group_counts['Count'])*1.1)  # Set y limit higher to accommodate text

plt.tight_layout()
plt.show()


