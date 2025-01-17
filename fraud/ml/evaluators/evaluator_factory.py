"""Evaluator Factory."""
from __future__ import annotations

import enum

from fraud.ml import metrics
from fraud.ml.evaluators.evaluator import Evaluator
from fraud.ml.evaluators.evaluator_params import TimeEvaluatorParams
from fraud.ml.evaluators.time_evaluator import TimeEvaluator


class EvaluatorType(str, enum.Enum):
    """Available evaluators."""

    TIME_EVALUATOR: EvaluatorType = "TIME_EVALUATOR"


class EvaluatorFactory:
    """Evaluator factory."""

    def __init__(self):
        """Initialize evaluator factory."""
        self._params = {EvaluatorType.TIME_EVALUATOR: TimeEvaluatorParams}
        self._catalogue = {EvaluatorType.TIME_EVALUATOR: TimeEvaluator}
        self.metric_type_list = [
            metrics.MetricType.AVERAGE_PRECISION,
            metrics.MetricType.PR_AUC,
            metrics.MetricType.RANDOM_PR_AUC,
            metrics.MetricType.CARD_PRECISION_TOP_K,
            metrics.MetricType.PERFECT_CARD_PRECISION_TOP_K,
        ]

    def create(self, evaluator_type: EvaluatorType) -> Evaluator:
        """Instantiate an evaluator implementation.

        Args:
            evaluator_type: EvaluatorType
                Evaluator to instantiate.

        Returns:
            Evaluator:
                evaluator instance.
        """
        params = self._params.get(evaluator_type, None)

        if params is None:
            raise NotImplementedError(
                f"{evaluator_type} parameters not implemented"
            )

        evaluator = self._catalogue.get(evaluator_type, None)

        if evaluator is None:
            raise NotImplementedError(f"{evaluator_type} not implemented")

        return evaluator(
            metric_type_list=self.metric_type_list, **params().__dict__
        )
