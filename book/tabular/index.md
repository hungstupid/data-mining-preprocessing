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

## 02 — Controlled Missing Value Imputation

[Read the executed imputation benchmark](02_preprocessing.ipynb): Mean, Median,
numerical Mode, kNN k=3/5/10, and three posterior MICE completions. This is a
retrospective reconstruction experiment. Sections 1–9 preserve the original six-variable
benchmark, including post-metastatic BMI. Sections 10–15 audit all 69 numerical candidates
and add a separate joint benchmark using the same seven configurations. Broader coverage
is a scientific extension, not an explicit all-69 requirement in the official rubric.
Reconstruction eligibility does not establish prospective feature eligibility.

Two deterministic ZIP-disjoint splits reserve an outer assessment partition.
Imputers and internal distance conditioning fit only inner training rows. All
seven configurations reconstruct the same additional 10% mask of originally
observed inner-validation values. Raw and per-feature RMSE are reported; the
predeclared selection criterion is equal-feature RMSE normalized by training SD.
MICE reports mean draw-level scores and their variation, without inferential pooling.
Each scope has its own common mask; aggregate scores from different scopes are not pooled.
The expanded chapter reports computation/conditioning checks, all per-feature results,
bounded-share plausibility flags and a separate categorical missingness inventory.
Natural missingness is not assumed MCAR, and the outer reserve is not scored.

Saved aggregate outputs render in CI without the CSV; recomputation requires the
local data and `.venv` kernel. See README for the execution command and the audit
for measured results and verification.

## Planned work

Outlier treatment, full scaling and encoding comparisons, feature selection,
resampling and classifier evaluation remain future work. Internal train-fitted
scaling in the imputation benchmark does not complete the separate scaling rubric.
Temporal eligibility and source-period gaps must still be resolved for prediction.
