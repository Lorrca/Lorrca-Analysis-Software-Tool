import csv
import logging
import os


class FileHelper:

    @staticmethod
    def peek_headers(file_path: str) -> list:
        """Extract headers directly, automatically detecting the file's delimiter."""
        try:
            with open(file_path, 'r') as file:
                delimiter = FileHelper.detect_delimiter(file)
                file.seek(0)
                csv_reader = csv.reader(file, delimiter=delimiter)

                for row in csv_reader:
                    if row and row[0].strip() == "#":
                        # Return cleaned header by stripping extra whitespace and handling delimiters properly
                        return [header.strip() for header in row[1:]]
        except Exception as e:
            logging.error(f"Error reading headers from {file_path}: {e}")
            raise
        return []

    @staticmethod
    def are_valid_paths(urls):
        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                continue
            elif os.path.isfile(path) and path.lower().endswith('.csv'):
                continue
            else:
                return False
        return True

    @staticmethod
    def collect_csv_files(paths):
        csv_files = []
        for path in paths:
            if os.path.isfile(path) and path.lower().endswith('.csv'):
                csv_files.append(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    csv_files.extend(
                        os.path.join(root, file) for file in files if file.lower().endswith('.csv')
                    )
        return csv_files

    @staticmethod
    def detect_delimiter(file):
        """Automatically detect the file's delimiter."""
        sample = file.read(1024)  # Read a sample of the file
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
