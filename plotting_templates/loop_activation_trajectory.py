import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_gp_coordinates(path_gp: str) -> np.array:
    """
    loads the gp-data with pandas and returns the xy-coordinates as numpy array
    """
    gp_data = pd.read_csv(path_gp, header=None)
    coordinates_xy_gp = np.asarray(np.array(gp_data.iloc[:, 2:4])[1:], dtype=float)

    return coordinates_xy_gp

def plot_camera_trajectory(coordinates_xy_gp: np.array, point_size: float = .02) -> None:
    """
    plots the x'y'-trajectory of the camera position
    (the OAS coordinate system has mirrored axes "xy", while "x'y'" refers to the motor coordinate system)
    """
    plt.figure(figsize=(30, 30))  # Here, we're setting the figure size to 10 inches by 10 inches
    x_gp, y_gp = coordinates_xy_gp[:, 0], coordinates_xy_gp[:, 1]
    plt.scatter(x_gp, y_gp, s=point_size)
    plt.title("Camera Trajectory")
    plt.axis('equal')
    plt.xlabel("x'-position [mm]")
    plt.ylabel("y'-position [mm]")

    # plt.savefig("plot_atr_neg_wrm3.svg")    # Uncomment to save in svg file
    plt.show()

# example call:
if __name__ == '__main__':
    path_gp = r"Z:\neurobiology\zimmer\zidaric\data\oas2\loop_activation\2023_08_29_11_42_loop_activation_atr_neg_wrm1_sam\2023_08_29_11_42_loop_activation_atr_neg_wrm1_sam_gantry_position.csv"
    plot_camera_trajectory(load_gp_coordinates(path_gp))
