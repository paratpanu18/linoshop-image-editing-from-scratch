from enum import Enum
import numpy as np
import cv2

class FilterType(Enum):
    COOL_TONE = "Cool Tone"
    WARM_TONE = "Warm Tone"
    VINTAGE_TONE = "Vintage Tone"
    HIGH_CONTRAST = "High Contrast"

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

    # Retrieve filter settings for the specified filter type
    settings = FILTER_SETTINGS[filter_type]
    
    return apply_rgb_adjustment(image, settings['scaling'], settings['offset'])

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