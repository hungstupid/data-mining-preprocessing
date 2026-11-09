# HCMUS Data Preprocessing — WiDS and E-commerce

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
comparisons, not a deployable clinical model.

Part B uses [E-commerce Text Classification](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification),
from [Gautam's Zenodo record](https://zenodo.org/records/3355823) (CC BY 4.0): 50,425
product descriptions, four category labels, and a headerless two-column CSV (`label`, `text`).
The input is a product description; the target is its category. **Stages 01–02 are implemented**:
source/quality audit and Text EDA, followed by normalization and four tokenization strategies.
Stopwords/morphology and representations remain planned. Read the
[Part B overview](book/text/index.md), [Text Stage 01](book/text/01_eda.ipynb) and
[Text Stage 02](book/text/02_normalization_tokenization.ipynb).

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
Text Stage 01 uses `wordcloud==1.9.6`; Stage 02 adds `nltk==3.10.4` and
`tokenizers==0.23.3` with their required dependencies. Install the updated lock in the
existing environment; no existing package was upgraded. No torch, sentence-transformers
or gensim package is required.
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

## Obtain the text data

With the existing `.venv` active, Stage 01 automatically prepares the original Kaggle CSV
**only when missing**, reusing a local archive and never replacing an existing CSV.
For an explicit CLI download in a fresh data directory:

```bash
mkdir -p data/raw/ecommerce
# Run the download only if neither CSV nor archive already exists.
if [ ! -f data/raw/ecommerce/ecommerceDataset.csv ] && [ ! -f data/raw/ecommerce/ecommerce-text-classification.zip ]; then
  kaggle datasets download -d saurabhshahane/ecommerce-text-classification -p data/raw/ecommerce
fi
# Stage 01 safely extracts the CSV if needed; it does not overwrite it.
```

If Kaggle authentication/download fails, manually download `ecommerceDataset.csv` from the
[original Kaggle dataset](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification)
and put it at `data/raw/ecommerce/ecommerceDataset.csv`. Configure credentials outside Git;
never commit the CSV/ZIP. Do not substitute a cleaned mirror. The notebook explicitly reads
`header=None`, preserves literal NA-like text, and measures missingness, source size and hashes.
The verified original MD5 is `6f2cfdb475096244916aeed6f776c1a6` and SHA-256 is
`1d44be1780bc9558f40ab4cee5b32051ddfe90647cd525b9652b47cdb233593f`.
Source/version differences are reported; observed counts are never forced to reference values.

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

For Text Stage 01 only, without rerunning Part A:

```bash
.venv/bin/python -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=hcmus-wids \
  --ExecutePreprocessor.timeout=600 book/text/01_eda.ipynb
.venv/bin/python -m unittest discover -s tests -p 'test_text_data.py' -v
```

Text Stage 01 also runs independently from `book/text/` with the same kernel. It keeps the
raw file unchanged and stores real aggregate outputs. Main EDA excludes one missing text;
exact deduplication is a separate sensitivity view. There is no final cleaning pipeline,
trained model or exported split. All text rows/labels inform EDA, so any later internal
holdout must disclose that exposure. The Part A protocol and results are unchanged.

For Text Stage 02, run independently from root:

```bash
.venv/bin/python -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=hcmus-wids \
  --ExecutePreprocessor.timeout=600 book/text/02_normalization_tokenization.ipynb
.venv/bin/python -m unittest discover -s tests -p 'test_text*.py' -v
```

The notebook guards `punkt_tab` lookup/download and reuses existing English resources.
For manual bootstrap if missing:

```bash
.venv/bin/python -m nltk.downloader -d .cache/nltk_data punkt_tab
```

No other NLTK corpus/model is downloaded. Resource download failures stop with instructions;
there is no fake tokenizer fallback. English resource-file hashes are retained in the notebook.
The notebook also runs from `book/text/` with the same project kernel.

`src/text_data.py::make_text_protocol(raw, test_size=.2, seed=42)` rebuilds the text population
and membership from raw records. It removes missing/blank/invalid rows, all conflicting-label
canonical groups, exact duplicates and additional canonical duplicates, then stratifies
27,752 examples into **22,201 train / 5,551 internal post-EDA assessment** rows. `row_id` traces
the zero-based original CSV record position; canonical keys and row IDs never cross partitions.
Related product variants may still remain. Later chapters call this same helper rather than
executing a prior notebook or requiring a processed cache.

Stage 02 measures normalization on TRAIN and compares a fixed number-removal alternative.
Its tokenizer benchmark uses one punctuation-preserving light input for all four methods;
BPE learns from TRAIN only. The test partition supplies coverage/OOV and sequence diagnostics,
not seed/configuration selection. No classifier or accuracy winner is asserted.

## Build and publish

```bash
source .venv/bin/activate
jupyter book start
BASE_URL=/data-mining-preprocessing jupyter book build --html
```

HTML is written to `_build/html/`. `myst.yml` is the sole Jupyter Book 2 configuration.
The workflow `.github/workflows/deploy.yml` builds **without `--execute`**, rendering
real aggregate outputs saved in the notebooks. Rendering requires neither CSV nor Kaggle
credentials; recomputing Part A requires its training CSV and Text Stages 01–02 require the
original E-commerce CSV. Keep saved outputs.

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
Part B chooses text and has implemented Stages 01–02 (audit/EDA and normalization/tokenization);
Stages 03–04 remain pending, so the whole assignment is incomplete. The current/archived tabular audits
retain their original Part A scope and are not text-completion audits.
Earlier implementation/deployment records are archived
[separately](docs/history/RUBRIC_AUDIT_82617d1.md); Git preserves the original notebook history.
