# Submission Review — Official Rubric Coverage

Reviewed **2026-11-16**, final-polish baseline `638ab5b6804142c897faf88b29446b3dfcb3d408`.
The initial tree was clean. This review reads notebook source **and saved outputs**, shared
modules, tests, README and the single book configuration. It preserves all algorithms,
datasets, splits, seeds, folds, hyperparameters and valid experimental results.

Source: [official HCMUS assignment and scoring table](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/).
Only **tabular Part A** and **text Part B** apply; image/time-series branches are alternatives.
The weights are Part A 30% (EDA 10%, outliers/encoding 10%, selection/CV 10%), Part B 30%
(text EDA 10%, normalization/tokenization 10%, representations 10%) and code/book 40%
(code/reproduction 10%, repository/README 10%, comparative report 20%). No minimum F1 is specified.

**B = required; A = advanced; C = conditional.** PASS means the requested implementation,
measurements and explanation are present, not an awarded mark. Scientific limitations are
not automatically missing rubric deliverables. CHECK identifies a genuine interpretation
question, not a reason to add unrelated experiments.

## Requirement-to-evidence checklist

| Official requirement / type | Notebook or code | Actual experimental evidence | Status | Score impact / qualification |
|---|---|---|---|---|
| A dataset: ≥10,000 rows, ≥10 attributes, mixed types, ≥5% missing in a feature (B) | [Tabular 01](book/tabular/01_eda.ipynb) | 12,906×83; 69 numerical candidates, 12 nominal/code/text fields; BMI 69.46% missing | PASS | No structural gap |
| Normality per numerical feature; use results to motivate scaling (B) | Tabular 01 normality/scaling rationale | All 69 results; Shapiro n≤5,000, D’Agostino–Pearson otherwise; observed N, statistic, p and per-feature interpretation | PASS | Rejection motivates comparison; scaling does not make affine-transformed data Gaussian |
| Pearson/Spearman heatmaps, strong pairs and treatment proposal (B) | Tabular 01 correlation | Two full 69×69 matrices, paired N, 17 unique strong pairs and redundancy discussion | PASS | Retaining related fields with an explicit later selection comparison is a justified proposal |
| Missingno, Little MCAR, MCAR/MAR/MNAR discussion (B) | Tabular 01; [Little implementation](src/little_mcar.py) | Full missingno matrix; age/BMI χ²=3.506534, df=1, p=.061127; explicit scope/exclusions and mechanism discussion | PASS, scoped | Does not classify the entire cohort as MCAR or distinguish natural MAR/MNAR; that stronger claim is not required evidence to fabricate |
| Mean/median/mode, kNN 3/5/10, MICE; 10% MCAR masking and RMSE; justified choice (B) | [Tabular 02](book/tabular/02_preprocessing.ipynb) | Seven configurations, identical 14,181 known-cell gaps in the joint 69-feature benchmark; kNN10 macro NRMSE=.676330; raw RMSE and three MICE draws retained | PASS | Six-feature supporting scope kept separate; no extra imputation experiment needed |
| IQR, Z-score, IF .01/.05/.10, LOF 10/20/50, DBSCAN; rates, overlap, removal KS (B) | [Tabular 03](book/tabular/03_outliers.ipynb) | Nine configurations, full Jaccard and 621 KS comparisons; IQR 60.60%, Z 23.43%; DBSCAN 291 noise/16 clusters | PASS | KS D is descriptive; nested-sample p-values nominal. Keeping all rows is a supported treatment decision |
| Min-Max, Z-score, Robust, Quantile; distribution plots (B); Levene permitted | [Tabular 04](book/tabular/04_scaling.ipynb) | Five transformations, both quantile outputs, 414 summaries, three violin figures; observed-BMI Levene W=4.285635 for original/affine views | PASS | Levene is optional in the wording; no need for extra tests or a forced scaler winner |
| One-Hot, Ordinal, CV Target, Binary for >20 levels, Frequency (B) | [Tabular 05](book/tabular/05_encoding.ipynb) | Five methods; state qualifies for genuine binary bits; ZIP-disjoint OOF Target; output widths 67/5/5/27/5 | PASS | Lexical Ordinal is clearly illustrative for nominal categories; no invented natural order |
| Multicollinearity after every encoding, VIF (B) | Tabular 05 `encoding_vif` | 145 per-column VIF rows: every encoded column + same six numeric fields; separate full 69+encoded rank audit | PASS, scoped | VIF is variance inflation, not explained-variance ratio despite the rubric wording. Scope is explicit; all-69 per-column VIF is not explicitly demanded |
| ANOVA, categorical Chi-square, MI (B) | [Tabular 06](book/tabular/06_feature_selection.ipynb) | Fold-local scores/ranks, k=10/30/50; correct numerical/indicator routing | PASS | Chi-square uses nonnegative indicators; no centered numerical Chi-square |
| RF/GB importance and RFE with CV (B) | Tabular 06 | Both tree rankers and LR-RFE; all selected feature identities and fold results retained | PASS | Shared preprocessing/ranking only within a fitting fold |
| PCA and t-SNE (B) | Tabular 06 | PCA .90/.95/.99 targets in CV; scree and two-dimensional PCA/t-SNE; fixed 2,000-row display | PASS | Display fits are separate from predictive CV |
| UMAP if dataset is large (C) | Tabular 06 PCA/t-SNE discussion | 12,906 source rows; fixed 2,000-training-row display; saved t-SNE runtime 7.23 s; scope choice now explained locally | Conditional, justified omission | Rubric defines no “large” threshold. PCA/t-SNE already meet the selected visualization purpose; no resource-driven need for another projector is observed. The marker may interpret the condition differently |
| Five-fold F1 and performance versus feature count (scoring-table requirement) | Tabular 06 | 22 configurations/110 evaluations; every fold, sample SD, count-performance plot; baseline .452154 versus best reduced .451716 | PASS | Low F1 is not a rubric failure; the report explains why selection did not improve this fixed classifier |
| SMOTE, ADASYN, RUS; original-prevalence evaluation, Precision/Recall/F1-macro/AUC (A) | [Tabular 07](book/tabular/07_class_imbalance.ipynb) | 20 fold results; RUS CV F1=.509298; locked reserve F1=.500629/AUC=.529792; class counts and confusion matrix | PASS | Resampling is fit-only; F1 gain is not misreported as improved ranking or calibration |
| B dataset: ≥10,000 texts and ≥2 labels (B) | [Text 01](book/text/01_eda.ipynb); [source protocol](src/text_data.py) | 50,425 descriptions/four labels; 27,752 eligible canonical-unique records; TRAIN 22,201/assessment 5,551 | PASS | Source and post-dedup populations are distinguished |
| Length by class and Mann–Whitney (B) | Text 01 lengths/tests | Word/character summaries and full-range plots; six pairs per metric, U/p/effect sizes; exact-dedup sensitivity | PASS | Holm and sensitivity are supporting additions, not extra requirements |
| Class word clouds/top-50/TTR (B) | Text 01 lexical view | Four clouds and four complete 50-row tables; corpus V/T=81,531/5,918,452; controlled-token-budget TTR | PASS | TTR depends on token definition and sample size; explained |
| Zipf log-log analysis (B) | Text 01 Zipf | Corpus/class rank-frequency curves; slope −1.173, R²=.9772 on declared ranks | PASS | Descriptive fit, not proof of a power-law generator |
| Full normalization; per-step vocabulary/length impact; conditional numbers/symbols (B) | [Text 02](book/text/02_normalization_tokenization.ipynb); [shared functions](src/text_preprocessing.py) | Ten steps with individual change/length tables; TRAIN lexical V 72,746→72,299; number-removal sensitivity | PASS | Keeping product numbers is a declared conditional policy; known mention/identifier losses are disclosed |
| Word/sentence/character/BPE; train vocab, assessment OOV and average sequence length (B) | Text 02 common-input benchmark | Same light input; OOV 3.0714%/75.6723%/.0029%/0%; vocabulary sizes and lengths printed | PASS | Whole sentences are the sentence-token unit; byte coverage explains BPE zero OOV |
| Stopword vocabulary/mean MI/NB before-after and interpretation (B) | [Text 03 A1–A3](book/text/03_stopwords_morphology.ipynb) | 180 types removed; mean MI .00041228→.00039878 nats; NB F1 .938031→.939891 | PASS | Mean MI changes its averaging set; common-word MI unchanged; removal is not universally better |
| Porter/Snowball/WordNet collisions and LR five-fold CV (B) | Text 03 B1–B2 | Compression and collision-membership both reported; LR means .947950/.948559/.948589/.948760 | PASS | WordNet is a declared noun baseline; stemming brands/order/senses has limits |
| BoW, TF-IDF n=1/2/3 and project-trained Word2Vec (B) | [Text 04 §1–2](book/text/04_representations.ipynb) | Correct cumulative n-grams, 30k cap effect measured; real CBOW D=100/V=40,880, 10 epochs, TRAIN only | PASS | No globally fitted Word2Vec classifier CV score is claimed |
| Dimensions and sparsity per representation (B) | Text 04 §4 | All six N×D, numerical nnz, 1−nnz/(ND), memory and zero rows; sparse 99.63–99.77% | PASS | Full sparse document-term matrices never densified |
| Same/different-class cosine (B) | Text 04 §5 | Same 2,400+2,400 controlled pair IDs for all methods; means/medians/IQR/ECDF; Word2Vec gap .21408 | PASS | Pair quotas/seeds are reproducibility choices; no universal ranking claim |
| Label-colored t-SNE and class-separation silhouette (B) | Text 04 §6–7 | Six panels on same 1,200 IDs; original-space true-label and cluster silhouettes separately | PASS | Silhouette is not measured on distorted two-dimensional coordinates |
| Sentence Transformer, K-Means/silhouette and TF-IDF vs Linear SVM (A in prose, named in scoring table) | Text 04 §3/6/8 | Actual pinned MiniLM; K-Means ARI .727192 vs TF-IDF .326454; SVM .937824 vs .957514; all five scores/sample SD | PASS | Included despite the prose/scoring inconsistency; no extra model needed |
| Python, appropriate packages, numerical values in variables, readable reusable code (B) | All 11 notebooks; `src/`; `tests/`; requirements | Every chapter has real saved outputs, mathematical explanations and analysis; targeted tests exercise actual functions | PASS, dependency qualification | Gensim numerical-fix source pin retained and tested. General library list omits gensim despite requiring Word2Vec; this disclosed interpretation remains for the marker |
| Personal repository, identity, dataset links, installation and build README (B) | [README](README.md), requirements, `myst.yml` | Nguyễn Đức Hưng/24127174; both Kaggle sources; exact runtime lock and commands; no raw data/weights in Git | PASS | Source build needs Git/compiler; already documented |
| One public Jupyter Book, clean chapter execution/build, comparative discussion (B) | All notebook chapters; existing Pages workflow | 11 executed notebooks, six report sections each, 47 saved figures; test/build/browser verification below; published Stage 04 checked | PASS | New documentation from this review stays local until an authorized push |

