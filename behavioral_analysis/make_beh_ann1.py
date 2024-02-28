import os
import pandas as pd
import numpy as np

def categorize_value(x):
    """Categorize the value into 1, 0, or -1."""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def modify_csv(beh_ann1_path, project_folder):
    threshold = 50

    # Read the CSV file using pandas, assuming no header
    df = pd.read_csv(beh_ann1_path, header=None)

    # Ensure initial values are 1, 0, or -1
    df[1] = df[1].apply(categorize_value)

    # Perform the rolling mean operation
    df[1] = df[1].rolling(window=50, min_periods=1).mean()

    # Categorize the rolling mean results into 1, 0, or -1
    df[1] = df[1].apply(categorize_value)

    # Apply the majority filtering from the first script
    for i in range(1, len(df)):  # Start from 1 to skip the header row
        window = df[1].iloc[max(i - threshold, 1):min(i + threshold, len(df))]
        majority = window.mode()[0]
        if len(window[window == df[1].iloc[i]]) < threshold:
            df[1].iloc[i] = majority

    # Define the output file path
    output_file = os.path.join(project_folder, "beh_annotation1.csv")

    # Write the modified dataframe to a new CSV file
    df.to_csv(output_file, header=False, index=False)
    print(f"Modified CSV saved at: {output_file}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Modify behavior annotation CSV file')
    parser.add_argument('-i', '--input_path', help='Input CSV file path', required=True)

    args = vars(parser.parse_args())
    main_folder = args['input_path']

    project_folder = main_folder

    beh_ann1_path = os.path.join(project_folder, "beh_annotation0.csv")

    modify_csv(beh_ann1_path, project_folder)

