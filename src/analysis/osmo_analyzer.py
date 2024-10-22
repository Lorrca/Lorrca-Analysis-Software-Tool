import numpy as np


from scipy.signal import find_peaks
from scipy import integrate

# Constants for data keys
EI_KEY = "EI"
O_KEY = "O."


class OsmoAnalyzer:
    def __init__(self, data, osmo_metadata):
        self.data = data
        self.metadata = osmo_metadata

    def analyze(self):
        """Perform all analyses and return results."""
        results = {
            "ei_max": self.calculate_ei_max(),
            "o_at_ei_max": self.calculate_o_max_and_idx()[0],
            "ei_hyper": self.calculate_ei_hyper(),
            "o_hyper": self.calculate_o_hyper(),
            "ei_min": float(
                self.data[EI_KEY][self._get_valley_with_highest_prominence()]),
            "o_min": float(
                self.data[O_KEY][self._get_valley_with_highest_prominence()]),
            "ei_first_peak": float(
                self.data[EI_KEY][self._get_peak_with_highest_prominence()]),
            "o_first_peak": float(
                self.data[O_KEY][self._get_peak_with_highest_prominence()]),
            "area": self.calculate_area()
        }
        return results

    def calculate_ei_max(self) -> float:
        """Calculates EI_max value."""
        if EI_KEY not in self.data:
            raise ValueError("EI data is not available.")
        return float(np.max(self.data[EI_KEY]))

    def calculate_ei_hyper(self) -> float:
        """Calculate EI hyper value."""
        ei_max = self.calculate_ei_max()
        return ei_max / 2

    def calculate_o_max_and_idx(self) -> (float, int):
        """Finds O value corresponding to EI_max and its index."""
        if EI_KEY not in self.data or O_KEY not in self.data:
            raise ValueError(f"{EI_KEY} or {O_KEY} data is not available.")

        ei = np.array(self.data[EI_KEY])  # Ensure ei is a numpy array
        o = self.data[O_KEY]

        ei_max = self.calculate_ei_max()
        indices = np.nonzero(ei == ei_max)[0]

        if len(indices) == 0:
            raise ValueError("EI max not found in the EI array")

        # Get the middle index if there are multiple occurrences of EI_max
        center_idx = indices[len(indices) // 2]

        # Return the corresponding O value and the index
        return float(o[center_idx]), int(center_idx)

    def calculate_o_hyper(self) -> float | None:
        """Calculate O hyper based on EI hyper."""
        if EI_KEY not in self.data or O_KEY not in self.data:
            raise ValueError(f"{EI_KEY} or {O_KEY} data is not available.")

        ei_hyper = self.calculate_ei_hyper()
        ei = self.data[EI_KEY]
        o = self.data[O_KEY]

        # Find the index of O(EI_max)
        _, o_max_idx = self.calculate_o_max_and_idx()

        # Get the relevant part of the curve, starting after O(EI_max)
        relevant_ei_values = ei[o_max_idx:]
        relevant_o_values = o[o_max_idx:]

        # Find the first point where EI < EI_hyper
        for i, ei_value in enumerate(relevant_ei_values):
            if ei_value < ei_hyper:
                # Perform linear interpolation
                if i == 0:
                    return None  # Cannot interpolate if no prior point exists

                x1, y1 = relevant_ei_values[i - 1], relevant_o_values[i - 1]
                x2, y2 = relevant_ei_values[i], relevant_o_values[i]

                # Calculate O hyper using linear interpolation
                o_hyper = y1 + (y2 - y1) * (ei_hyper - x1) / (x2 - x1)
                return float(o_hyper)

        return None  # If no point found

    def _get_peak_with_highest_prominence(self) -> int:
        """Find the peak with the highest prominence."""
        filtered_ei = self.data[EI_KEY][:self.calculate_o_max_and_idx()[1]]

        peaks, properties = find_peaks(filtered_ei, prominence=0)
        prominences = properties['prominences']

        # Find the index of the peak with the highest prominence
        highest_prominence_idx = np.argmax(prominences)
        highest_peak_value = filtered_ei[peaks[highest_prominence_idx]]

        # Determine the index of the highest prominence peak
        highest_peak_index = peaks[highest_prominence_idx]

        # Define the search window: ±5 data points from the highest prominence index
        start_idx = max(0, highest_peak_index - 10)
        end_idx = min(len(filtered_ei), highest_peak_index + 10 + 1)

        # Search for peaks with the same value within this narrowed window
        search_window = filtered_ei[start_idx:end_idx]
        matching_indices = np.nonzero(search_window == highest_peak_value)[0]

        if len(matching_indices) > 1:
            # If multiple peaks found within the window, choose the middle one
            center_idx = matching_indices[len(matching_indices) // 2]
        elif len(matching_indices) == 1:
            # If only one peak is found, use it directly
            center_idx = matching_indices[0]
        else:
            # If no matching peak is found, raise an error
            raise ValueError(
                "No matching peak found within the search window.")

        # Adjust center_idx to the original index in filtered_ei
        peak_idx = start_idx + center_idx

        # Return the index of the peak with the highest prominence
        return int(peak_idx)

    def _get_valley_with_highest_prominence(self) -> int:
        """Find the valley with the highest prominence."""
        filtered_ei = self.data[EI_KEY][
                      self._get_peak_with_highest_prominence():
                      self.calculate_o_max_and_idx()[1]]

        # Find valleys and their properties by inverting the data
        valleys, properties = find_peaks(-filtered_ei, prominence=0)
        prominences = properties['prominences']

        # Find the index of the valley with the highest prominence
        highest_prominence_idx = np.argmax(prominences)
        highest_valley_value = filtered_ei[valleys[highest_prominence_idx]]

        # Determine the index of the highest prominence peak
        highest_valley_index = valleys[highest_prominence_idx]

        # Define the search window: ±10 data points from the highest prominence valley
        start_idx = max(0, highest_valley_index - 10)
        end_idx = min(len(filtered_ei), highest_valley_index + 10 + 1)

        # Search for valleys with the same value within this narrowed window
        search_window = filtered_ei[start_idx:end_idx]
        matching_indices = np.nonzero(search_window == highest_valley_value)[0]

        if len(matching_indices) > 1:
            # If multiple valleys found within the window, choose the middle one
            center_idx = matching_indices[len(matching_indices) // 2]
        elif len(matching_indices) == 1:
            # If only one valley is found, use it directly
            center_idx = matching_indices[0]
        else:
            # If no matching valley is found, raise an error
            raise ValueError(
                "No matching valley found within the search window.")

        # Adjust center_idx to the original index in filtered_ei
        valley_idx = start_idx + center_idx
        # Adjust valley_inx to the original index in ei
        valley_idx += self._get_peak_with_highest_prominence()

        # Return the valley index
        return int(valley_idx)

    def calculate_area(self):
        # Assuming self.data['O.'] and self.data['EI'] are your x and y data respectively

        upper_limit = self.metadata.get('upper_limit')

        # Find indices for Omin and Upper limit
        lower_idx = self._get_valley_with_highest_prominence()
        upper_idx = \
        np.nonzero(self.data['O.'] <= upper_limit)[0]

        if upper_idx.size == 0:
            raise ValueError("Upper limit exceeds available O. values.")

        upper_idx = upper_idx[
            -1]  # Get the last index where O. is less than or equal to upper_limit

        # Slice the data for the integration
        o_segment = self.data['O.'][lower_idx:upper_idx + 1]
        ei_segment = self.data['EI'][lower_idx:upper_idx + 1]

        # Check if the segments are valid for integration
        if len(o_segment) < 2 or len(ei_segment) < 2:
            raise ValueError("Not enough data points for area calculation.")

        # Calculate the area using Simpson's rule
        area = integrate.simpson(y=ei_segment, x=o_segment)

        return area, o_segment, ei_segment
