"""API routes module."""
from fastapi import (
    APIRouter,
    Depends,
)

from fraud.config import settings
from fraud.entrypoints.assets import Assets
from fraud.ml.estimators.estimator import Estimator
from fraud.services.contracts import (
    PredictionRequest,
    PredictionResponse,
)
from fraud.services.prediction_service import PredictionService


def get_estimator() -> Estimator:
    """Get Estimator."""
    return Assets(settings.ENV)()


def get_router() -> APIRouter:
    """Get API Router."""
    router = APIRouter()

    @router.get(path="/ping")
    def ping() -> str:
        """Healthcheck function."""
        return "pong"

    @router.post(
        path="/invocations",
        response_model=PredictionResponse,
    )
    def predict(
        transaction_id: str,
        request: PredictionRequest,
        estimator: Estimator = Depends(get_estimator),
    ) -> PredictionResponse:
        """Prediction endpoint.

        Args:
            transaction_id: str - Unique ID for the transaction.
            request: ModifiedPredictionRequest - Input features.
            estimator: Estimator - Estimator class.

        Returns:
            ModifiedPredictionResponse: Decision to block the transaction or
            not.
        """
        service = PredictionService(estimator)
        prediction = service.make_prediction(
            prediction_request=request, transaction_id=int(transaction_id)
        )

        return PredictionResponse(
            transaction_id=transaction_id, transaction_to_block=prediction
        )

    return router
