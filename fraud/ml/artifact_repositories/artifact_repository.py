# -*- coding: utf-8 -*-
"""Artifact repository."""
from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Dict,
    Union,
)

import pandas as pd

from fraud import (
    config,
    data_schemas,
    utils,
)
from fraud.ml.algorithms.algorithm import Algorithm
from fraud.ml.algorithms.algorithm_factory import AlgorithmType
from fraud.ml.transformers.transformer_chain import TransformerChain

logger = utils.get_logger()


@dataclass
class ArtifactRepo:
    """ML Algorithm artifacts."""

    model: Dict[
        str, Union[data_schemas.BaseSchema, TransformerChain, Algorithm]
    ]
    integration_test_set: pd.DataFrame

    def dump_artifacts(self) -> None:
        """Dump artifact repo items."""
        file_path = config.settings.DUMP_PATH
        logger.info(f"Saving artifacts at: {file_path}")
        for key, value in self.__dict__.items():
            utils.dump_artifacts(obj=value, file_path=file_path, file_name=key)

    @classmethod
    def load_from_assets(cls, algorithm_type: AlgorithmType) -> ArtifactRepo:
        """Loads an instance of ArtifactRepo from stored assets.

        Args:
            algorithm_type: AlgorithmType
                Algorithm artifacts that will be loaded.

        Returns:
            ArtifactRepo:
                Artifact repo.
        """
        files_path = config.settings.ASSETS_PATH
        return cls(
            model=utils.load_artifacts(file_path=files_path / "model.pickle"),
            integration_test_set=utils.load_artifacts(
                file_path=files_path / "integration_test_set.pickle"
            ),
        )
