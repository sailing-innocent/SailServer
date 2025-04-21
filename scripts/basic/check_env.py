# -*- coding: utf-8 -*-
# @file check_env.py
# @brief Scripts to Check Environment
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

import dotenv
import os 
from utils.env import read_env

if __name__ == "__main__":
    read_env('dev')
    # read_env('debug')
    # read_env('prod')