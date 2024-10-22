import numpy as np
from scipy.signal import find_peaks


class DataColumnNotFoundError(KeyError):
    pass


class InsufficientDataError(ValueError):
    pass


class OsmoModel:
    EI_KEY = 'EI'
    O_KEY = 'O.'

    def __init__(self, osmo_data: dict[str, np.ndarray]):
        self.data = osmo_data
        self._ei = self._get_data_column(self.EI_KEY)
        self._o = self._get_data_column(self.O_KEY)
        self._ei_max = self._calculate_ei_max_value()
        self._ei_hyper = self._calculate_ei_hyper_value()
        self._o_max, self._o_max_idx = self._get_o_max_value_and_idx()
        self._o_hyper = self._calculate_o_hyper()
        self._first_peak_idx = self._find_prominent_peak()
        self._valley_idx = self._find_prominent_valley()

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
    def valley(self):
        if self._valley_idx is not None:
            return self._o[self._valley_idx], self._ei[self._valley_idx]
        return None

    def _get_data_column(self, column: str) -> np.ndarray:
        """Retrieve a data column by key."""
        value = self.data.get(column)
        if value is None:
            raise DataColumnNotFoundError(
                f"Column '{column}' not found in data.")
        return value

    def _calculate_ei_max_value(self) -> float:
        """Calculate the maximum EI value."""
        return float(np.max(self.ei))

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

    def _find_prominent_point(self, data, find_func, offset=0) -> int:
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
