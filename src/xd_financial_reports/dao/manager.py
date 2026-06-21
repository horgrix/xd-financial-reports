"""
DAO 管理器

提供所有 DAO 的单例访问入口，方便统一管理和使用。
"""
import threading
from typing import Optional

from ..db.connection import ConnectionPool, get_pool
from .base_dao import BaseDAO
from .xd_revenue_report_dao import XdRevenueReportDAO
from .xd_revenue_game_report_dao import XdRevenueGameReportDAO
from .xd_balance_report_dao import XdBalanceReportDAO
from .xd_core_financial_report_dao import XdCoreFinancialReportDAO
from .xd_core_operational_report_dao import XdCoreOperationalReportDAO
from .xd_expense_report_dao import XdExpenseReportDAO


class DAOManager:
    """
    DAO 管理器，集中管理所有 DAO 实例

    使用方式:
        manager = DAOManager(pool)
        data = manager.revenue_report.get_by_year(2025)
    """

    def __init__(self, pool: Optional[ConnectionPool] = None):
        """
        初始化 DAO 管理器

        Args:
            pool: 连接池实例，如不提供则使用全局连接池
        """
        self._pool = pool or get_pool()
        self._revenue_report: Optional[XdRevenueReportDAO] = None
        self._revenue_game_report: Optional[XdRevenueGameReportDAO] = None
        self._balance_report: Optional[XdBalanceReportDAO] = None
        self._core_financial_report: Optional[XdCoreFinancialReportDAO] = None
        self._core_operational_report: Optional[XdCoreOperationalReportDAO] = None
        self._expense_report: Optional[XdExpenseReportDAO] = None

    @property
    def revenue_report(self) -> XdRevenueReportDAO:
        """分业务收入成本毛利表 DAO"""
        if self._revenue_report is None:
            self._revenue_report = XdRevenueReportDAO(self._pool)
        return self._revenue_report

    @property
    def revenue_game_report(self) -> XdRevenueGameReportDAO:
        """游戏收入构成细分表 DAO"""
        if self._revenue_game_report is None:
            self._revenue_game_report = XdRevenueGameReportDAO(self._pool)
        return self._revenue_game_report

    @property
    def balance_report(self) -> XdBalanceReportDAO:
        """现金及合约负债表 DAO"""
        if self._balance_report is None:
            self._balance_report = XdBalanceReportDAO(self._pool)
        return self._balance_report

    @property
    def core_financial_report(self) -> XdCoreFinancialReportDAO:
        """核心财务指标表 DAO"""
        if self._core_financial_report is None:
            self._core_financial_report = XdCoreFinancialReportDAO(self._pool)
        return self._core_financial_report

    @property
    def core_operational_report(self) -> XdCoreOperationalReportDAO:
        """运营指标表 DAO"""
        if self._core_operational_report is None:
            self._core_operational_report = XdCoreOperationalReportDAO(self._pool)
        return self._core_operational_report

    @property
    def expense_report(self) -> XdExpenseReportDAO:
        """三大费用及占比表 DAO"""
        if self._expense_report is None:
            self._expense_report = XdExpenseReportDAO(self._pool)
        return self._expense_report

    def get_all_daos(self) -> dict[str, BaseDAO]:
        """获取所有 DAO 实例的字典"""
        return {
            "revenue_report": self.revenue_report,
            "revenue_game_report": self.revenue_game_report,
            "balance_report": self.balance_report,
            "core_financial_report": self.core_financial_report,
            "core_operational_report": self.core_operational_report,
            "expense_report": self.expense_report,
        }


# 全局 DAOManager 单例
_dao_manager: Optional[DAOManager] = None
_dao_manager_lock = threading.Lock()


def get_dao_manager(pool: Optional[ConnectionPool] = None) -> DAOManager:
    """
    获取全局 DAOManager 单例

    Args:
        pool: 连接池实例

    Returns:
        DAOManager: 全局单例
    """
    global _dao_manager
    if _dao_manager is None:
        with _dao_manager_lock:
            if _dao_manager is None:
                _dao_manager = DAOManager(pool)
    return _dao_manager


def reset_dao_manager():
    """重置全局 DAOManager 单例（主要用于测试）"""
    global _dao_manager
    _dao_manager = None