# Appendix — Supporting Evidence and Verification

The seven notebooks are the sole computational sources. The embeds below reuse their saved
outputs through native MyST labels; they do not execute code or create duplicate experiments.
Open the source chapter to inspect complete code, variables and fitted objects. Every chapter
starts from raw data in an independent kernel; the shared module contains no fit at import time.

## Original six-feature imputation scope

This experiment remains separate from the joint 69-feature benchmark. Different matrices/masks
prevent interpreting differences between aggregate scores as an effect of feature expansion.

```{embed} #stage02-cell-19
:remove-input: true
:remove-output: false
```

## Numerical and leakage correctness

Checks remain in the corresponding notebook's Conclusion or supporting cells. They include
known-value fixtures, column/index alignment, deterministic repeats, nonmutation, raw checksums,
ZIP separation, own-label/prior leakage tests, full-Pipeline reproduction and sampler traps.
Cross-chapter regression additionally compares original result arrays and actual fold/partition
hashes; cross-kernel foreign-object assertions are replaced by this explicit comparison.

### Imputation

```{embed} #stage02-cell-37
:remove-input: true
:remove-output: false
```

### Outliers

```{embed} #stage03-cell-71
:remove-input: true
:remove-output: false
```

### Scaling

```{embed} #stage04-cell-91
:remove-input: true
:remove-output: false
```

### Encoding and Target OOF

```{embed} #stage05-cell-111
:remove-input: true
:remove-output: false
```

### Feature selection and pipeline correctness

```{embed} #stage06-cell-131
:remove-input: true
:remove-output: false
```

### Class imbalance and held-prediction traps

```{embed} #stage07-cell-147
:remove-input: true
:remove-output: false
```

## Complete numerical evidence

All 69 normality rows, all three 69×69 correlation/paired-N matrices, 17 strong pairs,
full imputation/per-feature errors, nine detectors/621 KS comparisons, 414 scaling summaries,
145 scoped VIF rows, 110 selections and 20 sampler evaluations remain in their chapter outputs.
Large tables use expandable containers rather than disappearing from the book.

The current repository audit is a compact criterion→evidence matrix. Historical development
and deployment narratives are preserved in `docs/history/RUBRIC_AUDIT_82617d1.md` and Git;
they are not the current experimental specification.
