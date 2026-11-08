# Part B — Text Preprocessing

## Dataset and objective

Use [E-commerce Text Classification on Kaggle](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification),
from [Gautam's original Zenodo record](https://zenodo.org/records/3355823)
([DOI](https://doi.org/10.5281/zenodo.3355823), version 2, CC BY 4.0).
Each row pairs a product description (`text`, input) with its category (`label`, target):
**Household, Books, Clothing & Accessories, Electronics**. The application is predicting a
product category from its description. The source describes an Indian e-commerce platform;
performance in other markets or languages remains unverified.

The original headerless CSV has **50,425 rows and two columns**. Stage 01 measures one
missing text, no additional blank texts, and 22,622 redundant rows after the first occurrence
of each exact text. These are audit observations, not a cleaned replacement dataset.
The nonempty valid-label view has 50,424 rows, and the exact-unique sensitivity view has
27,802. This satisfies the assignment minimum of 10,000 examples and at least two labels.
All figures, tests and counts are computed in the notebook, with saved outputs for static HTML.

## Read and run

| Stage | Status and scope |
|---|---|
| [01 — Dataset audit and Text EDA](01_eda.ipynb) | Implemented: source/quality audit; length distributions and pairwise Mann–Whitney; class word clouds/top-50; TTR and Zipf |
| 02 — Normalization and tokenization | Planned: `02_normalization_tokenization.ipynb`; per-step normalization impact and word/sentence/character/BPE comparisons with OOV |
| 03 — Stopwords and morphology | Planned: `03_stopwords_morphology.ipynb`; stopword information/performance comparisons and stemming/lemmatization |
| 04 — Representations | Planned: `04_representations.ipynb`; BoW/TF-IDF/Word2Vec and semantic representation comparisons |

Only Stage 01 exists. **Part B and the whole assignment are not complete.** No placeholder
notebooks or links to unimplemented chapters are included.

Use a fresh project `.venv` kernel (`hcmus-wids`). The notebook runs independently from the
repository root or `book/text/`; it does not execute Part A or depend on a processed cache.
The small `src/text_data.py` helper handles only source parsing and duplicate-audit semantics;
EDA stays in the notebook. The six report sections follow Objective → Methodology →
Implementation → Results → Discussion → Conclusion, with expandable code/supporting tables.

## Data preparation and integrity

Keep the original Kaggle file at `data/raw/ecommerce/ecommerceDataset.csv`.
Stage 01 downloads only when the CSV is missing, reuses an existing archive, and never
replaces an existing CSV. Configure Kaggle authentication outside the repository. If automatic
download is unavailable, download the original `ecommerceDataset.csv` from the linked Kaggle
dataset, extract it locally and place it at that exact path. Do not use a cleaned mirror.
The README provides the CLI alternative and environment commands.

The notebook computes file size, MD5 and SHA-256 and compares them with the documented source
reference. A version mismatch is reported explicitly, without coercing observed results to
match. Empty CSV fields are missing; literal NA-like strings are preserved. Raw bytes and
raw frame remain unchanged, with a final integrity check. No raw CSV/ZIP or credentials are
committed. Saved outputs permit static builds without data or Kaggle access.

## Interpretation boundaries

Exact and canonical duplicates, and illustrative related product descriptions, motivate
leakage controls before a later split. Canonical NFKC/lowercase/whitespace keys serve this
audit only. No split, final normalization pipeline, stopword removal, morphology, vectorization
benchmark or model is produced here. Lexical lowercasing is a descriptive view; digits and
stopwords remain counted.

All rows and labels inform EDA. A later holdout from this corpus is an **internal post-EDA
assessment**, not an unobserved external test. Duplicate removal does not guarantee independence;
Mann–Whitney p-values retain that calibration limit. Word lengths are not model subword lengths,
raw TTR is size-sensitive, and a descriptive Zipf fit does not prove a power law.
