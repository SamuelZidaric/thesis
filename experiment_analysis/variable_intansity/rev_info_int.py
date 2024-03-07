import pandas as pd
import os
import glob
import numpy as np

main_path = 'Z:/neurobiology/zimmer/zidaric/data/uli_pip/int_neg/data/'

# Mapping for Activation numbers to specific intensity values
subdivision_values = [60, 0, 40, 10, 80, 20, 40, 10, 60, 20, 80, 0, 40, 60, 80, 20, 10, 0, 60, 40, 20, 80, 0, 10, 60, 40, 80, 0, 10, 20]

# Function to perform data analysis for each intensity level and save the output
def perform_data_analysis_by_subgroup_and_save(main_path):
    # Paths to find files
    rev_reaction_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))
    rev_duration_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_duration_all.xlsx'))

    # Initialize a dictionary to hold data for each intensity level
    data_by_intensity = {value: {
                        'all_reaction_times': [],
                        'status_counts': pd.Series(dtype='int'),
                        'induced_reversal_durations': []  # This will be used for durations from rev_reaction.xlsx
                    } for value in set(subdivision_values)}

    # Process each rev_reaction file for intensity-based data
    for path in rev_reaction_paths_list:
        df = pd.read_excel(path)
        
        df = df[df['Activation'] <= 30]

        # Iterate over each row in the dataframe
        for index, row in df.iterrows():
            activation_index = row['Activation'] - 1  # Adjust for 0-based indexing
            intensity = subdivision_values[activation_index % len(subdivision_values)]
            
            # Process data for current intensity
            reaction_time = pd.to_numeric(row['Status/Reaction Time'], errors='coerce')
            if not pd.isna(reaction_time):
                data_by_intensity[intensity]['all_reaction_times'].append(reaction_time)
                data_by_intensity[intensity]['induced_reversal_durations'].append(row['Reversal duration'])
            
            adjusted_status = 'Reversals' if not pd.isna(reaction_time) else row['Status/Reaction Time']
            data_by_intensity[intensity]['status_counts'][adjusted_status] = data_by_intensity[intensity]['status_counts'].get(adjusted_status, 0) + 1

    all_durations = []
    for path in rev_duration_paths_list:
        duration_df = pd.read_excel(path)
        all_durations.extend(duration_df['Duration (seconds)'])

    total_reaction_times = []
    for path in rev_reaction_paths_list:
        reaction_df = pd.read_excel(path)
        reaction_df = reaction_df[reaction_df['Activation'] <= 30]

        # Convert 'Status/Reaction Time' to numeric, ignoring non-numeric values
        numeric_reaction_times = pd.to_numeric(reaction_df['Status/Reaction Time'], errors='coerce').dropna()
        total_reaction_times.extend(numeric_reaction_times)

    # Prepare the directory for output
    script_dir = os.getcwd()  # Or specify another directory where you have write permission
    output_file_path = os.path.join(script_dir, "data_analysis_summary_by_intensity.txt")
    
    with open(output_file_path, "w") as file:
        for intensity, data in data_by_intensity.items():
            all_reaction_times = data['all_reaction_times']
            ind_durations = data['induced_reversal_durations']
            status_counts = data['status_counts']
            total_reversals = status_counts.sum()
            
            # Calculate specific percentages as described
            for key in ['Reversals', 'No Reversal', 'Already Reversing', 'No movement']:
                if key not in status_counts:
                    status_counts[key] = 0

            induced_reversals_count = status_counts['Reversals']
            no_reversal_count = status_counts['No Reversal']
            already_reversing_count = status_counts['Already Reversing']
            no_movement_count = status_counts['No movement']

            # Calculate percentages for each status within the subgroup
            reversal_percentage = (induced_reversals_count / (induced_reversals_count + no_reversal_count) * 100) if (induced_reversals_count + no_reversal_count) else 0
            no_reversal_percentage = (no_reversal_count / (induced_reversals_count + no_reversal_count) * 100) if (induced_reversals_count + no_reversal_count) else 0
            already_reversing_percentage = (already_reversing_count / (total_reversals) * 100) if total_reversals else 0
            no_movement_percentage = (no_movement_count / (total_reversals) * 100) if total_reversals else 0

            # Calculate averages and medians
            average_reaction_time = np.mean(all_reaction_times) if all_reaction_times else 'N/A'
            median_reaction_time = np.median(all_reaction_times) if all_reaction_times else 'N/A'
            average_duration_induced_reversals = np.mean(ind_durations) if ind_durations else 'N/A'
            median_duration_induced_reversals = np.median(ind_durations) if ind_durations else 'N/A'

            # Write intensity-specific summary to file
            file.write(f"Intensity Level: {intensity}\n")
            file.write(f"- Average Reaction Time: {average_reaction_time}\n")
            file.write(f"- Median Reaction Time: {median_reaction_time}\n")
            file.write(f"- Average Duration of Induced Reversals: {average_duration_induced_reversals}\n")
            file.write(f"- Median Duration of Induced Reversals: {median_duration_induced_reversals}\n")
            file.write(f"- Counts of Different Statuses:\n{status_counts}\n\n")
            file.write(f'- "Reversals": {reversal_percentage:.2f}%\n')
            file.write(f'- "No Reversal": {no_reversal_percentage:.2f}%\n')
            file.write(f'- "Already Reversing": {already_reversing_percentage:.2f}%\n')
            file.write(f'- "Not detected": {no_movement_percentage:.2f}%\n\n')

        # Write overall summary of durations from rev_duration_all.xlsx
        average_duration_total = np.mean(all_durations) if all_durations else 'N/A'
        median_duration_total = np.median(all_durations) if all_durations else 'N/A'
        file.write("Overall Duration Summary from rev_duration_all.xlsx:\n")
        file.write(f"- Average Duration of Total Reversals: {average_duration_total}\n")
        file.write(f"- Median Duration of Total Reversals: {median_duration_total}\n")

        # Write overall summary of reaction times from rev_reaction.xlsx
        average_reaction_total = np.mean(total_reaction_times) if total_reaction_times else 'N/A'
        median_reaction_total = np.median(total_reaction_times) if total_reaction_times else 'N/A'
        file.write("Overall Duration Summary from rev_reaction.xlsx:\n")
        file.write(f"- Average Duration of Total Reversals: {average_reaction_total}\n")
        file.write(f"- Median Duration of Total Reversals: {median_reaction_total}\n")


    print(f"Summary saved to {output_file_path}")

# Assuming your main_path is correctly set up
perform_data_analysis_by_subgroup_and_save(main_path)




