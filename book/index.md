# HCMUS Data Preprocessing

An individual **Data Mining and Applications** project at the University of
Science, VNU-HCM (HCMUS).

This book documents reproducible data preprocessing decisions and their evaluation.
Stage 01 EDA is completed. Stage 02 numerical missing-value imputation is completed:
69 numerical features, seven configurations, and raw/per-feature/normalized RMSE
comparisons. Stage 03 Outlier Detection & Treatment is completed with nine detector
configurations, Jaccard agreement and hypothetical-removal KS analysis. The treatment
recommendation preserves original observations with review flags. Stage 04 Scaling is
completed: five configurations on the same 69-feature training matrix, full numerical
summaries, provenance-aware violins and a focused variance diagnostic. Stage 05 Categorical
Encoding is completed for a retrospective five-field comparison, including ZIP-disjoint
OOF Target Encoding, high-cardinality state bits and scoped VIF/rank diagnostics. Ordinal
codes are illustrative because no semantic ordering is verified. Stage 06 Feature Selection
and Dimensionality Reduction is completed with 22 configurations, fold-local preprocessing,
group-aware five-fold F1 evaluation and separate PCA/t-SNE displays. Stage 07 compares
no resampling, SMOTE, ADASYN and Random Under-sampling on the same 69 numerical fields
with fold-local learning and one locked post-EDA internal reserved assessment. External
clinical validation and text preprocessing remain future work. These completed numerical experiments do not establish that the
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
- [Stage 03 — Outlier Detection & Treatment](tabular/02_preprocessing.ipynb):
  Sections 16–27 compare all nine configurations on training data and justify a
  conservative retention policy. KS D is descriptive; nominal p-values have
  dependent-sample limitations. Controlled predictive assessment is in Stages 06–07;
  clinical validation remains future work.
- [Stage 04 — Scaling](tabular/02_preprocessing.ipynb): Sections 28–36 compare Min-Max,
  Standard, Robust and both uniform/normal quantile transforms. Mechanical scaling
  checks and training distributions do not select a predictive winner.
- [Stage 05 — Categorical Encoding](tabular/02_preprocessing.ipynb): Sections 37–46
  audit categorical eligibility and compare five representations, missing/unseen rules,
  dimensionality/storage, group-aware cross-fitting and multicollinearity. Prospective
  feature eligibility and a predictive encoding winner remain unverified.
- [Stage 06 — Feature Selection & Dimensionality Reduction](tabular/02_preprocessing.ipynb):
  Sections 47–56 compare statistical, model-based and wrapper selection plus PCA using
  the same ZIP-grouped folds and LR. Descriptive embeddings and development selection
  do not establish prospective performance or independent final generalization.
- [Stage 07 — Class Imbalance & Controlled Evaluation](tabular/02_preprocessing.ipynb):
  Sections 57–64 retain original held-fold prevalence, report actual sampling counts,
  Precision/Recall/F1-macro/ROC-AUC, uncertainty, confusion matrices and one locked
  internal reserved score. Synthetic realism, clinical label polarity and prospective
  validity remain qualified.
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
