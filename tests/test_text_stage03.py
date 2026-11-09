"""Known-answer statistics and held-out-word traps for Stage 03 notebook functions."""
from collections import Counter, defaultdict
from pathlib import Path
from time import perf_counter
import unittest
import warnings

import nbformat
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, accuracy_score
from sklearn.exceptions import ConvergenceWarning


class Stage03DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        namespace={"Counter":Counter,"defaultdict":defaultdict,"perf_counter":perf_counter,
            "warnings":warnings,"np":np,"pd":pd,"sparse":sparse,
            "CountVectorizer":CountVectorizer,"TfidfVectorizer":TfidfVectorizer,
            "MultinomialNB":MultinomialNB,"LogisticRegression":LogisticRegression,
            "Pipeline":Pipeline,"f1_score":f1_score,"accuracy_score":accuracy_score,
            "ConvergenceWarning":ConvergenceWarning}
        path=Path(__file__).resolve().parents[1]/"book/text/03_stopwords_morphology.ipynb"
        notebook=nbformat.read(path,as_version=4)
        for cell in notebook.cells:
            if "stage03-functions" in cell.metadata.get("tags",[]):
                exec(compile(cell.source,str(path),"exec"),namespace)
        cls.functions=namespace

    def test_whole_token_stopwords_preserve_substrings_and_codes(self):
        result=self.functions["remove_stopwords"](["the","theatre","not","notebook","usb3","3"],{"the","not"})
        self.assertEqual(result,["theatre","notebook","usb3","3"])
        self.assertEqual(self.functions["remove_stopwords"](["the"],{"the"}),[])

    def test_binary_mi_known_four_class_contingencies(self):
        labels=np.repeat(["A","B","C","D"],2)
        matrix=sparse.csr_matrix(np.column_stack([
            [0,0,0,0,1,1,1,1],  # two classes absent, two present: log(2) nats
            [0,1,0,1,0,1,0,1],  # independent within every class
            np.ones(8,dtype=int)]))
        result=self.functions["binary_word_mi"](matrix,labels)
        np.testing.assert_allclose(result,[np.log(2),0,0],atol=1e-14)
        with self.assertRaises(ValueError):
            self.functions["binary_word_mi"](matrix*2,labels)

    def test_collision_compression_and_membership_have_distinct_numerators(self):
        report,groups=self.functions["collision_summary"](
            {"dog":"dog","dogs":"dog","cat":"cat","cats":"cat","usb3":"usb3","7":"7"})
        self.assertEqual((report["V_input_types"],report["U_output_forms"]),(6,4))
        self.assertAlmostEqual(report["compression_pct"],100*2/6)
        self.assertAlmostEqual(report["collision_membership_pct"],100*4/6)
        self.assertEqual(report["types_in_collision_groups"],4)
        self.assertEqual(set(groups["dog"]),{"dog","dogs"})

    def test_real_fold_helper_never_fits_validation_vocabulary_or_idf(self):
        documents=pd.Series([["alpha","shared"],["alpha","trainonly"],
                             ["beta","shared"],["beta","trainonly"],
                             ["validation_only_sentinel"],["validation_only_sentinel","shared"]])
        labels=np.array(["A","A","B","B","A","B"])
        fitting=np.array([0,1,2,3]);validation=np.array([4,5])
        for family in ["NB","LR"]:
            record,pipeline,caught=self.functions["score_fold"](documents,labels,fitting,validation,family=family)
            vectorizer=pipeline.named_steps["vectorizer"]
            self.assertNotIn("validation_only_sentinel",vectorizer.vocabulary_)
            self.assertEqual(set(vectorizer.vocabulary_),{"alpha","beta","shared","trainonly"})
            self.assertEqual(record["vocabulary"],4)
            if family=="LR":
                self.assertAlmostEqual(vectorizer.idf_[vectorizer.vocabulary_["shared"]],np.log(5/3)+1)
            else:
                np.testing.assert_array_equal(pipeline.named_steps["classifier"].class_count_,[2,2])
            self.assertEqual(caught,[])


if __name__=="__main__":
    unittest.main()
