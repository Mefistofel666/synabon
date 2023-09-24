from datetime import datetime, timedelta
from random import randrange
import uuid
from typing import Callable, List

import numpy as np
import pandas as pd


class UserGenerator:
    def __init__(
        self,
        n_users: int,
        n_interactions: int,
    ) -> None:
        self.n_users = n_users
        self.n_interactions = n_interactions

        self.default_columns = [
            "user_id",
            "user_balance",
            "interaction_sum",
            "interaction_type",
            "date",
        ]

    @staticmethod
    def __get_random_date(start: datetime, end: datetime) -> datetime:
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def __get_transactions(
        self, start_balance: float, end_balance: float
    ) -> np.ndarray:
        low = -start_balance / self.n_interactions
        high = start_balance / self.n_interactions
        transactions = np.random.uniform(low=low, high=high, size=self.n_interactions)
        transactions = (
            transactions / np.sum(transactions, axis=0) * (end_balance - start_balance)
        )
        return transactions

    def __get_record(
        self,
        user_id: uuid.UUID,
        user_balance: float,
        interaction_sum: float,
        interaction_type: str,
        interaction_dt: datetime,
    ) -> List:
        return [
            user_id,
            user_balance,
            interaction_sum,
            interaction_type,
            interaction_dt,
        ]

    def __get_random_id(self) -> uuid.UUID:
        return uuid.uuid4()

    def __get_user_end_balance(self, start_balance: float) -> float:
        return np.random.normal(loc=start_balance, scale=10)

    def get_data(
        self, balance_generator: Callable, start_dt: datetime, end_dt: datetime
    ) -> pd.DataFrame:
        data = []
        for _ in range(self.n_users):
            user_id = self.__get_random_id()
            user_start_balance = balance_generator()
            user_end_balance = self.__get_user_end_balance(user_start_balance)
            user_interactions = self.__get_transactions(
                start_balance=user_start_balance, end_balance=user_end_balance
            )
            row = self.__get_record(
                user_id, user_start_balance, None, "registration", start_dt
            )
            data.append(row)
            user_curr_balance = user_start_balance
            for j in range(1, self.n_interactions):
                date = self.__get_random_date(self.start_dt, self.end_dt)
                interaction = user_interactions[j]
                user_curr_balance += interaction
                row = self.__get_record(
                    user_id, user_curr_balance, interaction, "transaction", date
                )
                data.append(row)
        df = pd.DataFrame(data, columns=self.default_columns).sort_values(by="date")
        return df
