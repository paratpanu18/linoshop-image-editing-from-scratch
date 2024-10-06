from enum import Enum
import numpy as np
from numba import jit
import cv2

class BlurType(Enum):
    GAUSSIAN = "Gaussian Blur"
    BOX = "Box Blur"
    VERTICAL = "Vertical Blur"

BLUR_FUNCTIONS = {
    BlurType.GAUSSIAN: lambda img, kernel_size, sigma: BlurFilter.gaussian_blur(img, kernel_size, sigma),
    BlurType.BOX: lambda img, kernel_size, sigma: BlurFilter.box_blur(img, kernel_size),
    BlurType.VERTICAL: lambda img, kernel_size, sigma: BlurFilter.vertical_blur(img, kernel_size),
}

def apply_blur(image: np.ndarray, blur_type: BlurType, kernel_size: int = 5, sigma: int = 5) -> np.ndarray:
    """
    Apply the specified blur to the image using the dispatch table.
    
    :param image: Input image in BGR format (height, width, 3).
    :param blur_type: The type of blur to apply.
    :param kernel_size: The size of the kernel to use for the blur.
    :param sigma: The standard deviation for Gaussian blur (if applicable).
    :return: Image with the specified blur applied.
    """
    
    blur_function = BLUR_FUNCTIONS.get(blur_type)
    if blur_function:
        return blur_function(image, kernel_size, sigma)
    else:
        raise ValueError(f"Invalid blur type: {blur_type}")
    
class BlurFilter:
    @staticmethod
    def gaussian_blur(image: np.ndarray, kernel_size: int = 5, sigma: int = 5) -> np.ndarray:
        def create_gaussian_kernel(size: int, sigma: int = 1) -> np.ndarray:
            center = (size - 1) / 2
            
            def gaussian_function(x, y):
                exponent = -((x - center)**2 + (y - center)**2) / (2 * sigma**2)
                return (1 / (2 * np.pi * sigma**2)) * np.exp(exponent)
            
            kernel = np.fromfunction(gaussian_function, (size, size))
            return kernel / np.sum(kernel)
        
        kernel = create_gaussian_kernel(kernel_size, sigma)
        return convolution(image, kernel)

    @staticmethod
    def box_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        def create_box_kernel(size: int) -> np.ndarray:
            return np.ones((size, size)) / (size * size)
        
        kernel = create_box_kernel(kernel_size)
        return convolution(image, kernel)

    @staticmethod
    def vertical_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        def create_vertical_kernel(size: int) -> np.ndarray:
            kernel = np.zeros((size, size))
            kernel[:, size // 2] = 1 / size
            return kernel
    
        kernel = create_vertical_kernel(kernel_size)
        return convolution(image, kernel)

def convolution(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    image_height, image_width, channels = image.shape
    kernel_height, kernel_width = kernel.shape

    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    output = np.zeros_like(image)
    
    for c in range(channels):
        padded_image = np.pad(image[:, :, c], ((pad_height, pad_height), (pad_width, pad_width)), mode='reflect')
        
        for i in range(image_height):
            for j in range(image_width):
                region = padded_image[i:i+kernel_height, j:j+kernel_width]
                output[i, j, c] = np.sum(region * kernel)
        
    return output