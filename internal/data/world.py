# -*- coding: utf-8 -*-
# @file world.py
# @brief The Novel World
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .orm import ORMBase


class Character(ORMBase):
    __tablename__ = "characters"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)  # character name
    data = Column(JSONB, nullable=True)  # character data in json binary


class Setting(ORMBase):
    __tablename__ = "settings"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)  # setting name
    data = Column(JSONB, nullable=True)  # setting data in json binary


class Story(ORMBase):
    __tablename__ = "stories"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)  # story name
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode", backref="stories")
    data = Column(JSONB, nullable=True)  # story data in json binary


class Description(ORMBase):
    __tablename__ = "descriptions"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode")
    data = Column(JSONB, nullable=True)


class ContentNote(ORMBase):
    __tablename__ = "content_notes"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode", backref="content_notes")
    data = Column(JSONB, nullable=True)  # note data in json binary
