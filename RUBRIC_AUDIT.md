# Rubric audit — EDA and completed preprocessing Stages 02–07: 27 October 2026

Source: https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/

The entire official HTML page was retrieved with HTTP 200 on 25 October 2026 and read through the grading/policy sections. The web-tool rendering failed, so the direct HTTP response was used. The page’s linked raw Markdown returned 404; it is not used as evidence. Requirements below are concise technical paraphrases, with exact numeric parameters preserved. Cell references in the initial audit are **zero-based indices of the original 29-cell notebook**. PASS records observed code/output evidence, not an inference from a clean run. Future work uses NOT VERIFIED; it does not count as completed.

## Current Stage 07 — Advanced Class Imbalance & Controlled Evaluation

Starting/current HEAD: `0f276c25301552222b37b7332290dfe7d9ee50ba` (Stage 04).
**The initial tree already contained five uncommitted Stage 05–06 files**: README,
this audit, homepage, tabular index and preprocessing notebook. These are preserved;
the Stage 06 final verifier passed before edits. No commit/push/PR is made. The
[official assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)
was fetched/read again with HTTP 200; HTML SHA-256 stays
`8d2a4a6e79902495d8f13e50530baf78433059b9620a05a7956298defa391720`.

Sections **57–64**, zero-based cells **132–147**, append 16 cells / eight code cells.
Total: **148 cells / 72 code cells**. All 132 earlier sources/IDs/order and 15 prior
PNG figures remain exact. Earlier statements deferring resampling/reserved scoring
are historical and superseded here. EDA, raw data, dependencies/config/workflow and
all Stage 01–06 experimental designs remain unchanged. No class weighting, tuning,
new dependency, exported patient dataset, Text or image experiment is added.

### Actual class roles, representation and leakage boundary

Full file: **4,846 label 0 / 8,060 label 1**, moderate imbalance; inner training
**3,064 / 5,109** (8,173 rows; 443 ZIPs); other validation **778 / 1,303** (2,081 rows;
148 ZIPs); reserve **1,004 / 1,648** (2,652 rows; 148 ZIPs).
The [official dictionary](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data)
confirms an indicator concerning diagnosis within 90 days, but accessible text does
not explicitly map numeric 0/1 to clinical events or fully establish timing anchors/
boundaries. **Numeric clinical polarity remains UNVERIFIED.** Positive-class metrics
mean numeric 1; minority is 0. No conclusion about delayed/favorable clinical outcomes
is inferred from these labels. BMI remains post-metastatic and prospective eligibility
is not approved by this retrospective experiment.

All four treatments use exactly the same **69 numerical candidates**, no feature
selection, nominal fields/One-Hot, ID, target, ZIP or diagnosis/treatment code/text.
The five Stage 05 nominal fields are deliberately omitted so plain SMOTE/ADASYN
interpolate a common numerical space. This fresh baseline differs from Stage 06's
mixed 74-field scope; cross-stage score changes cannot be attributed to resampling.

Reuse the **exact Stage 06 five StratifiedGroupKFold index arrays**, without drawing
new splits. Each fitting fold learns observed StandardScaler → KNNImputer(k=10,
uniform, keep_empty_features=True) → completed StandardScaler; one preprocessing fit
is shared among four treatments only within that fold. All five learned states are
separate. No global Stage 04/05/06 fitted matrix enters this comparison. Sampling uses
training arrays only; raw-input imbalanced-learn pipelines transform original held
rows and skip sampling. Preprocessing steps are flattened into the outer pipeline:
an initial independent complete Pipeline.fit test caught that nested sklearn Pipeline
intermediates are unsupported. This integration correction changed no fitted algorithm,
split, parameter, representation or metric; the full final Run All passes.

All samplers request `sampling_strategy=1.0`, seed=42. SMOTE k_neighbors=5,
ADASYN n_neighbors=5; RUS replacement=False. Both labels and sufficient neighbors
exist in every fitting fold; no k clipping/fallback occurs. LR parameters are reused
unchanged from Stage 06: C=1, L2/l1_ratio=0, lbfgs, intercept, max_iter=2000,
tol=1e-4, no class weights, seed=42; threshold=.5. No seed/ratio/model/threshold search
is introduced after outcomes. ZIP overlap is zero within every fit/held pair; other
validation and reserve rows never enter CV fitting. Repeated/nearby ZIP context and
retrospective timing remain limitations beyond these mechanical leakage guards.

### Actual counts and validation performance

| Fold | Original fit 0 / 1 | SMOTE after 0 / 1 | ADASYN actual 0 / 1 | RUS after 0 / 1 | Original held 0 / 1 |
|---:|---:|---:|---:|---:|---:|
| 0 | 2452 / 4087 | 4087 / 4087 | 4098 / 4087 | 2452 / 2452 | 612 / 1022 |
| 1 | 2447 / 4085 | 4085 / 4085 | 4092 / 4085 | 2447 / 2447 | 617 / 1024 |
| 2 | 2453 / 4088 | 4088 / 4088 | 4070 / 4088 | 2453 / 2453 | 611 / 1021 |
| 3 | 2451 / 4088 | 4088 / 4088 | 4092 / 4088 | 2451 / 2451 | 613 / 1021 |
| 4 | 2453 / 4088 | 4088 / 4088 | 4080 / 4088 | 2453 / 2453 | 611 / 1021 |

Across five **overlapping fitting sets**, SMOTE creates **8,180**, ADASYN **8,176**
synthetic rows; RUS discards **8,180** majority observations. These sums are fit-level
interventions, not distinct-patient counts. ADASYN's actual label-0 counts can exceed
or fall below the requested label-1 counts because rounded local allocations do not
sum exactly to the requested gap. No exact-balance claim or silent clipping is made.
Every method is evaluated on the same original **8,173 held observations once** across
five folds; no validation/reserve observation is resampled or bootstrapped.

| Method | Precision (1) | Recall (1) | Recall (0) | F1-macro | ROC-AUC (1) |
|---|---:|---:|---:|---:|---:|
| No resampling | 0.628064 ± 0.004525 | 0.956142 ± 0.022758 | 0.055493 ± 0.038001 | 0.426654 ± 0.027742 | 0.533587 ± 0.024787 |
| SMOTE | 0.639866 ± 0.022133 | 0.549589 ± 0.081786 | 0.480334 ± 0.103921 | 0.507408 ± 0.017542 | 0.527965 ± 0.026273 |
| ADASYN | 0.638552 ± 0.019155 | 0.543321 ± 0.058278 | 0.484659 ± 0.080689 | 0.507336 ± 0.015890 | 0.528217 ± 0.024360 |
| Random undersampling | 0.641183 ± 0.015931 | 0.559947 ± 0.103856 | 0.474508 ± 0.110716 | 0.509298 ± 0.016373 | 0.528749 ± 0.026107 |

Mean ± sample fold SD (ddof=1), **not independent-fold confidence intervals**. Full
20-row fold tables include both class precisions/recalls/F1, macro P/R/F1, continuous
class-1 ROC-AUC, Brier, all TN/FP/FN/TP and wall times. Paired F1 differences and four
pooled confusion matrices remain visible; pooled and mean-fold F1 are distinct.
Shared preprocessing times are separate from sampler+LR+prediction timings; total
CV runtime on this run is **15.658s**, a host measurement rather
than a reproducible constant. Brier combines discrimination/calibration and is not
reported as a pure calibration test. Baseline/selected mean Brier is
**0.236120 / 0.251017**;
the selected higher value indicates worse probability error despite better F1.
No significance p-value or training-score gain
is used to claim generalization.

The greatest mean F1 selects **Random undersampling** (0.509298 ± 0.016373);
baseline delta=**+0.082644**. Resamplers improve F1 in all five folds
relative to their same-fold no-resampling baseline, primarily with a large class-recall
trade-off. Class-1 recall falls from 0.956142
to 0.559947, while class-0 recall rises from
0.055493 to 0.474508.
AUC changes from 0.533587 to
0.528749, so the improved threshold-dependent F1 is not evidence
of stronger ranking. RUS has only a small mean advantage over SMOTE/ADASYN relative
to fold variation; no reliable universal ordering is established. **RUS is supported
as the declared candidate in this numerical LR benchmark, not as a clinically validated
or statistically proven superior treatment.** Weak near-chance ranking remains explicit.

### Synthetic validity and distribution changes

All 20 matrices have 69 finite columns in fixed order; oversamplers retain the
original training prefix, RUS uses unique original sample indices without replacement.
The complete **1,380 fold × method × feature diagnostics** report standardized mean
shifts and SD ratios; fold-0 age/BMI/density ECDFs illustrate before/after fitting
distributions without expanding into redundant plots. There are zero synthetic
cells outside fitting-column completed ranges and zero violations of the 52 audited
share bounds. Nevertheless SMOTE produces **7,500** and ADASYN **7,619** fractional
synthetic ages across fitting sets; no rounding is applied. Convex bounds/finiteness
do not enforce valid patient combinations, age discreteness, geographic contexts or
imputation uncertainty. Synthetic rows have no asserted real patient/ZIP identity.

Balancing changes the effective training prior from ~62.5% label 1 to ~50%, alters
the LR intercept and may change calibration/precision at the .5 threshold. Original
held prevalence must remain the evaluation reference. RUS loses original majority
information/geographic mix. Sampling before splitting leaks neighbors/geometry and
can split synthetic relatives across train/held, while changing the apparent held
population; the training-only order here avoids those mechanisms. Geographic grouping
does not itself settle temporal leakage, missingness or clinical realism.

### Locked internal reserved assessment

Before computing reserved predictions/metrics, the fixed rule locks the complete
method/69-feature/preprocessing/LR/seed/threshold configuration; SHA-256:
`d2cbcc55c7142be96f0b32a8b8b172bfe9eef1f2a9f6c6fb07e9d1db5aced897`. A fresh final fitting uses **8,173 inner-training rows only**,
not the 2,081 other-validation rows. Actual final fitting counts after RUS are
**3064 label 0 / 3064 label 1**
(2,045 majority observations discarded). Only this one method is scored on the
original **2,652 reserved rows** at their original prevalence; no other method is
scored there and no choice is revised afterwards.

Reserved confusion, actual rows [0,1] × predicted columns [0,1]:
**[[599, 405], [916, 732]]**.
Precision(1)=**0.643799**, Recall(1)=**0.444175**,
Recall(0)=**0.596614**, F1-macro=**0.500629**,
ROC-AUC(1)=**0.529792**, Brier=**0.261664**.
This is a **post-EDA internal reserved point estimate**. Prior whole-file EDA exposure
precludes a wholly untouched/external claim, and one pipeline's score cannot establish
a reserve improvement versus an unscored baseline. Reexecuting this identical locked
configuration for integration/reproducibility verification is disclosed; it does not
introduce reserve-driven tuning or claim repeated runs as independent tests.

### Verification and publication

- Fresh `.venv` Restart Kernel → Run All executes all **72 code cells**, with outputs
  saved and no notebook exception/stderr. **54 notebook check groups pass** (47 preserved,
  seven new); all **five existing unit tests** pass. Kernel startup's external TCP notice
  remains a tooling notice, not a cell failure. No dependency is installed.
- Analytic fixtures verify confusion counts, both-class/macro P/R/F1, continuous AUC=.75
  and Brier=.1675. Independent sampler fixtures verify deterministic arrays, exact
  SMOTE/RUS counts, actual ADASYN behavior, original prefix/subset provenance, finite
  dimensions, nonmutation and honest failure for infeasible k=5.
- Actual-data checks verify all 20 fold counts/metrics, exact reused indices, no ZIP
  overlap, no validation/reserve fitting, observed-fit means/counts, kNN fitting arrays,
  fresh learned states and sampler traps on held prediction. An independent complete
  **raw-input ADASYN Pipeline.fit** receives only the asserted fitting matrix/labels,
  calls the sampler once, skips it on held prediction and reproduces probabilities
  to 1e-12. A deterministic final **training-only** sampler repeat reproduces actual
  final arrays/counts without another reserved prediction or model choice.
- All **110 Stage 06 primary results**, plus all earlier scores/masks/splits/model
  parameters/selections/transform hashes, match the pre-Stage-07 snapshot exactly,
  except timings/OS-memory snapshots and the timing-containing Stage 06 score hash.
  The score hash remains unchanged *within* Stage 07; cross-run comparison separately
  checks the actual metrics. All **132 prior sources/IDs** and **15 prior PNGs** remain
  exact. The original **912 out-of-range MICE predictions** remain documented unchanged.
- A source snapshot with **no data directory or CSV** builds all five Jupyter Book
  pages from saved outputs without `--execute`. Headless Chrome verifies the four-method
  table, 20 count/20 metric rows, all 1,380 distribution rows, one reserved row and seven
  new checks. All **18 figures** load, formulas render with no KaTeX errors, page width
  stays within viewport, and all **eight** homepage progress/navigation links return
  local HTTP 200. The three new plots and result/formula tables are visually inspected; the four
  confusion matrices share one color scale.
  Node's existing `url.parse` deprecation is an external build notice. GitHub Pages
  deployment is separate and not triggered or newly verified.

Raw/EDA SHA-256 and all ten protected hashes match the baseline:
raw `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`;
EDA `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`.
The same five initially dirty files receive this extension; staging stays empty,
HEAD unchanged, no CSV tracked and `git diff --check` passes.

| Stage 07 requirement | Status | Evidence / limit |
|---|---|---|
| Actual class counts and computational positive/minority | PASS | Full/train/validation/reserve and every fold |
| Numeric clinical polarity and complete target-time contract | PARTIAL — UNVERIFIED | Official concept confirmed; explicit 0/1 mapping/anchors unavailable |
| Common numerical-only four-treatment design | PASS — retrospective | 69 columns, nominal exclusions, same folds/LR/threshold |
| Train-only preprocessing and three required samplers | PASS | Fresh fold fits, actual counts, Pipeline.fit reproduction and held traps |
| P/R/F1/AUC, confusion, class distributions, runtime and fold SD | PASS | 20 original-prevalence held evaluations; no independent-CI claim |
| Distribution/realism/prior/geographic leakage discussion | PASS | Quantified diagnostics with unresolved clinical realism |
| Locked reserved evaluation | PASS — internal only | One prelocked candidate; 2,652 original observations; EDA exposure disclosed |
| Reproduction/preservation/CSV-free book | PASS | 72 executed cells, 54 check groups, 5 unit tests, prior results exact |
| External/prospective validity, calibration and clinical costs | NOT VERIFIED | Not inferred from this assignment benchmark |

**Advanced imbalance algorithms and controlled evaluation are implemented and verified
in the declared retrospective numerical scope.** The documentation criterion about
clinical 0/1 meaning is only partially verified; overall 100% rubric completion is
not asserted. Before the tabular branch can be described as scientifically complete
for an application, establish numeric label/temporal eligibility and intended prediction
time, justify missingness/synthetic constraints, and obtain independent external/
prospective performance with appropriate calibration/cost assessment. These are separate
from mechanically completing the rubric experiments. Mandatory Text/image part (b)
remains outside this task and unsatisfied by its placeholder.

## Historical Stage 06 — Feature Selection, Dimensionality Reduction & Group-aware F1

Starting HEAD: `0f276c25301552222b37b7332290dfe7d9ee50ba`. **The initial working tree already contained the five completed Stage 05 modified files; these were preserved, not discarded or committed.** The Stage 05 verifier was rerun successfully before extension. Its 112-cell notebook is the source/output preservation baseline for this task, rather than the historical HEAD's 92-cell Stage 04 notebook.

The complete [official assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) was retrieved with HTTP 200 and read through technical/reporting/grading requirements before editing; HTML SHA-256 remains `8d2a4a6e79902495d8f13e50530baf78433059b9620a05a7956298defa391720`. Required statistical/model/wrapper selectors, PCA/t-SNE, five-fold F1 and feature-count plots are implemented. UMAP is optional and omitted without a new dependency. No rebalancing or Text task is started; no commit/push/PR is made.

### Scope and independent fold-local learning

Sections **47–56**, zero-based cells **112–131**, append 20 cells / 10 code cells. Notebook total: **132 cells / 64 executed code cells**. All 112 previous sources/IDs/order and all **12 previous PNGs** are byte-identical; earlier statements deferring Feature Selection are superseded by Section 47. Historical records below remain intact.

The complete 83-field gate defines **74 raw retrospective supplied-record candidates**: the 69 audited numerical fields plus patient_race, payer_type, patient_state, Region and Division. ID/ZIP/target are never predictor columns; diagnosis code/text, novel treatment and constant gender remain excluded as documented. All 8,173 original inner-training observations remain. BMI is post-metastatic, payer/state are at-metastatic and contextual periods/clinical target anchors remain unresolved. **No earlier-baseline prediction timing or deployable clinical predictor set is established.** Temporal leakage is not repaired by grouped CV; conclusions apply to this explicitly retrospective supplied-table task.

Five fixed `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` splits use the original ZIP key; both labels occur in every fitting/held fold and ZIP overlap is zero. Held sizes are **1,634 / 1,641 / 1,632 / 1,634 / 1,632** with **86 / 81 / 99 / 81 / 96 ZIPs**. Fitting sizes are 6,539/6,532/6,541/6,539/6,541. All 22 configurations share these exact folds. The existing 2,081 validation and 2,652 reserved rows are not scored or consulted for Stage 06 selection/tuning. Prior full-file EDA exposure remains disclosed; the reserve is not advertised as an untouched external cohort.

Each fold freshly fits a numeric StandardScaler on observed fitting values, kNN10 (uniform, keep_empty_features=True), categorical constant-missing imputer and dense `OneHotEncoder(drop="first", handle_unknown="ignore")`, then a new StandardScaler on the completed mixed fitting matrix. Lexical fold-local reference coding is explicit and differs from Stage 05's most-frequent-reference demonstration. Chi-square sees nonnegative **pre-final-scaling 0/1 indicators**, not negative standardized coordinates. The final scaler standardizes numerical and indicator columns consistently for LR/RFE/PCA. Actual mixed dimensions are **136/133/135/136/135**, with fitting arrays 6.63–6.78 MiB. Means/observed counts, the pinned sklearn imputer fitting array, final-scaler N and categorical vocabularies are verified against each original fitting fold.

