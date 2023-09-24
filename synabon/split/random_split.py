import pandas as pd


def random_split(data: pd.DataFrame, fraction: float = 0.5) -> pd.DataFrame:
    part_1 = data.sample(frac=fraction)
    part_2 = data.drop(part_1.index)
    return part_1, part_2
