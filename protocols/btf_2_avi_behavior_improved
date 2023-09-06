import shutil  # Unused import, consider removing
import os
import argparse

from video_conversions.avi.tiff2avi import tiff2avi, tiff2avi_full_directory  # Importing tiff2avi functions

def convert_behavior_folder_to_avi(root_folder, folder_ext="_sam", fps=80, fourcc="MJPG"):
    print("Converting .btf to .avi")
    
    # Determine whether the root folder itself is a behavior folder
    is_beh_folder = root_folder.endswith(folder_ext)
    
    if is_beh_folder:
        beh_folder = [root_folder]
    else:
        folder_list = os.listdir(root_folder)
        beh_folder = [os.path.join(root_folder, folder) for folder in folder_list if folder.endswith(folder_ext)]

    if not beh_folder:
        print(f"Error: Couldn't find any folders ending with {folder_ext} in {root_folder}.")
        return

    for folder in beh_folder:
        files = os.listdir(folder)
        
        # Filter for .btf files in the current folder
        btf_files = [os.path.join(folder, file) for file in files if file.endswith(".btf")]

        # Initialize to None
        btf_file = None
        
        # Error detection: Check if .btf files exist in the folder
        if len(btf_files) > 0:
            btf_file = btf_files[0]
            print(f"Found .btf file: {btf_file}")
            avi_path = btf_file.replace(".btf", ".avi")
        else:
            print(f"Error: No .btf files found in {folder}.")
            
        if btf_file:
            tiff2avi(tiff_path=btf_file, avi_path=avi_path, fps=fps, fourcc=fourcc, alpha=1.0)
        else:
            print("No .btf file found, converting an ome.tiff folder instead")
            sorting_options = dict(regex_str=r'MMStack_[0-9]{1,}', index_for_no_match=0)
            tiff2avi_full_directory(input_folder=beh_folder, fps=fps, output_folder=beh_folder, fourcc=fourcc, alpha=1.0, sorting_options=sorting_options)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default='.', help='The directory to be processed')
    parser.add_argument('--path', default='.', help='path to the main recording folder')
    parser.add_argument('--ext', default='_sam', help='ending string to find the relevant sub folder')
    parser.add_argument('--fps', default=80, help='fps of movie')
    parser.add_argument('--fourcc', default='MJPG', help='compression, default MJPG')
    args = parser.parse_args()

    print(f"Processing directory: {args.directory}")

    convert_behavior_folder_to_avi(root_folder=args.path, folder_ext=args.ext, fps=args.fps, fourcc=args.fourcc)
