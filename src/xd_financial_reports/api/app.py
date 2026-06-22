"""FastAPI 应用入口

创建并配置 FastAPI 应用，注册各报表路由。
"""
import sys
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

# 确保 src 目录在 sys.path 中
_src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from xd_financial_reports.db import init_database, get_pool
from xd_financial_reports.dao import get_dao_manager, DAOManager
from .routers import (
    revenue_report_router,
    revenue_game_report_router,
    balance_report_router,
    core_financial_report_router,
    core_operational_report_router,
    expense_report_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期：启动时初始化数据库，关闭时释放连接池。"""
    pool = init_database()
    get_dao_manager(pool)
    yield
    get_pool().close_all()


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用。"""
    app = FastAPI(
        title="XD Financial Reports API",
        description="心动公司 (XD Inc.) 2021-2025 财务数据分析接口",
        version="0.1.0",
        lifespan=lifespan,
    )

    prefix = "/api/v2/financial/xd"

    app.include_router(revenue_report_router, prefix=prefix)
    app.include_router(revenue_game_report_router, prefix=prefix)
    app.include_router(balance_report_router, prefix=prefix)
    app.include_router(core_financial_report_router, prefix=prefix)
    app.include_router(core_operational_report_router, prefix=prefix)
    app.include_router(expense_report_router, prefix=prefix)

    @app.get("/api/v2/financial/health")
    async def health():
        return {"status": "ok"}

    return app


# 全局 app 实例，供 uvicorn 直接引用
app = create_app()