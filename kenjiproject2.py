import csv
import time
import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import ttk, simpledialog

import pandas as pd
from PIL import Image, ImageTk

# Load the flight information from the CSV file
flight_info = pd.read_csv("Updated_Flight_Schedule3.csv")  # Adjust the path to your CSV file
def clear_csv_file(file_path):
    print(f"Clearing file: {file_path}")
    try:
        with open(file_path, 'w') as file:
            headers = "Airline Name,Flight Number,Plane Model,Boarding Time,Departure Time,Gate Number,Destination\n"
            file.write(headers)
        print("File cleared successfully.")
    except Exception as e:
        print(f"Failed to clear file: {e}")
clear_csv_file("Temp flight file.csv")
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

        # Capture new boarding time, departure time, and gate number via dialogues
        new_boarding = simpledialog.askstring("Update Boarding Time", "Enter new boarding time (HH:MM):", parent=tree)
        new_departure = simpledialog.askstring("Update Departure Time", "Enter new departure time (HH:MM):", parent=tree)
        new_gate = None
        while True:
            temp_gate = simpledialog.askstring("Update Gate number", "Enter gate number (1-11):", parent=tree)
            try:
                if temp_gate is not None and 1<= int(temp_gate) <= 11:
                    new_gate = temp_gate
                    break
                else:
                    print("ERROR: INVALID GATE")
            except ValueError:
                print("ERROR: PLEASE INPUT A VALID GATE NUMBER")
        # Initialize a flag to track any value change
        values_changed = False
        new_values = list(original_values)

        # Update boarding time if changed
        if new_boarding and new_boarding != original_values[0]:
            new_values[0] = new_boarding
            values_changed = True

        # Update departure time if changed
        if new_departure and new_departure != original_values[1]:
            new_values[1] = new_departure
            values_changed = True

        # Update gate if changed
        if new_gate:
            try:
                if new_gate != str(original_values[5]):
                    new_values[5] = new_gate
                    values_changed = True
            except IndexError:
                print("IndexError: 'New Gate' not found")

        # Apply the update if any value changed
        if values_changed:
            tree.item(selected_item, values=new_values)
            with open("Temp flight file.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_values[2], original_values[1], "", new_boarding, new_departure, new_gate, new_values[3]])


#Write the flight information from the csv files into their gate number windows
def open_info_window(gate_number):
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

        # First, iterate over the primary CSV file
        gate_flights_primary = flight_info[flight_info['Gate Number'] == gate_number]
        for index, flight in gate_flights_primary.iterrows():
            tree.insert('', tk.END, values=(flight['Boarding Time'], flight['Departure Time'], flight['Airline Name'], flight['Destination'], "On-Time", "", ""))

        # Prepare the secondary CSV (already cleared by clear_csv_file function)
        temp_flight_info = "Temp flight file.csv"
        temp_flight_info_read = pd.read_csv(temp_flight_info)

        gate_flights_secondary = temp_flight_info_read[temp_flight_info_read['Gate Number'] == gate_number]
        for index, flight in gate_flights_secondary.iterrows():
            # Assuming you've simplified your CSV structure and removed 'Additional Info'
            tree.insert('', tk.END, values=(flight['Boarding Time'], flight['Departure Time'], flight['Airline Name'], flight['Destination'], "Delayed", flight['Gate Number']))

        tree.pack(expand=True, fill='both')

        # Delay button
        delay_button = tk.Button(info_window, text="Delay", command=lambda: delay_flight(tree))
        delay_button.pack(side=tk.BOTTOM, anchor=tk.E)

        # Close window handler
        def on_close(gate_number=gate_number, window=info_window):
            window.destroy()  # Destroy the window
            open_windows.pop(gate_number, None)  # Remove its reference from the dictionary

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
        matching_flights = flight_info[flight_info['Gate Number'] == gate_number]
        if not matching_flights.empty:
            flight = matching_flights.iloc[0]
            if is_flight_time_now(flight['Boarding Time'], flight['Departure Time']):
                button.config(image=image2_photo)
            else:
                button.config(image=image1_photo)
        else:
            pass
    root.after(1000, update_icons)  # Check every second for updates


def check_flight_times():
    current_time = datetime.now().strftime('%H:%M:%S')
    for index, flight in flight_info.iterrows():
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
