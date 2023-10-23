import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_led_data(path_led: str) -> pd.DataFrame:
    """
    Load the LED activation data using pandas.
    """
    return pd.read_csv(path_led, header=0)  # Adjust header argument if needed

def get_first_led_frames(led_data: pd.DataFrame) -> np.array:
    """
    Extract frame numbers of the first frame of each LED activation.
    """
    # Identifying transitions from 0 to 4095 in the 'dp' column.
    activated_indices = np.where((led_data['dp'].shift() == 0) & (led_data['dp'] == 4095))[0]
    
    # Extracting the frame numbers at these indices.
    frames = led_data.loc[activated_indices, 'frame_nr'].to_numpy()
    
    return frames

def plot_led_activations(frames: np.array) -> None:
    """
    Plot frame numbers of the first frame of each LED activation.
    """
    plt.figure(figsize=(15, 10))
    plt.scatter(frames, [1]*len(frames), color='red') # plotting at y=1 for visibility, adjust as needed
    plt.title("LED Activations")
    plt.xlabel("Frame Number")
    plt.ylabel("LED Activation")
    plt.yticks([]) # hide y axis ticks
    # plt.savefig("NAME_OF_PLOT_FILE.svg")    # Uncomment to save the plot as an SVG file    
    plt.show()

if __name__ == '__main__':
    path_led = r"PATH_TO_TEH_LED_DATA_CSV"
    led_data = load_led_data(path_led)
    first_frames = get_first_led_frames(led_data)
    plot_led_activations(first_frames)
