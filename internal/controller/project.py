# -*- coding: utf-8 -*-
# @file life.py
# @brief Life Controller
# @author sailing-innocent
# @date 2025-08-24
# @version 1.0
# ---------------------------------
from __future__ import annotations
from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig
from litestar import Controller, delete, get, post, put, Request, Response
from litestar.exceptions import NotFoundException

from internal.data.life import ProjectData
from internal.model.project import (
    create_project_impl,
    get_project_impl,
    get_projects_impl,
    update_project_impl,
    delete_project_impl,
)
from sqlalchemy.orm import Session
from typing import Generator, List, Optional


class ProjectDataWriteDTO(DataclassDTO[ProjectData]):
    config = DTOConfig(exclude={"id", "ctime", "mtime", "parent_id", "state", "extra"})

class ProjectDataUpdateDTO(DataclassDTO[ProjectData]):
    config = DTOConfig(exclude={"id", "ctime", "mtime", "parent_id", "state", "extra"})

class ProjectDataReadDTO(DataclassDTO[ProjectData]):
    config = DTOConfig(exclude={"ctime"})

class ProjectController(Controller):
    dto = ProjectDataWriteDTO
    return_dto = ProjectDataReadDTO
    path = "/project"

    @get("/")
    async def get_projects(
        self,
        router_dependency: Generator[Session, None, None],
        request: Request,
        skip: int = 0,
        limit: int = -1,
        parent_id: Optional[int] = None,
    ) -> List[ProjectData]:
        db = next(router_dependency)
        projects = get_projects_impl(db, skip, limit, parent_id)
        request.logger.info(f"Get projects: {len(projects)}")
        return projects

    @get("/{project_id:int}")
    async def get_project(
        self,
        project_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ProjectData:
        """
        Get a project by its ID.
        """
        db = next(router_dependency)
        project = get_project_impl(db, project_id)
        request.logger.info(f"Get project {project_id}: {project}")
        if not project:
            raise NotFoundException(detail=f"Project with ID {project_id} not found")
        return project

    @post("/")
    async def create_project(
        self,
        data: ProjectData,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ProjectData:
        """
        Create a new project.
        """
        db = next(router_dependency)
        project = create_project_impl(db, data)
        request.logger.info(f"Created project: {project.name}")
        return project

    @put("/{project_id:int}")
    async def update_project(
        self,
        project_id: int,
        data: ProjectData,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ProjectData:
        """
        Update a project by its ID.
        """
        db = next(router_dependency)
        project = update_project_impl(db, project_id, data)
        request.logger.info(f"Updated project {project_id}: {project}")
        if not project:
            raise NotFoundException(detail=f"Project with ID {project_id} not found")
        return project

    @delete("/{project_id:int}", status_code=200)
    async def delete_project(
        self,
        project_id: int,
        router_dependency: Generator[Session, None, None],
        request: Request,
    ) -> ProjectData:
        """
        Delete a project by its ID.
        """
        db = next(router_dependency)
        project = delete_project_impl(db, project_id)
        request.logger.info(f"Deleted project {project_id}")
        if not project:
            raise NotFoundException(detail=f"Project with ID {project_id} not found")
        return project
