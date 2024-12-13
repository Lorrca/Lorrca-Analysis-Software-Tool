import csv
from abc import ABC, abstractmethod

import numpy as np


class BaseDataLoader(ABC):
    """Base class for reading measurement files."""

    def __init__(self, delimiter=';'):
        self.delimiter = delimiter

    def load_data(self, filepath: str):
        """Load data from a measurement file."""

        metadata = {}
        data = {}

        try:
            with open(filepath, 'r') as file:
                csv_reader = csv.reader(file, delimiter=self.delimiter)

                # Step 1: Extract metadata
                headers, start_reading = self.initialize_reading(csv_reader, metadata)

                if not headers:
                    raise ValueError(f"No valid headers found in the file: {filepath}")

                # Step 2: Read tabular data
                if start_reading:
                    data = self.read_tabular_data(csv_reader, headers)

            # Step 3: Convert data to structured format
            data = self.convert_to_numpy(data)

            return metadata, data

        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
            raise
        except ValueError as ve:
            print(f"Validation Error: {ve}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while loading data: {e}")
            raise

    def initialize_reading(self, csv_reader, metadata):
        """Parse headers and extract metadata."""
        headers = []
        start_reading = False
        for row in csv_reader:
            if not row or row[0].strip() == "":
                continue  # Skip empty rows
            if self.extract_metadata(row, metadata):
                continue  # Process metadata rows
            if row[0].strip() == "#":
                headers = [header.strip() for header in row[1:]]  # Extract headers
                start_reading = True
                break
        return headers, start_reading

    @abstractmethod
    def extract_metadata(self, row, metadata) -> bool:
        """Extract metadata from a given row."""
        pass

    def read_tabular_data(self, csv_reader, headers) -> dict:
        """Read data rows from the CSV file."""

        data = {key: [] for key in headers}
        for row in csv_reader:
            if not row or row[0].strip() == "#":  # Skip empty or comment rows
                continue
            values = row[1:]  # Skip the first column (index)
            if len(values) != len(headers):
                print(
                    f"Warning: Row length mismatch. Expected {len(headers)}, got {len(values)}. Skipping row.")
                continue
            self.process_row(headers, values, data)

        return data

    @staticmethod
    def process_row(headers, values, data):
        """Process a single row of data."""

        for key, value in zip(headers, values):
            try:
                data[key].append(float(value.replace(",", ".")))  # Convert numeric values
            except ValueError:
                data[key].append(value.strip())  # Append non-numeric values as-is

    @staticmethod
    def convert_to_numpy(data, dtype=None) -> dict:
        """Convert lists in the data dictionary to NumPy arrays."""
        for key, values in data.items():
            try:
                data[key] = np.array(values, dtype=dtype) if dtype else np.array(values)
            except ValueError:
                print(
                    f"Warning: Could not convert data for key '{key}' to NumPy array. Keeping as list.")
        return data
