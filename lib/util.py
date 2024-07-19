# Copyright 2024 John Hanley. MIT licensed.
from hashlib import file_digest, sha3_224
from pathlib import Path


def fingerprint(in_file: Path, nybbles: int = 8) -> tuple[int, str]:
    """Returns the given file's size along with a truncated SHA3 hash,
    so we know we have the expected file version.
    """
    with open(in_file, "rb") as fin:
        digest = file_digest(fin, sha3_224)
    return in_file.stat().st_size, digest.hexdigest()[:nybbles]
