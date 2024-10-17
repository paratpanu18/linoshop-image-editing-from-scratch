import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk  # For modern themes
from PIL import Image, ImageTk

from tools.blur import apply_blur, BlurType
from tools.grayscale import rgb_to_grayscale
from tools.image_filter_color import apply_filter, FilterType
from tools.reshape import apply_mask, MaskType
from tools.rotate import rotate_image
from tools.cosine_similarity import cosine_similarity

filter_list = [filter.value for filter in FilterType]
blur_option_list = [blur.value for blur in BlurType]
mask_list = [mask.value for mask in MaskType]

undo_stack = []
redo_stack = []

def save_to_undo():
    """Save the current processed image state to the undo stack."""
    global undo_stack
    undo_stack.append(processed_image.copy())
    if len(undo_stack) > 10:  # Limit history to 10 states (optional)
        undo_stack.pop(0)

def undo():
    """Undo the last operation by popping from the undo stack."""
    global processed_image, redo_stack
    if undo_stack:
        redo_stack.append(processed_image.copy())
        processed_image = undo_stack.pop()
        update_processed_image(processed_image)

def redo():
    """Redo the last undone operation by popping from the redo stack."""
    global processed_image
    if redo_stack:
        undo_stack.append(processed_image.copy())
        processed_image = redo_stack.pop()
        update_processed_image(processed_image)
        
def preview_original(event):
    """Preview the original image when the mouse hovers over the image."""
    previwed_image.config(image=original_image_tk)

def show_processed_image(event):
    """Show the processed image again when the mouse leaves the image."""
    previwed_image.config(image=processed_image_tk)

