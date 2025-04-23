# -*- coding: utf-8 -*-
# @file test.py
# @brief The TestSuite Entry
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from utils.env import read_env
read_env('dev') # use dev environment for testing

if __name__ == "__main__":
    print(os.environ.get('POSTGRE_URI'))
    # ----------------------------------------
