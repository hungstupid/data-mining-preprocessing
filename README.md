# HCMUS Data Preprocessing — WiDS 2024

**Student:** Nguyễn Đức Hưng — **Student ID:** 24127174.

Official assignment: [HCMUS preprocessing project](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/).
The complete requirements and grading were audited on 25 October 2026; see
[RUBRIC_AUDIT.md](RUBRIC_AUDIT.md) for before/final traceability, unresolved
statistical assumptions, and the exact later-stage checklist.

Individual project for **Data Mining and Applications, HCMUS**. This repository
provides a reproducible Python workspace and a Jupyter Book 2 publication scaffold.
Stage 01 EDA and Stage 02 controlled numerical imputation are implemented with
saved local results. Later preprocessing comparisons and classifier training remain future work.

## Dataset

Use only [WiDS Datathon 2024 — Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data).
This healthcare classification dataset concerns diagnosis delays among patients
with metastatic breast cancer. The binary target is `DiagPeriodL90D`; `patient_id`
is the identifier and must not be treated as a predictive feature.
Refer to the competition data dictionary and rules for clinical definitions and use terms.
Training data must contain both columns; the test CSV does not provide the target.

Raw data, processed data, API credentials, local environments, and generated book
files are excluded from Git. Download data directly from the official competition;
do not substitute Challenge #2 or redistribute the files through the book.

## Structure

```text
data-mining-preprocessing/       # actual cloned Git repository
├── README.md
├── requirements.txt            # exact direct dependency versions
├── requirements-lock.txt       # installed transitive dependency snapshot
├── .gitignore
├── .python-version
├── .vscode/settings.json
├── myst.yml                    # Jupyter Book 2 / MyST configuration
├── book/
│   ├── index.md
│   ├── tabular/
│   │   ├── index.md
│   │   ├── 01_eda.ipynb          # read-only EDA with locally computed outputs
│   │   └── 02_preprocessing.ipynb # controlled imputation benchmark; saved outputs
│   └── text/index.md
├── data/
│   ├── raw/                    # local, unmodified competition files
│   └── processed/              # local derived files, when implemented
├── src/validate_dataset.py
├── .github/workflows/deploy.yml
└── .venv/
```

On the original development machine, the clone was already inside another
directory with the same name. Open the inner Git repository in VS Code and run
commands there. No additional clone or nested project directory is needed.
Check the actual root with `git rev-parse --show-toplevel`.

## Python environment

The setup uses **Python 3.13.3** because Python 3.12 was not installed. The previous
pip-only Python 3.14 environment was preserved in `.venv-python314-backup/`;
it is not the active project environment. No global packages are required.

For a fresh checkout with Python 3.13 installed:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
python --version
python -c "import sys; print(sys.executable); print(sys.prefix)"
python -m pip --version
```

For an existing working `.venv`, activate it; do not recreate it. Use
`python -m pip install -r requirements.txt` for the pinned direct dependencies;
the lock snapshot also pins their transitive dependencies for closer reproduction.
Both files record actual installed versions. Recheck compatibility on another OS.
Optional packages such as UMAP and category encoders are not included.

If the course specifically requires Python 3.12, install it explicitly with
`brew install python@3.12` (user action), then create a new environment with
`$(brew --prefix python@3.12)/bin/python3.12 -m venv .venv` **only in a fresh
checkout or after safely preserving the current environment**. Verify the
dependencies again; the supplied snapshot was validated with Python 3.13.

Jupyter Book also needs **Node.js 24.x and npm** on `PATH`. Check `node --version`
and `npm --version`. If using nvm, `nvm install 24` and `nvm use 24` install/select
that version without changing system Python. The first HTML build downloads its
web theme and needs internet access.

### Notebook kernel

Register a kernel inside the environment, without writing a user-wide kernelspec:

```bash
python -m ipykernel install --sys-prefix --name hcmus-wids --display-name "Python (HCMUS WiDS .venv)"
python -m jupyter lab
```

In VS Code, select `.venv/bin/python` as interpreter and the matching notebook
kernel. Inside a notebook, `import sys; print(sys.executable)` must point to this
repository's `.venv/bin/python`. The workspace setting supplies the default;
an earlier VS Code selection may need to be changed manually.

## Download the official dataset

1. Sign in to Kaggle, open the [competition rules](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/rules),
   and join/accept the rules if requested.
2. Configure authentication locally using `kaggle auth login`, or generate an
   API token in [Kaggle settings](https://www.kaggle.com/settings/api) and store it
   in `~/.kaggle/access_token`. Legacy `~/.kaggle/kaggle.json` is also supported.
   Keep credentials outside this repository and restrict credential-file access
   to your account (`chmod 600` on the credential file). Do not paste tokens into
   notebooks, shell commands saved in this repository, or chat.
3. With `.venv` active, download and extract the official archive:

```bash
kaggle competitions download widsdatathon2024-challenge1 -p data/raw
python -m zipfile -e data/raw/widsdatathon2024-challenge1.zip data/raw
```

If Kaggle returns 401, complete authentication. For 403, verify competition
acceptance and account access in the browser. A manual download from the official
Data page into `data/raw/`, followed by extraction, is also valid.
See the [official Kaggle authentication documentation](https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication).

## Validate the dataset

```bash
python src/validate_dataset.py --csv data/raw/training.csv \
  --min-rows 10000 --min-features 10 --min-numeric 1 --min-categorical 1
