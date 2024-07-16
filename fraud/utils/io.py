"""Input and output module."""
import os
import pathlib
import pickle
from typing import Any

from fraud.utils.logging import get_logger

logger = get_logger()


def dump_artifacts(obj: Any, file_path: pathlib.Path, file_name: str) -> None:
    """Dump object to pickle format.

    Args:
        obj: Any
            Object to save.
        file_path: pathlib.Path
            File path
        file_name: str
            Name of the file
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_name += ".pickle"
    with open(file=file_path / file_name, mode="wb") as handle:
        pickle.dump(obj=obj, file=handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_artifacts(file_path: pathlib.Path) -> Any:
    """Load a pickle object from memory.

    Args:
        file_path: pathlib.Path
            file path

    Returns:
        object:
            Saved object.
    """
    logger.info(f"Loading artifact from {file_path}")

    try:
        with open(file=file_path, mode="rb") as handle:
            obj = pickle.load(handle)
    except FileNotFoundError:
        logger.error(f"No pickle file found {file_path}")
        obj = None

    return obj
