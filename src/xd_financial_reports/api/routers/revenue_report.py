"""分业务收入/成本/毛利/毛利率表 API 路由."""
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from xd_financial_reports.dao import get_dao_manager

router = APIRouter(tags=["revenue-report"])


@router.get("/revenue-report", summary="按时间范围查询分业务收入数据")
async def query_revenue_report(
    start_year: int = Query(..., ge=2021, le=2030, description="起始财年"),
    end_year: int = Query(..., ge=2021, le=2030, description="截止财年"),
    period: Optional[str] = Query(None, pattern="^(H1|H2|FY)$", description="期间: H1/H2/FY"),
):
    """查询指定财年范围内的分业务收入/成本/毛利数据。"""
    if start_year > end_year:
        raise HTTPException(400, "start_year must be <= end_year")

    mgr = get_dao_manager()
    dao = mgr.revenue_report

    where = "report_year >= ? AND report_year <= ?"
    params = [start_year, end_year]

    if period:
        where += " AND period = ?"
        params.append(period)

    rows = dao.get_by_condition(where, tuple(params), order_by="report_year, period")
    return dao.rows_to_dicts(rows)