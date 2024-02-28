# This script creates an average intensity image from a given input image.

import argparse
import os
import skimage.io
import numpy as np
import tifffile

def create_average_intensity_image(image):
    """
    Create an image with the average intensity of the original image.
    :param image: Numpy array representing the image.
    :return: Image with average intensity.
    """
    # Calculate the average intensity
    average_intensity = np.mean(image)

    # Create a new image with the same shape as the original, filled with the average intensity
    average_intensity_image = np.full(image.shape, average_intensity, dtype=image.dtype)

    return average_intensity_image

def process_image(input_path, output_file):
    """
    Process the image file to create an average intensity image and save it.
    :param input_path: Path to the image file.
    :param output_file: Path to save the output image.
    """
    print(f"Creating average intensity image from: {input_path}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Read the image
    image = tifffile.imread(input_path)

    # Check if the image is already in grayscale
    if image.ndim == 3 and image.shape[2] in [3, 4]:  # RGB or RGBA
        image = skimage.color.rgb2gray(image)

    # Create an average intensity image
    avg_intensity_image = create_average_intensity_image(image)

    # Save the result
    tifffile.imsave(output_file, avg_intensity_image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an average intensity image")
    parser.add_argument("--input", required=True, help="Path to the image file")
    parser.add_argument("--output", required=True, help="Path for the output TIFF file")
    args = parser.parse_args()

    process_image(args.input, args.output)
