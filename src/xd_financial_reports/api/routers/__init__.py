"""API 路由模块集合."""

from .revenue_report import router as revenue_report_router
from .revenue_game_report import router as revenue_game_report_router
from .balance_report import router as balance_report_router
from .core_financial_report import router as core_financial_report_router
from .core_operational_report import router as core_operational_report_router
from .expense_report import router as expense_report_router

__all__ = [
    "revenue_report_router",
    "revenue_game_report_router",
    "balance_report_router",
    "core_financial_report_router",
    "core_operational_report_router",
    "expense_report_router",
]