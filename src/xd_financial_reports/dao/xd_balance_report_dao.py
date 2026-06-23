"""
心动公司现金及合约负债表 DAO

表: xd_balance_report
"""
from typing import Optional

from .base_dao import BaseDAO


class XdBalanceReportDAO(BaseDAO):
    """xd_balance_report 表数据访问对象"""

    table_name = "xd_balance_report"
    pk_field = "id"
    columns = [
        "id", "report_year", "period",
        "cash_and_cash_equivalents", "contract_liabilities", "total_liabilities",
        "created_at", "updated_at",
    ]

    # ============================================================
    # 业务查询方法
    # ============================================================

    def get_by_year_period(self, report_year: int, period: str) -> Optional[dict]:
        """根据财年和期间查询唯一记录"""
        row = self.get_one_by_condition(
            "report_year = ? AND period = ?",
            (report_year, period)
        )
        return self.row_to_dict(row)

    def get_by_year(self, report_year: int, order_by: str = "period") -> list[dict]:
        """查询指定财年的所有记录"""
        rows = self.get_by_condition(
            "report_year = ?", (report_year,), order_by=order_by
        )
        return self.rows_to_dicts(rows)

    def get_by_period(self, period: str, order_by: str = "report_year") -> list[dict]:
        """查询指定期间的所有记录"""
        rows = self.get_by_condition(
            "period = ?", (period,), order_by=order_by
        )
        return self.rows_to_dicts(rows)

    def upsert(self, report_year: int, period: str, **kwargs) -> int:
        """根据 year+period 唯一键插入或更新记录"""
        kwargs["report_year"] = report_year
        kwargs["period"] = period
        return self.insert_or_replace(**kwargs)