## Review decisions

No algorithm, formula, metric, fitting-boundary or result mismatch requiring a scientific
change was found. Keep the notebook-oriented structure, small existing helpers and targeted
leakage/numerical tests. Repeated setup makes chapters independently runnable; extracting a
framework would add complexity without rubric coverage. Do not add model searches, datasets,
POS tagging, significance tests, more regressions or higher-F1 targets. Short method-level
explanations now cover the previously bare tabular headings; the Little section explains
its actual two patterns, df, age-mean contrast and implications without changing the test.

The rubric requires controlled implementation and interpretation, not verified clinical
suitability, an external deployment cohort, causal identification, a significant improvement,
a prescribed CI or a guaranteed natural MCAR/MAR/MNAR label. Existing limitations on those
claims remain valid, but do not create additional missing assignment criteria.

Useful supporting additions already present include canonical/normalized grouping, Holm
adjustment, token-budget TTR, macro NRMSE, ARI, Euclidean silhouette sensitivity, runtime/storage,
Brier and the native Word2Vec regression. Keep them; none is a new requirement imposed here.

The essential gensim source fix stays pinned at `ecf22c266f3b8930610114c149d8991ed14e2a16`.
The latest PyPI stable 4.4.0 wheel was tested separately and still fails the negative-one
regression; the exact source pin was rebuilt without pip cache and passes all four cases.
The remaining practical limit is a third-party source build requiring Git/compiler, not an
unverified change to earlier dependency pins. See the [text audit](docs/TEXT_RUBRIC_AUDIT.md).

