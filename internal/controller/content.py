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


# Write to DB DTO
class WeightDataWriteDTO(DataclassDTO[ContentData]): ...


# Read from DB DTO
class ContentDataReadDTO(DataclassDTO[ContentData]): ...


class ContentController(Controller):
    dto = WeightDataWriteDTO
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
