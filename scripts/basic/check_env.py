# -*- coding: utf-8 -*-
# @file check_env.py
# @brief Scripts to Check Environment
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

import dotenv
import os 

def read_env(mode='dev'):
    # read .env.dev file or .env.prod file
    if mode == 'dev':
        env_file = '.env.dev'
    elif mode == 'prod':
        env_file = '.env.prod'
    else:
        raise ValueError('mode must be dev or prod')

    dotenv.load_dotenv(env_file)

