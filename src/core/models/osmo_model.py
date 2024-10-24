from typing import Optional

import numpy as np
from scipy.signal import find_peaks
from scipy import integrate


class DataColumnNotFoundError(KeyError):
    """Exception raised when a requested data column is not found."""
    pass


class InsufficientDataError(ValueError):
    """Exception raised when there is insufficient data for a calculation."""
    pass


class MissingDataError(ValueError):
    """Exception raised when required data for a calculation is missing or incomplete."""
    pass


class OsmoModel:
    """Model for processing and analyzing osmo data."""
    # Key values for data columns
    EI_KEY = 'EI'
    O_KEY = 'O.'

    def __init__(self, osmo_data: dict[str, np.ndarray], osmo_metadata: dict):
        """
        Initialize the OsmoModel with provided data and metadata.

        Parameters:
        - osmo_data: A dictionary containing measurement data arrays.
        - osmo_metadata: A dictionary containing metadata for the measurements.
        """
        # Additional validation for input types
        if not isinstance(osmo_data, dict):
            raise TypeError("osmo_data must be a dictionary.")
        if not isinstance(osmo_metadata, dict):
            raise TypeError("osmo_metadata must be a dictionary.")
        if not osmo_data or not all(isinstance(arr, np.ndarray) for arr in osmo_data.values()):
            raise MissingDataError("osmo_data must contain non-empty numpy arrays.")

        self.data = osmo_data

        # Set metadata
        self._measurement_id = osmo_metadata.get('measurement_id')
        self._date = osmo_metadata.get('date')
        self._instrument_info = osmo_metadata.get('instrument_info')
        self._upper_limit = osmo_metadata.get('upper_limit')
        self._lower_limit = osmo_metadata.get('lower_limit')

        self._ei = self._get_data_column(self.data, self.EI_KEY)
        self._o = self._get_data_column(self.data, self.O_KEY)

        # Initialize calculated attributes to None
        self._ei_max: Optional[float] = None
        self._ei_hyper: Optional[float] = None
        self._o_max: Optional[float] = None
        self._o_max_idx: Optional[int] = None
        self._o_hyper: Optional[float] = None
        self._first_peak_idx: Optional[int] = None
        self._o_first_peak: Optional[float] = None
        self._ei_first_peak: Optional[float] = None
        self._min_idx: Optional[int] = None
        self._o_min: Optional[float] = None
        self._ei_min: Optional[float] = None
        self._area: Optional[float, np.ndarray, np.ndarray] = None

    @property
    def id(self) -> str:
        return self._measurement_id

    @property
    def date(self) -> str:
        return self._date

    @property
    def info(self) -> str:
        return self._instrument_info

    @property
    def ei(self) -> np.ndarray:
        return self._ei

    @property
    def o(self) -> np.ndarray:
        return self._o

    @property
    def ei_max(self) -> float:
        """Lazy calculation of ei_max, stored in a field after the first call."""
        if self._ei_max is None:
            self._ei_max = self._calculate_ei_max_value(self._ei)
        return self._ei_max

    @property
    def ei_hyper(self) -> float:
        if self._ei_hyper is None:
            self._ei_hyper = self._calculate_ei_hyper_value(self.ei_max)
        return self._ei_hyper

    @property
    def o_max(self) -> float:
        if self._o_max is None:
            self._o_max = self._o[self.max_idx]
        return self._o_max

    @property
    def max_idx(self) -> int:
        if self._o_max_idx is None:
            self._o_max_idx = self._get_o_idx_at_ei_max(self._ei, self.ei_max)
        return self._o_max_idx

    @property
    def o_hyper(self) -> float:
        if self._o_hyper is None:
            self._o_hyper = self._calculate_o_hyper(self._o, self._ei, self.max_idx,
                                                    self.ei_hyper)
        return self._o_hyper

    @property
    def first_peak_idx(self):
        if self._first_peak_idx is None:
            self._first_peak_idx = self._find_prominent_peak(self._ei, self.max_idx)
        return self._first_peak_idx

    @property
    def o_first_peak(self):
        if self._o_first_peak is None:
            self._o_first_peak = self._o[self.first_peak_idx]
        return self._o_first_peak

    @property
    def ei_first_peak(self):
        if self._ei_first_peak is None:
            self._ei_first_peak = self._ei[self.first_peak_idx]
        return self._ei_first_peak

    @property
    def min_idx(self) -> int:
        if self._min_idx is None:
            self._min_idx = self._find_prominent_valley(self._ei, self.first_peak_idx,
                                                        self.max_idx)
        return self._min_idx

    @property
    def o_min(self) -> float:
        if self._o_min is None:
            self._o_min = self._o[self.min_idx]
        return self._o_min

    @property
    def ei_min(self) -> float:
        if self._ei_min is None:
            self._ei_min = self._ei[self.min_idx]
        return self._ei_min

    @property
    def area(self) -> tuple[float, np.ndarray, np.ndarray]:
        if self._area is None:
            self._area = self._calculate_area(self._o, self._ei, self._lower_limit,
                                              self._upper_limit)
        return self._area

    # Returns a data column based on key value
    @staticmethod
    def _get_data_column(data: dict[str, np.ndarray], column: str) -> np.ndarray:
        """Retrieve a data column by key."""
        value = data.get(column)
        if value is None:
            raise DataColumnNotFoundError(f"Column '{column}' not found in data.")
        return value

    # Calculates the highest Elongation Index value
    @staticmethod
    def _calculate_ei_max_value(ei_data: np.ndarray) -> float:
        """Calculate the maximum EI value."""
        if ei_data.size == 0:
            raise InsufficientDataError("EI data is insufficient to calculate max EI value.")
        return float(np.max(ei_data))

    @staticmethod
    def _calculate_ei_hyper_value(ei_max: float) -> float:
        """Calculate EI hyper, which is half of EI max."""
        if ei_max is None:
            raise ValueError("EI maximum is None. Call _calculate_ei_max_value() first.")
        return ei_max / 2

    @staticmethod
    def _get_o_idx_at_ei_max(ei_data: np.ndarray, ei_max: float) -> int:
        """Find the O max value and its corresponding index."""
        indices = np.nonzero(ei_data == ei_max)[0]
        if len(indices) == 0:
            raise InsufficientDataError("EI max not found in the EI array.")
        center_idx = indices[len(indices) // 2]
        return int(center_idx)

    @staticmethod
    def _calculate_o_hyper(o_data: np.ndarray, ei_data: np.ndarray, o_max_idx: int,
                           ei_hyper: float) -> float | None:
        """Interpolate and calculate O hyper based on EI hyper."""
        relevant_o = o_data[o_max_idx:]
        relevant_ei = ei_data[o_max_idx:]

        if len(relevant_ei) < 2:
            raise InsufficientDataError("Not enough data points to perform interpolation.")

        for i, ei_value in enumerate(relevant_ei):
            # Check if ei_value is a tuple
            if isinstance(ei_value, tuple):
                ei_value = ei_value[0]

            if ei_value == ei_hyper:
                return float(relevant_o[i])
            elif ei_value < ei_hyper:
                return OsmoModel._interpolate_two_points(ei_hyper, relevant_ei[i - 1],
                                                         relevant_o[i - 1], relevant_ei[i],
                                                         relevant_o[i])
        return None

    @staticmethod
    def _interpolate_two_points(value, x1, y1, x2, y2) -> float:
        """Linear interpolation between two points."""
        return y1 + (y2 - y1) * (value - x1) / (x2 - x1)

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

    @staticmethod
    def _find_prominent_peak(ei_data: np.ndarray, o_max_idx: int) -> int:
        """Find the peak with the highest prominence before O max."""
        return OsmoModel._find_prominent_point(ei_data[:o_max_idx], find_peaks)

    @staticmethod
    def _find_prominent_valley(ei_data: np.ndarray, first_peak_idx: int, o_max_idx: int) -> int:
        """Find the valley with the highest prominence after the first peak."""
        filtered_ei = ei_data[first_peak_idx:o_max_idx]
        return OsmoModel._find_prominent_point(-filtered_ei, find_peaks, first_peak_idx)

    @staticmethod
    def _calculate_area(o_data: np.ndarray, ei_data, lower_limit: int, upper_limit: int) -> (
            float, np.ndarray, np.ndarray):
        """Calculate area between lower & upper limits set by Lorrca"""

        # Validate limits
        if upper_limit > max(o_data) or lower_limit < min(o_data):
            raise ValueError("Invalid limits for area calculation.")

        # Find indices for Omin and Upper limit
        lower_idx = np.nonzero(o_data >= lower_limit)[0]
        upper_idx = np.nonzero(o_data <= upper_limit)[0]

        if upper_idx.size == 0:
            raise ValueError("Upper limit exceeds available O. values.")
        if lower_idx.size == 0:
            raise ValueError("Lower limit exceeds available O. values.")

        # Get the last index where O. is less than or equal to the upper_limit
        upper_idx = upper_idx[-1]
        # Get the first index where Osmolality is bigger than or equal to the lower_limit
        lower_idx = lower_idx[0]

        # Slice the data for the integration
        o_segment = o_data[lower_idx:upper_idx + 1]
        ei_segment = ei_data[lower_idx:upper_idx + 1]

        # Check if the segments are valid for integration
        if len(o_segment) < 2 or len(ei_segment) < 2:
            raise InsufficientDataError("Not enough data points for area calculation.")

        # Calculate the area using Simpson's rule
        area = integrate.simpson(y=ei_segment, x=o_segment)

        return area, o_segment, ei_segment
