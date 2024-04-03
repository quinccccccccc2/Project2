import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

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

# Load and resize images for the buttons
image1 = Image.open("blackplane.png")
image1 = image1.resize((50, 50), Image.Resampling.LANCZOS)
image1_photo = ImageTk.PhotoImage(image1)

image2 = Image.open("yellowplane.png")
image2 = image2.resize((50, 50), Image.Resampling.LANCZOS)
image2_photo = ImageTk.PhotoImage(image2)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height}")

# Function to change the button's image
def on_button_press(button, image1_photo, image2_photo):
    current_image = button.cget('image')
    new_image = image2_photo if current_image == str(image1_photo) else image1_photo
    button.config(image=new_image)

# List of button positions
button_positions = [
    (30, 120),
    (30, 260),
    (30, 365),
    (145, 390),
    (305, 445),
    (470, 500),
    (715, 580),
    (830, 615),
    (940, 560),
    (950, 460),
    (945, 325),
    # Add more tuples for each button you want to add, like:
    # (x_position, y_position),
]

# Create and place buttons on the window
buttons = []
for position in button_positions:
    button = tk.Button(root, image=image1_photo)
    command = partial(on_button_press, button, image1_photo, image2_photo)
    button.config(command=command)
    button.place(x=position[0], y=position[1])
    buttons.append(button)

# Keep references to the PhotoImage objects to prevent garbage collection
image_references = [image1_photo, image2_photo]

# Start the Tkinter event loop
root.mainloop()