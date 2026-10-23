# Tabular preprocessing

## Input

Source: [WiDS Datathon 2024 — Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data).
Use `DiagPeriodL90D` as the target and `patient_id` as the record identifier.
Keep official CSV files unchanged under the local `data/raw/` directory.

## Structural validation

Run `python src/validate_dataset.py` from the repository root after downloading
and extracting the official data. The validator locates the training CSV by its
schema and reports dimensions, memory, missingness, type counts, class balance,
duplicates, low-variance columns, categorical cardinality, and possible sentinels.
It performs no cleaning or transformations.

Actual dataset results are pending local data access. Course structural
compliance also requires the thresholds from the course rubric; the validator
accepts these as explicit command-line options documented in the README.

## Planned work

Preprocessing experiments and evaluations will be added after dataset validation
and confirmation of the course requirements. No imputation, outlier treatment,
scaling, feature selection, resampling, or model training has been performed.
