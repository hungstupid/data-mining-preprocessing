# Rubric audit — latest EDA handoff: 26 October 2026

Source: https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/

The entire official HTML page was retrieved with HTTP 200 on 25 October 2026 and read through the grading/policy sections. The web-tool rendering failed, so the direct HTTP response was used. The page’s linked raw Markdown returned 404; it is not used as evidence. Requirements below are concise technical paraphrases, with exact numeric parameters preserved. Cell references in the initial audit are **zero-based indices of the original 29-cell notebook**. PASS records observed code/output evidence, not an inference from a clean run. Future work uses NOT VERIFIED; it does not count as completed.

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

Current notebook: 31 cells / 16 code cells. Indices below are zero-based, execution counts in parentheses. PASS is evidence for the stated scope, not a grade or claim of known natural missingness. Correctly reporting an unidentified mechanism satisfies the interpretation task; the separate BLOCKED row limits a cohort-wide inferential claim and does not require another EDA study before preprocessing.

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

## Exact later-stage checklist — no experiments implemented in this change

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
