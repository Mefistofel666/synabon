import os
import base64
import hashlib
from typing import List

import pandas as pd


def salt_generator(salt: str = "default") -> str:
    salt = os.urandom(8)
    return base64.b64encode(salt).decode("ascii")


def make_buckets(
    df: pd.DataFrame,
    id_column: str,
    n_buckets: int | List[int] = 100,
    user_salt: str = None,
) -> pd.DataFrame:
    """Splitting on A/B using sha256."""
    salt = user_salt if user_salt else salt_generator()
    df["hash"] = (df[id_column].astype(str) + "#" + salt).apply(
        lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()
    )
    df["hash_int_part"] = df["hash"].str.slice(start=-6).apply(int, base=16)
    if isinstance(n_buckets, int):
        df["group"] = df["hash_int_part"] % n_buckets
    elif isinstance(n_buckets, list):
        for idx, n_buckets in enumerate(n_buckets):
            df["group" + str(idx)] = df["hash_int_part"] % n_buckets

    del df["hash_int_part"]
    del df["hash"]
