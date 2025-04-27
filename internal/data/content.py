# -*- coding: utf-8 -*-
# @file content.py
# @brief The Content Storage
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
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
    id = Column(Integer, primary_key=True)
    from_content_node_id = Column(Integer, ForeignKey("content_node.id"))
    to_content_node_id = Column(Integer, ForeignKey("content_node.id"))

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


class DBImage(ORMBase):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # image name
    data = Column(LargeBinary, nullable=False)  # image data in binary
    htime = Column(Integer, nullable=False)  # update time
    desp = Column(String(255), nullable=True)  # image description

