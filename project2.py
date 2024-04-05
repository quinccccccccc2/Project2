import tkinter as tk
import time
from tkinter import ttk, simpledialog, filedialog
from PIL import Image, ImageTk
from functools import partial
import pandas as pd
from datetime import datetime
import csv
import re

# Initialize Tkinter window
root = tk.Tk()
root.title("Billy Bishop Universal Airport Management System")

csv_file_path = filedialog.askopenfilename(title="Uploading Today's Flight Manifest",
                                           filetypes=[("CSV files", "*.csv")])
if not csv_file_path:
    print("No file selected. Exiting application.")
    exit()  # Exit the application if no file is selected

df = pd.read_csv(csv_file_path)


def clear_csv_file(file_path):
    print(f"Clearing file: {file_path}")
    try:
        with open(file_path, 'w', newline='') as file:
            # Replicating the provided CSV file's header format exactly
            headers = "Airline Name,Flight Number,Plane Model,Boarding Time,Departure Time,Gate Number,Destination,Status\n"
            file.write(headers)
        print("File cleared successfully.")
    except Exception as e:
        print(f"Failed to clear file: {e}")


clear_csv_file("Temp flight file.csv")

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
# Dictionary to store labels for each gate
gate_labels = {}


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

        time_format_regex = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'

        new_boarding = None
        while new_boarding is None:
            temp_boarding = simpledialog.askstring("Update Boarding Time", "Enter new boarding time (HH:MM:SS):",
                                                   parent=tree)
            if temp_boarding is None:  # User cancelled
                break
            if re.match(time_format_regex, temp_boarding):
                new_boarding = temp_boarding
            else:
                tk.messagebox.showerror("Invalid Format", "Please enter the time in HH:MM:SS format.")

        new_departure = None
        while new_departure is None:
            temp_departure = simpledialog.askstring("Update Departure Time", "Enter new departure time (HH:MM:SS):",
                                                    parent=tree)
            if temp_departure is None:  # User cancelled
                break
            if re.match(time_format_regex, temp_departure):
                new_departure = temp_departure
            else:
                tk.messagebox.showerror("Invalid Format", "Please enter the time in HH:MM:SS format.")

        while True:
            temp_gate = simpledialog.askstring("Update Gate number", "Enter gate number (1-11):", parent=tree)
            try:
                if temp_gate is not None and 1 <= int(temp_gate) <= 11:
                    new_gate = temp_gate
                    break
                else:
                    print("ERROR: INVALID GATE")
            except ValueError:
                print("ERROR: PLEASE INPUT A VALID GATE NUMBER")
        # Determine if any value has changed
        values_changed = False
        new_values = list(original_values)  # Make a copy of the original values

        # Adjustments for boarding and departure times, considering the indices shift.
        if new_boarding and new_boarding != original_values[1]:
            new_values[1] = new_boarding  # Update boarding time
            values_changed = True
        if new_departure and new_departure != original_values[2]:
            new_values[2] = new_departure  # Update departure time
            values_changed = True

        if new_gate:
            try:
                if new_gate != str(original_values[6]):
                    new_values[6] = new_gate
                    values_changed = True
            except IndexError:
                print("IndexError: 'New Gate' not found")
        # Apply the update if any value changed
        if values_changed:
            new_values[5] = "Delayed"
            tree.item(selected_item, values=new_values, tags=('modified',))
            with open("Temp flight file.csv", "a", newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([
                    new_values[3],  # Airline Name
                    new_values[0],  # Flight Number
                    "",  # Plane Model, assuming empty for simplicity
                    new_boarding,  # Boarding Time
                    new_departure,  # Departure Time
                    new_gate,  # Gate Number
                    new_values[4],  # Destination
                    new_values[5]  # Status
                ])


def open_info_window(gate_number):
    if gate_number not in open_windows or not open_windows[gate_number].winfo_exists():
        info_window = tk.Toplevel(root)
        info_window.title(f"Flight Information for Gate {gate_number}")
        open_windows[gate_number] = info_window

        frame = tk.Frame(info_window)
        frame.pack(expand=True, fill='both')

        tree = ttk.Treeview(frame, columns=(
            'Flight Number', 'Boarding Time', 'Departure Time', 'Airline', 'Destination', 'Status', 'New Gate'),
                            show='headings')
        tree.heading('New Gate', text='New Gate')
        tree.heading('Flight Number', text='Flight Number')
        tree.heading('Boarding Time', text='Boarding Time')
        tree.heading('Departure Time', text='Departure Time')
        tree.heading('Airline', text='Airline')
        tree.heading('Destination', text='Destination')
        tree.heading('Status', text='Status')

        # Correctly accessing DataFrame for primary flights
        gate_flights_primary = df[df["Gate Number"].astype(str) == str(gate_number)]
        for _, flight in gate_flights_primary.iterrows():
            tree.insert('', tk.END, values=(
                flight['Flight Number'],
                flight['Boarding Time'],
                flight['Departure Time'],
                flight['Airline Name'],
                flight['Destination'],
                "On-Time",
                ""  # Assuming no 'New Gate' information for primary CSV
            ))

        temp_flight_info = "Temp flight file.csv"
        temp_flight_info_read = pd.read_csv(temp_flight_info)

        # Filter for the specified gate number in the secondary CSV
        # Make sure 'Gate Number' is treated consistently as an integer or string across both DataFrames
        gate_flights_secondary = temp_flight_info_read[temp_flight_info_read['Gate Number'] == int(gate_number)]
        for index, flight in gate_flights_secondary.iterrows():
            # Insert values into the tree, assuming 'Flight Number' and 'Airline Name' are present and need to be shown
            tree.insert('', tk.END, values=(
                flight['Flight Number'],  # Assuming this column exists in your secondary CSV
                flight['Boarding Time'],
                flight['Departure Time'],
                flight['Airline Name'],  # Or another placeholder if the airline name isn't in the secondary CSV
                flight['Destination'],
                "Delayed",  # Status for delayed flights
                flight['Gate Number']  # Assuming 'New Gate' is a column in your secondary CSV
            ))

        # Prepare the secondary CSV (already cleared by clear_csv_file function)
        temp_flight_info = "Temp flight file.csv"
        temp_flight_info_read = pd.read_csv(temp_flight_info)

        # Create a Scrollbar and associate it with the treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scrollbar.set)

        # Define the treeview style for highlighting
        style = ttk.Style(info_window)
        style.configure("Treeview", font=('Helvetica', 12))  # Set the font size
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'))  # Set the font size for headings

        # Define a tag for highlighting the current flight
        style.map('currentFlight', background=[('selected', 'yellow'), ('!selected', 'yellow')])  # Highlight background

        # Insert flight data into the treeview
        current_time = datetime.now()
        for index, flight in df[df['Gate Number'] == gate_number].iterrows():
            boarding_time = datetime.strptime(flight['Boarding Time'], '%H:%M:%S').time()
            departure_time = datetime.strptime(flight['Departure Time'], '%H:%M:%S').time()

            # Determine if the flight is currently boarding
            is_current = boarding_time <= current_time.time() <= departure_time

            # Insert the flight into the tree with or without the 'currentFlight' tag
            if is_current:
                tree.insert('', tk.END, values=(
                    flight['Flight Number'], flight['Boarding Time'], flight['Departure Time'], flight['Airline Name'],
                    flight['Destination'], "Boarding"), tags=('currentFlight',))
            else:
                tree.insert('', tk.END, values=(
                    flight['Flight Number'], flight['Boarding Time'], flight['Departure Time'], flight['Airline Name'],
                    flight['Destination'], "On-Time"), tags=())

        # Apply the tag style to the tree
        tree.tag_configure('currentFlight', background='yellow')  # Apply the defined style to the 'currentFlight' tag
        tree.tag_configure('cancelled', background='red')

        # Display the treeview
        tree.pack(expand=True, fill='both')

        # In the same open_info_window function, create and pack a cancel button
        cancel_button = tk.Button(info_window, text="Cancel Flight", command=lambda: cancel_flight(tree))
        cancel_button.pack(side=tk.BOTTOM, anchor=tk.E)
        # Create a delay button
        delay_button = tk.Button(info_window, text="Delay", command=lambda: delay_flight(tree))
        delay_button.pack(side=tk.BOTTOM, anchor=tk.E)

        # When closing the window, remove its reference
        def on_close(gate_number=gate_number, window=info_window):
            window.destroy()  # Destroy the window
            open_windows.pop(gate_number, None)  # Remove its reference

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
    label = tk.Label(root, text=f"Gate {i}", bg='white')  # Set default background color
    label.place(x=position[0] + 60, y=position[1] + 20)
    gate_buttons[i] = button
    gate_labels[i] = label  # Store the label


def cancel_flight(tree):
    selected_item = tree.selection()[0] if tree.selection() else None
    if selected_item:
        item = tree.item(selected_item)
        values = list(item['values'])

        # Ensure 'Status' is correctly set to 'Cancelled'
        if len(values) >= 6:  # Assuming 'Status' is the 6th value
            values[5] = 'Cancelled'  # Update status; adjust index as necessary
        else:
            # Handle the case where there are fewer elements than expected
            print("Unexpected item structure:", values)
            return  # Optionally, handle this case more gracefully

        # Update the Treeview item with modified values
        tree.item(selected_item, values=values, tags=('cancelled',))

        # Update DataFrame and persist changes as needed
        flight_number = values[0]  # Assuming flight number is the first value
        df.loc[df['Flight Number'] == flight_number, 'Status'] = 'Cancelled'
        df.to_csv(csv_file_path, index=False)


def update_all():
    current_time = datetime.now().strftime('%H:%M:%S')
    time_label.config(text="Current Time: " + current_time)

    try:
        temp_df = pd.read_csv("Temp flight file.csv")
        # Ensure 'Status' column exists, setting a default if not
        if 'Status' not in temp_df.columns:
            temp_df['Status'] = 'On-Time'  # Assuming 'On-Time' as default status
    except Exception as e:
        print("Error reading Temp flight file.csv:", e)
        temp_df = pd.DataFrame()

    # Attempt to read the temp flight information
    try:
        temp_df = pd.read_csv("Temp flight file.csv")
    except Exception as e:
        print("Error loading Temp flight file.csv:", e)
        temp_df = pd.DataFrame()

    # First, reset all gate icons to default
    for gate_number, button in gate_buttons.items():
        button.config(image=image1_photo)  # Reset to default icon
        gate_labels[gate_number].config(bg='white')  # Reset label background color

    # Iterate over delayed flights to update gate icons
    delayed_gates = temp_df[temp_df['Status'] == 'Delayed']['Gate Number'].unique()
    for gate_number in delayed_gates:
        if gate_number in gate_buttons:
            gate_buttons[gate_number].config(image=image2_photo)  # Set to delayed flight icon
            gate_labels[gate_number].config(bg='orange')  # Optional: change label bg color for visual cue

    # Check for current flights to highlight boarding
    for _, flight in df.iterrows():
        gate_number = flight['Gate Number']
        if gate_number in gate_buttons and gate_number not in delayed_gates:
            boarding_time = datetime.strptime(flight['Boarding Time'], '%H:%M:%S').time()
            departure_time = datetime.strptime(flight['Departure Time'], '%H:%M:%S').time()
            current_time_dt = datetime.strptime(current_time, '%H:%M:%S').time()
            if boarding_time <= current_time_dt <= departure_time:
                gate_buttons[gate_number].config(image=image2_photo)
                gate_labels[gate_number].config(bg='yellow')  # Highlight boarding

    root.after(1000, update_all)


def update_time():
    current_time = time.strftime('%H:%M:%S')
    time_label.config(text="Current Time: " + current_time)
    root.after(1000, update_time)  # Update the time every second


# Display the current time at the bottom left
time_label = tk.Label(root, font=('Helvetica', 20), bg='white', text='')
time_label.place(x=10, y=background_height - 30)

update_all()
update_time()

# Keep references to the PhotoImage objects to prevent garbage collection
image_references = [image1_photo, image2_photo]

root.mainloop()
