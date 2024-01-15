import pandas as pd


def sort_unique(s: pd.Series) -> pd.Series:
    return s.drop_duplicates().sort_values(
        key=lambda col: col.str.lower()
    )
