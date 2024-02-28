import matplotlib.cm as cm
import matplotlib as mpl
mpl.use('Agg') # this turns of X server to run on the cluster which has not display
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import colors
import pandas as pd
import numpy as np
import os
import glob



def plot_main_figure(nrows, ncols):
    """Function to plot the main behavioural features of a single worm behavioral recording
    input:
    project_folder
    """

    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(nrows, ncols, figure=fig)

    #kymogram
    # ax1 = fig.add_subplot(gs[0, :])
    #
    # ax2 = fig.add_subplot(gs[1, :5])


    return fig, gs

def plot_ethogram(etho_path, axes):
    """
    Note: plot_kymogram.py exists in curvature package. At the moment it is not using this function. Maybe this fucntion should go there.
    :param project_path:
    :param fig:
    :param axes:
    :return:
    """
    #kymo_path = os.path.join(project_path, 'skeleton_spline_K.csv')
    try:
        df_etho = pd.read_csv(etho_path, index_col=0)
        num_frames = len(df_etho)
        num_lines = 2
        cut_frames = num_frames // num_lines
        # df_etho = df_etho.rolling(100, center=True, min_periods=10).mean()
        fig, axs = plt.subplots(num_lines, 1, dpi=400, figsize=(10, 1*num_lines))

        for i, ax in enumerate(axs):
            start_idx = i * cut_frames
            end_idx = start_idx + cut_frames
            ax.imshow(df_etho.iloc[start_idx:end_idx].T, origin="upper", cmap='seismic_r', aspect=20*100, vmin=-0.06, vmax=0.06)
            ax.set_xticks(np.linspace(0, cut_frames, 5))
            ax.set_xticklabels(np.linspace(start_idx, end_idx, 5).astype(int))
            if i == num_lines - 1:
                ax.set_xlabel('Frame')            
            ax.set_ylabel('Beh. State')

            # Add the legend
            if i == 0:
                from matplotlib.lines import Line2D
                legend_elements = [Line2D([0], [0], color='red', label='Reversal'),
                                   Line2D([0], [0], color='blue', label='Forward motion')]
                ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.1, 1), frameon=True)

        plt.tight_layout()
        #plt.show()
        
    except:
        print('problem reading the kymograph csv file')

    return axes


if __name__ == '__main__':
    import argparse


    # TODO: add beh annotation in speed plot
    # add head speed, total curvature, PC1, PC2, PC3, etc. See notebook wbfm_analysis
    # TODO: make it for every worm

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-i', '--input_path', help='folder with the tracker position', required=True)

    args = vars(parser.parse_args())
    main_folder = args['input_path']

    #main_folder = "/Volumes/scratch/neurobiology/zimmer/ulises/wbfm/20221127/data/ZIM2165_Gcamp7b_worm1"

    #OLD PARSER
    # parser.add_argument('-i', '--input_path', help='', required=True)
    # parser.add_argument('-k', '--kymo_path', help='', required=True)
    # parser.add_argument('-pcs', '--pcs_path', help='', required=True)
    # parser.add_argument('-stage', '--stage_path', help='', required=True)
    # parser.add_argument('-beh', '--beh_annotation_path', help='', required=True)
    # parser.add_argument('-speed', '--raw_worm_speed_path', help='', required=True)


    #TO RUN LOCALLY (with debugger)
    # main_folder = "/Volumes/scratch/neurobiology/zimmer/ulises/wbfm/20221210/data/ZIM2165_Gcamp7b_worm3"

    #main_folder="/Volumes/scratch/neurobiology/zimmer/ulises/wbfm/20221127/data/ZIM2165_Gcamp7b_worm1/"

    #ALL
    # project_folder = glob.glob(os.path.join(main_folder, "*w*_Ch0"))[0]
    project_folder = main_folder
    print("project folder is: ", project_folder)

    #Start Figure
    fig, gs = plot_main_figure(nrows=7, ncols=10)

    #Set size
    fig.set_size_inches(11.69, 8.27)  # Use if you need to put on A4
    # fig.set_size_inches(11.69, 4.13)  # Use if you need other formats

    #Ethogram
    ax1 = fig.add_subplot(gs[4, :-2])
    etho_path = glob.glob(os.path.join(project_folder, 'beh_annotation0.csv'))[0]
    print(etho_path)
    plot_ethogram(etho_path, axes=ax1)
    ax1.set_ylabel('Beh. State')
    ax1.set_xlabel('Frames')    

    plt.savefig(os.path.join(project_folder, 'ethogram.png'), dpi=500)
    #plt.show()

    print('end of script')
