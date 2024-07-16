"""Metrics Factory."""
from __future__ import annotations

import enum

from fraud.ml.metrics.average_precision import AveragePrecisionScore
from fraud.ml.metrics.card_precision_top_k import CardPrecisionTopK
from fraud.ml.metrics.metric import Metric
from fraud.ml.metrics.perf_card_precision_top_k import PerfCardPrecisionTopK
from fraud.ml.metrics.pr_auc import PRAUCScore
from fraud.ml.metrics.random_pr_auc import RandomPRAUCScore
from fraud.ml.metrics.roc_auc import ROCAUCScore


class MetricType(str, enum.Enum):
    """Available metrics."""

    ROC_AUC: MetricType = "ROC_AUC"
    AVERAGE_PRECISION: MetricType = "AVERAGE_PRECISION"
    CARD_PRECISION_TOP_K: MetricType = "CARD_PRECISION_TOP_K"
    PERFECT_CARD_PRECISION_TOP_K: MetricType = "PERFECT_CARD_PRECISION_TOP_K"
    PR_AUC: MetricType = "PR_AUC"
    RANDOM_PR_AUC: MetricType = "RANDOM_PR_AUC"


class MetricFactory:
    """Metric Factory."""

    def __init__(self):
        """Initialize metric factory."""
        self._catalogue = {
            MetricType.AVERAGE_PRECISION: AveragePrecisionScore,
            MetricType.ROC_AUC: ROCAUCScore,
            MetricType.CARD_PRECISION_TOP_K: CardPrecisionTopK,
            MetricType.PERFECT_CARD_PRECISION_TOP_K: PerfCardPrecisionTopK,
            MetricType.PR_AUC: PRAUCScore,
            MetricType.RANDOM_PR_AUC: RandomPRAUCScore,
        }

    def create(self, metric_type: MetricType) -> Metric:
        """Instantiate a metric implementation.

        Args:
            metric_type: MetricType
                Metric  type to instantiate.

        Returns:
            Metric:
                Metric instance.
        """
        metric = self._catalogue.get(metric_type, None)

        if metric is None:
            raise NotImplementedError(f"{metric_type} not implemented")

        return metric(name=metric.name, params=metric.params)
