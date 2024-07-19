#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path

import pandas as pd
import typer

from lib.util import fingerprint

CSV_DIR = Path("~/Desktop/lafco").expanduser()


def get_voter() -> pd.DataFrame:
    voter_tsv = CSV_DIR / "2024-06-21_EPASD_Raw_Registered_Voters.txt"
    assert (6_270_079, "24977496") == fingerprint(voter_tsv), fingerprint(voter_tsv)
    voter = pd.read_csv(voter_tsv, sep="\t", low_memory=False)
    assert 114 == len(voter.columns)
    voter = voter.dropna(axis=1, how="all")  # 19 columns are uninformative
    assert 95 == len(voter.columns)
    assert 9679 == len(voter)
    return voter


def get_protest() -> pd.DataFrame:
    protest_csv = CSV_DIR / "2024-05-21_qry_EPASD_APNs_Landowner_Protests.csv"
    assert (353_809, "3acdad47") == fingerprint(protest_csv), fingerprint(protest_csv)
    protest = pd.read_csv(protest_csv)
    assert (4273, 6) == protest.shape
    return protest


def report() -> None:
    voter = get_voter()
    protest = get_protest()
    protest["phone"] = voter.PhoneNumber
    protest["email"] = voter.EmailAddress
    print(protest)


if __name__ == "__main__":
    typer.run(report)
