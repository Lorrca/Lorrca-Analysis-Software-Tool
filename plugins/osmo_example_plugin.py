import numpy as np
from scipy.signal import find_peaks

from src.base_classes.base_plugin import BasePlugin


class OsmoExamplePlugin(BasePlugin):
    @property
    def plugin_name(self):
        return "Osmo Example Plugin"

    def run_plugin(self, model):
        self.model = model
        o = self.model.O
        ei = self.model.EI

        # Calculate primary values
        ei_max = self._calculate_ei_max_value(ei)
        ei_hyper = self._calculate_ei_hyper_value(ei_max)

        max_idx = self._get_o_idx_at_ei_max(ei, ei_max)

        o_max = o[max_idx]
        o_hyper = self._calculate_o_hyper(o, ei, max_idx, ei_hyper)

        first_peak_idx = self._find_prominent_peak(ei, max_idx)
        o_first_peak = o[first_peak_idx]
        ei_first_peak = ei[first_peak_idx]

        min_idx = self._find_prominent_valley(ei, first_peak_idx, max_idx)
        o_min = o[min_idx]
        ei_min = ei[min_idx]

        area, o_segment, ei_segment = self._calculate_area(o, ei, self.model.lower_limit,
                                                           self.model.upper_limit)

        # Draw elements
        self.draw_raw(o, ei)
        self.draw_ei_max(o_max, ei_max)
        self.draw_hyper(o_hyper, ei_hyper)
        self.draw_first_peak(o_first_peak, ei_first_peak)
        self.draw_valley(o_min, ei_min)
        self.draw_area(o_segment, ei_segment, area)

    # Draw raw data
    def draw_raw(self, o, ei):
        self.add_line_element(o, ei, label="Raw O vs EI")

    # Draw EI max
    def draw_ei_max(self, o_max, ei_max):
        self.add_point_element(o_max, ei_max, label="EI max")

    # Draw hyper point
    def draw_hyper(self, o_hyper, ei_hyper):
        self.add_point_element(o_hyper, ei_hyper, label="Hyper")

    # Draw first prominent peak
    def draw_first_peak(self, o_first_peak, ei_first_peak):
        self.add_point_element(o_first_peak, ei_first_peak, label="First Peak")

    # Draw valley
    def draw_valley(self, o_min, ei_min):
        self.add_point_element(o_min, ei_min, label="Valley")

    # Draw area between limits
    def draw_area(self, o_segment, ei_segment, area):
        y2 = np.zeros_like(ei_segment)
        self.add_area_element(o_segment, ei_segment, y2, label=f"Area: {area:.2f}")

    @staticmethod
    def _calculate_ei_max_value(ei_data: np.ndarray) -> float:
        return float(np.max(ei_data))

    @staticmethod
    def _calculate_ei_hyper_value(ei_max: float) -> float:
        return ei_max / 2

    @staticmethod
    def _get_o_idx_at_ei_max(ei_data: np.ndarray, ei_max: float) -> int:
        indices = np.nonzero(ei_data == ei_max)[0]
        center_idx = indices[len(indices) // 2]
        return int(center_idx)

    def _calculate_o_hyper(self, o_data: np.ndarray, ei_data: np.ndarray, o_max_idx: int,
                           ei_hyper: float) -> float | None:
        relevant_o = o_data[o_max_idx:]
        relevant_ei = ei_data[o_max_idx:]

        for i, ei_value in enumerate(relevant_ei):
            if ei_value == ei_hyper:
                return float(relevant_o[i])
            elif ei_value < ei_hyper:
                return self._interpolate_two_points(ei_hyper, relevant_ei[i - 1], relevant_o[i - 1],
                                                    relevant_ei[i], relevant_o[i])
        return None

    @staticmethod
    def _interpolate_two_points(value, x1, y1, x2, y2) -> float:
        return y1 + (y2 - y1) * (value - x1) / (x2 - x1)

    @staticmethod
    def _find_prominent_peak(ei_data: np.ndarray, o_max_idx: int) -> int:
        peaks, properties = find_peaks(ei_data[:o_max_idx], prominence=0)
        if not peaks.size:
            raise ValueError("No prominent peak found.")
        return peaks[np.argmax(properties['prominences'])]

    @staticmethod
    def _find_prominent_valley(ei_data: np.ndarray, first_peak_idx: int, o_max_idx: int) -> int:
        filtered_ei = -ei_data[first_peak_idx:o_max_idx]
        peaks, properties = find_peaks(filtered_ei, prominence=0)
        if not peaks.size:
            raise ValueError("No prominent valley found.")
        return first_peak_idx + peaks[np.argmax(properties['prominences'])]

    @staticmethod
    def _calculate_area(o_data: np.ndarray, ei_data: np.ndarray, lower_limit: int,
                        upper_limit: int) -> tuple[float, np.ndarray, np.ndarray]:
        lower_idx = np.searchsorted(o_data, lower_limit, side='left')
        upper_idx = np.searchsorted(o_data, upper_limit, side='right')

        o_segment = o_data[lower_idx:upper_idx]
        ei_segment = ei_data[lower_idx:upper_idx]

        if len(o_segment) < 2:
            raise ValueError("Not enough data points for area calculation.")

        area = np.trapz(ei_segment, o_segment)
        return area, o_segment, ei_segment
