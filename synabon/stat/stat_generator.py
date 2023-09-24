import uuid
from datetime import datetime, timedelta
from random import randrange
from typing import List, Tuple

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
    data: pd.DataFrame,
    values: List[str],
    column_name: str,
    distribution: List[float] = None,
) -> pd.DataFrame:
    if (sum(distribution) != 1) or (len(distribution) != len(values)):
        raise ValueError("Incorrent distribution!")
    data[column_name] = np.random.choice(values, data.shape[0], p=distribution)
    return data


def add_normal(
    data: pd.DataFrame, mu: float, sigma: float, column_name: str
) -> pd.DataFrame:
    data[column_name] = np.random.normal(mu, sigma, data.shape[0])
    return data


def add_exponential(data: pd.DataFrame, scale: float, column_name: str) -> pd.DataFrame:
    data[column_name] = np.random.exponential(scale, data.shape[0])
    return data


def transform_continuous(value: float, effect_size: float = None) -> pd.Series:
    if effect_size:
        value *= effect_size
    return value


def get_experiment_data(
    control: pd.DataFrame,
    treatment: pd.DataFrame,
    target_column: str,
    date_column: str,
    experiment_duration: timedelta,
    effect_size: float,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    control_exp = control
    control_exp[target_column] = control_exp[target_column].apply(
        lambda x: transform_continuous(x)
    )
    control_exp[target_column] += np.random.normal(0, 1, size=control_exp.shape[0])

    treatment_exp = treatment
    treatment_exp[target_column] = treatment_exp[target_column].apply(
        lambda x: transform_continuous(x, effect_size)
    )
    treatment_exp[target_column] += np.random.normal(0, 1, size=treatment_exp.shape[0])

    max_control_dt = control_exp[date_column].max()
    max_treatment_dt = treatment_exp[date_column].max()
    max_dt = max(max_control_dt, max_treatment_dt)

    start_dt = max_dt + timedelta(days=1)
    end_dt = start_dt + experiment_duration

    control_exp = add_date(
        data=control_exp, start_dt=start_dt, end_dt=end_dt, column_name=date_column
    )
    treatment_exp = add_date(
        data=treatment_exp, start_dt=start_dt, end_dt=end_dt, column_name=date_column
    )

    return control_exp, treatment_exp
