import numpy as np


class OsmoModel:
    def __init__(self, osmo_data: dict):
        self.data = osmo_data
        #
        self._ei_max = self._calculate_ei_max()
        self._ei_hyper = self._calculate_ei_hyper()
        self._o_max = self._get_o_max()
        self._o_hyper = self._calculate_o_hyper()

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

    def _get_data_column(self, column: str) -> list:
        value = self.data.get(column)
        if value is not None:
            return value
        else:
            raise KeyError(f"The column '{column}' does not exist.")

    def _calculate_ei_max(self):
        return max(self.ei)

    def _calculate_ei_hyper(self):
        if self.ei_max is None:
            raise ValueError("EI max has not been calculated.")
        return self.ei_max / 2

    def _get_o_max(self):
        indices = [i for i, ei_value in enumerate(self.ei) if
                   ei_value == self.ei_max]
        if not indices:
            raise ValueError("EI max not found in the EI list")
        center_index = indices[len(indices) // 2]
        return self.o[center_index]

    def _calculate_o_hyper(self):
        # Check if EI_hyper is calculated
        if self.ei_hyper is None:
            raise ValueError("EI hyper has not been calculated.")

        o_max_pos = self.o.index(self._o_max)

        # Get the relevant part of the curve
        relevant_ei_values = self.ei[o_max_pos + 1:]
        relevant_o_values = self.o[o_max_pos + 1:]

        if len(relevant_ei_values) < 2:
            raise ValueError(
                "Not enough data points to perform interpolation.")

        # Search if EI_hyper already exist or for the first point where EI < EI_hyper
        for i, ei_value in enumerate(relevant_ei_values):
            # Check for an exact match with EI_hyper
            if ei_value == self.ei_hyper:
                return relevant_o_values[i]

            elif ei_value < self.ei_hyper:
                # Perform linear interpolation
                # Get the previous and current points for interpolation
                if i == 0:
                    return None  # Cannot interpolate if no prior point exists

                x1, y1 = relevant_ei_values[i - 1], relevant_o_values[i - 1]
                x2, y2 = relevant_ei_values[i], relevant_o_values[i]

                # Calculate O hyper using linear interpolation
                _o_hyper = y1 + (y2 - y1) * (self.ei_hyper - x1) / (x2 - x1)
                return _o_hyper

        return None  # If no point found
