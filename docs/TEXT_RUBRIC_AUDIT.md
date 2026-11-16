# Part B — Text Rubric Evidence

Audit date: **2026-11-16**. Reviewed repository baseline:
`da488b35ebb233f3968faae7599e051bd308fbcd`; local `main` matched `origin/main`, with a clean
initial tree. The original audit recorded local Stage 04 verification before publication. The final review
also verifies the published baseline f33849e; see the [submission audit](../RUBRIC_AUDIT.md).
The root `RUBRIC_AUDIT.md` now consolidates the submission review across both selected parts.

**PASS** means implemented with inspected saved evidence and stated checks; **PARTIAL** means
an explicit unresolved interpretation condition. Neither predicts an awarded mark or
removes scientific limits. No 10/10 or external deployment-validity claim is made.

## Official criterion interpretation

The [official HCMUS assignment](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)
was retrieved on the audit date. Its text-data, implementation and scoring sections require:

- At least 10,000 examples and two labels; raw EDA with length/Mann–Whitney, class word clouds/
  top-50, TTR and Zipf.
- Normalization step effects and four tokenizer/OOV comparisons; stopword vocabulary/MI/Naive
  Bayes; Porter/Snowball/WordNet collision rates and Logistic Regression five-fold CV.
- BoW, TF-IDF word n-grams n=1,2,3 and project-trained Word2Vec; dimensions/sparsity,
  within/between-class cosine, t-SNE and silhouette.
- Sentence Transformer is marked **[Nâng cao]** in descriptive requirements, but the scoring
  table's vectorization row explicitly includes **Sentence Transformer**. It is implemented,
  including K-Means/silhouette and Linear SVM comparisons, rather than treated as dispensable.
- The general allowed-library list omits gensim while explicitly requesting Word2Vec.
  Standard gensim is used transparently for that method; this is an interpretation, not
  fabricated instructor authorization. PyTorch is explicitly in the general list.

TF-IDF ranges `(1,1)`, `(1,2)`, `(1,3)` include all three requested orders, as specified by the
Stage 04 task. Actual retained feature composition confirms bigrams/trigrams are constructed;
using a callable vectorizer analyzer would incorrectly bypass this step and is avoided.

## Criterion → evidence

