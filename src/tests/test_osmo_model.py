import unittest
import numpy as np
from src.models.osmo_model import OsmoModel
from src.setup import load_data, load_metadata


class TestOsmoModel(unittest.TestCase):
    EXPECTED_UPPER_LIMIT = 450

    def setUp(self):
        """Set up test data for each test method."""
        self.data = load_data()
        self.metadata = load_metadata()
        self.model = OsmoModel(self.data, self.metadata)

    def test_attribute_access(self):
        """Test that attribute-like access works for data and metadata."""
        for key in self.data:
            # Use numpy.array_equal to compare arrays
            self.assertTrue(np.array_equal(self.data[key], getattr(self.model, key)))

        for key in self.metadata:
            self.assertEqual(self.metadata[key], getattr(self.model, key))

    def test_attribute_error(self):
        """Test that accessing a non-existent attribute raises an AttributeError."""
        with self.assertRaises(AttributeError):
            getattr(self.model, "non_existent_attribute")

    def test_o_attribute_mapping(self):
        """Test that accessing 'O' returns the correct data mapped from 'O.'."""
        np.testing.assert_array_equal(self.data["O."], self.model.O)

    def test_non_existent_metadata_access(self):
        """Test that accessing non-existent metadata returns an AttributeError."""
        with self.assertRaises(AttributeError):
            getattr(self.model, "non_existent_metadata")


if __name__ == "__main__":
    unittest.main()
