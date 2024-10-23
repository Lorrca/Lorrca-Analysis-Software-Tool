import numpy as np
from scipy.signal import find_peaks
from scipy import integrate


class DataColumnNotFoundError(KeyError):
    pass


class InsufficientDataError(ValueError):
    pass


class OsmoModel:
    # Key values for data columns
    EI_KEY = 'EI'
    O_KEY = 'O.'

    def __init__(self, osmo_data: dict[str, np.ndarray], osmo_metadata: dict):
        self.data = osmo_data

        # Set metadata
        self._measurement_id = osmo_metadata.get('measurement_id')
        self._date = osmo_metadata.get('date')
        self._instrument_info = osmo_metadata.get('instrument_info')
        self._upper_limit = osmo_metadata.get('upper_limit')
        self._lower_limit = osmo_metadata.get('lower_limit')

        self._ei = self._get_data_column(self.EI_KEY)
        self._o = self._get_data_column(self.O_KEY)
        self._ei_max = self._calculate_ei_max_value()
        self._ei_hyper = self._calculate_ei_hyper_value()
        self._o_max, self._o_max_idx = self._get_o_max_value_and_idx()
        self._o_hyper = self._calculate_o_hyper()
        self._first_peak_idx = self._find_prominent_peak()
        self._valley_idx = self._find_prominent_valley()
        self._area = self._calculate_area()

    @property
    def id(self):
        return self._measurement_id

    @property
    def date(self):
        return self._date

    @property
    def info(self):
        return self._instrument_info

    @property
    def ei(self):
        return self._ei

    @property
    def o(self):
        return self._o

    @property
    def ei_max(self):
        return self._ei_max

    @property
    def o_max(self):
        return self._o[self._o_max_idx]

    @property
    def ei_hyper(self):
        return self._ei_hyper

    @property
    def o_hyper(self):
        return self._o_hyper

    @property
    def first_peak(self):
        if self._first_peak_idx is not None:
            return self._o[self._first_peak_idx], self._ei[
                self._first_peak_idx]
        return None

    @property
    def min(self):
        if self._valley_idx is not None:
            return self._o[self._valley_idx], self._ei[self._valley_idx]
        return None

    @property
    def area(self):
        return self._area

    # Returns a data column based on key value
    def _get_data_column(self, column: str) -> np.ndarray:
        """Retrieve a data column by key."""
        value = self.data.get(column)
        if value is None:
            raise DataColumnNotFoundError(
                f"Column '{column}' not found in data.")
        return value

    # Calculates the highest Elongation INdex value
    def _calculate_ei_max_value(self) -> float:
        """Calculate the maximum EI value."""
        return float(np.max(self.ei))

    # Calculates
    def _calculate_ei_hyper_value(self) -> float:
        """Calculate EI hyper, which is half of EI max."""
        return self._ei_max / 2

    def _get_o_max_value_and_idx(self) -> (float, int):
        """Find the O max value and its corresponding index."""
        indices = np.nonzero(self.ei == self._ei_max)[0]
        if len(indices) == 0:
            raise InsufficientDataError("EI max not found in the EI array.")
        center_idx = indices[len(indices) // 2]
        return float(self.o[center_idx]), center_idx

    def _calculate_o_hyper(self) -> float | None:
        """Interpolate and calculate O hyper based on EI hyper."""
        relevant_ei = self.ei[self._o_max_idx:]
        relevant_o = self.o[self._o_max_idx:]

        if len(relevant_ei) < 2:
            raise InsufficientDataError(
                "Not enough data points to perform interpolation.")

        for i, ei_value in enumerate(relevant_ei):
            # Check if ei_value is a tuple
            if isinstance(ei_value, tuple):
                ei_value = ei_value[0]

            if ei_value == self._ei_hyper:
                return float(relevant_o[i])
            elif ei_value < self._ei_hyper:
                return self._interpolate(relevant_ei[i - 1], relevant_o[i - 1],
                                         relevant_ei[i], relevant_o[i])
        return None

    def _interpolate(self, x1, y1, x2, y2) -> float:
        """Linear interpolation between two points."""
        return y1 + (y2 - y1) * (self._ei_hyper - x1) / (x2 - x1)

    def _find_prominent_peak(self) -> int:
        """Find the peak with the highest prominence before O max."""
        return self._find_prominent_point(self.ei[:self._o_max_idx],
                                          find_peaks)

    def _find_prominent_valley(self) -> int:
        """Find the valley with the highest prominence after the first peak."""
        filtered_ei = self.ei[self._first_peak_idx:self._o_max_idx]
        return self._find_prominent_point(-filtered_ei, find_peaks,
                                          self._first_peak_idx)

    @staticmethod
    def _find_prominent_point(data, find_func, offset=0) -> int:
        """General method to find the most prominent peak or valley."""
        peaks, properties = find_func(data, prominence=0)
        prominences = properties['prominences']

        if len(peaks) == 0:
            raise InsufficientDataError("No prominent points found.")

        highest_prominence_idx = np.argmax(prominences)
        highest_peak_value = data[peaks[highest_prominence_idx]]
        peak_idx = peaks[highest_prominence_idx]

        start_idx = max(0, peak_idx - 10)
        end_idx = min(len(data), peak_idx + 10 + 1)
        search_window = data[start_idx:end_idx]
        matching_indices = np.nonzero(search_window == highest_peak_value)[0]

        if len(matching_indices) > 1:
            center_idx = matching_indices[len(matching_indices) // 2]
        elif len(matching_indices) == 1:
            center_idx = matching_indices[0]
        else:
            raise InsufficientDataError(
                "No matching prominent points found within the search window.")

        return int(start_idx + center_idx) + offset

    def _calculate_area(self):
        """Calculates area between lower & upper limits set by Lorrca"""

        # Find indices for Omin and Upper limit
        lower_idx = np.nonzero(self._o >= self._lower_limit)[0]
        upper_idx = np.nonzero(self._o <= self._upper_limit)[0]

        if upper_idx.size == 0:
            raise ValueError("Upper limit exceeds available O. values.")
        if lower_idx.size == 0:
            raise ValueError("Upper limit exceeds available O. values.")

        # Get the last index where O. is less than or equal to the upper_limit
        upper_idx = upper_idx[-1]
        # Get the first index where Osmolality is bigger than or equal to the lower_limit
        lower_idx = lower_idx[0]

        # Slice the data for the integration
        o_segment = self._o[lower_idx:upper_idx + 1]
        ei_segment = self._ei[lower_idx:upper_idx + 1]

        # Check if the segments are valid for integration
        if len(o_segment) < 2 or len(ei_segment) < 2:
            raise ValueError("Not enough data points for area calculation.")

        # Calculate the area using Simpson's rule
        area = integrate.simpson(y=ei_segment, x=o_segment)

        return area, o_segment, ei_segment
