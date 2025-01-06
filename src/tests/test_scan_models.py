import unittest
import numpy as np
from src.models.osmo_model import OsmoModel
from src.models.oxy_model import OxyModel


class TestScanModels(unittest.TestCase):

    # Test the initialization of the OsmoModel
    def test_osmo_model_initialization(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'measurement_id': 'osmo123'}

        model = OsmoModel(data=data, metadata=metadata)

        # Test default behavior for `O` (should match the 'O.' data key)
        self.assertTrue(np.array_equal(model.O, np.array([1, 2, 3])))

        # Test that 'name' correctly maps to 'measurement_id' in metadata
        self.assertEqual(model.name, 'osmo123')

        # Test attribute-like access for 'measurement_id'
        self.assertEqual(model.measurement_id, 'osmo123')

    # Test the __getattr__ behavior in OsmoModel
    def test_osmo_model_getattr(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'measurement_id': 'osmo123'}

        model = OsmoModel(data=data, metadata=metadata)

        # Test that accessing 'O' returns the correct data
        self.assertTrue(np.array_equal(model.O, np.array([1, 2, 3])))

        # Test that accessing 'name' returns the correct metadata value
        self.assertEqual(model.name, 'osmo123')

        # Test for missing attribute, should raise AttributeError
        with self.assertRaises(AttributeError):
            getattr(model, 'non_existent_key')

    # Test the initialization of the OxyModel
    def test_oxy_model_initialization(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'patient_name': 'John Doe'}

        model = OxyModel(data=data, metadata=metadata)

        # Test that 'name' maps to 'patient_name' in metadata
        self.assertEqual(model.name, 'John Doe')

        # Test attribute-like access for 'patient_name'
        self.assertEqual(model.patient_name, 'John Doe')

    # Test the __getattr__ behavior in OxyModel
    def test_oxy_model_getattr(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'patient_name': 'John Doe'}

        model = OxyModel(data=data, metadata=metadata)

        # Test that accessing 'name' returns the correct metadata value
        self.assertEqual(model.name, 'John Doe')

        # Test for missing attribute, should raise AttributeError
        with self.assertRaises(AttributeError):
            getattr(model, 'non_existent_key')

    # Test equality comparison (__eq__) for OsmoModel instances
    def test_osmo_model_equality(self):
        data1 = {'O.': np.array([1, 2, 3])}
        metadata1 = {'measurement_id': 'osmo123'}
        model1 = OsmoModel(data=data1, metadata=metadata1)

        data2 = {'O.': np.array([1, 2, 3])}
        metadata2 = {'measurement_id': 'osmo123'}
        model2 = OsmoModel(data=data2, metadata=metadata2)

        # Models with the same data and metadata should be equal
        self.assertEqual(model1, model2)

        # Change data and check equality (models should not be equal)
        data3 = {'O.': np.array([4, 5, 6])}
        model3 = OsmoModel(data=data3, metadata=metadata2)

        # Models with different data should not be equal
        self.assertNotEqual(model1, model3)

    # Test equality comparison (__eq__) for OxyModel instances
    def test_oxy_model_equality(self):
        data1 = {'O.': np.array([1, 2, 3])}
        metadata1 = {'patient_name': 'John Doe'}
        model1 = OxyModel(data=data1, metadata=metadata1)

        data2 = {'O.': np.array([1, 2, 3])}
        metadata2 = {'patient_name': 'John Doe'}
        model2 = OxyModel(data=data2, metadata=metadata2)

        # Models with the same data and metadata should be equal
        self.assertEqual(model1, model2)

        # Change data and check equality (models should not be equal)
        data3 = {'O.': np.array([4, 5, 6])}
        model3 = OxyModel(data=data3, metadata=metadata2)

        # Models with different data should not be equal
        self.assertNotEqual(model1, model3)

    # Test hashing (__hash__) for OsmoModel instances
    def test_osmo_model_hash(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'measurement_id': 'osmo123'}

        model1 = OsmoModel(data=data, metadata=metadata)
        model2 = OsmoModel(data=data, metadata=metadata)

        # Models with the same data and metadata should have the same hash
        self.assertEqual(hash(model1), hash(model2))

        # Modify data and check hashes (should be different)
        data3 = {'O.': np.array([4, 5, 6])}
        model3 = OsmoModel(data=data3, metadata=metadata)

        # Models with different data should have different hashes
        self.assertNotEqual(hash(model1), hash(model3))

    # Test hashing (__hash__) for OxyModel instances
    def test_oxy_model_hash(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'patient_name': 'John Doe'}

        model1 = OxyModel(data=data, metadata=metadata)
        model2 = OxyModel(data=data, metadata=metadata)

        # Models with the same data and metadata should have the same hash
        self.assertEqual(hash(model1), hash(model2))

        # Modify data and check hashes (should be different)
        data3 = {'O.': np.array([4, 5, 6])}
        model3 = OxyModel(data=data3, metadata=metadata)

        # Models with different data should have different hashes
        self.assertNotEqual(hash(model1), hash(model3))

    # Test the __repr__ string representation for OsmoModel instances
    def test_osmo_model_repr(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'measurement_id': 'osmo123'}

        model = OsmoModel(data=data, metadata=metadata)

        # Test string representation format
        self.assertEqual(repr(model), "OsmoModel(id=" + model.id + ")")

    # Test the __repr__ string representation for OxyModel instances
    def test_oxy_model_repr(self):
        data = {'O.': np.array([1, 2, 3])}
        metadata = {'patient_name': 'John Doe'}

        model = OxyModel(data=data, metadata=metadata)

        # Test string representation format
        self.assertEqual(repr(model), "OxyModel(id=" + model.id + ")")


# Run all the tests
if __name__ == "__main__":
    unittest.main()
