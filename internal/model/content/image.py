# -*- coding: utf-8 -*-
# @file image.py
# @brief The DBImage
# @author sailing-innocent
# @date 2025-05-22
# @version 1.0
# ---------------------------------
# ----------------------------------------
# Image Resources
# ----------------------------------------

from internal.data.content import DBImage, DBImageData


def image_from_create(create: DBImageData):
    return DBImage(
        name=create.name,
        data=create.data,
        htime=create.htime,
        desp=create.desp,
    )


def image_from_read(read: DBImageData):
    return DBImage(
        id=read.id,
        name=read.name,
        data=read.data,
        htime=read.htime,
        desp=read.desp,
    )


def read_from_image(image: DBImage, no_data: bool = False):
    data = image.data if not no_data else None
    return DBImageData(
        id=image.id,
        name=image.name,
        data=data,
        htime=image.htime,
        desp=image.desp,
    )


def create_image_impl(db, image_create: DBImageData):
    image = image_from_create(image_create)
    db.add(image)
    db.commit()
    return read_from_image(image)


def get_image_impl(db, image_id: int, no_data: bool = False):
    image = db.query(DBImage).filter(DBImage.id == image_id).first()
    if image is None:
        return None
    return read_from_image(image, no_data)


def update_image_impl(db, image_id: int, image_update: DBImageData):
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
