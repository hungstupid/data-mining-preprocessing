# Part A — Tabular Preprocessing

## Dataset and interpretation

Use the official [WiDS 2024 Challenge #1 training data](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data):
12,906 rows, 83 columns, 69 numerical candidates and 12 nominal/code/text fields.
Target `DiagPeriodL90D`: 1 is the 90-day diagnosis group, 0 its complement;
[source confirmation](https://blogs.mathworks.com/student-lounge/2024/01/01/predicting-timely-diagnosis-of-metastatic-breast-cancer-for-the-wids-datathon-2024/).
ID is never a predictor. ZIP3 is preserved as a string and used only for geographic grouping.
BMI/treatment are post-metastatic; exact clinical anchors, source periods/units and prospective
eligibility remain unresolved. Literal tokens such as ZIP `999` are not recoded without evidence.

## Fixed protocol

| Partition | Rows | ZIPs | Label 0 | Label 1 | Role |
|---|---:|---:|---:|---:|---|
| Inner training | 8,173 | 443 | 3,064 | 5,109 | Fit descriptive methods; grouped model CV |
| Imputation validation | 2,081 | 148 | 778 | 1,303 | Fixed observed-cell masking/reconstruction; not pooled into final fitting |
| Reserved assessment | 2,652 | 148 | 1,004 | 1,648 | One locked Stage 07 policy at original prevalence |

GroupShuffleSplit seeds 42/43 fix these partitions. Stages 06–07 use identical five
StratifiedGroupKFold splits (shuffle=True, seed=42) within inner training. The notebooks
recreate the same fixed recipe independently.
No seed search, cross-fold learned state or resampling of held/reserved rows occurs.
Whole-file EDA already informed the project, so the final reserve is a **post-EDA internal
assessment**, not an untouched external cohort. Reexecution repeats the same locked policy;
it does not authorize further reserved-data tuning.

## Read and run

| Stage | Scope and conclusion |
|---|---|
| [01 — EDA](01_eda.ipynb) | Required 69 normality results, full Pearson/Spearman, missingno and limited Little reference |
| [02 — Imputation](02_preprocessing.ipynb) | Seven configurations; original six-feature support plus primary joint 69-feature reconstruction |
| [03 — Outliers](03_outliers.ipynb) | Nine detector settings; agreement/KS/composition support preserving all original rows |
| [04 — Scaling](04_scaling.ipynb) | Five fixed transformations; mechanical shape/variance evidence, no global winner |
| [05 — Encoding](05_encoding.ipynb) | Five methods; genuine state bits and group-OOF Target; scoped VIF and full-design rank |
| [06 — Feature selection](06_feature_selection.ipynb) | All 110 evaluations retained; no reduction exceeds no-selection mean F1 |
| [07 — Class imbalance](07_class_imbalance.ipynb) | Four same-scope treatments; RUS wins fixed F1 criterion, while AUC/Brier remain weak |

Run each notebook with a **fresh `hcmus-wids` kernel**. Stage 01 and Stage 02 include their own
input preparation. Later notebooks use the small shared `src/tabular_data.py` module to read
raw data, reconstruct splits/semantic metadata and, for descriptive Stages 03–05 only,
reproduce the same train-only kNN10 preparation. They never execute a previous notebook or
read its saved outputs. Stages 06–07 fit learned preprocessing from raw fitting folds only.
No private processed-data cache/checkpoint is needed.

The six report sections make the main argument visible. Expand code, diagnostics and full
per-feature tables for details; use the [appendix](appendix.md) for original-scope evidence
and the separate test command. Scores/p-values remain in Python variables and real saved outputs.

## Reproduction and publication

The repository README gives exact environment/data/test/build commands. Run the notebooks in
01→07 order for a complete review, or open any chapter independently. The notebooks retain
raw-file integrity and essential data/leakage boundaries; separate tests cover analytic formulas,
observed-value preservation and synthetic held-data traps. No patient-level processed table
is exported or committed. The optional Stage 01 download never replaces an
existing file and requires your own authorized Kaggle access.

Jupyter Book builds saved aggregate outputs **without `--execute`**; private CSVs are required
for local Run All, not for static rendering or GitHub Actions. Keep the outputs when publishing.
The [current rubric audit](../../RUBRIC_AUDIT.md) distinguishes implementation evidence from
statistical validity: natural missingness, clinical timing, independent external performance,
Ordinal interpretation and the rubric's conditional UMAP wording retain explicit limits.
Part B is outside this work.
