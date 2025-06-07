# -*- coding: utf-8 -*-
# @file content.py
# @brief The content model
# @author sailing-innocent
# @date 2025-01-31
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from sqlalchemy import and_

from internal.data.content import (
    Book,
    Chapter,
    ContentNode,
    Content,
    ParagraphTree,
    ContentData,
    ChapterData,
)
from internal.model.content.content import (
    create_content_with_node_impl,
    read_content_data_by_node_impl,
)
from utils.book_parser import BPChapter
import time
import logging


def clean_all_impl(db):
    db.query(Chapter).delete()
    db.query(Book).delete()
    db.commit()


def chapter_from_create(create: ChapterData):
    return Chapter(
        title=create.title,
        book_id=create.book_id,
        content_node_id=create.content_node_id,
        ctime=int(time.time()),
        mtime=int(time.time()),
        order=create.order,
    )


def create_chapter_impl(db, crt: ChapterData):
    chapter = chapter_from_create(crt)
    db.add(chapter)
    db.commit()
    return chapter.id


def info_from_chapter(chapter: Chapter):
    return ChapterData(
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


def read_chapter_impl(db, chapter_id: int):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        return None
    # return read_from_chapter(chapter)
    content_data = read_content_data_by_node_impl(db, chapter.content_node_id)
    return ChapterData(
        id=chapter.id,
        title=chapter.title,
        book_id=chapter.book_id,
        content=content_data,
        order=chapter.order,
    )


def read_book_chapter_impl(db, book_id: int, chapter_order: int):
    """
    target SQL:
    SELECT content_node.start, content_node.offset, content.data, content.size FROM chapter
    INNER JOIN book ON chapter.book_id=book.id
    INNER JOIN content_node ON content_node.id=chapter.content_node_id
    INNER JOIN content ON content.id=content_node.content_id
    WHERE book.id=1 AND chapter.order=13;
    """
    result = (
        db.query(
            Chapter.id,
            Chapter.title,
            Chapter.order,
            ContentNode.start,
            ContentNode.offset,
            Content.data,
            Content.size,
        )
        .join(Book, Chapter.book_id == Book.id)
        .join(ContentNode, ContentNode.id == Chapter.content_node_id)
        .join(Content, Content.id == ContentNode.content_id)
        .filter(and_(Book.id == book_id, Chapter.order == chapter_order))
        .first()
    )

    if result is None:
        return None

    # Extract content data based on start and offset
    content_data = (
        result.data[result.start : result.start + result.offset]
        if result.start is not None and result.offset is not None
        else result.data
    )

    return ChapterData(
        id=result.id,
        title=result.title,
        book_id=book_id,
        content=content_data,
        order=result.order,
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
    content_crt = ContentData(data=chapter.content, size=len(chapter.content))
    content_node_id = create_content_with_node_impl(db, content_crt)
    crt = ChapterData(
        title=chapter.title,
        book_id=book_id,
        content_node_id=content_node_id,
        order=order,
    )
    return create_chapter_impl(db, crt)
