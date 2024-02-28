import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

main_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'
rev_reaction_paths_list: list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))
path_rev_duration_all_list: list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_duration_all.xlsx'))


triggered_rev_durations_10 = []
non_triggered_rev_durations_10 = []
len_df_10 = []

for nr in range(len(rev_reaction_paths_list)):
    print(nr)
    window_triggers = pd.read_excel(rev_reaction_paths_list[nr])
    rev_duration_all_pd = pd.read_excel(path_rev_duration_all_list[nr])
    
    # Preprocess window_triggers and rev_duration_all_pd as needed
    window_triggers = window_triggers.iloc[:-1, 1:4]
    
    # Ensure the column is treated as string before applying .str.contains()
    window_triggers.iloc[:, 2] = window_triggers.iloc[:, 2].astype(str)
    
    window_triggers = window_triggers[~window_triggers.iloc[:, 2].str.contains('Already Reversing', na=False)]
    print('hi1')
    window_triggers = window_triggers[~window_triggers.iloc[:, 2].str.contains('No Reversal', na=False)]
    print('hi2')
    window_triggers = window_triggers[~window_triggers.iloc[:, 2].str.contains('No movement', na=False)]
    print('hi3')
    
    rev_duration_all = rev_duration_all_pd.iloc[:, 1:4]
    len_df_10.append(len(rev_duration_all))
    
    frame_windows = np.array(window_triggers.iloc[:, 0:2])
    
    triggered_rev_durations = []
    all_rev_durations = list(rev_duration_all.iloc[:, 2])

    for j in range(len(rev_duration_all)):
        rev_start = rev_duration_all.iloc[j, 0]
        if any(frame_windows[i, 0] <= rev_start <= frame_windows[i, 1] for i in range(len(frame_windows))):
            triggered_rev_durations.append(rev_duration_all.iloc[j, 2])
    
    # Now, identify non-triggered reversals as those not in triggered_rev_durations
    non_triggered_rev_durations = [dur for dur in all_rev_durations if dur not in triggered_rev_durations]

    # Proceed with your calculations and plotting as before
    # (No changes needed in this part of the script)
    triggered_rev_durations_10.append(triggered_rev_durations)
    non_triggered_rev_durations_10.append(non_triggered_rev_durations)


flattened_triggered_rev_durations_10 = [item for sublist in triggered_rev_durations_10 for item in sublist]
flattened_non_triggered_rev_durations_10 = [item for sublist in non_triggered_rev_durations_10 for item in sublist]

print(f'length of flattened_triggered_rev_durations_10: {len(flattened_triggered_rev_durations_10)}')
print(f'length of flattened_non_triggered_rev_durations_10: {len(flattened_non_triggered_rev_durations_10)}')

print(f'\n')
print(len_df_10)
len_df_10_ar = np.array(len_df_10)
sum_len_ar_10 = np.sum(len_df_10_ar)
print(f'sum of all rows of rev duration all: {sum_len_ar_10}')

# Calculate median values
median_triggered = np.median(flattened_triggered_rev_durations_10)
median_non_triggered = np.median(flattened_non_triggered_rev_durations_10)


# draw one figure with 2 histograms of triggered and all rev_durations
fig, ax = plt.subplots()
ax.hist(flattened_triggered_rev_durations_10, bins=30, alpha=0.5, color='blue', label=f'stimulated ($n$ = {len(flattened_triggered_rev_durations_10)})', histtype="stepfilled", density=True)
ax.axvline(median_triggered, color='blue', linestyle='--', linewidth=2, label=f' median: {median_triggered:.1f} sec')

ax.hist(flattened_non_triggered_rev_durations_10, bins=30, alpha=0.5, color='red', label=f'stochastic ($n$ = {len(flattened_non_triggered_rev_durations_10)})', histtype="stepfilled", density=True)
ax.axvline(median_non_triggered, color='red', linestyle='--', linewidth=2, label=f' median : {median_non_triggered:.1f} sec')


plt.xlabel('Reversal Duration [sec]')
plt.ylabel('Probability Density')
plt.title('Duration of Triggered and Stochastic Reversals (ATR+)')

# Make sure to call plt.legend() after plotting all elements to include them in the legend
plt.legend(loc='upper right')

plt.show()


