# -*- coding: utf-8 -*-
# @file project.py
# @brief The Project Model
# @author sailing-innocent
# @date 2025-01-30
# @version 1.0
# ---------------------------------

from pydantic import BaseModel
from internal.data.project import Project, Mission, TimeSpan, ProjectState, Event
from internal.data.orm import TIME_START, TIME_END 
import time
import logging
from datetime import datetime 
# from typing import Union, List

def clean_all_impl(db):
    db.query(Mission).delete()
    db.query(Project).delete()
    db.query(Event).delete()
    db.query(TimeSpan).delete()
    db.commit()


# ------------------------------------------------
# TimeSpan
# ------------------------------------------------


class TimeSpanCreate(BaseModel):
    start: int
    end: int


class TimeSpanRead(BaseModel):
    id: int
    start: int
    end: int


def time_span_from_create(create: TimeSpanCreate):
    return TimeSpan(start=create.start, end=create.end)


def read_from_time_span(time_span: TimeSpan):
    return TimeSpanRead(id=time_span.id, start=time_span.start, end=time_span.end)


def create_timespan_impl(db, timespan_create: TimeSpanCreate):
    timespan = time_span_from_create(timespan_create)
    db.add(timespan)
    db.commit()
    return read_from_time_span(timespan)


def get_timespan_impl(db, timespan_id: int):
    timespan = db.query(TimeSpan).filter(TimeSpan.id == timespan_id).first()
    return read_from_time_span(timespan)


def get_timespans_from_time_to_time_impl(db, start: int, end: int):
    timespans = (
        db.query(TimeSpan).filter(TimeSpan.start >= start, TimeSpan.end <= end).all()
    )
    if len(timespans) > 0:
        return [read_from_time_span(timespan) for timespan in timespans]
    return None


# ------------------------------------------------
# Project
# ------------------------------------------------


class ProjectCreate(BaseModel):
    parent_id: int
    name: str
    time_required: int
    ddl: int


class ProjectRead(BaseModel):
    id: int
    parent_id: int
    name: str
    description: str
    raw_tags: str
    tags: str
    weight: int
    time_required: int
    children: list  # list[int] or list[ProjectRead]
    state: int
    ddl: int


# not changing parent and children
class ProjectUpdate(BaseModel):
    parent_id: int
    name: str
    description: str = ""
    raw_tags: str = ""
    tags: str = ""
    weight: int = 100
    time_required: int
    ddl: int


def project_from_create(create: ProjectCreate):
    init_state = ProjectState(0)
    init_state.set_valid()
    return Project(
        parent_id=create.parent_id,
        name=create.name,
        description="",
        raw_tags="",
        tags="",
        weight=100,
        time_required=create.time_required,
        state=init_state.value,
        ddl=create.ddl,
    )


def read_from_project_shallow(db, project: Project):
    children = db.query(Project).filter(Project.parent_id == project.id).all()
    if len(children) == 0:
        children = []
    else:
        children = [child.id for child in children]
    return ProjectRead(
        id=project.id,
        parent_id=project.parent_id,
        name=project.name,
        description=project.description,
        raw_tags=project.raw_tags,
        tags=project.tags,
        weight=project.weight,
        time_required=project.time_required,
        children=children,
        state=project.state,
        ddl=project.ddl,
    )


def read_from_project(project: Project, children=[]):
    return ProjectRead(
        id=project.id,
        parent_id=project.parent_id,
        name=project.name,
        description=project.description,
        raw_tags=project.raw_tags,
        tags=project.tags,
        weight=project.weight,
        time_required=project.time_required,
        children=children,
        state=project.state,
        ddl=project.ddl,
    )


def create_project_impl(db, project_create: ProjectCreate):
    project = project_from_create(project_create)
    db.add(project)
    db.commit()
    return read_from_project(project)


def get_project_impl(db, project_id: int, recursive: bool):
    project = db.query(Project).filter(Project.id == project_id).first()
    children = db.query(Project).filter(Project.parent_id == project_id).all()

    if len(children) == 0:
        children = []
    else:
        if recursive:
            children = [get_project_impl(db, child.id, recursive) for child in children]
        else:
            children = [child.id for child in children]
    return read_from_project(project, children)


def get_projects_impl(db):
    projects = db.query(Project).all()

    return [read_from_project_shallow(db, project) for project in projects]


def delete_project_impl(db, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        return None
    db.delete(project)
    db.commit()
    return read_from_project(project)


def update_project_impl(db, project_id: int, project_update: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        return None
    project.parent_id = project_update.parent_id
    project.name = project_update.name
    project.description = project_update.description
    project.raw_tags = project_update.raw_tags
    project.tags = project_update.tags
    project.weight = project_update.weight
    project.time_required = project_update.time_required
    project.ddl = project_update.ddl
    db.commit()
    return read_from_project_shallow(db, project)


# ------------------------------------------------
# Mission
# ------------------------------------------------


class MissionCreate(BaseModel):
    project_id: int
    time_span_id: int
    weight: int
    time_required: int
    state: int


class MissionRead(BaseModel):
    id: int
    project_id: int
    time_span_id: int
    weight: int
    time_required: int
    state: int


def mission_from_create(create: MissionCreate):
    return Mission(
        project_id=create.project_id,
        time_span_id=create.time_span_id,
        weight=create.weight,
        time_required=create.time_required,
        state=create.state,
    )


def read_from_mission(mission: Mission):
    return MissionRead(
        id=mission.id,
        project_id=mission.project_id,
        time_span_id=mission.time_span_id,
        weight=mission.weight,
        time_required=mission.time_required,
        state=mission.state,
    )


def create_mission_impl(db, mission_create: MissionCreate):
    mission = mission_from_create(mission_create)
    db.add(mission)
    db.commit()
    return read_from_mission(mission)


def get_mission_impl(db, mission_id: int):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    return read_from_mission(mission)

# ------------------------------------------------
# Event 
# ------------------------------------------------

class EventCreate(BaseModel):
    start: int
    end: int 
    description: str
    tags: str 

    def __str__(self):
        start_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start))
        end_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end))
        return f"EventCreate(start={start_t}, end={end_t}, description={self.description}, tags={self.tags})"


class EventRead(BaseModel):
    id: int
    start: int
    end: int
    description: str
    tags: str

def event_from_create(create: EventCreate):
    return Event(
        start=create.start,
        end=create.end,
        description=create.description,
        tags=create.tags,
    )

def read_from_event(event: Event):
    return EventRead(
        id=event.id,
        start=event.start, 
        end=event.end,
        description=event.description,
        tags=event.tags,
    )


def create_event_impl(db, event_create: EventCreate):
    event = event_from_create(event_create)
    db.add(event)
    db.commit()
    return read_from_event(event)

def get_event_impl(db, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    return read_from_event(event)

def get_events_impl(db, start: int = -1, end: int = -1, tags_like: str = ""):
    query = db.query(Event)
    if start != -1:
        query = query.filter(Event.start >= start)
    if end != -1:
        query = query.filter(Event.end <= end)
    if tags_like != "":
        tags = f"%{tags_like}%"
        query = query.filter(Event.tags.like(tags))
    events = query.all()
    if len(events) > 0:
        return [read_from_event(event) for event in events]
    return None

def delete_event_impl(db, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        return None
    db.delete(event)
    db.commit()
    return read_from_event(event)

def update_event_impl(db, event_id: int, event_update: EventCreate):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        return None
    event.start = event_update.start
    event.end = event_update.end
    event.description = event_update.description
    event.tags = event_update.tags
    db.commit()
    return read_from_event(event)

# ------------------------------------------------