import tkinter as tk
from PIL import Image, ImageTk

# Initialize Tkinter window
root = tk.Tk()
root.title("Image Toggle Button")

# Load the background image and set as the window background
background_image_path = "backgroundbilly.png"
background_image = Image.open(background_image_path)
background_width, background_height = background_image.size
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load and resize images for the button, keep a reference at the module level to avoid garbage collection
global image1_photo, image2_photo
image1 = Image.open("blackplane.png")
image1 = image1.resize((50, 50), Image.Resampling.LANCZOS)
image1_photo = ImageTk.PhotoImage(image1)

image2 = Image.open("yellowplane.png")
image2 = image2.resize((50, 50), Image.Resampling.LANCZOS)
image2_photo = ImageTk.PhotoImage(image2)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height}")

# Use global variable to keep track of which image is currently shown
global toggle_image
toggle_image = False

# Function to change the button's image and open a form
def on_button_press():
    global toggle_image, image1_photo, image2_photo
    toggle_image = not toggle_image
    button.config(image=(image2_photo if toggle_image else image1_photo))
    # ... rest of the function

# ... rest of the code including `on_form_close` function

# Create a pressable button that changes its image
button = tk.Button(root, image=image1_photo, command=on_button_press)
button.place(x=30, y=120)
button = tk.Button(root, image=image1_photo, command=on_button_press)
button.place(x=30, y=260)

# Start the Tkinter event loop
root.mainloop()