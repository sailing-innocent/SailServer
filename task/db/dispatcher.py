# -*- coding: utf-8 -*-
# @file dispatcher.py
# @brief The DB Task Dispatcher
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

from task.db.basic import check_db_conn 

class DBTaskDispatcher:
    def __init__(self, db_func):
        self.db_func = db_func
        
        self.tasks = {
            "check_db_conn": check_db_conn,
        }

    def dispatch(self, task_name, task_args):
        if task_name in self.tasks:
            task_func = self.tasks[task_name]
            return task_func(self.db_func, *task_args)
        else:
            raise ValueError(f"Task {task_name} not found")