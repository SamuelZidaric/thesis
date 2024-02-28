import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import glob

# path_rev_duration_all = '/Users/fabio/Documents/PhD/Neuro/supervision/sam/data/rev_duration_all.xlsx'
# rev_reaction = '/Users/fabio/Documents/PhD/Neuro/supervision/sam/data/rev_reaction.xlsx'

main_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'
rev_reaction_paths_list: list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))
path_rev_duration_all_list: list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_duration_all.xlsx'))

triggered_rev_durations_10 = []
non_triggered_rev_durations_10 = []
len_df_10 = []

for nr in range(len(rev_reaction_paths_list)):

    window_triggers = pd.read_excel(rev_reaction_paths_list[nr])
    rev_duration_all_pd = pd.read_excel(path_rev_duration_all_list[nr])
    # read 2nd : 4th columns
    window_triggers = window_triggers.iloc[:-1, 1:4]
    rev_duration_all = rev_duration_all_pd.iloc[:, 1:4]
    len_df_10.append(len(rev_duration_all))
    # delete the rows which contain the string 'Already Reversing' in the fourth column
    window_triggers = window_triggers[~window_triggers.iloc[:, 2].str.contains('Already Reversing', na=False)]
    # print(f"window_triggers: {window_triggers}")

    frame_windows = np.array(window_triggers.iloc[:, 0:2])
    print(f"frame_windows: {frame_windows}")

    triggered_rev_durations = []
    non_triggered_rev_durations = []

    # if the frame number of the first column of rev_duration_all is within the range of the first and second column
    # of frame_windows -> append to triggered_rev_durations

    for i in range(len(frame_windows)):
        for j in range(len(rev_duration_all)):
            if frame_windows[i, 0] <= rev_duration_all.iloc[j, 0] <= frame_windows[i, 1]:
                triggered_rev_durations.append(rev_duration_all.iloc[j, 2])
                
            # else:
                # non_triggered_rev_durations.append(rev_duration_all.iloc[j, 2])


    # delete all rows of non_triggered_rev_durations which occur more than once
    non_triggered_rev_durations = list(set(non_triggered_rev_durations))
    # remove all durations from non_triggered_rev_durations which are not in triggered_rev_durations
    non_triggered_rev_durations = [x for x in non_triggered_rev_durations if x not in triggered_rev_durations]

    print(f"length of triggered_rev_durations: {len(triggered_rev_durations)}")
    print(f"length of non_triggered_rev_durations: {len(non_triggered_rev_durations)}")

    # print(f"triggered_rev_durations: {triggered_rev_durations}")
    # print(f"non_triggered_rev_durations: {non_triggered_rev_durations}")

    print(f"average, min, max of triggered_rev_durations: {np.mean(triggered_rev_durations)}, {np.min(triggered_rev_durations)}, {np.max(triggered_rev_durations)}")
    print(f"average, min, max of all rev_durations: {np.mean(rev_duration_all.iloc[:, 2])}, {np.min(rev_duration_all.iloc[:, 2])}, {np.max(rev_duration_all.iloc[:, 2])}")
    print(f"first, second and third quartile of triggered_rev_durations: {np.percentile(triggered_rev_durations, [25, 50, 75])}")
    print(f"first, second and third quartile of all rev_durations: {np.percentile(rev_duration_all.iloc[:, 2], [25, 50, 75])}")

    triggered_rev_durations_10.append(triggered_rev_durations)
    non_triggered_rev_durations_10.append(non_triggered_rev_durations)

print(f'length of triggered_rev_durations_10: {len(triggered_rev_durations_10)}')
print(f'length of non_triggered_rev_durations_10: {len(non_triggered_rev_durations_10)}')

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
ax.hist(flattened_triggered_rev_durations_10, bins=30, alpha=0.5, color='blue', label=f'stimulated ($n$ = {len(flattened_triggered_rev_durations_10)})', histtype="stepfilled", density=True, )
ax.hist(flattened_non_triggered_rev_durations_10, bins=30, alpha=0.5, color='red', label=f'stochastic ($n$ = {len(flattened_non_triggered_rev_durations_10)})', histtype="stepfilled", density=True, )
plt.legend(loc='upper right')
plt.xlabel('Reversal Duration (sec)')
plt.ylabel('Density')
#ax.set_yscale('log')

# Draw vertical lines for median values
ax.axvline(median_triggered, color='blue', linestyle='--', linewidth=2, label=f'Median Stimulated: {median_triggered:.1f}')
ax.axvline(median_non_triggered, color='red', linestyle='--', linewidth=2, label=f'Median Stochastic: {median_non_triggered:.1f}')

# title
plt.title('Duration of Triggered and Stochastic Reversals (ATR+)')
plt.show()


# # draw figure with violin plot instead of histograms
# fig, ax = plt.subplots()
# sns.violinplot(data=[triggered_rev_durations, non_triggered_rev_durations], ax=ax)
# # label groups on x-axis
# ax.set_xticklabels(['stimulated', 'stochastic'])
# plt.ylabel('Reversal Duration (sec)')
# plt.show()



