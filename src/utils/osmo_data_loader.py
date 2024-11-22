import csv
import numpy as np

from src.models.osmo_model import OsmoModel


def load_data(filepath: str) -> OsmoModel:
    metadata = {}  # Initialize metadata here
    try:
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file, delimiter=';')
            headers, start_reading = initialize_reading(csv_reader, metadata)
            data = read_data(csv_reader, headers) if start_reading else {}

        # Convert lists to NumPy arrays
        data = convert_to_numpy(data)

        return OsmoModel(data, metadata)

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return OsmoModel({}, {})
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return OsmoModel({}, {})

def initialize_reading(csv_reader, metadata):
    headers = []
    start_reading = False

    for row in csv_reader:
        if extract_metadata(row, metadata):  # Pass metadata to the function
            continue
        elif row and row[0].strip() == "#":
            headers = [header.strip() for header in row[1:]]  # Clean headers
            start_reading = True  # Start reading subsequent rows
            break
    return headers, start_reading

def extract_metadata(row, metadata) -> bool:
    if not row:
        return False

    if "Upper limit area" in row[0] and len(row) > 1:
        metadata["upper_limit"] = int(row[1])
    if "Lower limit area" in row[0] and len(row) > 1:
        metadata["lower_limit"] = int(row[1])
    if "Date (Y-M-D)" in row[0] and len(row) > 1:
        metadata["date"] = row[1].strip()  # Store date value
    if "Instrument info" in row[0] and len(row) > 1:
        metadata["instrument_info"] = row[1].strip()  # Store instrument info
    if "Measurement ID" in row[0] and len(row) > 1:
        metadata["measurement_id"] = row[1].strip()
        return True
    return False

def read_data(csv_reader, headers) -> dict:
    data = {key: [] for key in headers}  # Initialize the dictionary
    for row in csv_reader:
        # Process data rows (skip the first column in each row)
        if row and row[0].strip() != "#":  # Ensure we're reading actual data
            values = row[1:]  # Skip the first index column
            process_row(headers, values, data)
    return data

def process_row(headers, values, data):
    for key, value in zip(headers, values):
        # Convert values to float, handling commas as decimal points
        try:
            # Replace commas with dots and convert to float
            data[key].append(float(value.replace(",", ".")))
        except ValueError:
            data[key].append(value)  # Keep non-numeric values as they are

def convert_to_numpy(data) -> dict:
    # Convert lists to NumPy arrays
    for key in data:
        data[key] = np.array(data[key])
    return data


class OsmoDataLoader:
    pass