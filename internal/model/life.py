# -*- coding: utf-8 -*-
# @file necessity.py
# @brief The Necessity Model
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.life import (
    ServiceAccount,
    Project,
    ProjectData,
)
from datetime import datetime


def clean_all_impl(db):
    db.query(Project).delete()
    db.commit()


# ------------------------------------------------
# Project Management
# ------------------------------------------------


def project_from_create(create: ProjectData):
    return Project(
        parent_id=create.parent_id,
        name=create.name,
        description=create.description,
        raw_tags=create.raw_tags,
        tags=create.tags,
        state=create.state,
        weight=create.weight,
        extra=create.extra,
        ddl=create.ddl if create.ddl else datetime.now(),
    )


def read_from_project(project: Project):
    return ProjectData(
        id=project.id,
        parent_id=project.parent_id,
        name=project.name,
        description=project.description,
        raw_tags=project.raw_tags,
        tags=project.tags,
        state=project.state,
        ctime=project.ctime,
        mtime=project.mtime,
        ddl=project.ddl,
        weight=project.weight,
        extra=project.extra,
    )


def create_project_impl(db, project_create: ProjectData):
    project = project_from_create(project_create)
    db.add(project)
    db.commit()
    db.refresh(project)
    return read_from_project(project)


def get_project_impl(db, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    return read_from_project(project)


def get_projects_impl(db, skip: int = 0, limit: int = -1, parent_id: int = None):
    query = db.query(Project)

    if parent_id is not None:
        if parent_id == 0:  # Special case for root projects
            query = query.filter(Project.parent_id.is_(None))
        else:
            query = query.filter(Project.parent_id == parent_id)

    # Order by weight (high to low) and then by name
    query = query.order_by(Project.weight.desc(), Project.name)

    if skip > 0:
        query = query.offset(skip)
    if limit > 0:
        query = query.limit(limit)

    projects = query.all()
    return [read_from_project(project) for project in projects]


def update_project_impl(db, project_id: int, project_update: ProjectData):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None

    project.name = project_update.name
    project.description = project_update.description
    project.raw_tags = project_update.raw_tags
    project.tags = project_update.tags
    project.state = project_update.state
    project.weight = project_update.weight
    project.extra = project_update.extra
    project.ddl = project_update.ddl if project_update.ddl else project.ddl
    project.mtime = datetime.now()
    project.parent_id = project_update.parent_id

    db.commit()
    db.refresh(project)
    return read_from_project(project)


def delete_project_impl(db, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None

    # Find and delete all child projects first
    children = db.query(Project).filter(Project.parent_id == project_id).all()
    for child in children:
        delete_project_impl(db, child.id)

    db.delete(project)
    db.commit()
    return read_from_project(project)


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
