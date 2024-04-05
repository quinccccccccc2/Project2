import tkinter as tk
import time
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial
import pandas as pd

# Load the flight information from the CSV file
df = pd.read_csv("Flight info.csv")

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
image1 = Image.open("airplaneicon.jpg")
image1 = image1.resize((50, 64), Image.Resampling.LANCZOS)
image1_photo = ImageTk.PhotoImage(image1)

image2 = Image.open("airplaneiconblk.jpg")
image2 = image2.resize((50, 64), Image.Resampling.LANCZOS)
image2_photo = ImageTk.PhotoImage(image2)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height+30}")

# Dictionary to keep track of windows
open_windows = {}

def close_window(gate_number, button, image1_photo):
    if gate_number in open_windows:
        open_windows[gate_number].destroy()
        open_windows.pop(gate_number, None)
    button.config(image=image1_photo)

# Function to open or close the flight information window
def toggle_flight_info(button, gate_number, image1_photo, image2_photo):
    if gate_number in open_windows and open_windows[gate_number].winfo_exists():
        open_windows[gate_number].destroy()
        open_windows.pop(gate_number, None)
        button.config(image=image1_photo)
    else:
        info_window = tk.Toplevel(root)
        info_window.title(f"Flight Information for Gate {gate_number}")
        open_windows[gate_number] = info_window
        button.config(image=image2_photo)

        info_window.protocol("WM_DELETE_WINDOW", partial(close_window, gate_number, button, image1_photo))

        tree = ttk.Treeview(info_window, columns=('Boarding Time', 'Departure Time', 'Airline', 'Destination'), show='headings')
        tree.heading('Boarding Time', text='Boarding Time')
        tree.heading('Departure Time', text='Departure Time')
        tree.heading('Airline', text='Airline')
        tree.heading('Destination', text='Destination')

        # Filter flights for this gate
        gate_flights = df[df['Gate Number'] == gate_number]
        for index, flight in gate_flights.iterrows():
            tree.insert('', tk.END, values=(flight['Boarding Time'], flight['Departure Time'], flight['Airline Name'], flight['Destination']))

        tree.pack(expand=True, fill='both')

def update_time():
    current_time = time.strftime('%H:%M:%S')
    time_label.config(text=current_time)
    root.after(1000, update_time)

time_label = tk.Label(root, font=('Helvetica', 20), bg='white')
time_label.place(x=10, y=background_height-30)

update_time()

button_positions = [
    (30, 120), (30, 260), (30, 365), (145, 390),
    (305, 445), (470, 500), (715, 580), (830, 615),
    (940, 560), (950, 460), (945, 325),
]

for i, position in enumerate(button_positions, start=1):
    button = tk.Button(root, image=image1_photo)
    command = partial(toggle_flight_info, button, i, image1_photo, image2_photo)
    button.config(command=command)
    button.place(x=position[0], y=position[1])
    label = tk.Label(root, text=f"Gate {i}")
    label.place(x=position[0] + 60, y=position[1] + 70)

# Keep references to the PhotoImage objects to prevent garbage collection
image_references = [image1_photo, image2_photo]

root.mainloop()
