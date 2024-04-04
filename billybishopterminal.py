import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from functools import partial

# Initialize Tkinter window
root = tk.Tk()
root.title("Billy Bishop Universal Airport Management System")

# Load the background image and set as the window background
background_image_path = "backgroundbilly.png"
background_image = Image.open(background_image_path)
background_width, background_height = background_image.size
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height+30}")

# Load and resize images for the button statuses
status_images = {
    'Vacant': ImageTk.PhotoImage(Image.open("airplaneiconb.jpg").resize((50, 64), Image.Resampling.LANCZOS)),
    'Occupied': ImageTk.PhotoImage(Image.open("airplaneiconblk.jpg").resize((50, 64), Image.Resampling.LANCZOS)),
    'Delayed': ImageTk.PhotoImage(Image.open("airplaneiconblu.jpg").resize((50, 64), Image.Resampling.LANCZOS)),
}

# Function to update the button image based on the combobox selection
def update_button_image(event, button, combobox):
    status = combobox.get()
    button.config(image=status_images[status])
    combobox.destroy()  # Remove the combobox after selection

# Function to display the combobox when the button is clicked
def on_button_click(button):
    combobox = ttk.Combobox(root, values=list(status_images.keys()), state='readonly')
    combobox.bind('<<ComboboxSelected>>', partial(update_button_image, button=button, combobox=combobox))
    combobox.place(x=button.winfo_x(), y=button.winfo_y() + 60)  # Position below the button

# Create and place buttons on the window
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
]


buttons = []
for position in button_positions:
    button = tk.Button(root, image=list(status_images.values())[0])  # Use the first status image as default
    button.config(command=partial(on_button_click, button))
    button.place(x=position[0], y=position[1])
    buttons.append(button)

# Function to update the time
def update_time():
    current_time = time.strftime('%H:%M:%S')  # Military time format
    time_label.config(text=current_time)
    root.after(1000, update_time)

# Display the time
time_label = tk.Label(root, font=('Helvetica', 20), bg='white', fg='black')
time_label.place(x=10, y=background_height - 30)
update_time()

# Start the Tkinter event loop
root.mainloop()