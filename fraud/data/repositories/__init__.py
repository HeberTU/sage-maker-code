# -*- coding: utf-8 -*-
"""Data Repository library.

This library is used to encapsulate all the data layer related modules.
"""
from fraud.data.repositories.repository import DataRepository
from fraud.data.repositories.repository_factory import (
    DataRepositoryFactory,
    DataRepositoryType,
)

__all__ = ["DataRepositoryFactory", "DataRepositoryType", "DataRepository"]
