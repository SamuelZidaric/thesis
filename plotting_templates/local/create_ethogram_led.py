import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import re
import matplotlib.colors as mcolors


def filter_short_changes(df, threshold=40):
    in_change = False
    start_idx = None 
    for i, value in enumerate(df['0']):
        if value == -1 and not in_change:
            in_change = True
            start_idx = i
        elif value == 1 and in_change:
            in_change = False
            if i - start_idx < threshold:
                df['0'].iloc[start_idx:i] = 1
    return df

# Create a custom colormap
# colors = {'0': '#000066', '1': '#000066','-1': '#CC0000', '2': '#000066', '3': '#90EE90'}
# cmap = mcolors.LinearSegmentedColormap.from_list("", [colors[str(i)] for i in range(-1, 4)])

main_path='Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'

etho_paths=glob.glob(os.path.join(main_path,'w5/*Ch0*/*beh_annotation.csv'))
print(etho_paths)
print(len(etho_paths))

final_title = etho_paths[0].split('\\')[-2]
print(final_title)

for etho_path in etho_paths:
    print(etho_path)
    
    try:
        # Reading 'beh_annotation.csv'
        df_etho = pd.read_csv(etho_path, index_col=0) 
        df_etho = filter_short_changes(df_etho, 40)

        # Reading 'beh_annotation2.csv'
        beh2_path = etho_path.replace('beh_annotation.csv', 'beh_annotation2.csv')
        df_etho2 = pd.read_csv(beh2_path, index_col=0)
        num_frames = len(df_etho)
        num_lines = 4
        cut_frames = num_frames // num_lines
        df_etho = df_etho.rolling(100, center=True, min_periods=10).mean()
        fig, axs = plt.subplots(num_lines, 1, dpi=400, figsize=(10, 1*num_lines))
        fig.suptitle(final_title)

        for i, ax in enumerate(axs):
            start_idx = i * cut_frames
            end_idx = start_idx + cut_frames
            #ax.imshow(df_etho.iloc[start_idx:end_idx].T, origin="upper", cmap=cmap, aspect=20*100, vmin=-0.06, vmax=0.06)
            ax.imshow(df_etho.iloc[start_idx:end_idx].T, origin="upper", cmap='seismic_r', aspect=20*100, vmin=-0.06, vmax=0.06)

            # Overlay the '3' values from the beh_annotation2.csv file
            mask = df_etho2['0'].iloc[start_idx:end_idx] == 3
            ax.scatter(np.where(mask)[0], [0] * mask.sum(), color='#90EE90', marker='s')

            ax.set_xticks(np.linspace(0, cut_frames, 5))
            ax.set_xticklabels(np.linspace(start_idx, end_idx, 5).astype(int))
            if i == num_lines - 1:
                ax.set_xlabel('Frames')            
            ax.set_ylabel('Beh. State')

            # Add the legend
            if i == 0:
                from matplotlib.lines import Line2D
                legend_elements = [Line2D([0], [0], color='red', label='Reversal'),
                                   Line2D([0], [0], color='blue', label='Forward motion'),
                                   Line2D([0], [0], marker='s', color='#90EE90', label='LED light',
                                          markerfacecolor='green', markersize=10)]
                ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), frameon=True)

        plt.tight_layout()
        plt.show()
        
    except:
        print('problem reading the kymograph csv file')
