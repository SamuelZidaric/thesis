import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import os
import glob

main_path='Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli_ero/data/'

kymo_paths=glob.glob(os.path.join(main_path,'w5/*Ch0*/*skeleton_spline_K.csv'))

for kymo_path in kymo_paths:
    print(kymo_path)
    
    try:
        df_kymo = pd.read_csv(kymo_path, header=None)
        num_frames = len(df_kymo)
        num_lines = 4
        cut_frames = num_frames // num_lines
        df_kymo = df_kymo.rolling(100, center=True, min_periods=10).mean()
        fig, axs = plt.subplots(num_lines, 1, dpi=400, figsize=(10, 1*num_lines))

        for i, ax in enumerate(axs):
            start_idx = i * cut_frames
            end_idx = start_idx + cut_frames
            ax.imshow(df_kymo.iloc[start_idx:end_idx].T, origin="upper", cmap='seismic', aspect=20, vmin=-0.06, vmax=0.06)
            ax.set_xticks(np.linspace(0, cut_frames, 5))
            ax.set_xticklabels(np.linspace(start_idx, end_idx, 5).astype(int))
            if i == num_lines - 1:
                ax.set_xlabel('Frame')            
            ax.set_ylabel('Body Part') 

        plt.tight_layout()
        plt.show()
    
    except:
        print('problem reading the kymograph csv file')
