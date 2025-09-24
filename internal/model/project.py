# -*- coding: utf-8 -*-
# @file necessity.py
# @brief The Necessity Model
# @author sailing-innocent
# @date 2025-02-03
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.life import (
    ProjectState,
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
        name=create.name,
        description=create.description,
    )



def read_from_project(project: Project):
    return ProjectData(
        id=project.id,
        name=project.name,
        description=project.description,
        state=ProjectState(project.state),
        ctime=project.ctime,
        mtime=project.mtime,
        ddl=project.ddl,
        extra=project.extra,
    )


def create_project_impl(db, project_create: ProjectData):
    project = project_from_create(project_create)
    db.add(project)
    db.commit()
    db.refresh(project)
    return read_from_project(project)

def change_project_state_impl(db, project_id: int, change_func: callable):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    new_state = ProjectState(project.state)
    change_func(new_state)

    project.state = new_state.get_state()
    db.commit()
    db.refresh(project)
    return read_from_project(project)

def valid_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.valid())

def prepare_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.prepare())

def tracking_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.tracking())

def pending_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.pending())

def restore_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.restore())

def done_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.done())

def cancel_project_impl(db, project_id: int):
    return change_project_state_impl(db, project_id, lambda state: state.cancel())

def get_project_impl(db, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    return read_from_project(project)


def get_projects_impl(db, skip: int = 0, limit: int = -1):
    query = db.query(Project)
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
    project.ddl = project_update.ddl if project_update.ddl else project.ddl
    project.mtime = datetime.now()
    project.extra = project_update.extra

    db.commit()
    db.refresh(project)
    return read_from_project(project)


def delete_project_impl(db, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None

    db.delete(project)
    db.commit()
    return read_from_project(project)


