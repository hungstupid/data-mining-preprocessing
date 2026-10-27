"""Shared input/split/conditioning for the independent Part A notebooks.

No estimators fit at import time. Stages 06–07 use load/split/audit only: their
predictive preprocessing is fitted separately inside each CV training fold.
"""
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from sklearn import config_context
from sklearn.impute import KNNImputer
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

ID, TARGET, ZIP = "patient_id", "DiagPeriodL90D", "patient_zip3"
CLINICAL_FIELDS = {"breast_cancer_diagnosis_code", "breast_cancer_diagnosis_desc",
    "metastatic_cancer_diagnosis_code", "metastatic_first_novel_treatment",
    "metastatic_first_novel_treatment_type"}
CATEGORICAL_FEATURES = ["patient_race", "payer_type", "patient_state", "Region", "Division"]
REPRESENTATIVE_FEATURES = ["patient_age", "bmi", "density", "income_household_median",
    "education_college_or_above", "PM25"]
MISSING_TOKEN = "__WIDS_MISSING__"
KNN_MEMORY_MIB = 128
LR_SETTINGS = dict(C=1., l1_ratio=0., solver="lbfgs", fit_intercept=True,
    max_iter=2000, tol=1e-4, class_weight=None, random_state=42)


def numerical_columns(frame):
    forbidden = CLINICAL_FIELDS | {ID, TARGET, ZIP, *CATEGORICAL_FEATURES, "patient_gender"}
    return [column for column in frame.select_dtypes("number") if column not in forbidden]


def load_data(root, expected_shape=(12906, 83)):
    """Read the training file only, preserving ZIP tokens and returning its SHA-256."""
    path = Path(root) / "data/raw/training.csv"
    checksum = hashlib.sha256(path.read_bytes()).hexdigest()
    frame = pd.read_csv(path, dtype={ZIP: "string"})
    if expected_shape is not None and frame.shape != expected_shape:
        raise ValueError(f"Unexpected training shape: {frame.shape}")
    if not (frame.columns.is_unique and frame[ID].notna().all() and frame[ID].is_unique
            and frame[ZIP].notna().all() and frame[TARGET].notna().all()
            and set(frame[TARGET].unique()) == {0, 1}):
        raise ValueError("Training schema/ID/ZIP/target integrity check failed")
    return frame, checksum


def split_data(frame):
    """Reproduce the existing ZIP group reserve (42) and inner validation (43)."""
    development_pos, reserved_pos = next(GroupShuffleSplit(
        n_splits=1, test_size=.20, random_state=42).split(frame, groups=frame[ZIP]))
    development = frame.index[development_pos]
    train_pos, validation_pos = next(GroupShuffleSplit(
        n_splits=1, test_size=.25, random_state=43).split(
            development, groups=frame.loc[development, ZIP]))
    train, validation, reserved = development[train_pos], development[validation_pos], frame.index[reserved_pos]
    for left, right in [(train, validation), (train, reserved), (validation, reserved)]:
        assert left.intersection(right).empty
        assert set(frame.loc[left, ZIP]).isdisjoint(frame.loc[right, ZIP])
    assert len(train) + len(validation) + len(reserved) == len(frame)
    return train, validation, reserved


def prepare_numeric_training(frame, train_index, columns):
    """Original train-only kNN10 preparation for descriptive Stages 03–05.

    Return observed input, its missing mask, fitted observed-value scaler/imputer,
    standardized incomplete input, and completed frames in raw/standardized units.
    Restore every originally observed cell exactly after inverse transformation.
    """
    original = frame.loc[train_index, columns].copy(deep=True)
    missing = original.isna()
    scaler = StandardScaler().fit(original)
    standardized = scaler.transform(original)
    imputer = KNNImputer(n_neighbors=10, weights="uniform", metric="nan_euclidean",
                         keep_empty_features=True).fit(standardized.copy())
    with threadpool_limits(limits=1), config_context(working_memory=KNN_MEMORY_MIB):
        estimates = pd.DataFrame(scaler.inverse_transform(imputer.transform(standardized.copy())),
                                 index=train_index, columns=columns)
    completed = original.where(~missing, estimates)
    completed_z = pd.DataFrame(scaler.transform(completed), index=train_index, columns=columns)
    assert np.isfinite(completed.to_numpy()).all()
    pd.testing.assert_frame_equal(completed.where(~missing), original)
    return original, missing, scaler, imputer, standardized, completed, completed_z


def memory_gib():
    """Existing OS-memory diagnostic used by the unchanged DBSCAN allocation guard."""
    total = available = np.nan
    if sys.platform == "darwin":
        total = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True))/1024**3
        vm = subprocess.check_output(["vm_stat"], text=True)
        page_size = int(re.search(r"page size of (\d+) bytes", vm).group(1))
        available = sum(int(re.search(rf"Pages {name}:\s+(\d+)", vm).group(1))
                        for name in ["free", "inactive", "speculative"])*page_size/1024**3
    elif hasattr(os, "sysconf"):
        total = os.sysconf("SC_PHYS_PAGES")*os.sysconf("SC_PAGE_SIZE")/1024**3
        available = os.sysconf("SC_AVPHYS_PAGES")*os.sysconf("SC_PAGE_SIZE")/1024**3
    return total, available


