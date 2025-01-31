import unittest
import numpy as np
from src.models.osmo_model import OsmoModel
from src.models.oxy_model import OxyModel

# Define constants for shared data and metadata
DATA = {'O.': np.array([1, 2, 3])}
ALT_DATA = {'O.': np.array([4, 5, 6])}
OSMO_METADATA = {'measurement_id': 'osmo123'}
OXY_METADATA = {'patient_name': 'John Doe'}
EXPECTED_OSMO_NAME = 'osmo123'
EXPECTED_OXY_NAME = 'John Doe'

class TestScanModels(unittest.TestCase):

    # Test the initialization of the OsmoModel
    def test_osmo_model_initialization(self):
        model = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)

        # Test default behavior for `O` (should match the 'O.' data key)
        self.assertTrue(np.array_equal(model.O, DATA['O.']))

        # Test that 'name' correctly maps to 'measurement_id' in metadata
        self.assertEqual(model.name, EXPECTED_OSMO_NAME)

        # Test attribute-like access for 'measurement_id'
        self.assertEqual(model.measurement_id, EXPECTED_OSMO_NAME)

    # Test the __getattr__ behavior in OsmoModel
    def test_osmo_model_getattr(self):
        model = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)

        # Test that accessing 'O' returns the correct data
        self.assertTrue(np.array_equal(model.O, DATA['O.']))

        # Test that accessing 'name' returns the correct metadata value
        self.assertEqual(model.name, EXPECTED_OSMO_NAME)

        # Test for missing attribute, should raise AttributeError
        with self.assertRaises(AttributeError):
            getattr(model, 'non_existent_key')

    # Test the initialization of the OxyModel
    def test_oxy_model_initialization(self):
        model = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)

        # Test that 'name' maps to 'patient_name' in metadata
        self.assertEqual(model.name, EXPECTED_OXY_NAME)

        # Test attribute-like access for 'patient_name'
        self.assertEqual(model.patient_name, EXPECTED_OXY_NAME)

    # Test the __getattr__ behavior in OxyModel
    def test_oxy_model_getattr(self):
        model = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)

        # Test that accessing 'name' returns the correct metadata value
        self.assertEqual(model.name, EXPECTED_OXY_NAME)

        # Test for missing attribute, should raise AttributeError
        with self.assertRaises(AttributeError):
            getattr(model, 'non_existent_key')

    # Test equality comparison (__eq__) for OsmoModel instances
    def test_osmo_model_equality(self):
        model1 = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)
        model2 = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)

        # Models with the same data and metadata should be equal
        self.assertEqual(model1, model2)

        # Change data and check equality (models should not be equal)
        model3 = OsmoModel(data=ALT_DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)
        self.assertNotEqual(model1, model3)

    # Test equality comparison (__eq__) for OxyModel instances
    def test_oxy_model_equality(self):
        model1 = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)
        model2 = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)

        # Models with the same data and metadata should be equal
        self.assertEqual(model1, model2)

        # Change data and check equality (models should not be equal)
        model3 = OxyModel(data=ALT_DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)
        self.assertNotEqual(model1, model3)

    # Test hashing (__hash__) for OsmoModel instances
    def test_osmo_model_hash(self):
        model1 = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)
        model2 = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)

        # Models with the same data and metadata should have the same hash
        self.assertEqual(hash(model1), hash(model2))

        # Modify data and check hashes (should be different)
        model3 = OsmoModel(data=ALT_DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)
        self.assertNotEqual(hash(model1), hash(model3))

    # Test hashing (__hash__) for OxyModel instances
    def test_oxy_model_hash(self):
        model1 = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)
        model2 = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)

        # Models with the same data and metadata should have the same hash
        self.assertEqual(hash(model1), hash(model2))

        # Modify data and check hashes (should be different)
        model3 = OxyModel(data=ALT_DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)
        self.assertNotEqual(hash(model1), hash(model3))

    # Test the __repr__ string representation for OsmoModel instances
    def test_osmo_model_repr(self):
        model = OsmoModel(data=DATA, metadata=OSMO_METADATA, name=EXPECTED_OSMO_NAME)
        self.assertEqual(repr(model), f"OsmoModel(id={model.id})")

    # Test the __repr__ string representation for OxyModel instances
    def test_oxy_model_repr(self):
        model = OxyModel(data=DATA, metadata=OXY_METADATA, name=EXPECTED_OXY_NAME)
        self.assertEqual(repr(model), f"OxyModel(id={model.id})")


# Run all the tests
if __name__ == "__main__":
    unittest.main()
