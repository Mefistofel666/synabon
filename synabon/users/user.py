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

        self.trans_commission_mult = 0.003  # 0.3%

        self.default_columns = [
            "user_id",
            "user_balance",
            "interaction_sum",
            "interaction_type",
            "transaction_commission",
            "date",
        ]

    @staticmethod
    def __get_random_date(start: datetime, end: datetime) -> datetime:
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        random_date = start + timedelta(seconds=random_second)

        while random_date.weekday() in [5, 6]:
            delta = end - start
            int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
            random_second = randrange(int_delta)
            random_date = start + timedelta(seconds=random_second)

        return random_date

    def __get_dates(
        self, start_dt: datetime, end_dt: datetime, n_dates: int
    ) -> List[datetime]:
        dates = [self.__get_random_date(start_dt, end_dt) for _ in range(n_dates)]
        return sorted(dates)

    def __get_transactions(
        self, start_balance: float, end_balance: float
    ) -> np.ndarray:
        curr_balance = start_balance
        max_balance = np.random.uniform(1, 3) * max(curr_balance, end_balance)
        transactions = []
        for _ in range(self.n_interactions - 1):
            next_balance = np.random.uniform(0, max_balance)
            transaction = next_balance - curr_balance
            transactions.append(transaction)
            curr_balance = next_balance

        end_transaction = end_balance - curr_balance
        transactions.append(end_transaction)

        return transactions

    def __get_record(
        self,
        user_id: uuid.UUID,
        user_balance: float,
        interaction_sum: float,
        interaction_type: str,
        transaction_commision: float,
        interaction_dt: datetime,
    ) -> List:
        return [
            user_id,
            user_balance,
            interaction_sum,
            interaction_type,
            transaction_commision,
            interaction_dt,
        ]

    def __get_random_id(self) -> uuid.UUID:
        return uuid.uuid4()

    def __get_user_end_balance(self, start_balance: float) -> float:
        scale = 10
        loc = start_balance
        end_balance = loc + scale * np.random.standard_cauchy()
        while end_balance <= 0:
            end_balance = loc + scale * np.random.standard_cauchy()
        return end_balance

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
            user_dates = self.__get_dates(start_dt, end_dt, self.n_interactions)
            row = self.__get_record(
                user_id, user_start_balance, None, "registration", None, start_dt
            )
            data.append(row)
            user_curr_balance = user_start_balance
            for j in range(0, self.n_interactions):
                date = user_dates[j]
                transaction = user_interactions[j]
                user_curr_balance += transaction
                transaction_commission = self.trans_commission_mult * abs(transaction)
                row = self.__get_record(
                    user_id,
                    user_curr_balance,
                    transaction,
                    "transaction",
                    transaction_commission,
                    date,
                )
                data.append(row)
        df = pd.DataFrame(data, columns=self.default_columns).sort_values(by="date")
        return df
