# HCMUS Data Preprocessing — WiDS 2024

**Nguyễn Đức Hưng — MSSV 24127174** · Data Mining and Applications, HCMUS.

[Published Jupyter Book](https://hungstupid.github.io/data-mining-preprocessing/) ·
[Official rubric](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) ·
[Current evidence audit](RUBRIC_AUDIT.md).

Part A uses [WiDS Datathon 2024 Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data):
12,906 labeled records, 83 columns, 69 numerical candidates and 12 nominal/code/text fields.
`patient_id` is an identifier; `patient_zip3` is a string geographic group key.
The target `DiagPeriodL90D` uses 1 for the 90-day diagnosis group and 0 for its complement;
see the [MathWorks source](https://blogs.mathworks.com/student-lounge/2024/01/01/predicting-timely-diagnosis-of-metastatic-breast-cancer-for-the-wids-datathon-2024/).
Precise clinical timing/eligibility remains unresolved. These are retrospective methodological
comparisons, not a deployable clinical model. Part B is unchanged and not implemented.

## Read Part A

| Stage | Executable chapter | Main evidence |
|---|---|---|
| 01 | [EDA](book/tabular/01_eda.ipynb) | Normality 69/69, Pearson/Spearman, missingno and scoped Little reference |
| 02 | [Imputation](book/tabular/02_preprocessing.ipynb) | Seven configurations, fixed 10% masking, raw RMSE and Macro NRMSE |
| 03 | [Outliers](book/tabular/03_outliers.ipynb) | Nine configurations, Jaccard, KS and keep-all recommendation |
| 04 | [Scaling](book/tabular/04_scaling.ipynb) | Five configurations, provenance-aware violins and focused Levene diagnostic |
| 05 | [Encoding](book/tabular/05_encoding.ipynb) | Five methods, group-OOF Target Encoding and scoped VIF/rank |
| 06 | [Feature selection](book/tabular/06_feature_selection.ipynb) | 22 configurations / 110 CV evaluations, PCA and t-SNE |
| 07 | [Class imbalance](book/tabular/07_class_imbalance.ipynb) | Four treatments, original-prevalence evaluation and locked internal assessment |

Every chapter follows Objective → Methodology → Implementation → Results → Discussion →
Conclusion. Full scientific diagnostics and long code are expandable; the
[appendix](book/tabular/appendix.md) provides supporting experiments and separate test instructions.
[src/tabular_data.py](src/tabular_data.py) contains only shared read/split/semantic/preparation
functions. Each notebook starts from the raw CSV in its own fresh kernel. It does not execute
an earlier notebook, load its saved HTML, or depend on a processed-data cache.

Stages 03–05 reconstruct the same train-only kNN10 descriptive input. Stages 06–07 start
from raw predictors and fit every learned transformation inside each CV training fold;
they never reuse a full-training completed/scaled matrix. The same deterministic group folds
are independently recreated from the fixed recipe. Whole-file EDA exposure is disclosed: the reserve
is an internal post-EDA assessment, not an untouched external cohort.

## Environment

Run commands at the Git root (`git rev-parse --show-toplevel`). On the original machine,
the clone is inside another directory with the same name; open the inner repository.
The verified environment uses Python **3.13.3**, exact dependencies in
`requirements-lock.txt`, and Node.js **24.x** for Jupyter Book 2.1.7.

For a fresh checkout:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
python -m ipykernel install --sys-prefix --name hcmus-wids --display-name "Python (HCMUS WiDS .venv)"
```

For an existing `.venv`, activate it and keep it. Select its `hcmus-wids` kernel in Jupyter/VS Code.
No additional dependency is required by this cleanup.
Check `node --version` and `npm --version`; the first book-theme download needs network access.

## Obtain and validate the data

Accept the [competition rules](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/rules)
and configure [Kaggle authentication](https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication)
locally, outside the repository. With `.venv` active:

```bash
kaggle competitions download widsdatathon2024-challenge1 -p data/raw
python -m zipfile -e data/raw/widsdatathon2024-challenge1.zip data/raw
python src/validate_dataset.py --csv data/raw/training.csv \
  --min-rows 10000 --min-features 10 --min-numeric 1 --min-categorical 1
```

Use exactly `data/raw/training.csv`. The submission template also has ID/target headers;
it is not training data. Do not replace existing raw files or publish CSVs/credentials.
Stage 01 contains an optional guarded download (`DOWNLOAD_IF_MISSING=False` by default)
that never replaces an existing training CSV. Executing that download requires your own
Kaggle authorization; it is not run during this refactor.

The validator reports structural/integrity diagnostics read-only. Explicit thresholds are
required for its structural PASS, and semantic types/missingness are checked in EDA.
The notebooks retain schema/ZIP checks, disjoint group boundaries and one final raw-file
integrity check per chapter. Analytic correctness and synthetic leakage fixtures live in
`tests/`, not the report narrative. No transformed patient table is exported.

## Reproduce the experiments

Run Stage 01–07 in order, each with Restart Kernel → Run All. For a clean command-line run:

```bash
for notebook in book/tabular/0[1-7]_*.ipynb; do
  .venv/bin/python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=hcmus-wids \
    --ExecutePreprocessor.timeout=600 "$notebook" || exit 1
done
.venv/bin/python -m unittest discover -s tests -v
```

The notebooks also run independently from the repository root or `book/tabular/`.
Stage 02 retains both the original six-feature and the joint 69-feature experiments.
The expanded winner remains kNN10 Macro NRMSE=0.676330; MICE has lower raw RMSE but
912 bounded-share violations. No clipping, reweighting, retuning or new experiment is added.
Stage 06 retains its no-selection reference; Stage 07 selects RUS by fixed mean F1,
with weak AUC and worse Brier explicitly reported. Repeated execution of the same locked
assessment checks reproducibility; reserved outcomes are never used for new choices.

## Build and publish

```bash
source .venv/bin/activate
jupyter book start
BASE_URL=/data-mining-preprocessing jupyter book build --html
```

HTML is written to `_build/html/`. `myst.yml` is the sole Jupyter Book 2 configuration.
The workflow `.github/workflows/deploy.yml` builds **without `--execute`**, rendering
real aggregate outputs saved in the notebooks. Rendering requires neither CSV nor Kaggle
credentials; recomputing the experiments requires the local training CSV. Keep saved outputs.

GitHub Pages must use **Settings → Pages → Build and deployment → Source → GitHub Actions**.
This setting was enabled and the reviewed deployment verified in the archived audit.
A separately authorized push to `main` or workflow dispatch publishes the committed source.
Local build success does not certify a new remote deployment. This cleanup does not
commit, push, change Pages settings, or alter the deployment workflow.

## Completion boundaries

The [current audit](RUBRIC_AUDIT.md) maps every applicable Part A requirement to evidence.
Little's age/BMI statistic is a limited Gaussian-model reference; calibrated cohort-wide
MCAR inference and natural MAR/MNAR identification remain unsupported. Ordinal meaning,
prospective eligibility, external validity and conditional UMAP wording retain explicit limits.
No grade or 100% scientific-validity claim follows from passing execution checks.
Part B (choose text or image) is mandatory for the whole assignment and remains outside
this work. Earlier implementation/deployment records are archived
[separately](docs/history/RUBRIC_AUDIT_82617d1.md); Git preserves the original notebook history.
