import unittest
import numpy as np
from src.core.models.osmo_model import OsmoModel
from src.setup import load_data, load_metadata


class TestOsmoModel(unittest.TestCase):
    # Constants for expected results
    EXPECTED_EI_MAX = 0.517
    EXPECTED_O_MAX = 213
    EXPECTED_EI_HYPER = 0.259
    EXPECTED_O_HYPER = 364
    EXPECTED_EI_MIN = 0.228
    EXPECTED_O_MIN = 114
    EXPECTED_AREA = 124

    def setUp(self):
        """Set up test data for each test method."""
        self.data = load_data()
        self.metadata = load_metadata()
        self.model = OsmoModel(self.data, self.metadata)

    def test_get_ei(self):
        """Test that the 'EI' property returns the correct data."""
        np.testing.assert_array_equal(self.model.ei, self.data["EI"])

    def test_get_ei_max(self):
        """Test that ei_max returns the expected maximum EI value."""
        self.assertEqual(self.model.ei_max, self.EXPECTED_EI_MAX)

    def test_get_o_max(self):
        """Test that o_max returns the expected Osmolality value at ei_max."""
        rounded_o_max = round(self.model.o_max)
        self.assertEqual(rounded_o_max, self.EXPECTED_O_MAX)

    def test_get_ei_hyper(self):
        """Test that ei_hyper returns the expected value."""
        rounded_ei_hyper = round(self.model.ei_hyper, 3)
        self.assertEqual(rounded_ei_hyper, self.EXPECTED_EI_HYPER)

    def test_get_o_hyper(self):
        """Test that o_hyper returns the expected value."""
        rounded_o_hyper = round(self.model.o_hyper)
        self.assertEqual(rounded_o_hyper, self.EXPECTED_O_HYPER)

    def test_get_ei_min(self):
        """Test that ei_min returns the expected minimum EI value."""
        rounded_ei_min = round(self.model.min[1], 3)
        self.assertEqual(rounded_ei_min, self.EXPECTED_EI_MIN)

    def test_get_o_min(self):
        """Test that o_min returns the expected minimum Osmolality value."""
        rounded_o_min = round(self.model.min[0])
        self.assertEqual(rounded_o_min, self.EXPECTED_O_MIN)

    def test_get_area(self):
        """Test that area calculation returns the expected value."""
        rounded_area = round(self.model.area[0])
        self.assertEqual(rounded_area, self.EXPECTED_AREA)


if __name__ == "__main__":
    unittest.main()
