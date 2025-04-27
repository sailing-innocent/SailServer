# -*- coding: utf-8 -*-
# @file content.py
# @brief Parse and use Content
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

from internal.model.content import create_book_from_parser
from utils.book_parser import BPBook, BPChapter, BookParser

def read_book(db_func, book_path: str) -> str:
    return "Done"