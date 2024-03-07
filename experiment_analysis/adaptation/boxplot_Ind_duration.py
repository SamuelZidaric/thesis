import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# Your main path
main_path = 'Z:/neurobiology/zimmer/zidaric/data/pre_pos_uli/data/'

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Function to aggregate reversal durations and intensity levels into a DataFrame
def create_reversal_duration_dataframe(main_path):
    rev_reaction_paths_list = glob.glob(os.path.join(main_path, 'w*/*Ch0/rev_reaction.xlsx'))

    for file_path in rev_reaction_paths_list:
        temp_data = pd.read_excel(file_path)
        temp_data = temp_data[temp_data['Activation'] <= 56]  # Filter activations up to 56
        
        # Add an identifier column to distinguish between datasets
        identifier = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        temp_data['Identifier'] = identifier
        
        # Convert 'Reversal duration' to numeric, coercing errors to NaN
        temp_data['Duration (seconds)'] = pd.to_numeric(temp_data['Reversal duration'], errors='coerce')
        
        # Append the filtered data to the all_data DataFrame
        global all_data
        all_data = pd.concat([all_data, temp_data], ignore_index=True)

# Call the function to create the DataFrame
create_reversal_duration_dataframe(main_path)

# Filter out rows without a valid numeric reversal duration
filtered_data = all_data.dropna(subset=['Duration (seconds)'])

# Function to plot reversal durations with jitter and sample size annotations
def plot_reversal_durations_with_jitter_and_n(df):
    # Visualization with Seaborn: Box plot of reversal durations by Identifier
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Identifier', y='Duration (seconds)', data=df, color='lightblue')
    sns.stripplot(x='Identifier', y='Duration (seconds)', data=df, size=4, color='darkblue', alpha=0.5)
    plt.title('Distribution of Induced Reversal Durations by Individual Worm in ATR+')
    plt.xlabel('Worms')
    plt.ylabel('Reversal duration (seconds)')
    plt.xticks(rotation=45)  # Rotate labels if they overlap
    # Add a textbox with the total sample size
    total_sample_size = len(df)
    plt.text(0.94, 0.95, f'Total sample size = {total_sample_size}', transform=plt.gcf().transFigure, 
            ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))
    plt.tight_layout()
    plt.show()

# Plot the reversal durations with jittering and sample size annotations
plot_reversal_durations_with_jitter_and_n(filtered_data)
