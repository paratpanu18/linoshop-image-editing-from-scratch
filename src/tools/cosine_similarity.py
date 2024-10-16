import numpy as np

def dot_product(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculate the dot product of two vectors."""
    result = 0.0
    for a, b in zip(v1, v2):
        result += a * b
    return result

def magnitude(v: np.ndarray) -> float:
    """Calculate the magnitude of a vector."""
    sum_squares = 0.0
    for x in v:
        sum_squares += x ** 2
    return sum_squares ** 0.5

def resize_vector(v: np.ndarray, new_size: int) -> np.ndarray:
    """Resize a vector to a new size by repeating elements if necessary."""
    if len(v) >= new_size:
        return v[:new_size]
    else:
        # Repeat elements to fill the new size
        resized = np.empty(new_size, dtype=v.dtype)
        for i in range(new_size):
            resized[i] = v[i % len(v)]
        return resized

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """
    Compute the cosine similarity between two images by flattening them into vectors.

    :param v1: First image (RGB).
    :param v2: Second image (RGB).
    :return: Cosine similarity between the two flattened images.
    """
    # Flatten the images into 1D vectors
    v1_flat = v1.flatten().astype(np.float32)
    v2_flat = v2.flatten().astype(np.float32)

    # Resize v2_flat to match the size of v1_flat if they are different
    if v1_flat.shape != v2_flat.shape:
        v2_flat = resize_vector(v2_flat, v1_flat.shape[0])
        
    # Compute the dot product of the two vectors
    dot_product_result = dot_product(v1_flat, v2_flat)
    
    # Compute the magnitudes of the two vectors
    magnitude_v1 = magnitude(v1_flat)
    magnitude_v2 = magnitude(v2_flat)
    
    # Avoid division by zero by checking if magnitudes are zero
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
    
    # Compute the cosine similarity
    similarity = dot_product_result / (magnitude_v1 * magnitude_v2)
    return similarity
