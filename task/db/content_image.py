# -*- coding: utf-8 -*-
# @file content_image.py
# @brief The content image model
# @author sailing-innocent
# @date 2025-04-24
# @version 1.0
# ---------------------------------

from utils.image import image_to_bytes, bytes_to_image
from internal.model.content import create_image_impl, get_image_impl, delete_image_impl, ImageCreate
from PIL import Image 
import os 
import numpy as np 

def create_image(db_func, img_path, img_name):
    db = next(db_func())
    image = Image.open(img_path).convert("RGB")
    img_data = image_to_bytes(image, format="PNG")
    img_create = ImageCreate(
        name=img_name,
        data=img_data,
        htime=0,
        desp="Sample Image")
    image = create_image_impl(db, img_create)
    
    # Read image from db
    print("Saved image to db, with id: ", image.id)
    id = image.id
    image = get_image_impl(db, id)
    print("Read image from db, with id: ", image.id)

    image = bytes_to_image(image.data)

    # print image metadata
    print("Image size: ", image.size)
    print("Image format: ", image.format)
    print("Image mode: ", image.mode)
    # Save to out.png
    image.save("out.png")
    print("Saved image to out.png")

    # delete image from db
    delete_image_impl(db, id)
    print("Deleted image from db, with id: ", id)
    

    return "Done"
