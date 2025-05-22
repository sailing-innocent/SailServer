# -*- coding: utf-8 -*-
# @file necessity.py
# @brief The Necessity Model
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.info import Accommodation, Asset, ClothState, ServiceAccount


def clean_all_impl(db):
    db.query(Asset).delete()
    db.query(Accommodation).delete()
    db.query(ServiceAccount).delete()
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
    return Accommodation(
        name=create.name, description=create.description, address=create.address
    )


def read_from_accommodation(accommodation: Accommodation):
    return AccommodationRead(
        id=accommodation.id,
        name=accommodation.name,
        description=accommodation.description,
        address=accommodation.address,
    )


def create_accommodation_impl(db, accommodation_create: AccommodationCreate):
    accommodation = accommodation_from_create(accommodation_create)
    db.add(accommodation)
    db.commit()
    return read_from_accommodation(accommodation)


def get_accommodation_impl(db, accommodation_id: int):
    accommodation = (
        db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    )
    return read_from_accommodation(accommodation)


def get_accommodations_impl(db):
    accommodations = db.query(Accommodation).all()
    return [read_from_accommodation(accommodation) for accommodation in accommodations]


def update_accommodation_impl(
    db, accommodation_id: int, accommodation_update: AccommodationCreate
):
    accommodation = (
        db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    )
    accommodation.name = accommodation_update.name
    accommodation.description = accommodation_update.description
    accommodation.address = accommodation_update.address
    db.commit()
    return read_from_accommodation(accommodation)


def delete_accommodation_impl(db, accommodation_id: int):
    accommodation = (
        db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    )
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
    return Asset(
        name=create.name,
        description=create.description,
        asset_type=create.asset_type,
        state=create.state,
        tags=create.tags,
        accomodation_id=create.accomodation_id,
    )


def read_from_asset(asset: Asset):
    return AssetRead(
        id=asset.id,
        name=asset.name,
        description=asset.description,
        asset_type=asset.asset_type,
        state=asset.state,
        tags=asset.tags,
        accomodation_id=asset.accomodation_id,
    )


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


# ------------------------------------------------
# Service Account
# ------------------------------------------------


class ServiceAccountCreate(BaseModel):
    name: str
    entry: str
    username: str
    password: str
    desp: str
    expire_time: int


class ServiceAccountRead(BaseModel):
    id: int
    name: str
    entry: str
    username: str
    password: str
    desp: str
    expire_time: int


def service_account_from_create(create: ServiceAccountCreate):
    return ServiceAccount(
        name=create.name,
        entry=create.entry,
        username=create.username,
        password=create.password,
        desp=create.desp,
        expire_time=create.expire_time,
    )


def read_from_service_account(service_account: ServiceAccount):
    return ServiceAccountRead(
        id=service_account.id,
        name=service_account.name,
        entry=service_account.entry,
        username=service_account.username,
        password=service_account.password,
        desp=service_account.desp,
        expire_time=service_account.expire_time,
    )


def create_service_account_impl(db, service_account_create: ServiceAccountCreate):
    service_account = service_account_from_create(service_account_create)
    db.add(service_account)
    db.commit()
    return read_from_service_account(service_account)


def get_service_account_impl(db, service_account_id: int):
    service_account = (
        db.query(ServiceAccount).filter(ServiceAccount.id == service_account_id).first()
    )
    return read_from_service_account(service_account)


def query_service_account_by_name_impl(db, name: str):
    service_account = (
        db.query(ServiceAccount).filter(ServiceAccount.name == name).first()
    )
    return read_from_service_account(service_account)


def get_service_accounts_impl(db, skip: int = 0, limit: int = -1):
    query = db.query(ServiceAccount)
    if skip > 0:
        query = query.offset(skip)
    if limit > 0:
        query = query.limit(limit)

    service_accounts = query.all()
    return [
        read_from_service_account(service_account)
        for service_account in service_accounts
    ]


def update_service_account_impl(
    db, service_account_id: int, service_account_update: ServiceAccountCreate
):
    service_account = (
        db.query(ServiceAccount).filter(ServiceAccount.id == service_account_id).first()
    )
    service_account.name = service_account_update.name
    service_account.entry = service_account_update.entry
    service_account.username = service_account_update.username
    service_account.password = service_account_update.password
    service_account.desp = service_account_update.desp
    service_account.expire_time = service_account_update.expire_time
    db.commit()
    return read_from_service_account(service_account)


def delete_service_account_impl(db, service_account_id: int):
    service_account = (
        db.query(ServiceAccount).filter(ServiceAccount.id == service_account_id).first()
    )
    db.delete(service_account)
    db.commit()
    return read_from_service_account(service_account)
