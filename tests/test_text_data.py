"""Small fixtures for headerless parsing and audit counts, independent of private data."""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.text_data import LABELS, canonical_key, duplicate_groups, make_text_protocol, read_ecommerce


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


class TextProtocolTests(unittest.TestCase):
    def test_conflicts_removed_whole_dedup_before_reproducible_split(self):
        records=[(label,f"{label} product {number}") for label in LABELS for number in [1,2,3]]
        records += [("Household","Household product 1"),("Household"," HOUSEHOLD  product ２ "),
                    ("Books","CONFLICT 3"),("Electronics"," conflict ３ "),
                    ("Books"," "),("Books",None),("invalid","valid-looking description")]
        raw=pd.DataFrame(records,columns=["label","text"],dtype="string")
        snapshot=raw.copy(deep=True)
        first=make_text_protocol(raw,test_size=1/3,seed=42)
        second=make_text_protocol(raw,test_size=1/3,seed=42)
        self.assertEqual(first["flow"].removed_rows.tolist(),[0,2,1,2,1,1])
        self.assertEqual(len(first["conflicts"]),1)
        self.assertEqual(len(first["corpus"]),12)
        self.assertNotIn("conflict 3",set(first["corpus"].canonical_key))
        self.assertEqual(first["train"].row_id.tolist(),second["train"].row_id.tolist())
        self.assertTrue(set(first["train"].row_id).isdisjoint(first["test"].row_id))
        self.assertTrue(set(first["train"].canonical_key).isdisjoint(first["test"].canonical_key))
        self.assertEqual(set(first["test"].label),set(LABELS))
        self.assertTrue(first["corpus"].text.is_unique)
        self.assertEqual(first["corpus"].iloc[0].row_id,0)
        pd.testing.assert_frame_equal(raw,snapshot)
        for row in first["corpus"].itertuples():
            self.assertEqual(row.text,raw.iloc[row.row_id].text)


if __name__ == "__main__":
    unittest.main()
