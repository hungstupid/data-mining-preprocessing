"""Known-answer checks of shared Stage 02 views and its notebook BPE definitions."""
from collections import Counter
from functools import wraps
from pathlib import Path
import html
import re
import unicodedata
import unittest

import nbformat
import numpy as np
import pandas as pd
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders

from src.text_preprocessing import normalize_default


class Stage02DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        namespace={"Counter":Counter,"wraps":wraps,"html":html,"re":re,"unicodedata":unicodedata,
                   "np":np,"pd":pd,"Tokenizer":Tokenizer,"models":models,"trainers":trainers,
                   "pre_tokenizers":pre_tokenizers,"decoders":decoders}
        path=Path(__file__).resolve().parents[1]/"book/text/02_normalization_tokenization.ipynb"
        notebook=nbformat.read(path,as_version=4)
        for cell in notebook.cells:
            if "stage02-functions" in cell.metadata.get("tags",[]):
                exec(compile(cell.source,str(path),"exec"),namespace)
        cls.functions=namespace

    def test_missing_empty_numeric_and_markup_boundaries(self):
        f=self.functions
        for name in ["unicode_nfkc","lowercase","remove_html_tags","decode_entities","remove_urls",
                     "remove_mentions","remove_hashtag_marker","conditional_symbols","keep_numbers",
                     "drop_standalone_numbers","normalize_whitespace","light_input"]:
            for missing in [None,pd.NA,np.nan]:
                self.assertTrue(pd.isna(f[name](missing)),name)
            self.assertEqual(f[name](""),"",name)
        self.assertEqual(f["normalize_whitespace"](f["drop_standalone_numbers"]("10cm A12 12 3.5 -7")),"10cm A12")
        self.assertEqual(f["remove_hashtag_marker"]("#A12 #sale"),"A12 sale")
        text='weight <5 kg <10cm> <b title="a > b">bold</b> &lt;3'
        cleaned=f["light_input"](text)
        self.assertEqual(cleaned,"weight <5 kg <10cm> bold <3")
        self.assertEqual(f["light_input"]("Don't stop. Second sentence!"),"Don't stop. Second sentence!")
        self.assertEqual(f["conditional_symbols"]("M3-10 2.5cm 5% <3"),"M3-10 2.5cm 5% <3")
        # Freeze the documented Stage 02 policy, including its known mention-loss risk.
        self.assertEqual(normalize_default("@home <b>USB3</b> #A12 10cm &amp; 12."),"usb3 a12 10cm 12.")

    def test_oov_counts_occurrences_rather_than_unique_types(self):
        unknown,total,rate=self.functions["oov_counts"](Counter(["known","new","known","new","other"]),{"known","other"})
        self.assertEqual((unknown,total),(2,5))
        self.assertAlmostEqual(rate,.4)

    def test_bpe_consumes_training_iterator_and_freezes_during_encoding(self):
        training=["common gadget common gadget"]*3
        seen=[]
        def training_only():
            for text in training:
                seen.append(text)
                yield text
        bpe=self.functions["fit_bpe"](training_only(),vocab_size=300,min_frequency=2)
        self.assertEqual(seen,training)
        before=bpe.to_str()
        held_out="NEVERSEEN 🚀 123 xyz"
        encoded=bpe.encode(held_out,add_special_tokens=False)
        self.assertNotIn(bpe.token_to_id("[UNK]"),encoded.ids)
        self.assertEqual(bpe.decode(encoded.ids,skip_special_tokens=False),held_out)
        self.assertEqual(bpe.to_str(),before)
        self.assertNotIn(held_out,bpe.get_vocab())


if __name__=="__main__":
    unittest.main()
