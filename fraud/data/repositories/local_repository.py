"""Local data repository."""
import os

import pandas as pd
import pathlib

from fraud import utils
from fraud.data.repositories.repository import DataRepository
from fraud.domain import feature_transformations

logger = utils.get_logger()


class LocalRepository(DataRepository):
    """Local data repository."""

    def __init__(
        self,
        file_path: pathlib.Path
    ) -> None:
        """Instantiate local data repository.

        Args:
            file_path: path where the raw data is stored.
        """
        self._file_path = file_path

    @utils.timer
    def load_data(self) -> pd.DataFrame:
        """Simulate the credit card transactional data.

        Returns:
            pd.DataFrame: Credit card transactional data.
        """
        logger.info(f"Reading from - Data Path {self._file_path}")
        return pd.read_pickle(self._file_path / 'raw_data.pickle')

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