No globally fitted Stage 04 matrix, Stage 05 Target Encoding or pre-CV selector enters the experiment. Shared preprocessing/ranking caches are confined to one fold and reused only across its prescribed feature counts. Fresh sklearn objects are used across folds. Fitted raw-input sklearn Pipelines are assembled for all candidates; raw-held baseline predictions equal the cached transformed-held route in all five folds. Independently cloning and calling a complete **RFE Pipeline.fit on raw fold data** reproduces selected support and held probabilities, verifying equivalence of the explicit staged implementation. This avoids unnecessarily repeating kNN fits for every candidate while preserving fold locality.

### Predeclared candidate design

- Common classifier: L2 Logistic Regression, C=1, l1_ratio=0, solver=lbfgs, intercept=True, max_iter=2000, tol=1e−4, class_weight=None, seed=42, fixed threshold .5. Installed sklearn 1.9.1 supports this without deprecated penalty arguments. Primary F1-macro and secondary balanced accuracy, class-1 ROC-AUC, per-class recalls and predicted-label proportions are saved. No threshold/class-weight search occurs.
- Statistical filters: numerical ANOVA F/p; categorical occurrence Chi-square/p on 0/1 indicators; MI with the correct discrete-indicator/continuous-numerical mask, n_neighbors=3 and seed=42. k={10,30,50}. ANOVA passes all categorical columns; Chi-square passes all numerical columns. MI selects total top-k. Thus actual total counts differ by eligible scope, not by an undisclosed implementation shortcut.
- RF ranking: 100 trees, min_samples_leaf=2, max_features=sqrt, bootstrap=True, class_weight=None, seed=42, n_jobs=1. Tree bootstrap is the algorithm's standard mechanism, not class rebalancing. GB ranking: 50 trees, learning_rate=.1, max_depth=2, min_samples_leaf=5, seed=42. Each ranking model fits once per fitting fold; its top-k sets are evaluated using the same LR, not its own classifier predictions. Per-column and original-field aggregated importance are stored.
- RFE: same L2 LR family, step=.25, separate prescribed counts 10/30/50 fitted inside each training fold. The common five-fold evaluation is a valid group-aware comparison of these RFE counts; no uncontrolled nested RFECV search is performed. Actual masks, elimination ranks, transformed dimensions and runtime are retained.
- PCA: full SVD, whiten=False, all completed mixed coordinates standardized; fitting-fold cumulative-variance thresholds .90/.95/.99 determine actual q. The same LR evaluates each representation. PCA is unsupervised variance retention, not supervised selection of original variables or proof that low-variance directions lack discrimination.

There are **22 configurations / 110 primary held-fold LR evaluations**. All features/ranks/nominal p-values/selected identities/metrics remain available in Python. Wide full fold-ranking tables avoid printing thousands of repetitive long rows; absent fold-vocabulary columns are explicitly unavailable. All 110 selections are saved in an expandable table. Shared preparation, ranking/RFE/PCA and local LR fit/predict times are separate; their reused components should not be summed into a fictitious independent wall-time total.

### Actual CV results

The primary table below prints all five F1 values. SD is the sample SD (ddof=1) across five folds, **not an independent-fold confidence interval**. ANOVA/Chi-square k denotes the retained eligible block; other top-k methods denote total columns. PCA names its fixed training-variance target. No candidate was retuned after inspecting scores.

| Configuration | Actual columns | Fold 0 | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Mean F1-macro | Fold SD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No selection | 133–136 | 0.466550 | 0.426838 | 0.485373 | 0.460908 | 0.421101 | 0.452154 | 0.027352 |
| ANOVA k=10 | 74–77 | 0.432397 | 0.436448 | 0.429446 | 0.406189 | 0.406116 | 0.422119 | 0.014786 |
| ANOVA k=30 | 94–97 | 0.430935 | 0.438371 | 0.433535 | 0.416674 | 0.408853 | 0.425674 | 0.012396 |
| ANOVA k=50 | 114–117 | 0.439576 | 0.433125 | 0.454582 | 0.488448 | 0.442850 | 0.451716 | 0.021961 |
| Chi2 k=10 | 79–79 | 0.461776 | 0.425191 | 0.428139 | 0.433323 | 0.405301 | 0.430746 | 0.020338 |
| Chi2 k=30 | 99–99 | 0.457758 | 0.436458 | 0.454543 | 0.461533 | 0.414466 | 0.444952 | 0.019573 |
| Chi2 k=50 | 119–119 | 0.462966 | 0.428314 | 0.463882 | 0.464876 | 0.417312 | 0.447470 | 0.022852 |
| MI k=10 | 10–10 | 0.385862 | 0.383778 | 0.386626 | 0.390163 | 0.392463 | 0.387778 | 0.003487 |
| MI k=30 | 30–30 | 0.433833 | 0.401909 | 0.403049 | 0.431450 | 0.419685 | 0.417985 | 0.015140 |
| MI k=50 | 50–50 | 0.434608 | 0.392513 | 0.428452 | 0.465370 | 0.393087 | 0.422806 | 0.030756 |
| RF k=10 | 10–10 | 0.384557 | 0.383778 | 0.384151 | 0.391135 | 0.383453 | 0.385415 | 0.003224 |
| RF k=30 | 30–30 | 0.415932 | 0.406658 | 0.408603 | 0.403015 | 0.391232 | 0.405088 | 0.009065 |
| RF k=50 | 50–50 | 0.438265 | 0.421491 | 0.433176 | 0.456023 | 0.391213 | 0.428034 | 0.024048 |
| GB k=10 | 10–10 | 0.414238 | 0.383778 | 0.412869 | 0.383505 | 0.386259 | 0.396130 | 0.015949 |
| GB k=30 | 30–30 | 0.428432 | 0.414253 | 0.433010 | 0.403019 | 0.392831 | 0.414309 | 0.016867 |
| GB k=50 | 50–50 | 0.456353 | 0.405781 | 0.443922 | 0.415638 | 0.405033 | 0.425345 | 0.023432 |
| RFE k=10 | 10–10 | 0.384093 | 0.384240 | 0.384847 | 0.391655 | 0.386553 | 0.386278 | 0.003161 |
| RFE k=30 | 30–30 | 0.424943 | 0.396860 | 0.401262 | 0.442064 | 0.418795 | 0.416785 | 0.018355 |
| RFE k=50 | 50–50 | 0.432359 | 0.423474 | 0.437888 | 0.445739 | 0.432373 | 0.434367 | 0.008191 |
| PCA 90% | 53–54 | 0.437422 | 0.423781 | 0.427827 | 0.421872 | 0.395185 | 0.421217 | 0.015740 |
| PCA 95% | 63–65 | 0.450385 | 0.433711 | 0.439343 | 0.420677 | 0.410527 | 0.430929 | 0.015640 |
| PCA 99% | 86–87 | 0.449994 | 0.432432 | 0.435907 | 0.444040 | 0.407178 | 0.433910 | 0.016448 |

**No feature-reduction candidate exceeded the no-selection mean.** The best reduced candidate is **ANOVA k=50**, retaining 114–117 total columns, mean F1=**0.4517162106093749**, SD=**0.021960816247211058**, versus no-selection **0.4521541171754245 ± 0.027352296643557903** on 133–136 columns; difference=**−0.0004379065660496**. This is a descriptive same-fold comparison, not formal evidence of equivalence or independent significance. The protocol is preserved despite weak results; diagnosis fields, feature counts, classifier/threshold and seeds are not changed to improve appearances.

Baseline balanced accuracy=**0.51012856**, class-1 ROC-AUC=**0.54324012**, mean class-0 recall=**0.09798189**, class-1 recall=**0.92227522**, predicted class-1 proportion=**91.4683%**. These diagnose weak discrimination/fixed-threshold majority prediction in this feature/classifier scope, without proving why performance is low or that rebalancing would fix it. No downstream generalization or clinical utility claim is made.

### Selected features, stability and importance interpretation

For ANOVA k=50, mean cross-fold column Jaccard=**0.820856**, original-field Jaccard=**0.683400**. Its five nominal fields are **passthrough by design**, not selected by ANOVA. Numerical fields selected in all five folds include patient_age, density, family_size, income_household_median, home_value, education_less_highschool, labor_force_participation, unemployment_rate and PM25; the complete 74-field frequency table records every selected/unselected field, including unresolved semantic fields without interpreting their names clinically. Actual per-fold selected feature identities are preserved rather than replaced with one hypothetical global feature set.

RF mean original-field importance is led by **patient_age=0.246197, bmi=0.183103, patient_race=0.088822, payer_type=0.070191**; GB is led by **patient_age=0.474391, patient_state=0.081800, payer_type=0.050165**. All per-column scores and original-field sums/SDs remain auditable. Impurity cardinality bias, correlated geographic alternatives and field-size effects prevent causal or model-independent interpretation. Aggregating dummies improves traceability but does not eliminate bias. RFE coefficient elimination also depends on conditioning/correlated alternatives. Column stability reflects fitted vocabularies as well as selection; original-field stability is separately reported. PCA component names can rotate/sign-flip across folds, so PC-name Jaccard is deliberately unavailable.

ANOVA normality/equal-variance/independence references and Chi-square expected-count asymptotics are not guaranteed under ZIP repetition, ties, rare levels and imputation. Their p-values are nominal, unadjusted ranking references, without formal rejection/causal conclusions; numeric zeros are described as zero/underflow rather than literal probabilities. Chi-square's occurrence score is not misrepresented as the complete presence/absence contingency test. MI estimates may be zero-clipped and rely on internal continuous-value jitter; zero does not prove independence. Univariate filters can retain redundancy/miss interactions.

### PCA and t-SNE evidence

CV PCA counts are **53–54 / 63–65 / 86–87** for 90/95/99%. After freezing CV metrics, a **separate unsupervised display-only fit** on all 8,173 inner-training rows reports the complete 136-component spectrum and **55 / 65 / 88** components for 90/95/99%. Different display/fold populations and vocabularies explain why counts need not coincide. Neither this display imputer/scaler/PCA nor its coordinates enter CV predictions. Scree/cumulative-variance and 2D PCA plots are saved. Standardized redundant/rare indicator coordinates contribute separate variance weight; variance retention is not supervised discrimination.

A deterministic **2,000-patient** sample is drawn uniformly from inner training using seed=42 **without labels**, not stratified by outcome or selected for visual separation. t-SNE uses the first **50 display PCs**, retaining **0.8703757049** of display variance, perplexity=30, init=pca, learning_rate=auto, max_iter=1000, Barnes–Hut, seed=42, n_jobs=1. Both labels only color the resulting PCA/t-SNE plots after fitting. Actual sample labels are 742 class0 / 1,258 class1; ZIP coverage, runtime, 999 iteration attribute and KL objective **0.3121621013** are printed. The iteration attribute/budget and KL are optimization diagnostics, not proof of convergence or prediction. Apparent clusters/overlap, local distances and axis positions are exploratory, sensitive to sample/PCA/perplexity/seed and repeated ZIP context. UMAP remains optional/not implemented; no fragile dependency is introduced.

### Execution, preservation and publication

- Fresh `.venv` Restart Kernel / Run All completes **64 code cells sequentially**, with real saved outputs and no notebook exception/stderr. **47 notebook check groups pass**: 40 earlier plus seven new Stage 06 groups. All **five existing unit tests** pass without skips.
- Independent fixtures verify known ANOVA ordering, analytic Chi-square=20/0, discrete MI=log(2)/0, top-k/feature order, RFE signal support/dimensions, held-extreme/unknown-category train-only preprocessing, known PCA spectrum/counts and nonmutation. Real checks cover five fresh learned states, zero group overlap, original-feature provenance, all 110 metrics/pipeline dimensions, PCA threshold arithmetic, score freezing before displays and the independent complete raw-input Pipeline.fit repeat.
- The complete experiment was rerun after adding class diagnostics and the independent Pipeline.fit check. **All 110 primary F1/balanced-accuracy/AUC and feature counts reproduce exactly.** All previous Stage 02–05 score/parameter/mask/split/selection/VIF/transform-hash results remain exact, except measured runtimes/OS-memory snapshots. All 112 previous sources/IDs and 12 prior images remain exact. The 912 MICE support violations and all older caveats remain visible.
- A final source snapshot **without a data directory or CSV** builds all five Jupyter Book pages from saved outputs without `--execute`. Headless Chrome verifies the 83-row gate, five-fold fit audits, **22-row five-F1 table**, 22 secondary-metric rows, six full ranking tables, all **110 saved selections**, three PCA-threshold rows and seven new check rows. All **15 figures** load, **26 KaTeX expressions** have zero errors, document width stays within the viewport and all **seven** homepage progress/navigation links return local HTTP 200. The main F1 table and all three new figures/formulas were visually inspected.
- Six CV sklearn notices for unknown held categories are captured/described (cached-held and raw-held verification routes); **no convergence warning** remains. The existing external Jupyter TCP-transport and Node `url.parse` deprecation notices are explained as tooling notices, not scientific-cell failures. No dependency/kernel/deployment setting is changed to suppress them. GitHub Pages deployment is separate and not newly verified or altered.

Raw CSV SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. All ten protected-file hashes match the baseline. Raw schema/values, all original training rows, imputation provenance and both external holdouts remain unchanged. The five already-modified Stage 05 files receive the Stage 06 additions only: preprocessing notebook, homepage, tabular index, README and this audit. No raw/prediction dataset, helper module, dependency, rebalancing/Text experiment, commit or push is added.

| Stage 06 requirement | Status | Evidence / scope |
|---|---|---|
| Semantic/temporal primary-feature gate | PASS — retrospective | All 83 fields; 74 explicit candidates; protected/clinical exclusions; prospective approval not established |
| ANOVA F-test | PASS | All 69 numerical fields per fitting fold, full F/p/ranks, three blockwise counts |
| Chi-square | PASS | Nonnegative categorical indicators before centering; full score/p/ranks; other block retained |
| Mutual Information | PASS | Correct discrete/continuous declarations, fixed seed/neighbors, rankings/top-k |
| Random Forest importance | PASS | Five train-fold fits; stored column/group importances; common LR evaluation |
| Gradient Boosting importance | PASS | Five fixed train-fold fits; same reporting/evaluation and bias caveats |
| RFE with CV | PASS | 15 fitting-fold RFE fits at three k, elimination ranks/runtime and shared grouped held evaluation |
| PCA | PASS | Fold-local threshold comparison; separate complete display spectrum, 90/95/99% counts, scree/2D |
| t-SNE | PASS | Training-only label-independent sample/fit, seed/settings/diagnostics and cautious 2D interpretation |
| UMAP | OPTIONAL — omitted | No demonstrated need for an extra dependency beyond required PCA/t-SNE |
| Five-fold F1 and feature-count comparison | PASS | 22 configs, 110 evaluations, five F1s/mean/SD, secondary metrics, stability and plot |
| Fold-local learning / reserve protection | PASS | Raw-input fits, learned-state audits, zero ZIP overlap, independent Pipeline.fit reproduction; no external-holdout score |
| Reproducibility / preservation | PASS | 64-cell Run All, 47 notebook checks, 5 unit tests, exact repeated CV/prior sources/results/hashes |
| Jupyter Book presentation | PASS | CSV-free five-page build; all tables/plots/formulas/links checked |
| Independent final/prospective predictive performance | NOT VERIFIED | Current CV also supports candidate selection; temporal contract and external final assessment remain unresolved |

**Stage 06 is complete for the requested retrospective development comparison, with no identified correctness/execution blocker to a separately scoped Stage 07.** No feature reduction improved mean F1 in this fixed experiment. Further stages must retain fold-local learning, establish the intended prediction-time contract and reserve an appropriate independent final assessment; no 100% overall-project completion, deployability or performance gain is claimed.

## Historical Stage 05 handoff — Categorical Encoding & Multicollinearity

