# -*- coding: utf-8 -*-
# @file world.py
# @brief The DB World Management
# @author sailing-innocent
# @date 2025-04-28
# @version 1.0
# ---------------------------------

import csv 
from internal.model.content import get_chapter_info_by_book_impl
from internal.model.world import StoryCreate, create_story_impl, get_storys_by_content_node_impl
from utils.jsonb import dict_to_json_bytes, json_bytes_to_dict

def story_conclude(db_func, csv_fpath: str) -> str:
    """
    1. Read the CSV file and parse the data.
    2. Store the data in the database using db_func.
    3. Return a success message.
    """
    db = next(db_func())
    with open(csv_fpath, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Assuming db_func is a function that takes a dictionary and stores it in the database
            book_id = row['book_id']
            chapter_order = row['chapter_order']
            print(f"Processing Book ID: {book_id}, Chapter Order: {chapter_order}")

            chapter_info = get_chapter_info_by_book_impl(db, book_id, chapter_order)
            if len(chapter_info) == 0:
                print(f"Chapter info not found for Book ID: {book_id}, Chapter Order: {chapter_order}")
                continue
            print(f"Chapter Info: {chapter_info[0]}")
            story = row['story']
            print(f"Story: {story}")
            content_node_id = chapter_info[0].content_node_id
            print(f"Content Node ID: {content_node_id}")
            story_dict = {}
            story_dict["raw_data"] = story 

            story_crt = StoryCreate(
                name="conclude",
                content_node_id=content_node_id,
                data=dict_to_json_bytes(story_dict),
            )

            create_story_impl(db, story_crt)

            # fetched_storys = get_storys_by_content_node_impl(db, content_node_id)

            # print(f"Fetched Storys: {fetched_storys}")
            # if len(fetched_storys) == 1:
            #     story_data = json_bytes_to_dict(fetched_storys[0].data)
            #     print(f"Story Data: {story_data}")

        return "Done"