# Copyright 2024 John Hanley. MIT licensed.
import re
from hashlib import file_digest, sha3_224
from pathlib import Path

import pandas as pd


def fingerprint(in_file: Path, nybbles: int = 8) -> tuple[int, str]:
    """Returns the given file's size along with a truncated SHA3 hash,
    so we know we have the expected file version.
    """
    with open(in_file, "rb") as fin:
        digest = file_digest(fin, sha3_224)
    return in_file.stat().st_size, digest.hexdigest()[:nybbles]


def _clean_column_name(name: str) -> str:
    """Converts raw multi-word column name to a clean identifier."""
    xlate = str.maketrans(" ./:", "____", "()?")
    name = name.replace("$", "").strip().translate(xlate).lower()
    name = re.sub(r"__+", "_", name)
    assert re.search(r"^[a-z0-9_]+$", name), name
    return name


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={col: _clean_column_name(col) for col in df.columns})
