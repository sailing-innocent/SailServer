# -*- coding: utf-8 -*-
# @file content.py
# @brief The content model
# @author sailing-innocent
# @date 2025-01-31
# @version 1.0
# ---------------------------------

from pydantic import BaseModel

from internal.data.content import Book, Chapter, ContentNode, Content, ParagraphTree
from utils.book_parser import BPChapter
import time
import logging


def clean_all_impl(db):
    db.query(Content).delete()
    db.query(ContentNode).delete()
    db.query(Chapter).delete()
    db.query(Book).delete()
    db.commit()


class ContentCreate(BaseModel):
    data: str
    size: int


def content_from_create(create: ContentCreate):
    return Content(data=create.data, size=create.size)


def create_content_impl(db, crt: ContentCreate):
    content = content_from_create(crt)
    db.add(content)
    db.commit()
    return content.id, content.size


class ContentNodeCreate(BaseModel):
    raw_tags: str
    tags: str
    content_id: int
    start: int
    offset: int


def content_node_from_create(create: ContentNodeCreate):
    return ContentNode(
        raw_tags=create.raw_tags,
        tags=create.tags,
        content_id=create.content_id,
        start=create.start,
        offset=create.offset,
    )


def create_content_node_impl(db, crt: ContentNodeCreate):
    content_node = content_node_from_create(crt)
    db.add(content_node)
    db.commit()
    return content_node.id


def create_content_with_node_impl(db, crt: ContentCreate):
    cid, sz = create_content_impl(db, crt)
    # the auto binding full node
    node_crt = ContentNodeCreate(
        raw_tags="",
        tags="",
        content_id=cid,
        start=0,
        offset=sz,
    )
    return create_content_node_impl(db, node_crt)


class ChapterCreate(BaseModel):
    title: str
    book_id: int
    content_node_id: int
    order: int


def chapter_from_create(create: ChapterCreate):
    return Chapter(
        title=create.title,
        book_id=create.book_id,
        content_node_id=create.content_node_id,
        ctime=int(time.time()),
        mtime=int(time.time()),
        order=create.order,
    )


def create_chapter_impl(db, crt: ChapterCreate):
    chapter = chapter_from_create(crt)
    db.add(chapter)
    db.commit()
    return chapter.id


class ChapterRead(BaseModel):
    id: int
    title: str
    book_id: int
    content: str
    order: int


class ChapterInfo(BaseModel):
    title: str
    book_id: int
    content_node_id: int
    order: int


def info_from_chapter(chapter: Chapter):
    return ChapterInfo(
        title=chapter.title,
        book_id=chapter.book_id,
        content_node_id=chapter.content_node_id,
        order=chapter.order,
    )


def get_chapter_info_impl(db, chapter_id: int):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        return None
    return info_from_chapter(chapter)


def get_chapter_info_by_book_impl(db, book_id: int, order: int = -1):
    if order == -1:
        chapters = db.query(Chapter).filter(Chapter.book_id == book_id).all()
    else:
        chapters = (
            db.query(Chapter)
            .filter(Chapter.book_id == book_id, Chapter.order == order)
            .all()
        )
    return [info_from_chapter(chapter) for chapter in chapters]


def read_content_by_node_impl(db, node_id: int):
    node = db.query(ContentNode).filter(ContentNode.id == node_id).first()
    if node is None:
        return None
    content = db.query(Content).filter(Content.id == node.content_id).first()
    if content is None:
        return None
    if node.start + node.offset > content.size:
        logging.error("ContentNode out of range")
        return None

    return content.data[node.start : node.start + node.offset]


def read_chapter_impl(db, chapter_id: int):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        return None
    # return read_from_chapter(chapter)
    content = read_content_by_node_impl(db, chapter.content_node_id)
    return ChapterRead(
        id=chapter.id,
        title=chapter.title,
        book_id=chapter.book_id,
        content=content,
        order=chapter.order,
    )


class ParagraphTreeCreate(BaseModel):
    from_content_node_id: int
    to_content_node_id: int


class ParagraphTreeRead(BaseModel):
    id: int
    from_content_node_id: int
    to_content_node_id: int


def paragraph_tree_from_create(create: ParagraphTreeCreate):
    return ParagraphTree(
        from_content_node_id=create.from_content_node_id,
        to_content_node_id=create.to_content_node_id,
    )


def read_from_paragraph_tree(tree: ParagraphTree):
    return ParagraphTreeRead(
        id=tree.id,
        from_content_node_id=tree.from_content_node_id,
        to_content_node_id=tree.to_content_node_id,
    )


def create_paragraph_tree_impl(db, tree_create: ParagraphTreeCreate):
    tree = paragraph_tree_from_create(tree_create)
    db.add(tree)
    db.commit()
    return read_from_paragraph_tree(tree)


def get_paragraph_tree_impl(db, tree_id: int):
    tree = db.query(ParagraphTree).filter(ParagraphTree.id == tree_id).first()
    if tree is None:
        return None
    return read_from_paragraph_tree(tree)


def create_chapter_from_parser(db, chapter: BPChapter, book_id, order):
    content_crt = ContentCreate(data=chapter.content, size=len(chapter.content))
    content_node_id = create_content_with_node_impl(db, content_crt)
    crt = ChapterCreate(
        title=chapter.title,
        book_id=book_id,
        content_node_id=content_node_id,
        order=order,
    )
    return create_chapter_impl(db, crt)
