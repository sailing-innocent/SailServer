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

LAST_TIMESTAMP_LIFE = datetime.date(2199, 1, 1)

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
    name = Column(String)
    description = Column(String)
    state = Column(Integer)  # Project State
    ctime = Column(TIMESTAMP, server_default=func.current_timestamp())  # creation time
    mtime = Column(TIMESTAMP, server_default=func.current_timestamp())  # modification time
    ddl = Column(TIMESTAMP)  # deadline in timestamp in seconds
    extra = Column(
        JSONB, nullable=True
    )  # extra information, e.g. priority, progress, requirement condition, etc.

class ProjectState:
    # Project State Machine
    # -----------------------------------------------------
    # INVALID -> VALID -> PREPARE -> TRACKING ---> DONE
    #                                  ^   |
    #                                  |   v
    #                                  PENDING---> CANCEL
    # ------------------------------------------------------
    # state enum
    INVALID = 0
    VALID = 1
    PREPARE = 2
    TRACKING = 3
    DONE = 4
    PENDING = 5
    CANCELED = 6
    _state = INVALID
    def __init__(self, state: int = INVALID):
        self._state = self.INVALID

    def valid(self):
        self._state = self.VALID

    def prepare(self):
        if (self._state == self.VALID):
            self._state = self.PREPARE
        else:
            raise ValueError("Invalid state for prepare")

    def tracking(self):
        if (self._state == self.PREPARE):
            self._state = self.TRACKING
        else:
            raise ValueError("Invalid state for tracking")

    def pending(self):
        if (self._state == self.TRACKING):
            self._state = self.PENDING
        else:
            raise ValueError("Invalid state for pending")

    def restore(self):
        if (self._state == self.PENDING):
            self._state = self.TRACKING
        else:
            raise ValueError("Invalid state for restore")

    def done(self):
        if (self._state == self.PENDING):
            self._state = self.DONE
        else:
            raise ValueError("Invalid state for done")

    def cancel(self):
        # no need to check state
        self._state = self.CANCELED

    def get_state(self) -> int:
        return self._state


@dataclass
class ProjectData:
    """
    The Project Data
    """

    id: int = field(default=None)
    name: str = field(default="")
    description: str = field(default="")
    state: ProjectState = field(default_factory=lambda: ProjectState())
    ctime: datetime = field(default_factory=lambda: datetime.now())
    mtime: datetime = field(default_factory=lambda: datetime.now())
    ddl: datetime = field(default_factory=lambda: LAST_TIMESTAMP_LIFE)
    extra: dict = field(default_factory=dict)

class ProjectExtra:
    def __init__(self):
        self.json_data = {}

    def _from_json(self, json_data: dict):
        self.json_data = json_data

    def _to_json(self):
        return self.json_data

