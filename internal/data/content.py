# -*- coding: utf-8 -*-
# @file content.py
# @brief The Content Storage
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, TEXT, DateTime, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from dataclasses import dataclass, field
from .orm import ORMBase
import datetime


class Book(ORMBase):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)


@dataclass
class BookData:
    """
    The Book Data
    """

    author: str
    title: str
    id: int = field(default=-1)
    chapters: list[int] = field(default_factory=list)  # list of chapter ids


class Chapter(ORMBase):
    __tablename__ = "chapter"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    book_id = Column(Integer, ForeignKey("book.id"))
    book = relationship("Book", backref="chapters")
    content_node_id = Column(Integer, ForeignKey("content_node.id"))
    content_node = relationship("ContentNode")
    ctime = Column(TIMESTAMP, server_default=func.current_timestamp())
    mtime = Column(TIMESTAMP, server_default=func.current_timestamp())
    order = Column(Integer)  # order of the chapter in the book


@dataclass
class ChapterData:
    id: int = field(default=-1)
    title: str = field(default="")
    book_id: int = field(default=-1)
    content_node_id: int = field(default=-1)
    ctime: datetime = field(default_factory=lambda: datetime.datetime.now())
    mtime: datetime = field(default_factory=lambda: datetime.datetime.now())
    order: int = field(default=0)
    content: str = field(default="")  # return content as string


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


@dataclass
class ContentNodeData:
    id: int = field(default=-1)
    content_id: int = field(default=-1)
    raw_tags: str = field(default="")
    tags: str = field(default="")
    start: int = field(default=0)
    offset: int = field(default=0)


@dataclass
class ContentData:
    """
    The Content Data
    """

    id: int = field(default=-1)
    data: str = field(default="")
    size: int = field(default=0)


class ParagraphTree(ORMBase):
    __tablename__ = "paragraph_tree"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    root_content_node_id = Column(
        Integer, ForeignKey("content_node.id")
    )  # root node attached
    data = Column(JSONB)  # json binary data


# --------------
# Image Storage
# --------------


class DBImage(ORMBase):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # image name
    data = Column(LargeBinary, nullable=False)  # image data in binary
    htime = Column(Integer, nullable=False)  # update time
    desp = Column(String(255), nullable=True)  # image description


@dataclass
class DBImageData:
    id: int
    name: str
    data: bytes
    htime: int
    desp: str = field(default="")


# --------------
# Vault Note
# --------------


class VaultNote(ORMBase):
    __tablename__ = "vault_note"
    id = Column(Integer, primary_key=True)
    vault_name = Column(String(255), nullable=False)  # vault name
    note_path = Column(String(255), nullable=False)  # note path
    note_id = Column(String(255), nullable=False)  # note uuid
    title = Column(String(255), nullable=False)  # note title
    desc = Column(String(255), nullable=True)  # note description
    ctime = Column(TIMESTAMP, server_default=func.current_timestamp())  # create time
    mtime = Column(TIMESTAMP, server_default=func.current_timestamp())  # update time
    tags = Column(String(255), nullable=True)  # note tags
    content = Column(TEXT, nullable=True)  # raw content with metadata


@dataclass
class VaultNoteData:
    """
    The Vault Note Data
    """

    vault_name: str
    note_path: str
    note_id: str
    title: str
    desc: str = field(default="")
    ctime: datetime = field(default_factory=lambda: datetime.datetime.now())
    mtime: datetime = field(default_factory=lambda: datetime.datetime.now())
    tags: str = field(default="")
    content: str = field(default="")
    id: int = field(default=-1)
