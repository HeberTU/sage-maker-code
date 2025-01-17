"""Time cosine transformer."""
from typing import Union

import pandas as pd

from fraud.domain.feature_transformations.time_enconding import (
    TimeEncoderFunc,
    encode_day_time,
)
from fraud.ml.transformers.transformer import FeatureTransformer


class TimeCosTransformer(FeatureTransformer):
    """Machine learning algorithm."""

    def fit_transformation(
        self, features: Union[pd.DataFrame, pd.Series]
    ) -> None:
        """Wraps the fit method.

        Args:
            features: pd.DataFrame
                Input features to fit the transformation.

        Returns:
            None
        """
        pass

    def apply_transformation(
        self, features: Union[pd.DataFrame, pd.Series]
    ) -> Union[pd.DataFrame, pd.Series]:
        """Apply the transformation.

        Args:
            features: pd.DataFrame
                Features to apply transformation

        Returns:
            pd.DataFrame:
                Transformed features.
        """
        return encode_day_time(
            tx_datetime=features, encoder_function=TimeEncoderFunc.COS
        )

    def fit_apply_transformation(
        self, features: Union[pd.DataFrame, pd.Series]
    ) -> Union[pd.DataFrame, pd.Series]:
        """Fit and apply the transformation.

        Args:
            features: pd.DataFrame
                Features to fit and apply transformation

        Returns:
            pd.DataFrame:
                Transformed features.
        """
        return encode_day_time(
            tx_datetime=features, encoder_function=TimeEncoderFunc.COS
        )
