# -*- coding: utf-8 -*-
# @file content.py
# @brief Content Controller
# @author sailing-innocent
# @date 2025-06-02
# @version 1.0
# ---------------------------------

from __future__ import annotations
from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig
from litestar import Controller, get, post, Request

from internal.data.content import ContentData
from sqlalchemy.orm import Session
from typing import Generator

from internal.model.content.content import (
    read_content_impl,
)

from internal.model.content.chapter import read_chapter_impl, read_book_chapter_impl
from internal.data.content import ChapterData


# --------------------------
# CONTENT CONTROLLER
# --------------------------


# Write to DB DTO
class ContentDataWriteDTO(DataclassDTO[ContentData]): ...


# Read from DB DTO
class ContentDataReadDTO(DataclassDTO[ContentData]): ...


class ContentController(Controller):
    dto = ContentDataWriteDTO
    return_dto = ContentDataReadDTO
    path = "/content"

    @get("/{content_id:int}")
    async def get_content(
        self,
        content_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ContentData:
        """
        Get the content data by ID.
        """
        db = next(router_dependency)
        content = read_content_impl(db, content_id)
        request.logger.info(f"Get content: {content}")
        if content is None:
            return None

        return content


# --------------------------
# CHAPTER CONTROLLER
# --------------------------


# Write to DB DTO
class ChapterDataWriteDTO(DataclassDTO[ChapterData]):
    config = DTOConfig(exclude={"id", "ctime", "mtime", "content", "content_node_id"})


class ChapterDataUpdateDTO(DataclassDTO[ChapterData]):
    config = DTOConfig(exclude={"ctime", "mtime", "content_node_id"})


# Read from DB DTO, all available
class ChapterDataReadDTO(DataclassDTO[ChapterData]): ...


class ChapterController(Controller):
    dto = ChapterDataWriteDTO
    return_dto = ChapterDataReadDTO
    path = "/chapter"

    @get("/{chapter_id:int}")
    async def get_chapter(
        self,
        chapter_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ChapterData:
        """
        Get the chapter data by ID.
        """
        db = next(router_dependency)
        chapter = read_chapter_impl(db, chapter_id)
        request.logger.info(f"Get chapter: {chapter}")
        if chapter is None:
            return None

        return chapter

    # get '/' with param ? book={book_id}&order={chapter_order}
    @get("/")
    async def get_book_chapter(
        self,
        book: int,
        order: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ChapterData:
        """
        Get the chapter data by book ID and chapter order.
        """
        db = next(router_dependency)
        chapter = read_book_chapter_impl(db, book, order)
        request.logger.info(f"Get book chapter: {chapter}")
        if chapter is None:
            return None

        return chapter
