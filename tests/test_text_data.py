"""Small fixtures for headerless parsing and audit counts, independent of private data."""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.text_data import canonical_key, duplicate_groups, read_ecommerce


class TextSourceTests(unittest.TestCase):
    def test_headerless_first_record_and_literal_na_survive(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            path.write_text('Household,"first, product"\nBooks,NA\nElectronics,\n', encoding="utf-8")
            frame = read_ecommerce(path)
        self.assertEqual(frame.shape, (3, 2))
        self.assertEqual(frame.iloc[0].tolist(), ["Household", "first, product"])
        self.assertEqual(frame.iloc[1].text, "NA")
        self.assertTrue(pd.isna(frame.iloc[2].text))

    def test_extra_column_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            path.write_text("Household,text,extra\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_ecommerce(path)

    def test_groups_excess_conflicts_and_canonical_boundaries(self):
        frame = pd.DataFrame({"label": ["A", "A", "B", "A", "A"],
                              "text": ["USB 3!", "USB 3!", "USB 3!", " usb ３! ", "USB 4!"]})
        exact = duplicate_groups(frame, frame.text)
        canonical = duplicate_groups(frame, frame.text.map(canonical_key))
        self.assertEqual(int(exact.rows.gt(1).sum()), 1)
        self.assertEqual(int((exact.rows - 1).sum()), 2)
        self.assertEqual(int(exact.labels.gt(1).sum()), 1)
        self.assertEqual(int((canonical.rows - 1).sum()), 3)
        self.assertEqual(canonical_key(" USB\t３! "), "usb 3!")
        self.assertNotEqual(canonical_key("USB 3!"), canonical_key("USB 4!"))
        self.assertNotEqual(canonical_key("USB 3!"), canonical_key("USB 3?"))


if __name__ == "__main__":
    unittest.main()
