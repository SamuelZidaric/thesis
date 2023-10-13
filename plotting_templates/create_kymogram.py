import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

main_path='Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli_ero/data/'
#main_path="/Users/ulises.rey/local_data/local_spline_files_20230124"

kymo_paths=glob.glob(os.path.join(main_path,'w5/*Ch0*/*skeleton_spline_K.csv'))
#kymo_paths=glob.glob(os.path.join(main_path,'*12-10*2319*worm3*skeleton_spline_K.csv'))

nan_centerlines = []

for kymo_path in kymo_paths:
    print(kymo_path)
    
    try:
        df_kymo = pd.read_csv(kymo_path, header=None)
        print(df_kymo.shape)
        fig, axes = plt.subplots(dpi=400, figsize=(40, 4))
        fig.suptitle(os.path.basename(kymo_path))
        df_kymo = df_kymo.rolling(100, center=True, min_periods=10).mean()
        
        axes.imshow(df_kymo.T, origin="upper", cmap='seismic', extent=[0, df_kymo.shape[0], df_kymo.shape[1], 0],
                    aspect=20, vmin=-0.06, vmax=0.06)

        # Plot the transition points as black dots on the top border of the image
        axes.scatter(transition_points, [0]*len(transition_points), color='black', s=5)

        # Decorate figure
        axes.set_xlabel('Volume')
        axes.set_ylabel('Body Part')
        plt.show()
        
    except:
        print('problem reading the kymograph csv file')

df_kymo=pd.read_csv(r"Z:\neurobiology\zimmer\zidaric\data\pre_neg_uli_ero\data\w5\2023_09_01_13_19_loop_activation_atr_neg_wrm5_sam_image_stack_Ch0\skeleton_spline_K.csv", header=None)
plt.imshow(df_kymo.loc[0:144000].T, origin="upper", cmap='seismic', aspect=50, vmin=-0.06, vmax=0.06)
plt.show()
