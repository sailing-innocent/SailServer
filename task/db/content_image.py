# -*- coding: utf-8 -*-
# @file content_image.py
# @brief The content image model
# @author sailing-innocent
# @date 2025-04-24
# @version 1.0
# ---------------------------------

from utils.image import image_to_bytes, bytes_to_image
from internal.data.content import DBImageData
from internal.model.content.image import (
    create_image_impl,
    get_image_impl,
    delete_image_impl,
    get_images_impl,
)
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def create_image(db_func, img_path: str, img_name: str = "", debug: bool = False):
    db = next(db_func())
    image = Image.open(img_path).convert("RGB")
    img_data = image_to_bytes(image, format="PNG")
    if img_name == "":
        img_name = img_path.split("\\")[-1].split(".")[0]

    img_create = DBImageData(name=img_name, data=img_data, htime=0, desp="Sample Image")
    image = create_image_impl(db, img_create)

    # Read image from db
    logger.info("Saved image to db, with id: ", image.id)
    id = image.id
    image = get_image_impl(db, id)
    logger.info("Read image from db, with id: ", image.id)

    image = bytes_to_image(image.data)

    # print image metadata
    logger.info("Image size: ", image.size)
    logger.info("Image format: ", image.format)
    logger.info("Image mode: ", image.mode)
    # Save to out.png
    if debug:
        image.save("out.png")
        logger.info("Saved image to out.png")
        delete_image_impl(db, id)
        logger.info("Deleted image from db, with id: ", id)

    return "Done"


def read_image(db_func, id: int):
    db = next(db_func())
    image = get_image_impl(db, id)
    logger.info("Read image from db, with id: ", image.id)

    image = bytes_to_image(image.data)

    # print image metadata
    logger.info("Image size: ", image.size)
    logger.info("Image format: ", image.format)
    logger.info("Image mode: ", image.mode)
    # Save to out.png
    image.save("out.png")
    logger.info("Saved image to out.png")
    return "Done"


def read_images(db_func, out_dir: str):
    db = next(db_func())
    images = get_images_impl(db)
    logger.info("Read images from db, with ids: ", [image.id for image in images])
    for dbimage in images:
        image = bytes_to_image(dbimage.data)
        # print image metadata
        logger.info("Image size: ", image.size)
        logger.info("Image format: ", image.format)
        logger.info("Image mode: ", image.mode)
        # Save to out.png
        image.save(f"{out_dir}/{dbimage.name}.png")
        logger.info(f"Saved image to {out_dir}/{dbimage.name}.png")
    return "Done"
