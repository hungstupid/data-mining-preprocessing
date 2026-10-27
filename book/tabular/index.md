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
disease-code meanings, clinical timing anchors, units, and feature timestamps remain
partly unverified. The focused review in Section 57 of the preprocessing notebook resolves
target polarity without changing the historical EDA or its remaining source limitations.
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

## 05 — Categorical Encoding & Multicollinearity

[Sections 37–46](02_preprocessing.ipynb) audit all 12 categorical/code/text fields
plus protected ID/target, and compare One-Hot, illustrative Ordinal, ZIP-disjoint
OOF Target, Binary hybrid and Frequency Encoding on the same five nominal fields:
race, payer, state, Region and Division. State qualifies for >20-category bit encoding;
low-cardinality fields retain reference One-Hot in the hybrid. ZIP remains only a
split key; clinical codes/text, post-event treatment and constant gender are excluded.

The source dictionary records some attributes on the metastatic date. Inclusion here
is for a retrospective supplied-table demonstration, not earlier-baseline predictor
approval. No genuine ordinal ordering is verified. Target mappings use five
label-independent GroupKFold ZIP splits and fixed smoothing, with separate OOF training
values and full-inner-training maps for validation/future transformation. No validation
or reserved labels enter fitting. Later model CV must reconstruct supervised encodings
inside its own training folds.

The executed comparison reports dimensions, sparse/dense payload, unknown/missing
behavior, full-design rank and VIF. Per-column VIF uses every encoded column plus the
same six original numerical illustrations; a separate full 69-numerical+encoded rank
audit exposes wider conditioning issues. An intercept/reference convention, constant
and numerical perfect-dependence handling, and scope limits are explicit. Lower VIF
or fewer columns does not establish better encoding. Original data remain unchanged;
saved aggregate results publish without CSV access in CI.

## 06 — Feature Selection, Dimensionality Reduction & Grouped F1

[Sections 47–56](02_preprocessing.ipynb) compare no selection, numerical ANOVA,
categorical-indicator Chi-square, MI, RF/GB importance, RFE and PCA with 22 fixed
configurations and 110 held-fold LR evaluations. The raw retrospective pool retains
69 numerical/five nominal fields and every inner-training patient. Five shared
StratifiedGroupKFold splits separate ZIPs and retain both classes. External validation
and reserve are not scored or used for Stage 06 model selection; Stage 07 below later
scores only one locked numerical pipeline on the reserve.

Fresh preprocessing is fitted within each fitting fold: observed numerical scaling,
kNN10 completion, categorical missing/One-Hot rules, final scaling and ranking/selection.
Stage 04 completed matrices and Stage 05 OOF Target Encoding are not reused for CV.
ANOVA keeps selected numerical features plus all categorical columns; Chi-square keeps
selected nonnegative indicators plus all numerical features. MI/RF/GB/RFE use whole-matrix
top-k. The actual counts, complete scores/p-values, selected identities, original-field
importances and selection stability are saved alongside all five F1-macro values,
secondary metrics, class recalls and computation times.

Fold-local PCA thresholds are evaluated with the same LR. Separate training-only
display fits report the spectrum, 90/95/99% component counts, scree and 2D PCA/t-SNE
plots; no label enters embedding fitting. A Stage 06 mixed-feature candidate chosen using these CV results
has no independent final performance estimate; Stage 07's separate numerical scope
is assessed below. Temporal availability, post-metastatic
BMI, imputation uncertainty, correlated ZIP context and fixed-classifier/threshold
limitations remain. UMAP is optional and omitted; Stage 06 itself does not rebalance.
The Stage 07 extension follows; Text remains future work.

## 07 — Class Imbalance & Controlled Evaluation

[Sections 57–64](02_preprocessing.ipynb) compare no resampling, SMOTE, ADASYN and Random
Under-sampling on a common 69-numerical-field space. Five raw-data fitting folds learn
fresh StandardScaler → kNN10 → completed StandardScaler; sampling and the fixed Stage 06
LR follow inside training only. Fold-local preprocessing is shared within, never across,
the four treatments. Nominal fields/codes are excluded to avoid interpolating categorical
representations. ZIP only defines groups. The same Stage 06 folds and original row
identities are reused; the numerical-only baseline is recomputed for fair comparison.

Both labels occur in every fold. The [MathWorks WiDS walkthrough](https://blogs.mathworks.com/student-lounge/2024/01/01/predicting-timely-diagnosis-of-metastatic-breast-cancer-for-the-wids-datathon-2024/) confirms
1/True as the 90-day diagnosis group and 0/False as its complement. Thus the positive
class remains 1 and the minority remains 0; metrics and label values are unchanged.
Precise timing anchors and prospective feature eligibility are separate unresolved issues.
All original/resampled/held class counts, five-fold metrics and confusion matrices,
mean/sample SD, runtime and distribution changes are saved. ADASYN rounding is measured,
not replaced with an assumed exact ratio. Synthesized fractional ages/context mixtures,
prior/calibration changes, geographic dependence and RUS information loss are discussed.

The fixed mean-F1 rule selects **Random undersampling**: CV F1-macro **0.509298 ±
0.016373**, versus no-resampling **0.426654**.
This supports a candidate in the stated benchmark; weak AUC and small differences among
resamplers prevent a general superiority or clinical utility claim. Fold SD is not an
independent confidence interval. A configuration hash precedes a single selected-method
assessment on the original 2,652 reserved rows: F1-macro **0.500629**,
ROC-AUC **0.529792**. The 2,081 other-validation rows remain separate.
Whole-file EDA was already conducted; this is a post-EDA internal estimate, not an untouched
external cohort. No reserve-driven retuning or multi-method reserve comparison is performed.

The 148-cell notebook retains 72 sequentially executed code cells and saved aggregate outputs.
Independent tests check training-only inputs, sampler skipping on held prediction, actual
class counts/schema/finiteness, deterministic samplers, analytic metrics and raw-input
complete Pipeline.fit equivalence. Original data/EDA and all previous results remain preserved.
The existing CSV-free saved-output publication mechanism applies.

## Planned work

External/prospective validation, explicit prediction-time eligibility, precise clinical
timing anchors and application-specific calibration/cost decisions remain unresolved.
Natural missingness assumptions and synthetic realism are not established by successful
execution. No overall 100% scientific-completion claim is made. Text remains a separate
future task; mandatory part (b) of the assignment is not satisfied by its placeholder.
