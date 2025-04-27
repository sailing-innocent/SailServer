# -*- coding: utf-8 -*-
# @file world.py
# @brief The Novel World
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .orm import ORMBase

class Character(ORMBase):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # character name
    data = Column(LargeBinary, nullable=False)  # character data in json binary

class Setting(ORMBase):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # setting name
    data = Column(LargeBinary, nullable=False)  # setting data in json binary

class Story(ORMBase):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # story name
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode", backref="stories")
    data = Column(LargeBinary, nullable=False)  # story data in json binary

class Description(ORMBase):
    __tablename__ = "descriptions"
    id = Column(Integer, primary_key=True)
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode")
    data = Column(LargeBinary, nullable=False)  # description data in json binary

class ContentNote(ORMBase):
    __tablename__ = "content_notes"
    id = Column(Integer, primary_key=True)
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode", backref="content_notes")
    data = Column(LargeBinary, nullable=False)  # note data in json binary