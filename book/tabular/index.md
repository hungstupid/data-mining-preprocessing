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

## 03 — Outlier Detection & Treatment

[Sections 16–19 of the preprocessing notebook](02_preprocessing.ipynb) add the
69-feature training audit, IQR fences (1.5 × IQR) and strict absolute Z-score >3
with population SD (ddof 0). Both methods use originally observed inner-training
values only; NaNs are never flagged. Feature-level masks, same-index ANY-feature
row flags and trigger counts are retained in memory for later comparisons.

A separate shared complete training matrix reuses the train-fitted kNN10 and
conditioning from Stage 02. It preserves observed cells and records which cells
are estimated; univariate thresholds do not use those imputations. No patients
are removed or exported, and neither detector is selected as a final treatment.
Repeated ZIP context, overlapping shares, skewness and unknown outlier labels
limit interpretation of the flag rates.

[Sections 20–27](02_preprocessing.ipynb) complete the stage with Isolation Forest
contamination=.01/.05/.10, LOF neighbors=10/20/50 with contamination=auto, and one
DBSCAN calibrated by a prespecified training-only k-distance heuristic. All seven
new configurations use the same complete 69-feature conditioned training matrix.

The executed nine-configuration comparison includes all aligned row flags, the full
Jaccard matrix/counts, nine independent hypothetical retained subsets and 621
observed-value KS comparisons. KS D describes distribution changes; nominal p-values
are not calibrated because retained records are nested in the original sample,
with ZIP repetition and ties. The conservative treatment recommendation keeps all
original observations and retains anomaly flags for investigation. No final cleaned
patient dataset is exported or predictive improvement claimed.

Outlier Detection & Treatment is completed for this retrospective training scope;
Sections 16–19 preserve the earlier Part 1 handoff. Final predictive preprocessing
still requires temporal eligibility and fold-local downstream evaluation.

## 04 — Controlled Scaling Comparison

[Sections 28–36 of the preprocessing notebook](02_preprocessing.ipynb) compare
MinMaxScaler [0,1], StandardScaler (population SD), RobustScaler (median/IQR), and
QuantileTransformer with uniform and normal outputs. Both quantile outputs are
an extension; the official rubric permits either. All five fit the same original-unit
8173×69 completed training matrix, retaining every observation and the original
imputation provenance. Validation/reserve and target/identifiers are not used for fitting.

The executed comparison includes all 414 feature/representation summaries (original
reference plus five transformations), fitted parameter audits and three violin figures
covering six declared features with observed/imputed groups separated. A focused
median-centered Levene diagnostic compares observed BMI across fixed training-age
strata. Its p-values are nominal under ZIP dependence and fitted-data limitations;
affine invariance is checked. No raw-versus-own-transformation variance test or
p-value-based scaling winner is reported.

Stage 04 Scaling is completed for this training-only descriptive comparison. Constant,
tied and unseen-value behavior, mechanical properties and reproducibility are checked.
Quantile target shapes are approximate, and imputation/contextual repetition affect
their interpretation. Later model-dependent choices require fold-local fitting,
temporal eligibility and held-out evaluation. Saved outputs render without CSVs in CI.

## Planned work

Stage 05 Categorical Encoding, feature selection,
resampling and classifier evaluation remain future work. The completed Stage 04
comparison is separate from internal scaling used by imputation/anomaly methods.
Temporal eligibility and source-period gaps must still be resolved for prediction.
