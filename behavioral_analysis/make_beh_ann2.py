import os

def make_beh_ann2(beh_ann2_path, project_folder):
    with open(beh_ann2_path, 'r') as f:
        lines = f.readlines()

    offset = 0
    while offset < len(lines):
            start_i = offset + 2400 - 1
            end_i = offset + 2640

            for i in range(start_i, end_i):
                if i < len(lines):
                     parts = lines[i].strip().split(',') # Splitting line by comma
                     if len(parts) > 1:                  # Checking if there's at least two columns
                          parts[1] = '3'                  # Modifying the B column
                     lines[i] = ','.join(parts) + '\n'   # Joining parts back together
            
            offset += 2560

    # Setting output filename based on the original filename but in the provided project folder
    output_path = os.path.join(project_folder, "beh_annotation2.csv")

    with open(output_path, 'w') as f:
        f.writelines(lines)

    print(f"Modified CSV saved at: {output_path}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-i', '--input_path', help='folder with the tracker position', required=True)

    args = vars(parser.parse_args())
    main_folder = args['input_path']

    project_folder = main_folder

    beh_ann2_path = os.path.join(project_folder, "beh_annotation1.csv")

    make_beh_ann2(beh_ann2_path, project_folder)