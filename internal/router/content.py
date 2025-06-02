# -*- coding: utf-8 -*-
# @file content.py
# @brief Content Router
# @author sailing-innocent
# @date 2025-06-02
# @version 1.0
# ---------------------------------


from litestar import Router
from litestar.di import Provide
from internal.controller.content import ContentController
from internal.db import get_db_dependency

router = Router(
    path="/content",
    dependencies={"router_dependency": Provide(get_db_dependency)},
    route_handlers=[
        ContentController,
    ],
)
