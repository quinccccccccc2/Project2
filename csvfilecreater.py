import pandas as pd
from datetime import datetime, timedelta
import numpy as np

#THIS PROGRAM IS ENTIRLY CHATGPT AND SHOULD NOT BE CONSIDERED APART OF ASSIGNMENT, THIS IS ONLY TO CREATE AN EXAMPLE FOR
#DEVELOPERS AND TESTERS TO ANALYSE THE PROGRAM.

# Define the start and end times for the flight schedule
start_time = datetime.strptime("00:00", "%H:%M")
end_time = datetime.strptime("23:59", "%H:%M")

# Create time slots every minute
time_slots = pd.date_range(start_time, end_time, freq='1T').time

# Define a list of destinations and airlines for the example
destinations = ["New York", "Ottawa", "Montreal", "Chicago", "Washington", "Boston"]
airlines = ["WestJet", "Porter Airlines", "Air Canada"]

# Gates available for scheduling and their last used times initialized to start time
gates = {gate: start_time for gate in [1, 2, 3, 4, 5, 6]}

# Generate the flight schedule
schedule = []

for time_slot in time_slots:
    # Select gates to use in this time slot ensuring no conflict
    for gate_number, last_used_time in gates.items():
        # Determine boarding time ensuring it's after the last used time plus grace period
        boarding_time = max(datetime.combine(datetime.today(), time_slot) - timedelta(minutes=np.random.randint(1, 5)),
                            last_used_time + timedelta(minutes=2))
        if boarding_time.time() > time_slot:  # Skip if boarding time would be in the future relative to the slot
            continue

        # Create a new flight entry
        flight = {
            "Airline Name": np.random.choice(airlines),
            "Flight Number": "PD" + str(np.random.randint(100, 999)),
            "Plane Model": "Embraer E190" if gate_number % 2 == 0 else "ATR 72",
            "Boarding Time": boarding_time.strftime("%H:%M:%S"),
            "Departure Time": (boarding_time + timedelta(minutes=np.random.randint(1, 4))).strftime("%H:%M:%S"),
            "Gate Number": gate_number,
            "Destination": np.random.choice(destinations)
        }
        schedule.append(flight)

        # Update the last used time for the gate
        gates[gate_number] = boarding_time + timedelta(minutes=2)  # Include grace period for next calculation

# Convert the schedule to a DataFrame
df_schedule = pd.DataFrame(schedule)

# Save the DataFrame to a CSV file
output_csv_path = "Updated_Flight_Schedule3.csv"
df_schedule.to_csv(output_csv_path, index=False)

output_csv_path