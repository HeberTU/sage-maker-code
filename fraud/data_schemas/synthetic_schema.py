# -*- coding: utf-8 -*-
"""Synthetic Data Schema."""
import pandera as pa
from pandera.typing import (
    DateTime,
    Float,
    Int,
    Series,
)

from fraud.data_schemas.data_schema import BaseSchema


class SyntheticFeaturesSchema(BaseSchema):
    """Synthetic feature space schema."""

    tx_amount: Series[Float] = pa.Field(nullable=False)
    customer_id_mean_tx_amount_5_days: Series[Float] = pa.Field(nullable=False)
    terminal_id_mean_tx_fraud_5_days: Series[Float] = pa.Field(nullable=False)
    tx_day_linear: Series[Int] = pa.Field(nullable=False)
    tx_time_cos: Series[Float] = pa.Field(nullable=False)
    tx_time_sin: Series[Float] = pa.Field(nullable=False)


class SyntheticTargetSchema(BaseSchema):
    """Synthetic target schema."""

    tx_fraud: Series[Int] = pa.Field(nullable=False)


class SyntheticTimeStampSchema(BaseSchema):
    """Synthetic TimeStam schema."""

    tx_datetime: Series[DateTime] = pa.Field(nullable=False)


class SyntheticCustomerIDSchema(BaseSchema):
    """Synthetic TimeStam schema."""

    customer_id: Series[Int] = pa.Field(nullable=False)
