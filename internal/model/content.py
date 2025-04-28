# -*- coding: utf-8 -*-
# @file content.py
# @brief The content model
# @author sailing-innocent
# @date 2025-01-31
# @version 1.0
# ---------------------------------

from pydantic import BaseModel

from internal.data.content import Book, Chapter, ContentNode, Content, ParagraphTree
from utils.book_parser import BPBook, BPChapter
import time
import logging
from tqdm import tqdm


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


class BookCreate(BaseModel):
    title: str
    author: str

def book_from_create(create: BookCreate):
    return Book(title=create.title, author=create.author)

def create_book_impl(db, crt: BookCreate):
    book = book_from_create(crt)
    db.add(book)
    db.commit()
    return book.id


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    chapters: list[int]  # list of chapter ids


class BookInfo(BaseModel):
    id: int
    title: str

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
        chapters = db.query(Chapter).filter(
            Chapter.book_id == book_id, Chapter.order == order
        ).all()
    return [info_from_chapter(chapter) for chapter in chapters]

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


def create_book_from_parser(db, book: BPBook):
    book_crt = BookCreate(title=book.title, author=book.author)
    book_id = create_book_impl(db, book_crt)
    for i, chapter in tqdm(enumerate(book.chapters)):
        create_chapter_from_parser(db, chapter, book_id, i)
    return book_id


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

def read_book_impl(db, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        return None
    chapters = (
        db.query(Chapter)
        .filter(Chapter.book_id == book_id)
        .order_by(Chapter.order)
        .all()
    )
    return BookRead(
        id=book.id,
        title=book.title,
        author=book.author,
        chapters=[chapter.id for chapter in chapters],
    )


def read_books_info_impl(db, skip: int, limit: int):
    books = db.query(Book).order_by(Book.id).offset(skip).limit(limit).all()
    return [BookInfo(id=book.id, title=book.title) for book in books]

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

# ----------------------------------------
# Image Resources
# ----------------------------------------

from internal.data.content import DBImage

class ImageCreate(BaseModel):
    name: str
    data: bytes
    htime: int
    desp: str

class ImageRead(BaseModel):
    id: int
    name: str
    data: bytes
    htime: int
    desp: str

def image_from_create(create: ImageCreate):
    return DBImage(
        name=create.name,
        data=create.data,
        htime=create.htime,
        desp=create.desp,
    )

def image_from_read(read: ImageRead):
    return DBImage(
        id=read.id,
        name=read.name,
        data=read.data,
        htime=read.htime,
        desp=read.desp,
    )

def read_from_image(image: DBImage, no_data: bool = False):
    data = image.data if not no_data else None
    return ImageRead(
        id=image.id,
        name=image.name,
        data=data,
        htime=image.htime,
        desp=image.desp,
    )

def create_image_impl(db, image_create: ImageCreate):
    image = image_from_create(image_create)
    db.add(image)
    db.commit()
    return read_from_image(image)

def get_image_impl(db, image_id: int, no_data: bool = False):
    image = db.query(DBImage).filter(DBImage.id == image_id).first()
    if image is None:
        return None
    return read_from_image(image, no_data)

def update_image_impl(db, image_id: int, image_update: ImageCreate):
    image = db.query(DBImage).filter(DBImage.id == image_id).first()
    if image is None:
        return None
    if image_update.name is not None:
        image.name = image_update.name
    if image_update.data is not None:
        image.data = image_update.data
    if image_update.htime is not None:
        image.htime = image_update.htime
    if image_update.desp is not None:
        image.desp = image_update.desp
    db.commit()
    return read_from_image(image)

def delete_image_impl(db, image_id: int):
    image = db.query(DBImage).filter(DBImage.id == image_id).first()
    if image is None:
        return None
    db.delete(image)
    db.commit()
    return read_from_image(image)

def get_images_impl(db, skip: int = 0, limit: int = 0, no_data: bool = False):
    query = db.query(DBImage).order_by(DBImage.id)
    if skip > 0:
        query = query.offset(skip)
    if limit > 0:
        query = query.limit(limit)
    images = query.all()
    return [read_from_image(image, no_data) for image in images]