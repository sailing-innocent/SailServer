# -*- coding: utf-8 -*-
# @file health.py
# @brief The Health Data Storage
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String
from .orm import ORMBase

class Weight(ORMBase):
    __tablename__ = "weights"
    id = Column(Integer, primary_key=True)
    value = Column(String)  # float in kg
    htime = Column(Integer)  # happen time
