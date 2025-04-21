# -*- coding: utf-8 -*-
# @file debug.py
# @brief The Debug Script Entry
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

import os 
from utils.env import read_env

if __name__ == "__main__":
    read_env('debug') # use debug environment for testing
    print(os.environ.get('POSTGRE_URI'))
