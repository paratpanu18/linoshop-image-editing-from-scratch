from enum import Enum
import numpy as np
import cv2
from tools.grayscale import rgb_to_grayscale

class FilterType(Enum):
    COOL_TONE = "Cool Tone"
    WARM_TONE = "Warm Tone"
    VINTAGE_TONE = "Vintage Tone"
    HIGH_CONTRAST = "High Contrast"
    INVERT = "Invert"
    OUTLINE = "Outline"

FILTER_SETTINGS = {
    FilterType.COOL_TONE: {
        'scaling': (1.25, 1.05, 0.8), 
        'offset': (0, 0, 0)        
    },
    FilterType.WARM_TONE: {
        'scaling': (0.85, 1.05, 1.3),
        'offset': (0, 0, 0)
    },
    FilterType.VINTAGE_TONE: {
        'scaling': (0.5, 0.7, 1.2),
        'offset': (0, 30, 15)
    },
    FilterType.HIGH_CONTRAST: {
        'scaling': (1.5, 1.5, 1.5),
        'offset': (-50, -50, -50)
    },
    FilterType.INVERT: {    # Light areas in the original image become dark, and dark areas become light.
        'scaling': (-1, -1, -1),  # Negative scaling to invert colors
        'offset': (255, 255, 255)  # Offset so inverted value is in range [0, 255]
    },
    FilterType.OUTLINE: {
        'scaling': (0, 0, 0),    # Remove color, focus on edges
        'offset': (255, 255, 255)   # Turn edges to white (outline effect)
    }
}

def apply_filter(image: np.ndarray, filter_type: FilterType) -> np.ndarray:
    """
    Apply the specified filter to the image.
    
    :param image: Input image in BGR format (height, width, 3).
    :param filter_type: The type of filter to apply.
    :return: Image with the specified filter applied.
    """
    # If the image is grayscale, convert it to BGR format
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Check for the INVERT filter type
    if filter_type == FilterType.INVERT:
        return cv2.bitwise_not(image)  # Invert colors directly Ex. image(50, 100, 150) invert is image(255-50, 255-100, 255-150)
    
    # Check for the OUTLINE filter type
    if filter_type == FilterType.OUTLINE:
        return apply_outline(image)

    # Retrieve filter settings for the specified filter type
    settings = FILTER_SETTINGS[filter_type]
    
    return apply_rgb_adjustment(image, settings['scaling'], settings['offset'])

def apply_outline(image: np.ndarray) -> np.ndarray:
    """
    Apply an outline effect to the image using a Sobel filter for edge detection.
    
    :param image: Input image in BGR format (height, width, 3).
    :return: Image with outline effect applied.
    """

    grayscale_image = rgb_to_grayscale(image)  # Change variable name to grayscale_image
    # Convert to grayscale for easier edge detection 
    # It reduces the complexity of processing three color channels (BGR) to just one channel (grayscale).

    # Define Sobel kernels for edge detection
    sobel_x = np.array([[1, 0, -1],
                        [2, 0, -2],
                        [1, 0, -1]], dtype=np.float32)  # Horizontal edges

    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]], dtype=np.float32)  # Vertical edges

    # Get image dimensions
    height, width = grayscale_image.shape

    # Create an empty array for the output image
    outline_image = np.zeros_like(grayscale_image)

    # Apply the Sobel filter to detect edges
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Convolution for Sobel X
            gx = (sobel_x[0, 0] * grayscale_image[y - 1, x - 1] + sobel_x[0, 1] * grayscale_image[y - 1, x] + sobel_x[0, 2] * grayscale_image[y - 1, x + 1] +
                  sobel_x[1, 0] * grayscale_image[y, x - 1] + sobel_x[1, 1] * grayscale_image[y, x] + sobel_x[1, 2] * grayscale_image[y, x + 1] +
                  sobel_x[2, 0] * grayscale_image[y + 1, x - 1] + sobel_x[2, 1] * grayscale_image[y + 1, x] + sobel_x[2, 2] * grayscale_image[y + 1, x + 1])
            
            # Convolution for Sobel Y
            gy = (sobel_y[0, 0] * grayscale_image[y - 1, x - 1] + sobel_y[0, 1] * grayscale_image[y - 1, x] + sobel_y[0, 2] * grayscale_image[y - 1, x + 1] +
                  sobel_y[1, 0] * grayscale_image[y, x - 1] + sobel_y[1, 1] * grayscale_image[y, x] + sobel_y[1, 2] * grayscale_image[y, x + 1] +
                  sobel_y[2, 0] * grayscale_image[y + 1, x - 1] + sobel_y[2, 1] * grayscale_image[y + 1, x] + sobel_y[2, 2] * grayscale_image[y + 1, x + 1])
            
            # Calculate gradient magnitude
            magnitude = np.sqrt(gx ** 2 + gy ** 2)
            outline_image[y, x] = np.clip(magnitude, 0, 255)

    # Normalize the outline image to the range [0, 255] for calculate threshold value 
    outline_image = (outline_image / outline_image.max() * 255).astype(np.uint8)

    # Grayscale outline image is converted back to a 3-channel BGR image
    color_outline_image = cv2.cvtColor(outline_image, cv2.COLOR_GRAY2BGR)

    # Set a threshold to keep only significant edges
    mask = (outline_image > 50).astype(np.uint8)  # (If outline_image > 50 are considered edges )
    color_outline_image[mask == 0] = (255, 255, 255)  # (And below 50 are set to white)

    return color_outline_image


def apply_rgb_adjustment(image: np.ndarray, scaling: tuple, offset: tuple) -> np.ndarray:
    """
    Apply RGB channel scaling and offset adjustments to the image.
    
    :param image: Input image in BGR format (height, width, 3).
    :param scaling: Tuple of scaling factors for (B, G, R) channels.
    :param offset: Tuple of offset values for (B, G, R) channels.
    :return: Adjusted image with the given RGB scaling and offset.
    """
    B = image[:, :, 0] * scaling[0] + offset[0]
    G = image[:, :, 1] * scaling[1] + offset[1]
    R = image[:, :, 2] * scaling[2] + offset[2]

    # Clip values to ensure they are in the valid range [0, 255]
    B = np.clip(B, 0, 255)
    G = np.clip(G, 0, 255)
    R = np.clip(R, 0, 255)

    # Merge the adjusted channels back into a BGR image
    adjusted_image = np.dstack((B, G, R)).astype(np.uint8)

    return adjusted_image