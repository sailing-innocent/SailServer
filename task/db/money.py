# -*- coding: utf-8 -*-
# @file money.py
# @brief My Personal Money Calculation Task
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

import numpy as np
from internal.model.finance.account import AccountData, fix_account_balance_impl
from internal.model.finance.transaction import read_transactions_impl
import logging
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

logger = logging.getLogger(__name__)


# 计算等额本息方法计价下，初始Q经过利率R和n期数的计算后，得到每月还款金额
def per_mon(Q, R, n):
    return R * (1 + R) ** n / ((1 + R) ** n - 1) * Q


def fix_account_balance(db_func, account_id: int, fix_value: float = 0.0):
    logger.info(
        f"Fixing account balance for account_id={account_id} with fix_value={fix_value}"
    )
    fix_data = AccountData(id=account_id, balance=fix_value)

    try:
        db = next(db_func())
        result = fix_account_balance_impl(db, fix_data)
        logger.info(f"Fixed account balance: {result}")
        return result
    except Exception as e:
        logger.error(f"Error fixing account balance: {e}")
        raise e


def read_transaction(db_func):
    db = next(db_func())
    start_date_literal = "2025-02-20"
    end_date_literal = "2025-05-30"
    start_date = datetime.datetime.strptime(start_date_literal, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_literal, "%Y-%m-%d")

    transactions = read_transactions_impl(
        db,
        from_time=start_date.timestamp(),
        to_time=end_date.timestamp(),
        skip=0,
        limit=1000,
    )

    logger.info(
        f"Read {len(transactions)} transactions from {start_date_literal} to {end_date_literal}"
    )

    return "Done"
