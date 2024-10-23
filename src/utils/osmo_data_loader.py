import csv

import numpy as np


class OsmoDataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.metadata = {}

    def load_data(self):
        try:
            with open(self.filepath, 'r') as file:
                csv_reader = csv.reader(file, delimiter=';')
                headers, start_reading = self._initialize_reading(csv_reader)
                data = self._read_data(csv_reader,
                                       headers) if start_reading else {}

            # Convert lists to NumPy arrays
            data = self._convert_to_numpy(data)

            return data, self.metadata

        except FileNotFoundError:
            print(f"Error: The file '{self.filepath}' was not found.")
            return {}, {}
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return {}, {}

    def _initialize_reading(self, csv_reader):
        headers = []
        start_reading = False

        for row in csv_reader:
            if self._extract_metadata(row):
                continue
            elif row and row[0].strip() == "#":
                headers = [header.strip() for header in
                           row[1:]]  # Clean headers
                start_reading = True  # Start reading subsequent rows
                break
        return headers, start_reading

    def _extract_metadata(self, row) -> bool:
        if not row:
            return False

        if "Upper limit area" in row[0] and len(row) > 1:
            self.metadata["upper_limit"] = int(row[1])
        if "Lower limit area" in row[0] and len(row) > 1:
            self.metadata["lower_limit"] = int(row[1])
        if "Date (Y-M-D)" in row[0] and len(row) > 1:
            self.metadata["date"] = row[1].strip()  # Store date value
        if "Instrument info" in row[0] and len(row) > 1:
            self.metadata["instrument_info"] = row[
                1].strip()  # Store instrument info
        if "Measurement ID" in row[0] and len(row) > 1:
            self.metadata["measurement_id"] = row[1].strip()
            return True
        return False

    def _read_data(self, csv_reader, headers) -> dict:
        data = {key: [] for key in headers}  # Initialize the dictionary
        for row in csv_reader:
            # Process data rows (skip the first column in each row)
            if row and row[
                0].strip() != "#":  # Ensure we're reading actual data
                values = row[1:]  # Skip the first index column
                self._process_row(headers, values, data)
        return data

    @staticmethod
    def _process_row(headers, values, data):
        for key, value in zip(headers, values):
            # Convert values to float, handling commas as decimal points
            try:
                # Replace commas with dots and convert to float
                data[key].append(float(value.replace(",", ".")))
            except ValueError:
                data[key].append(value)  # Keep non-numeric values as they are

    @staticmethod
    def _convert_to_numpy(data) -> list:
        # Convert lists to NumPy arrays
        for key in data:
            data[key] = np.array(data[key])
        return data
