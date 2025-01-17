"""ML Algorithm's factory."""
from __future__ import annotations

import enum

from fraud.ml.algorithms.algorithm import Algorithm
from fraud.ml.algorithms.algorithm_params import (
    LightGBMHPOParams,
    LightGBMParams,
)
from fraud.ml.algorithms.light_gbm import LightGBM


class AlgorithmType(str, enum.Enum):
    """Available ml algorithms."""

    LIGHT_GBM: AlgorithmType = "LightGBM"


class AlgorithmFactory:
    """Algorithm factory."""

    def __init__(self):
        """Initialize ml algorithm factory."""
        self._default_params = {
            AlgorithmType.LIGHT_GBM: LightGBMParams,
        }
        self._hpo_params = {
            AlgorithmType.LIGHT_GBM: LightGBMHPOParams,
        }
        self._catalogue = {
            AlgorithmType.LIGHT_GBM: LightGBM,
        }

    def create(self, algorithm_type: AlgorithmType) -> Algorithm:
        """Instantiate an ML algorithm implementation.

        Args:
            algorithm_type: AlgorithmType
                algorithm type.

        Returns:
            BaseEstimator:
                ML algorithm instance.
        """
        default_params = self._default_params.get(algorithm_type, None)

        if default_params is None:
            raise NotImplementedError(
                f"{algorithm_type} parameters not implemented"
            )

        hpo_params = self._hpo_params.get(algorithm_type, None)

        if hpo_params is None:
            raise NotImplementedError(
                f"{algorithm_type} parameters not implemented"
            )

        algorithm = self._catalogue.get(algorithm_type, None)

        if algorithm is None:
            raise NotImplementedError(f"{algorithm_type} not implemented")

        return algorithm(
            default_params=default_params(), hpo_params=hpo_params()
        )
