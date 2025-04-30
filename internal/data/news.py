# -*- coding: utf-8 -*-
# @file news.py
# @brief The News Storage
# @author sailing-innocent
# @date 2025-04-29
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB 
from .orm import ORMBase 

# The News Source to Fetch the latest news
class NewsSource(ORMBase):
    __tablename__ = "news_source"
    id = Column(Integer, primary_key=True)

# The News Article  
class NewsArticle(ORMBase):
    __tablename__ = "news_article"
    id = Column(Integer, primary_key=True)

# The Report ID Analyised from Article Fetched
class NewsReport(ORMBase):
    __tablename__ = "news_reports"
    id = Column(Integer, primary_key=True)
