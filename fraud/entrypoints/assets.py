"""Local Estimator Module."""
from __future__ import annotations

from fraud.config import Environment
from fraud.data.repositories.repository_factory import DataRepositoryType
from fraud.ml.algorithms.algorithm_factory import AlgorithmType
from fraud.ml.artifact_repositories import ArtifactRepo
from fraud.ml.estimators.estimator import Estimator
from fraud.ml.estimators.estimator_factory import (
    EstimatorFactory,
    EstimatorType,
)
from fraud.ml.evaluators.evaluator_factory import EvaluatorType


class Assets:
    """Returns the assets configuration depending on ENV variable."""

    def __init__(self, env: Environment):
        """Init Assets Factory."""
        self.env = env
        self._assets = {
            Environment.PROD.value: self.get_prod_assets,
            Environment.TEST.value: self.get_test_assets,
        }

    def __call__(self) -> Estimator:
        """Load assets depending on environment."""
        return self._assets.get(self.env, self.get_prod_assets)()

    @staticmethod
    def get_test_assets() -> Estimator:
        """Get tests assets."""
        return EstimatorFactory().create(
            estimator_type=EstimatorType.FAKE_ESTIMATOR,
            data_repository_type=DataRepositoryType.SYNTHETIC,
            evaluator_type=EvaluatorType.TIME_EVALUATOR,
            algorithm_type=AlgorithmType.LIGHT_GBM,
            do_hpo=False,
        )

    @staticmethod
    def get_prod_assets() -> Estimator:
        """Get prod assets."""
        return EstimatorFactory().create_from_artifact_repo(
            estimator_type=EstimatorType.ML_ESTIMATOR,
            artifact_repo=ArtifactRepo.load_from_assets(
                algorithm_type=AlgorithmType.LIGHT_GBM
            ),
        )
