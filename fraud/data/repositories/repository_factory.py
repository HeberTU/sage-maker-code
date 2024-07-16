"""Data repository Factory."""
from __future__ import annotations

import enum

from fraud.data.repositories.repository import DataRepository
from fraud.data.repositories.repository_params import (
    SyntheticParams,
    LocalParams
)
from fraud.data.repositories.synthetic_repository import Synthetic
from fraud.data.repositories.local_repository import LocalRepository


class DataRepositoryType(str, enum.Enum):
    """Available Data Repositories."""

    SYNTHETIC: DataRepositoryType = "SYNTHETIC"
    LOCAL: DataRepositoryType = "LOCAL"


class DataRepositoryFactory:
    """Data repository Factory."""

    def __init__(self):
        """Initialize data repository factory."""
        self._params = {
            DataRepositoryType.SYNTHETIC: SyntheticParams,
            DataRepositoryType.LOCAL: LocalParams,
        }
        self._catalogue = {
            DataRepositoryType.SYNTHETIC: Synthetic,
            DataRepositoryType.LOCAL: LocalRepository,
        }

    def create(
        self, data_repository_type: DataRepositoryType
    ) -> DataRepository:
        """Instantiate a data repository implementation.

        Args:
            data_repository_type: DataRepositoryType
                Data repository type to instantiate.

        Returns:
            DataRepository:
                Data repository instance.
        """
        params = self._params.get(data_repository_type, None)

        if params is None:
            raise NotImplementedError(
                f"{data_repository_type} parameters not implemented"
            )

        data_repository = self._catalogue.get(data_repository_type, None)

        if data_repository is None:
            raise NotImplementedError(
                f"{data_repository_type} not implemented"
            )

        return data_repository(**params().__dict__)
