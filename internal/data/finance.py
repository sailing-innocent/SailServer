# -*- coding: utf-8 -*-
# @file finance.py
# @brief The Finance Data Model
# @author sailing-innocent
# @date 2025-04-21
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey
from .orm import ORMBase
from sqlalchemy.orm import relationship
import time
from internal.util.state import StateBits
from enum import Enum

__all__ = [
    "Account",
    "Transaction",
    "_acc",
    "_acc_inv",
    "_htime",
]


# ------------------------------------
# Financial State
# ------------------------------------
def _acc(x):
    return x if x != -1 else None


def _acc_inv(x):
    return x if x is not None else -1


def _htime(x):
    return x.htime if x.htime != 0 else int(time.time())


class Account(ORMBase):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    balance = Column(String)
    state = Column(Integer)  # 0: physical account 1: budget pocket
    ctime = Column(Integer)
    mtime = Column(Integer)

    # Define relationships without circular foreign_keys
    in_transactions = relationship(
        "Transaction",
        back_populates="to_acc",
        primaryjoin="Account.id==Transaction.to_acc_id",
    )
    out_transactions = relationship(
        "Transaction",
        back_populates="from_acc",
        primaryjoin="Account.id==Transaction.from_acc_id",
    )


class AccountState(StateBits):
    def __init__(self, value: int):
        super().__init__(value)
        # State Machine
        self.set_attrib_map({"valid": 0, "updated": 1})

    def set_valid(self):
        self.set_attrib("valid")

    def unset_valid(self):
        self.unset_attrib("valid")

    def is_valid(self):
        return self.is_attrib("valid")

    def set_updated(self):
        self.set_attrib("updated")

    def unset_updated(self):
        self.unset_attrib("updated")

    def is_updated(self):
        return self.is_attrib("updated")


# transaction
class Transaction(ORMBase):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    from_acc_id = Column(Integer, ForeignKey("accounts.id"))
    to_acc_id = Column(Integer, ForeignKey("accounts.id"))
    # Define relationships with back_populates
    from_acc = relationship(
        "Account", back_populates="out_transactions", foreign_keys=[from_acc_id]
    )
    to_acc = relationship(
        "Account", back_populates="in_transactions", foreign_keys=[to_acc_id]
    )

    value = Column(String)  # Decimal float
    prev_value = Column(String)  # Decimal float
    description = Column(String)
    tags = Column(String)
    state = Column(Integer)  # 0: create 1: valid 2: virtual 3: done 4: cancel
    htime = Column(Integer)  # happen time
    ctime = Column(Integer)
    mtime = Column(Integer)


class TransactionState(StateBits):
    def __init__(self, value: int):
        super().__init__(value)
        # State Machine
        # INVALID -> VALID -> ....(Some Operations)
        # -> VALID -> (Update Operation) UPDATED
        # -> CHANGED -> (Change Operation) -> UPDATED -> ....(Some Operations)
        # -> DEPRECATED (Deprecate Ops)-> INVALID
        self.set_attrib_map(
            {
                "from_acc_valid": 0,
                "to_acc_valid": 1,
                "from_acc_updated": 2,
                "to_acc_updated": 3,
                "from_acc_changed": 4,
                "to_acc_changed": 5,
                "from_acc_deprecated": 6,
                "to_acc_deprecated": 7,
            }
        )

    def set_from_acc_valid(self):
        self.set_attrib("from_acc_valid")

    def unset_from_acc_valid(self):
        self.unset_attrib("from_acc_valid")

    def is_from_acc_valid(self):
        return self.is_attrib("from_acc_valid")

    def set_to_acc_valid(self):
        self.set_attrib("to_acc_valid")

    def unset_to_acc_valid(self):
        self.unset_attrib("to_acc_valid")

    def is_to_acc_valid(self):
        return self.is_attrib("to_acc_valid")

    def set_from_acc_updated(self):
        self.set_attrib("from_acc_updated")

    def unset_from_acc_updated(self):
        self.unset_attrib("from_acc_updated")

    def is_from_acc_updated(self):
        return self.is_attrib("from_acc_updated")

    def set_to_acc_updated(self):
        self.set_attrib("to_acc_updated")

    def unset_to_acc_updated(self):
        self.unset_attrib("to_acc_updated")

    def is_to_acc_updated(self):
        return self.is_attrib("to_acc_updated")

    def set_from_acc_changed(self):
        self.set_attrib("from_acc_changed")

    def unset_from_acc_changed(self):
        self.unset_attrib("from_acc_changed")

    def is_from_acc_changed(self):
        return self.is_attrib("from_acc_changed")

    def set_to_acc_changed(self):
        self.set_attrib("to_acc_changed")

    def unset_to_acc_changed(self):
        self.unset_attrib("to_acc_changed")

    def is_to_acc_changed(self):
        return self.is_attrib("to_acc_changed")

    def set_from_acc_deprecated(self):
        self.set_attrib("from_acc_deprecated")

    def unset_from_acc_deprecated(self):
        self.unset_attrib("from_acc_deprecated")

    def is_from_acc_deprecated(self):
        return self.is_attrib("from_acc_deprecated")

    def set_to_acc_deprecated(self):
        self.set_attrib("to_acc_deprecated")

    def unset_to_acc_deprecated(self):
        self.unset_attrib("to_acc_deprecated")

    def is_to_acc_deprecated(self):
        return self.is_attrib("to_acc_deprecated")
