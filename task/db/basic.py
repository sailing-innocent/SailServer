# -*- coding: utf-8 -*-
# @file basic.py
# @brief The Basic DB Script
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------


def check_db_conn(db_func):
    db = next(db_func())
    return db is not None
