import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import pandas as pd
import time
from functools import partial

# Load the flight information from the CSV file (adjust path as needed)
df = pd.read_csv("Flight info.csv")

# Initialize Tkinter window
root = tk.Tk()
root.title("Billy Bishop Universal Airport Management System")

# Load the background image and set as the window background
background_image_path = "backgroundbilly.png"  # Adjust path as needed
background_image = Image.open(background_image_path)
background_width, background_height = background_image.size
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load and resize images for the buttons
image1 = Image.open("airplaneicon.jpg")  # Adjust path as needed
image1 = image1.resize((50, 64), Image.Resampling.LANCZOS)
image1_photo = ImageTk.PhotoImage(image1)

image2 = Image.open("airplaneiconblk.jpg")  # Adjust path as needed
image2 = image2.resize((50, 64), Image.Resampling.LANCZOS)
image2_photo = ImageTk.PhotoImage(image2)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height+30}")

def close_window(gate_number, button, image1_photo):
    open_windows[gate_number].destroy()
    button.config(image=image1_photo)

def delay_flight(tree):
    selected_item = tree.selection()[0] if tree.selection() else None
    if selected_item:
        item = tree.item(selected_item)
        original_values = item['values']

        # Request new values
        new_boarding = simpledialog.askstring("Update Boarding Time", "Enter new boarding time (HH:MM):", parent=tree)
        new_departure = simpledialog.askstring("Update Departure Time", "Enter new departure time (HH:MM):", parent=tree)
        new_gate = simpledialog.askstring("Update Gate Number", "Enter new gate (if unchanged, press Cancel):", parent=tree)

        # Determine if any value has changed
        values_changed = False
        new_values = list(original_values)  # Copy to a new list for potential modification

        if new_boarding and new_boarding != original_values[0]:
            new_values[0] = new_boarding
            values_changed = True
        if new_departure and new_departure != original_values[1]:
            new_values[1] = new_departure
            values_changed = True
        if new_gate and new_gate != str(original_values[-1]):  # Assuming gate number is the last value
            new_values[-1] = new_gate
            values_changed = True

        # If any value changed, update the item with new values and apply the 'modified' tag
        if values_changed:
            tree.item(selected_item, values=new_values, tags='modified')

def toggle_flight_info(button, gate_number, image1_photo, image2_photo):
    if gate_number in open_windows and open_windows[gate_number].winfo_exists():
        open_windows[gate_number].destroy()
        del open_windows[gate_number]
        button.config(image=image1_photo)
    else:
        info_window = tk.Toplevel(root)
        info_window.title(f"Flight Information for Gate {gate_number}")
        open_windows[gate_number] = info_window
        button.config(image=image2_photo)

        tree = ttk.Treeview(info_window, columns=('Boarding Time', 'Departure Time', 'Airline', 'Destination', 'Status', 'New Gate'), show='headings')
        tree.heading('Boarding Time', text='Boarding Time')
        tree.heading('Departure Time', text='Departure Time')
        tree.heading('Airline', text='Airline')
        tree.heading('Destination', text='Destination')
        tree.heading('Status', text='Status')
        tree.heading('New Gate', text='New Gate')

        # Filter flights for this gate and assume all flights are initially "On-Time"
        gate_flights = df[df['Gate Number'] == gate_number]
        for index, flight in gate_flights.iterrows():
            tree.insert('', tk.END, values=(flight['Boarding Time'], flight['Departure Time'], flight['Airline Name'], flight['Destination'], "On-Time", ""))

        tree.pack(expand=True, fill='both')

        # Delay button
        delay_button = tk.Button(info_window, text="Delay", command=lambda: delay_flight(tree))
        delay_button.pack(side=tk.BOTTOM, anchor=tk.E)

def update_time():
    current_time = time.strftime('%H:%M:%S')
    time_label.config(text=current_time)
    root.after(1000, update_time)

time_label = tk.Label(root, font=('Helvetica', 20), bg='white')
time_label.place(x=10, y=background_height-30)

update_time()

# Define button positions for the gates
button_positions = [
    (30, 120), (30, 260), (30, 365), (145, 390),
    (305, 445), (470, 500), (715, 580), (830, 615),
    (940, 560), (950, 460), (945, 325),
]

open_windows = {}

for i, position in enumerate(button_positions, start=1):
    button = tk.Button(root, image=image1_photo)
    command = partial(toggle_flight_info, button, i, image1_photo, image2_photo)
    button.config(command=command)
    button.place(x=position[0], y=position[1])
    label = tk.Label(root, text=f"Gate {i}", bg="white")
    label.place(x=position[0], y=position[1] + 70)

# Keep references to the PhotoImage objects to prevent garbage collection
image_references = [image1_photo, image2_photo]

root.mainloop()
