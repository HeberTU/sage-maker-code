"""Data repository parameters."""
from dataclasses import (
    dataclass,
    field,
)
import pathlib

import pandas as pd


@dataclass
class SyntheticParams:
    """Synthetic data repository parameters."""

    n_customers: int = 5000
    n_terminals: int = 10000
    geo_uniform_lower_bound: int = 0
    geo_uniform_upper_bound: int = 100
    amount_uniform_lower_bound: int = 5
    amount_uniform_upper_bound: int = 100
    trans_uniform_lower_bound: int = 0
    trans_uniform_upper_bound: int = 4
    start_date: pd.Timedelta = field(
        default_factory=lambda: (
            pd.Timestamp("2023-09-30") - pd.Timedelta(value=30, unit="days")
        )
    )
    nb_days: int = 30
    radius: float = 5
    random_state: int = 0


@dataclass
class LocalParams:
    """Synthetic data repository parameters."""

    file_path: pathlib.Path = pathlib.Path("/opt/ml/input/data/train/")
    # file_path: pathlib.Path = pathlib.Path("./data")