def numeric_audit(df, train_index, validation_index):
    """Existing 69-feature eligibility rules and source/timing notes, without fitting."""
    numerical_candidates = numerical_columns(df)
    forbidden = CLINICAL_FIELDS | {ID, TARGET, ZIP, *CATEGORICAL_FEATURES, "patient_gender"}
    expanded_train_all = df.loc[train_index, numerical_candidates].copy(deep=True)
    expanded_reference_all = df.loc[validation_index, numerical_candidates].copy(deep=True)
    assert set(numerical_candidates).isdisjoint(forbidden)

    # Dictionary-confirmed population/household shares; rent_burden is a ratio, not a <=100 share.
    other_context = {"population", "density", "age_median", "family_size",
                     "income_household_median", "income_individual_median", "housing_units",
                     "home_value", "rent_median", "commute_time", "rent_burden", "poverty"}
    air_features = {"Ozone", "PM25", "N02"}
    bounded_share_features = set(numerical_candidates) - other_context - air_features - {"patient_age", "bmi"}
    eligibility_rows = []
    for column in numerical_candidates:
        train_column = expanded_train_all[column]
        observed_values = df[column].dropna().to_numpy()
        support = (train_column.count() >= 2 and train_column.nunique() >= 2
                   and np.isfinite(train_column.std(ddof=0)) and train_column.std(ddof=0) > 0
                   and expanded_reference_all[column].count() >= 10
                   and np.isfinite(observed_values).all())
        if column == "patient_age":
            role, reason = "Individual age", "Index/baseline alignment unverified"
        elif column == "bmi":
            role, reason = "Individual BMI", "Post-metastatic; retrospective only"
        elif column == "poverty":
            role, reason = "Area numerical; meaning UNVERIFIED", "Conflicting dictionary; no poverty-rate/bound assumption"
        elif column in air_features:
            role, reason = "Annual ZIP3 air context", "Units/exposure year and baseline availability unverified"
        elif column in bounded_share_features:
            role, reason = "Area share [0,100]", "Context/reference period unresolved; unbounded MICE may violate support"
        else:
            role, reason = "Area numerical summary", "Context/reference period unresolved; units vary"
        if column == "rent_burden":
            reason += "; rent/income percentage can exceed 100; no upper bound imposed"
        if column == "widowed":
            reason += "; exact dictionary wording inconsistent"
        eligibility_rows.append({"Feature": column, "Semantic role": role,
            "Missing %": df[column].isna().mean()*100, "Observed N": int(df[column].count()),
            "Unique N": int(df[column].nunique()),
            "Train availability": f"{train_column.count()} observed; {train_column.nunique()} unique",
            "Eligibility": "Included: retrospective" if support else "Excluded: support/finite/SD rule",
            "Reason": reason})
    numerical_eligibility = pd.DataFrame(eligibility_rows).set_index("Feature")
    EXPANDED_FEATURES = numerical_eligibility.index[numerical_eligibility.Eligibility.eq("Included: retrospective")].tolist()
    assert len(numerical_eligibility) == 69 and len(EXPANDED_FEATURES) == 69  # Actual dataset: no exclusions needed.
    return numerical_eligibility, bounded_share_features


def categorical_audit(df, train_index):
    """Existing categorical-role gate; shared only for provenance in Stage 06."""
    numerical_candidates = numerical_columns(df)
    clinical_fields = CLINICAL_FIELDS
    ENCODING_FEATURES = CATEGORICAL_FEATURES
    encoding_audit_fields = [c for c in df if c not in numerical_candidates]
    encoding_meanings = {"patient_race": "Recorded race; nominal", "payer_type": "Payer category; nominal",
        "patient_state": "Coarse geographic state; nominal", "patient_zip3": "ZIP3 geographic group key",
        "patient_gender": "Recorded gender; nominal", "Region": "Regional location summary; nominal",
        "Division": "Geographic division; nominal", "breast_cancer_diagnosis_code": "ICD-9/10 code; numeric-looking tokens are nominal",
        "breast_cancer_diagnosis_desc": "Diagnosis code description; text, not an ordinal measurement",
        "metastatic_cancer_diagnosis_code": "ICD-10 code; nominal",
        "metastatic_first_novel_treatment": "First novel treatment after metastatic diagnosis",
        "metastatic_first_novel_treatment_type": "Type of first novel treatment after metastatic diagnosis",
        ID: "Protected unique patient identifier", TARGET: "Protected binary outcome"}
    encoding_audit_rows = []
    for feature in encoding_audit_fields:
        values = df.loc[train_index, feature]
        counts = values.value_counts(dropna=True)
        rare = counts[counts/len(values) < .01]
        if feature in [ID, TARGET, ZIP]:
            eligibility, reason = "EXCLUDED", "Protected ID/outcome/geographic group key"
        elif feature in clinical_fields:
            eligibility, reason = "EXCLUDED", "Clinical/temporal gate unresolved; treatment is post-event; description belongs to text/clinical scope"
        elif values.nunique() <= 1:
            eligibility, reason = "EXCLUDED", "Constant nonmissing training category; no representation information"
        else:
            eligibility, reason = "Included: retrospective only", "Common nominal comparison; prospective availability NOT VERIFIED"
        timing = ("Recorded on metastatic date; earlier-baseline availability unverified" if feature in ["payer_type", "patient_state", "patient_gender", ZIP]
                  else "Post-metastatic" if "novel_treatment" in feature else "Recording/reference time unverified")
        encoding_audit_rows.append({"Feature": feature, "Storage dtype": str(values.dtype),
            "Semantic meaning": encoding_meanings[feature], "Observed categories": int(values.nunique()),
            "Missing N": int(values.isna().sum()), "Missing %": values.isna().mean()*100,
            "Rare observed categories <1%": len(rare), "Rows in rare categories %": rare.sum()/len(values)*100,
            "Cardinality >20": values.nunique() > 20, "Genuine ordinal meaning": "No verified ordering" if feature != TARGET else "Outcome, not predictor",
            "Temporal availability": timing, "Baseline predictor approved": False, "Encoding eligibility": eligibility, "Reason": reason})
    encoding_audit = pd.DataFrame(encoding_audit_rows).set_index("Feature")
    return encoding_audit
