import csv
import numpy as np
from src.models.osmo_model import OsmoModel
from src.utils.data_validator import DataValidator


def load_data(filepath: str) -> OsmoModel:
    """Load data from a CSV file and construct an OsmoModel."""
    metadata = {}
    data = {}

    try:
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file, delimiter=';')

            # Step 1: Initialize reading process (headers and metadata)
            headers, start_reading = initialize_reading(csv_reader, metadata)

            if not headers:
                raise ValueError("No valid headers found in the file.")

            # Step 2: Read data if initialization succeeded
            if start_reading:
                data = read_data(csv_reader, headers)

        # Step 3: Convert lists to NumPy arrays
        data = convert_to_numpy(data)

        # Step 4: Validate the data and metadata
        if not DataValidator.validate_osmo_file(data, metadata):
            raise ValueError("Validation failed: The loaded data or metadata is invalid.")

        # Step 5: Construct and return the OsmoModel
        return OsmoModel(data, metadata)

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        raise
    except ValueError as ve:
        print(f"Validation Error: {ve}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        raise


def initialize_reading(csv_reader, metadata):
    """Parse headers and extract metadata."""
    headers = []
    start_reading = False

    for row in csv_reader:
        if not row or row[0].strip() == "":
            continue  # Skip empty rows
        if extract_metadata(row, metadata):
            continue  # Process metadata rows
        if row[0].strip() == "#":
            headers = [header.strip() for header in row[1:]]  # Extract headers
            start_reading = True
            break
    return headers, start_reading


def extract_metadata(row, metadata) -> bool:
    """Extract metadata from a given row."""
    if not row:
        return False

    metadata_mappings = {
        "Upper limit area": "upper_limit",
        "Lower limit area": "lower_limit",
        "Date (Y-M-D)": "date",
        "Instrument info": "instrument_info",
        "Measurement ID": "measurement_id",
    }

    for key, metadata_key in metadata_mappings.items():
        if key in row[0] and len(row) > 1:
            metadata[metadata_key] = row[1].strip() if "limit" not in key else int(row[1].strip())
            return True
    return False


def read_data(csv_reader, headers) -> dict:
    """Read data rows from the CSV file."""
    data = {key: [] for key in headers}

    for row in csv_reader:
        if not row or row[0].strip() == "#":  # Skip empty or comment rows
            continue
        values = row[1:]  # Skip the first column (index)
        if len(values) != len(headers):
            print(f"Warning: Row length mismatch. Expected {len(headers)}, got {len(values)}. Skipping row.")
            continue
        process_row(headers, values, data)

    return data


def process_row(headers, values, data):
    """Process a single row of data."""
    for key, value in zip(headers, values):
        try:
            data[key].append(float(value.replace(",", ".")))  # Convert numeric values
        except ValueError:
            data[key].append(value.strip())  # Append non-numeric values as-is


def convert_to_numpy(data, dtype=None) -> dict:
    """Convert lists in the data dictionary to NumPy arrays."""
    for key, values in data.items():
        try:
            data[key] = np.array(values, dtype=dtype) if dtype else np.array(values)
        except ValueError:
            print(f"Warning: Could not convert data for key '{key}' to NumPy array. Keeping as list.")
    return data
