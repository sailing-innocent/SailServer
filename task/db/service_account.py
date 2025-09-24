# -*- coding: utf-8 -*-
# @file service_account.py
# @brief The Service Account Model
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

from internal.model.service import (
    ServiceAccount,
    ServiceAccountCreate,
    ServiceAccountRead,
    create_service_account_impl,
    get_service_account_impl,
    get_service_accounts_impl,
    update_service_account_impl,
    delete_service_account_impl,
)

from internal.db import g_db_func
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import time


def create_service_account_from_csv(db_func, csv_path: str) -> List[ServiceAccountRead]:
    db = next(db_func())
    service_accounts = []
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            e_time = row["expire_time"]
            # if None, set to 2099-12-31
            if e_time == "":
                e_time = "2037-12-31"
            # transfer to timestamp
            e_time = time.mktime(time.strptime(e_time, "%Y-%m-%d"))
            service_account_create = ServiceAccountCreate(
                name=row["name"],
                entry=row["entry"],
                username=row["username"],
                password=row["password"],
                desp=row["desp"],
                expire_time=e_time,
            )
            print("Creating service account: ", service_account_create)

            create_service_account_impl(db, service_account_create)

    return "Done"
