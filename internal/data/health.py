# -*- coding: utf-8 -*-
# @file health.py
# @brief The Health Data Storage
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String
from .orm import ORMBase
from dataclasses import dataclass, field


# The Raw Weight Data
class Weight(ORMBase):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True)
    value = Column(String)  # float in kg
    htime = Column(Integer)  # happen time


# The Preprocessed Weight Data with Filter
class WeightRecord(ORMBase):
    __tablename__ = "weight_records"
    id = Column(Integer, primary_key=True)
    value = Column(String)  # float in kg
    htime = Column(Integer)  # happen time
    tag = Column(String)  # tag (daily, weekly, monthly)


@dataclass
class WeightData:
    """
    The Weight Data
    """

    value: float
    htime: int
    id: int = field(default=-1)


@dataclass
class WeightRecordData:
    """
    The Weight Data
    """

    value: float
    htime: int
    id: int = field(default=-1)
    tag: str = field(default="daily")
