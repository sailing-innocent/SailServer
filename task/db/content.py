# -*- coding: utf-8 -*-
# @file content.py
# @brief Parse and use Content
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

from internal.model.content.book import create_book_from_parser
from internal.model.content.chapter import read_chapter_impl
from utils.book_parser import BPBook, BPChapter, BookParser

import logging

logger = logging.getLogger(__name__)


def read_book(db_func, book_path: str) -> str:
    return "Done"


def split_paragraph(db_func, chapter_id: str) -> str:
    db = next(db_func())
    chapter_id = int(chapter_id)
    chapter = read_chapter_impl(db, chapter_id)
    logger.info(chapter)

    return "Done"
