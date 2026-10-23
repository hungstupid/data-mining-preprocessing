# HCMUS Data Preprocessing — WiDS 2024

Individual project for **Data Mining and Applications, HCMUS**. This repository
provides a reproducible Python workspace and a Jupyter Book 2 publication scaffold.
Preprocessing experiments, evaluations, and model training have not been implemented.

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
│   ├── tabular/index.md
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
python src/validate_dataset.py
```

The validator searches `data/raw/` recursively, ignores filename capitalization,
and identifies training CSVs by their required columns. When multiple files match,
choose explicitly with `python src/validate_dataset.py --csv data/raw/training.csv`.
It loads data read-only and reports dimensions, deep DataFrame memory, target
balance, missingness, inferred feature types, duplicate IDs/rows, constants,
near-constants, categorical cardinality, and possible missing-value sentinels.
The default near-constant threshold is 95% of non-missing values. Sentinel reports
are suggestions for later review, not replacements or confirmed missingness.

Course minimum thresholds were not included in the setup request. Supply the
actual rubric values through `--min-rows`, `--min-features`, `--min-numeric`, and
`--min-categorical`. Feature counts exclude target and ID. Until all four values
are supplied, course compliance is reported as **UNCONFIRMED**. Exit status 0
means supplied checks passed, 1 means integrity/threshold failure, and 2 means
missing/unreadable input or invalid schema. Exit 0 alone does not certify a rubric.
Missing raw data is expected until the download is completed; no real-dataset
validation results are included in this scaffold.

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
and actual validation output locally when data is available. Add experiments
later as notebooks under `book/tabular/`, using the project kernel, explicit
random seeds, documented decisions, and leakage-safe train/validation splits.
Add notebooks to the explicit `project.toc` in `myst.yml`. The text section is
reserved for later work; no text dataset or text processing is configured.

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

## Setup verification — 23 October 2026

- Python 3.13.3 in `.venv`; pip 25.0.1; `pip check` passed.
- All 15 direct dependencies imported successfully. Kaggle import/CLI checks used
  an empty configuration directory inside the ignored project cache, since the
  setup sandbox prevents creating the default `~/.kaggle/` directory. No
  authentication was configured or credentials created by these checks.
- The `hcmus-wids` kernel executed an in-memory notebook with the project's
  `.venv/bin/python`; no placeholder notebook was saved.
- Validator checks passed on synthetic fixtures, including input byte preservation.
  The official WiDS CSV remains unavailable; its validation is blocked on download.
- Jupyter Book 2.1.7 generated static HTML for all three pages with the Pages
  subpath. The initial theme download timed out; the retry succeeded.
- MyST/workflow YAML, workflow shell syntax, TOC paths, dependency pins, and Git
  exclusions passed local checks. GitHub Actions and deployment were not run.
- The public repository had zero Actions workflows before setup. The unauthenticated
  Pages API returned 404, which does not establish the remote Pages settings.
