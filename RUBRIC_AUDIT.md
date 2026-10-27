# Part A — Current Rubric Evidence

Reviewed baseline: `82617d1bbe17bf0675d3ca770f5bb493b3dfacdc` (initial working tree clean).
Scope: presentation and independent execution of Stages 01–07; no new experiment or Part B work.
The [official HCMUS rubric](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)
was retrieved and read in full for this refactor. **PASS** below records implementation/output
coverage; **LIMITED** records an unresolved scientific or rubric interpretation. Neither means
an awarded grade. The rubric also requires Part B for the complete assignment.

## Criterion → evidence

| Criterion | Current evidence | Status / qualification |
|---|---|---|
| Suitable mixed table; ≥10,000 rows, ≥10 predictors, ≥5% missing in a feature | [01 EDA](book/tabular/01_eda.ipynb): 12,906×83, 69 numerical candidates, 12 nominal/code/text predictors; BMI 69.46% missing | PASS; raw data remain private |
| Semantic types, integrity and target | EDA semantic audit; zero duplicate/missing IDs; ZIP tokens read as string; literal `999` preserved | PASS; clinical code meanings/feature eligibility not invented |
| Target polarity and source | Competition dictionary + [MathWorks WiDS walkthrough](https://blogs.mathworks.com/student-lounge/2024/01/01/predicting-timely-diagnosis-of-metastatic-breast-cancer-for-the-wids-datathon-2024/): 1=True/90-day group, 0=complement/minority | Verified polarity; clinical anchor and exact-day boundary remain unresolved |
| Normality for every numerical feature | EDA: Shapiro for n≤5,000, D’Agostino–Pearson otherwise; all 69 rows, observed-case N, p-values and interpretation retained | PASS implementation; dependent/skewed observations limit calibration; raw tests do not control FWER |
| Pearson/Spearman and strong correlations | Both 69×69 matrices, pairwise-N matrix, heatmaps and all 17 unique strong pairs retained | PASS; descriptive, no automatic deletion or causality |
| Missingness visualizations/patterns | Full missingno matrix and seeded focus; per-feature/class missing rates, co-missingness and patterns | PASS; missingness association does not establish a mechanism |
| Little's MCAR test and mechanisms | Age/BMI Gaussian-EM reference: χ²=3.506534, df=1, p=.061127; 2 patterns, converged covariance; four-scope feasibility audit and tested local implementation | **LIMITED**: working-reference non-rejection only; calibrated cohort-wide MCAR unsupported; no MAR/MNAR identification |
| Mean, Median, Mode, kNN 3/5/10, MICE; 10% masks; RMSE | [02 Imputation](book/tabular/02_preprocessing.ipynb): seven configurations, original six-feature support plus primary joint 69-feature benchmark; identical 14,181-cell expanded mask | PASS; training-only fits; natural missing-case accuracy not established |
| IQR/Z-score, IF 3 settings, LOF 3 settings, DBSCAN | [03 Outliers](book/tabular/03_outliers.ipynb): all 9 configurations, formulae, flags/rates, complete Jaccard, 621 KS comparisons and composition effects | PASS; no ground-truth anomaly labels; nested/ZIP-dependent KS p-values nominal; keep-all decision retained |
| Min-Max, Standard, Robust, Quantile; distributions and optional Levene | [04 Scaling](book/tabular/04_scaling.ipynb): five settings including both quantile outputs, 414 summaries, three provenance-aware violin figures and observed-BMI Levene | PASS; no scaler chosen by normality/Levene p-value |
| Five encodings; CV Target; Binary for >20 levels | [05 Encoding](book/tabular/05_encoding.ipynb): One-Hot, Ordinal, ZIP-disjoint Target OOF, genuine state binary bits/hybrid, Frequency | PASS implementation; Ordinal is an illustration, not a verified nominal ordering |
| Multicollinearity/VIF | Encoding: complete 145-row VIF on encoded columns + fixed six numerical fields; separate full 69+encoded design rank audit | PASS scoped comparison; VIF is variance **inflation factor**, not explained-variance ratio; not all-69 per-column VIF |
| ANOVA, Chi-square, MI, RF/GB, RFE with CV | [06 Feature selection](book/tabular/06_feature_selection.ipynb): 22 configurations/110 held-fold evaluations; all ranks, selected identities and stability | PASS; k/block scopes explicit; fresh learned preprocessing in every fold |
| PCA, t-SNE, conditional UMAP | All 3 PCA variance targets in CV; training-only scree/2D PCA and fixed 2,000-row t-SNE display | PCA/t-SNE PASS; **LIMITED** UMAP omitted, rubric's “large” condition has no threshold; no unverified coverage claim |
| Five-fold F1-macro comparison and theory/results | Stage 06: same ZIP-aware folds/classifier, all five scores, means/SD, feature counts, formulas and count-performance plot | PASS; SD is descriptive, no-selection reference remains strongest |
| Imbalance analysis; SMOTE/ADASYN/RUS; original-prevalence evaluation | [07 Class imbalance](book/tabular/07_class_imbalance.ipynb): four treatments including baseline, 20 held-fold results, both-class metrics, continuous AUC, confusion tables, original reserved rows | PASS; moderate imbalance, numerical-only common scope; no synthetic categorical interpolation |
| Reproducibility, leakage and data integrity | Fixed masks/ZIP partitions/folds; train-only transforms/sampling; analytic and Pipeline fixtures; source hashes; no private processed cache | PASS execution checks; whole-file EDA exposure and unresolved timing disclosed |
| One Jupyter Book, chapter notebooks, source/setup/personal identity | [README](README.md), seven independently executable notebooks, [Part A overview](book/tabular/index.md), [appendix](book/tabular/appendix.md), `myst.yml` and existing Pages workflow | PASS source structure; local publication checks below; new remote deployment not attempted |

## Fixed experimental contract

- Training/validation/reserve: 8,173/2,081/2,652 rows, 443/148/148 disjoint ZIPs;
  GroupShuffleSplit seeds 42/43. The submission template is never a training source.
- Stage 02: observed-value masks, seed 2024; MICE m=3, seeds 101/102/103, ten rounds,
  posterior sampling. Same algorithms, eligibility, losses and selection criterion.
- Stages 03–05: same observed-value StandardScaler→kNN10 preparation, restore known values
  exactly, preserve all rows. `src/tabular_data.py` reproduces this preparation without
  executing previous notebooks. No fit occurs at import time.
- Stages 06–07: same five StratifiedGroupKFold splits, shuffle/seed 42; preprocessing learned
  only on each fitting fold. Stage 07 uses the existing numerical-only scope and fresh baseline;
  it is not a direct effect comparison against Stage 06's mixed-feature baseline.
- LR/hyperparameters, threshold .5, sampler settings, selection rules, reserve policy and
  original code/experimental units are preserved. Only presentation, explicit imports and
  cross-notebook dependency/verification plumbing change.
- Raw training SHA-256:
  `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`.

## Reproduction and numerical regression

The following checks use the existing `.venv` / `hcmus-wids` kernel. Aggregate before/after
reports and source snapshots are retained locally under ignored `.cache/part-a-refactor/`;
Git preserves the baseline source. Timings/available OS memory vary and are not model results.

| Check | Result |
|---|---|
| Restart Kernel → Run All, each of seven chapters | Executed independently; 93 sequential code cells saved without exception (88 original computational units + 5 independent bootstraps) |
| Unit tests | 8 pass: existing 5 Little tests + 3 shared-input/split/training-only preparation tests |
| Notebook correctness groups | 54 Stage 02–07 groups pass; synthetic fixtures, held-label traps and full-pipeline reproductions retained |
| Before/after aggregate comparison | EDA plus all Stage 02–07 legacy result fields compared; numerical values identical; only runtime/memory measures and documented prose/check names exempted |
| Partitions/prepared matrices/folds | Actual partition hashes agree in all chapters; Stage 03–05 completed matrices match Stage 02 reference; Stage 06/07 actual grouped fold indices match |
| Plots and original computational units | All 26 PNG outputs byte-identical; all 88 original code-cell units represented; no experiment removed |
| Protected sources | All three local raw CSV hashes unchanged; Part B, validator, Little implementation, dependencies and deployment workflow unchanged |
| Notebook format | JSON/schema, unique cell IDs, sequential execution counts, six report sections and no error outputs checked |
| CSV-free Jupyter Book / browser | PASS: 11-page CSV-free build without `--execute`; local Chrome checks Part A navigation, tables, formulas, images and page widths; remote publication not attempted |

| Preserved result | Before | After |
|---|---:|---:|
| kNN10 Macro NRMSE, joint 69-feature scope | 0.6763300629944509 | 0.6763300629944509 |
| MICE pooled raw RMSE | 12463.419984895585 | 12463.419984895585 |
| MICE bounded-share violations (no clipping) | 912 | 912 |
| DBSCAN eps / noise / non-noise clusters | 6.892189118008946 / 291 / 16 | 6.892189118008946 / 291 / 16 |
| Stage 06 no-selection mean F1-macro | 0.4521541171754245 | 0.4521541171754245 |
| Stage 07 RUS mean CV F1-macro | 0.5092981864054043 | 0.5092981864054043 |
| Locked RUS reserved F1-macro / ROC-AUC | 0.5006293996862623 / 0.5297922388117433 | 0.5006293996862623 / 0.5297922388117433 |

## Remaining limits and review decisions

1. Gaussian/independence assumptions prevent calibrated Little inference; no expanded-feature
   p-value search is used to force a PASS. Natural MAR/MNAR cannot be decided from these outputs.
2. BMI/treatments are post-metastatic; baseline timing, environmental periods/units, `poverty`
   dictionary conflict and prospective availability remain unresolved. Target polarity is verified
   separately from timing. ZIP grouping reduces geographic overlap, not all dependence or temporal leakage.
3. Whole-file EDA informed design. The reserve is a post-EDA internal assessment, not an untouched
   external clinical cohort; reruns check the same locked policy, not authorize retuning.
4. RUS improves threshold F1 here but not AUC/Brier; synthetic ages/context mixtures lack validated
   realism. Reconstruction, VIF, normality and embeddings do not establish predictive/clinical utility.
5. The marker should confirm scoped VIF, illustrative Ordinal and conditional UMAP interpretation.
   These are disclosed rather than filled with unnecessary experiments. Part B remains out of scope.

Historical audit/deployment narratives are preserved verbatim in
[the baseline audit archive](docs/history/RUBRIC_AUDIT_82617d1.md). They are historical evidence,
not current notebook cell references or a specification. Notebook Markdown is reduced from 15,690 to 3,783 whitespace-delimited words (about 76%);
all 26 original display formulas remain. No commit, push or PR is performed.
