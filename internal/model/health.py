# -*- coding: utf-8 -*-
# @file health.py
# @brief The Health Data Storage
# @author sailing-innocent
# @date 2025-04-24
# @version 1.0
# ---------------------------------

from internal.data.health import Weight, WeightData
import time
from datetime import datetime


def read_from_weight(weight: Weight):
    # print(f"Reading weight: {weight.htime.timestamp()}")
    # if weight is None:
    #     return None
    return WeightData(
        id=weight.id,
        value=weight.value,
        htime=weight.htime.timestamp(),
    )


def weight_from_data(weight_data: WeightData):
    return Weight(
        id=weight_data.id,
        value=weight_data.value,
        htime=datetime.fromtimestamp(weight_data.htime),
        tag=weight_data.tag,
        description=weight_data.description,
    )


def create_weight_impl(db, weight_create: WeightData):
    weight = weight_from_data(weight_create)
    db.add(weight)
    db.commit()
    db.refresh(weight)
    return read_from_weight(weight)


def read_weight_impl(db, weight_record_id: int = -1, _tag: str = None):
    q = db.query(Weight)
    if _tag is not None:
        q = q.filter(Weight.tag == _tag)
    if weight_record_id != -1:
        q = q.filter(Weight.id == weight_record_id)
    weight = q.first()
    return read_from_weight(weight) if weight else None


def read_weights_impl(
    db,
    skip: int = 0,
    limit: int = -1,
    start_time: float = None,  # timestamp in seconds
    end_time: float = None,  # timestamp in seconds
    _tag: str = "raw",
):
    query = db.query(Weight)
    if _tag is not None:
        query = query.filter(Weight.tag == _tag)
    if start_time != None:
        query = query.filter(Weight.htime >= datetime.fromtimestamp(start_time))
    if end_time != None:
        query = query.filter(Weight.htime <= datetime.fromtimestamp(end_time))
    weights = query.order_by(Weight.htime).offset(skip)
    if limit != -1:
        weights = weights.limit(limit)
    weights = weights.all()
    res = [read_from_weight(weight) for weight in weights]
    return res


def update_weight_impl(db, id, weight: WeightData):
    db.query(Weight).filter(Weight.id == id).update(weight_from_data(weight))
    db.commit()
    return read_weight_impl(db, id)


def delete_weight_impl(db, id=None):
    if id is not None:
        db.query(Weight).filter(Weight.id == id).delete()
    else:
        db.query(Weight).delete()
    db.commit()
