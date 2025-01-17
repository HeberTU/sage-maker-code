"""Feature Transformers factory."""
from __future__ import annotations

import enum

from fraud.ml.transformers.day_linear_transformer import DayLinearTransformer
from fraud.ml.transformers.identity import IdentityTransformer
from fraud.ml.transformers.min_max import MinMaxTransformer
from fraud.ml.transformers.standar import StandardTransformer
from fraud.ml.transformers.time_cos_transformer import TimeCosTransformer
from fraud.ml.transformers.time_sin_transformer import TimeSinTransformer
from fraud.ml.transformers.transformer import FeatureTransformer


class TransformerType(str, enum.Enum):
    """Available feature transformers."""

    STANDARD_SCALER: TransformerType = "STANDARD_SCALER"
    MIN_MAX_SCALER: TransformerType = "MIN_MAX_SCALER"
    IDENTITY: TransformerType = "IDENTITY"
    TIME_COS: TransformerType = "TIME_COS"
    TIME_SIN: TransformerType = "TIME_SIN"
    DAY_LINEAR: TransformerType = "DAY_LINEAR"


class TransformerFactory:
    """Transformer factory."""

    def __init__(self):
        """Instantiate a transformer factory."""
        self._params = {
            TransformerType.STANDARD_SCALER: {},
            TransformerType.MIN_MAX_SCALER: {},
            TransformerType.IDENTITY: {},
            TransformerType.TIME_COS: {},
            TransformerType.TIME_SIN: {},
            TransformerType.DAY_LINEAR: {},
        }

        self._catalogue = {
            TransformerType.STANDARD_SCALER: StandardTransformer,
            TransformerType.MIN_MAX_SCALER: MinMaxTransformer,
            TransformerType.IDENTITY: IdentityTransformer,
            TransformerType.TIME_COS: TimeCosTransformer,
            TransformerType.TIME_SIN: TimeSinTransformer,
            TransformerType.DAY_LINEAR: DayLinearTransformer,
        }

    def create(self, transformer_type: TransformerType) -> FeatureTransformer:
        """Instantiate an ML algorithm implementation.

        Args:
            transformer_type: TransformerType
                Feature transformer type.

        Returns:
            BaseEstimator:
                ML algorithm instance.
        """
        params = self._params.get(transformer_type, None)

        if params is None:
            raise NotImplementedError(
                f"{transformer_type} parameters not implemented"
            )

        transformer = self._catalogue.get(transformer_type, None)

        if transformer is None:
            raise NotImplementedError(f"{transformer_type} not implemented")

        return transformer(**params)
