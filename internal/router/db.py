# -*- coding: utf-8 -*-
# @file db.py
# @brief The Database Connection deps router
# @author sailing-innocent
# @date 2025-05-20
# @version 1.0
# ---------------------------------

from litestar import Router
from litestar.di import Provide
from internal.controller.health import WeightController, WeightRecordController
from internal.db import g_db_func


# 修改为创建一个函数来生成依赖而不是直接用Provide包装g_db_func
async def get_db_dependency():
    # 返回函数调用，而不是函数对象本身
    return g_db_func()


router = Router(
    path="/health",
    dependencies={"router_dependency": Provide(get_db_dependency)},
    route_handlers=[
        WeightController,
        WeightRecordController,
    ],
)
