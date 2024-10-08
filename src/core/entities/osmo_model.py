import numpy as np
from scipy.signal import find_peaks


class OsmoModel:
    def __init__(self, osmo_data: dict):
        self.data = osmo_data
        #
        self._ei_max = self._calculate_ei_max_value()
        self._ei_hyper = self._calculate_ei_hyper_value()
        self._o_max, self._o_max_idx = self._get_o_max_value_and_inx()
        self._o_hyper = self._calculate_o_hyper()
        self._first_peak_idx = self._get_peak_with_highest_prominence()
        self._valley_idx = self._get_valley_with_highest_prominence()

    @property
    def ei(self):
        return self._get_data_column("EI")

    @property
    def o(self):
        return self._get_data_column("O.")

    @property
    def ei_max(self):
        return self._ei_max

    @property
    def ei_hyper(self):
        return self._ei_hyper

    @property
    def o_hyper(self):
        return self._o_hyper

    @property
    def o_max(self):
        return self._o_max

    @property
    def o_max_idx(self):
        return self._o_max_idx

    @property
    def first_peak_idx(self):
        return self._first_peak_idx

    @property
    def valley_idx(self):
        return self._valley_idx


    def _get_data_column(self, column: str) -> np.ndarray:
        value = self.data.get(column)
        if value is not None:
            return np.array(value)
        else:
            raise KeyError(f"The column '{column}' does not exist.")

    def _calculate_ei_max_value(self):
        return max(self.ei)

    def _calculate_ei_hyper_value(self):
        if self.ei_max is None:
            raise ValueError("EI max has not been calculated.")
        return self.ei_max / 2

    def _get_o_max_value_and_inx(self):
        # Find the indices where EI equals EI_max
        indices = np.nonzero(self.ei == self.ei_max)[0]

        if len(indices) == 0:
            raise ValueError("EI max not found in the EI array")

        # Get the middle index if there are multiple occurrences of EI_max
        _center_idx = indices[len(indices) // 2]

        # Return the corresponding O value and the index
        return self.o[_center_idx], _center_idx

    def _calculate_o_hyper(self):
        # Check if EI_hyper is calculated
        if self.ei_hyper is None:
            raise ValueError("EI hyper has not been calculated.")

        # Get the relevant part of the curve
        relevant_ei_values = self.ei[self._o_max_idx:]
        relevant_o_values = self.o[self._o_max_idx:]

        if len(relevant_ei_values) < 2:
            raise ValueError(
                "Not enough data points to perform interpolation.")

        # Search if EI_hyper already exist or for the first point where EI < EI_hyper
        for i, ei_value in enumerate(relevant_ei_values):
            # Check for an exact match with EI_hyper
            if ei_value == self._ei_hyper:
                return relevant_o_values[i]

            elif ei_value < self._ei_hyper:
                # Perform linear interpolation
                # Get the previous and current points for interpolation
                if i == 0:
                    return None  # Cannot interpolate if no prior point exists

                x1, y1 = relevant_ei_values[i - 1], relevant_o_values[i - 1]
                x2, y2 = relevant_ei_values[i], relevant_o_values[i]

                # Calculate O hyper using linear interpolation
                o_hyper = y1 + (y2 - y1) * (self._ei_hyper - x1) / (x2 - x1)
                return o_hyper

        return None  # If no point found

    def _get_peak_with_highest_prominence(self):
        filtered_ei = self.ei[:self._o_max_idx]

        peaks, properties = find_peaks(filtered_ei, prominence=0)
        prominences = properties['prominences']
        highest_prominence_idx = np.argmax(prominences)
        highest_prominence_peak_idx = peaks[highest_prominence_idx]
        return highest_prominence_peak_idx

    def _get_valley_with_highest_prominence(self):
        filtered_ei = self.ei[self._first_peak_idx:self._o_max_idx]
        valleys, properties = find_peaks(-filtered_ei, prominence=0)
        prominences = properties['prominences']
        lowest_prominence_idx = np.argmax(prominences)
        valley_idx = valleys[lowest_prominence_idx] + self._first_peak_idx
        return valley_idx
