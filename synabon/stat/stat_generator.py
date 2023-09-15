import uuid
from datetime import datetime, timedelta
from random import randrange
from typing import List

import numpy as np
import pandas as pd


def get_random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_objects_ids(
    n_unique_objects: int,
    n_records_per_object: int,
    column_name: str = "object_id",
) -> pd.DataFrame:
    data = []
    for _ in range(n_unique_objects):
        curr_uuid = uuid.uuid4()
        data += [curr_uuid for _ in range(n_records_per_object)]
    np.random.shuffle(data)
    return pd.DataFrame(data, columns=[column_name])


def add_date(
    data: pd.DataFrame,
    start_dt: datetime,
    end_dt: datetime,
    column_name: str,
) -> pd.DataFrame:
    dates = [get_random_date(start_dt, end_dt) for _ in range(data.shape[0])]
    data[column_name] = dates
    return data


def add_category(
    data: pd.DataFrame, values: List[str], column_name: str
) -> pd.DataFrame:
    data[column_name] = np.random.choice(values, data.shape[0])
    return data


def add_continuous(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    data[column_name] = np.random.normal(10, 1, data.shape[0])
    return data
