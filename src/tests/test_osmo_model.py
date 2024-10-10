import unittest

from src.core.models.osmo_model import OsmoModel


class TestOsmoModel(unittest.TestCase):

    def setUp(self):
        """Set up test data."""
        self.data = {
            "EI": [0.1, 0.2, 0.3],
            "OtherColumn": [10, 20, 30]
        }
        self.model = OsmoModel(self.data)

    def test_get_property_valid_column(self):
        """Test get_property returns the correct values for an existing column."""
        expected_result = [0.1, 0.2, 0.3]
        self.assertEqual(self.model._get_data_column("EI"), expected_result)

    def test_get_property_invalid_column(self):
        """Test get_property raises KeyError when the column does not exist."""
        with self.assertRaises(KeyError):
            self.model._get_data_column("NonExistentColumn")

    def test_get_ei(self):
        """Test get_ei calls get_property for the 'EI' column."""
        expected_result = [0.1, 0.2, 0.3]
        self.assertEqual(self.model._get_data_column("EI"), expected_result)


if __name__ == "__main__":
    unittest.main()
