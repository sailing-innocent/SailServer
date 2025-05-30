# -*- coding: utf-8 -*-
# @file money.py
# @brief My Personal Money Calculation Task
# @author sailing-innocent
# @date 2025-04-23
# @version 1.0
# ---------------------------------

import numpy as np
from internal.model.finance.account import AccountData, fix_account_balance_impl
import logging

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
