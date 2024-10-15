import numpy as np

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
    
    # Compute the dot product of the two vectors
    dot_product = np.dot(v1_flat, v2_flat)
    
    # Compute the magnitudes of the two vectors
    magnitude_v1 = np.linalg.norm(v1_flat)
    magnitude_v2 = np.linalg.norm(v2_flat)
    
    # Avoid division by zero by checking if magnitudes are zero
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
    
    # Compute the cosine similarity
    similarity = dot_product / (magnitude_v1 * magnitude_v2)
    
    return similarity