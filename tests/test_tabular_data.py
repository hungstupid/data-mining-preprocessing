"""Data-boundary fixtures for independent tabular chapters; no private CSV required."""
import hashlib
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from src.tabular_data import load_data, prepare_numeric_training, split_data


class TabularDataTests(unittest.TestCase):
    def test_read_preserves_zip_tokens_and_source_bytes(self):
        frame = pd.DataFrame({"patient_id": [1, 2, 3, 4], "patient_zip3": ["001", "002", "999", "001"],
                              "DiagPeriodL90D": [0, 1, 1, 0], "measurement": [2., 3., 4., 5.]})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"data/raw/training.csv"
            path.parent.mkdir(parents=True)
            frame.to_csv(path, index=False)
            before = path.read_bytes()
            loaded, checksum = load_data(directory, expected_shape=(4, 4))
            self.assertEqual(loaded.patient_zip3.tolist(), ["001", "002", "999", "001"])
            self.assertEqual(checksum, hashlib.sha256(before).hexdigest())
            self.assertEqual(path.read_bytes(), before)

    def test_split_is_group_disjoint_and_label_independent(self):
        frame = pd.DataFrame({"patient_zip3": np.repeat([f"{i:03}" for i in range(40)], 3),
                              "DiagPeriodL90D": np.tile([0, 1, 0], 40)})
        first = split_data(frame)
        changed = frame.assign(DiagPeriodL90D=1-frame.DiagPeriodL90D)
        second = split_data(changed)
        self.assertEqual([len(index) for index in first], [72, 24, 24])
        for left, right in zip(first, second):
            np.testing.assert_array_equal(left, right)
        for left, right in [(first[0], first[1]), (first[0], first[2]), (first[1], first[2])]:
            self.assertFalse(set(frame.loc[left, 'patient_zip3']) & set(frame.loc[right, 'patient_zip3']))
        self.assertEqual(set().union(*(set(index) for index in first)), set(frame.index))

    def test_preparation_uses_only_training_and_restores_known_values(self):
        frame = pd.DataFrame({"a": [0., 2., 4., np.nan, 1e9],
                              "b": [10., 10., 20., 30., -1e9]}, index=[10, 20, 30, 40, 50])
        before = frame.copy(deep=True)
        original, missing, scaler, imputer, standardized, completed, completed_z = prepare_numeric_training(
            frame, pd.Index([10, 20, 30, 40]), ["a", "b"])
        np.testing.assert_allclose(scaler.mean_, [2., 17.5])
        self.assertEqual(imputer._fit_X.shape, (4, 2))
        np.testing.assert_allclose(completed.loc[40, 'a'], 2.)
        pd.testing.assert_frame_equal(completed.where(~missing), original)
        pd.testing.assert_frame_equal(frame, before)
        self.assertTrue(np.isfinite(completed_z.to_numpy()).all())
        self.assertTrue(np.isnan(standardized[3, 0]))


if __name__ == '__main__':
    unittest.main()
