# -*- coding: utf-8 -*-
"""Data Schema Factory."""
from typing import Dict

from fraud.data import repositories as dr
from fraud.data_schemas.data_schema import BaseSchema
from fraud.data_schemas.synthetic_schema import (
    SyntheticCustomerIDSchema,
    SyntheticFeaturesSchema,
    SyntheticTargetSchema,
    SyntheticTimeStampSchema,
)


class DataSchemaFactory:
    """Data Schema factory."""

    def __init__(self):
        """Initialize data schema factory."""
        self._catalogue = {
            dr.DataRepositoryType.SYNTHETIC: {
                "feature_space": SyntheticFeaturesSchema,
                "target": SyntheticTargetSchema,
                "timestamp": SyntheticTimeStampSchema,
                "customer_id": SyntheticCustomerIDSchema,
            },
            dr.DataRepositoryType.LOCAL: {
                "feature_space": SyntheticFeaturesSchema,
                "target": SyntheticTargetSchema,
                "timestamp": SyntheticTimeStampSchema,
                "customer_id": SyntheticCustomerIDSchema,
            },
        }

    def create(
        self, data_repository_type: dr.DataRepositoryType
    ) -> Dict[str, BaseSchema]:
        """Instantiate the data schemas.

        Args:
            data_repository_type: dr.DataRepositoryType
                Data repository type.

        Returns:
            Dict[str, BaseSchema]:
                Data Schemas
        """
        data_schemas = self._catalogue.get(data_repository_type, None)

        if data_schemas is None:
            raise NotImplementedError(
                f"{data_repository_type} not implemented"
            )

        return data_schemas
