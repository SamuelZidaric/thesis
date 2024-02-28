# This script processes TIFF images by segmenting, cropping, and analyzing frames based on regions of interest (ROIs). 

import os
import tifffile
import numpy as np
from skimage import measure
import argparse
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def process_frame(frame, crop_size):
    crop_width, crop_height = crop_size

    # Segment the image
    labeled_frame = measure.label(frame)
    regions = measure.regionprops(labeled_frame)

    if not regions:
        print("No regions found. Returning a blank frame.")
        return np.zeros(crop_size, dtype=frame.dtype), 0, 0

    # Sort regions by area and get the largest
    largest_region = max(regions, key=lambda r: r.area)

    # Get the centroid of the largest region
    centroid_y, centroid_x = largest_region.centroid

    # Calculate the top-left corner of the crop area, ensuring it doesn't go out of bounds
    start_x = int(max(min(centroid_x - crop_width // 2, frame.shape[1] - crop_width), 0))
    start_y = int(max(min(centroid_y - crop_height // 2, frame.shape[0] - crop_height), 0))

    # Crop the frame
    cropped_frame = frame[start_y:start_y + crop_height, start_x:start_x + crop_width]

    return cropped_frame, start_x, start_y

def crop_tiff(path, output_path, crop_size):
    print(f"Cropping: {path}")

    x_roi_data = []
    y_roi_data = []

    with tifffile.TiffFile(path) as tif:
        total_frames = len(tif.pages)
        cropped_data = []

        for i in range(total_frames):
            frame = tif.asarray(key=i)
            result = process_frame(frame, crop_size)
            if result is None:
                # Handle empty frame case - e.g., skip or use a blank frame
                blank_frame = np.zeros(crop_size, dtype=np.uint8)
                cropped_data.append(blank_frame)
                continue
            cropped_frame, start_x, start_y = result
            cropped_data.append(cropped_frame)
            x_roi_data.append(start_x)
            y_roi_data.append(start_y)

        # Ensuring all frames have the same size and type
        uniform_cropped_data = np.stack([np.asarray(frame, dtype=np.uint8) for frame in cropped_data])

        tifffile.imsave(output_path, uniform_cropped_data, bigtiff=True)

    return x_roi_data, y_roi_data


def save_to_excel(x_roi_data, y_roi_data, excel_file):
    # Create a DataFrame with the appropriate column names
    df = pd.DataFrame({
        'x_roi': x_roi_data,
        'y_roi': y_roi_data
    })

    # Ensure the file ends with '.xlsx'
    if not excel_file.endswith('.xlsx'):
        excel_file += '.xlsx'

    # Save the DataFrame to an Excel file
    df.to_excel(excel_file, index=False)
    print(f"ROI data saved to {excel_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="crop_worm_from_binary_mask_tiff")
    parser.add_argument("--binary_stack", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--crop_size", required=True, help="Crop size in format 'width,height'")
    parser.add_argument("--excel_file", required=True, help="Output Excel file to store ROI data")
    args = parser.parse_args()

    path = args.binary_stack
    output = args.output
    excel_file = args.excel_file
    crop_size = tuple(map(int, args.crop_size.split(',')))
    search_margin = 50  # Define how far from the last known position to search, adjust as needed

    print(f"Excel file path: {excel_file}")
    print("Processing TIFF...")
    x_roi_data, y_roi_data = crop_tiff(path, output, crop_size)
    
    print("Saving ROI data to Excel file...")
    save_to_excel(x_roi_data, y_roi_data, excel_file)
