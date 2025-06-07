# -*- coding: utf-8 -*-
# @file book.py
# @brief The Book Controller Impl
# @author sailing-innocent
# @date 2025-05-21
# @version 1.0
# ---------------------------------

from internal.data.content import BookData, Book, Chapter
from utils.book_parser import BPBook, BPChapter
import logging

logger = logging.getLogger(__name__)

from tqdm import tqdm
from .chapter import create_chapter_from_parser


def book_from_create(create: BookData):
    return Book(title=create.title, author=create.author)


def create_book_impl(db, crt: BookData):
    book = book_from_create(crt)
    db.add(book)
    db.commit()
    return book.id


def create_book_from_parser(db, book: BPBook):
    book_crt = BookData(title=book.title, author=book.author)
    book_id = create_book_impl(db, book_crt)
    for i, chapter in tqdm(enumerate(book.chapters)):
        create_chapter_from_parser(db, chapter, book_id, i)
    return book_id


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

    return BookData(
        id=book.id,
        title=book.title,
        author=book.author,
        chapters=[chapter.id for chapter in chapters],
    )


def read_books_info_impl(db, skip: int, limit: int):
    books = db.query(Book).order_by(Book.id).offset(skip).limit(limit).all()
    return [BookData(id=book.id, title=book.title) for book in books]