## Verification for this review

- Full existing unit suite in a fresh, isolated Python 3.13.3 environment: **48 pass**;
  no tests added. All 158 runtime pins match the lock exactly, imports succeed and the Git
  dependency builds from source without cache. Platform verified: macOS arm64; Linux/Windows
  scientific execution is **NOT VERIFIED**.
- `python -m pip check`: no broken requirements. `git diff --check`: clean.
- All 11 notebook schemas validate; all 154 code cells have saved execution counts and no
  error outputs; 47 actual PNG outputs. No scientific cell or output is edited by this review.
- Fresh-kernel Run All in that clean environment: **Tabular 01 and Text 04 PASS**.
  All 33 EDA table outputs and 24 selected scientific representation/CV tables match the saved
  originals exactly. Original repository outputs are retained. The other nine full notebook
  reruns are **NOT VERIFIED in this pass**: their code/results are unchanged and were inspected.
- The clean environment also builds the 16-page book after removing the local data/model-cache
  symlinks, disabling transformer download and hiding GPUs. Static publication remains distinct
  from executing notebook experiments.
- `BASE_URL=/data-mining-preprocessing .venv/bin/jupyter book build --html`: PASS,
  16 pages. Chrome checks all 11 notebook pages and all 47 figure images, with no JavaScript,
  HTTP or KaTeX errors. The existing theme's Node `url.parse()` deprecation warning is nonfatal.
- Published baseline: [successful Pages workflow for f33849e](https://github.com/hungstupid/data-mining-preprocessing/actions/runs/43894173758).
  Chrome verifies the public [Stage 04 chapter](https://hungstupid.github.io/data-mining-preprocessing/representations/),
  all nine figure images, both main SVM values (.957514/.937824), no KaTeX or HTTP errors.
- Commit/push are authorized separately by the user for this final polish; no merge,
  force-push, Pages-setting change or manual workflow dispatch is needed.

## Submission decision

All unconditional requirements for the selected tabular/text branches have implementation,
measured evidence and discussion. No required experiment is presently missing. Conditional
UMAP applicability and the general gensim library-list interpretation remain honest grading
qualifications, not reasons to invent further experiments. The existing published scientific
book is ready for submission and oral preparation. The final polish changes only Markdown
and verification documentation; no new experiment or framework is introduced. No score is guaranteed.
