# -*- coding: utf-8 -*-
# @file content.py
# @brief The Content Storage
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .orm import ORMBase


class Book(ORMBase):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)


class Chapter(ORMBase):
    __tablename__ = "chapter"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    book_id = Column(Integer, ForeignKey("book.id"))
    book = relationship("Book", backref="chapters")
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode")
    ctime = Column(Integer)
    mtime = Column(Integer)
    order = Column(Integer)  # order of the chapter in the book


class ContentNode(ORMBase):
    __tablename__ = "content_node"
    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey("content.id"))
    content = relationship(
        "Content", back_populates="attached_nodes", foreign_keys=[content_id]
    )

    raw_tags = Column(String)  # raw tags, by user
    tags = Column(String)  # tags, by system
    start = Column(Integer)
    offset = Column(Integer)


# The Real Content Storage
class Content(ORMBase):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True)
    data = Column(String)
    size = Column(Integer)
    attached_nodes = relationship(
        "ContentNode",
        back_populates="content",
        primaryjoin="Content.id==ContentNode.content_id",
    )
