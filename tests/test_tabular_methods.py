"""Analytic and leakage fixtures moved out of Part A; no private data or notebook execution."""
import ast
from collections import Counter
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import warnings

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, levene
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import RFE, chi2, f_classif, mutual_info_classif
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (brier_score_loss, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import ADASYN, SMOTE
from imblearn.pipeline import Pipeline as ImbalancedPipeline
from imblearn.under_sampling import RandomUnderSampler
from threadpoolctl import threadpool_limits

from src.tabular_data import LR_SETTINGS, MISSING_TOKEN

ROOT = Path(__file__).resolve().parents[1]


def notebook_functions(filename, names, **variables):
    """Load only named function definitions, testing the real code without running its cells."""
    notebook = json.loads((ROOT / "book/tabular" / filename).read_text())
    definitions = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            definitions.extend(node for node in ast.parse("".join(cell["source"])).body
                               if isinstance(node, ast.FunctionDef) and node.name in names)
    namespace = {"np": np, "pd": pd, **variables}
    exec(compile(ast.Module(body=definitions, type_ignores=[]), filename, "exec"), namespace)
    return {name: namespace[name] for name in names}


class MaskAndScoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = notebook_functions("02_preprocessing.ipynb", ["make_mcar_mask", "score_masked"])

    def test_mask_uses_observed_cells_fixed_counts_and_no_values(self):
        frame = pd.DataFrame({"a": np.arange(30.), "b": 3*np.arange(30.)+1})
        frame.loc[::11, "a"] = np.nan
        frame.loc[::13, "b"] = np.nan
        original = frame.copy(deep=True)
        mask = self.methods["make_mcar_mask"](frame, .10, 71)
        pd.testing.assert_frame_equal(mask, self.methods["make_mcar_mask"](frame+1000, .10, 71))
        self.assertFalse((mask & frame.isna()).to_numpy().any())
        np.testing.assert_array_equal(mask.sum(), np.floor(frame.count()*.10))
        pd.testing.assert_frame_equal(frame, original)

    def test_raw_and_macro_normalized_errors_use_only_masked_truth(self):
        truth = pd.DataFrame({"a": [1., 2., np.nan], "b": [3., 4., 5.]})
        mask = pd.DataFrame({"a": [True, False, False], "b": [False, True, False]})
        completed = truth+10000  # Large unscored errors must not enter either loss.
        completed.loc[0, "a"], completed.loc[1, "b"] = 3., 8.
        result = self.methods["score_masked"](truth, completed, mask, pd.Series({"a": 1., "b": 2.}))
        self.assertAlmostEqual(result["RMSE"], np.sqrt(10))
        self.assertEqual(result["Normalized RMSE"], 2.)
        self.assertEqual(result["Reconstructed N"], 2)

    def test_scoring_rejects_missing_truth_nonfinite_predictions_and_misalignment(self):
        truth = pd.DataFrame({"a": [1., np.nan], "b": [2., 3.]})
        mask = pd.DataFrame({"a": [True, False], "b": [False, True]})
        sd = pd.Series({"a": 1., "b": 2.})
        invalid_prediction = truth.copy()
        invalid_prediction.loc[0, "a"] = np.nan
        invalid_mask = mask.copy()
        invalid_mask.loc[1, "a"] = True
        for completed, selected, scale in [(invalid_prediction, mask, sd),
                                            (truth, invalid_mask, sd),
                                            (truth[["b", "a"]], mask, sd),
                                            (truth, mask, sd*0)]:
            with self.subTest(), self.assertRaises(ValueError):
                self.methods["score_masked"](truth, completed, selected, scale)


class OutlierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = notebook_functions("03_outliers.ipynb",
            ["detect_iqr", "detect_zscore", "jaccard_matrices", "ks_observed_change", "select_dbscan_eps"],
            ks_2samp=ks_2samp)

    def test_strict_iqr_and_zscore_boundaries_preserve_missing_values(self):
        frame = pd.DataFrame({"x": [-2.1, -2., 0., 1., 1., 1.5, 2., 2.5, 3., 3., 4., 6., 6.1, np.nan]})
        before = frame.copy(deep=True)
        parameters, flags = self.methods["detect_iqr"](frame)
        np.testing.assert_allclose(parameters.loc["x", ["Q1", "Q3", "Lower fence", "Upper fence"]].to_numpy(float), [1, 3, -2, 6])
        self.assertEqual(np.flatnonzero(flags.x).tolist(), [0, 12])
        pd.testing.assert_frame_equal(frame, before)
        zframe = pd.DataFrame({"x": [-4., -3., 3., 4.]+[0.]*46+[np.nan]})
        parameters, scores, flags = self.methods["detect_zscore"](zframe)
        self.assertEqual(np.flatnonzero(flags.x).tolist(), [0, 3])
        self.assertTrue(np.isnan(scores.x.iloc[-1]))
        self.assertEqual(parameters.loc["x", "SD (ddof 0)"], 1.)

    def test_unsupported_outlier_columns_are_not_flagged(self):
        frame = pd.DataFrame({"constant": [2.]*5+[np.nan], "zero_iqr": [0.]*5+[1.],
                              "missing": [np.nan]*6, "invalid": [1., 2., np.inf, 3., 4., 5.]})
        parameters, flags = self.methods["detect_iqr"](frame)
        self.assertFalse(parameters.Eligible.any())
        self.assertFalse(flags.to_numpy().any())
        _, _, zflags = self.methods["detect_zscore"](frame)
        self.assertFalse(zflags[["constant", "missing", "invalid"]].to_numpy().any())

    def test_jaccard_empty_sets_ks_missingness_and_fixed_elbow(self):
        flags = pd.DataFrame({"a": [True, True, False, False], "b": [False, True, True, False], "empty": [False]*4})
        jaccard, intersection, union = self.methods["jaccard_matrices"](flags)
        self.assertAlmostEqual(jaccard.loc["a", "b"], 1/3)
        self.assertEqual((intersection.loc["a", "b"], union.loc["a", "b"]), (1, 3))
        self.assertTrue(np.isnan(jaccard.loc["empty", "empty"]))
        change = self.methods["ks_observed_change"](pd.Series([0., 1., 2., 3., np.nan]), pd.Series([0., 1., np.nan]))
        self.assertEqual(change["KS D"], .5)
        self.assertEqual(change["Retained observed N"], 2)
        self.assertEqual(self.methods["select_dbscan_eps"]([0., 1., 2., 10.])[:2], (2., 2))
        self.assertGreater(self.methods["select_dbscan_eps"]([0., 0., 0.])[0], 0)


class ScalingDiagnosticTests(unittest.TestCase):
    def test_known_levene_statistic_and_unavailable_groups(self):
        diagnostic = notebook_functions("04_scaling.ipynb", ["scaling_levene_diagnostic"],
            levene=levene, SCALING_MIN_GROUP_N=20)["scaling_levene_diagnostic"]
        self.assertAlmostEqual(diagnostic([0, 1, 2, 3], [0, 2, 4, 6], min_group_n=2)["Levene W"], 2.4)
        self.assertTrue(np.isnan(diagnostic([1], [2])["Levene W"]))
        self.assertIn("constant group", diagnostic([1]*20, list(range(20)))["Status"])
        self.assertIn("centered deviations", diagnostic([0, 1], [2, 3], min_group_n=2)["Status"])


class EncodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = notebook_functions("05_encoding.ipynb", ["categorical_tokens", "onehot_training_spec",
            "fit_target_mapping", "transform_target", "group_target_oof", "fit_binary_category",
            "transform_binary_category", "encoding_vif"], ENCODING_MISSING=MISSING_TOKEN, ENCODING_ALPHA=10.)

    def test_reference_and_reserved_missing_token(self):
        frame = self.methods["categorical_tokens"](pd.DataFrame({"c": ["a"]*199+["rare", None]}))
        categories, references = self.methods["onehot_training_spec"](frame)
        self.assertEqual(references, ["a"])
        self.assertEqual(set(categories[0]), {"a", "rare", MISSING_TOKEN})
        with self.assertRaises(ValueError):
            self.methods["categorical_tokens"](pd.DataFrame({"c": [MISSING_TOKEN]}))

    def test_binary_codes_are_injective_and_distinguish_unknown_missing(self):
        levels = pd.Series([f"level_{i:02}" for i in range(25)]+[MISSING_TOKEN])
        mapping, width = self.methods["fit_binary_category"](levels)
        bits = self.methods["transform_binary_category"](levels, mapping, width)
        self.assertEqual(width, 5)
        self.assertEqual(len(np.unique(bits, axis=0)), len(levels))
        np.testing.assert_array_equal(bits@2**np.arange(width-1, -1, -1), levels.map(mapping))
        special = self.methods["transform_binary_category"](pd.Series(["unseen", MISSING_TOKEN]), mapping, width)
        self.assertEqual(special[0].sum(), 0)
        self.assertEqual(special[1].sum(), 1)

    def test_target_oof_excludes_own_and_same_zip_labels_including_prior(self):
        frame = pd.DataFrame({"unique": [f"u{i}" for i in range(24)], "zip_level": np.repeat(np.arange(6).astype(str), 4)})
        labels = pd.Series(np.tile([0, 1, 0, 1], 6))
        groups = pd.Series(np.repeat(np.arange(6), 4))
        folds = list(GroupKFold(n_splits=3, shuffle=True, random_state=42).split(frame, groups=groups))
        first, models, _ = self.methods["group_target_oof"](frame, labels, groups, folds)
        for model in models:
            np.testing.assert_allclose(first.loc[model["held_index"]], model["prior"])
        held = folds[0][1]
        changed = labels.copy()
        changed.iloc[held[0]] = 1-changed.iloc[held[0]]  # Also changes the full-sample prior.
        second, _, _ = self.methods["group_target_oof"](frame, changed, groups, folds)
        pd.testing.assert_frame_equal(first.iloc[held], second.iloc[held])
        small = pd.DataFrame({"c": ["a", "a", "b", MISSING_TOKEN]})
        mappings, prior, _ = self.methods["fit_target_mapping"](small, pd.Series([0, 1, 0, 1]))
        np.testing.assert_allclose(mappings["c"].loc[["a", "b", MISSING_TOKEN]], [.5, 5/11, 6/11])
        self.assertEqual(prior, .5)

    def test_vif_intercept_constants_and_perfect_dependence(self):
        frame = pd.DataFrame({"x": [-1., -1., 1., 1.], "z": [-1., 1., -1., 1.]})
        np.testing.assert_allclose(self.methods["encoding_vif"](frame).VIF, 1.)
        result = self.methods["encoding_vif"](frame.assign(twice_x=2*frame.x, constant=7))
        self.assertTrue(np.isinf(result.loc[["x", "twice_x"], "VIF"]).all())
        self.assertTrue(np.isnan(result.loc["constant", "VIF"]))
        np.testing.assert_allclose(self.methods["encoding_vif"](frame*7+13).VIF, 1.)


class FeatureSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = notebook_functions("06_feature_selection.ipynb", ["make_stage06_preprocessor",
            "stage06_take_columns", "stage06_top_positions", "stage06_statistical_scores"],
            ColumnTransformer=ColumnTransformer, Pipeline=Pipeline, StandardScaler=StandardScaler,
            KNNImputer=KNNImputer, SimpleImputer=SimpleImputer, OneHotEncoder=OneHotEncoder,
            ENCODING_MISSING=MISSING_TOKEN, f_classif=f_classif, chi2=chi2,
            mutual_info_classif=mutual_info_classif, STAGE06_SEED=42)

    def test_extreme_held_values_and_unseen_categories_do_not_fit_preprocessing(self):
        frame = pd.DataFrame({"x": [0., 1., 2., np.nan, 4., 5.], "c": ["a", "b", "a", "b", "a", None]})
        original = frame.copy(deep=True)
        prep = self.methods["make_stage06_preprocessor"](["x"], ["c"]).fit(frame)
        with warnings.catch_warnings(record=True):
            values = prep.transform(pd.DataFrame({"x": [1e6, np.nan], "c": ["unseen", "a"]}))
        np.testing.assert_allclose(prep.named_transformers_["numeric"].named_steps["distance_scale"].mean_, [2.4])
        self.assertTrue(np.isfinite(values).all())
        np.testing.assert_array_equal(values[0, 1:], 0)
        pd.testing.assert_frame_equal(frame, original)

    def test_filter_routing_and_stable_top_k(self):
        labels = np.tile([0, 0, 1, 1], 10)
        indicators = np.c_[labels, np.tile([0, 1, 0, 1], 10)]
        numeric = np.c_[labels+np.random.default_rng(42).normal(0, .03, len(labels)), np.arange(len(labels))]
        mixed = np.c_[numeric, indicators]
        scores = self.methods["stage06_statistical_scores"](mixed, StandardScaler().fit_transform(mixed), labels, 2)
        self.assertEqual(len(scores["ANOVA"][0]), 2)
        np.testing.assert_allclose(scores["Chi2"][0], [20, 0])
        self.assertEqual(len(scores["MI"][0]), 4)
        np.testing.assert_array_equal(self.methods["stage06_top_positions"]([1., 5., 5., np.nan], 2), [1, 2])
        with self.assertRaises(ValueError):
            self.methods["stage06_top_positions"]([1., np.nan], 2)

    def test_complete_raw_input_rfe_pipeline_reproduces_fit(self):
        rng = np.random.default_rng(42)
        frame = pd.DataFrame(rng.normal(size=(80, 12)), columns=[f"x{i}" for i in range(12)])
        frame["c"] = np.tile(["a", "b", "c", "a"], 20)
        labels = (frame.x0 > frame.x0.median()).astype(int)
        pipe = Pipeline([("mixed", self.methods["make_stage06_preprocessor"](list(frame.columns[:-1]), ["c"])),
            ("scale", StandardScaler()),
            ("rfe", RFE(LogisticRegression(**LR_SETTINGS), n_features_to_select=10, step=.25)),
            ("classifier", LogisticRegression(**LR_SETTINGS))])
        with threadpool_limits(limits=1):
            first = clone(pipe).fit(frame.iloc[:60], labels.iloc[:60])
            second = clone(pipe).fit(frame.iloc[:60], labels.iloc[:60])
        np.testing.assert_allclose(first.predict_proba(frame.iloc[60:]), second.predict_proba(frame.iloc[60:]))
        np.testing.assert_array_equal(first.named_steps["rfe"].support_, second.named_steps["rfe"].support_)
        self.assertEqual(first.named_steps["classifier"].n_features_in_, 10)


class ClassImbalanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.methods = notebook_functions("07_class_imbalance.ipynb",
            ["make_stage07_preprocessor", "make_stage07_sampler", "stage07_metrics"],
            Pipeline=Pipeline, StandardScaler=StandardScaler, KNNImputer=KNNImputer,
            SMOTE=SMOTE, ADASYN=ADASYN, RandomUnderSampler=RandomUnderSampler, STAGE07_SEED=42,
            confusion_matrix=confusion_matrix, f1_score=f1_score, precision_score=precision_score,
            recall_score=recall_score, roc_auc_score=roc_auc_score, brier_score_loss=brier_score_loss)

    def test_class_specific_and_macro_metrics_match_analytic_confusion(self):
        result = self.methods["stage07_metrics"]([0, 0, 1, 1], [0, 1, 1, 1], [.1, .7, .6, .9])
        self.assertEqual([result[k] for k in ["TN", "FP", "FN", "TP"]], [1, 1, 0, 2])
        np.testing.assert_allclose([result[k] for k in ["Precision class1", "Recall class1", "F1 macro",
            "Precision macro", "Recall macro", "ROC AUC class1", "Brier class1"]], [2/3, 1, 11/15, 5/6, .75, .75, .1675])

    def test_sampler_reproducibility_counts_and_original_provenance(self):
        values = np.random.default_rng(42).normal(size=(80, 3))
        labels = np.r_[np.zeros(30, dtype=int), np.ones(50, dtype=int)]
        original = values.copy()
        with threadpool_limits(limits=1):
            for method in ["SMOTE", "ADASYN", "Random undersampling"]:
                with self.subTest(method=method):
                    sampler = self.methods["make_stage07_sampler"](method)
                    completed, sampled = sampler.fit_resample(values, labels)
                    repeated, repeated_labels = self.methods["make_stage07_sampler"](method).fit_resample(values, labels)
                    np.testing.assert_array_equal(completed, repeated)
                    np.testing.assert_array_equal(sampled, repeated_labels)
                    if method == "Random undersampling":
                        self.assertEqual(Counter(sampled), {0: 30, 1: 30})
                        self.assertEqual(len(np.unique(sampler.sample_indices_)), 60)
                        np.testing.assert_array_equal(completed, original[sampler.sample_indices_])
                    else:
                        np.testing.assert_array_equal(completed[:80], original)
                        self.assertEqual(Counter(sampled)[1], 50)
                        self.assertGreater(Counter(sampled)[0], 30)
        np.testing.assert_array_equal(values, original)

    def test_full_pipelines_sample_only_fit_rows_and_never_predict_rows(self):
        frame = pd.DataFrame(np.random.default_rng(42).normal(size=(80, 3)))
        labels = np.r_[np.zeros(30, dtype=int), np.ones(50, dtype=int)]
        held = pd.DataFrame([[1e6, 2., np.nan], [np.nan, 4., 5.]])
        for method in ["SMOTE", "ADASYN", "Random undersampling"]:
            with self.subTest(method=method), threadpool_limits(limits=1):
                sampler = self.methods["make_stage07_sampler"](method)
                pipe = ImbalancedPipeline(self.methods["make_stage07_preprocessor"]().steps+
                    [("sampler", sampler), ("classifier", LogisticRegression(**LR_SETTINGS))])
                with patch.object(sampler, "fit_resample", wraps=sampler.fit_resample) as spy:
                    pipe.fit(frame, labels)
                    self.assertEqual(spy.call_count, 1)
                    self.assertEqual(len(spy.call_args.args[0]), len(frame))
                mean = pipe.named_steps["distance_scale"].mean_.copy()
                with patch.object(sampler, "fit_resample", side_effect=AssertionError("Held resampling forbidden")):
                    probability = pipe.predict_proba(held)
                self.assertEqual(probability.shape, (len(held), 2))
                np.testing.assert_array_equal(pipe.named_steps["distance_scale"].mean_, mean)


if __name__ == "__main__":
    unittest.main()
