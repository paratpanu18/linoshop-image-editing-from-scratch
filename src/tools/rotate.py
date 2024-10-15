import numpy as np

def rotate_function(rotation_matrix: np.ndarray, pos_x: int, pos_y: int):
    """
    Rotate a point around the origin (0, 0) by a given angle.

    :param angle: Angle in degrees.
    :param pos_x: X-coordinate of the point.
    :param pos_y: Y-coordinate of the point.
    :return: Rotated point coordinates.
    """
    point = np.array([pos_x, pos_y])
    rotated_point = np.dot(rotation_matrix, point)
    return rotated_point[0], rotated_point[1]

def get_new_dimensions(width, height, angle):
    """
    Calculate the new dimensions of the image after rotation to fit the entire content.
    
    :param width: Original image width.
    :param height: Original image height.
    :param angle: Angle in degrees.
    :return: New width and height after rotation.
    """
    angle_rad = np.radians(angle)
    
    # Calculate new dimensions
    new_width = abs(width * np.cos(angle_rad)) + abs(height * np.sin(angle_rad))
    new_height = abs(width * np.sin(angle_rad)) + abs(height * np.cos(angle_rad))
    
    return int(np.ceil(new_width)), int(np.ceil(new_height))

def rotate_image(image: np.ndarray, angle: float):
    """
    Rotate an image by a given angle around its center, adjusting dimensions to fit.

    :param image: Input image as a NumPy array (height, width, 3).
    :param angle: Angle in degrees for rotation.
    :return: Rotated image.
    """
    height, width, _ = image.shape
    
    # Get the new dimensions after rotation
    new_width, new_height = get_new_dimensions(width, height, angle)
    
    # Find the center of the original and new image
    center_x, center_y = width // 2, height // 2
    new_center_x, new_center_y = new_width // 2, new_height // 2

    # Create an empty output image with new dimensions
    rotated_image = np.zeros((new_height, new_width, image.shape[2]), dtype=image.dtype)
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                 [np.sin(angle_rad), np.cos(angle_rad)]])

    # Iterate over each pixel in the output image
    for y in range(new_height):
        for x in range(new_width):
            # Compute the coordinates relative to the center of the new image
            rel_x = x - new_center_x
            rel_y = y - new_center_y

            # Rotate the point using the rotate_function
            orig_x, orig_y = rotate_function(rotation_matrix, rel_x, rel_y)

            # Shift the rotated coordinates back to the original image space
            orig_x = int(orig_x + center_x)
            orig_y = int(orig_y + center_y)

            # If the new coordinates are within the bounds of the original image, assign the pixel
            if 0 <= orig_x < width and 0 <= orig_y < height:
                rotated_image[y, x] = image[orig_y, orig_x]

    return rotated_image