# -*- coding: utf-8 -*-
# @file content.py
# @brief The Content Storage
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, TEXT, DateTime
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


@dataclass
class BookChaptersData:
    id: int
    title: str
    author: str
    chapters: list[int]


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


# 如果不想进行分段，可以直接从ContentNode查询到Content的id，然后通过Content的id查询到Content的内容，用start和offset来截取返回
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


# The LINKS between content-nodes
# 想要进行分段操作的话，通过Chapter查询到ContentNode的id，然后在ParagraphTree中查询所有分段ID, 迭代出所有的分段
# 通过分段ID查询到ContentNode的id, 然后通过ContentNode的id查询到Content的id, 然后通过Content的id查询到Content的内容


class ParagraphTree(ORMBase):
    __tablename__ = "paragraph_tree"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    root_content_node_id = Column(
        Integer, ForeignKey("content_node.id")
    )  # root node attached
    data = Column(JSONB)  # json binary data


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
    ctime = Column(Integer, nullable=False)  # create time
    mtime = Column(Integer, nullable=False)  # update time
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
    ctime: int = field(default_factory=lambda: int(datetime.datetime.now().timestamp()))
    mtime: int = field(default_factory=lambda: int(datetime.datetime.now().timestamp()))
    tags: str = field(default="")
    content: str = field(default="")
    id: int = field(default=-1)
