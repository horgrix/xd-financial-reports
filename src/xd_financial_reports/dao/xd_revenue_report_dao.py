"""
心动公司分业务收入/成本/毛利/毛利率表 DAO

表: xd_revenue_report
"""
from typing import Optional, Any

from .base_dao import BaseDAO


class XdRevenueReportDAO(BaseDAO):
    """xd_revenue_report 表数据访问对象"""

    table_name = "xd_revenue_report"
    pk_field = "id"
    columns = [
        "id", "report_year", "period",
        "game_revenue", "game_cost", "game_gross_profit", "game_gross_profit_margin",
        "taptap_platform_revenue", "taptap_platform_cost",
        "taptap_platform_gross_profit", "taptap_platform_gross_profit_margin",
        "created_at", "updated_at",
    ]

    # ============================================================
    # 业务查询方法
    # ============================================================

    def get_by_year_period(self, report_year: int, period: str) -> Optional[dict]:
        """
        根据财年和期间查询唯一记录

        Args:
            report_year: 财年
            period: 期间 (H1/H2/FY)

        Returns:
            记录字典或 None
        """
        row = self.get_one_by_condition(
            "report_year = ? AND period = ?",
            (report_year, period)
        )
        return self.row_to_dict(row)

    def get_by_year(self, report_year: int, order_by: str = "period") -> list[dict]:
        """
        查询指定财年的所有记录

        Args:
            report_year: 财年
            order_by: 排序字段

        Returns:
            记录字典列表
        """
        rows = self.get_by_condition(
            "report_year = ?", (report_year,), order_by=order_by
        )
        return self.rows_to_dicts(rows)

    def get_by_period(self, period: str, order_by: str = "report_year") -> list[dict]:
        """
        查询指定期间的所有记录

        Args:
            period: 期间 (H1/H2/FY)
            order_by: 排序字段

        Returns:
            记录字典列表
        """
        rows = self.get_by_condition(
            "period = ?", (period,), order_by=order_by
        )
        return self.rows_to_dicts(rows)

    def upsert(self, report_year: int, period: str, **kwargs) -> int:
        """
        根据 year+period 唯一键插入或更新记录

        Args:
            report_year: 财年
            period: 期间
            **kwargs: 其他字段值

        Returns:
            记录的 id
        """
        kwargs["report_year"] = report_year
        kwargs["period"] = period
        return self.insert_or_replace(**kwargs)