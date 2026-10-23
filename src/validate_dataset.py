"""Read-only structural validation of the official WiDS 2024 Challenge #1 CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TARGET = "DiagPeriodL90D"
IDENTIFIER = "patient_id"
SENTINELS = {"", "na", "n/a", "nan", "null", "none", "unknown", "missing", "?", "-", "--", "not available", "not reported", "-9", "-99", "-999", "-9999", "999", "9999"}


def find_training_csv(raw_dir: Path) -> Path:
    """Identify by schema, regardless of filename or extension capitalization."""
    candidates = []
    failures = []
    for path in sorted(raw_dir.rglob("*")):
        if not path.is_file() or path.suffix.casefold() != ".csv":
            continue
        try:
            columns = pd.read_csv(path, nrows=0).columns
        except (OSError, ValueError, pd.errors.ParserError) as exc:
            failures.append(f"{path.name}: {type(exc).__name__}")
            continue
        if {TARGET, IDENTIFIER}.issubset(columns):
            candidates.append(path)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        raise ValueError("Multiple training CSVs match; choose one with --csv: " + ", ".join(str(p) for p in candidates))
    detail = f" Unreadable headers: {'; '.join(failures)}." if failures else ""
    raise FileNotFoundError(
        f"No CSV containing {TARGET} and {IDENTIFIER} found in {raw_dir}. "
        "Download and extract widsdatathon2024-challenge1, or use --csv PATH." + detail
    )


def positive_int(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return number


def validate(path: Path, args: argparse.Namespace) -> bool:
    frame = pd.read_csv(path)
    print(f"Training CSV: {path}")
    print(f"Rows: {len(frame):,}; columns: {len(frame.columns):,}")
    print(f"DataFrame memory (deep): {frame.memory_usage(index=True, deep=True).sum() / 1024**2:.2f} MiB")
    required = {TARGET, IDENTIFIER}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("The training CSV has no data rows")

    print("\nTarget class distribution (including missing):")
    print(frame[TARGET].value_counts(dropna=False).to_string())
    binary_target = frame[TARGET].notna().all() and frame[TARGET].isin([0, 1]).all()
    print(f"Target contains only non-missing 0/1 labels: {binary_target}")
    missing_ids = int(frame[IDENTIFIER].isna().sum())
    duplicate_ids = int(frame[IDENTIFIER].dropna().duplicated().sum())
    duplicate_rows = int(frame.duplicated().sum())
    print(f"Missing identifiers: {missing_ids:,}")
    print(f"Duplicated non-missing identifiers (after first occurrence): {duplicate_ids:,}")
    print(f"Duplicate rows (after first occurrence): {duplicate_rows:,}")

    print("\nMissing values per column (%; pandas default NA recognition):")
    print(frame.isna().mean().mul(100).sort_values(ascending=False).to_string(float_format=lambda x: f"{x:.2f}"))
    features = frame.drop(columns=[TARGET, IDENTIFIER])
    numerical = list(features.select_dtypes(include="number").columns)
    categorical = [name for name in features if name not in numerical]
    print(f"\nFeature columns, excluding target and identifier: numerical={len(numerical)}, categorical={len(categorical)}")
    print("Types are inferred from CSV; numeric category codes may require later semantic review.")

    cardinalities = frame.nunique(dropna=True)
    print("\nAll-missing columns:", ", ".join(cardinalities[cardinalities == 0].index) or "none")
    print("Constant columns (one distinct non-missing value):", ", ".join(cardinalities[cardinalities == 1].index) or "none")
    print(f"Near-constant columns (dominant non-missing value >= {args.near_constant:.1%}, excluding constants):")
    near = []
    for name in frame:
        if cardinalities[name] > 1:
            share = frame[name].value_counts(normalize=True).iloc[0]
            if share >= args.near_constant:
                near.append(f"  {name}: {share:.2%}")
    print("\n".join(near) or "  none")
    print("\nCategorical feature cardinality (non-missing distinct values):")
    print(features[categorical].nunique(dropna=True).sort_values(ascending=False).to_string() if categorical else "none")

    # A separate lexical read preserves tokens that pandas would already call NA.
    # No replacements, saved data, or raw row values are produced.
    lexical = pd.read_csv(path, dtype="string", keep_default_na=False)
    print("\nPotential missing-value sentinels (counts only; not proof of missingness):")
    found = False
    for name in lexical:
        counts = lexical[name].str.strip().str.casefold().value_counts()
        matches = counts[counts.index.isin(SENTINELS)]
        if not matches.empty:
            found = True
            print(f"  {name}: " + ", ".join(f"{token!r}={int(count)}" for token, count in matches.items()))
    if not found:
        print("  none from the documented candidate token set")
    print("Sentinels such as 999 may be legitimate. Domain-specific codes are not exhaustively detected.")

    schema_ok = bool(binary_target and not missing_ids and not duplicate_ids and not duplicate_rows)
    print(f"\nBasic training-schema/integrity checks: {'PASS' if schema_ok else 'FAIL'}")
    measurements = {"rows": len(frame), "features": len(features.columns), "numeric": len(numerical), "categorical": len(categorical)}
    thresholds = {name: getattr(args, f"min_{name}") for name in measurements}
    rubric_ok = True
    for name, minimum in thresholds.items():
        if minimum is not None:
            passed = measurements[name] >= minimum
            rubric_ok &= passed
            print(f"Minimum {name}: {measurements[name]} >= {minimum}: {'PASS' if passed else 'FAIL'}")
    if any(value is None for value in thresholds.values()):
        print("Course structural requirements: UNCONFIRMED; supply all four --min-* values from the actual rubric.")
    else:
        print(f"Course structural requirements (user-supplied thresholds): {'PASS' if rubric_ok else 'FAIL'}")
    return schema_ok and rubric_ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, help="Explicit training CSV (read-only)")
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "data/raw")
    parser.add_argument("--near-constant", type=float, default=0.95, help="Dominant non-missing value fraction (default: 0.95)")
    for name in ["rows", "features", "numeric", "categorical"]:
        parser.add_argument(f"--min-{name}", type=positive_int, help="Minimum from your course rubric; no assumed default")
    args = parser.parse_args()
    if not 0 < args.near_constant <= 1:
        parser.error("--near-constant must be in (0, 1]")
    try:
        path = args.csv if args.csv is not None else find_training_csv(args.raw_dir)
        return 0 if validate(path, args) else 1
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        print(f"Validation unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
