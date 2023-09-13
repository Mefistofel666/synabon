from datetime import datetime
from typing import Tuple

import numpy as np
import pandas as pd

from .utils import random_date


class DataGenerator:
    def __init__(
        self,
        n_unique_ids: int,
        n_rows_per_id: int,
        start_dt: datetime,
        end_dt: datetime,
        mu: float = 0,
        sigma: float = 1,
    ) -> None:
        self.n_unique_ids = n_unique_ids
        self.n_rows_per_id = n_rows_per_id
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.mu = mu
        self.sigma = sigma

        self.total_rows = n_rows_per_id * n_unique_ids

    def get_normal(self) -> Tuple[np.ndarray, np.ndarray]:
        size = (2, self.total_rows)
        s1, s2 = np.random.normal(self.mu, self.sigma, size=size)
        return s1, s2

    def generate_data(
        self,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        sample_1, sample_2 = self.get_normal()
        sample_1.sort()
        sample_2.sort()

        data_1 = []
        data_2 = []
        for i in range(self.n_unique_ids):
            start, end = i * self.n_rows_per_id, (i + 1) * self.n_rows_per_id
            vals_1 = sample_1[start:end]
            vals_2 = sample_2[start:end]
            for x in vals_1:
                date = random_date(self.start_dt, self.end_dt)
                data_1.append([i, x, date])
            for x in vals_2:
                date = random_date(self.start_dt, self.end_dt)
                data_2.append([i, x, date])

        np.random.shuffle(data_1)
        np.random.shuffle(data_2)

        df_1 = pd.DataFrame(data_1, columns=["user_id", "money", "date"])
        df_2 = pd.DataFrame(data_2, columns=["user_id", "money", "date"])
        return df_1, df_2
