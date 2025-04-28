# -*- coding: utf-8 -*-
# @file dispatcher.py
# @brief The DB Task Dispatcher
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

from task.db.basic import check_db_conn 
from task.db.content_image import create_image, read_image, read_images
from task.db.service_account import create_service_account_from_csv
from task.db.world import story_conclude

class DBTaskDispatcher:
    def __init__(self, db_func):
        self.db_func = db_func
        
        self.tasks = {
            "check_db_conn": check_db_conn,
            "create_image": create_image,
            "read_image": read_image,
            "read_images": read_images,
            "create_service_account_from_csv": create_service_account_from_csv,
            "story_conclude": story_conclude,
        }

    def dispatch(self, task_name, task_args):
        if task_name in self.tasks:
            task_func = self.tasks[task_name]
            return task_func(self.db_func, *task_args)
        else:
            raise ValueError(f"Task {task_name} not found")