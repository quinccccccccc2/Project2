import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

# Function to change the button's image and open a form
def on_button_press():
    global toggle_image
    toggle_image = not toggle_image
    button.config(image=(image2 if toggle_image else image1))

    # Open a new window with a form directly without checking if one is already open
    if toggle_image:  # Only opens the form when the plane is black again
        form_window = tk.Toplevel(root)
        form_window.title("Fillable Form")
        tk.Label(form_window, text="Flight number").pack()

        entry = tk.Entry(form_window)
        entry.pack()

        # Disable the button to prevent opening multiple forms
        button.config(state='disabled')

        # Re-enable the button when the form window is closed
        form_window.protocol("WM_DELETE_WINDOW", lambda: on_form_close(form_window))


def on_form_close(form_window):
    """Re-enable the button and destroy the form window."""
    button.config(state='normal')
    form_window.destroy()


# Initialize Tkinter window
root = tk.Tk()
root.title("Image Toggle Button")

# Load the background image
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load and resize images for the button
image1 = Image.open("blackplane.png")
image1 = image1.resize((10, 10), Image.Resampling.LANCZOS)
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open("yellowplane.png")
image2 = image2.resize((10, 10), Image.Resampling.LANCZOS)
image2 = ImageTk.PhotoImage(image2)

toggle_image = False  # Track which image is currently shown

# Create a pressable button that changes its image
button = tk.Button(root, image=image1, command=on_button_press)
button.pack()

# Start the Tkinter event loop
root.mainloop()