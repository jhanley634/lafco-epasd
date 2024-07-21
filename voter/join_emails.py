#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import defaultdict
from pathlib import Path

import pandas as pd
import typer

from lib.util import clean_column_names, fingerprint

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


def _get_contacts(voter: pd.DataFrame) -> tuple[dict[str, str], dict[str, str]]:
    voter = voter.fillna("")
    addr_to_phone: dict[str, str] = defaultdict(str)
    addr_to_email: dict[str, str] = defaultdict(str)
    for row in voter.itertuples():
        addr = f"{row.addr}"
        addr_to_phone[addr] = addr_to_phone[addr] or f"{row.phone}"
        addr_to_email[addr] = addr_to_email[addr] or f"{row.email}"
    return addr_to_phone, addr_to_email


def get_protest() -> pd.DataFrame:
    protest_csv = CSV_DIR / "2024-05-21_qry_EPASD_APNs_Landowner_Protests.csv"
    assert (353_809, "3acdad47") == fingerprint(protest_csv), fingerprint(protest_csv)
    protest = pd.read_csv(protest_csv)
    assert (4273, 6) == protest.shape
    protest = clean_column_names(protest)
    return protest


def report() -> None:
    voter = get_voter()
    voter["addr"] = voter.ResidenceAddress.str.rstrip().str.upper()
    voter = voter.rename(columns={"PhoneNumber": "phone"})
    voter = voter.rename(columns={"EmailAddress": "email"})
    voter["email"] = voter.email.str.lower()
    voter = voter[["addr", "phone", "email"]]
    addr_to_phone, addr_to_email = _get_contacts(voter)

    protest = get_protest()
    protest = protest.rename(columns={"epa_address": "addr"})
    protest = protest.dropna(subset=["addr"])
    assert 4162 == len(protest), len(protest)
    protest = protest.drop_duplicates(subset=["addr"])
    assert 3664 == len(protest), len(protest)
    joined = protest.copy()
    joined["phone"] = protest.addr.map(lambda addr: addr_to_phone[addr])
    joined["email"] = protest.addr.map(lambda addr: addr_to_email[addr])

    fname = "2024-05-21_qry_EPASD_APNs_Landowner_Protests_with_phone_email.csv"
    fspec = Path("/tmp") / fname
    joined.to_csv(fspec, index=False)
    print(f"Wrote {len(joined)} rows to {fspec}")
    assert (377_083, "463771c6") == fingerprint(fspec), fingerprint(fspec)


if __name__ == "__main__":
    with pd.option_context("display.max_columns", None):
        typer.run(report)
