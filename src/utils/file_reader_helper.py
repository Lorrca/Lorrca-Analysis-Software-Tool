import csv
import logging


class FileHelper:

    @staticmethod
    def peek_headers(file_path: str, delimiter: str = ';') -> list:
        """Extract headers directly without relying on a loader."""
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file, delimiter=delimiter)
                for row in csv_reader:
                    if row and row[0].strip() == "#":
                        return [header.strip() for header in row[1:]]
        except Exception as e:
            logging.error(f"Error reading headers from {file_path}: {e}")
            raise
        return []
