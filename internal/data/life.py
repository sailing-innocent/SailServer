# -*- coding: utf-8 -*-
# @file info.py
# @brief Peronsal Information Storage
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from .orm import ORMBase
from sqlalchemy.orm import relationship
from utils.state import StateBits
from dataclasses import dataclass, field
from datetime import datetime


# 服务资产，存在有效期限
class ServiceAccount(ORMBase):
    __tablename__ = "service_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # account name
    entry = Column(String(255), nullable=False)  # entry website/app name
    username = Column(String(255), nullable=False)  # username
    password = Column(String(255), nullable=False)  # password
    desp = Column(String(255), nullable=True)  # account description
    expire_time = Column(
        BigInteger, nullable=False
    )  # expire time, store as timestamp in seconds


@dataclass
class ServiceAccountData:
    id: int = field(default=None)
    name: str = field(default="")
    entry: str = field(default="")
    username: str = field(default="")
    password: str = field(default="")
    desp: str = field(default="")
    expire_time: int = field(default=0)


# -----------------------------------------
# Long-Term Project Management
# -----------------------------------------
class Project(ORMBase):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    parent_id = Column(
        Integer, ForeignKey("projects.id"), nullable=True
    )  # self reference for sub-projects
    parent = relationship(
        "Project", remote_side=[id], backref="sub_projects"
    )  # self reference for sub-projects
    name = Column(String)
    description = Column(String)
    raw_tags = Column(String)  # raw tags, comma separated
    tags = Column(String)  # processed tags, space separated
    state = Column(Integer)  # 0: active, 1: archived
    ctime = Column(TIMESTAMP, server_default=func.current_timestamp())  # creation time
    mtime = Column(
        TIMESTAMP, server_default=func.current_timestamp()
    )  # modification time
    ddl = Column(BigInteger)  # deadline in timestamp in seconds
    weight = Column(Integer)  # weight for sorting importance, default to 0
    extra = Column(
        JSONB, nullable=True
    )  # extra information, e.g. priority, progress, requirement condition, etc.


@dataclass
class ProjectData:
    """
    The Project Data
    """

    id: int = field(default=None)
    parent_id: int = field(default=None)
    name: str = field(default="")
    description: str = field(default="")
    raw_tags: str = field(default="")
    tags: str = field(default="")
    state: int = field(default=0)
    ctime: datetime = field(default_factory=lambda: datetime.now())
    mtime: datetime = field(default_factory=lambda: datetime.now())
    ddl: int = field(default=0)
    weight: int = field(default=0)
    extra: dict = field(default_factory=dict)
