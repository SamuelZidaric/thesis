import pandas as pd
import os
import glob

main_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_neg_uli/data/'

# Function to perform data analysis
def perform_data_analysis(main_path):
    # Paths to find files
    rev_reaction_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))
    rev_duration_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_duration_all.xlsx'))

    # Initialize aggregation variables
    all_reaction_times = []
    all_durations = []
    status_counts = pd.Series(dtype='int')
    induced_reversal_durations = []

    # Process each rev_reaction file
    for path in rev_reaction_paths_list:
        df = pd.read_excel(path)
        if 'Activation' in df.columns:
            df = df[df['Activation'] <= 56]       
        # Handle reaction times and statuses
        reaction_times = pd.to_numeric(df['Status/Reaction Time'], errors='coerce').dropna()
        all_reaction_times.extend(reaction_times)
        df['Adjusted Status'] = df['Status/Reaction Time'].apply(lambda x: 'Reversals' if not pd.isna(pd.to_numeric(x, errors='coerce')) else x)
        new_counts = df['Adjusted Status'].value_counts()
        status_counts = status_counts.add(new_counts, fill_value=0)
        # Collect durations for induced reversals
        induced_reversal_durations.extend(df.loc[df['Status/Reaction Time'].apply(lambda x: not pd.isna(pd.to_numeric(x, errors='coerce'))), 'Reversal duration'])

    # Print the count of rev_reaction files processed
    print(f"Processed {len(rev_reaction_paths_list)} rev_reaction.xlsx files.")

    # Process each rev_duration file
    for path in rev_duration_paths_list:
        df = pd.read_excel(path)
        all_durations.extend(df['Duration (seconds)'])

    # Safe calculation of averages
    average_reaction_time = sum(all_reaction_times) / len(all_reaction_times) if all_reaction_times else None
    average_reversal_duration = sum(all_durations) / len(all_durations) if all_durations else None
    average_duration_induced_reversals = sum(induced_reversal_durations) / len(induced_reversal_durations) if induced_reversal_durations else None

    total_reversals = len(all_durations)
    induced_reversals_count = status_counts.get('Reversals', 0)
    stochastic_reversals_count = total_reversals - induced_reversals_count

    # Prepare summary
    summary_text = f"""
Comprehensive Data Analysis Summary:

Overall Dataset Summary:
- Average Reaction Time: {'N/A' if average_reaction_time is None else f'{average_reaction_time:.2f}'} seconds
- Average Reversal Duration (Total): {'N/A' if average_reversal_duration is None else f'{average_reversal_duration:.2f}'} seconds
- Average Duration of Induced Reversals: {'N/A' if average_duration_induced_reversals is None else f'{average_duration_induced_reversals:.2f}'} seconds

Reversal Counts and Percentages:
- Total Reversals: {total_reversals}
  - Stochastic (Naturally Occurring) Reversals: {stochastic_reversals_count} ({(stochastic_reversals_count / total_reversals * 100) if total_reversals else 0:.2f}% of Total)
  - Induced Reversals: {induced_reversals_count} ({(induced_reversals_count / total_reversals * 100) if total_reversals else 0:.2f}% of Total)

Subgroup Analysis (Up to Activation 56):
- Counts of Different Statuses:
  - "Reversals": {induced_reversals_count}
  - "Already Reversing": {status_counts.get('Already Reversing', 0)}
  - "No Reversal": {status_counts.get('No Reversal', 0)} (if applicable)
  - "Not detected": {status_counts.get('No movement', 0)} (if applicable)


- Percentages of Each Status within Subgroup:
  - "Reversals": {(induced_reversals_count / (induced_reversals_count + status_counts.get('No Reversal', 0)) * 100) if induced_reversals_count + status_counts.get('No Reversal', 0) else 0:.2f}%
  - "No Reversal": {(status_counts.get('No Reversal', 0) / (induced_reversals_count + status_counts.get('No Reversal', 0)) * 100) if induced_reversals_count + status_counts.get('No Reversal', 0) else 0:.2f}%
  - "Already Reversing": {(status_counts.get('Already Reversing', 0) / (induced_reversals_count + status_counts.get('Already Reversing', 0) + status_counts.get('No Reversal', 0) + status_counts.get('No movement', 0)) * 100) if induced_reversals_count + status_counts.get('Already Reversing', 0) + status_counts.get('No Reversal', 0) + status_counts.get('No movement', 0) else 0:.2f}%
  - "Not detected": {(status_counts.get('No movement', 0) / (induced_reversals_count + status_counts.get('Already Reversing', 0) + status_counts.get('No Reversal', 0) + status_counts.get('No movement', 0)) * 100) if induced_reversals_count + status_counts.get('Already Reversing', 0) + status_counts.get('No Reversal', 0) + status_counts.get('No movement', 0) else 0:.2f}%
"""

    # Save summary in the script's directory
    script_dir = os.path.dirname(__file__)
    output_file_path = os.path.join(script_dir, "full_data_analysis_summary.txt")
    with open(output_file_path, "w") as file:
        file.write(summary_text)

    print(f"Summary saved to {output_file_path}")

# Assuming your main_path is correctly set up
perform_data_analysis(main_path)

