"""Aggregated features."""
import enum
from typing import List

import pandas as pd

from fraud import utils


class TimeUnits(str, enum.Enum):
    """Available time unites to aggregate."""

    DAYS = "days"
    MINUTES = "minutes"


class AggFunc(str, enum.Enum):
    """Available aggregation functions."""

    SUM = "sum"
    COUNT = "count"
    MEAN = "mean"


def aggregate_feature(
    transactions_df: pd.DataFrame,
    windows_size_in_days: List[int],
    time_unit: TimeUnits,
    feature_name: str,
    agg_func_list: List[AggFunc],
    datetime_col: str,
    index_name: str,
    grouping_column: str,
    delay_period: int = 0,
) -> pd.DataFrame:
    """Aggregate a feature by a time window and another grouping variable.

    Args:
        transactions_df: pd.DataFrame
            Transactions data frame.
        windows_size_in_days: List[int]
            List of the window sizes to aggregate the feature.
        time_unit: TimeUnits
            Time unit for the window size.
        feature_name: str
            Name of the feature that will be transformed.
        agg_func_list: AggFunc
            List of the Aggregation functions to be applied.
        datetime_col: str
            Name of the timestamp column.
        index_name: str
            Name of the index.
        grouping_column: str
            Outer grouping variable
        delay_period: int
            Delay period for transactions that do not are reflected immediately
            ,e.g., frauds usually consolidate in a db after experts analyze
            them.

    Returns:
        pd.DataFrame
            Data frame with the aggregated features.
    """
    transactions_df = transactions_df.groupby(by=grouping_column).apply(
        lambda x: aggregate_feature_by_time_window(
            data=x,
            windows_size_in_days=windows_size_in_days,
            time_unit=time_unit,
            feature_name=feature_name,
            agg_func_list=agg_func_list,
            datetime_col=datetime_col,
            index_name=index_name,
            grouping_column=grouping_column,
            delay_period=delay_period,
        )
    )

    transactions_df = transactions_df.reset_index(drop=True)

    transactions_df["transaction_id"] = range(len(transactions_df))

    return transactions_df.set_index("transaction_id")


def aggregate_feature_by_time_window(
    data: pd.DataFrame,
    windows_size_in_days: List[int],
    time_unit: TimeUnits,
    feature_name: str,
    agg_func_list: List[AggFunc],
    datetime_col: str,
    index_name: str,
    grouping_column: str,
    delay_period: int = 0,
) -> pd.DataFrame:
    """Aggregate a feature by the given time window.

    Args:
        data: pd.DataFrame
            Data frame to be aggregated
        windows_size_in_days: List[int]
            List of the window sizes to aggregate the feature.
        time_unit: TimeUnits
            Time unit for the window size.
        feature_name: str
            Name of the feature that will be transformed.
        agg_func_list: AggFunc
            List of the Aggregation functions to be applied.
        datetime_col: str
            Name of the timestamp column.
        index_name: str
            Name of the index.
        delay_period: int
            Delay period for transactions that do not are reflected immediately
            ,e.g., frauds usually consolidate in a db after experts analyze
            them.

    Returns:
        pd.Series:
            Feature aggregated.
    """
    data = data.sort_values(datetime_col)

    data = data.reset_index().set_index(keys=datetime_col)

    for window_size in windows_size_in_days:

        for agg_func in agg_func_list:
            aggregated_feature = (
                data[feature_name]
                .rolling(
                    window=pd.Timedelta(
                        value=window_size + delay_period, unit=time_unit.value
                    )
                )
                .agg(agg_func.value)
            )

            if delay_period > 0:

                aggregated_feature_delay = (
                    data[feature_name]
                    .rolling(
                        window=pd.Timedelta(
                            value=delay_period,
                            unit=TimeUnits.DAYS.value,
                        )
                    )
                    .agg(agg_func.value)
                )

                aggregated_feature = (
                    aggregated_feature - aggregated_feature_delay
                )

            data[
                grouping_column
                + "_"
                + agg_func.value
                + "_"
                + feature_name
                + "_"
                + str(window_size)
                + "_"
                + time_unit.value
            ] = list(aggregated_feature)

    data = data.reset_index().set_index(keys=index_name)

    return data


@utils.cacher
def get_time_since_previous_transaction(
    transactions_df: pd.DataFrame,
    datetime_col: str,
    grouping_column: str,
) -> pd.DataFrame:
    """Get time since last transaction per customer.

    Args:
        transactions_df: pd.DataFrame
            Transactions data frame.
        feature_name: str
            Name of the feature that will be transformed.
        datetime_col: str
            Name of the timestamp column.
        grouping_column: str
            Outer grouping variable

    Returns:
        pd.DataFrame
            Data frame with last transaction per customer.
    """
    transactions_df = transactions_df.groupby(by=grouping_column).apply(
        lambda x: time_since_previous_transaction(
            data=x,
            datetime_col=datetime_col,
        )
    )

    transactions_df = transactions_df.reset_index(drop=True)

    transactions_df["transaction_id"] = range(len(transactions_df))

    return transactions_df.set_index("transaction_id")


def time_since_previous_transaction(
    data: pd.DataFrame,
    datetime_col: str,
) -> pd.DataFrame:
    """Get time since last transaction.

        data: pd.DataFrame
            Data frame to be aggregated
        feature_name: str
            Name of the feature that will be transformed.
        datetime_col: str
            Name of the timestamp column.

    Returns:
        pd.DataFrame:
            Data with time since last transaction.
    """
    data = data.sort_values(datetime_col)
    data["last_datetime"] = data[datetime_col].shift(periods=1)

    data["time_since_last_tx"] = (
        data[datetime_col] - data["last_datetime"]
    ).dt.seconds / 60

    fill_value = data["time_since_last_tx"].max()

    data["time_since_last_tx"] = data["time_since_last_tx"].fillna(fill_value)

    data = data.drop(columns=["last_datetime"])

    return data
