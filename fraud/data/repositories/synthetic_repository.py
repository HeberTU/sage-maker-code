"""Synthetic Data Repository."""
import pandas as pd

from fraud import (
    domain,
    utils,
)
from fraud.data.repositories.repository import DataRepository
from fraud.domain import feature_transformations


class Synthetic(DataRepository):
    """Synthetic Data Repository."""

    def __init__(
        self,
        n_customers: int,
        n_terminals: int,
        geo_uniform_lower_bound: int,
        geo_uniform_upper_bound: int,
        amount_uniform_lower_bound: int,
        amount_uniform_upper_bound: int,
        trans_uniform_lower_bound: int,
        trans_uniform_upper_bound: int,
        start_date: pd.Timedelta,
        nb_days: int,
        radius: float,
        random_state: int,
    ):
        """Instantiate synthetic data repository.

        Args:
            n_customers: int
                Number of simulated customers.
            n_terminals: int
                Number of simulated terminal.
            geo_uniform_lower_bound: int
                Lower limit from the uniform distribution that will be used to
                simulate geographical data.
            geo_uniform_upper_bound: int
                Upper limit from the uniform distribution that will be used to
                simulate geographical data.
            amount_uniform_lower_bound: int
                Lower limit from the uniform distribution that will be used to
                simulate the customer spending amounts data.
            amount_uniform_upper_bound: int
                Upper limit from the uniform distribution that will be used to
                simulate the customer spending amounts data.
            trans_uniform_lower_bound: int
                Lower limit from the uniform distribution that will be used to
                simulate the customer spending frequency data.
            trans_uniform_upper_bound: int
                Upper limit from the uniform distribution that will be used to
                simulate the customer spending frequency data.
            start_date: pd.Timestamp
                Date from which the transactions will be generated.
            nb_days: int
                Number of day to generate data.
            radius: float
                Radius representing the maximum distance for a customer to use
                a terminal.
            random_state: int
                Random seed for reproducibility purposes.
        """
        self.n_customers = n_customers
        self.n_terminals = n_terminals

        self.geo_uniform_lower_bound = geo_uniform_lower_bound
        self.geo_uniform_upper_bound = geo_uniform_upper_bound
        self.amount_uniform_lower_bound = amount_uniform_lower_bound
        self.amount_uniform_upper_bound = amount_uniform_upper_bound
        self.trans_uniform_lower_bound = trans_uniform_lower_bound
        self.trans_uniform_upper_bound = trans_uniform_upper_bound

        self.start_date = start_date
        self.nb_days = nb_days
        self.radius = radius

        self.random_state = random_state

    @utils.timer
    def load_data(self) -> pd.DataFrame:
        """Simulate the credit card transactional data.

        Returns:
            pd.DataFrame: Credit card transactional data.
        """
        transactions_df = domain.simulate_credit_card_transactions_data(
            n_terminals=self.n_terminals,
            n_customers=self.n_customers,
            geo_uniform_lower_bound=self.geo_uniform_lower_bound,
            geo_uniform_upper_bound=self.geo_uniform_upper_bound,
            amount_uniform_lower_bound=self.amount_uniform_lower_bound,
            amount_uniform_upper_bound=self.amount_uniform_upper_bound,
            trans_uniform_lower_bound=self.trans_uniform_lower_bound,
            trans_uniform_upper_bound=self.trans_uniform_upper_bound,
            radius=self.radius,
            start_date=self.start_date,
            nb_days=self.nb_days,
            random_state=self.random_state,
        )

        transactions_df["transaction_id"] = range(len(transactions_df))

        return transactions_df.set_index("transaction_id")

    @utils.timer
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess credit card transactional data to fit an ML algorithm.

        Returns:
            pd.DataFrame: Credit card transactional data.
        """
        data = data.assign(
            is_weekday=lambda row: feature_transformations.is_weekday(
                tx_datetime=row.tx_datetime,
            ),
            is_night=lambda row: feature_transformations.is_night(
                tx_datetime=row.tx_datetime,
            ),
        )

        data = feature_transformations.aggregate_feature(
            transactions_df=data,
            windows_size_in_days=[5],
            time_unit=feature_transformations.TimeUnits.DAYS,
            feature_name="tx_amount",
            agg_func_list=[
                feature_transformations.AggFunc.MEAN,
            ],
            datetime_col="tx_datetime",
            index_name="transaction_id",
            grouping_column="customer_id",
            delay_period=0,
        )

        data = feature_transformations.aggregate_feature(
            transactions_df=data,
            windows_size_in_days=[5],
            time_unit=feature_transformations.TimeUnits.DAYS,
            feature_name="tx_fraud",
            agg_func_list=[
                feature_transformations.AggFunc.MEAN,
            ],
            datetime_col="tx_datetime",
            index_name="transaction_id",
            grouping_column="terminal_id",
            delay_period=7,
        )

        return data