def select_image():
    """Open a file dialog to select an image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if file_path:
        image_path.set(file_path)
        load_image(file_path)

def resize_with_aspect_ratio(image, max_height=400):
    """Resize an image while maintaining its aspect ratio, with a max height of 400px."""
    h, w = image.shape[:2]
    if h > max_height:
        aspect_ratio = w / h
        new_height = max_height
        new_width = int(aspect_ratio * new_height)
        return cv2.resize(image, (new_width, new_height))
    return image

def load_image(image_path):
    """Load and display the selected image."""
    global original_image, processed_image, original_image_tk

    original_image = cv2.imread(image_path)
    if original_image is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    processed_image = original_image.copy()
    
    # Resize while maintaining the aspect ratio
    resized_original = resize_with_aspect_ratio(original_image)
    original_image_rgb = cv2.cvtColor(resized_original, cv2.COLOR_BGR2RGB)
    original_image_pil = Image.fromarray(original_image_rgb)
    original_image_tk = ImageTk.PhotoImage(original_image_pil)
    
    # Display the original image in the label
    previwed_image.config(image=original_image_tk)

def toggle_blur():
    """Enable or disable the blur method dropdown and blur radius slider based on the blur checkbox."""
    if blur_var.get():
        blur_menu.configure(state="normal")
        blur_radius_slider.configure(state="normal")
    else:
        blur_menu.configure(state="disabled")
        blur_radius_slider.configure(state="disabled")


def set_loading(loading=True):
    """Show or hide the loading label."""
    if loading:
        loading_label.grid(row=8, column=0, columnspan=2, pady=10)
    else:
        loading_label.grid_remove()

def update_processed_image(image):
    """Update the processed image in the Tkinter label."""
    global processed_image_tk
    # Resize while maintaining the aspect ratio
    resized_image = resize_with_aspect_ratio(image)
    image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    processed_image_tk = ImageTk.PhotoImage(image_pil)
    previwed_image.config(image=processed_image_tk)

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
    
    # Save the current state for undo before applying any filter
    save_to_undo()

    # Clear redo stack when a new filter is applied
    redo_stack.clear()

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
    if mask_option.get() != "None":
        mask_type = MaskType(mask_option.get())
        processed_image = apply_mask(processed_image, mask_type)

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

    processed_image = rotate_image(processed_image.copy(), angle)
    update_processed_image(processed_image)

def apply_rotate_image_thread(angle):
    """Wrapper to rotate image in a separate thread."""
    run_in_thread(apply_rotate_image, angle)

def calculate_cosine_similarity():
    """Calculate the cosine similarity between the original and processed image."""
    global original_image, processed_image
    if original_image is None:
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    similarity = cosine_similarity(original_image, processed_image)
    cosine_similarity_label.config(text=f"Cosine Similarity: {similarity:.4f} - {similarity * 100:.2f}%")

    
def preview_original(event):
    """Preview the original image when the button is pressed."""
    previwed_image.config(image=original_image_tk)

def show_processed_image(event):
    """Show the processed image again when the button is released."""
    update_processed_image(processed_image)
    
def save_image():
    """Save the processed image to a file."""
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")]
    )
    if path:
        cv2.imwrite(path, processed_image)
        messagebox.showinfo("Success", "Image saved successfully.")

def close_windows():
    """Close all OpenCV windows and quit the application."""
    cv2.destroyAllWindows()
    root.quit()
    root.destroy()

# Initialize the main window with a modern theme
root = ThemedTk(theme="arc")
root.title("Linoshop | Image Editing Software from Scratch")
root.geometry("1280x720")
root.configure(bg='#f5f5f5')  # Light grey background for modern feel

# Style Configurations
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 12), background='#f5f5f5')
style.configure('TCheckbutton', font=('Helvetica', 12), background='#f5f5f5')

# StringVar to store image path and options
image_path = tk.StringVar()
blur_option = tk.StringVar()
filter_option = tk.StringVar()
mask_option = tk.StringVar()

# Variables to control checkboxes
grayscale_var = tk.BooleanVar()
blur_var = tk.BooleanVar()

# Configure grid for root window with 2 columns
root.grid_columnconfigure(0, weight=1)  # Left side (tools)
root.grid_columnconfigure(1, weight=3)  # Right side (image preview)

# Frame for controls (Tools on the left side)
tools_frame = ttk.Frame(root, padding=20)
tools_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10, pady=10)

# Button to select an image with an icon (use any relevant icon you have)
select_button = ttk.Button(tools_frame, text="📂 Select Image", command=select_image)
select_button.grid(row=0, column=0, pady=10)

# Undo and Redo Buttons
undo_button = ttk.Button(tools_frame, text="↩️ Undo", command=undo)
undo_button.grid(row=0, column=1, pady=10)

redo_button = ttk.Button(tools_frame, text="↪️ Redo", command=redo)
redo_button.grid(row=0, column=2, pady=10)

# Grayscale checkbox
grayscale_checkbox = ttk.Checkbutton(tools_frame, text="🖤 Grayscale", variable=grayscale_var)
grayscale_checkbox.grid(row=1, column=0, pady=10)

# Blur checkbox and slider
blur_checkbox = ttk.Checkbutton(tools_frame, text="💨 Apply Blur", variable=blur_var, command=toggle_blur)
blur_checkbox.grid(row=2, column=0, pady=10)

blur_method_label = ttk.Label(tools_frame, text="Blur Method:")
blur_method_label.grid(row=2, column=1, pady=10)

blur_menu = ttk.OptionMenu(tools_frame, blur_option, "Gaussian Blur", *blur_option_list)
blur_menu.grid(row=2, column=2, padx=5)

blur_radius_label = ttk.Label(tools_frame, text="Blur Radius:")
blur_radius_label.grid(row=3, column=2, pady=10)

blur_radius = tk.IntVar(value=25)  # Default value
blur_radius_slider = ttk.Scale(tools_frame, from_=1, to=50, variable=blur_radius, orient=tk.HORIZONTAL)
blur_radius_slider.grid(row=3, column=3, pady=10)

blur_menu.configure(state="disabled")
blur_radius_slider.configure(state="disabled")

# Initially hide blur options
# blur_method_label.grid_remove()
# blur_menu.grid_remove()
# blur_radius_label.grid_remove()
# blur_radius_slider.grid_remove()

# Filter Dropdown
filter_label = ttk.Label(tools_frame, text="Filter:")
filter_label.grid(row=4, column=0, pady=10)

filter_menu = ttk.OptionMenu(tools_frame, filter_option, "None", "None", *filter_list)
filter_menu.grid(row=4, column=1, padx=5)

# Mask Dropdown
mask_label = ttk.Label(tools_frame, text="Mask:")
mask_label.grid(row=5, column=0, pady=10)

mask_menu = ttk.OptionMenu(tools_frame, mask_option, "None", "None", *mask_list)
mask_menu.grid(row=5, column=1)

# Rotate Buttons
rotate_label = ttk.Label(tools_frame, text="Rotate Image:")
rotate_label.grid(row=6, column=0, pady=10)

rotate_left_button = ttk.Button(tools_frame, text="⏪ Rotate Left", command=lambda: apply_rotate_image_thread(90))
rotate_left_button.grid(row=6, column=1, padx=5)

rotate_right_button = ttk.Button(tools_frame, text="⏩ Rotate Right", command=lambda: apply_rotate_image_thread(-90))
rotate_right_button.grid(row=6, column=2, padx=5)

# Apply Button
apply_button = ttk.Button(tools_frame, text="✨ Apply Filters", command=apply_filters_thread)
apply_button.grid(row=7, column=0, pady=20)

save_button = ttk.Button(tools_frame, text="💾 Save Image", command=save_image)
save_button.grid(row=7, column=1, pady=20)

# Button to calculate cosine similarity
cosine_button = ttk.Button(tools_frame, text="📊 Cosine Similarity", command= calculate_cosine_similarity )
cosine_button.grid(row=8, column=1, pady=10)

# Label to show cosine similarity value
cosine_similarity_label = ttk.Label(tools_frame, text="Cosine Similarity: N/A")
cosine_similarity_label.grid(row=8, column=2, pady=10, padx=10)



# Frame for image preview on the right side
image_frame = ttk.Frame(root, padding=20)
image_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10, pady=10)

# Preview label (Processed Image Display)
previwed_image = ttk.Label(image_frame, borderwidth=2, relief="solid")
previwed_image.grid(row=0, column=0, padx=20, pady=20)

previwed_image.bind("<Enter>", preview_original)
previwed_image.bind("<Leave>", show_processed_image)

# Loading Label
loading_label = ttk.Label(image_frame, text="Processing...", foreground="red", font=('Helvetica', 12, 'bold'))
loading_label.grid_remove()

# Bind closing event to cleanup
root.protocol("WM_DELETE_WINDOW", close_windows)

# Start the GUI event loop
root.mainloop()