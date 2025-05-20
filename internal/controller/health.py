# -*- coding: utf-8 -*-
# @file health.py
# @brief Health Controler
# @author sailing-innocent
# @date 2025-05-20
# @version 1.0
# ---------------------------------
from __future__ import annotations
from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig
from litestar import Controller, delete, get, post, put, Request

from internal.data.health import WeightData, WeightRecordData
from internal.model.health import read_weight_impl
from sqlalchemy.orm import Session
from typing import Generator


class WeightDataWriteDTO(DataclassDTO[WeightData]):
    config = DTOConfig(exclude={"id"})


class WeightDataReadDTO(DataclassDTO[WeightData]): ...


class WeightController(Controller):
    dto = WeightDataWriteDTO
    return_dto = WeightDataReadDTO
    path = "/weight"

    @get("/{weight_id:int}")
    async def get_weight(
        self,
        weight_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> WeightData:
        """
        Get the weight data.
        """
        db = next(router_dependency)
        weight = read_weight_impl(db, weight_id)
        request.logger.info(f"Get weight: {weight}")
        if weight is None:
            return None

        return weight


class WeightRecordDataWriteDTO(DataclassDTO[WeightRecordData]):
    config = DTOConfig(exclude={"id"})


class WeightRecordDataReadDTO(DataclassDTO[WeightRecordData]): ...


class WeightRecordController(Controller):
    dto = WeightRecordDataWriteDTO
    read_dto = WeightRecordDataReadDTO
    path = "/weight_record"

    @get("/{weight_record_id:int}")
    async def get_weight_record(
        self, weight_record_id: int, router_dependency: Generator[Session, None, None]
    ) -> WeightRecordData:
        """
        Get the weight record data.
        """
        db = next(router_dependency)
        weight_record = read_weight_impl(db, weight_record_id)
        if weight_record is None:
            return None

        return weight_record
