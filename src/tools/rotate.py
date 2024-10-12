import numpy as np

def rotate_function(angle: float, pos_x: int, pos_y: int):
    """
    Rotate a point around the origin (0, 0) by a given angle.

    :param angle: Angle in degrees.
    :param pos_x: X-coordinate of the point.
    :param pos_y: Y-coordinate of the point.
    :return: Rotated point coordinates.
    """
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                 [np.sin(angle_rad), np.cos(angle_rad)]])
    point = np.array([pos_x, pos_y])
    rotated_point = np.dot(rotation_matrix, point)
    return rotated_point[0], rotated_point[1]

def rotate_image(image: np.ndarray, angle: float):
    """
    Rotate an image by a given angle around its center.

    :param image: Input image as a NumPy array (height, width, 3).
    :param angle: Angle in degrees for rotation.
    :return: Rotated image.
    """
    height, width, _ = image.shape
    # Find the center of the image
    center_x, center_y = width // 2, height // 2

    # Create an empty output image (same size as original)
    rotated_image = np.zeros_like(image)

    # Iterate over each pixel in the output image
    for y in range(height):
        for x in range(width):
            # Compute the coordinates relative to the center
            rel_x = x - center_x
            rel_y = y - center_y

            # Rotate the point using the rotate_function
            new_x, new_y = rotate_function(-angle, rel_x, rel_y)  # Use negative angle for reverse rotation
            
            # Shift the rotated coordinates back to image space
            new_x = int(new_x + center_x)
            new_y = int(new_y + center_y)

            # If the new coordinates are within the bounds, assign the pixel
            if 0 <= new_x < width and 0 <= new_y < height:
                rotated_image[y, x] = image[new_y, new_x]

    return rotated_image