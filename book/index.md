# HCMUS Data Preprocessing

An individual **Data Mining and Applications** project at the University of
Science, VNU-HCM (HCMUS).

This book documents reproducible data preprocessing decisions and their evaluation.
Stage 01 EDA is completed. Stage 02 numerical missing-value imputation is completed:
69 numerical features, seven configurations, and raw/per-feature/normalized RMSE
comparisons. Later preprocessing stages are pending; text preprocessing remains
future work. These completed numerical experiments do not establish that the
entire dataset is fully preprocessed or that all features are eligible for prediction.

## Dataset and project scope

The tabular section uses [WiDS Datathon 2024 — Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data),
a healthcare classification dataset concerning diagnosis delays. The binary
target is `DiagPeriodL90D`; `patient_id` identifies records. Use the official
competition dictionary and rules when interpreting the variables.

- [Tabular preprocessing](tabular/index.md): dataset access, validation and current progress.
- [Stage 01 — Exploratory Data Analysis](tabular/01_eda.ipynb): executed dataset audit,
  distributions, relationships, missingness and temporal-eligibility limitations.
- [Stage 02 — Numerical Missing Value Imputation](tabular/02_preprocessing.ipynb):
  the original six-feature benchmark and the joint 69-feature comparison of Mean,
  Median, Mode, kNN k=3/5/10 and MICE with three posterior completions.
- [Text preprocessing](text/index.md): reserved for a future, separately defined task.

## Reproduce the workspace

Clone the [project repository](https://github.com/hungstupid/data-mining-preprocessing)
and use its root directory. The verified interpreter and package versions are
recorded in `.python-version`, `requirements.txt`, and `requirements-lock.txt`.
For a fresh checkout with Python 3.13 installed:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
```

Node.js 24.x and npm are also required for the book. Preview with
`jupyter book start` or produce static HTML with `jupyter book build --html`.
These pages render independently of the raw dataset and Kaggle credentials.

For data validation, first authenticate with Kaggle and accept any required
competition rules, then download and extract the official files into `data/raw/`:

```bash
kaggle competitions download widsdatathon2024-challenge1 -p data/raw
python -m zipfile -e data/raw/widsdatathon2024-challenge1.zip data/raw
python src/validate_dataset.py
```

Raw and processed datasets, credentials, environments, and generated HTML stay
outside version control. The repository README contains complete environment,
kernel, validation, and GitHub Pages instructions.
