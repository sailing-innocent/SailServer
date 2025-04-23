# -*- coding: utf-8 -*-
# @file debug.py
# @brief The Debug Script Entry
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------
from utils.env import read_env
read_env('debug') # use debug environment for testing
import os 
import argparse 

from internal.db import g_db_func
from task.db.dispatcher import DBTaskDispatcher


if __name__ == "__main__":
    print(os.environ.get('POSTGRE_URI'))
    parser = argparse.ArgumentParser(description="Debug Script")
    parser.add_argument("--task", type=str, help="Task to run")
    # Task arguments, A, B, C, ..
    parser.add_argument("--args", type=str, nargs='+', help="Task arguments")
    args = parser.parse_args()

    task_name = args.task
    task_args = args.args
    if task_args is None: # change None to empty list iterable
        task_args = []

    dispatcher = DBTaskDispatcher(g_db_func)
    try:
        result = dispatcher.dispatch(task_name, task_args)
        print(f"Task {task_name} result: {result}")
    except Exception as e:
        print(f"Error: {e}")
