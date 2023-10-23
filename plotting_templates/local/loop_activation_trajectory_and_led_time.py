import matplotlib.pyplot as plt    # Importing the plotting library
import pandas as pd                # Importing the library for data manipulation
import numpy as np                 # Importing the numerical computation library

def load_led_data(path_led: str) -> pd.DataFrame:
    data = pd.read_csv(path_led, header=0)                          # Reading the LED data from a CSV file
    data['time'] = data['time'].apply(convert_time_to_seconds)      # Converting the time column to seconds
    return data                                                     # Returning the processed data

def convert_time_to_seconds(time_str: str) -> float:
    """
    Convert a time string of format 'HH:MM:SS.mmmmm' or 'HH:MM:SS.mmmm' to seconds.
    """
    if time_str == 'time':         # Handle the case where the string is the header "time"
        return time_str
    
    parts = time_str.split(':')                          # Splitting the time string at colons
    hours, minutes = float(parts[0]), float(parts[1])    # Extracting hours and minutes and converting to float
    seconds = float(parts[2])                            # Extracting seconds (including milliseconds)
    return hours * 3600 + minutes * 60 + seconds         # Converting everything to seconds and returning

def get_first_led_frames(led_data: pd.DataFrame) -> np.array:
    activated_indices = np.where((led_data['dp'].shift() == 0) & (led_data['dp'] == 4095))[0]    # Finding the indices where LED was activated
    frames = led_data.loc[activated_indices, 'time'].to_numpy()                                  # Getting the corresponding times
    return frames                                                                                # Returning the times

def get_last_led_frames(led_data: pd.DataFrame) -> np.array:
    deactivated_indices = np.where((led_data['dp'].shift() == 4095) & (led_data['dp'] == 0))[0]    # Finding the indices where LED was deactivated
    frames = led_data.loc[deactivated_indices, 'time'].to_numpy()                                  # Getting the corresponding times
    return frames                                                                                  # Returning the times

def load_gp_coordinates(path_gp: str) -> np.array:
    gp_data = pd.read_csv(path_gp, header=None, names=['cycle_nr', 'time', 'x', 'y', 'z'])       # Reading gantry position data from CSV file
    gp_data['time'] = gp_data['time'].apply(convert_time_to_seconds)                             # Converting the time column to seconds
    coordinates_xy_gp = np.asarray(np.array(gp_data[['x', 'y']])[1:], dtype=float)               # Extracting x and y coordinates
    return coordinates_xy_gp, gp_data['time'].iloc[1:].to_numpy()                                # Returning the coordinates and the corresponding times

def get_nearest_indices(gp_times: np.array, led_times: np.array, threshold=0.5):     # or adjust as needed
    """
    Returns indices in gp_times that are closest to each entry in led_times.
    """
    indices = []                                                                     # List to store indices
    for led_time in led_times:                                                       # Iterating over each LED time
        absolute_differences = np.abs(gp_times - led_time)                           # Computing differences with each gp_time
        if np.min(absolute_differences) <= threshold:                                # Checking if the minimum difference is within threshold
            indices.append(np.argmin(absolute_differences))                          # Appending the index of the closest gp_time
    return np.array(indices)                                                         # Returning the indices as an array

def plot_camera_trajectory(coordinates_xy_gp: np.array, led_times: np.array, gp_times: np.array, point_size: float = .02) -> None:
    plt.figure(figsize=(30, 30), facecolor='white')                               # Initializing a figure with white background
    
    # Plotting the trajectory
    x_gp, y_gp = coordinates_xy_gp[:, 0], coordinates_xy_gp[:, 1]
    plt.scatter(x_gp, y_gp, s=point_size)                                         # Plotting the x and y coordinates of the gantry
    
    # Finding and plotting the times where LED was activated and deactivated
    mask_indices = get_nearest_indices(gp_times, led_times)                       # Indices for LED activations
    print(f"Number of indices for LED activation visualization: {len(mask_indices)}")
    mask_indices_deactivation = get_nearest_indices(gp_times, last_led_times)     # Indices for LED deactivations
    plt.scatter(x_gp[mask_indices], y_gp[mask_indices], color='green', s=point_size*1250, marker='^')
    plt.scatter(x_gp[mask_indices_deactivation], y_gp[mask_indices_deactivation], color='red', s=point_size*1250, marker='s')
    
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
    
    # plt.savefig("NAME_OF_PLOT_FILE.svg")    # Uncomment to save the plot as an SVG file    
    plt.show()                                # Displaying the plot    
    
if __name__ == '__main__':
    # File paths
    path_led = r"PATH_TO_TEH_LED_DATA_CSV"
    path_gp = r"PATH_TO_TEH_GANTRY_POSITION_CSV"

    # Processing data
    led_data = load_led_data(path_led)                            # Loading LED data
    first_led_times = get_first_led_frames(led_data)              # Getting activation times
    print(f"Number of LED activations: {len(first_led_times)}")
    last_led_times = get_last_led_frames(led_data)                # Getting deactivation times
    print(f"Number of LED deactivations: {len(last_led_times)}")
    print(f"Min LED Time: {min(first_led_times)}, Max LED Time: {max(first_led_times)}")
    coordinates, gp_times = load_gp_coordinates(path_gp)          # Loading gantry position data

    # Plotting the data
    plot_camera_trajectory(coordinates, first_led_times, gp_times)
