import matplotlib.pyplot as plt    # Importing the plotting library
import pandas as pd                # Importing the library for data manipulation
import numpy as np                 # Importing the numerical computation library

def load_led_data(path_led: str) -> pd.DataFrame:
    data = pd.read_csv(path_led, header=0)                          # Reading the LED data from a CSV file
    data = data.iloc[1:]                                            # Skip the first frame because it's wrong
    return data                                                     # Returning the processed data

def get_first_led_frames(led_data: pd.DataFrame) -> np.array:
    activated_indices = np.where((led_data['dp'].shift() == 0) & (led_data['dp'] == 4095))[0]    # Finding the indices where LED was activated
    frames = led_data.loc[activated_indices, 'frame_nr'].to_numpy()                              # Getting the corresponding times
    return frames                                                                                # Returning the times

def get_last_led_frames(led_data: pd.DataFrame) -> np.array:
    deactivated_indices = np.where((led_data['dp'].shift() == 4095) & (led_data['dp'] == 0))[0]    # Finding the indices where LED was deactivated
    frames = led_data.loc[deactivated_indices, 'frame_nr'].to_numpy()                              # Getting the corresponding times
    return frames                                                                                  # Returning the times

def load_gp_coordinates(path_gp: str) -> np.array:
    gp_data = pd.read_csv(path_gp, header=None, names=['cycle_nr', 'time', 'x', 'y', 'z'])       # Reading gantry position data from CSV file
    coordinates_xy_gp = np.asarray(np.array(gp_data[['x', 'y']])[1:], dtype=float)               # Extracting x and y coordinates
    cycle_nr = gp_data['cycle_nr'].iloc[1:].astype(int).to_numpy()  # Ensure it's integer
    return coordinates_xy_gp, gp_data['cycle_nr'].iloc[1:].to_numpy()                                # Returning the coordinates and the corresponding times

def get_common_indices(led_frames: np.array, gp_cycles: np.array) -> tuple:
    common_frames = np.intersect1d(led_frames, gp_cycles)
    led_indices = np.isin(led_frames, common_frames)
    gp_indices = np.isin(gp_cycles, common_frames)
    return led_indices, gp_indices

def plot_camera_trajectory(coordinates_xy_gp: np.array, first_led_frames: np.array, last_led_frames: np.array, gp_cycles: np.array, point_size: float = .02) -> None:
    plt.figure(figsize=(30, 30), facecolor='white')                               # Initializing a figure with white background
    
    # Plotting the trajectory
    x_gp, y_gp = coordinates_xy_gp[:, 0], coordinates_xy_gp[:, 1]
    
    # Create a colormap to map the trajectory points to colors based on their order
    colors = plt.cm.viridis(np.linspace(0, 1, len(x_gp)))
    
    # Scatter plot where each point gets its color from the colors array
    plt.scatter(x_gp, y_gp, s=point_size)
    
    # Finding and plotting the times where LED was activated and deactivated
    led_indices, gp_indices = get_common_indices(first_led_times, gp_cycles)           # Indices for LED activations
    last_led_indices, last_gp_indices = get_common_indices(last_led_times, gp_cycles)  # Indices for LED deactivations

    plt.scatter(x_gp[gp_indices], y_gp[gp_indices], color='green', s=point_size*1250, marker='^')
    plt.scatter(x_gp[last_gp_indices], y_gp[last_gp_indices], color='red', s=point_size*1250, marker='s')
    
    # Setting plot title and labels
    plt.title("Camera Trajectory with LED Activations", color='black')
    plt.axis('equal')
    plt.xlabel("x'-position [mm]", color='black')
    plt.ylabel("y'-position [mm]", color='black')
    
    # Adjusting axis colors
    ax = plt.gca()
    ax.set_facecolor('white')                      # Making the background of the axes white
    ax.tick_params(axis='both', colors='black')    # Setting tick colors to black
    
    # Making axis spines black
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
    
    plt.savefig("plot_atr_pos_wrm10.svg")    # Uncomment to save the plot as an SVG file    
    plt.show()      
    
if __name__ == '__main__':
    # File paths
    path_led = r"Z:\neurobiology\zimmer\zidaric\data\oas2\loop_activation\preliminary_adaptation\useful\positive\2023_08_30_13_27_loop_activation_atr_pos_wrm1_sam_Ch0\2023_08_30_13_27_loop_activation_atr_pos_wrm1_sam_led_data.csv"
    path_gp = r"Z:\neurobiology\zimmer\zidaric\data\oas2\loop_activation\preliminary_adaptation\useful\positive\2023_08_30_13_27_loop_activation_atr_pos_wrm1_sam_Ch0\2023_08_30_13_27_loop_activation_atr_pos_wrm1_sam_gantry_position.csv"

    # Processing data
    led_data = load_led_data(path_led)                            # Loading LED data
    first_led_times = get_first_led_frames(led_data)              # Getting activation times
    print(f"Number of LED activations: {len(first_led_times)}")
    last_led_times = get_last_led_frames(led_data)                # Getting deactivation times
    print(f"Number of LED deactivations: {len(last_led_times)}")
    print(f"Max LED frames: {min(first_led_times)}, Min LED frames: {max(first_led_times)}")
    coordinates, gp_cycles = load_gp_coordinates(path_gp)          # Loading gantry position data
    
    print("Data type of first_led_times:", first_led_times.dtype)
    print("Data type of gp_cycles:", gp_cycles.dtype)
    
    try:
        gp_cycles = gp_cycles.astype(int)
    except ValueError:
        unique_types = {type(item) for item in gp_cycles}
        print(f"Unique types in gp_cycles: {unique_types}")
        
        non_integer_values = {item for item in gp_cycles if not isinstance(item, (int, np.integer))}
        print(f"Unique non-integer values in gp_cycles: {non_integer_values}")
        raise
    
    try:
        plot_camera_trajectory(coordinates, first_led_times, last_led_times, gp_cycles)
    except Exception as e:
        print(f"An error occurred: {e}")
