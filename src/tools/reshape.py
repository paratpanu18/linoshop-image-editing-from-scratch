import numpy as np
from enum import Enum
# from skimage.draw import polygon  # Make sure you have scikit-image installed

class MaskType(Enum):
    CIRCULAR = "Circular Mask"
    HEART = "Heart Mask"
    # STAR = "Star Mask"

def apply_mask(image: np.ndarray, mask_type: MaskType) -> np.ndarray:
    """
    Apply the specified mask to the image.

    :param image: Input image in RGB format (height, width, 3).
    :param mask_type: The type of mask to apply.
    :return: Image with the specified mask applied.
    """
    if mask_type == MaskType.CIRCULAR:
        return apply_circular_mask(image)
    elif mask_type == MaskType.HEART:
        return apply_heart_mask(image)
    # elif mask_type == MaskType.STAR:
    #     return apply_star_mask(image)
    else:
        raise ValueError(f"Invalid mask type: {mask_type}")

def apply_circular_mask(image: np.ndarray) -> np.ndarray:
    """
    Apply a circular mask to a color image.

    :param image: Color image (height, width, 3).
    :return: Image with a circular mask.
    """
    height, width = image.shape[:2]
    center_y, center_x = height // 2, width // 2
    radius = min(center_y, center_x)  # Radius of the circle

    # Create a circular mask
    Y, X = np.ogrid[:height, :width]
    distance_from_center = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
    mask = distance_from_center <= radius

    # Apply the mask to the original image
    masked_image = np.zeros_like(image)
    masked_image[mask] = image[mask]

    return masked_image

# def apply_star_mask(image: np.ndarray) -> np.ndarray:
#     """
#     Apply a star-shaped mask to a color image.

#     :param image: Color image (height, width, 3).
#     :return: Image with a star-shaped mask.
#     """
#     height, width = image.shape[:2]
#     center_y, center_x = height // 2, width // 2
#     radius = min(center_y, center_x) * 0.9

#     # Define points for a star-shaped polygon (5-point star)
#     points_y = np.array([center_y, center_y - radius, center_y, center_y + radius, center_y]) * 0.75
#     points_x = np.array([center_x - radius, center_x, center_x + radius, center_x, center_x - radius]) * 0.75
#     rr, cc = polygon(points_y, points_x, shape=image.shape[:2])

#     # Create mask and apply it to the original image
#     mask = np.zeros_like(image, dtype=bool)
#     mask[rr, cc] = True
#     masked_image = np.zeros_like(image)
#     masked_image[mask] = image[mask]

#     return masked_image

def apply_heart_mask(image: np.ndarray) -> np.ndarray:
    """
    Apply a heart-shaped mask to a color image.

    :param image: Color image (height, width, 3).
    :return: Image with a heart-shaped mask.
    """
    height, width = image.shape[:2]
    center_y, center_x = height // 2, width // 2
    scale_factor = min(center_y, center_x) / 1.5  # Scale factor for heart size

    Y, X = np.ogrid[:height, :width]
    X = (X - center_x) / scale_factor
    Y = (Y - center_y) / scale_factor

    # Parametric equation of a heart (simplified form)
    heart_mask = ((X ** 2 + Y ** 2 - 1) ** 3 - X ** 2 * -1*(Y ** 3)) <= 0 # add -1 because of the inversion of the y-axis
    # Apply the mask to the original image
    masked_image = np.zeros_like(image)
    masked_image[heart_mask] = image[heart_mask]

    return masked_image
