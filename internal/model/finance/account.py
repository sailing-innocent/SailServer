# -*- coding: utf-8 -*-
# @file account.py
# @brief Financial account model
# @author sailing-innocent
# @date 2025-05-22
# @version 1.0
# ---------------------------------
from internal.data.finance import Account, AccountState, AccountData
from internal.data.finance import _acc, _acc_inv, _htime
from utils.money import Money
import time
import logging

logger = logging.getLogger(__name__)


def clean_all_impl(db):
    db.query(Account).delete()
    db.commit()


def account_from_create(create: AccountData):
    return Account(
        name=create.name,
    )


def read_from_account(account: Account):
    return AccountData(
        id=account.id,
        name=account.name,
        description=account.description,
        balance=account.balance,
        state=account.state,
        mtime=account.mtime,
    )


def create_account_impl(db, account_create: AccountData):
    account = account_from_create(account_create)
    db.add(account)
    db.commit()
    db.refresh(account)
    return read_from_account(account)


def read_accounts_impl(db, skip: int = 0, limit: int = 10):
    accounts = db.query(Account).offset(skip).limit(limit).all()
    res = [read_from_account(account) for account in accounts]
    return res


def read_account_impl(db, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    res = read_from_account(account)
    return res


def delete_account_impl(db, account_id: int = None):
    if account_id is None:
        # db.query(Account).delete()
        return None
    else:
        db.query(Account).filter(Account.id == account_id).delete()
    db.commit()