```

The validator searches `data/raw/` recursively, ignores filename capitalization,
and identifies training CSVs by their required columns. When multiple files match,
choose explicitly with `python src/validate_dataset.py --csv data/raw/training.csv`.
Use this explicit path with the official files: `sample_submission.csv` also has
ID and target columns, so those headers alone do not identify training data.
It loads data read-only and reports dimensions, deep DataFrame memory, target
balance, missingness, inferred feature types, duplicate IDs/rows, constants,
near-constants, categorical cardinality, and possible missing-value sentinels.
The default near-constant threshold is 95% of non-missing values. Sentinel reports
are suggestions for later review, not replacements or confirmed missingness.

The official tabular choice requires at least 10 attributes, 10,000 rows, both
numerical and categorical attributes, and at least 5% missingness in one attribute.
The notebook checks all four requirements on actual data. The validator's command
above checks structural minima conservatively on features excluding target/ID;
its dtype counts do not replace the semantic audit or the notebook's 5% missingness
check. Without explicit `--min-*` values, the standalone validator reports
structural compliance as **UNCONFIRMED**. Exit status 0
means supplied checks passed, 1 means integrity/threshold failure, and 2 means
missing/unreadable input or invalid schema. Exit 0 alone does not certify a rubric.
If raw data is absent, the validator reports the missing input explicitly.
The EDA notebook below contains results computed from the local training CSV.

## Stage 01 — Exploratory Data Analysis

`book/tabular/01_eda.ipynb` audits the 12,906-row, 83-column training CSV, semantic
feature roles, missingness, distributions, categorical support, and relationships.
It reads `patient_zip3` as a string geographic code and audits its literal CSV
tokens and distinguishes recorded values, semantic roles and temporal availability.
Descriptive summaries and the required normality/correlation/missingness analyses
support candidate preprocessing comparisons. Class recording rates do not identify
a missingness mechanism, causal effect or useful predictor.
The mandatory rubric corrections add per-feature Shapiro/D’Agostino normality
tables, both full numerical correlation matrices/heatmaps and the complete strong-pair
union, and actual `missingno.matrix` views. `src/little_mcar.py` implements the
Gaussian ML/EM version of Little's mean-pattern statistic using existing NumPy/SciPy.
Run its numerical checks with `python -m unittest discover -s tests -v`.
It was also checked against the published `naniar` airquality example. The WiDS
age/BMI calculation is a limited normal-model reference; an assumption-supported
cohort-wide MCAR verdict remains **BLOCKED**, not converted into a MAR/MNAR claim.
The selective review of commit `3baa00b` adds an official-source/timing audit and
wider-scope feasibility diagnostics without adding Little p-values. The official
[data dictionary](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data)
identifies BMI and treatment recording after metastatic diagnosis. BMI's descriptive
audit remains retrospective; neither BMI nor its missingness indicator is approved
for prediction before that event. Contextual repetition,
sparse missing patterns and covariance dependencies leave broader calibrated MCAR
inference unresolved; numerical convergence alone does not resolve them.
A short mechanism-assessment table separates missing percentages, descriptive
evidence, the age/BMI MCAR reference, hypothetical MAR/MNAR explanations and
imputation candidates. MAR/MNAR is not identifiable from observed data alone.
This uncertainty is documented for the preprocessing experiments; no mechanism
label is forced and no imputation/scaling/encoding/model is fitted in EDA.
The standalone validator reports inferred dtype counts; the notebook separately
reviews semantic roles, so numeric-looking codes are not continuous variables.

The reviewed notebook also compares relative and absolute category-support
diagnostics and proposes a ZIP-aware validation protocol. All labeled rows have
already informed EDA: a later split of this CSV is a **post-EDA internal
assessment**, not a completely untouched test set. Learn future preprocessing
rules only within development training folds; confirm the deployment question
and evaluation protocol before running experiments.

With `.venv` active, rerun from the repository root:

```bash
python -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=hcmus-wids \
  --ExecutePreprocessor.timeout=180 book/tabular/01_eda.ipynb
