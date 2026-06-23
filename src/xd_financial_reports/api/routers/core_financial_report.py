"""核心财务指标表 API 路由."""
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from xd_financial_reports.dao import get_dao_manager

VALID_PERIODS = {"H1", "H2", "FY"}

router = APIRouter(tags=["core-financial-report"])


@router.get("/core-financial-report", summary="按时间范围查询核心财务指标数据")
async def query_core_financial_report(
    start_year: int = Query(..., ge=2021, le=2030, description="起始财年"),
    end_year: int = Query(..., ge=2021, le=2030, description="截止财年"),
    period: Optional[List[str]] = Query(None, description="期间: H1/H2/FY，支持多值，如 period=H1&period=FY"),
):
    """查询指定财年范围内的核心财务指标（收入、毛利、溢利等）。"""
    if start_year > end_year:
        raise HTTPException(400, "start_year must be <= end_year")

    mgr = get_dao_manager()
    dao = mgr.core_financial_report

    where = "report_year >= ? AND report_year <= ?"
    params: list = [start_year, end_year]

    if period:
        # 校验每个 period 值是否合法
        invalid = [p for p in period if p not in VALID_PERIODS]
        if invalid:
            raise HTTPException(400, f"Invalid period value(s): {invalid}. Must be one of H1, H2, FY")

        placeholders = ", ".join(["?" for _ in period])
        where += f" AND period IN ({placeholders})"
        params.extend(period)

    rows = dao.get_by_condition(where, tuple(params), order_by="report_year, period")
    return dao.rows_to_dicts(rows)


@router.get("/core-financial-report/years", summary="查询所有可用的财年列表")
async def get_report_years():
    """返回 xd_core_financial_report 表中所有不重复的 report_year，按升序排列。"""
    mgr = get_dao_manager()
    dao = mgr.core_financial_report
    years = dao.get_distinct_years()
    return {"years": years}

