import unittest
import numpy as np
from src.models.osmo_model import OsmoModel, DataColumnNotFoundError, MissingDataError
from src.setup import load_data, load_metadata


class TestOsmoModel(unittest.TestCase):
    # Constants for expected results
    EXPECTED_O_MAX = 213
    EXPECTED_EI_MAX = 0.517
    EXPECTED_O_HYPER = 364
    EXPECTED_EI_HYPER = 0.259
    EXPECTED_O_MIN = 114
    EXPECTED_EI_MIN = 0.228
    EXPECTED_AREA = 124

    def setUp(self):
        """Set up test data for each test method."""
        self.data = load_data()
        self.metadata = load_metadata()
        self.model = OsmoModel(self.data, self.metadata)

    # Properties Testing
    def test_get_ei(self):
        """Test that the 'EI' property returns the correct data."""
        np.testing.assert_array_equal(self.data["EI"], self.model.get_ei)

    def test_get_o_max(self):
        """Test that o_max returns the expected maximum O value."""
        rounded_result = round(self.model.get_o_max)
        self.assertEqual(self.EXPECTED_O_MAX, rounded_result)

    def test_get_ei_max(self):
        """Test that ei_max returns the expected maximum EI value."""
        self.assertEqual(self.EXPECTED_EI_MAX, self.model.get_ei_max)

    def test_get_o_hyper(self):
        """Test that o_hyper returns the expected O value."""
        rounded_result = round(self.model.get_o_hyper)
        self.assertEqual(self.EXPECTED_O_HYPER, rounded_result)

    def test_get_ei_hyper(self):
        """Test that ei_hyper returns the expected EI value."""
        rounded_result = round(self.model.get_ei_hyper, 3)
        self.assertEqual(self.EXPECTED_EI_HYPER, rounded_result)

    def test_get_o_min(self):
        """Test that o_min returns the expected O value."""
        rounded_result = round(self.model.get_o_min)
        self.assertEqual(self.EXPECTED_O_MIN, rounded_result)

    def test_get_ei_min(self):
        """Test that o_min returns the expected O value."""
        self.assertEqual(self.EXPECTED_EI_MIN, self.model.get_ei_min)

    def test_get_area(self):
        """Test that area returns the expected area value."""
        # Get area value without plotting segments
        area, _, _ = self.model.get_area
        area = round(area)
        self.assertEqual(self.EXPECTED_AREA, area)

    # Calculations
    def test_two_points_interpolation(self):
        # Test data
        x1, y1, x2, y2 = 10, 10, 20, 20

        value = 15
        expected_interpolated_ei_value = 15

        result = self.model._interpolate_two_points(value, x1, y1, x2, y2)
        self.assertEqual(expected_interpolated_ei_value, result)


if __name__ == "__main__":
    unittest.main()