```

Alternatively open the notebook, select **Python (HCMUS WiDS .venv)**, restart the
kernel, and run all cells. Root discovery also works from `book/tabular/`. The
direct `python -m nbconvert` form uses the active interpreter's package instead
of letting the Jupyter dispatcher select a global executable from `PATH`. The
notebook reads exactly `data/raw/training.csv`; it never uses the submission
template or test CSV. Its final cell verifies the raw-file checksum and the
loaded frame's values, index, dtypes, and shape. No transformed dataset is saved.

Publication uses the aggregate tables, figures, and interpretation outputs saved
inside the executed `.ipynb`. The existing Pages workflow builds **without
`--execute`**, so MyST renders those stored outputs without Kaggle credentials,
the CSV, or the notebook kernel. See the [MyST execution documentation](https://mystmd.org/guide/execute-notebooks).
Keep the executed outputs when preparing publication; if they are cleared, rerun
locally before publishing. Raw patient rows and IDs are not displayed. Executing
EDA requires local data even though rendering the book does not.

## Stage 02 — Controlled Missing Value Imputation

[`book/tabular/02_preprocessing.ipynb`](book/tabular/02_preprocessing.ipynb)
compares Mean, Median, numerical Mode, kNN k=3/5/10 and MICE with three
posterior-sampled completions (`sample_posterior=True`, seeds 101/102/103,
ten rounds). The six predeclared features are `patient_age`, `bmi`, `density`,
`income_household_median`, `education_college_or_above` and `PM25`. This original
experiment remains in Sections 1–9, with its own results and scope. Sections 10–15
audit all 69 numerical candidates and add a separate joint numerical benchmark;
the original six-feature ranking is not extrapolated to the expanded scope.
Full coverage is an extension for scientific completeness, not a literal all-69 rubric rule.
This retrospective reconstruction task does not approve post-metastatic BMI
for an earlier prediction time. Target, ID, ZIP, diagnosis and treatment fields
never enter an imputer.

ZIP-disjoint `GroupShuffleSplit` seeds 42/43 produce 8,173 inner-training,
2,081 imputation-validation and 2,652 reserved rows. All estimator statistics
and internal conditioning fit only inner training. Seed 2024 uniformly masks
`floor(0.10 * observed N)` cells per validation feature; natural NaNs and the
reference remain unchanged. Every configuration uses the same 1,101 known-cell
positions in the original scope. The expanded scope uses the same masking rule
on its ordered 69-column matrix and reports its own counts and mask hash.
The outer reserve is not used to choose an imputer; prior whole-file
EDA exposure is disclosed.

Raw pooled RMSE and per-feature RMSE are retained. Selection uses the declared
equal-feature mean of RMSE divided by observed inner-training SD (ddof 0), so
large-unit income does not dominate the choice. MICE uses mean draw-level metrics
and sample SD, not errors of averaged imputations or Rubin-rule pooling. The
notebook includes actual fit/transform timings, focused synthetic checks and a
real-data fixed-seed MICE repeat in each scope. The extension also reports complete
eligibility, pairwise support, conditioning, memory/model-count estimates, an
unscored full-population pilot, posterior support violations and categorical gaps.
Highly correlated features are retained; no clipping or score-based exclusions
are applied. No completed patient dataset is exported.

With `.venv` active, rerun from the repository root:

```bash
python -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.kernel_name=hcmus-wids \
  --ExecutePreprocessor.timeout=300 book/tabular/02_preprocessing.ipynb
