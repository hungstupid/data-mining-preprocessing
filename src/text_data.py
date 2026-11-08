"""Small, read-only source and duplicate helpers for the E-commerce text chapters."""
from pathlib import Path
import unicodedata

import pandas as pd

LABELS = ("Household", "Books", "Clothing & Accessories", "Electronics")


def read_ecommerce(path: str | Path) -> pd.DataFrame:
    """Read the original headerless two-column CSV; preserve literal NA-like text.

    Only empty CSV fields become pd.NA. Whitespace-only strings stay unchanged.
    Read without names first so malformed extra columns cannot become a silent index.
    """
    frame = pd.read_csv(path, header=None, dtype="string", keep_default_na=False,
                        na_values=[""], encoding="utf-8", on_bad_lines="error")
    if frame.shape[1] != 2:
        raise ValueError(f"Expected two headerless columns, found {frame.shape[1]}")
    frame.columns = ["label", "text"]
    return frame


def canonical_key(text: str) -> str:
    """Audit only: NFKC, lowercase, collapse Unicode whitespace; keep numbers/punctuation.

    NFKC may fold compatibility glyphs (e.g. full-width digits); it is not lossless.
    """
    return " ".join(unicodedata.normalize("NFKC", text).lower().split())


def duplicate_groups(frame: pd.DataFrame, keys: pd.Series) -> pd.DataFrame:
    """One row per non-null key; distinguish group size from redundant row count.

    Callers select eligible rows. Missing labels are excluded from distinct-label counts
    and are audited separately; a group conflicts only with >1 observed label.
    """
    keyed = frame.loc[keys.index, ["label"]].assign(key=keys)
    return keyed.groupby("key", sort=False, dropna=True).agg(
        rows=("label", "size"), labels=("label", "nunique"))
