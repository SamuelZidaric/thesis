import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Agg') # this turns of X server to run on the cluster which has not display
import pandas as pd
import os
import glob
import argparse
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle


# def filter_short_changes(df, threshold=40):
#     in_change = False
#     start_idx = None 
#     for i, value in enumerate(df['0']):
#         if value == -1 and not in_change:
#             in_change = True
#             start_idx = i
#         elif value == 1 and in_change:
#             in_change = False
#             if i - start_idx < threshold:
#                 df['0'].iloc[start_idx:i] = 1
#     return df

def plot_ethogram(etho_path, beh2_path, axes):
    """
    Function to plot ethogram based on given paths.
    """
    try:
        df_etho = pd.read_csv(etho_path, index_col=0) 
        #df_etho = filter_short_changes(df_etho, 40)

        beh2_path = etho_path.replace('beh_annotation1.csv', 'beh_annotation2.csv')
        df_etho2 = pd.read_csv(beh2_path, index_col=0)
        
        num_frames = len(df_etho)
        num_lines = 2
        cut_frames = num_frames // num_lines
        #df_etho = df_etho.rolling(100, center=True, min_periods=10).mean()
        
        fig, axs = plt.subplots(num_lines, 1, dpi=400, figsize=(10, 1*num_lines))
        
        # TODO: Define 'final_title' or remove if not required
        #fig.suptitle('Provide Title Here or Define final_title elsewhere')

        for i, ax in enumerate(axs):
            start_idx = i * cut_frames
            end_idx = start_idx + cut_frames
            
            ax.imshow(df_etho.iloc[start_idx:end_idx].T, origin="upper", cmap='seismic_r', aspect=20*100, vmin=-0.06, vmax=0.06)
            
            # Overlay from the beh_annotation2.csv file
            mask = df_etho2['0'].iloc[start_idx:end_idx] == 3
            square_height = 0.3 # adjust this to control the height of the square
            y_position = 0.25 # adjust this to control the vertical position of the square

            for x in np.where(mask)[0]:
                rect = Rectangle((x, y_position - 0.4), width=1, height=square_height, color='#90EE90')
                ax.add_patch(rect)            
            ax.set_xticks(np.linspace(0, cut_frames, 5))
            ax.set_xticklabels(np.linspace(start_idx, end_idx, 5).astype(int))
            ax.set_xlabel('Frames')
            ax.set_ylabel('Beh. State')

            # Add the legend
            if i == 0:
                from matplotlib.lines import Line2D
                legend_elements = [Line2D([0], [0], color='red', label='Reversal'),
                                   Line2D([0], [0], color='blue', label='Forward motion'),
                                   Line2D([0], [0], marker='s', color='#90EE90', label='LED light', markerfacecolor='green', markersize=10)]
                ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.1, 1), frameon=True)

        plt.tight_layout()
        #plt.show()

    except Exception as e:
        print(f'Error occurred during plotting: {e}')

    return axes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-i', '--input_path', help='folder with the tracker position', required=True)

    args = vars(parser.parse_args())
    main_folder = args['input_path']

    project_folder = main_folder
    print("project folder is: ", project_folder)

    # TODO: Define plot_main_figure or remove if not required
    fig = plt.figure(figsize=(11.69, 8.27))
    gs = plt.GridSpec(7, 10, figure=fig)


    ax1 = fig.add_subplot(gs[4, :-2])
    etho_path = glob.glob(os.path.join(project_folder, 'beh_annotation1.csv'))[0]
    beh2_path = glob.glob(os.path.join(project_folder, 'beh_annotation2.csv'))[0]
    
    plot_ethogram(etho_path, beh2_path, axes=ax1)

    plt.savefig(os.path.join(project_folder, 'ethogram_led.png'), dpi=500)

    print('end of script')

