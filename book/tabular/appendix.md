# Appendix — Supporting Results and Reproducibility

The seven notebooks are the computational sources. The embed below reuses a saved output
through a native MyST label; it does not execute code or duplicate an experiment.

## Original six-feature imputation scope

This experiment remains separate from the joint 69-feature benchmark. Different matrices/masks
prevent interpreting aggregate-score differences as an effect of feature expansion.

```{embed} #stage02-cell-19
:remove-input: true
:remove-output: false
```

## Separate tests

Run from the repository root:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

`tests/` covers the Little implementation, input/split/known-value preservation, analytic
masking/RMSE, strict outlier boundaries, Jaccard/KS/elbow, Levene, binary codes, Target OOF
label/prior leakage, VIF, fold-local preprocessing, selector routing and prediction-time
sampling traps. The tests use synthetic fixtures; no private CSV or full notebook run is
required. Notebook-method tests load only the actual named function definitions, without
executing other cells or copying algorithm implementations.

The notebooks keep essential schema/semantic boundaries, disjoint ZIPs, observed-only masks,
finite outputs, CV coverage, convergence and one final raw-file integrity check per chapter.
Repeated full-data verification fits, matrix fingerprints and test ledgers are removed.
See the [Part A guide](index.md) for independent Run All and CSV-free publication.

## Complete numerical evidence

All 69 normality rows, all three 69×69 correlation/paired-N matrices, 17 strong pairs,
full imputation/per-feature errors, nine detectors/621 KS comparisons, 414 scaling summaries,
145 scoped VIF rows, 110 selection evaluations and 20 sampler evaluations remain available.
Large tables are expandable. Both imputation scopes retain all seven scored configurations,
including three ten-round MICE draws.