```

Alternatively select **Python (HCMUS WiDS .venv)** and use Restart Kernel → Run All.
The same saved-output publication mechanism as Stage 01 applies: keep the real
aggregate outputs, and build without `--execute` to render without private data.
Natural missingness mechanisms, prospective availability and performance on
naturally missing values remain unresolved. See [RUBRIC_AUDIT.md](RUBRIC_AUDIT.md)
for results and the exact scope of completion.

## Preview and build the book

With `.venv` active, run from the repository root:

```bash
jupyter book --version
jupyter book start
```

Use the local URL printed by the CLI; stop the server with Ctrl+C. For static HTML:

```bash
jupyter book build --html
```

Output is under `_build/html/`. To reproduce the eventual project subpath:

```bash
BASE_URL=/data-mining-preprocessing jupyter book build --html
```

The landing page and section introductions are Markdown; rendering them requires
no dataset, Kaggle authentication, or notebook execution. `myst.yml` is the only
book configuration; Jupyter Book 1 `_config.yml`/`_toc.yml` are not used.
See the [Jupyter Book 2 documentation](https://jupyterbook.org/stable/).

## Reproducibility and future work

Keep raw files unchanged. Record the official source, download date, checksums,
and actual validation output locally when data is available. Add the remaining
experiments as notebooks under `book/tabular/`, using the project kernel, explicit
random seeds, documented decisions, and leakage-safe train/validation splits.
Add notebooks to the explicit `project.toc` in `myst.yml`. The text section is
reserved for later work; no text dataset or text processing is configured.
Under the official assignment, part (b) is **mandatory**: choose image or text in
addition to the tabular choice in part (a). The text placeholder does not satisfy
that requirement. Advanced items and ambiguities between prose and grading tables
are recorded separately in the audit; they are not silently counted as completed.

Use `python -m pip check` after dependency changes and refresh both version files
from the successfully tested environment. Confirm Git exclusions with
`git status --short --ignored` before sharing. Review notebook outputs before
committing so that raw records and credentials are not published accidentally.

## GitHub Pages

`.github/workflows/deploy.yml` builds the Markdown book and prepares a Pages
artifact without downloading competition data or installing the data-science stack.
It uses the same pinned Jupyter Book version as the local environment, Node 24,
and the repository subpath through `BASE_URL`. CI selects an available Python 3.13
patch release because the local 3.13.3 pin is unavailable on Ubuntu 26.04 runners.
The workflow definition follows
the [supported Jupyter Book / MyST deployment approach](https://mystmd.org/guide/deployment-github-pages).

Publishing is a separate, manual step: in the GitHub repository, select
**Settings → Pages → Build and deployment → Source: GitHub Actions**, then
commit/push the reviewed files only when you intend to publish. A push to `main`
or a manual workflow dispatch triggers the prepared workflow. Nothing in this
local setup changes remote settings or triggers deployment.

The intended public address after a successful deployment is
`https://hungstupid.github.io/data-mining-preprocessing/`; this setup does not
assert that the site is already live. Remote Actions execution and Pages
deployment must be verified after the owner authorizes publication.

## Initial setup verification — 23 October 2026

- Python 3.13.3 in `.venv`; pip 25.0.1; `pip check` passed.
- All 15 direct dependencies imported successfully. Kaggle import/CLI checks used
  an empty configuration directory inside the ignored project cache, since the
  setup sandbox prevents creating the default `~/.kaggle/` directory. No
  authentication was configured or credentials created by these checks.
- The `hcmus-wids` kernel executed an in-memory notebook with the project's
  `.venv/bin/python`; no placeholder notebook was saved.
- Validator checks initially passed on synthetic fixtures, including input byte preservation.
  The official WiDS CSV was unavailable at initial setup; the Stage 01 notebook
  above now records analysis of the subsequently obtained local training CSV.
- Jupyter Book 2.1.7 generated static HTML for all three pages with the Pages
  subpath. The initial theme download timed out; the retry succeeded.
- MyST/workflow YAML, workflow shell syntax, TOC paths, dependency pins, and Git
  exclusions passed local checks. GitHub Actions and deployment were not run.
- The public repository had zero Actions workflows before setup. The unauthenticated
  Pages API returned 404, which does not establish the remote Pages settings.
