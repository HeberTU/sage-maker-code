# -*- coding: utf-8 -*-
"""Prediction service class.

Created on: 4/10/23
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import pandas as pd
from fastapi.encoders import jsonable_encoder

from fraud import utils
from fraud.ml.estimators.estimator import Estimator
from fraud.services.contracts import PredictionRequest

logger = utils.get_logger()


class PredictionService:
    """Prediction Service Class."""

    def __init__(self, estimator: Estimator):
        """Instantiate the prediction service."""
        self.estimator = estimator

    def make_prediction(
        self, prediction_request: PredictionRequest, transaction_id: int
    ) -> float:
        """Generate predictions using the estimator.

        Args:
            prediction_request: PredictionRequest
                Input contract.

        Returns:
            float
                prediction.
        """
        logger.info(f"features: {prediction_request}")
        data = pd.DataFrame(
            jsonable_encoder(prediction_request), index=[transaction_id]
        )

        data.tx_datetime = pd.to_datetime(data.tx_datetime, unit="ms")
        results = self.estimator.predict(data=data)
        return results.predictions
