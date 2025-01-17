"""Evaluator Abstraction."""
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

import pandas as pd

from fraud import utils
from fraud.ml import metrics

logger = utils.get_logger()


class Evaluator(ABC):
    """Machine learning model evaluator."""

    def __init__(self, metric_type_list: List[metrics.MetricType]):
        """Initialize model evaluator.

        Args:
            metric_type_list: List[metrics.MetricType]
                list of model metrics.
        """
        self.metrics = []
        for metric_type in metric_type_list:
            metric_instance = metrics.MetricFactory().create(
                metric_type=metric_type
            )
            self.metrics.append(metric_instance)

    @abstractmethod
    def split(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split the data for training and testig.

        Args:
            data: pd.DataFrame
                Data to split in training and testing.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]:
                Training and testing data.
        """
        raise NotImplementedError

    @staticmethod
    def hash_data(data: pd.DataFrame) -> str:
        """Hash data for tracking purposes.

        Args:
            data: pd.DataFrame
                Data that will be used to train and test the model.

        Returns:
            str: hashed representation of the data.
        """
        hashed_object = utils.make_obj_hash(obj=data, is_training=True)
        return hashed_object

    def evaluate(
        self,
        results: metrics.Results,
        true_values: metrics.TrueValues,
        plot_results: bool = False,
    ) -> Dict[str, float]:
        """Evaluate model predictions.

        Args:
            results: metrics.Result.
                Estimator results.
            true_values: metrics.TrueValues
                True values that we want to predict.
            plot_results: bool
                If True, model results will be plotted.

        Returns:
            Dict[str, float]:
                Evaluation metrics.
        """
        scores = {}
        for metric_instance in self.metrics:
            score = metric_instance.measure(
                results=results,
                true_values=true_values,
                plot_results=plot_results,
            )
            scores[metric_instance.name] = score

        return scores

    def log_testing(
        self,
        estimator_params: Dict[str, Any],
        hashed_data: str,
        results: metrics.Results,
        true_values: metrics.TrueValues,
        plot_results: bool = False,
    ) -> Dict[str, Any]:
        """Log model evaluation.

        Args:
            estimator_params: Dict[str, Any]
                Estimator parameters.
            hashed_data: str
                Hashed representation of the data.
            results: metrics.Results
                Estimator results.
            true_values:metrics.TrueValues
                True values that we want to predict.
            plot_results: bool
                If True, model results will be plotted.

        Returns:
            Dict[str, Any]:
                Model results.

        """
        scores = self.evaluate(
            results=results, true_values=true_values, plot_results=plot_results
        )
        results = {
            "scores": scores,
            "estimator_params": estimator_params,
            "hashed_data": hashed_data,
        }
        if plot_results:
            utils.log_model_results(logger=logger, results=results)
        return results
