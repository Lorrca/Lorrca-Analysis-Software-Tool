import unittest
import numpy as np
from src.core.models.osmo_model import OsmoModel
from src.setup import load_data


class TestOsmoModel(unittest.TestCase):
    EXPECTED_EI_MAX = 0.517
    EXPECTED_O_MAX = 213
    EXPECTED_EI_HYPER = 0.259
    EXPECTED_O_HYPER = 364
    EXPECTED_EI_MIN = 0.228
    EXPECTED_O_MIN = 114

    def setUp(self):
        """Set up test data."""
        self.data = load_data()
        self.model = OsmoModel(self.data)

    def test_get_ei(self):
        """Test get_ei calls get_property for the 'EI' column."""
        expected_result = self.data["EI"]
        actual_result = self.model.ei

        np.testing.assert_array_equal(actual_result, expected_result)

    def test_get_ei_max(self):
        """Test ei_max returns expected result."""
        expected_result = self.EXPECTED_EI_MAX
        actual_result = self.model.ei_max  # Ensure this property exists

        self.assertEqual(expected_result, actual_result)

    def test_get_o_max(self):
        """Test o_max returns expected result."""
        expected_result = self.EXPECTED_O_MAX
        actual_result = round(self.model.o_max)  # Ensure this property exists

        self.assertEqual(expected_result, actual_result)

    def test_get_ei_hyper(self):
        """Test ei_hyper returns expected result."""
        expected_result = self.EXPECTED_EI_HYPER
        actual_result = round(self.model.ei_hyper, 3)  # Ensure this property exists

        self.assertEqual(expected_result, actual_result)

    def test_get_o_hyper(self):
        """Test o_hyper returns expected result."""
        expected_result = self.EXPECTED_O_HYPER
        actual_result = round(self.model.o_hyper)  # Ensure this property exists

        self.assertEqual(expected_result, actual_result)

    def test_get_ei_min(self):
        """Test ei_min returns the expected result at the valley index."""
        ei_min = self.model.min[1]  # Ensure valley_idx is defined
        expected_result = self.EXPECTED_EI_MIN
        actual_result = round(ei_min, 3)  # Using get_ei method

        self.assertEqual(expected_result, actual_result)

    def test_get_o_min(self):
        """Test o_min returns the expected result at the valley index."""
        o_min = self.model.min[0]
        expected_result = self.EXPECTED_O_MIN
        actual_result = round(o_min)  # Ensure this property exists

        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
