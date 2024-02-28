# Extracting a single frame from the original 'raw_stack.btf' file for use in creating the average background (AVG_background)

import tifffile
import argparse
import os

def crop_tiff(input_path, output_path, frame):
    print(f"Cropping frame {frame} from: {input_path}")

    # Check if output directory exists, create if not
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with tifffile.TiffFile(input_path) as tif:
        # Check if the frame is within the range of available frames
        total_frames = len(tif.pages)
        if frame >= total_frames:
            raise ValueError("The specified frame is beyond the total number of frames in the file.")

        # Read the specified frame
        data = tif.asarray(key=frame)

        # Save the extracted frame to the specified output file
        tifffile.imsave(output_path, data, bigtiff=True)

    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a single frame from a BTF file")
    parser.add_argument("--raw_img", required=True, help="Path to the BTF file")
    parser.add_argument("--frame", type=int, required=True, help="Frame number to extract")
    parser.add_argument("--output", required=True, help="Path for the output BTF file")
    args = parser.parse_args()

    crop_tiff(args.raw_img, args.output, args.frame)
