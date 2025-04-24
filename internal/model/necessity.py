# -*- coding: utf-8 -*-
# @file necessity.py
# @brief The Necessity Model
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.necessity import Accommodation, Asset, ClothState

def clean_all_impl(db):
    db.query(Asset).delete()
    db.query(Accommodation).delete()
    db.commit()

# ------------------------------------------------
# Accommodation
# ------------------------------------------------

class AccommodationCreate(BaseModel):
    name: str
    description: str
    address: str

class AccommodationRead(BaseModel):
    id: int
    name: str
    description: str
    address: str

def accommodation_from_create(create: AccommodationCreate):
    return Accommodation(name=create.name, description=create.description, address=create.address)

def read_from_accommodation(accommodation: Accommodation):
    return AccommodationRead(id=accommodation.id, name=accommodation.name, description=accommodation.description, address=accommodation.address)

def create_accommodation_impl(db, accommodation_create: AccommodationCreate):
    accommodation = accommodation_from_create(accommodation_create)
    db.add(accommodation)
    db.commit()
    return read_from_accommodation(accommodation)

def get_accommodation_impl(db, accommodation_id: int):
    accommodation = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    return read_from_accommodation(accommodation)

def get_accommodations_impl(db):
    accommodations = db.query(Accommodation).all()
    return [read_from_accommodation(accommodation) for accommodation in accommodations]

def update_accommodation_impl(db, accommodation_id: int, accommodation_update: AccommodationCreate):
    accommodation = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    accommodation.name = accommodation_update.name
    accommodation.description = accommodation_update.description
    accommodation.address = accommodation_update.address
    db.commit()
    return read_from_accommodation(accommodation)

def delete_accommodation_impl(db, accommodation_id: int):
    accommodation = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    db.delete(accommodation)
    db.commit()
    return read_from_accommodation(accommodation)

# ------------------------------------------------
# Asset
# ------------------------------------------------

class AssetCreate(BaseModel):
    name: str
    description: str
    asset_type: str
    state: int
    tags: str
    accomodation_id: int

class AssetRead(BaseModel):
    id: int
    name: str
    description: str
    asset_type: str
    state: int
    tags: str
    accomodation_id: int

def asset_from_create(create: AssetCreate):
    return Asset(name=create.name, description=create.description, asset_type=create.asset_type, state=create.state, tags=create.tags, accomodation_id=create.accomodation_id)

def read_from_asset(asset: Asset):
    return AssetRead(id=asset.id, name=asset.name, description=asset.description, asset_type=asset.asset_type, state=asset.state, tags=asset.tags, accomodation_id=asset.accomodation_id)

def create_asset_impl(db, asset_create: AssetCreate):
    asset = asset_from_create(asset_create)
    db.add(asset)
    db.commit()
    return read_from_asset(asset)

def get_asset_impl(db, asset_id: int):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    return read_from_asset(asset)

def get_assets_impl(db, asset_type: str = None, tag: str = None):
    query = db.query(Asset)
    if asset_type is not None:
        query = query.filter(Asset.asset_type == asset_type)
    if tag is not None:
        query = query.filter(Asset.tags.like(f"%{tag}%"))
    
    assets = query.all()
    return [read_from_asset(asset) for asset in assets]

def update_asset_impl(db, asset_id: int, asset_update: AssetCreate):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    asset.name = asset_update.name
    asset.description = asset_update.description
    asset.asset_type = asset_update.asset_type
    asset.state = asset_update.state
    asset.tags = asset_update.tags
    asset.accomodation_id = asset_update.accomodation_id
    db.commit()
    return read_from_asset(asset)

def delete_asset_impl(db, asset_id: int):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    db.delete(asset)
    db.commit()
    return read_from_asset(asset)

