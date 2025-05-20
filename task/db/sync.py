# -*- coding: utf-8 -*-
# @file sync.py
# @brief Sync Database
# @author sailing-innocent
# @date 2025-05-20
# @version 1.0
# ---------------------------------


def sync(db_gen, from_db_name: str, to_db_name: str):
    """
    Sync the database from one to another, in a Master-Slave setup. for all tables in from_db, if already exist in to_db,
    then clear the table in to_db, and copy all data from from_db to to_db.

    Args:
        db_gen: The database function to use for syncing.
        from_db_name (str): The name of the source database.
        to_db_name (str): The name of the target database.
    """

    pass
