import tkinter as tk
import time
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from functools import partial
import pandas as pd
from datetime import datetime

# Load the flight information from the CSV file
df = pd.read_csv("Flight info.csv")  # Adjust the path to your CSV file

# Initialize Tkinter window
root = tk.Tk()
root.title("Billy Bishop Universal Airport Management System")

# Load the background image and set as the window background
background_image_path = "backgroundbilly.png"  # Adjust the path to your background image
background_image = Image.open(background_image_path)
background_width, background_height = background_image.size
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load and resize images for the buttons
image1 = Image.open("airplaneicon.jpg")  # Adjust the path to your airplane icon
image1 = image1.resize((50, 64), Image.Resampling.LANCZOS)
image1_photo = ImageTk.PhotoImage(image1)

image2 = Image.open("airplaneiconblk.jpg")  # Adjust the path to your alternate airplane icon
image2 = image2.resize((50, 64), Image.Resampling.LANCZOS)
image2_photo = ImageTk.PhotoImage(image2)

# Set the root window size to match the background image
root.geometry(f"{background_width}x{background_height + 30}")

# Dictionary to keep track of windows
open_windows = {}


def is_flight_time_now(boarding_time_str, departure_time_str):
    current_time = datetime.now().time()
    boarding_time = datetime.strptime(boarding_time_str, '%H:%M:%S').time()
    departure_time = datetime.strptime(departure_time_str, '%H:%M:%S').time()
    return boarding_time <= current_time <= departure_time

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

def open_info_window(gate_number):
    # Ensure the button does not change the icon upon being pressed
    if gate_number not in open_windows or not open_windows[gate_number].winfo_exists():
        info_window = tk.Toplevel(root)
        info_window.title(f"Flight Information for Gate {gate_number}")
        open_windows[gate_number] = info_window

        tree = ttk.Treeview(info_window,
                            columns=('Boarding Time', 'Departure Time', 'Airline', 'Destination', 'Status', 'New Gate'),
                            show='headings')
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

        # Remove the window from the dictionary when it is closed
        def on_close(gate_number=gate_number, window=info_window):
            window.destroy()  # Destroy the window
            open_windows.pop(gate_number, None)  # Remove its reference from the dictionary

            # Set the protocol for the window close button ('X')

        info_window.protocol("WM_DELETE_WINDOW", on_close)


# Prepare gate buttons
gate_buttons = {}
button_positions = [
    (30, 120), (30, 260), (30, 365), (145, 390),
    (305, 445), (470, 500), (715, 580), (830, 615),
    (940, 560), (950, 460), (945, 325),
]

for i, position in enumerate(button_positions, start=1):
    button = tk.Button(root, image=image1_photo, command=partial(open_info_window, i))
    button.place(x=position[0], y=position[1])
    label = tk.Label(root, text=f"Gate {i}")
    label.place(x=position[0] + 60, y=position[1] + 20)
    gate_buttons[i] = button  # Store the button with its gate number for easy reference


def update_icons():
    current_time_str = datetime.now().strftime('%H:%M:%S')
    for gate_number, button in gate_buttons.items():
        matching_flights = df[df['Gate Number'] == gate_number]
        if not matching_flights.empty:
            flight = matching_flights.iloc[0]
            if is_flight_time_now(flight['Boarding Time'], flight['Departure Time']):
                button.config(image=image2_photo)
            else:
                button.config(image=image1_photo)
        else:
            # Optional: Update button configuration for gates with no flights
            # For example, you could disable the button or change its appearance
            pass
    root.after(1000, update_icons)  # Check every second for updates


def check_flight_times():
    current_time = datetime.now().strftime('%H:%M:%S')
    for index, flight in df.iterrows():
        boarding_time = datetime.strptime(flight['Boarding Time'], '%H:%M:%S').time()
        departure_time = datetime.strptime(flight['Departure Time'], '%H:%M:%S').time()
        current_time_dt = datetime.strptime(current_time, '%H:%M:%S').time()
        gate_number = flight['Gate Number']
        if gate_number in gate_buttons:
            button = gate_buttons[gate_number]
            # Change icon based on boarding and departure times
            if boarding_time <= current_time_dt < departure_time:
                button.config(image=image2_photo)  # Occupied
            else:
                button.config(image=image1_photo)  # Vacant or after departure
    root.after(60000, check_flight_times)  # Check every minute


def update_time():
    current_time = time.strftime('%H:%M:%S')
    time_label.config(text="Current Time: " + current_time)
    root.after(1000, update_time)  # Update the time every second


# Display the current time at the bottom left
time_label = tk.Label(root, font=('Helvetica', 20), bg='white', text='')
time_label.place(x=10, y=background_height - 30)

update_icons()
update_time()  # Start the clock
check_flight_times()  # Start checking flight times to update icons

# Keep references to the PhotoImage objects to prevent garbage collection
image_references = [image1_photo, image2_photo]

root.mainloop()
