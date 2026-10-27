# HCMUS Data Preprocessing

**Nguyễn Đức Hưng — 24127174** · Data Mining and Applications, HCMUS.

This book presents reproducible preprocessing decisions for
[WiDS Datathon 2024 Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data).
Read **Part A** in seven stages; each executable chapter separates its objective, methodology,
implementation, results, discussion and conclusion. Code and numbers come from the same
notebook sources; full scientific tables and supporting results remain expandable.
Analytic and leakage fixtures are maintained separately in `tests/`.

| Part A chapter | Question |
|---|---|
| [01 — EDA](tabular/01_eda.ipynb) | What are the distributions, missingness and semantic/temporal limits? |
| [02 — Imputation](tabular/02_preprocessing.ipynb) | Which method reconstructs the same hidden observed cells? |
| [03 — Outliers](tabular/03_outliers.ipynb) | Which records are flagged, and what would removal change? |
| [04 — Scaling](tabular/04_scaling.ipynb) | How do scale, shape and observed/imputed provenance change? |
| [05 — Encoding](tabular/05_encoding.ipynb) | What do five representations retain, lose or make collinear? |
| [06 — Feature selection](tabular/06_feature_selection.ipynb) | Does reduction improve grouped five-fold F1? |
| [07 — Class imbalance](tabular/07_class_imbalance.ipynb) | Does training-only rebalancing improve original-prevalence assessment? |

Start with the [Part A protocol and reproduction guide](tabular/index.md).
The [appendix](tabular/appendix.md) provides supporting benchmarks and separate test instructions.
Each notebook runs from a fresh project kernel; saved outputs allow CSV-free static builds.
The repository README contains environment, data-access, test and publication commands.

These are retrospective supplied-table comparisons. Full-file EDA exposure, geographic
dependence, post-metastatic BMI and unresolved clinical timing limit prospective claims.
F1 improvement alone does not establish stronger ranking, calibration or clinical utility.

[Part B — Text placeholder](text/index.md) remains unchanged and is not a completed second
modality. The official assignment requires Part B in addition to Part A; no overall grade
or whole-project completion is asserted here.
