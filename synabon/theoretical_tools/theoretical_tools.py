import pandas as pd
import numpy as np
import statsmodels.stats.api as sms
import statsmodels.stats as stats


def get_mde(
    mean: float,
    std: float,
    sample_size: int,
    alpha: float = 0.05,
    beta: float = 0.2,
    groups_ratio: float = 1.0,
    alternative: str = "two-sided",
):
    power_class = stats.power.TTestIndPower()
    mde = power_class.solve_power(
        effect_size=None,
        nobs1=sample_size,
        alpha=alpha,
        power=1 - beta,
        ratio=groups_ratio,
        alternative=alternative,
    )
    return mde * std / mean


def get_minimal_determinable_effect(
    df: pd.DataFrame,
    target_col: str,
    alpha: float = 0.05,
    beta: float = 0.2,
    groups_ratio: float = 1.0,
    alternative: str = "two-sided",
) -> float:
    """
    Calculate minimum detectable effect.

    Parameters
    ----------
    df : pd.DataFrame
    target_col : str
        Metric column
    mean : float
        Sample mean
    std : float
        Sample standard deviation
    sample_size : int
        Size of sample
    alpha : float, default: 0.05
        First type error
    beta : float, default: 0.2
        Second type error
    groups_ratio : float, default: 1.0
        Ratio between two groups.
    alternative : str, default: "two-sided"
        Alternative hypothesis, can be "two-sided", "larger"
        or "smaller".
        "larger" - if effect is positive.
        "smaller" - if effect is negative.

    Returns
    -------
    mde : float
        Minimal effect which we can find

    """
    mean = df[target_col].mean()
    std = df[target_col].std()
    n = int(df.shape[0] / 2)
    res = get_mde(mean, std, n, alpha, beta, groups_ratio, alternative)
    return res


def calculate_sample_size(
    mean: float,
    std: float,
    eff: float,
    alpha: float = 0.05,
    beta: float = 0.2,
    groups_ratio: float = 1.0,
    alternative: str = "two-sided",
):
    power_class = stats.power.TTestIndPower()

    stabilized_effect = (eff - 1) * mean / std

    sample_size = power_class.solve_power(
        effect_size=stabilized_effect,
        nobs1=None,
        alpha=alpha,
        power=1 - beta,
        ratio=groups_ratio,
        alternative=alternative,
    )
    return int(np.ceil(sample_size))


def get_sample_size(
    df: pd.DataFrame,
    target_col: str,
    eff: float,
    alpha: float = 0.05,
    beta: float = 0.2,
    groups_ratio: float = 1.0,
    alternative: str = "two-sided",
) -> int:
    """
    Calculate minimum sample size to catch effect with fixed errors.

    Parameters
    ----------
    mean : float
        Sample mean
    std : float
        Sample standard deviation
    eff : float
        Effect for which we calculate sample size
    alpha : float, default: 0.05
        First type error
    beta : float, default: 0.2
        Second type error
    groups_ratio : float, default: 1.0
        Ratio between two groups.
    alternative : str, default: "two-sided"
        Alternative hypothesis, can be "two-sided", "larger"
        or "smaller".
        "larger" - if effect is positive.
        "smaller" - if effect is negative.

    Returns
    -------
    sample_size : int
        Minimal sample size

    """
    mean = df[target_col].mean()
    std = df[target_col].std()

    res = calculate_sample_size(mean, std, eff, alpha, beta, groups_ratio, alternative)

    return res
