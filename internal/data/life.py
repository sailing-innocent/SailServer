# -*- coding: utf-8 -*-
# @file info.py
# @brief Peronsal Information Storage
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from .orm import ORMBase
from sqlalchemy.orm import relationship
from utils.state import StateBits
from internal.data.finance import Transaction
from dataclasses import dataclass, field


class Accommodation(ORMBase):
    __tablename__ = "accommodation"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    assets = relationship("Asset", back_populates="accomodation")


@dataclass
class AccommodationData:
    id: int = field(default=None)
    name: str = field(default="")
    description: str = field(default="")
    address: str = field(default="")


# 固定资产，存放于某个特定住所
class Asset(ORMBase):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    asset_type: str = Column(String)  # cloth, consumable, fixed asset, portable asset
    state = Column(Integer)  # store, wear, dirty, washed, deprecated
    tags = Column(String)  # season, upper/lower, etc.
    accomodation_id = Column(Integer, ForeignKey("accommodation.id"))
    accomodation = relationship("Accommodation", back_populates="assets")
    extra = Column(JSONB, nullable=True)  # extra information, e.g. size, color, etc.


@dataclass
class AssetData:
    id: int = field(default=None)
    name: str = field(default="")
    description: str = field(default="")
    asset_type: str = field(default="")
    state: int = field(default=0)  # default to store
    tags: str = field(default="")
    accomodation_id: int = field(default=None)


class ClothState(StateBits):
    def __init__(self, value: int):
        super().__init__(value)
        # State Machine
        # store, wear, dirty, washed, deprecated
        self.set_attrib_map(
            {"store": 0, "wear": 1, "dirty": 2, "washed": 3, "deprecated": 4}
        )

    def set_store(self):
        self.set_attrib("store")

    def unset_store(self):
        self.unset_attrib("store")

    def is_store(self):
        return self.is_attrib("store")

    def set_wear(self):
        self.set_attrib("wear")

    def unset_wear(self):
        self.unset_attrib("wear")

    def is_wear(self):
        return self.is_attrib("wear")

    def set_dirty(self):
        self.set_attrib("dirty")

    def unset_dirty(self):
        self.unset_attrib("dirty")

    def is_dirty(self):
        return self.is_attrib("dirty")

    def set_washed(self):
        self.set_attrib("washed")

    def unset_washed(self):
        self.unset_attrib("washed")

    def is_washed(self):
        return self.is_attrib("washed")

    def set_deprecated(self):
        self.set_attrib("deprecated")

    def unset_deprecated(self):
        self.unset_attrib("deprecated")

    def is_deprecated(self):
        return self.is_attrib("deprecated")


# 服务资产，存在有效期限
class ServiceAccount(ORMBase):
    __tablename__ = "service_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # account name
    entry = Column(String(255), nullable=False)  # entry website/app name
    username = Column(String(255), nullable=False)  # username
    password = Column(String(255), nullable=False)  # password
    desp = Column(String(255), nullable=True)  # account description
    expire_time = Column(
        BigInteger, nullable=False
    )  # expire time, store as timestamp in seconds


@dataclass
class ServiceAccountData:
    id: int = field(default=None)
    name: str = field(default="")
    entry: str = field(default="")
    username: str = field(default="")
    password: str = field(default="")
    desp: str = field(default="")
    expire_time: int = field(default=0)


class MarketItem(ORMBase):
    __tablename__ = "market_item"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # item name
    description = Column(String(255), nullable=True)  # item description
    MarketItemType = Column(
        String(255), nullable=False
    )  # item type, "stock" | "necessary" | "luxury"
    tag = Column(String(255), nullable=True)  # item tag
    raw_tag = Column(String(255), nullable=True)  # raw item tag
    extra = Column(
        JSONB, nullable=True
    )  # extra information, e.g. item source, item trend, etc.


@dataclass
class MarketItemData:
    id: int = field(default=None)
    name: str = field(default="")
    description: str = field(default="")
    MarketItemType: str = field(default="")  # asset
    tag: str = field(default="")


class MarketPriceRecord(ORMBase):
    __tablename__ = "market_price_record"
    id = Column(Integer, primary_key=True)
    price = Column(
        Integer, nullable=False
    )  # item price, for comparison, store money as int
    payment = Column(
        JSONB, nullable=False
    )  # payment attribute e.g. currency, payment routine, payment method ...
    item_id = Column(Integer, ForeignKey("market_item.id"), nullable=False)
    item = relationship("MarketItem", backref="price_records")
    date = Column(
        BigInteger, nullable=False
    )  # record date, store as timestamp in seconds
    extra = Column(
        JSONB, nullable=True
    )  # extra information, e.g. price source, price trend, etc.


@dataclass
class MarketPriceRecordData:
    id: int = field(default=None)
    price: int = field(default=0)
    payment: dict = field(default_factory=dict)
    item_id: int = field(default=None)


# The Purchase Record, link the transaction and market price record
class Purchase(ORMBase):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    transaction = relationship("Transaction", backref="payments")
    item_amount = Column(Integer, nullable=False)  # purchase amount
    market_price_record_id = Column(
        Integer, ForeignKey("market_price_record.id"), nullable=False
    )  # binding price record
    total_price = Column(
        Integer, nullable=False
    )  # total price estimated/valid, store money as int
    extra = Column(
        JSONB, nullable=True
    )  # extra information, e.g. purchase source, purchase trend, is_budget, etc.


@dataclass
class PurchaseData:
    id: int = field(default=None)
    transaction_id: int = field(default=None)
    item_amount: int = field(default=0)
    market_price_record_id: int = field(default=None)
    total_price: int = field(default=0)
    extra: dict = field(default_factory=dict)


# -----------------------------------------
# The Life Project Notification
# -----------------------------------------


class Project(ORMBase):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    parent_id = Column(
        Integer, ForeignKey("projects.id"), nullable=True
    )  # self reference for sub-projects
    parent = relationship(
        "Project", remote_side=[id], backref="sub_projects"
    )  # self reference for sub-projects
    name = Column(String)
    description = Column(String)
    raw_tags = Column(String)  # raw tags, comma separated
    tags = Column(String)  # processed tags, space separated
    state = Column(Integer)  # 0: active, 1: archived
    ctime = Column(
        BigInteger, nullable=False
    )  # creation time, store as timestamp in seconds
    mtime = Column(
        BigInteger, nullable=False
    )  # modification time, store as timestamp in seconds
    ddl = Column(BigInteger)  # deadline in timestamp in seconds
    weight = Column(Integer)  # weight for sorting importance, default to 0
    extra = Column(
        JSONB, nullable=True
    )  # extra information, e.g. priority, progress, requirement condition, etc.


@dataclass
class ProjectData:
    """
    The Project Data
    """

    id: int = field(default=None)
    parent_id: int = field(default=None)
    name: str = field(default="")
    description: str = field(default="")
    raw_tags: str = field(default="")
    tags: str = field(default="")
    state: int = field(default=0)
    ctime: int = field(default=0)
    mtime: int = field(default=0)
    ddl: int = field(default=0)
    weight: int = field(default=0)
    extra: dict = field(default_factory=dict)


class Notification(ORMBase):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)  # notification title
    content = Column(String(1024), nullable=False)  # notification content
    expire_time = Column(
        BigInteger, nullable=False
    )  # expire time, store as timestamp in seconds
    state = Column(
        Integer, nullable=False, default=0
    )  # notification state, unread|expired|read|archived


@dataclass
class NotificationData:
    id: int = field(default=None)
    title: str = field(default="")
    content: str = field(default="")
    expire_time: int = field(default=0)
    state: int = field(default=0)
