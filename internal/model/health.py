# -*- coding: utf-8 -*-
# @file health.py
# @brief The Health Data Storage
# @author sailing-innocent
# @date 2025-04-24
# @version 1.0
# ---------------------------------

from internal.data.health import Weight, WeightData
import time


def weight_from_create(create: WeightData):
    return Weight(
        value=create.value,
        htime=create.htime,
    )


def read_from_weight(weight: Weight):
    return WeightData(
        id=weight.id,
        value=weight.value,
        htime=weight.htime,
    )


def create_weight_impl(db, weight_create: WeightData):
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
    return WeightData(weight.id, weight.value, weight.htime) if weight else None


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
