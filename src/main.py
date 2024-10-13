import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from tools.blur import apply_blur, BlurType
from tools.grayscale import rgb_to_grayscale
from tools.image_filter_color import apply_filter, FilterType
from tools.reshape import apply_circular_mask, apply_heart_mask
from tools.rotate import rotate_image

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
    global original_image, processed_image, original_image_tk

    original_image = cv2.imread(image_path)
    if original_image is None:
        messagebox.showerror("Error", "Could not read the image.")
        return
    
    processed_image = original_image.copy()
    # Convert image to RGB for display in Tkinter
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    original_image_pil = Image.fromarray(original_image_rgb)
    original_image_tk = ImageTk.PhotoImage(original_image_pil.resize((400, 400)))
    
    # Display the original image in the label
    original_label.config(image=original_image_tk)
    processed_label.config(image=original_image_tk)

def toggle_blur():
    """Enable or disable the blur radius slider based on the blur checkbox."""
    if blur_var.get():
        blur_method_label.grid(row=2, column=1, pady=5)
        blur_menu.grid(row=2, column=2, padx=5)
        blur_radius_label.grid(row=3, column=1, pady=5)
        blur_radius_slider.grid(row=3, column=2, pady=5)
    else:
        blur_method_label.grid_remove()
        blur_menu.grid_remove()
        blur_radius_label.grid_remove()
        blur_radius_slider.grid_remove()

def set_loading(loading=True):
    """Show or hide the loading label."""
    if loading:
        loading_label.grid(row=8, column=0, columnspan=2, pady=10)
    else:
        loading_label.grid_remove()

def update_processed_image(image):
    """Update the processed image in the Tkinter label."""
    global processed_image_tk
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    processed_image_tk = ImageTk.PhotoImage(image_pil.resize((400, 400)))
    processed_label.config(image=processed_image_tk)

def run_in_thread(target_func, *args):
    """Run a target function in a separate thread and show loading indicator."""
    def wrapper():
        set_loading(True)
        try:
            target_func(*args)
        finally:
            set_loading(False)
    
    threading.Thread(target=wrapper, daemon=True).start()

def apply_filters():
    """Apply the selected filters and update the processed image."""
    global processed_image
    path = image_path.get()
    if not path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    # Apply grayscale if selected
    if grayscale_var.get():
        processed_image = rgb_to_grayscale(processed_image)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)  # Convert to 3 channels for consistency

    # Apply blur if selected
    if blur_var.get():
        kernel_size = int(blur_radius.get())
        blur_type = BlurType(blur_option.get())
        processed_image = apply_blur(processed_image, blur_type, kernel_size)

    # Apply the selected filter
    selected_filter = filter_option.get()
    if selected_filter != "None":
        filter_type = FilterType(selected_filter)
        processed_image = apply_filter(processed_image, filter_type)

    # Apply shape mask if selected
    if mask_option.get() == "Circle Mask":
        processed_image = apply_circular_mask(processed_image)
    elif mask_option.get() == "Heart Mask":
        processed_image = apply_heart_mask(processed_image)

    update_processed_image(processed_image)

def apply_filters_thread():
    """Wrapper to apply filters in a separate thread."""
    run_in_thread(apply_filters)

def apply_rotate_image(angle: float = 0):
    """Rotate the image."""
    global processed_image
    path = image_path.get()
    if not path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    processed_image = rotate_image(original_image.copy(), angle)
    update_processed_image(processed_image)

def apply_rotate_image_thread(angle):
    """Wrapper to rotate image in a separate thread."""
    run_in_thread(apply_rotate_image, angle)

def preview_original(event):
    """Preview the original image when the button is pressed."""
    original_label.config(image=original_image_tk)
    processed_label.config(image=original_image_tk)

def show_processed_image(event):
    """Show the processed image again when the button is released."""
    update_processed_image(processed_image)

def close_windows():
    """Close all OpenCV windows and quit the application."""
    cv2.destroyAllWindows()
    root.quit()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Filter Image Application")

# StringVar to store image path
image_path = tk.StringVar()
blur_option = tk.StringVar()
filter_option = tk.StringVar()
mask_option = tk.StringVar()

# Variables to control checkboxes
grayscale_var = tk.BooleanVar()
blur_var = tk.BooleanVar()

# Frame for controls
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Button to select an image
select_button = ttk.Button(frame, text="Select Image", command=select_image)
select_button.grid(row=0, column=0, pady=5)

# Grayscale checkbox
grayscale_checkbox = ttk.Checkbutton(frame, text="Grayscale", variable=grayscale_var)
grayscale_checkbox.grid(row=1, column=0, pady=5)

# Blur checkbox and slider
blur_checkbox = ttk.Checkbutton(frame, text="Apply Blur", variable=blur_var, command=toggle_blur)
blur_checkbox.grid(row=2, column=0, pady=5)

blur_method_label = ttk.Label(frame, text="Select Blur Method:")
blur_method_label.grid(row=2, column=1, pady=5)

blur_menu = ttk.OptionMenu(frame, blur_option, "Gaussian Blur", "Gaussian Blur", "Box Blur", "Vertical Blur")
blur_menu.grid(row=2, column=2, padx=5)

blur_radius_label = ttk.Label(frame, text="Blur Radius (Kernel Size):")
blur_radius_label.grid(row=3, column=0, pady=5)

blur_radius = tk.IntVar(value=25)  # Default value
blur_radius_slider = ttk.Scale(frame, from_=1, to=50, variable=blur_radius, orient=tk.HORIZONTAL)
blur_radius_slider.grid(row=3, column=1, pady=5)

# Initially hide the blur options
blur_method_label.grid_remove()
blur_menu.grid_remove()
blur_radius_label.grid_remove()
blur_radius_slider.grid_remove()

# Dropdown for filter selection
filter_label = ttk.Label(frame, text="Select a Filter:")
filter_label.grid(row=4, column=0, pady=5)
filter_menu = ttk.OptionMenu(frame, filter_option, "None", "None", "Cool Tone", "Warm Tone", "Vintage Tone", "High Contrast", "Invert", "Outline")
filter_menu.grid(row=4, column=1, padx=5)

# Dropdown for shape mask selection
mask_label = ttk.Label(frame, text="Select a Mask:")
mask_label.grid(row=5, column=0, pady=5)
mask_menu = ttk.OptionMenu(frame, mask_option, "None", "None", "Circle Mask", "Heart Mask")
mask_menu.grid(row=5, column=1)

# Rotate image
rotate_label = ttk.Label(frame, text="Rotate Image:")
rotate_label.grid(row=6, column=0, pady=5)
rotate_left_button = ttk.Button(frame, text="Rotate Left", command=lambda: apply_rotate_image_thread(-90))
rotate_left_button.grid(row=6, column=1, padx=5)

rotate_right_button = ttk.Button(frame, text="Rotate Right", command=lambda: apply_rotate_image_thread(90))
rotate_right_button.grid(row=6, column=2, padx=5)

# Button to apply filters
apply_button = ttk.Button(frame, text="Apply Filters", command=apply_filters_thread)
apply_button.grid(row=7, column=0, pady=10)

# Loading label (hidden by default)
loading_label = ttk.Label(root, text="Processing...", foreground="red")
loading_label.grid_remove()

# Labels to show original and processed images
original_label = ttk.Label(root)
original_label.grid(row=1, column=0)

processed_label = ttk.Label(root)
processed_label.grid(row=1, column=1)

# Bind closing event to cleanup
root.protocol("WM_DELETE_WINDOW", close_windows)

# Start the GUI event loop
root.mainloop()