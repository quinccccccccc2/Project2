import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
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

# Load and resize images for the buttons
image1 = Image.open("blackplane.png")
image1 = image1.resize((50, 50), Image.Resampling.LANCZOS)
image1_photo = ImageTk.PhotoImage(image1)

image2 = Image.open("yellowplane.png")
image2 = image2.resize((50, 50), Image.Resampling.LANCZOS)
image2_photo = ImageTk.PhotoImage(image2)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height+30}")

# Dictionary to keep track of windows
open_windows = {}

# Function to open or close the flight information window
def toggle_flight_info(button, gate_number, image1_photo, image2_photo):
    # Close the window if already open
    if gate_number in open_windows and open_windows[gate_number].winfo_exists():
        open_windows[gate_number].destroy()
        open_windows.pop(gate_number, None)
        button.config(image=image1_photo)  # Revert button image
    else:
        # Open a new information window
        info_window = tk.Toplevel(root)
        info_window.title(f"Flight Information for Gate {gate_number}")
        open_windows[gate_number] = info_window  # Track the window
        button.config(image=image2_photo)  # Change button image

        # Set the window to revert button image when closed
        info_window.protocol("WM_DELETE_WINDOW", partial(close_window, gate_number, button, image1_photo))

        # Create and populate the Treeview with flight information
        tree = ttk.Treeview(info_window, columns=('Boarding Time', 'Departure Time', 'Airline', 'Destination', 'Delay', 'New Gate'), show='headings')
        tree.heading('Boarding Time', text='Boarding Time')
        tree.heading('Departure Time', text='Departure Time')
        tree.heading('Airline', text='Airline')
        tree.heading('Destination', text='Destination')
        tree.heading('Delay', text='Delay')
        tree.heading('New Gate', text='New Gate')

        # Sample flight information
        flights_info = [
            ('12:00 PM', '1:00 PM', 'Example Airline 1', 'New York', '', ''),
            ('3:00 PM', '4:00 PM', 'Example Airline 2', 'Los Angeles', 'Delayed', 'Gate 5'),
            # Add more sample or dynamic flight information here
        ]

        for flight in flights_info:
            tag = ('delayed',) if flight[4] else ()  # Tag for styling delayed flights
            tree.insert('', tk.END, values=flight, tags=tag)

        tree.tag_configure('delayed', foreground='red')  # Style for delayed flights
        tree.pack(expand=True, fill='both')

def close_window(gate_number, button, image1_photo):
    if gate_number in open_windows:
        open_windows[gate_number].destroy()
        open_windows.pop(gate_number, None)
    button.config(image=image1_photo)

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
]

# Create and place buttons on the window
for i, position in enumerate(button_positions, start=1):
    button = tk.Button(root, image=image1_photo)
    command = partial(toggle_flight_info, button, i, image1_photo, image2_photo)
    button.config(command=command)
    button.place(x=position[0], y=position[1])
    label = tk.Label(root, text=f"Gate {i}")
    label.place(x=position[0] + 9, y=position[1] + 60)

# Keep references to the PhotoImage objects to prevent garbage collection
image_references = [image1_photo, image2_photo]

# Start the Tkinter event loop
root.mainloop()
