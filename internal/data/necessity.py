# -*- coding: utf-8 -*-
# @file necessity.py
# @brief The Necessity Data Format
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from sqlalchemy import Column, Integer, String, ForeignKey
from .orm import ORMBase
from sqlalchemy.orm import relationship
from internal.util.state import StateBits

class Accommodation(ORMBase):
    __tablename__ = "accommodation"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    assets = relationship("Asset", back_populates="accomodation")

class Asset(ORMBase):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    asset_type: str = Column(String) # cloth, consumable, fixed asset, portable asset
    state = Column(Integer) # store, wear, dirty, washed, deprecated
    tags = Column(String) # season, upper/lower, etc.
    accomodation_id = Column(Integer, ForeignKey("accommodation.id"))
    accomodation = relationship("Accommodation", back_populates="assets")

class ClothState(StateBits):
    def __init__(self, value: int):
        super().__init__(value)
        # State Machine
        # store, wear, dirty, washed, deprecated
        self.set_attrib_map({"store": 0, "wear": 1, "dirty": 2, "washed": 3, "deprecated": 4})

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
