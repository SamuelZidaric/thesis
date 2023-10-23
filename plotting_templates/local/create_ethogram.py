import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

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

main_path='Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'

etho_paths=glob.glob(os.path.join(main_path,'w5/*Ch0*/*beh_annotation.csv'))
print(etho_paths)
print(len(etho_paths))

final_title = etho_paths[0].split('\\')[-2]
print(final_title)

for etho_path in etho_paths:
    print(etho_path)
    
    try:
        df_etho = pd.read_csv(etho_path, index_col=0) 
        df_etho = filter_short_changes(df_etho, 40)
        num_frames = len(df_etho)
        num_lines = 4
        cut_frames = num_frames // num_lines
        df_etho = df_etho.rolling(100, center=True, min_periods=10).mean()
        fig, axs = plt.subplots(num_lines, 1, dpi=400, figsize=(10, 1*num_lines))
        fig.suptitle(final_title)


        for i, ax in enumerate(axs):
            start_idx = i * cut_frames
            end_idx = start_idx + cut_frames
            ax.imshow(df_etho.iloc[start_idx:end_idx].T, origin="upper", cmap='seismic_r', aspect=20*100, vmin=-0.06, vmax=0.06)
            ax.set_xticks(np.linspace(0, cut_frames, 5))
            ax.set_xticklabels(np.linspace(start_idx, end_idx, 5).astype(int))
            if i == num_lines - 1:
                ax.set_xlabel('Frames')            
            ax.set_ylabel('Beh. State')

        # Add the legend
        if i == 0:
            from matplotlib.lines import Line2D
            legend_elements = [Line2D([0], [0], color='red', label='Reversal'),
                               Line2D([0], [0], color='blue', label='Forward motion')]
            ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), frameon=True)

        plt.tight_layout()
        plt.show()
        
    except:
        print('problem reading the csv file')
