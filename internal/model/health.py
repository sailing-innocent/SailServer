# -*- coding: utf-8 -*-
# @file health.py
# @brief The Health Data Storage
# @author sailing-innocent
# @date 2025-04-24
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.health import Weight, WeightRecord
import time


class WeightCreate(BaseModel):
    value: str
    htime: int


class WeightRead(BaseModel):
    id: int
    value: str
    htime: int


def weight_from_create(create: WeightCreate):
    return Weight(
        value=create.value,
        htime=create.htime,
    )


def read_from_weight(weight: Weight):
    return WeightRead(
        id=weight.id,
        value=weight.value,
        htime=weight.htime,
    )


def create_weight_impl(db, weight_create: WeightCreate):
    # if htime is None, use current time
    if weight_create.htime == 0:
        weight_create.htime = int(time.time())

    weight = weight_from_create(weight_create)
    db.add(weight)
    db.commit()
    db.refresh(weight)
    return read_from_weight(weight)


def read_weight_impl(db, weight_record_id: int):
    weight = db.query(Weight).filter(Weight.id == weight_record_id).first()
    return weight


def read_weights_impl(
    db, skip: int = 0, limit: int = -1, start_time: int = -1, end_time: int = -1
):
    # weights = db.query(Weight).order_by(Weight.htime).offset(skip).limit(limit).all()
    query = db.query(Weight)
    if start_time != -1:
        query = query.filter(Weight.htime >= start_time)
    if end_time != -1:
        query = query.filter(Weight.htime <= end_time)
    weights = query.order_by(Weight.htime).offset(skip)
    if limit != -1:
        weights = weights.limit(limit)
    weights = weights.all()
    res = [read_from_weight(weight) for weight in weights]
    return res


def update_weight_impl(db, id, weight):
    db.query(Weight).filter(Weight.id == id).update(weight.dict())
    db.commit()
    return read_weight_impl(db, id)


def delete_weight_impl(db, id=None):
    if id is not None:
        db.query(Weight).filter(Weight.id == id).delete()
    else:
        db.query(Weight).delete()
    db.commit()


class WeightRecordCreate(BaseModel):
    value: str
    htime: int
    tag: str


class WeightRecordRead(BaseModel):
    id: int
    value: str
    htime: int
    tag: str


def weight_record_from_create(create: WeightRecordCreate):
    return WeightRecord(
        value=create.value,
        htime=create.htime,
        tag=create.tag,
    )


def read_from_weight_record(weight: WeightRecord):
    return WeightRecordRead(
        id=weight.id,
        value=weight.value,
        htime=weight.htime,
        tag=weight.tag,
    )


def create_weight_record_impl(db, weight_create: WeightRecordCreate):
    # if htime is None, use current time
    if weight_create.htime == 0:
        weight_create.htime = int(time.time())

    weight = weight_record_from_create(weight_create)
    db.add(weight)
    db.commit()
    db.refresh(weight)
    return read_from_weight_record(weight)


def read_weight_record_impl(db, weight_record_id: int = -1, _tag: str = ""):
    if weight_record_id == -1 and _tag == "":
        weight = db.query(WeightRecord).first()
    elif weight_record_id != -1:
        weight = (
            db.query(WeightRecord).filter(WeightRecord.id == weight_record_id).first()
        )
    elif _tag != "":
        # filter WeightRecord.tag contains _tag
        weight = (
            db.query(WeightRecord)
            .filter(WeightRecord.tag.contains(_tag))
            .order_by(WeightRecord.htime)
            .first()
        )

    return weight


def read_weight_records_impl(
    db, skip: int = 0, limit: int = -1, start_time: int = -1, end_time: int = -1
):
    # weights = db.query(Weight).order_by(Weight.htime).offset(skip).limit(limit).all()
    query = db.query(WeightRecord)
    if start_time != -1:
        query = query.filter(WeightRecord.htime >= start_time)
    if end_time != -1:
        query = query.filter(WeightRecord.htime <= end_time)
    weights = query.order_by(WeightRecord.htime).offset(skip)
    if limit != -1:
        weights = weights.limit(limit)
    weights = weights.all()
    res = [read_from_weight_record(weight) for weight in weights]
    return res


def update_weight_record_impl(db, id, weight):
    db.query(WeightRecord).filter(WeightRecord.id == id).update(weight.dict())
    db.commit()
    return read_weight_record_impl(db, id)


def delete_weight_record_impl(db, id=None):
    if id is not None:
        db.query(WeightRecord).filter(WeightRecord.id == id).delete()
    else:
        db.query(WeightRecord).delete()
    db.commit()