Starting HEAD: `0f276c25301552222b37b7332290dfe7d9ee50ba`; initial working tree clean. The complete [official assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) was retrieved with HTTP 200 and read before editing, through technical/reporting/grading requirements; HTML SHA-256 remains `8d2a4a6e79902495d8f13e50530baf78433059b9620a05a7956298defa391720`. The indexed [official Challenge #1 dictionary](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data), installed sklearn APIs and [statsmodels VIF reference](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html) were reviewed. No Challenge #2 data/solution or unverified code lookup supplies clinical interpretations. The rubric's ambiguous explained-variance wording is interpreted as its named **variance inflation factor**, not an explained-variance ratio.

### Preserved work and explicit eligibility contract

Sections **37–46**, zero-based cells **92–111**, append 20 cells / 10 code cells. The notebook now has **112 cells / 54 executed code cells**. All preceding 92 sources, IDs and order remain exactly unchanged, as do all 11 prior PNGs. Earlier pending-Encoding statements in the notebook are explicitly superseded by Section 37; no preceding bug required a source change.

The complete audit covers **12 categorical/code/text fields plus protected patient ID and target**, recording dtype, dictionary-supported broad meaning, training cardinality/missingness, rare-category counts/row share, >20 status, ordering/timing and eligibility/reasons. Rare means <1% of all inner-training records; no category is merged. Numeric-looking ICD tokens remain nominal; no ordinal disease severity or category order is invented. The other 69 audited measurements/contextual columns remain numerical; no numerical measurement stored as a categorical string is identified in this field inventory.

**Common comparison: five nominal fields**, patient_race, payer_type, patient_state, Region and Division, on all **8,173 original inner-training rows**. State is included as a repeated coarse geographic attribute before method results, not a unique patient identifier or a replacement ZIP key. Region/Division are retained to expose redundancy. ZIP3 remains **only the group key**; patient ID and target never enter predictors. Diagnosis code/description fields await clinical/temporal validation and are outside the controlled nominal scope; post-metastatic treatments and constant gender are excluded. This is an audited encoding scope, not automatic Feature Selection or a claim that excluded fields can never be encoded.

**Retrospective supplied-table demonstration, not earlier-baseline predictor approval.** The dictionary records payer/state/gender/ZIP on the metastatic date and treatment afterward; race chronology, regional periods and diagnosis-code dates/clinical interpretation remain unresolved. All audited baseline-predictor approvals remain false. Encoding implementation eligibility is distinguished from prospective eligibility. Group-aware cross-fitting prevents a particular target leakage route; it cannot fix temporal availability. The prior full-file EDA exposure remains disclosed.

| Included field | Nonmissing training categories | Missing N | Encoding role |
|---|---:|---:|---|
| patient_race | 5 | 4023 | Nominal patient descriptor; no ordering |
| payer_type | 3 | 1179 | Nominal payer, recorded at metastatic date |
| patient_state | 46 | 39 | High-cardinality coarse geography; 6-bit encoding qualifies |
| Region | 4 | 39 | Regional context; recorded hierarchy checked |
| Division | 9 | 39 | Regional context; recorded hierarchy checked |

Validation/reserved sizes remain **2,081 / 2,652**; all ZIP-disjoint splits, Stage 03 keep-all policy, raw values and prior imputation/scaling are preserved. Unsupervised maps fit inner training only. Validation categories are transformed solely to audit unseen handling, without labels/tuning; the reserve is not transformed or used for encoding design. No patient-level encoded dataset is printed/exported.

### Methods, mappings and actual storage comparison

Canonical copies preserve literal strings and use a reserved missing token with collision rejection. This is an explicit representation policy, not a clinical missingness mechanism or raw-data replacement. No spelling/code normalization, rare grouping or missingness imputation experiment is added. All mappings/names/row identities and matrices remain inspectable in memory. Payload below excludes index/estimator maps and measures actual CSR data/indices/indptr or dense array bytes, not just dimensionality.

| Method | Input fields | Output columns | Nonzero density % | Actual payload MiB | Dense float64 equivalent MiB |
|---|---:|---:|---:|---:|---:|
| One-Hot | 5 | 67 | 5.17795 | 0.355667 | 4.177788 |
| Ordinal illustrative | 5 | 5 | 79.17289 | 0.311775 | 0.311775 |
| Target OOF | 5 | 5 | 100 | 0.311775 | 0.311775 |
| Binary hybrid | 5 | 27 | 19.50506 | 0.523758 | 1.683586 |
| Frequency | 5 | 5 | 100 | 0.311775 | 0.311775 |

- **One-Hot:** sklearn float64 CSR, handle_unknown=ignore, no rare grouping, one most frequent **nonmissing** training reference per field with lexical tie-break. References and all categories are saved. A missing level is explicitly reserved; drop-one coding avoids each field's intercept/dummy trap but not cross-field dependence. Unseen categories have zero blocks and collide with the reference representation; no learned missing value is claimed for them.
- **Ordinal:** sklearn OrdinalEncoder, deterministic lexical categories, explicit missing token, unknown_value=−1. No genuine ordinal meaning is verified. This satisfies the requested **clearly labeled implementation illustration**, not a clinical scale or recommended nominal distance representation. Ordering changes can affect geometry/correlations/VIF.
- **Target:** five label-independent shuffled ZIP GroupKFold splits, seed=42, fixed smoothing alpha=10. For held fold f, category counts/sums and global prior use only other folds: (sum+alpha×prior)/(count+alpha); unseen categories use that other-fold prior. All fitting/held folds contain both labels and have zero row/ZIP overlap. OOF training values remain separate from maps fitted on the entire **inner-training** set for validation/future transformation; train+validation is not pooled. Label 1's numeric mean is encoded without inventing clinical target polarity.
- **Binary hybrid:** state has 46 nonmissing levels, plus missing code=1 and unknown code=0. Sorted nonmissing codes=2…47 require **ceil(log2(48))=6 bits**, most-significant first. Known/missing bit patterns are unique; unknown is all zero. Four low-cardinality fields keep the same reference One-Hot policy (21 columns), giving **27** total. This is not claimed to binary-encode every field. Bits/codes do not carry meaningful order or Hamming distance.
- **Frequency:** training-only relative counts n(category)/8173 including observed missing; absent/unknown levels map to zero. State's 47 fitted levels produce only **40 distinct frequencies**, seven category-to-value collisions. Other four fields have no within-field frequency collision in this sample. Counts are patient-weighted, not independent area-population prevalences.

Binary reduces columns but **increases actual CSR payload** versus One-Hot because bits are denser; smaller dimensions do not guarantee smaller storage. Validation contains **21 nonmissing state values unseen in training**, while the other four fields have none. All five methods produce finite outputs for these rows under their documented unknown policies. sklearn's expected One-Hot unknown/drop warning is captured and displayed, not hidden or left as unexplained stderr.

### Target leakage verification and later cross-validation

The five OOF held-fold sizes are **1,322 / 1,877 / 1,920 / 1,392 / 1,662**; held ZIP counts are **89 / 89 / 89 / 88 / 88**. Fitting priors range **0.621462–0.629447**; fourteen held category-cells are unseen in their fitting folds and receive the corresponding prior. Fold assignments are created without labels and never searched for desirable results. Actual per-fold class counts/ZIP support/priors are printed and stored.

Independent unique-category (>20 levels) and group-specific-category fixtures show held records receive other-fold priors. Flipping one held record's label (which changes the full-sample prior), or all labels in its held fold, leaves that fold's encodings unchanged with fixed folds. An analytic smoothing fixture checks values .5, 5/11 and 6/11; unknowns receive .5. Full-training mappings intentionally differ from OOF training values and are never substituted into the VIF training matrix. Real fold counts/sums are independently recomputed from raw matching categories/other-fold labels, priors are checked, and a deterministic full OOF repeat matches exactly.

Later model CV must reconstruct supervised encodings **inside each model-training fold**; globally precomputing these OOF features does not make an unrelated outer CV leakage-free. No validation/reserved labels fit/tune encoders, no model-selection performance is estimated, and no prospective validity follows from cross-fitting.

### Rank, exact/near dependence and scoped VIF

VIF_j=1/(1−R²_j) uses an auxiliary OLS regression of predictor j on the others **with an intercept**, not an outcome classifier. Columns are centered/scaled for numerical conditioning; this affine change leaves intercept-based VIF invariant. Exact constants remain in outputs but have unavailable VIF=NaN and are omitted only from auxiliary solves. RSS/TSS<=1e−12 is explicitly reported as **Inf: numerically perfect/near-perfect**, without fabricating a finite value or asserting every near-dependence is mathematically exact. The intercept itself is not assigned VIF.

Full-design centered SVD rank is audited for all **69 numerical columns plus each encoded block** using the stated NumPy machine-precision tolerance. The completed numerical baseline has rank **69/69** but condition **1.76372e10**: full rank does not imply good conditioning. This is a completed full-training design diagnostic, distinct from the earlier complete-case correlation diagnostic with a different matrix/population/tolerance. Recorded child→parent audits find state→Division, state→Region and Division→Region each have at most one parent per child level, including missing; no external geographic validation is inferred.

| Design | Full predictor columns (69 numerical + encoded) | Centered rank | Scoped per-column VIF columns (6 numerical + encoded) | Infinite / near-perfect VIF | Max finite scoped VIF |
|---|---:|---:|---:|---:|---:|
| Numerical baseline | 69 | 69 | 6 | 0 | 2.477783 |
| One-Hot | 136 | 123 | 73 | 55 | 2.978635 |
| Ordinal illustrative | 74 | 74 | 11 | 0 | 2.483542 |
| Target OOF | 74 | 74 | 11 | 0 | 2.902886 |
| Binary hybrid | 96 | 92 | 33 | 12 | 3.237051 |
| Frequency | 74 | 74 | 11 | 0 | 2.677666 |

The **145-row** auditable VIF table includes every encoded output plus the same six pre-existing numerical illustrations (age, BMI, density, household median income, education share, PM25), with a numerical-only baseline and before/after numerical VIF table. No numerical subset is chosen after inspecting VIF; primary matrices retain all 69 numerical columns. This bounded semantic scope avoids letting existing near-redundant geographical shares dominate each per-column diagnostic. VIF conclusions apply only to this scope; full-design rank remains a separate check. No actual output column is constant; all finite scoped VIF values are below the descriptive threshold 5 **while the explicitly infinite columns remain present**.

One-Hot's 13 full-design rank deficiencies and Binary hybrid's four remain despite drop-one reference coding. Compressed nominal/bit/frequency/OOF designs can hide dependencies nonlinearly or lose category information; their finite VIF does not establish superior encoding, independence, meaningful order or predictive benefit. OOF target features are supervised/fold-dependent, so their VIF is descriptive. No automatic dropping, feature selection, VIF p-value test or winner is introduced. One compact two-panel figure compares dimensions and finite/infinite scoped counts with these limits stated.

### Execution, integrity and publication evidence

- Fresh `.venv` **Restart Kernel / Run All** executes all **54 code cells in order**, saving real aggregate outputs without notebook exceptions/stderr. JSON/schema, unique IDs and old-source preservation validate. There are **40 passing notebook check groups**: 34 earlier plus six new Encoding groups. All **five existing project unit tests** pass without skips.
- New fixtures cover unknown/missing levels, token collisions, an actual <1% rare category retained without pooling, reference-coded One-Hot rank, arbitrary ordinal unknown codes, analytic relative frequencies/equal-frequency collisions, 25-level binary uniqueness/bit count, OOF own-label/prior/group leakage, analytic smoothing, independent VIF=1, perfect dependence=Inf, constants=NaN and affine invariance. Numerical-baseline VIF matches statsmodels; real mappings/masks/indices and full OOF repeats are checked.
- External comparison preserves all 92 previous sources/IDs and **all 11 prior PNGs** byte-for-byte. All Stage 02 aggregate/per-feature scores/masks/splits/settings/draws, Stage 03 thresholds/flags/Jaccard/KS/treatment outputs and Stage 04 fitted statistics/transform hashes reproduce exactly. Only runtimes and OS-memory snapshots refresh. kNN10 Macro NRMSE remains **0.6763300629944509**; MICE raw RMSE **12463.419984895585** and its **912 support violations** remain unchanged and documented.
- A final source snapshot with **no data directory/CSV** builds all **five Jupyter Book pages** from saved outputs without execution. Headless Chrome verifies the 14-row audit, five-method comparison, five-fold audit, six-row rank/VIF summaries, complete 145-row VIF table, six verification rows and Sections 37–46. All **12 figures** load, **24 KaTeX expressions** have zero errors, the document stays within the viewport and all **six** homepage progress/navigation links return local HTTP 200. Tables/math/figure were visually inspected.
- Captured sklearn unknown-category notices are expected behavior for the documented validation categories. The execution launcher also records the existing Jupyter TCP-transport notice, and the build records the existing Node `url.parse` deprecation notice; neither is a statistical-cell failure. No dependency/kernel/deployment configuration is changed to suppress them. Public GitHub Pages state is separate and is not changed/newly verified.

Raw CSV SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. All ten protected-file hashes match the initial snapshot; df schema/values, all training rows, both holdouts and imputation provenance remain unchanged. Only the preprocessing notebook, book homepage, tabular index, this audit and relevant README text change. No dependency/helper module, raw/encoded dataset export, Feature Selection/resampling/classifier/Text experiment, commit, push or PR is added.

| Stage 05 requirement | Status | Evidence / limitation |
|---|---|---|
| Complete categorical/code eligibility and leakage audit | PASS | 14 fields; protected/clinical/constant exclusions; retrospective versus prospective gate |
| One-Hot Encoding | PASS | Five fields, 67 CSR columns, explicit references/missing/unseen/rare behavior |
| Ordinal Encoding | PASS — illustration | sklearn implementation and tests; no genuine semantic ordinal scale verified or invented |
| Cross-validated Target Encoding | PASS | Label-independent ZIP OOF, fixed smoothing, separate full-inner-training map, label/prior leakage fixtures |
| High-cardinality Binary Encoding | PASS — hybrid scope | Real state >20 categories, six bits, four low-cardinality One-Hot fields; ZIP/ID excluded |
| Frequency Encoding | PASS | Train relative frequencies, unseen=0, actual category collisions and analytic fixtures |
| VIF/multicollinearity comparison | PASS — scoped | Full-design rank plus 145 scoped VIF rows; intercept/constants/Inf/tolerance and scope documented |
| Reproducibility/data preservation | PASS | 54-cell Run All, 40 notebook check groups, 5 unit tests, exact prior results/PNG/source/hash checks |
| Jupyter Book presentation | PASS | CSV-free five-page build, full tables, browser/math/link/figure checks |
| Earlier-baseline clinical predictor eligibility | NOT VERIFIED | At-metastatic recording, unresolved dates/clinical definitions; no predictive approval |

**Stage 05 is complete for the requested retrospective comparison, including the authorized Ordinal illustration and explicitly scoped Binary/VIF designs. No identified correctness/execution blocker prevents Stage 06 Feature Selection as a controlled methodological experiment.** Before prospective modeling or predictive claims, establish the feature-time contract and rebuild supervised encodings inside the relevant training folds. No global encoding winner, fully validated pipeline or 100% overall-project completion is asserted.

## Historical Stage 04 handoff — completed controlled Scaling comparison

Starting HEAD: `8a527795aaca85f2b0b1381d0a32e320bbec1341`; initial working tree clean. The complete [official assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) was retrieved with HTTP 200 and read again before editing, including tabular requirements, technical/reporting instructions and grading. Its HTML SHA-256 remains `8d2a4a6e79902495d8f13e50530baf78433059b9620a05a7956298defa391720`. The rubric requires Min-Max, Z-score, Robust and Quantile Transform with uniform **or** normal output; testing **both** quantile outputs is a deliberate extension. Levene is optional, and is included as one narrowly scoped diagnostic below. No overall grade or predictive improvement is claimed.

### Source preservation, population and feature coverage

Sections **28–36**, zero-based cells **72–91**, are appended to the existing preprocessing notebook: **92 cells / 44 executed code cells**. All previous 72 cell sources, IDs and order are preserved exactly; no preceding issue blocked Scaling and no historical experiment is rewritten. Earlier notebook statements deferring Scaling are explicitly superseded by Section 28. The EDA, raw data, configuration, dependencies and deployment workflow are unchanged.

Every method starts from the same **8,173×69 original-unit completed training frame**, `outlier_common_train_raw`, copied as `scaling_train`. It does not start from the standardized view. Stage 03's keep-all recommendation is honored: no row filtering, detector choice, re-imputation, outlier-treatment experiment or change in sampling occurs. The 2,081 validation and 2,652 reserved rows are not fitted/transformed/scored to select scalers. Target, ID, ZIP and nominal clinical codes are excluded. No imputer/detector is refitted by the new cells; new fits are the five scalers and declared correctness repeats only.

Original observed values are preserved exactly; all **5,717** estimated cells retain their provenance mask, including **5,642 BMI estimates** alongside **2,531 observed BMIs**. The 69-feature input audit checks finite values, unique row/column identities, constant/near-constant values, skewness and semantic/bounded roles. Actual constants=0, near-constants=0 under the declared >=99% identical-value convention, high-|skew|>1 completed columns=29, bounded area shares=52. These are descriptive tags, not exclusions or a new normality-testing study. Individual versus repeated ZIP context, post-metastatic BMI, unresolved periods/units and conflicting dictionary entries retain their previous cautions.

### Five configurations and actual fitted properties

Installed sklearn **1.9.1** supports `QuantileTransformer(subsample=None)`. All five estimators and complete transformed DataFrames remain in `scaling_models` / `scaling_frames`. Original is a reference, not a sixth method. The full 69-row parameter table records affine extrema/multipliers/offsets, means/variances/scales, medians/IQR scales, quantile-grid/distinct-knot counts and endpoint masses. Both quantile estimators retain their complete 1000×69 fitted knots and reference probabilities for inspection.

| Configuration | Explicit settings | Actual training evidence |
|---|---|---|
| Min-Max | feature_range=(0,1), clip=False, copy=True | All 69 fitted minima map to 0; max endpoint error 2.22045e−16 |
| Standard | with_mean=True, with_std=True, copy=True; ddof=0 | Max absolute mean 1.81874e−15; max absolute SD−1 error 2.22045e−16 |
| Robust | centering/scaling=True; quantile_range=(25,75); unit_variance=False; copy=True | All 69 transformed medians 0 and IQRs 1 to measured precision |
| Quantile Uniform | n_quantiles=1000, output=uniform, subsample=None, seed=42, copy=True | Finite outputs in [0,1]; feature SD range 0.288657–0.293802 |
| Quantile Normal | n_quantiles=1000, output=normal, subsample=None, seed=42, copy=True | Finite outputs approximately [−5.199338,5.199338]; feature SD range 1.000244–1.669680 |

All training rows contribute to both quantile fits; no quantile/subsampling parameter search is added. Uniform/normal fitted knots are exactly equal. Constants, zero-IQR scaling and quantile ties/endpoints are explained using sklearn semantics rather than arbitrary replacements of the source data. Min-Max `clip=False` permits future values outside [0,1]; quantile outputs saturate beyond fitted bounds, with finite normal-tail clipping. No extra clipping/jitter of the raw measurements is performed.

### Full numerical evidence and comparative interpretation

`scaling_full_summary` contains all **414 feature/representation rows** with N, mean, median, population SD, min/max, Q1/Q3/IQR, P01/P99, skewness and finiteness. The 69-row input audit and parameter table plus the 414-row summary render as expandable height-limited tables. The compact six-representation overview includes descriptive SD ranges, median absolute skew and runtime; raw-unit SD ranges do not rank feature quality or transformations. Maximum affine skewness change is **2.41585e−13**. Original/Min-Max/Standard/Robust all retain 29 high-|skew| features; Uniform has 0 and Normal has 2 under this descriptive threshold, without implying that any distribution is verified Gaussian or superior.

Representative **density** results, computed from the same completed population:

| Representation | Mean | Population SD | Median | IQR | Min / max | Skewness |
|---|---:|---:|---:|---:|---|---:|
| Original | 1336.089690 | 1894.117454 | 731.814286 | 1500.176062 | 0.916667 / 21172 | 3.798859 |
| Min-Max | 0.063066 | 0.089467 | 0.034523 | 0.070860 | 0 / 1 | 3.798859 |
| Standard | approximately 0 | 1 | −0.319027 | 0.792018 | −0.704905 / 10.472376 | 3.798859 |
| Robust | 0.402803 | 1.262597 | 0 | 1 | −0.487208 / 13.625191 | 3.798859 |
| Quantile Uniform | 0.500012 | 0.288723 | 0.498999 | 0.496997 | 0 / 1 | −0.000356 |
| Quantile Normal | 0.002411 | 1.014442 | −0.002509 | 1.339555 | −5.199338 / 5.199338 | 0.135471 |

Positive affine scaling changes units/location/scale while preserving within-feature shape, ordering and relative spacing. Min-Max density IQR=0.07086 illustrates central compression relative to its fitted extremes. Standard's unit SD does not remove the long tail; Robust's IQR scaling also leaves tails. Quantile mapping changes marginal spacing and can change Pearson relationships/distance geometry while remaining nondecreasing; it does not remove ZIP dependence or establish multivariate normality.

The largest Quantile Normal SD is **1.669680 for `farmer`**, skew=−1.786716. Its uniform map has **648 records at the lower endpoint and one at the upper**, with 336 distinct fitted knots: these endpoint masses limit a Gaussian approximation. This is reported without inventing a new clinical/domain interpretation of the column. BMI observed-only SD=**5.798** versus **1.926** among imputed cells; observed-only skew=0.930413 versus completed skew=1.143179. Estimated-value concentration is not evidence that missing patients truly have lower variability. The provenance-separated violins make that representation difference visible after a pooled quantile fit.

### Focused variance diagnostic and violin figures

One prespecified individual-level feature, **observed BMI**, is compared between age<=training-median and age>training-median groups. The actual training median is **59**, with **1,323 / 1,208 observed BMI values**. Age provides an interpretable life-stage grouping for descriptive spread; no clinical mechanism or target-based stratification is asserted. Every representation uses identical group membership/observed support; imputed BMI never enters this diagnostic. Feasibility minimum=20 per group, not a power guarantee.

| Representation | Median-centered Levene W | Nominal p |
|---|---:|---:|
| Original | 4.285634505 | 0.038537017 |
| Min-Max | 4.285634505 | 0.038537017 |
| Standard | 4.285634505 | 0.038537017 |
| Robust | 4.285634505 | 0.038537017 |
| Quantile Uniform | 3.825369583 | 0.050592163 |
| Quantile Normal | 3.877852015 | 0.049036124 |

This is `levene(center="median")` between **two nonoverlapping age groups within each representation**, not between measurements and their own scaled values. For any shared nonzero affine scale, centered absolute deviations multiply by |a| and both W sums of squares by a², so W/p remain invariant; the three affine rows verify this numerically. Nonlinear transforms may change group spread relationships. Repeated ZIP context, tied BMI, naturally missing-BMI selection and pooled fitted quantile maps limit independence/calibration. P-values are explicitly **nominal exploratory references**, with no formal significance classification, variance-equality acceptance, residual-homoscedasticity claim, clinical claim, multiple-testing correction or p-based winner. A nearby numerical p-value does not establish restored equal variances or predictive benefit.

Three violin figures cover exactly six predeclared features: age, BMI, density, household income median, education share and PM25. Each feature has six panels in two rows of three, with **independent numerical axes** and original versus transformed units labeled. Observed/imputed values are separated and N printed; all training values are retained without tail trimming or sampling. Cut=0, quartile interiors, width normalization and smoothing limitations are explained; constant groups use points, missing provenance groups remain empty. Counts include PM25's 8,148 observed / 25 estimated values. No individual patient IDs/rows are printed or exported.

### Recommendation, correctness and publication

**No global scaling winner is declared.** Standard is a transparent candidate for mean/SD-conditioned distances and linear regularization; Robust is a candidate when central-IQR conditioning is useful, with tails retained; Min-Max is a candidate for training-range coordinates with future-range checks. Quantile outputs are candidates only where nonlinear reshaping/tail saturation is acceptable. Bounded shares and area-level income retain their original semantic cautions. Mechanical invariants, desired marginal shape, preserving meaningful information and predictive gains are different objectives. Later decisions need training-fold-local imputation/scaling, geographic separation, temporal eligibility and held-out predictive evaluation; no classifier is trained here.

- Fresh `.venv` **Restart Kernel / Run All** completes all **44 code cells** in order, saving real outputs with no notebook exception/stderr. Notebook JSON/schema, unique IDs and source preservation validate. There are **34 passing notebook check groups**: 27 previous groups and seven new Scaling groups. All **five existing unit tests** pass without skips.
- Independent fixtures verify manually known Min-Max, Standard mean/variance, Robust median/IQR, constant/repeated inputs, both quantile output modes, finite tail saturation, monotonic ordering, out-of-training-bound behavior and nonmutation. Known median-Levene W=2.4 is checked; insufficient, constant and constant-centered-deviation groups return explicit unavailable results. No unsupported exact nonlinear inverse equality is imposed.
- Real-data checks cover all five aligned finite 8173×69 outputs, full 414 summaries, fitted train extrema/means/variances/medians/IQRs, full-population quantile grids, exact deterministic repeats for both quantile outputs, same observed-BMI groups and affine Levene invariance. Raw/original/common matrices, imputation provenance, holdouts and previous anomaly/KS results remain unchanged; numerical tolerances are declared.
- External before/after verification confirms all **72 earlier source cells/IDs**, all **eight earlier PNGs**, Stage 02 aggregate/per-feature scores/masks/splits/settings/MICE draws and all Stage 03 thresholds/flags/Jaccard/KS/treatment results reproduce exactly. Only runtimes and OS-memory observations refresh. kNN10 Macro NRMSE remains **0.6763300629944509**, MICE raw RMSE **12463.419984895585**; its **912 support violations** remain documented without clipping/model changes.
- A final snapshot containing **no data directory/CSV** builds all **five Jupyter Book pages** from saved outputs without `--execute`. Headless Chrome verifies 69-row input/parameter audits, all 414 summary rows, six overview/Levene rows, seven new check rows and Sections 28–36. All **11 figures** load, **20 KaTeX expressions** have zero errors, document width stays within the viewport and all five homepage progress/navigation links return local HTTP 200. Formulas/tables and all three new violin figures are visually inspected; violin font sizes and compact Levene display were improved after browser review.
- The execution launcher logs a Jupyter TCP-transport notice outside notebook outputs; the build logs an existing Node `url.parse` deprecation notice. Neither is a statistical-cell warning or execution/build failure. No dependency/kernel configuration/deployment workflow is altered to suppress them. Public GitHub Pages status is separate and is not changed or newly verified.

Raw CSV SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. All ten protected-file hashes match the initial snapshot. Only the preprocessing notebook, tabular index, book homepage, this audit and relevant README progress text change. Navigation/setup remain intact. No new dependency/module, Encoding/Feature Selection/rebalancing/model experiment, raw/processed data export, commit, push or PR is added.

| Stage 04 requirement | Status | Evidence / scope |
|---|---|---|
| Min-Max | PASS | Explicit [0,1], stored training extrema, range/incoming-bound fixtures |
| Z-score Standardization | PASS | Independent fit, ddof 0, verified mean/SD/parameters |
| Robust Scaling | PASS | Explicit median/IQR settings, verified centers/scales and degenerate fixtures |
| Quantile Uniform | PASS | Full training population, fixed 1000 quantiles/seed, bounds/ties/repeat |
| Quantile Normal | PASS | Same knots/settings, finite tails, actual target-deviation analysis |
| Controlled comparison | PASS | Five same-population/scope fits plus original reference; all 414 rows |
| Violin visualization | PASS | Six prespecified features, provenance separation, independent axes, visual inspection |
| Variance diagnostics and justified Levene treatment | PASS | Focused observed-BMI groups, W/p stored, affine invariance and calibration limits |
| Statistical interpretation | PASS | No invalid paired variance test, automatic Gaussianity, p-based winner or predictive claim |
| Reproducibility | PASS | 44-cell fresh Run All, 34 notebook check groups, 5 unit tests, previous-stage/raw integrity |
| Jupyter Book presentation | PASS | CSV-free build, complete outputs, browser/math/link/figure checks |

**Stage 04 Scaling is complete for the requested controlled training-only comparison, with no identified correctness/execution blocker before Stage 05 Categorical Encoding.** Feature Selection and later stages remain pending; a final predictive pipeline is not validated. Source/temporal eligibility, dependence, imputation uncertainty, nonlinear information loss and downstream model-dependent selection remain scientific limitations, not evidence of overall 100% project completion.

## Historical Stage 03 handoff — completed Outlier Detection & Treatment

Starting HEAD: `a1be75cbe6543bf1fc813996c7eb91d013568fa3`; initial working tree clean. The [complete official assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) was retrieved with HTTP 200 and read before implementation, including technical/reporting/grading sections. Current HTML SHA-256 is `8d2a4a6e79902495d8f13e50530baf78433059b9620a05a7956298defa391720`: the raw page changed, while its normalized Outlier Detection & Treatment requirement paragraph matches the earlier cached page. The [official competition dictionary](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data) and installed sklearn/SciPy API documentation were also reviewed. BMI's documented post-metastatic timing and unresolved contextual periods/units/dictionary conflicts remain limitations; reconstruction eligibility does not establish prospective eligibility.

### Preservation and experimental scope

The existing preprocessing notebook is extended from 52 to **72 cells / 34 executed code cells**, appending zero-based cells 52–71, Sections 20–27. All preceding 52 cell sources, IDs and order are unchanged. Review found **no genuine blocking Part 1 bug**: observed-only linear quartiles, 1.5-IQR strict fences, population SD, strict |z|>3, NaN/degeneracy handling and aligned ANY-feature aggregation are correct. A high IQR row rate is not itself a defect. Historical Part 1 pending-work statements below and in Sections 16–19 are superseded by this completion record and Sections 20–27.

All nine configurations use the same **8,173 inner-training row identities**. Validation 2,081 and reserved 2,652 records remain unchanged and are not used for detector calibration. Target, patient ID, ZIP and nominal clinical codes are excluded from numerical inputs. IQR/Z-score retain originally observed values; the seven new configurations reuse the same existing complete **8173×69** train-conditioned matrix, including 5,717 explicitly marked kNN10 estimates. No new imputer/scaler is fitted, no feature is dropped, and no detector-specific scope or evaluation subsample is introduced. This observed-versus-completed distinction is explicit in the comparison, so it is not an algorithm-only accuracy experiment.

The complete representation contains **1,592 additional identical rows**, maximum multiplicity 11. Its 52 overlapping area-share coordinates, correlated contextual summaries, 69-dimensional Euclidean geometry, ZIP repetition, skewness and BMI imputation can influence neighborhoods/isolation. These are concrete interpretation risks, not proven causal explanations or reasons to silently alter the common scope. Detected thread pools and estimator jobs are limited to one; no full dense pairwise distance matrix is retained.

### Nine executed primary configurations

All rows below use N=8,173 and 69 features. Status PASS means successful execution and checks, not verified anomaly accuracy. IQR/Z-score use observed-only inputs; all other rows use shared kNN10/train-z inputs. No verified ground-truth error labels exist.

| Method | Primary parameters | Flagged N | Flagged % | Would retain N | Status |
|---|---|---:|---:|---:|---|
| IQR | linear quartiles; strict 1.5 IQR; ANY | 4953 | 60.6020 | 3220 | PASS |
| Z-score | observed mean/SD; ddof=0; strict absolute z>3; ANY | 1915 | 23.4308 | 6258 | PASS |
| Isolation Forest .01 | contamination=.01; 100 trees; max_samples=auto (256); seed=42 | 81 | 0.9911 | 8092 | PASS |
| Isolation Forest .05 | contamination=.05; remaining settings identical | 406 | 4.9676 | 7767 | PASS |
| Isolation Forest .10 | contamination=.10; remaining settings identical | 817 | 9.9963 | 7356 | PASS |
| LOF 10 | neighbors=10; contamination=auto; novelty=False; Euclidean | 1691 | 20.6901 | 6482 | PASS |
| LOF 20 | neighbors=20; same policy and distance | 1536 | 18.7936 | 6637 | PASS |
| LOF 50 | neighbors=50; same policy and distance | 1220 | 14.9272 | 6953 | PASS |
| DBSCAN | eps=6.892189118008946; min_samples=20 including self; Euclidean | 291 | 3.5605 | 7882 | PASS |

Fitted estimators, actual predictions, Boolean masks, parameters, runtime, IF raw scores/decisions and LOF negative scores remain inspectable in memory. IF label conversion is checked against decision<0 and score−offset; all three IF raw-score vectors are exactly identical. The nominal contamination settings threshold the same ranking; ties explain why proportions need not be exactly nominal. Standard 256-record IF tree subsampling is disclosed; fits/predictions cover the full training population. LOF actual neighborhood sizes are 10/20/50, auto offset is −1.5, score/label conversion is verified, and no fit warning was recorded. Scores are not calibrated probabilities and rates do not measure accuracy.

**DBSCAN calibration:** min_samples=20 was declared before observing noise. Explicit `kneighbors(X, n_neighbors=20)` includes query/self (unlike X=None), so its final distance is to the nineteenth other neighbor. Sorted rank and distance are normalized to [0,1]; eps is the distance at the first maximum of normalized rank minus distance. The selected zero-based rank is 7,821, normalized chord gap 0.655092. Training k-distance median=1.312577, 95th percentile=6.753287, 99th=10.567842, maximum=22.636713. This deterministic elbow is a heuristic sensitive to tails/density/geometry, not an objectively unique boundary. Flat/zero-distance fallbacks are declared and tested; none is needed for the real fit. No noise-rate tuning, sensitivity grid, fallback or subset execution is used.

Batched radius diagnostics find **6,127,787 directed neighborhood entries including self**, mean 749.76/max 2,579 neighbors. A conservative allocation estimate is **336.56 MiB**, explicitly not measured peak RSS; it passes the contemporaneous available-memory guard before the full fit. sklearn DBSCAN can still have quadratic neighborhood storage; chunked diagnostics are not a total RAM guarantee. One primary fit produces **16 non-noise clusters and 291 noise candidates (3.5605%)**, neither all-noise nor no-noise. Cluster labels/counts, core count and runtime are saved as aggregate outputs. Noise does not establish erroneous observations.

### Agreement and hypothetical removal

The notebook provides the complete **9×9 Jaccard matrix**, annotated heatmap, intersection/union count matrices and all **36 unique pairs** in memory. Arithmetic uses aligned Boolean masks/int64 counts and is checked independently with sets of actual training-row identities. Symmetry and nonempty diagonals are verified; empty/empty is undefined NaN, empty/nonempty is zero.

| Pair | Intersection N | Union N | Jaccard |
|---|---:|---:|---:|
| IF .05 / IF .10 — highest | 406 | 817 | 0.496940 |
| IQR / Z-score | 1915 | 4953 | 0.386634 |
| LOF 10 / LOF 20 | 889 | 2338 | 0.380240 |
| IQR / IF .01 — lowest | 81 | 4953 | 0.016354 |
| IF .01 / LOF 10 | 36 | 1736 | 0.020737 |
| IF .01 / LOF 50 | 31 | 1270 | 0.024409 |

The lowest-ratio pair still contains **all 81 IF .01 flags within IQR's 4,953**: low Jaccard can reflect unequal set sizes, not disjoint decisions. IF threshold nesting also limits the meaning of its agreement. Agreement is not correctness and does not select treatment.

Nine independent hypothetical retained subsets are created from the original observed numerical training frame, preserving indices/columns/known values/natural NaNs. Removal policies are not cumulative. The composition table reports all original/removed/retained counts, retention%, ZIP loss and BMI/all-cell missingness. IQR would lose **319/443 ZIP groups**, retaining 3,220 records from 124 ZIP groups. Z-score would lose 180 groups; DBSCAN would lose 52. Under LOF10 removal, observed BMI count falls from 2,531 to 1,586 and missingness rises from **69.0322% to 75.5322%**. These geographic/measurement selection changes argue against automatic deletion without validated benefit; no causal attribution to a particular source of geometry is asserted.

### Observed-value KS distribution impact

All **9×69=621** comparisons have sufficient finite observed support; none is unavailable and none produces numerical-zero/underflow p. Each result records policy, feature/semantic role, original/retained observed N, D, nominal p and validity/computation status in the expandable full table. Natural NaNs are dropped independently; no imputed value enters KS. `ks_2samp(alternative="two-sided", method="asymp")` is fixed for computationally practical large comparisons. Insufficient/nonfinite-support and zero/underflow handling are explicit and tested where relevant.

| Hypothetical removal | Features evaluated | Median KS D | Maximum KS D | Largest-shift feature |
|---|---:|---:|---:|---|
| IQR | 69 | 0.157277 | 0.243606 | education_less_highschool — area share |
| Z-score | 69 | 0.044664 | 0.075565 | rent_burden — contextual summary |
| IF .01 | 69 | 0.003530 | 0.007267 | income_household_75_to_100 — area share |
| IF .05 | 69 | 0.013548 | 0.033769 | income_household_75_to_100 — area share |
| IF .10 | 69 | 0.025702 | 0.053237 | income_household_75_to_100 — area share |
| LOF 10 | 69 | 0.009636 | 0.067298 | bmi — individual measure |
| LOF 20 | 69 | 0.012187 | 0.048877 | bmi — individual measure |
| LOF 50 | 69 | 0.020538 | 0.039516 | income_household_35_to_50 — area share |
| DBSCAN | 69 | 0.007903 | 0.015522 | income_household_75_to_100 — area share |

For the largest IQR shift, nominal p=**3.5430123916142145e−121**. This is not calibrated evidence of formal significance: retained observations are selected subsets of the original sample, and ZIP repetition/ties further violate classical independent-continuous-sample assumptions. **D is the primary descriptive measure.** No significance classification, multiple-testing correction, causal conclusion or p-based policy selection is made. Small D does not imply better data quality or predictive benefit. BMI/density ECDFs and illustrative policies were declared before outcomes; all features/policies remain in the full analysis.

### Treatment decision and remaining limits

**Adopted recommendation: preserve all original observations and retain all nine anomaly flags for investigation; automatic deletion=False.** Detection and hypothetical-removal distribution-impact evaluation are completed, and the conservative keep-all policy is explicitly selected. No verified anomaly truth, physical impossibility review or downstream benefit supports permanent deletion. IQR's sample/ZIP losses and LOF's BMI composition shift reinforce this caution; the recommendation is not a lowest-rate/Jaccard/p-value winner. Candidate subsets exist only in memory; no cleaned patient dataset is exported and neither holdout is removed or refitted.

A final predictive pipeline remains future work: establish feature timestamps/units/clinical eligibility, fit appropriate transformations and detector policies inside development folds, respect training-versus-novelty APIs, test geographic/sample-selection consequences and predictive outcomes, then assess the reserve after choices are fixed. Unknown contextual periods, post-metastatic BMI, overlapping ZIP features, high missingness and imputation uncertainty remain scientific limits. Statistical rarity does not prove clinical/data-entry error.

### Execution, correctness and publication verification

- Fresh `.venv` kernel Restart / Run All executes all **34 code cells sequentially**, with saved actual outputs and no exception/stderr; notebook JSON/schema, cell IDs/uniqueness and structure validate. There are **27 passing notebook check groups**: 14 prior imputation, 6 Part 1 and 7 new verification groups.
- New independent fixtures verify actual IF/LOF/DBSCAN label conversion and isolated noise, Jaccard identical/disjoint/partial/empty cases and invalid input, known KS D=.5/1, independent NaN dropping/unavailable support, nonmutating row filtering, and deterministic elbow/flat/zero-distance rules. Real-data checks verify all masks/predictions/counts, 36 independent set overlaps, KS bounds including the nested-mixture bound, full-data fixed-seed IF/fixed-order LOF repeats, protected-input exclusion and input/raw/holdout integrity.
- All **five existing unit tests** pass without skips. Before/after comparison confirms exact equality of old sources/IDs, Stage 02 scores/per-feature matrices/masks/splits/settings/draw statistics, Part 1 thresholds/masks/counts and all four previous PNGs. Only runtimes/OS-memory snapshots refresh. kNN10 Macro NRMSE remains **0.6763300629944509**; MICE raw RMSE remains **12463.419984895585** and its **912 draw-cell support violations** remain documented, without clipping/model changes.
- A source snapshot with **no data directory or CSV** builds all **five Jupyter Book pages** from saved outputs without `--execute`. Headless Chrome verifies both original seven-row imputation comparisons, all 69-row tables, nine primary detector/composition/KS-summary rows, full 621-row KS output, 9×9 matrix, seven new check rows, all eight new headings, **eight loaded figures and 15 KaTeX expressions with zero errors**. Tables/formulas/heatmap/plots are visually inspected; four homepage progress/navigation links return local HTTP 200. A Node `url.parse` deprecation warning does not prevent build. This is local publication evidence; remote deployment is not changed or newly verified.
- Raw CSV SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. All ten protected-file hashes match the initial snapshot. No private row-level patient table/ID, raw CSV or retained dataset is exposed in saved outputs or added to Git.

Only `book/tabular/02_preprocessing.ipynb`, `book/tabular/index.md`, `book/index.md`, this audit and the relevant README progress section change. Setup/navigation and deployment workflow remain intact. No dependency/module, separate Scaling/encoding/selection experiment, classifier, commit, push or PR is added.

| Stage 03 requirement | Status | Evidence / remaining scientific limitation |
|---|---|---|
| IQR | PASS | All 69 observed-only features; unchanged verified fences/flags |
| Z-score | PASS | All 69; unchanged ddof 0 and strict threshold |
| Isolation Forest .01/.05/.10 | PASS | All three full-population fits, stored scores/labels, reproducibility |
| LOF 10/20/50 | PASS | All three full-population fits; explicit auto policy and actual k |
| DBSCAN | PASS | One full fit; training-only documented eps/min_samples; memory guard |
| Detection-rate comparison | PASS | Exactly nine same-index primary rows, counts/rates/scope/retained/status |
| Jaccard overlap comparison | PASS | Full matrix/counts/heatmap; 36 pairs; synthetic and independent real checks |
| KS distributional analysis | PASS | 621/621 observed-value comparisons, D/nominal-p validity limits, ECDFs |
| Treatment interpretation | PASS | Independent removal comparisons, composition consequences, explicit keep-all adoption |
| Notebook reproducibility | PASS | Fresh sequential Run All, 27 check groups, 5 unit tests, preserved prior experiment |
| Jupyter Book presentation | PASS | CSV-free 5-page build, browser/visual checks, saved outputs |

**Stage 03 is complete for the requested retrospective training-set scope and has no identified execution/analysis blocker before Stage 04 Scaling.** This is not a claim of 100% overall rubric marks, prospective clinical validity, public deployment or predictive improvement. Scaling is still a separate controlled experiment; scientific eligibility/dependence limits carry forward rather than disappearing after this stage.

## Historical Stage 03 — Part 1 of 3: IQR and Z-score

Starting HEAD: `ae2d0dc4b598825861b2500d0bc278d9a297ace5`; initial working tree clean. The replacement attachment is identical to the earlier Part 1 request. Source/rubric review was performed before implementation; official HTML returned HTTP 200 with unchanged SHA-256 `2cca63ea7b93788b4ae981e51ff92765d9e478d6c4d3469fa7458299a8d3dc38`. The named IQR/Z-score requirements are implemented here; this is **not full Outlier Detection & Treatment completion**. Earlier sections below record their dated Stage 01/02 handoffs.

### Scope, numerical eligibility and shared preparation

- Appended zero-based cells 41–51, Sections 16–19, to the existing preprocessing notebook. It now has 52 cells / 24 code cells. All 41 previous sources, IDs/order and execution logic remain unchanged; no helper module or dependency added. The two small notebook-local detector functions are reused in independent correctness fixtures.
- All 69 numerical candidates audited and eligible for both IQR and Z-score. No real training feature has zero IQR, zero SD, insufficient observed support or a nonfinite observed value, so no feature is excluded. The audit records dtype, semantic role/timing caveat, observed/missing N and %, unique N, constant/zero conditions, training skewness and eligibility. Descriptive |skew|>1 is not an exclusion or outlier threshold. Known overlapping/complementary shares are retained, with aggregation caveats; no correlation or hypothesis-test analysis is added.
- Reused actual Stage 02 indices: train 8,173, validation 2,081, reserved 2,652; thresholds are fitted only to originally observed train values. Target/ID/ZIP/nominal clinical codes are excluded from numerical inputs. Both holdouts are only hashed for integrity and are not used for threshold estimation, detector choice or new preparation.
- IQR uses pandas linear quartiles, multiplier 1.5 and strict outside-fence comparisons. The declared minimum is 4 observations with positive finite IQR; zero/nonpositive IQR is explicitly NOT EVALUATED, not interpreted as evidence that every non-modal value is anomalous. Z-score uses observed train mean/population SD (ddof 0), minimum 2 observations, positive finite SD and strict |z|>3. These support minima are implementation conventions, not official sample-size rules. Unsupported feature flags remain Boolean false with unavailable detection rates and explicit exception notes. NaN itself is never flagged or filled for these univariate detectors.
- `outlier_train_original` remains immutable by convention, verified against its checksum and source values. A separate full 8173×69 matrix for Part 2 reuses the existing train-fitted 69-feature kNN10 and StandardScaler, with no new fit or detector-specific subsets. All 5,717 natural training gaps are marked in `outlier_common_imputed_mask`; original observed cells are retained exactly. Complete raw-unit and train-conditioned views are finite and keep row/column order. Preparation took 2.006s; the dense train×train distance upper bound is 509.63 MiB, using the existing 128 MiB chunk budget (not a total RAM cap). These matrices are not used by IQR/Z-score or scored by a multivariate detector. kNN10 is a justified reconstruction candidate, not a proven optimal anomaly-detection imputer.

### Actual detection results

| Method | Eligible features | Training N | Flagged records N | Flagged records % | Would retain N | Flagged feature-values N |
|---|---:|---:|---:|---:|---:|---:|
| IQR | 69 | 8173 | 4953 | 60.6020 | 3220 | 15378 |
| Z-score | 69 | 8173 | 1915 | 23.4308 | 6258 | 4404 |

Row rates use all 8,173 training records and the same ANY-eligible-observed-feature rule. Would-retain values are arithmetic candidate-policy counts only; no records are removed, reduced datasets created or completed patient rows exported. Feature percentages use each feature's originally observed N, not the row-rate denominator. Complete 69-row audit and fitted-statistics/results tables are expandable with capped scroll regions in the notebook. Selected feature results:

| Training feature | Observed N | IQR flagged N | IQR % observed | Z-score flagged N | Z-score % observed |
|---|---:|---:|---:|---:|---:|
| patient_age | 8173 | 34 | 0.4160 | 10 | 0.1224 |
| bmi | 2531 | 2 | 0.0790 | 2 | 0.0790 |
| race_asian | 8173 | 928 | 11.3545 | 117 | 1.4315 |
| farmer | 8173 | 728 | 8.9074 | 173 | 2.1167 |
| Ozone | 8148 | 703 | 8.6279 | 0 | 0.0000 |
| race_pacific | 8173 | 591 | 7.2311 | 35 | 0.4282 |
| density | 8173 | 576 | 7.0476 | 142 | 1.7374 |
| limited_english | 8173 | 293 | 3.5850 | 293 | 3.5850 |
| race_multiple | 8173 | 193 | 2.3614 | 193 | 2.3614 |
| health_uninsured | 8173 | 445 | 5.4448 | 184 | 2.2513 |

Bounded area shares contribute 11,765/15,378 IQR flagged feature-values and 3,655/4,404 Z-score flagged feature-values, across 52 columns. Other area summaries contribute 2,387/693; annual air context 1,190/44; individual age/BMI 36/12. These counts reflect both group size and repeated contextual values, not independent errors. Maximum triggered features per record are 20 (IQR) and 16 (Z-score).

ANY over 69 eligible features can flag many records despite modest marginal rates; correlated/overlapping fields repeat triggers and frequent ZIP groups receive more patient-record weight. `race_pacific` training skewness=20.22, IQR 7.2311% versus Z 0.4282%, illustrates different tail sensitivity without proving its cause. Ozone is eligible for both methods despite 703 IQR flags and 0 Z flags. Neither count is a quality/accuracy score. Extremes may be legitimate; source/timing uncertainty and missing BMI remain limitations. No ground-truth outlier labels, Gaussian calibration, universal superiority or final removal benefit is claimed.

### Reusable outputs and verification

The notebook preserves `outlier_train_original`, `outlier_feature_audit`, `outlier_feature_summary`, `outlier_common_train_raw`, `outlier_common_train_z`, natural/imputed masks, `iqr_thresholds`, `zscore_parameters`, `outlier_z_scores`, both feature masks, both observation flags, per-row trigger counts and `outlier_comparison`. All row-level outputs share `train_index`. Two new aggregate figures show highest marginal flag rates and the trigger-count distribution; no patient IDs or row-level records are displayed.

A fresh `.venv` Restart Kernel / Run All completes all 24 code cells in order with saved real outputs and no exception/stderr. Six new check groups pass, in addition to all 14 pre-existing imputation checks:

- Independent IQR fixture: Q1=1, Q3=3, IQR=2, fences−2/6; boundary values retained, just-outside values flagged, NaN false, input unmodified.
- Independent Z-score fixture: 50 observed values with mean 0/population SD 1; ±3 retained and ±4 flagged; missing score stays NaN and index alignment is preserved.
- Degenerate fixtures: zero-IQR non-modal values are not silently flagged; constant/zero-SD, all-missing, insufficient and nonfinite-input cases are explicitly handled.
- Real-data Boolean/row-column alignment, missing-value exclusion and independent NumPy counts/ANY totals match pandas outputs; trigger-frequency distributions sum to the complete training population.
- Shared train-only preparation, finite complete matrices, exact known values, natural-gap provenance and absence of protected predictors are verified.
- Original numerical training frame, full validation/reserved frames, source schema and raw CSV remain unchanged.

All five existing project unit tests pass without skips. Stage 01 is byte-identical. Original six-feature and joint 69-feature imputation scores, per-feature matrices, masks, splits, parameters and draw statistics reproduce exactly, including kNN10 Macro NRMSE 0.6763300629944509 and the 912 MICE support-violation limitation. Both pre-existing imputation PNGs are byte-identical. Execution timings refresh; historical benchmark timings below are retained.

The final CSV-free source snapshot builds all five book pages from saved outputs without --execute or a data directory. Headless Chrome verifies Sections 16–19, both 69-row outlier tables, the 2-row comparison, six new check rows, four total loaded charts, 11 KaTeX expressions and zero rendering errors. The new tables, formulas and figures were visually inspected. This is local rendering evidence; no deployment setting/workflow or remote state is changed.

Raw CSV SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. All 12 protected file hashes match the initial snapshot. Only the preprocessing notebook, tabular index and this audit change. No commit/push/PR or new stage beyond this Part 1 is introduced.

| Stage 03 requirement | Status | Evidence / remaining work |
|---|---|---|
| Data preparation / 69-feature observed-value audit | PASS | Full training scope, leakage guards, semantic/support/degeneracy audit |
| IQR detection and feature/row counts/rates | PASS | All 69; fixed 1.5 fences; strict boundaries; missing/zero-IQR checks |
| Z-score detection and feature/row counts/rates | PASS | All 69; ddof 0; strict >3; zero/invalid-SD checks |
| Reusable common matrices and same-index flags | PASS | 8173×69 finite preparation; 5,717 estimated cells marked; exact known cells |
| Synthetic/real verification and local publication | PASS | 24-cell Run All; 20 total notebook check groups; 5 unit tests; CSV-free build/browser |
| Isolation Forest / LOF / DBSCAN | NOT IMPLEMENTED | Part 2; no fitting/scoring in this change |
| Jaccard and KS distribution-impact comparisons | NOT IMPLEMENTED | Part 3; no overlap statistic or KS test computed |
| Final treatment selection or removal | NOT IMPLEMENTED | Requires subsequent comparisons; no rows removed |
| Whole Stage 03 completion | PARTIAL | Only Part 1 of 3 is complete |

**Part 1 is technically complete, with no execution/coverage blocker to Part 2.** Subsequent methods can reuse the documented train-only matrices and aligned flags after declaring the common representation. Retain caveats about imputation geometry, patient weighting/ZIP dependence, source/temporal eligibility and unknown outlier truth. A flag alone does not justify deletion.

## Final targeted reproducibility and homepage fix — 26 October 2026

Starting HEAD: `8805ad2c883fe3fca6e515eb8a080109989b56e2`; initial working tree clean. Only notebook source cells 26 (explanation) and 27 (eligibility audit) change. Cell 27 no longer imports JSON, reads the EDA notebook, extracts saved HTML, calls `next(...)` on outputs, or annotates strong-pair membership. Eligibility criteria, semantic/timing explanations and all 69 included features are unchanged. No correlation calculation or module replaces the removed annotation.

A cleared-output EDA fixture was supplied through a temporary read mock, without changing the real EDA file. Negative control: the previous cell raises `StopIteration`. Fixed cell: zero EDA reads, all 69 features included, and the eligibility table matches the previous table after removing only that annotation. All 41 cell IDs/order are preserved. Fresh `.venv` Run All executes all 19 code cells with real saved outputs and no exception/stderr; all 14 existing notebook check groups and all five project unit tests pass.

Before/after comparison against the starting notebook confirms exact equality of all seven raw/Macro RMSE results, both scopes' per-feature scores, split diagnostics, mask counts/hashes, seeds/settings and MICE draw metrics. kNN10 Macro NRMSE remains `0.6763300629944509`; MICE raw RMSE remains `12463.419984895585`; 14,181 observed-cell masks and 301/304/307 out-of-range MICE predictions (912 draw-cell violations) remain. Both chart PNGs are byte-identical. Runtime and OS-memory observations are remeasured; the coverage handoff below retains its historical timings. No clipping, retuning or experimental extension.

`book/index.md` now records completed EDA and completed 69-feature/seven-configuration numerical imputation with RMSE comparison, while later preprocessing and text remain future work. It links directly to the tabular index and both existing notebooks; setup/download instructions and the site structure are preserved. A new CSV-free saved-output build produces five pages. Browser checks confirm all three homepage links return local HTTP 200, the stale pending-experiments claim is absent, two comparison scopes and all 69-row tables render, both charts load, and eight KaTeX expressions have zero errors.

Public deployment is checked separately: the homepage and EDA/imputation URLs return HTTP 404; the repository API reports `has_pages=false`, and the Pages endpoint returns 404. The [workflow for commit 8805ad2](https://github.com/hungstupid/data-mining-preprocessing/actions/runs/40295413584) failed at **Configure Pages**; build/upload/deploy were skipped. Its log says the Pages site was not found and requests Pages enabled with GitHub Actions as the source. Thus the public 404 is an unconfigured Pages site, not evidence of a notebook execution/build failure. Publishing requires repository Pages setup and a subsequent deployment; no settings/workflow/remote changes are made here.

| Check | Status | Remaining blocker |
|---|---|---|
| EDA-output dependency removal and absent-output regression | PASS | None |
| Notebook structure, full Run All and unchanged numerical experiment | PASS | None; 912 MICE support violations remain an explicit modeling limitation |
| Homepage progress/links and local static rendering | PASS | None |
| Raw/EDA integrity and restricted file scope | PASS | Raw CSV and EDA byte-identical; no new dependency/module; no commit/push/PR |
| Existing GitHub Pages deployment | FAIL | Pages is not enabled/configured; owner setup required before publication |

## Numerical coverage handoff before the targeted fix — 26 October 2026

Reference/starting HEAD: `ac8f7bb9e0adbf1e79abac8e9ea93d0a1efbac93`; working tree clean before this task. This section records the numerical coverage handoff before the targeted fix above. The original six-feature handoff below remains a historical record, including its measured timings. The [official assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) was read again (HTTP 200; HTML SHA-256 `2cca63ea7b93788b4ae981e51ff92765d9e478d6c4d3469fa7458299a8d3dc38`). **All-69 coverage is our completeness extension, not a literal all-69 rubric requirement.**

### Coverage and eligibility

- Existing notebook extended, not rewritten: 41 cells / 19 code cells. All original 26 cell IDs/order and all original code sources remain. Sections 1–9 are the original representative scope; Sections 10–15 are the joint expanded scope. No extra product helper module, dependency, classifier or later-stage experiment.
- All **69/69 numerical candidates** audited and included in one common predictor matrix for all seven configurations. **Zero exclusions, zero features missing any method, no group-wise fallback and no row subsampling.** All 63 candidates outside the original scope are now evaluated; inclusion was not selected by RMSE. Original score fields/per-feature values/mask/figure reproduce exactly; only run timings refresh.
- Cell27 gives the complete 69-row eligibility table: semantic role, missing%, observed N, unique N, training support, eligibility and reasons. Rules declared first: finite measurements; train count>=2, train unique>=2 and SD>0; validation observed N>=10 to permit a nonzero 10% floor mask. These are feasibility minima, not power guarantees. The actual minimum pairwise training support is 2,526. Correlation/skewness are diagnostics, not exclusions; no EDA-output annotations are needed for eligibility.
- Dictionary-backed broad roles distinguish two individual measures, three annual air measures,52 bounded population/household shares,11 other contextual summaries/ratios, and the 1 contextual numerical column with conflicting meaning (`poverty`). `rent_burden` is rent/income expressed as a percentage, so no arbitrary <=100 bound is imposed. `poverty` is a literal numerical reconstruction target with its meaning and bounds unverified, not silently asserted to be a poverty rate. `widowed` wording is inconsistent in the indexed dictionary. The [official dictionary](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data) was rechecked; no field is approved for an earlier clinical baseline by this reconstruction experiment.
- BMI remains documented post-metastatic. Target/ID/ZIP and nominal diagnosis/treatment fields never enter numerical fit, distance or score matrices. Context reference periods, units where unresolved, independent sampling and prospective availability remain limitations.

### One common expanded experiment and actual feasibility

Same ZIP-disjoint rows/seeds 42/43: train 8,173/443 ZIP, validation 2,081/148 ZIP, reserve 2,652/148 ZIP. No row/ID/ZIP overlap. The reserve is not fitted/imputed/scored for method selection; earlier full-file EDA exposure is disclosed. All training rows and all 69 included columns are used. The ordered69-column matrix has its own deterministic seed 2024 mask, SHA-256 `c9f042a41bed1b8ca6bc6223dd0eeb773886e0e3c2457643d7c8574fde438664`. **14,181/142,008 eligible observed validation cells** are masked; per-feature counts/rates and natural gaps are printed in cell 29. Rates range9.8592%–10% because of flooring. Every method/draw uses identical positions within this scope; do not compare aggregate errors across the 6- and69-column matrices as one controlled experiment.

Train-only StandardScaler conditions kNN/MICE and provides observed train SD (ddof0) for the declared equal-feature Macro NRMSE. Completions are scored in original units. Scaler means/SD/sample counts and Simple/MICE initialization statistics are verified against training only. Runtime includes fit/transform/inverse units; shared conditioning, feasibility pilot and correctness refit are separate.

Preflight uses the complete training data:2,526 complete cases; pairwise observed N 2,526–8,173; complete-case correlation rank 67/69, condition 6.29e16. This dimensionless diagnostic is neither a Little test nor the fitted conditional-model covariance. The default BayesianRidge shrinkage is retained, not tuned to force a PASS. No correlated feature is removed. All 2,070 fitted conditional-model covariance matrices in the three scored MICE draws are finite.

Training float64 matrix 4.30 MiB; one dense validation×train distance array 129.76 MiB; kNN working_memory128 MiB provides chunking, not a total RAM cap. The estimated conditional coefficient-covariance storage across three draws is73.03 MiB, excluding other allocations. Host physical RAM 8 GiB; OS free+inactive+speculative snapshot≈1.23 GiB. Detected thread pools are limited to one. An unscored full-population one-round69-model pilot takes 1.400s. The actual scored MICE experiment fits690 models per draw,2,070 total, in 38.320s; the separate first-seed repeat takes 12.589s. Both full69-feature kNN and full69-feature MICE are demonstrated feasible; no fallback is invoked.

### Executed expanded results

| Method | Parameters | Masked / reconstructed N | Raw pooled RMSE | Macro NRMSE | Fit + transform (s) | Status |
|---|---|---:|---:|---:|---:|---|
| Mean | training mean | 14181 / 14181 | 36213.2867 | 1.06377 | 0.0032 | PASS |
| Median | training median | 14181 / 14181 | 38163.5466 | 1.08172 | 0.0346 | PASS |
| Mode | training mode | 14181 / 14181 | 73213.8081 | 1.55649 | 0.0253 | PASS |
| kNN (k=3) | k=3; uniform; train z | 14181 / 14181 | 17657.8528 | 0.70408 | 1.4917 | PASS |
| kNN (k=5) | k=5; uniform; train z | 14181 / 14181 | 16829.0707 | 0.69521 | 2.0618 | PASS |
| kNN (k=10) | k=10; uniform; train z | 14181 / 14181 | 16203.8687 | 0.67633 | 2.0536 | PASS |
| MICE (m=3) | posterior; m=3; 10 rounds | 14181 / 14181 | 12463.4200 | 0.86314 | 38.3205 | PASS |

MICE retains seeds 101/102/103, `sample_posterior=True`, ten rounds, `skip_complete=False`, all 68 other predictors per conditional model. Its row/per-feature values average draw-level scores, not completed values or Rubin-rule inference. Mean Macro NRMSE=0.86314; sample draw SD=0.00473; raw RMSE sample draw SD=345.9785. Three ten-round runs do not prove convergence or Gaussian/MAR calibration.

Declared winner is **kNN (k=10)** in the expanded scope; original winner is **kNN (k=10)** in its own scope. Winner labels agree, but aggregate errors from different feature matrices/masks are not effect estimates for adding features. Expanded raw RMSE instead favors **MICE (m=3)**. Training-SD normalization and equal-feature weights remain fixed. Large correlated share blocks receive multiple feature weights; no outcome-driven domain reweighting is added.

All 69×7 raw and training-SD-normalized per-feature results are in separate expandable, height-limited scroll tables (cell 35). Selected examples below are all from the expanded scope:

| Expanded feature | Mean RMSE | kNN10 RMSE | MICE mean-draw RMSE | Per-feature minimum |
|---|---:|---:|---:|---|
| patient_age | 13.48408 | 15.10391 | 18.38778 | Median |
| bmi | 4.91823 | 5.50606 | 7.68989 | Mean |
| home_value | 297953.98201 | 133683.26390 | 102947.25725 | MICE (m=3) |
| income_household_median | 28312.35905 | 7292.75514 | 4518.53145 | MICE (m=3) |
| education_college_or_above | 13.90865 | 5.34736 | 5.60648 | kNN (k=10) |
| race_pacific | 0.16337 | 0.15442 | 2.12267 | kNN (k=10) |
| PM25 | 1.55368 | 1.15269 | 1.44572 | kNN (k=10) |

Per-feature minima: kNN10=33, MICE=27, kNN5=3, kNN3=3, Mean=2, Median=1, Mode=0. These are diagnostics, not an implemented hybrid imputer. MICE's gains on large-unit context can favor raw RMSE while poor normalized reconstruction on some shares opposes it; for example race_pacific normalized RMSE is 3.43885 versus kNN10 0.25017. Mechanistic causes are not separately tested.

### Domain limits and categorical handoff

For each completed table,10,799 masked values are dictionary-supported bounded shares. MICE produces301/304/307 out-of-[0,100] predictions across the three draws (912 draw-cell violations, not 912 distinct patients or positions). No clipping or score repair is performed. All six other configurations have zero violations beyond floating-point roundoff; kNN5 has one strict boundary violation attributable to inversion roundoff. The diagnostic tolerance is32×machine-epsilon×100 and only distinguishes roundoff in flags, never alters scored values. Exact-zero inverse-transform comparisons use1e-12 numerical tolerances; the raw input/frame hashes remain exact. Numerical completion PASS does not certify bounded/joint/compositional validity or clinical adoption.

All 12 categorical/code/text fields are inventoried in cell 39. Natural gaps remain in race6,385; payer1,803; state51; each treatment field12,882; Region52; Division52. Eligible categorical mode/unknown handling is a downstream candidate; treatment absence/applicability and timing require review first. No nominal RMSE or encoding is performed, and the dataset is not claimed fully preprocessed.

### Requirement status and verification

| Requirement | Status | Actual evidence / boundary |
|---|---|---|
| Complete69-feature eligibility and coverage | PASS | All 69 accounted for and included; no hidden exclusions; source uncertainty flagged |
| Preserve original representative experiment | PASS | Original code/IDs/score fields/6×7 results/mask/PNG unchanged; original timings retained historically |
| Mean / Median / Mode | PASS | All 69 columns, same 14,181 positions, training statistics checked |
| kNN k=3 /5 /10 | PASS | All 69 columns and full training donor rows; train-only conditioning/inverse units |
| Full-scope MICE | PASS | Three posterior completions;690 models/draw; finite outputs/covariances; seed 101 repeat exact |
| Additional10% MCAR masking | PASS | Observed-only uniform floor-count mask per feature; natural gaps preserved; same mask within scope |
| Raw/per-feature/normalized scoring and selection | PASS | Separate scopes;7-row comparisons;69×7 raw and normalized tables; declared criterion retained |
| Train-only fit / no reserved selection / alignment | PASS | Same ZIP splits; train-statistic checks; reference/protected-predictor and shape guards |
| Bounded/joint validity and prospective adoption | PARTIAL |912 MICE support violations; no clipping; no joint/plausibility or earlier-baseline approval |
| Categorical missingness inventory | PASS | All 12 accounted for; handling remains downstream, not claimed implemented |
| Reproducibility / local publication / integrity | PASS | Fresh19-cell run,14 check groups, 5 existing unit tests, CSV-free build/browser; unchanged raw/EDA |
| Source-period/clinical definitions and timing | PARTIAL | Poverty/widowed conflicts, environmental periods/units and prediction anchors unresolved |
| Natural-mechanism identification / global MCAR | BLOCKED | Prior EDA inference limit unchanged; not required to compare explicitly artificial MCAR masks |
| Remote deployment / remaining preprocessing / whole project | NOT VERIFIED | No push/PR/deployment or later-stage experiment in this extension |

Fresh `.venv` Restart Kernel / Run All: all 19 code cells in order, real saved outputs, no saved exception or stderr. Nine original plus five expanded check groups pass. New checks independently verify raw sqrt(10)/Macro NRMSE=2 under unequal units, reject swapped columns, exactly reproduce full-scope seed 101 MICE, verify common mask/coverage/alignment/finite scores/known-value preservation, and recheck raw/frame/train/reference/protected-feature/reserve integrity. Five existing Little unit tests pass without skips; no new cohort hypothesis tests were run.

The final book builds all five pages in a new snapshot without any CSV/data directory and without --execute. Headless Chrome verifies two separate seven-row comparisons, all 69 eligibility/mask/raw-RMSE/normalized-RMSE rows, three expanded posterior draws, 12 categorical fields, two loaded charts, eight KaTeX expressions and zero math errors. Expandable69-row tables have capped scroll containers, and the main comparison fits the content width. Screenshots verify equations/table/figure presentation. This is local evidence only; public Pages status is not inferred.

Raw SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. All 11 protected file hashes match the starting snapshot, including dependencies, helper/tests, TOC, workflow and unrelated pages. No patient rows/completed data are exported. Changed product files are only 02 notebook,tabular index,README and this audit. No commit/push/PR or new dependency.

**Numerical Missing Value Imputation is sufficiently complete to proceed to Outlier Detection under the official rubric.** There is no missing numerical-method/coverage/execution blocker. Retain the retrospective scope and source/timing limits, categorical handoff, patient weighting/spatial dependence and the distinction between artificial observed-cell error and natural-gap validity. This does not approve all 69 as prospective predictors, make MICE domain-valid, complete the entire dataset or certify a grade.

## Original six-feature Stage 02 handoff — 26 October 2026

Starting HEAD: `1f4d16efd14d1fd2551d3fc8318b22022343fbce`; clean working tree at start. The official assignment was read again; its retrieved HTML SHA-256 is unchanged (`2cca63ea7b93788b4ae981e51ff92765d9e478d6c4d3469fa7458299a8d3dc38`). The current T1 status is **PASS for the explicitly scoped six-feature retrospective benchmark**. The dated EDA matrices below preserve their EDA-only handoff status; they do not override this new evidence. Required T2–T5 comparisons and mandatory part(b) remain unimplemented. No whole-project percentage or grade is claimed.

### Protocol and scope fixed before scoring

- New notebook: `book/tabular/02_preprocessing.ipynb`, 26 cells / 12 code cells, using the existing `.venv` kernel. No product helper module, dependency or framework added. EDA is byte-identical.
- Six fixed numerical columns: `patient_age`, `bmi`, `density`, `income_household_median`, `education_college_or_above`, `PM25`. Whole-file missing rates are respectively 0%, 69.4638%, 0.0077%, 0.0310%, 0.0077%, 0.2247%. These cover individual measurements, skewed context, monetary/percentage/environmental scales and BMI missingness. Complete exclusions/reasons are printed in cell 3: 63 other numerical candidates, 12 categorical/code/text fields, plus ID/target. No subset/seed selection based on scores; ranking does not generalize to all 69 candidates.
- Retrospective reconstruction only: post-metastatic BMI remains ineligible for an earlier baseline; treatment/diagnosis, target, ID and ZIP are excluded from imputation matrices. Source-period/unit gaps remain. The same source/temporal restrictions as EDA apply.
- Outer GroupShuffleSplit reserves 20% of ZIP groups, seed42; inner split holds out 25% of development ZIP groups, seed43. Actual partitions: train 8,173 rows/443 ZIP; validation 2,081/148; reserved 2,652/148. Every pair has zero row/ID/ZIP overlap. Target distribution is diagnostic only. All train rows are used; six-feature complete cases and minimum pairwise observed support both equal 2,526. EDA already saw the full file, so the reserve is post-EDA, not an untouched external test; it is not imputed/scored for selection.
- Only originally observed validation values receive artificial gaps: uniform fixed-count sampling without replacement per column, floor(10% of eligible), seed2024. Counts in feature order: 208/63/208/207/208/207, total1,101; BMI is 63/639=9.8592% because of flooring. Every method/draw uses the same mask, SHA-256 `d4e1ced320653122022edadea5bac1d443271af2fccfdd26efb7db5842c8e22e`. Natural NaNs remain; original frame/train/reference are unchanged. This construction does not identify natural MCAR/MAR/MNAR.
- Mean/Median/Mode fit raw training values. Mode tie rule is smallest value, checked explicitly. kNN uses uniform weights, nan_euclidean distance, k=3/5/10. Train-fitted NaN-aware StandardScaler conditions kNN/MICE; completions return to original units. Theoretical dense distance array is129.76MiB; sklearn working_memory128MiB chunks distances, with possible additional overhead. This is not a separate scaling comparison.
- MICE: installed sklearn1.9.1 experimental IterativeImputer, default BayesianRidge, sample_posterior=True, m=3 seeds101/102/103, ten rounds, skip_complete=False, all six predictors. Train-complete features must still have models for new validation gaps. Posterior mode does not early-stop; ten rounds does not establish convergence. Writable NumPy copies handle the actual pandas3/sklearn initialization compatibility failure found in the first run; subsequent fresh runs pass. Canonical columns/alignment are asserted around the array interface.
- Predeclared primary score: equal-feature mean(RMSE_j / observed training SD_j), ddof0. Raw pooled RMSE is required secondary evidence and mixes units. MICE aggregate/per-feature scores are means of draw-level scores; not RMSE of averaged imputations, and not Rubin-rule pooling. Exact ties follow fixed displayed order.

### Actual saved-output results

| Method | Parameters | Masked / reconstructed N | Raw RMSE | Macro NRMSE | Fit + transform (s) | Status |
|---|---|---:|---:|---:|---:|---|
| Mean | training mean | 1101 / 1101 | 10781.6565 | 1.08081 | 0.0016 | PASS |
| Median | training median | 1101 / 1101 | 10811.5381 | 1.09145 | 0.0037 | PASS |
| Mode | training mode | 1101 / 1101 | 11130.5714 | 1.65760 | 0.0036 | PASS |
| kNN (k=3) | k=3; uniform; train z | 1101 / 1101 | 7380.0639 | 1.00923 | 0.3751 | PASS |
| kNN (k=5) | k=5; uniform; train z | 1101 / 1101 | 7175.3082 | 0.96711 | 0.3510 | PASS |
| kNN (k=10) | k=10; uniform; train z | 1101 / 1101 | 7297.4831 | 0.95477 | 0.3632 | PASS |
| MICE (m=3) | posterior; m=3; 10 rounds | 1101 / 1101 | 8634.4763 | 1.20891 | 0.4134 | PASS |

Every count is per completed table; MICE has three tables with the same1,101 positions, not3,303 independent evaluation cells. Runtime includes fit+validation transform (and inverse transform when used), summed over all MICE draws; shared train-only conditioning took 0.0056s, separate from method runtime. Validation/reproducibility refits are excluded. These are single local timings, not stable performance estimates.

Per-feature RMSE in original units; MICE cells are mean draw-level RMSEs:

| Feature | Mean | Median | Mode | kNN 3 | kNN 5 | kNN 10 | MICE 3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| patient_age | 13.4841 | 13.4668 | 14.6776 | 18.0744 | 16.4652 | 15.7661 | 18.9878 |
| bmi | 4.9182 | 5.0480 | 5.3690 | 5.9009 | 5.4493 | 5.2355 | 7.5224 |
| density | 1569.7986 | 1600.0282 | 4460.5083 | 1509.9410 | 1480.7631 | 1509.9854 | 2123.4401 |
| income_household_median | 24815.4659 | 24882.5840 | 25277.5869 | 16952.9091 | 16481.4186 | 16761.6885 | 19799.1297 |
| education_college_or_above | 14.3479 | 14.3842 | 15.5266 | 8.2498 | 8.0519 | 7.9101 | 10.0400 |
| PM25 | 1.7613 | 1.7918 | 4.2674 | 1.8624 | 1.8705 | 1.8676 | 2.1833 |

Declared winner: **kNN (k=10)**, macroNRMSE0.95477, 11.66% lower than Mean. Raw RMSE instead favors kNN k=5; retain the predeclared normalized criterion. Per-feature minima: Median(age), Mean(BMI/PM25), kNN5(density/income), kNN10(education). These are diagnostics, not an implemented feature-specific pipeline.

MICE mean macroNRMSE=1.20891, sample draw SD=0.01853; raw RMSE sample draw SD=152.3062. Its primary score is worse than Mean here, so this point-reconstruction criterion does not justify its additional modeling effort. Posterior variation can increase pointwise squared error without invalidating multiple imputation's inferential purpose. Conditional-model mismatch/weak information are possible explanations, not separately tested causes. Context gains and competitive individual-variable simple baselines motivate feature-specific review later. Without an unscaled-kNN arm there is no estimated causal benefit from scaling.

### Verification and current requirement statuses

Fresh `.venv` Restart Kernel / Run All completes all12 code cells in order (counts1–12), with real outputs in every code cell, no saved exception or stderr. Nine focused check groups pass: synthetic mask determinism/value independence/floor counts/no natural-NaN ground truth; analytic masked-only RMSE; invalid-prediction rejection; natural-NaN rejection; train-only mean/scaler/ties/inverse units; synthetic posterior reproducibility; real first-seed posterior reproduction; common mask/train rows/alignment/finite completions/excluded predictors; raw/frame/train/reference integrity. Five existing Little unit tests also pass, with no skips. Scaler sample counts and fitted means/SDs and Simple/MICE initialization statistics agree with inner training only.

The CSV-free source snapshot builds five pages from saved outputs with the existing command (no --execute) and project subpath. Headless Chrome verifies the chapter navigation, five display equations/eight total KaTeX expressions with zero errors, seven comparison rows, six per-feature rows, three MICE draw rows, six mask-audit rows and one loaded chart. Table/formula/chart screenshots are visually checked; both result tables fit the book content width, with horizontal overflow protection for smaller windows. No browser dependency or deployment workflow change. Local rendering does not verify remote Actions/Pages publication. The existing root `book/index.md` still describes the original scaffold; it is outside the permitted file list and remains unchanged. Current stage descriptions and links are in the updated tabular index, README and navigation.

| Criterion | Status | Evidence / boundary |
|---|---|---|
| 1. Mean | PASS | SimpleImputer mean; train statistics checked;1,101 scored cells |
| 2. Median | PASS | SimpleImputer median; same columns/mask/training partition |
| 3. Mode | PASS | Numerical most_frequent baseline; tie audit and synthetic tie check |
| 4. kNN k=3 | PASS | All training donors; train-only conditioning; raw-unit scoring |
| 5. kNN k=5 | PASS | Same protocol; raw-RMSE minimum disclosed |
| 6. kNN k=10 | PASS | Same protocol; predeclared normalized-score minimum |
| 7. MICE | PASS | Three distinct posterior seeds; ten rounds; draw variation and real fixed-seed repeat |
| 8. Additional10% MCAR masking | PASS | Fixed floor count per observed validation feature;1,101 shared positions; no natural NaNs scored |
| 9. RMSE comparison | PASS | Seven-row raw/normalized/runtime/status table; six-feature table; counts and chart |
| 10. Justified selection | PASS | Primary criterion fixed first; conflicting raw ranking, per-feature results, cost and limits explained |
| 11. Reproducibility/report presentation | PASS | Fresh12-cell run; nine check groups; five unit tests; CSV-free five-page build/browser inspection |

Raw CSV SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`; EDA SHA-256 remains `bdd5c5c602dd213b831dd9a69e550b97bd87aea51f128014cf1065457471b1d0`. Source helper/validator/tests, dependency files, workflow and unrelated book pages match initial hashes. No patient rows/completed dataset exported; no CSV tracked; no commit/push/PR performed.

**Controlled Missing Value Imputation is complete and ready for independent code review within this scope.** Remaining scientific limits: one split/mask, six selected numerical features, patient weighting/shared and potentially spatially dependent context, observed-ground-truth selection versus natural gaps (especially BMI), linear/Gaussian unbounded MICE with only three draws/ten rounds, and unresolved prediction-time eligibility. No confidence intervals across masks/ZIP populations or natural-mechanism verdict are claimed. Later preprocessing/model stages and whole-project submission remain NOT VERIFIED; global MCAR inference remains BLOCKED as documented by EDA.

## Historical before-edit traceability matrix (initial 29-cell version)

| Rubric ID | Original Requirement | Mandatory/Optional | Stage | Existing Code Cell | Existing Output | Status | Required Fix |
|---|---|---|---|---|---|---|---|
| D1 | Tabular: >=10 attributes, >=10000 rows, numeric + categorical, >=5% missing in one attribute | Mandatory | Dataset | 3,5,7 | 12906x83; 69/12 semantic roles; BMI 69.46% missing | PASS | Add explicit rubric assertions; results already present |
| E1 | Each numerical: Shapiro n<=5000; D’Agostino–Pearson n>5000; p-value classification and scaling rationale | Mandatory | EDA | 12 | Only summaries/skewness/plots/IQR; no normality-test table | FAIL | All continuous features; full results; guarded validity; method guidance |
| E2 | Pearson and Spearman heatmaps; identify strong pairs such as absolute r>0.9; propose handling | Mandatory | EDA | 16 | Two 6-feature heatmaps; full Spearman top-10 only | PARTIAL | Both full matrices, full pair counts and union threshold-pair table |
| E3 | Missing-data matrix using missingno | Mandatory | EDA | 7 | Boolean seaborn matrix; missingno dependency installed but not called | FAIL | Call missingno.matrix for overview/focus; state sample and scope |
| E4 | Little MCAR test; explain MCAR/MAR/MNAR and conclusions | Mandatory | EDA | 8,22 | Patterns/Fisher indicators exist; no Little statistic or df | FAIL | Verified ML/EM implementation, justified scope, tests, assumptions/status |
| T1 | Mean, median, mode, kNN k={3,5,10}, MICE; add 10% MCAR mask per strategy; RMSE comparison and justified choice | Mandatory | Later tabular preprocessing | — | Not implemented by current EDA scope | NOT VERIFIED | Record exact future checklist; do not implement here |
| T2 | IQR and Z-score; IF contamination={.01,.05,.1}; LOF neighbors={10,20,50}; DBSCAN; rates/overlap/Jaccard; KS after removal | Mandatory | Later tabular preprocessing | 12 | IQR diagnostic only, no method comparison | PARTIAL | Keep diagnostic; implement comparisons later; clarify wording counts with instructor |
| T3 | Min-Max, Z-score, Robust Scaling, Quantile Transform uniform/normal; distribution visualization | Mandatory | Later tabular preprocessing | — | No transforms fitted | NOT VERIFIED | Record methods; Levene is optional wording |
| T4 | One-Hot, Ordinal, cross-validated Target Encoding, Binary for cardinality>20, Frequency; VIF checks | Mandatory | Later tabular preprocessing | 14 | Cardinality/support only | PARTIAL | Future fold-local comparison; VIF is not explained-variance ratio |
| T5 | ANOVA F, categorical chi-square, MI; RF/Gradient Boosting importance; RFE CV; PCA/t-SNE; UMAP if large | Mandatory/conditional | Later tabular preprocessing | — | No feature selection or embedding | NOT VERIFIED | Record methods; optional wording for 5-fold CV F1; grading still allocates selection/CV points |
| T6 | SMOTE, ADASYN, Random Under-sampling when imbalanced; untouched-by-resampling test; Precision/Recall/F1-macro/AUC-ROC | Advanced/bonus; condition: imbalance | Later tabular preprocessing | 3 | Balance observed; no resampling | PARTIAL | Do only if pursuing bonus; clarify imbalance applicability with instructor |
| B1 | Choose exactly one modality in part (b): image or text; text >=10000 samples and >=2 labels | Mandatory | Second modality | — | Text placeholder only; no selected dataset | FAIL | Part (b) is required, not optional; retain complete text checklist |
| B2 | Selected second-modality EDA, preprocessing and quantitative evaluation; advanced items marked separately | Mandatory + advanced | Second modality | — | Not implemented; outside this edit | NOT VERIFIED | Record full text branch and alternate image/time-series scopes |
| R1 | One public Jupyter Book on personal-repository GitHub Pages; submit its single URL on Moodle; stable until grading; oral defense | Mandatory | Publication/submission | — | Local saved-output build previously passed; remote current state not checked | PARTIAL | Rebuild without CSV; no push/settings changes; actual submission remains unverified |
| R2 | README: full name, student ID, data description, environment/build, public data/external links; preparation code in book; no raw data commit | Mandatory | Reproducibility | 1,3,27,28 | Environment/data links/checks present; student ID and executable download preparation absent | PARTIAL | Add guarded notebook download preparation; request identity; preserve raw bytes |
| R3 | Python, permitted libraries; numeric results printed and stored; notebook source; theory/code/analysis for each preprocessing technique | Mandatory | All stages | All | EDA saved outputs exist; future stages absent | PARTIAL | No unapproved MCAR packages; explain/test local statistical helper |
| G1 | Weights: part(a)30%, part(b)30%, code/book40%; advanced prose versus grading-table ambiguity | Mandatory grading context | Whole project | — | No previous rubric mapping | FAIL | Publish audit and exact future work; do not claim overall completion |

## Final EDA traceability matrix — 26 October 2026

Starting HEAD: `5464d6eb43e8ce2345d46f4a60e1dba5795f82e2`; working tree clean. The official page was retrieved/read directly (HTTP 200) after the web renderer failed. Its HTML SHA-256 remains `2cca63ea7b93788b4ae981e51ff92765d9e478d6c4d3469fa7458299a8d3dc38`. Only the three published tabular EDA groups are treated as compulsory; later feature-selection tests and other-modality requirements remain in the exact checklist below.

EDA notebook: 31 cells / 16 code cells. Indices below are zero-based, execution counts in parentheses. PASS is evidence for the stated scope, not a grade or claim of known natural missingness. Correctly reporting an unidentified mechanism satisfies the interpretation task; the separate BLOCKED row limits a cohort-wide inferential claim and does not require another EDA study before preprocessing.

| Rubric ID | Requirement | Stage | Cell / evidence | Status | Remaining limit / next action |
|---|---|---|---|---|---|
| D1 | Qualifying tabular dataset and semantic/integrity audit | Dataset | 3(2),5(3),7(4):12906x83,81 features,69 numerical/12 categorical-code-text, missingness gate met | PASS | Descriptive eligibility, not clinical provenance verification |
| E1 | Per-numerical Shapiro n<=5000 / D’Agostino n>5000; statistic/p/decision | EDA | 21–22(12):full69 rows;1 Shapiro/68 D’Agostino;69 reject,0 fail,0 untestable ;39 underflows with log(p) | PASS | iid/marginal reference; rejection is not departure magnitude |
| A2 | Explained scaling candidates grounded in distributions | EDA | 22(12):five feature/group rows use actual ranges, skewness and IQR flags | PASS | Compare Min-Max/Standard/Robust/Quantile later; no automatic choice or fit |
| E2 | Full Pearson/Spearman heatmaps, strong pairs, multicollinearity proposals | EDA | 25–26(14):both69x69;2346 unique pairs;12 Pearson/15 Spearman/17 union; full matrices/N, group summary and algebraic checks retained | PASS | Rank/VIF/representatives/regularization/PCA are future comparisons; no feature dropped |
| E3 | Missingno matrix | EDA | 7(4),10(6):focus250x8 seed42, overview12906x81; full key saved | PASS | Visual patterns do not identify mechanisms |
| E4a | Valid Little implementation and actual H0/H1/statistic/df/p/result | EDA | 11–12(7):Gaussian ML/EM, age/BMI, patterns8965/3941;D²3.50653408,df1,p.06112721;45 iterations; closed form/unit/reference checks | PASS | Fail to reject only under the working reference; helper/tests unchanged |
| E4b | Define and assess MCAR/MAR/MNAR with honest limits | EDA | 11,15–16(9):five-row/seven-column assessment; test result/descriptive evidence/hypotheses distinguished; MAR/MNAR explicitly not identifiable from observed data alone | PASS | Natural mechanism remains unidentified; imputation comparisons require documented assumptions |
| E4c | Justify scope; do not force a wider invalid test | Scope review | 13–14(8):measurement levels, pattern support, complete-case correlation rank/condition and repeated ZIP context screened; no extra p-values | PASS | Four-variable full rank is not a Gaussian/independence guarantee; broader calibrated inference not established |
| E4d | Establish calibrated MCAR for the entire cohort | Scientific inference limit | Only age/BMI tested; bounded/nonnormal variables, dependence and scope limitations remain | BLOCKED | No global MCAR or MAR/MNAR label claimed; this is not a prerequisite to compare preprocessing under explicit assumptions |
| S1 | Document temporal eligibility and dictionary coverage | Scientific validity | 0,4–5(3),16(9),28–29:post-metastatic BMI/treatment documented; source gaps retained | PARTIAL | Freeze supplied-table versus prospective prediction question, eligible inputs and post-EDA validation before model comparisons |
| P1 | Minimal EDA without optional hypothesis-test framework | Presentation | Eight cells implementing/presenting seven exploratory tests deleted; import, variables, assertions and live references removed; duplicate 6-variable, weighting, rare-example and phi outputs removed | PASS | No replacement test/framework introduced |
| R1a | Reproducible sequential notebook with saved real outputs | Reproducibility | All16 code cells run from fresh .venv;21 retained result arrays match baseline; final CSV/frame checks | PASS | No preprocessing/model fitted; raw data and frame preserved |
| R1b | Book renders tables/plots/formula without private CSV | Local publication | Four-page saved-output build; eight figures; full numerical tables; rendered math and formatted prose verified in browser | PASS | Local verification only; remote Actions/Pages not invoked |
| R2 | Source/README/data preparation instructions aligned | Reproducibility | README + tabular index remove live references to deleted tests; guarded acquisition preserved | PARTIAL | Cold authenticated Kaggle acquisition not executed |
| T1–T5 | Required imputation/outlier/scaling/encoding/selection experiments | Later preprocessing | Candidate methods/checklist preserved; no experiments implemented here | NOT VERIFIED | Exact grids, masking rates, metrics and CV requirements retained below |
| B1–B2 | Mandatory image/text part(b) | Separate project part | Placeholder only; outside this EDA change | NOT VERIFIED | Must still choose/complete a modality |
| R3 | Remote publication/Moodle/defense/whole-project completion | Submission | No commit/push/PR/remote change during this task | NOT VERIFIED | This audit closes EDA work, not the whole project |

### Final edits and method verification

- Deleted the complete seven-test group: two Mann–Whitney, two exploratory Chi-square, three Fisher and Holm; their four code/four Markdown cells, multipletests import, variables, assertions and live prose references are gone. This does not remove future ANOVA/Chi-square/MI selection or text-EDA Mann–Whitney requirements.
- Removed unused six-variable duplicate correlation calculations, top-Spearman alias, ZIP-weighting comparison, rare literal examples and phi heatmap. Cardinality/support, exact co-missing counts, broad patterns, both missingno views, full correlations and all three algebraic checks remain. The repeated-context scope check supports the grouped-validation conclusion without an extra weighting exercise.
- Moved the mechanism assessment after Little and expanded it to the requested seven columns: feature/group, missing%, evidence, MCAR assessment, plausible MAR/MNAR explanations, limitations, preprocessing implications. Five rows include BMI/race/payer/treatment/geography. All hypothetical MAR/MNAR explanations are unconfirmed; every row states **Not identifiable from observed data alone**. The controlled10% artificial MCAR-mask RMSE plan does not assert that natural missingness is MCAR.
- Little helper reviewed unchanged: observed masks define patterns; Gaussian EM updates expected sums/crossproducts and ML covariance; likelihood/convergence/positive covariance checked; statistic is the pattern-weighted mean quadratic;df=sum(observed dimensions per pattern)−p;chi-square survival yields p. The age/BMI result matches its analytic age-pattern reduction. Five existing unit tests pass; the independently documented airquality benchmark remains reference evidence.
- Primary two-variable inference: pattern sizes8965/3941, complete-case support3941, ML covariance min eigenvalue32.280713 and condition5.514068, EM45 iterations, D²3.50653407757,df1,p=.06112720890. Non-rejection is neither proof of MCAR nor a probability that H0 is true. All69 variables are not forced into a Gaussian test; categorical codes are never arbitrarily converted.
- Full source/saved-output review found the former Little equation was literal text in the exported AST. Changed Markdown delimiters to supported display math. Browser inspection also found generated Markdown prose displayed literal formatting; those display calls now emit basic HTML with the same computed values. No statistical formula, helper or publication pipeline changed.

### Final executed validation

- A fresh `.venv` kernel runs all 16 code cells in 31 valid notebook cells without error outputs or saved stderr. All 21 retained core numerical/result arrays match the previously validated baseline exactly, including NaN positions. Deleted test variables/imports are absent in the fresh kernel; no preprocessing fit/export calls were introduced.
- All five existing Little unit tests pass with no skips; helper/test bytes, dependency files, workflow and TOC are unchanged. Raw SHA-256 remains `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`, and frame values/index/dtypes/shape are preserved. Eight retained plot images are byte-identical to the base (only the redundant phi figure is removed).
- A CSV-free source snapshot builds all four pages from saved outputs. Exported data keeps all 69 normality rows, 17 strong pairs, all three 69×69 numerical matrices, five scaling rows, the five-by-seven mechanism table and seven findings. Browser verification confirms eight expandable detail blocks, opened matrices with 69 rows each, a rendered Little equation with zero KaTeX errors, and formatted generated prose outside code blocks. Formula/table screenshots were visually inspected. The new mathematical display fixes a real previously unrendered formula, not a statistical change.
- Only non-failing kernel TCP startup and Node DEP0169 toolchain warnings were observed outside the notebook ;39 p-value underflows remain explicitly labeled with log(p), not exact-zero probabilities. `git diff --check` passes; no CSV is tracked, no changes are staged and HEAD remains `5464d6e`. No commit/push/PR/remote modification was made.

### Handoff decision

**The requested EDA work can end and controlled preprocessing can begin.** All required calculations, scoped conclusions and unknown mechanisms are reported. Fix the experiment's prediction question, eligible features and disclosed validation protocol; keep post-event BMI/treatment outside any earlier-baseline predictor set. Compare required imputers/scalers/outlier/encoding methods within folds and report assumptions/sensitivity, not a supposedly established MAR/MCAR label. Source gaps and global-MCAR calibration limits are transparent limitations, not a reason to add bootstrap/permutation studies or more hypothesis tests outside the rubric. No optimal preprocessing method, clinical conclusion, full-project completion or grade is claimed.

## Historical review records

The dated sections below describe earlier commits, including tests that were subsequently removed. They are provenance records, not the current notebook specification; the matrix above is authoritative. The later-stage checklist remains unchanged.

## Conciseness and interpretation refinement of f30af40 — 25 October 2026

The official assignment was retrieved/read again through direct HTTP 200 after the web reader failed; its HTML SHA-256 remains `2cca63ea7b93788b4ae981e51ff92765d9e478d6c4d3469fa7458299a8d3dc38`, unchanged from the prior full audit. The tabular EDA section adds no compulsory Mann–Whitney/contingency/Holm family; Mann–Whitney is required in the separate text branch and ANOVA/chi-square/MI feature selection belongs to later tabular preprocessing. Those future/other-branch requirements remain in the exact checklist below.

### Content classification and presentation decisions

| Existing component | Classification | Decision and evidence retained |
|---|---|---|
| All-feature normality + scaling rationale | Required tabular EDA | Keep all 69 tests/results visible; add explicit decision meanings and five evidence-based candidate rows |
| Full Pearson/Spearman heatmaps + strong pairs | Required tabular EDA | Keep both 69×69 heatmaps and 17-pair table; group 17 pairs into five review domains; full matrices/N/key expandable |
| Both missingno views, Little, mechanism explanation | Required tabular EDA | Keep plots and exact Little implementation/scope; five-row mechanism assessment distinguishes hypotheses/unknowns |
| Schema, semantic/timing audit, integrity | Useful supporting EDA and reproducibility | Preserve input/ZIP/clinical eligibility safeguards and full audit |
| Numerical summary, skewness, IQR flags | Useful supporting EDA; later outlier work still required | Full 69-row summary expandable; plots/flags and actual evidence retained; no outlier removal |
| Cardinality and ZIP rarity thresholds | Useful supporting EDA | Preserve counts and 1% versus absolute-support comparison; rare literal examples expandable |
| Seven Mann–Whitney/Chi-square/Fisher/Holm tests | Optional advanced/supporting analysis, no claimed bonus | Explicit supplementary heading; seven-test family, effect definitions, assumptions and all p-values unchanged |
| Wider Little feasibility | Optional supporting scope assessment | Short rationale; full four-scope results expandable; no additional p-values; global inference BLOCKED |
| ZIP weighting/consistency | Optional supporting analysis | Calculations/results expandable; geographic dependence and proposed validation remain in main text |
| Six-variable correlation heatmap | Redundant presentation | Remove only duplicate figure; six-variable Pearson/Spearman/paired N remain expandable |
| Large full-matrix printouts and repeated prose | Redundant presentation | Expandable complete numerical tables; concise optional explanations; no numerical coverage lost |
| Findings/conclusion | Required synthesis for a defensible report | Seven rows/four requested columns; evidence versus candidate action explicit; no claim of performed/effective preprocessing |

Strong-pair review groups use existing 17 pairs, not new tests: income 8, demographic 4, education 2, housing/population 2, age 1. The scaling roadmap uses the executed summary and IQR diagnostics for age, BMI, density and household income; four documented percentage variables illustrate bounded numerical proportions. BMI's post-metastatic timing remains a gate. The missingness table makes recording/coverage hypotheses explicit as unconfirmed; the reference p=.061127 does not establish global MCAR or distinguish MAR/MNAR.

No new notebook cells, helper modules, dependencies, tests, preprocessing fits or pipeline changes were introduced. All 37 original IDs/order and 19 code executions remain. Markdown source shrank from 416 to 319 lines. The figure count falls 10→9 solely by removing the duplicate six-variable heatmap; all nine retained PNGs are byte-identical to the base. Existing five Little unit tests pass without skips; no statistical result changes. No commit, push, PR or remote modification was performed.

Publication verification: a new source snapshot without data/CSV built all four pages from saved outputs. Exported page data contains the complete 69-row normality table, all three 69×69 numeric matrices, 17 strong pairs, five scaling rows, five mechanism-assessment rows and seven findings. Headless Chrome using the installed browser found 11 native details blocks and no iframes; clicking the full-matrix summary opens all three 69-row tables (the expanded block grows from 22 px to 6,897 px). No browser/package dependency or pipeline change is required by the notebook. This is local rendering evidence, not a remote Actions/Pages deployment.

### Readiness and unresolved issues

The notebook supports planning controlled preprocessing comparisons; first freeze prediction time/eligible features and the disclosed post-EDA validation design. BMI/treatment cannot be approved for an earlier baseline. The source gaps and Gaussian/independence limitations require explicit reporting; full MCAR rubric inference remains BLOCKED and needs instructor review rather than a forced mechanism label. Further generic normality tests/plots are unnecessary. Identifying the unobserved mechanism would require collection/design information or a separately justified sensitivity design, not more p-value searches. Later preprocessing/evaluation and mandatory part(b) remain NOT VERIFIED in this refinement.

## Selective scientific review of commit 3baa00b — 25 October 2026

### Source and temporal evidence

The official [Kaggle Data dictionary](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data) was read through its indexed text. Direct HTTP access returned a JavaScript shell (HTTP 200), not the dictionary itself; HTTP 200 alone is not source verification. The [WiDS technical director’s tutorial](https://www.widsworldwide.org/get-inspired/blog/triple-negative-breast-cancer-datathon-a-tutorial/) was readable via the web tool, although a separate direct HTTP request returned 403. No authenticated data download or new dependency was needed.

Confirmed source statements are distinguished from inferences in notebook cells 0/4/5: target event is diagnosis period below 90 days; breast codes ICD-9/ICD-10, metastatic codes ICD-10; BMI first recorded after metastatic diagnosis; novel-treatment fields describe post-metastatic treatment; payer/state/ZIP/gender are at the metastatic date; environmental measures are annual ZIP3 concentrations. Exact date anchors, boundary wording, explicit numeric target mapping, code editions/individual code meanings, environmental units/reference years and baseline availability remain unverified. The poverty entry duplicates a home-value description and is not silently reinterpreted from its name. Some contextual units (density per km², household median income in USD) can now be labeled from the dictionary.

The proposed pre-metastatic prediction question is not the same as a supplied-table competition benchmark. BMI and its missingness indicator cannot be approved for that earlier baseline. Existing BMI/target tests remain explicitly retrospective diagnostics and the previously reported seven-test Holm family is retained; no new target-association tests or feature-selection rules were introduced.

### Little scope decision and actual feasibility output

Primary scope is unchanged: age/BMI, 12,906 patient records, patterns 8,965 / 3,941. ML covariance minimum eigenvalue 32.280713 and condition 5.514068 are numerically acceptable; EM converges in 45 iterations. D²=3.50653407757 equals the age-pattern closed form 3.50653407757, df 1, p=.06112720890. Mean age is 59.329057 in BMI-unrecorded records and 58.851814 in BMI-recorded records. These numbers explain how narrow this calculation is: it compares age means across recording patterns, not the distribution of unobserved BMI. It remains a Gaussian-model reference, with formal inference BLOCKED.

Scope definitions were based on semantic measurement levels, not additional p-values. The screen checks complete-case correlation matrices as dimensionless covariance diagnostics; these are not the pairwise matrices or Gaussian ML covariance, and no scaler is fitted. Numerical rank depends on tolerance. Observed values AND missingness masks are invariant within ZIP for all 67 contextual numerical columns, allowing an explicit ZIP-unit diagnostic without arbitrary within-group selection.

| Screened scope | Unit / rows | Features | Missing-pattern sizes, descending | Complete-case correlation rank | Condition | Additional Little test |
|---|---|---|---|---|---|---|
| Primary age/BMI | Patient /12906 | 2 | 8965,3941 | 2/2 | 1.13649 | No; original reference retained |
| Age/BMI + income_household_median + PM25 | Patient /12906 | 4 | 8940,3933,21,8,4 | 4/4 | 1.28189 | NOT RUN |
| All numerical candidates | Patient /12906 | 69 | 8940,3933,21,8,3,1 | 67/69 | 1.10e16 | NOT RUN |
| Contextual variables, one record per ZIP | ZIP3 /739 | 67 | 731,6,1,1 | 65/67 | 2.97e16 | NOT RUN |

The four-variable scope has full rank: it is not rejected as singular. Repeated context, unresolved independent sampling, non-Gaussian measurements and weakly supported patterns do not establish better calibration. High-dimensional scopes add numerical dependencies; ZIP aggregation changes the unit/estimand, leaves only 8 incomplete ZIPs and does not establish spatial independence. There is no imported minimum-five contingency-cell rule. No wider calibrated sensitivity test is justified by these screens, and no search for a desired p-value or MAR/MNAR label was performed.

### Preservation and re-execution

A fresh project .venv kernel ran all 19 code cells, including the analytic reduction and scope screen. Outputs are saved in 37 cells; all 35 base cells/IDs/order are retained. All 69 normality tests, both 69×69 matrices, 2,346 unique pairs, 12 Pearson / 15 Spearman / 17 union strong pairs, two missingno views and the seven-test reference family reproduce the base results. Thirty-nine normality p-value underflows remain explicitly flagged with log(p). The local helper’s five tests pass; its code/tests and dependency files are byte-identical to the base. No preprocessing/model was fitted, no CSV changed, and no commit/push was made during this review. The unchanged ten-figure scope is sufficient; no duplicate correlation plot is added.

The final saved-output version also builds all four book pages in a new CSV-free source snapshot. Exported page data retains all 69 normality rows, 17 strong-pair rows, four feasibility rows and 10 image assets. Nine figure images are byte-identical to the base; only the numerical histogram labels changed to reflect verified units/source uncertainty, and that figure was visually inspected without clipping. The startup TCP and Node DEP0169 warnings remain external toolchain warnings, with no saved notebook stderr/error outputs. Remote deployment is outside this review.

## Exact requirement checklist — implementation status is recorded above

### Part (a): selected tabular branch

- Dataset gate: >=10 attributes, >=10,000 records, numerical and categorical data, at least one attribute with >=5% missingness. WiDS is checked conservatively on features excluding ID/target.
- EDA: all-numerical normality branch n<=5000 / n>5000; both correlation heatmaps and strong-pair review; missingno; Little MCAR and mechanism explanation. Alpha .05 is an audit convention because the official page supplies no alpha.
- Missing-data experiments: five named strategies (mean, median, mode, kNN, MICE). kNN must include k=3,5,10. For every strategy, add 10% artificial MCAR missingness and report imputation RMSE; compare all results and justify the selection. Mask known values only for measurable ground truth; retain the original missingness and fit within training folds.
- Outlier comparisons: the text says “4 methods” but its first bullet includes both IQR and Z-score, followed by Isolation Forest contamination=.01,.05,.1; LOF n_neighbors=10,20,50; DBSCAN. Keep BOTH IQR and Z-score in the plan, not silently one. Report outlier rates, set overlap/Jaccard, and distribution change after removal using KS. The four-group/five-algorithm wording needs instructor clarification.
- Scaling: Min-Max, Z-score, Robust Scaling, Quantile Transform with uniform or normal output. Plan both Quantile outputs for the requested comparison. Levene is expressly phrased as optional (“có thể”); violin visualizations are suggested for comparison. A scaler does not inherently establish a normal distribution.
- Encoding: One-Hot, Ordinal, cross-validated Target Encoding, Binary Encoding for cardinality>20, and Frequency Encoding. Check VIF for each representation. The source calls VIF an explained-variance ratio; these are distinct quantities. Record VIF as variance inflation factor and ask which additional explained-variance measure is intended. The allowed-library list does not explicitly include category-encoders; do not install it without resolving permission.
- Feature filtering/selection: numerical ANOVA F, categorical chi-square, mutual information; Random Forest and Gradient Boosting importance; RFE with CV. Dimensionality/visualization: PCA, t-SNE, UMAP conditionally for a “large” dataset, without a published size cutoff. The prose makes model evaluation on selected features optional (“có thể”), but grading explicitly names CV F1. Preserve the five-fold CV F1-score and performance-versus-feature-count plot in the plan and resolve the prose/grading ambiguity; do not omit it from planning.
- Advanced/bonus, conditional on imbalance: SMOTE, ADASYN, Random Under-sampling; evaluate on a test set without resampling using Precision, Recall, F1-macro and AUC-ROC. Explain why resampling must follow splitting. No numerical imbalance cutoff is supplied for tabular data; the image branch’s 3:1 rule must not be transplanted here.

### Part (b): mandatory choice of exactly one of text or image

The repository currently has a text placeholder, not a completed part (b). Choice remains to be confirmed; none of these experiments is introduced now.

Text branch:
- Dataset: >=10,000 texts, >=2 classification labels.
- Text EDA: word/character length distributions by label and Mann–Whitney; word clouds plus top-50 words per class; type-token ratio; log-log frequency/Zipf analysis.
- Normalization pipeline: lowercase, HTML/URL/mention/hashtag removal, justified special-character/number handling, whitespace normalization; report vocabulary-change rates and text-length effects at each step.
- Compare four tokenization strategies: word (NLTK/spaCy), sentence, character, BPE subword (Hugging Face tokenizers). Report vocabulary size, test OOV rate, mean token-sequence length.
- Stop words: before/after vocabulary size, mean word/label mutual information, and Naive Bayes performance; discuss whether removal always helps.
- Porter, Snowball and WordNet lemmatization: collision rate and Logistic Regression five-fold CV impact.
- BoW, TF-IDF n-grams n=1,2,3, and Word2Vec trained on the dataset: dimension, sparsity, same/different-class cosine similarity, label-colored 2D t-SNE, silhouette score.
- Advanced prose: pretrained Sentence Transformer (example all-MiniLM-L6-v2), compare K-Means silhouette and Linear SVM versus TF-IDF; discuss semantics. The grading table nevertheless names Sentence Transformer in a 10% text criterion: this optional/graded conflict needs the instructor, not an invented resolution.

Alternate image branch (not selected/implemented): >=5 classes and >=5,000 images; pixel histogram/KDE by channel; class ratios including >3x largest/smallest rule; pHash duplicates; per-class brightness/contrast and boxplots. Each preprocessing technique needs quantitative effects and simple-classifier ablation (kNN or Logistic Regression). Resize at >=3 sizes (32x32,64x64,128x128 are examples), SSIM/PSNR curves; >=3 color spaces from the listed RGB/Grayscale/HSV/LAB and PCA k=50 explained variance; Min-Max [0,1], [-1,1], global and per-channel Z-score, KS before/after; >=5 augmentation types and original/augmented t-SNE. Advanced: PCA components for 90/95/99% variance plus PCA/t-SNE plots; Sobel/Prewitt/Canny with >=2 parameter sets each, edge-density by class and one-way ANOVA. The text says >=3 spaces while listing four; preserve that wording rather than inventing a mandatory fourth.

### Alternate part (a): time series — not selected

>=2 years at daily/hourly frequency. EDA: time plot (trend/seasonality/noise), ACF/PACF with explicit maximum lag (the source’s example is min(10 log10(n), n/5)), rolling mean/std at 7,30,90 days or equivalent. Preprocessing: add 5% MCAR time gaps; forward-fill, linear, polynomial degrees 2/3, cubic spline; MAE/RMSE and Ljung–Box residual checks. ADF/KPSS/PP before and after first/second differences, log or Box-Cox until stationarity is assessed. Additive/multiplicative decomposition plus STL with justified period and residual-variance ratio. Cyclic sin/cos weekday/month features, holiday/event features, multiscale rolling mean/std/min/max/skewness. Compare deseasonalized Z-score, windowed Isolation Forest, and 1D autoencoder OR STL-residual anomaly detection. Build lags through p chosen from PACF plus rolling/time/decomposed features, train RF Regressor for t+1, report test MAE/RMSE. Granger is advanced in prose for multivariate series but appears in grading; preserve the conflict. These demands are not transferred onto WiDS tabular EDA.

### Whole project, book, submission, grading

- Python throughout; allowed libraries: NumPy/pandas/matplotlib/seaborn/scikit-learn/SciPy/statsmodels, image/text libraries stated on the page, missingno, imbalanced-learn, dataset loaders; TensorFlow/PyTorch for deep learning. No new MCAR dependency was installed.
- Numerical scores and p-values must be stored in Python variables and printed. Each later preprocessing technique needs theory/formulas, code and result analysis in notebook source. Comparative report chapters are required; the audit Markdown is an administrative traceability artifact, not a substitute for those notebooks.
- One public Jupyter Book/site from one personal source repository, working from first to last chapter; a runtime-broken chapter receives no credit. Git history is part of workflow traceability. README needs student name/ID, data/environment/build/external-resource instructions. Data-preparation code must be in/imported by a book notebook. Large raw data stays on Kaggle/Hugging Face; never commit the WiDS CSV.
- Submit exactly one published Pages book URL to Moodle; retain a stable URL until grading ends. Oral defense includes these projects. The page rejects late submission, assigns deadline changes to the instructor, and does not publish a concrete due date in the retrieved text.
- AI assistance is allowed, but the student must understand the code/analysis. Plagiarism, dishonesty or unauthorized collaboration can result in zero for the course.
- Weights: selected part(a)=30%, selected part(b)=30%, code/book=40%. Selected-tabular rows: statistical EDA/distribution/MCAR=10%, outliers/encoding=10%, selection with CV F1=10%. Selected-text rows: EDA/Zipf=10%, normalization/tokenization/OOV=10%, vectorization/silhouette/Sentence Transformer=10%. Code/reproduction=10%, personal repo/book/README=10%, comparative report/discussion=20%.
- The alternative branches’ three rows do not add extra compulsory branches. Advanced markers conflict with several grading-row names; grading-specific interpretation is NOT VERIFIED until instructor clarification.
- Performance bands: 90–100% of a criterion for correct/deep/critical work; 70–89% correct/reasonable but missing depth/tests; 50–69% correct implementation with insufficient comparison/argument; <50% for unsuitable/incomplete/non-building work. This audit does not award a grade.

### Verified-source boundaries

The original Little (1988) publisher endpoint returned HTTP 403. Formula/ML estimation were verified through the maintained naniar documentation and source, plus a closed-form special case and the documented airquality example. The benchmark used the public [Rdatasets airquality mirror](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/airquality.csv), selecting Ozone, Solar.R, Wind, Temp, Month, Day (excluding the exported row-name column), with EM tolerance 1e-10; its CSV is only in the ignored local cache. pyampute's inspected code uses marginal means/pairwise covariance (not Gaussian ML), so it was not adopted. Qolmat uses EM but imports extra packages outside the published list and applies a different covariance factor; it was inspected, not installed or used. No claim is made that the paywalled 1988 paper itself was read in full.
