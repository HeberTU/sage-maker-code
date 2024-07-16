"""ML Estimator Factory."""
from __future__ import annotations

import enum

from fraud import data_schemas as ds
from fraud.data import repositories
from fraud.ml.algorithms.algorithm_factory import (
    AlgorithmFactory,
    AlgorithmType,
)
from fraud.ml.artifact_repositories.artifact_repository import ArtifactRepo
from fraud.ml.estimators.estimator import Estimator
from fraud.ml.estimators.fake_estimator import FakeEstimator
from fraud.ml.estimators.ml_estimator import MLEstimator
from fraud.ml.evaluators.evaluator_factory import (
    EvaluatorFactory,
    EvaluatorType,
)
from fraud.ml.transformers.transformer_chain import TransformerChainFactory


class EstimatorType(str, enum.Enum):
    """Available Estimator."""

    ML_ESTIMATOR: EstimatorType = "ML_ESTIMATOR"
    FAKE_ESTIMATOR: EstimatorType = "FAKE_ESTIMATOR"


class EstimatorFactory:
    """Estimator factory."""

    def __init__(self):
        """Instantiate an estimator factory."""
        self._catalogue = {
            EstimatorType.ML_ESTIMATOR: MLEstimator,
            EstimatorType.FAKE_ESTIMATOR: FakeEstimator,
        }

    def create(
        self,
        estimator_type: EstimatorType,
        data_repository_type: repositories.DataRepositoryType,
        evaluator_type: EvaluatorType,
        algorithm_type: AlgorithmType,
        do_hpo: bool,
    ) -> Estimator:
        """Instantiate the estimator.

        Args:
            estimator_type: EstimatorType
                Estimator Type to instantiate.
            data_repository_type: data_repositories.DataRepositoryType
                Type of data repository to get the data.
            evaluator_type: EvaluatorType
                Type of Ml model evaluator.
            algorithm_type: AlgorithmType
                Type of ML algorithm to tran and test.
            do_hpo: bool
                If True, the estimator will do hyperparameter search.

        Returns:
            Evaluator
        """
        estimator = self._catalogue.get(estimator_type)

        if estimator is None:
            raise NotImplementedError(f"{estimator_type} not implemented")

        data_repository = repositories.DataRepositoryFactory().create(
            data_repository_type=data_repository_type
        )
        evaluator = EvaluatorFactory().create(evaluator_type=evaluator_type)
        data_schemas = ds.DataSchemaFactory().create(
            data_repository_type=data_repository_type
        )
        algorithm = AlgorithmFactory().create(algorithm_type=algorithm_type)
        transformer_chain = TransformerChainFactory().create(
            data_repository_type=data_repository_type
        )

        return estimator(
            data_repository=data_repository,
            evaluator=evaluator,
            feature_schemas=data_schemas.get("feature_space"),
            target_schema=data_schemas.get("target"),
            timestamp_schema=data_schemas.get("timestamp"),
            customer_id_schema=data_schemas.get("customer_id"),
            algorithm=algorithm,
            transformer_chain=transformer_chain,
            do_hpo=do_hpo,
        )

    def create_from_artifact_repo(
        self,
        estimator_type: EstimatorType,
        artifact_repo: ArtifactRepo,
    ) -> Estimator:
        """Create an evaluator from an ArtifactRpo.

        Args:
            estimator_type: EstimatorType
                Estimator Type to instantiate.
            artifact_repo: ArtifactRepo
                Artifact repository.

        Returns:
            Estimator:
                estimator instance.
        """
        estimator = self._catalogue.get(estimator_type)

        if estimator is None:
            raise NotImplementedError(f"{estimator_type} not implemented")

        return estimator(
            data_repository=None,
            evaluator=None,
            feature_schemas=artifact_repo.model.get("feature_schemas"),
            target_schema=None,
            timestamp_schema=None,
            customer_id_schema=None,
            algorithm=artifact_repo.model.get("algorithm"),
            transformer_chain=artifact_repo.model.get("transformer_chain"),
            do_hpo=False,
        )