| Criterion | File / section | Actual evidence | Status | Limitation |
|---|---|---|---|---|
| Dataset selection / four-class integrity | [Stage 01 source audit](../book/text/01_eda.ipynb); [Stage 04 source/folds](../book/text/04_representations.ipynb) | Headerless 50,425×2; four labels; 27,752 eligible canonical-unique records; 22,201 TRAIN / 5,551 internal assessment; source/outer/fold fingerprints match | PASS | Scraped product descriptions are not representative of every market/language |
| Raw quality / exact and canonical duplicates | Stage 01 quality audit; shared `src/text_data.py` | One missing text; 22,622 exact redundant rows; 50 additional canonical redundant rows; whole conflicting groups excluded by protocol, none observed | PASS | Product variants/near duplicates remain; canonicalization is not full family resolution |
| Length EDA / Mann–Whitney | Stage 01 lengths and pairwise tests | Words/characters, class N/mean/SD/median/quartiles/P95/max; 12 primary + 12 exact-dedup sensitivity tests; U, raw/Holm p, signed effect sizes | PASS | Repeated/related products weaken independence and p-value calibration; not a median-only test |
| Four word clouds / top-50 / TTR | Stage 01 lexical view | Four clouds and four complete 50-row frequency tables; corpus V/T=81,531/5,918,452; shared 100,000-token budget, seed 42 | PASS | TTR depends on sample size/token definition; stopwords intentionally retained in EDA |
| Zipf | Stage 01 rank-frequency | Corpus and class log-log curves; rank 10–10,000 slope −1.173, R²=.9772; −1 reference and singleton analysis | PASS | Descriptive regression does not prove a power-law generator |
| Normalization and impact | [Stage 02](../book/text/02_normalization_tokenization.ipynb); `src/text_preprocessing.py` | Ten declared steps; document/type/set/length changes; 72,746→72,299 TRAIN lexical types; standalone-number sensitivity changes 13,785 texts | PASS | Numbers retained by default; known `@home` deletion/identifier fragmentation risks remain |
| Four tokenizers and OOV | Stage 02 common light-input benchmark | Word/Punkt sentence/Unicode character/TRAIN-trained byte-BPE; same input and occurrence OOV; word 3.0714%, sentence 75.6723%, character .0029%, BPE 0% | PASS | Units differ; byte coverage explains BPE OOV=0 and does not prove classifier superiority |
| Stopword vocabulary / MI / NB | [Stage 03 A1–A3](../book/text/03_stopwords_morphology.ipynb) | 180 types and 820,416 occurrences removed; binary-presence MI in nats; mean .00041228→.00039878; NB F1 .938031→.939891, all five scores/SD shown | PASS | Mean MI changes averaging set; removed stopwords can be informative; CV gain is small |
| Morphology collision / LR five-fold CV | Stage 03 B1–B2 | None/Porter/Snowball/noun-WordNet; compression 0/20.55/20.72/7.47%; collision membership separate; LR means .947950/.948559/.948589/.948760 | PASS | Stems can conflate senses; noun-default WordNet is not POS-aware; small differences are not certainty |
| Frozen data/CV and fitting boundaries | Stage 04 source and Methodology; targeted tests | Same 11 normalized duplicate groups/12 redundant TRAIN rows; exact five Stage 03 validation hashes; all sparse vocabularies/IDF/SVMs fit inside each fitting fold | PASS | Group equality misses product families; full-file EDA exposure disclosed; no assessment classifier result |
| BoW and TF-IDF n=1,2,3 | Stage 04 §1 | Four actual matrices; min_df=2/cap 30,000; eligible cumulative candidates 36,099→299,680→631,052; trigram-range retained 9,661 uni / 15,212 bi / 5,127 tri features | PASS | Fixed cap and frequency threshold constrain coverage; larger ranges displace unigrams |
| TRAIN-trained Word2Vec | Stage 04 §2 | Real CBOW, D=100, 10 epochs, workers=1/stable hash/seed 42; 40,880 learned words; occurrence-weighted mean pooling; 1.233% TRAIN occurrence OOV; one zero document | PASS | No Word2Vec CV is reported; pooling loses order/sense and may emphasize common directions |
| Word2Vec numerical compatibility | Stage 04 §2; `word2vec_numeric_guard`; test | Unmodified PyPI 4.4.0 −1→0 bug reproduced; exact source fix `ecf22c266f3b8930610114c149d8991ed14e2a16`; four scoring symmetry cases pass; finite loss/weights and nonzero updates checked | PASS | Fix is from an open/unmerged third-party PR; source build needs Git/compiler; cross-platform build is not certified here |
| General library-list ambiguity | Methodology and README | Word2Vec implementation and gensim interpretation explicitly disclosed; no unrelated prior pin changed | PARTIAL | Instructor acceptance of the broad library-list interpretation is not independently confirmed |
| Dimensions / sparsity / storage | Stage 04 §4 | Every N×D, nnz, 1−nnz/(ND), CSR/dense buffer bytes and zero rows; sparse 99.63–99.77%; dense W2V 8.47 MiB, MiniLM 32.52 MiB | PASS | Buffer sizes exclude Python vocabulary objects/model weights; numerical zeros differ from a sparse model |
| Same/different cosine | Stage 04 §5 | Exactly 2,400 same + 2,400 different class-controlled pairs, seed 42, no self/duplicate pairs; same IDs; means/medians/quartiles/SD and gap | PASS | Pair quotas change class weighting; zero-vector cosine is a disclosed convention; no significance claim |
| t-SNE / true-label silhouette | Stage 04 §6–7 | Same 1,200 TRAIN IDs, 300 per class; six SVD(50)→unit-norm→t-SNE panels; original-space cosine plus Euclidean sensitivity | PASS | Balanced subset changes prevalence; t-SNE distortions/seed/perplexity affect appearance; no silhouette on 2D |
| Actual Sentence Transformer | Stage 04 §3 | Real all-MiniLM-L6-v2, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, CPU/float32/batch 32/frozen/unit vectors; D=384; safetensors hash | PASS | Public pretraining overlap/domain mismatch unknown; 2,864 TRAIN texts (12.90%) exceed 256 subwords |
| K-Means TF-IDF vs Sentence Transformer | Stage 04 §6 | Same IDs/unit rows/K=4/10 starts/seed 42; true vs cluster cosine S: TF-IDF .011249/.011900, MiniLM .085719/.104771; ARI .326454/.727192; all cluster sizes | PASS | K=4 does not identify categories; Euclidean K-Means objective differs from cosine evaluation |
| Controlled Linear SVM | Stage 04 §8 | New 25 fits; BoW .953151±.002563, TF-IDF 1 .957514±.001594, 1–2 .955232±.002086, 1–3 .954483±.002101, MiniLM .937824±.003783 macro-F1; all scores/accuracy/paired differences | PASS | Fixed C/input/cap, not optimized rankings; dependent-fold SD is not a CI; zero convergence warnings |
| Mathematical explanations and interpretation | Stage 04 six sections | BoW/TF-IDF, cosine, CBOW negative sampling, pooling, silhouette; encoder/classifier distinction and actual rank differences | PASS | No causal, universal superiority or guaranteed-grade claim |
| Code/tests/reproduction | `tests/test_text_stage04.py`, full suite, README | 48 tests pass; known n-grams, sparse/dense stats, cosine, sampling, OOV/zeros, validation-only vocabulary/IDF sentinel, invalid silhouette, BLAS regression; fresh root Run All | PASS | Unit tests avoid real transformer download; actual model integration is checked separately |
| Static HTML and path handling | Stage 04 outputs, MyST and verification | Root Run All; fresh `book/text/` imports/source/folds + real local-model encoding; both HTML builds pass; browser renders all nine figures and actual tables | PASS | `book/text/` check is a fresh-kernel path/model integration smoke, not a second full experiment run; remote publication is separate |
| Remote publication of Stage 04 | Existing deployment workflow, unchanged | [Pages run for f33849e](https://github.com/hungstupid/data-mining-preprocessing/actions/runs/43894173758) succeeded; public chapter, both SVM values and all nine images verified in Chrome | PASS | New local documentation is not published by this review |

## Scientific and dependency limitations

The library-policy ambiguity is distinct from successful implementation. The essential
[gensim correctness fix](https://github.com/piskvorky/gensim/pull/3668) changes only native
BLAS exception declarations, not the training objective. We pin the reviewed commit, verify
its installed origin and fail a negative-one regression rather than accepting erroneous
training. Earlier NumPy/SciPy/Part A pins remain unchanged. This source dependency is unmerged;
compiler availability and public source/model availability remain reproduction prerequisites.

Category geometry, unsupervised cohesion and supervised prediction have different rankings.
Word2Vec's larger cosine gap/cluster silhouette does not imply closer category agreement than
MiniLM; MiniLM's better K-Means/category geometry does not outrank TF-IDF's fixed-C SVM F1.
N-gram cap competition, generic pretraining and measured truncation are plausible limitations,
not demonstrated causal explanations of the score differences. Stage 04 does not evaluate or
select on the outer assessment and supplies no external deployment guarantee.

## Verification record

- Corrected-build fresh root Run All: all 13 code cells, six representations, nine figures,
  all 25 new fold-local SVM fits and zero classifier convergence warnings saved.
- `book/text/` fresh-kernel path smoke: authoritative raw/partition/fold checks, corrected BLAS
  guard and real two-document CPU encoding from the exact local MiniLM revision pass.
- `.venv/bin/python -m unittest discover -s tests -v`: **48 tests pass**.
- `.venv/bin/python -m pip check`: passes. Prior pinned package set is preserved; final runtime
  lock matches installed environment, including the exact corrected gensim source pin.
- Earlier Stage 01–03 code and all saved scientific outputs are unchanged; only their final
  roadmap prose links to the now-implemented next chapters. Part A/raw protocol/workflow remain
  byte-unchanged in the diff.
- `BASE_URL=/data-mining-preprocessing .venv/bin/jupyter book build --html`: PASS,
  16 pages including the new representations chapter and this audit. Existing Node theme
  emits a `url.parse()` deprecation warning; it does not fail the build.
- A second source-only temporary copy, excluding all `data/`, `.cache/` and credentials,
  builds successfully with `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, an absent `HF_HOME`,
  and `CUDA_VISIBLE_DEVICES=''`. Stage 04, this audit, Stage 03 and Part A HTML pages exist;
  no model cache is created. Saved outputs, rather than execution at build time, provide evidence.
- Local Chrome/Playwright inspection at the configured base URL: all nine figure images have
  nonzero natural dimensions; all computed tables render; six notebook sections and chapter
  navigation are present. No JavaScript errors, HTTP failures or KaTeX errors; all nine distinct
  internal link targets return successfully. At 1,440 px, neither chapter nor audit overflows
  the page horizontally. Cosine, MiniLM t-SNE and paired-SVM figures were also visually inspected.
