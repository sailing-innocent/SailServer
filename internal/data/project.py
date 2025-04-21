# -*- coding: utf-8 -*-
# @file time.py
# @brief Time Management
# @author sailing-innocent
# @date 2025-01-30
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey
from .orm import ORMBase
from sqlalchemy.orm import relationship
from internal.util.state import StateBits


# Available Time Arena
class TimeSpan(ORMBase):
    __tablename__ = "time_span"
    id = Column(Integer, primary_key=True)
    start = Column(Integer)  # start time of the span
    end = Column(Integer)  # end time of the span


class Project(ORMBase):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    # The Project Tree Relationship
    name: str = Column(String)  # name of the project
    parent_id = Column(Integer)
    description = Column(String)  # description of the project
    raw_tags = Column(String)  # raw tags, by user
    tags = Column(String)  # tags, by system
    weight = Column(Integer)  # weight of the project
    time_required = Column(Integer)  # time required to finish the project
    state = Column(Integer)  # 0: create 1: valid 2: done 3: cancel
    ddl = Column(Integer)  # deadline of the project

# Project Life Cycle
# Validated: The project is valid and can be conducted
# Updated: The project is updated ( all of its children are updated or done)
# Done: The project is done (all of its children are done)
# Cancel: The project is canceled
class ProjectState(StateBits):
    def __init__(self, value: int):
        super().__init__(value)
        # State Machine
        self.set_attrib_map({"valid": 0, "updated": 1, "done": 2, "cancel": 3})

    def set_valid(self):
        self.set_attrib("valid")

    def unset_valid(self):
        self.unset_attrib("valid")

    def is_valid(self):
        return self.is_attrib("valid")

    def set_updated(self):
        self.set_attrib("updated")

    def unset_updated(self):
        self.unset_attrib("updated")

    def is_updated(self):
        return self.is_attrib("updated")

    def set_done(self):
        self.set_attrib("done")

    def unset_done(self):
        self.unset_attrib("done")

    def is_done(self):
        return self.is_attrib("done")

    def set_cancel(self):
        self.set_attrib("cancel")

    def unset_cancel(self):
        self.unset_attrib("cancel")

    def is_cancel(self):
        return self.is_attrib("cancel")


# Mission is the real task conducted in specific time span for a specific project
class Mission(ORMBase):
    __tablename__ = "mission"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project", backref="missions")
    time_span_id = Column(Integer, ForeignKey("time_span.id"))
    time_span = relationship("TimeSpan", backref="missions")
    weight = Column(Integer)  # weight of the mission
    time_required = Column(Integer)  # time required to finish the mission
    state = Column(Integer)  # 0: create 1: valid 2: done 3: cancel

# Event Tracks the outside event
class Event(ORMBase):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    start = Column(Integer)  # start time of the event
    end = Column(Integer)  # end time
    description = Column(String)  # description of the event
    tags = Column(String)  # tags of the event