"""Read-only source, duplicate and fixed-split helpers for the E-commerce text chapters."""
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
    """Fixed audit/group key: NFKC, lowercase, collapse whitespace; keep numbers/punctuation.

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


def make_text_protocol(raw: pd.DataFrame, *, test_size: float = 0.2, seed: int = 42) -> dict:
    """Recreate the fixed text corpus/split from raw CSV records, without learned state.

    row_id is the zero-based CSV record position (not a physical line number: quoted
    records may contain newlines). Remove unusable rows, all conflicting canonical
    groups, then keep the first exact and canonical occurrence in file order.
    Stratify canonical-unique records by label. No normalization replaces raw text.
    Returns corpus/train/test frames, sequential flow counts and conflict-group counts.
    """
    from sklearn.model_selection import train_test_split

    frame = raw[["label", "text"]].reset_index(drop=True).rename_axis("row_id").reset_index()
    flow = [{"step": "raw CSV", "removed_rows": 0, "remaining_rows": len(frame)}]

    def remove(mask, step):
        nonlocal frame
        removed = int(mask.sum())
        frame = frame.loc[~mask].copy()
        flow.append({"step": step, "removed_rows": removed, "remaining_rows": len(frame)})

    remove(frame.text.isna() | frame.text.str.strip().eq("").fillna(False), "missing / blank text")
    remove(~frame.label.isin(LABELS), "missing / invalid label")
    frame["canonical_key"] = frame.text.map(canonical_key)
    groups = frame.groupby("canonical_key", sort=False).agg(
        rows=("row_id", "size"), labels=("label", "nunique"))
    conflicts = groups.loc[groups.labels.gt(1)].copy()
    remove(frame.canonical_key.isin(conflicts.index), "all conflicting-label canonical groups")
    remove(frame.text.duplicated(keep="first"), "exact duplicate rows after first")
    remove(frame.canonical_key.duplicated(keep="first"), "additional canonical duplicates after first")
    corpus = frame.sort_values("row_id").reset_index(drop=True)
    train, test = train_test_split(corpus, test_size=test_size, random_state=seed,
                                   shuffle=True, stratify=corpus.label)
    train = train.sort_values("row_id").reset_index(drop=True)
    test = test.sort_values("row_id").reset_index(drop=True)
    assert corpus.row_id.is_unique and corpus.canonical_key.is_unique
    assert set(train.row_id).isdisjoint(test.row_id)
    assert set(train.canonical_key).isdisjoint(test.canonical_key)
    return {"corpus": corpus, "train": train, "test": test,
            "flow": pd.DataFrame(flow), "conflicts": conflicts}
