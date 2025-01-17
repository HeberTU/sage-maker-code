"""Business domain models."""
from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import List

import pandas as pd


@dataclass
class CustomerProfile:
    """Represent the customer profile.

    Each customer profile will be defined by the following properties:

        - customer_id: The customer unique id.
        - x_customer_id, y_customer_id: A pair of coordinates in a 100 * 100
            grid, that defines the geographical location of the customer.
        - mean_amount, std_amount: The man and standard deviation of the
            transaction amounts for the customer.
        -  mean_nb_tx_per_day: The average number of transactions per day for
            the customer.
        - available_terminals: List of valid terminals for the customer.
    """

    customer_id: int
    x_customer_id: float
    y_customer_id: float
    mean_amount: float
    std_amount: float
    mean_nb_tx_per_day: float
    available_terminals: List[int] = field(default_factory=lambda: [])


@dataclass
class TerminalProfiles:
    """Represent terminal (point of sale) profiles.

    Each terminal will be defined by the following properties:

        - terminal_id: the terminal unique id.
        - x_terminal_id,y_terminal_id: A pair of coordinates in a 100 * 100
            grid, that defines the geographical location of the terminal.
    """

    terminal_id: int
    x_terminal_id: float
    y_terminal_id: float


@dataclass
class Transaction:
    """Represent terminal transactions.

    Each transaction will be defined by the following properties.
    """

    tx_datetime: pd.Timestamp
    customer_id: int
    terminal_id: int
    tx_amount: float
