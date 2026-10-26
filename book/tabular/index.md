# Tabular preprocessing

## Input

Source: [WiDS Datathon 2024 — Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data).
Use `DiagPeriodL90D` as the target and `patient_id` as the record identifier.
Keep official CSV files unchanged under the local `data/raw/` directory.

## Structural validation

Run `python src/validate_dataset.py --csv data/raw/training.csv` from the repository root after downloading
and extracting the official data. The validator locates the training CSV by its
schema and reports dimensions, memory, missingness, type counts, class balance,
duplicates, low-variance columns, categorical cardinality, and possible sentinels.
It performs no cleaning or transformations.

The local training CSV contains 12,906 rows and 83 columns. Course structural
compliance still requires the thresholds from the course rubric; the validator
accepts these as explicit command-line options documented in the README.

## 01 — Exploratory Data Analysis

[Read the executed EDA notebook](01_eda.ipynb) for input checks, semantic feature
roles, temporal leakage review, missingness, distributions, categorical support,
full Pearson/Spearman relationships, normality testing, missingno and Little's MCAR reference.
The findings table links numerical evidence to candidate methods and unresolved
questions. Diagnostic thresholds are documented choices, not treatment rules.

The notebook reads only `data/raw/training.csv` and verifies that both the raw
file and loaded frame remain unchanged. ZIP codes are categorical identifiers;
disease-code meanings, target polarity, units, and feature timestamps remain
partly unverified; the notebook distinguishes dictionary-supported facts from remaining gaps.
Its mechanism-assessment table evaluates MCAR/MAR/MNAR without assigning unsupported labels.

Saved aggregate outputs allow the book to render without private CSV access or
notebook execution in CI. Recomputing EDA requires the local training file and
the `.venv` kernel; see the repository README for the command.

## Planned work

Preprocessing experiments and evaluations remain future work, subject to
confirmation of temporal eligibility and course requirements. No imputation,
outlier treatment, scaling, feature selection, resampling, or model training
has been performed.
