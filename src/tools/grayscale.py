import numpy as np

def rgb_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert an RGB image to grayscale.
    
    :param image: Input image in RGB format (height, width, 3).
    :return: Grayscale image (height, width).
    """
    B = image[:, :, 0]  # Blue channel
    G = image[:, :, 1]  # Green channel
    R = image[:, :, 2]  # Red channel
    
    # Apply the formula to convert to grayscale
    grayscale_image = 0.299 * R + 0.587 * G + 0.114 * B
    
    # Convert the result to unsigned 8-bit integer (same as original image)
    grayscale_image = np.clip(grayscale_image, 0, 255).astype(np.uint8)
    
    return grayscale_image
