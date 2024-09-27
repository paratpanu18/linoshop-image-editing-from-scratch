# import cv2
# from tools.gaussian_blur import gaussian_blur

# def main() -> None:
#     image_path: str = "test-image/alya_720x720.jpg"
#     original_image = cv2.imread(image_path)
#     if not original_image.any():
#         raise ValueError(f"Could not read the image from the path: {image_path}")

#     blurred_image = gaussian_blur(original_image, kernel_size=10, sigma=5)

#     cv2.imshow("Original Image", original_image)
#     cv2.imshow("Blurred Image", blurred_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tools.gaussian_blur import gaussian_blur
from tools.grayscale import rgb_to_grayscale

def select_image():
    """Open a file dialog to select an image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if file_path:
        image_path.set(file_path)
        load_image(file_path)

def load_image(image_path):
    """Load and display the selected image."""
    original_image = cv2.imread(image_path)
    if original_image is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    # Convert the image from BGR to RGB for display
    # original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image_display = cv2.resize(original_image, (400, 400))

    cv2.imshow("Original Image", original_image_display)

def apply_blur():
    """Apply Gaussian blur to the image based on user input."""
    path = image_path.get()
    kernel_size = int(blur_radius.get())
    sigma = 5  # You can allow user input for sigma as well if desired

    original_image = cv2.imread(path)
    if original_image is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    blurred_image = gaussian_blur(original_image, kernel_size=kernel_size, sigma=sigma)

    # Convert images from BGR to RGB for display
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    blurred_image_rgb = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)

    original_image_display = cv2.resize(original_image_rgb, (400, 400))
    blurred_image_display = cv2.resize(blurred_image_rgb, (400, 400))

    cv2.imshow("Blurred Image", blurred_image)

def convert_to_grayscale():
    """Convert the selected image to grayscale and display it."""
    path = image_path.get()
    if not path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    original_image = cv2.imread(path)
    if original_image is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    grayscale_image = rgb_to_grayscale(original_image)

    # Resize and display grayscale image
    grayscale_image_display = cv2.resize(grayscale_image, (400, 400))
    cv2.imshow("Grayscale Image", grayscale_image_display)

    # Save the grayscale image for further processing (Gaussian blur)
    global processed_image
    processed_image = grayscale_image

def close_windows():
    """Close all OpenCV windows."""
    cv2.destroyAllWindows()

# Create the main window
root = tk.Tk()
root.title("Gaussian Blur Application")

# StringVar to store image path
image_path = tk.StringVar()

# Frame for controls
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Button to select an image
select_button = ttk.Button(frame, text="Select Image", command=select_image)
select_button.grid(row=0, column=0, pady=5)

# Label and Slider for blur radius
blur_radius_label = ttk.Label(frame, text="Blur Radius (Kernel Size):")
blur_radius_label.grid(row=1, column=0, pady=5)

blur_radius = tk.IntVar(value=5)  # Default value
blur_radius_slider = ttk.Scale(frame, from_=1, to=50, variable=blur_radius, orient=tk.HORIZONTAL)
blur_radius_slider.grid(row=1, column=1, pady=5)

# Button to apply blur
apply_button = ttk.Button(frame, text="Apply Blur", command=apply_blur)
apply_button.grid(row=2, column=0, columnspan=2, pady=10)

# Add button to convert to grayscale
convert_button = ttk.Button(frame, text="Grayscale", command=convert_to_grayscale)
convert_button.grid(row=3, column=0, columnspan=2, pady=5)

# Bind closing event to cleanup
root.protocol("WM_DELETE_WINDOW", close_windows())

# Start the GUI event loop
root.mainloop()
