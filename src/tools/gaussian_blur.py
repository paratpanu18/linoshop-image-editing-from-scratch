import numpy as np
import cv2

def create_gaussian_kernel(size: int, sigma: int = 1) -> np.ndarray:
    """
    This function creates a Gaussian kernel with the specified size and sigma.

    :param size: The size of the kernel (should be an odd number).
    :param sigma: The standard deviation of the Gaussian distribution.
    :return: The Gaussian kernel.
    """
    print(f"Creating Gaussian kernel with size {size} and sigma {sigma}...")
    # Define the center point of the kernel
    center = (size - 1) / 2
    
    def gaussian_function(x, y):
        exponent = -((x - center)**2 + (y - center)**2) / (2 * sigma**2)
        return (1 / (2 * np.pi * sigma**2)) * np.exp(exponent)
    
    # Create the kernel by applying the Gaussian function to each point
    kernel = np.fromfunction(gaussian_function, (size, size))

    print("Gaussian kernel created successfully!")
    print(kernel)

    return kernel / np.sum(kernel)

def convolution(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # Get the dimensions of the image and kernel
    image_height, image_width, channels = image.shape
    kernel_height, kernel_width = kernel.shape

    print(f"Performing convolution on image with shape {image.shape} and kernel with shape {kernel.shape}...")
    
    # Calculate the padding size
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    print(f"Padding the image with {pad_height} rows and {pad_width} columns...")

    # Initialize the output image
    output = np.zeros_like(image)
    
    # Convolution using dot-product
    for c in range(channels):
        print(f"Processing channel {c + 1} of {channels}...")
        padded_image = np.pad(image[:, :, c], ((pad_height, pad_height), (pad_width, pad_width)), mode='reflect')
        
        for i in range(image_height):
            for j in range(image_width):
                # Extract the region of interest for the current channel
                region = padded_image[i:i+kernel_height, j:j+kernel_width]
            
                # Dot product of the region and the kernel
                output[i, j, c] = np.sum(region * kernel)

    return output

def gaussian_blur(image: np.ndarray, kernel_size:int = 5, sigma: int = 1) -> np.ndarray:
    """
    Apply Gaussian blur to an image.

    :param image_path: The path to the image file.
    :param kernel_size: The size of the Gaussian kernel.
    :param sigma: The standard deviation of the Gaussian distribution.
    :return: The blurred image.
    """

    kernel = create_gaussian_kernel(kernel_size, sigma)
    blurred_image = convolution(image, kernel)
    
    return blurred_image
