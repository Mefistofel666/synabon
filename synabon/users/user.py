from datetime import datetime, timedelta
from random import randrange
import uuid
from typing import Callable, List, Optional
import warnings
from functools import partial

import numpy as np
import pandas as pd
from faker import Faker

from .utils import get_full


class UserGenerator:
    def __init__(
        self,
        n_users: int,
        countries: List[str] | None = None,
        n_countries: int | None = None,
        p_countries: List[float] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        n_users : int
            Numbers of users.
        start_balance_generator
            function to generate initial balance.
        end_balance_generator
            function to generate final balance.
        n_interactions_generator
            function to generate number of transactions per user.
        countries
            list of possible countries.
        n_countries
            number of possible countries.
        p_countries
            finite-dimensional distribution of countries.
        """
        self.__default_scale = 1000
        self.__default_lam = 10
        self.__default_columns = [
            "user_id",
            "user_balance",
            "interaction_sum",
            "interaction_type",
            "transaction_commission",
            "country",
            "device",
            "date",
        ]

        self.n_users = n_users
        self.__trans_commission_mult = 0.003  # 0.3%

        self.fake = Faker()

        self.countries = self.__get_possible_countries(countries, n_countries)
        self.p_countries = p_countries
        self.__check_p_countries()

    def __get_default_start_balance(self) -> Callable[..., float]:
        return partial(np.random.exponential, scale=self.__default_scale)

    def __get_default_end_balance(self) -> Callable[..., float]:
        return partial(np.random.exponential, scale=self.__default_scale)

    def __get_default_interactions_generator(self) -> Callable[..., float]:
        return partial(np.random.poisson, lam=self.__default_lam)

    def __check_gen(self, gen: Callable[..., float]) -> bool:
        try:
            gen()
        except Exception:
            return False

    def __get_start_balance_gen(self, gen: Optional[Callable]) -> Callable[..., float]:
        if not gen:
            return self.__get_default_start_balance()

        if not self.__check_gen(gen):
            warnings.warn(
                "The passed start_balance_generator should be callable without arguments!"
                "Use default start_balance_generator."
            )
            return self.__get_default_start_balance()

    def __get_end_balance_gen(self, gen: Optional[Callable]) -> Callable[..., float]:
        if not gen:
            return self.__get_default_end_balance()

        if not self.__check_gen(gen):
            warnings.warn(
                "The passed end_balance_generator should be callable without arguments!"
                "Use default start_end_generator."
            )
            return self.__get_default_end_balance()

    def __get_n_interactions_gen(self, gen: Optional[Callable]) -> Callable[..., float]:
        if not gen:
            return self.__get_default_interactions_generator()

        if not self.__check_gen(gen):
            warnings.warn(
                "The passed n_interactions_gen should be callable without arguments!"
                "Use default n_interactions_generator."
            )
            return self.__get_default_interactions_generator()

    def __get_possible_countries(
        self,
        countries: List[str] | None,
        n_countries: int | None,
    ) -> List[str]:
        if not countries and not n_countries:
            raise ValueError(
                "At least one of the arguments"
                / "`countries` or `n_countries` must be passed!"
            )
        if not countries:
            return [self.fake.country() for _ in range(n_countries)]
        return countries

    @staticmethod
    def get_random_date(start: datetime, end: datetime) -> datetime:
        """Function that generates a date in a given interval excluding weekends.
        Parameters
        ----------
        start : datetime
            Start interval
        end : datetime
            End interval
        Returns
        -------
        datetime
        """
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

    def __check_p_countries(self) -> None:
        if self.p_countries:
            if len(self.p_countries) != len(self.countries):
                raise ValueError(
                    "length of p_countries must be equal number of countries!"
                )

    def __get_random_country(self) -> str:
        return np.random.choice(self.countries, p=self.p_countries)

    def __get_random_device(self) -> str:
        return self.fake.user_agent()

    def __get_dates(
        self, start_dt: datetime, end_dt: datetime, n_dates: int
    ) -> List[datetime]:
        """Function that generates a dates in a given interval excluding weekends.
        Parameters
        ----------
        start : datetime
            Start interval
        end : datetime
            End interval
        n_dates : int
            Number of dates
        Returns
        -------
        list[datetime]
        """
        dates = [self.get_random_date(start_dt, end_dt) for _ in range(n_dates)]
        return sorted(dates)

    @staticmethod
    def get_transactions(
        start_balance: float, end_balance: float, n_transactions: int
    ) -> List[float]:
        """A function that generates several transactions with an balance.
        Parameters
        ----------
        start_balance : float
            Initial state of balance.
        end_balance : float
            Final state of balance.
        n_transactions: int
            Number of transactions.
        Returns
        -------
        list[float]
        """
        curr_balance = start_balance
        max_balance = np.random.uniform(1, 3) * max(curr_balance, end_balance)
        transactions = []
        for _ in range(n_transactions - 1):
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
        transaction_commission: float,
        country: str,
        device: str,
        interaction_dt: datetime,
    ) -> List:
        return [
            user_id,
            user_balance,
            interaction_sum,
            interaction_type,
            transaction_commission,
            country,
            device,
            interaction_dt,
        ]

    def __get_random_id(self) -> str:
        return str(uuid.uuid4())

    def append_data(
        self,
        df: pd.DataFrame,
        end_balance_generator: Callable[..., float] | None = None,
        n_interactions_generator: Callable[..., float] | None = None,
        duration: timedelta = timedelta(days=14),
    ) -> pd.DataFrame:
        """TODO: add docstring"""
        data = []
        end_balance_gen = self.__get_end_balance_gen(end_balance_generator)
        n_interactions_gen = self.__get_n_interactions_gen(n_interactions_generator)
        full = get_full(df)
        start_dt = df["date"].max().to_pydatetime()
        end_dt = start_dt + duration

        for idx, row in full.iterrows():
            user_id = row["user_id"]
            user_start_balance = row["user_balance"]
            user_end_balance = end_balance_gen()
            user_n_interaction = n_interactions_gen()
            user_dates = self.__get_dates(start_dt, end_dt, user_n_interaction)
            country = row["country"]
            device = row["device"]
            user_interactions = UserGenerator.get_transactions(
                start_balance=user_start_balance,
                end_balance=user_end_balance,
                n_transactions=user_n_interaction,
            )
            user_curr_balance = user_start_balance
            for j in range(user_n_interaction):
                date = user_dates[j]
                transaction = user_interactions[j]
                user_curr_balance += transaction
                transaction_commission = self.__trans_commission_mult * abs(transaction)
                row = self.__get_record(
                    user_id,
                    user_curr_balance,
                    transaction,
                    "transaction",
                    transaction_commission,
                    country,
                    device,
                    date,
                )
                data.append(row)
        new_df = pd.DataFrame(data, columns=self.__default_columns)
        return pd.concat([df, new_df]).sort_values(by="date").reset_index(drop=True)

    def get_data(
        self,
        start_balance_generator: Callable[..., float] | None = None,
        end_balance_generator: Callable[..., float] | None = None,
        n_interactions_generator: Callable[..., float] | None = None,
        start_dt: datetime = datetime(2023, 1, 1),
        end_dt: datetime = datetime(2023, 2, 1),
    ) -> pd.DataFrame:
        start_balance_gen = self.__get_start_balance_gen(start_balance_generator)
        end_balance_gen = self.__get_end_balance_gen(end_balance_generator)
        n_interactions_gen = self.__get_n_interactions_gen(n_interactions_generator)
        data = []
        for _ in range(self.n_users):
            user_id = self.__get_random_id()
            user_start_balance = start_balance_gen()
            user_end_balance = end_balance_gen()
            user_n_interaction = n_interactions_gen()
            user_dates = self.__get_dates(start_dt, end_dt, user_n_interaction)
            country = self.__get_random_country()
            device = self.__get_random_device()

            user_interactions = UserGenerator.get_transactions(
                start_balance=user_start_balance,
                end_balance=user_end_balance,
                n_transactions=user_n_interaction,
            )
            row = self.__get_record(
                user_id,
                user_start_balance,
                None,
                "registration",
                None,
                country,
                device,
                start_dt,
            )
            data.append(row)
            user_curr_balance = user_start_balance
            for j in range(user_n_interaction):
                date = user_dates[j]
                transaction = user_interactions[j]
                user_curr_balance += transaction
                transaction_commission = self.__trans_commission_mult * abs(transaction)
                row = self.__get_record(
                    user_id,
                    user_curr_balance,
                    transaction,
                    "transaction",
                    transaction_commission,
                    country,
                    device,
                    date,
                )
                data.append(row)
        df = (
            pd.DataFrame(data, columns=self.__default_columns)
            .sort_values(by="date")
            .reset_index(drop=True)
        )
        return df
