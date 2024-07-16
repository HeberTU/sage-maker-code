"""Standard feature transformer."""
from typing import Union

import pandas as pd
from sklearn.preprocessing import StandardScaler

from fraud.ml.transformers.transformer import FeatureTransformer


class StandardTransformer(StandardScaler, FeatureTransformer):
    """Machine learning algorithm."""

    def fit_transformation(
        self, features: Union[pd.DataFrame, pd.Series]
    ) -> None:
        """Wraps the fit method.

        Args:
            features: Union[pd.DataFrame, pd.Series]
                Input features to fit the transformation.

        Returns:
            None
        """
        self.fit(X=features)

    def apply_transformation(
        self, features: Union[pd.DataFrame, pd.Series]
    ) -> Union[pd.DataFrame, pd.Series]:
        """Apply the transformation.

        Args:
            features: pd.DataFrame
                Features to apply transformation

        Returns:
            Union[pd.DataFrame, pd.Series]:
                Transformed features.
        """
        return self.transform(X=features)

    def fit_apply_transformation(
        self, features: Union[pd.DataFrame, pd.Series]
    ) -> Union[pd.DataFrame, pd.Series]:
        """Fit and apply the transformation.

        Args:
            features: Union[pd.DataFrame, pd.Series]
                Features to fit and apply transformation

        Returns:
            Union[pd.DataFrame, pd.Series]:
                Transformed features.
        """
        return self.fit_transform(X=features)
