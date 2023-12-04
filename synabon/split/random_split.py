from typing import List

import pandas as pd
import numpy as np


def random_split(
    df: pd.DataFrame, id_column: str, group_size: int = None, groups_number: int = 2
) -> List[np.ndarray]:
    """
    Simple random uniform split approach.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe used for groups sampling.
    group_size : int
        Sampling size of groups.
    grops_number : int, default: ``2``
        Number of groups to be sampled.

    Returns
    -------
    groups : List[np.ndarray]
       List of arrays with indices for each groups.
    """
    ids = df[id_column].unique()
    if not group_size:
        group_size = int(len(ids) / 2)
    groups_ids = np.random.choice(ids, size=(groups_number, group_size), replace=False)

    groups = []
    for group_ids in groups_ids:
        group_df = df.set_index(id_column).loc[group_ids].reset_index()
        groups.append(group_df)
    return groups
