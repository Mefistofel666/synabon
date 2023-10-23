import pandas as pd


def get_end_balances(df: pd.DataFrame) -> pd.DataFrame:
    end_balances = (
        df.sort_values(by="date")
        .groupby(by="user_id")
        .tail(1)
        .reset_index()[["user_id", "user_balance"]]
    )
    return end_balances


def get_n_interactions(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["interaction_type"] != "registration"
    n_interactions = (
        df[mask].groupby("user_id").size().reset_index(name="n_interactions")
    )
    return n_interactions


def get_countries(df: pd.DataFrame) -> pd.DataFrame:
    countries = df.groupby("user_id")["country"].agg("max").reset_index()
    return countries


def get_devices(df: pd.DataFrame) -> pd.DataFrame:
    devices = df.groupby("user_id")["device"].agg("max").reset_index()
    return devices


def get_full(df: pd.DataFrame) -> pd.DataFrame:
    end_balance = get_end_balances(df)
    n_interactions = get_n_interactions(df)
    countries = get_countries(df)
    devices = get_devices(df)
    full = (
        end_balance.set_index("user_id")
        .join(n_interactions.set_index("user_id"), on=["user_id"], how="inner")
        .join(countries.set_index("user_id"), on=["user_id"], how="inner")
        .join(devices.set_index("user_id"), on=["user_id"], how="inner")
        .reset_index()
    )
    return full
