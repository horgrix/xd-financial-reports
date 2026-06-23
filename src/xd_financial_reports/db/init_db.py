"""
数据库初始化模块

负责创建所有表结构并导入初始数据。
根据 src/xd_financial_datas/ 下的 SQL 文件生成 SQLite 兼容的建表语句。
"""
import sqlite3
import threading
from pathlib import Path
from typing import Optional

from .connection import get_pool, ConnectionPool

# 数据库文件路径
DEFAULT_DB_PATH = Path(__file__).parent.parent.parent.parent / "xd_financial_1.1.db"

_init_lock = threading.Lock()
_initialized = False

# ============================================================
# SQLite 建表语句 (从 MySQL DDL 转换而来)
# ============================================================

CREATE_TABLES_SQL = """
-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 分业务收入/成本/毛利/毛利率表
-- ============================================================
CREATE TABLE IF NOT EXISTS xd_revenue_report (
    id                              INTEGER PRIMARY KEY AUTOINCREMENT,
    report_year                     INTEGER     NOT NULL,
    period                          TEXT        NOT NULL,
    period_index                    INT         NOT NULL,
    game_revenue                    INTEGER     NOT NULL,
    game_cost                       INTEGER     NOT NULL,
    game_gross_profit               INTEGER     NOT NULL,
    game_gross_profit_margin        REAL,
    taptap_platform_revenue         INTEGER     NOT NULL,
    taptap_platform_cost            INTEGER     NOT NULL,
    taptap_platform_gross_profit    INTEGER     NOT NULL,
    taptap_platform_gross_profit_margin REAL,
    created_at                      TEXT        DEFAULT (datetime('now','localtime')),
    updated_at                      TEXT        DEFAULT (datetime('now','localtime')),
    UNIQUE (report_year, period)
);

-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 游戏收入构成细分表
-- ============================================================
CREATE TABLE IF NOT EXISTS xd_revenue_game_report (
    id                              INTEGER PRIMARY KEY AUTOINCREMENT,
    report_year                     INTEGER     NOT NULL,
    period                          TEXT        NOT NULL,
    period_index                    INT         NOT NULL,
    game_operation_revenue          INTEGER     NOT NULL,
    online_game_revenue             INTEGER     NOT NULL,
    paid_game_revenue               INTEGER     NOT NULL,
    gross_basis_revenue             INTEGER     NOT NULL,
    net_basis_revenue               INTEGER     NOT NULL,
    other_game_revenue              INTEGER     NOT NULL,
    created_at                      TEXT        DEFAULT (datetime('now','localtime')),
    updated_at                      TEXT        DEFAULT (datetime('now','localtime')),
    UNIQUE (report_year, period)
);

-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 现金及合约负债表
-- ============================================================
CREATE TABLE IF NOT EXISTS xd_balance_report (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    report_year                 INTEGER     NOT NULL,
    period                      TEXT        NOT NULL,
    period_index                INT         NOT NULL,
    cash_and_cash_equivalents   INTEGER     NOT NULL,
    contract_liabilities        INTEGER     NOT NULL,
    total_liabilities           BIGINT      NOT NULL,
    created_at                  TEXT        DEFAULT (datetime('now','localtime')),
    updated_at                  TEXT        DEFAULT (datetime('now','localtime')),
    UNIQUE (report_year, period)
);

-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 核心财务指标表
-- ============================================================
CREATE TABLE IF NOT EXISTS xd_core_financial_report (
    id                                      INTEGER PRIMARY KEY AUTOINCREMENT,
    report_year                             INTEGER     NOT NULL,
    period                                  TEXT        NOT NULL,
    period_index                            INT         NOT NULL,
    revenue                                 INTEGER     NOT NULL,
    gross_profit                            INTEGER     NOT NULL,
    gross_profit_margin                     REAL,
    profit_for_year                         INTEGER     NOT NULL,
    profit_for_year_margin                  REAL,
    profit_attr_to_shareholders             INTEGER     NOT NULL,
    profit_attr_to_shareholders_margin      REAL,
    adjusted_profit_for_year                INTEGER     NOT NULL,
    adjusted_profit_for_year_margin         REAL,
    adjusted_profit_attr_to_shareholders         INTEGER     NOT NULL,
    adjusted_profit_attr_to_shareholders_margin  REAL,
    created_at                              TEXT        DEFAULT (datetime('now','localtime')),
    updated_at                              TEXT        DEFAULT (datetime('now','localtime')),
    UNIQUE (report_year, period)
);

-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 运营指标表
-- ============================================================
CREATE TABLE IF NOT EXISTS xd_core_operational_report (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    report_year                 INTEGER     NOT NULL,
    period                      TEXT        NOT NULL,
    period_index                INT         NOT NULL,
    online_games_mau            INTEGER     NOT NULL,
    online_games_mpu            INTEGER     NOT NULL,
    taptap_china_app_mau        INTEGER     NOT NULL,
    taptap_international_app_mau INTEGER    NOT NULL,
    created_at                  TEXT        DEFAULT (datetime('now','localtime')),
    updated_at                  TEXT        DEFAULT (datetime('now','localtime')),
    UNIQUE (report_year, period)
);

-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 三大费用及占比表
-- ============================================================
CREATE TABLE IF NOT EXISTS xd_expense_report (
    id                                      INTEGER PRIMARY KEY AUTOINCREMENT,
    report_year                             INTEGER     NOT NULL,
    period                                  TEXT        NOT NULL,
    period_index                            INT         NOT NULL,
    revenue                                 INTEGER     NOT NULL,
    selling_and_marketing_expenses          INTEGER     NOT NULL,
    selling_and_marketing_expenses_ratio    REAL,
    research_and_development_expenses       INTEGER     NOT NULL,
    research_and_development_expenses_ratio REAL,
    general_and_administrative_expenses     INTEGER     NOT NULL,
    general_and_administrative_expenses_ratio REAL,
    created_at                              TEXT        DEFAULT (datetime('now','localtime')),
    updated_at                              TEXT        DEFAULT (datetime('now','localtime')),
    UNIQUE (report_year, period)
);
"""

# ============================================================
# 触发器: 自动更新 updated_at 字段
# ============================================================

CREATE_TRIGGERS_SQL = """
-- 每个表创建 updated_at 自动更新触发器
CREATE TRIGGER IF NOT EXISTS trg_xd_revenue_report_update
    AFTER UPDATE ON xd_revenue_report
BEGIN
    UPDATE xd_revenue_report SET updated_at = datetime('now','localtime') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_xd_revenue_game_report_update
    AFTER UPDATE ON xd_revenue_game_report
BEGIN
    UPDATE xd_revenue_game_report SET updated_at = datetime('now','localtime') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_xd_balance_report_update
    AFTER UPDATE ON xd_balance_report
BEGIN
    UPDATE xd_balance_report SET updated_at = datetime('now','localtime') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_xd_core_financial_report_update
    AFTER UPDATE ON xd_core_financial_report
BEGIN
    UPDATE xd_core_financial_report SET updated_at = datetime('now','localtime') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_xd_core_operational_report_update
    AFTER UPDATE ON xd_core_operational_report
BEGIN
    UPDATE xd_core_operational_report SET updated_at = datetime('now','localtime') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_xd_expense_report_update
    AFTER UPDATE ON xd_expense_report
BEGIN
    UPDATE xd_expense_report SET updated_at = datetime('now','localtime') WHERE id = NEW.id;
END;
"""

# ============================================================
# 初始数据插入语句
# ============================================================

INSERT_DATA_SQL = """
-- ============================================================
-- xd_revenue_report 数据
-- ============================================================
INSERT OR IGNORE INTO xd_revenue_report
    (report_year, period, period_index,
     game_revenue, game_cost, game_gross_profit, game_gross_profit_margin,
     taptap_platform_revenue, taptap_platform_cost, taptap_platform_gross_profit, taptap_platform_gross_profit_margin)
VALUES
    (2021, 'H1',  1, 1042985, 636105, 406880,  39.01, 335722,  65903, 269819, 80.37),
    (2021, 'H2',  2,  967835, 647658, 320177,  33.08, 356631, 127264, 229367, 64.31),
    (2021, 'FY',  3, 2010820, 1283763, 727057,  36.16, 692353, 193167, 499186, 72.10),
    (2022, 'H1',  1, 1126287, 674263, 452024,  40.13, 467750, 136859, 330891, 70.74),
    (2022, 'H2',  2, 1326419, 664076, 662343,  49.93, 510480, 120479, 390001, 76.39),
    (2022, 'FY',  3, 2452706, 1338339, 1114367, 45.43, 978230, 257338, 720892, 73.69),
    (2023, 'H1',  1, 1149870, 606367, 543503,  47.27, 603232, 109474, 493758, 81.85),
    (2023, 'H2',  2,  941815, 509180, 432635,  45.94, 694227,  95753, 598474, 86.21),
    (2023, 'FY',  3, 2091685, 1115547, 976138,  46.67, 1297459, 205227, 1092232, 84.18),
    (2024, 'H1',  1, 1486257, 595409, 890848,  59.94, 734310, 128347, 605963, 82.52),
    (2024, 'H2',  2, 1947804, 690467, 1257337, 64.55, 843736, 119354, 724382, 85.85),
    (2024, 'FY',  3, 3434061, 1285876, 2148185, 62.56, 1578046, 247701, 1330345, 84.31),
    (2025, 'H1',  1, 2071260, 663812, 1407448, 67.95, 1010726, 165416, 845310, 83.63),
    (2025, 'H2',  2, 1724807, 573335, 1151472, 66.76,  956946, 106621, 850325, 88.86),
    (2025, 'FY',  3, 3796067, 1237147, 2558920, 67.41, 1967672, 272037, 1695635, 86.18);

-- ============================================================
-- xd_revenue_game_report 数据
-- ============================================================
INSERT OR IGNORE INTO xd_revenue_game_report
    (report_year, period, period_index,
     game_operation_revenue, online_game_revenue, paid_game_revenue,
     gross_basis_revenue, net_basis_revenue, other_game_revenue)
VALUES
    (2021, 'H1', 1, 1028557,  939995,  88562,  811587, 216970, 14428),
    (2021, 'H2', 2,  959442,  844037, 115405,  818214, 141228,  8393),
    (2021, 'FY', 3, 1987999, 1784032, 203967, 1629801, 358198, 22821),
    (2022, 'H1', 1, 1114697, 1042055,  72642,  971753, 142944, 11590),
    (2022, 'H2', 2, 1319712, 1268702,  51010, 1206979, 112733,  6707),
    (2022, 'FY', 3, 2434409, 2310757, 123652, 2178732, 255677, 18297),
    (2023, 'H1', 1, 1144657, 1080122,  64535, 1044393, 100264,  5213),
    (2023, 'H2', 2,  937394,  881347,  56047,  858440,  78954,  4421),
    (2023, 'FY', 3, 2082051, 1961469, 120582, 1902833, 179218,  9634),
    (2024, 'H1', 1, 1481074, 1425896,  55178, 1413438,  67636,  5183),
    (2024, 'H2', 2, 1946446, 1890893,  55553, 1866690,  79756,  1358),
    (2024, 'FY', 3, 3427520, 3316789, 110731, 3280128, 147392,  6541),
    (2025, 'H1', 1, 2045113, 1982085,  63028, 1760461, 284652, 26147),
    (2025, 'H2', 2, 1679306, 1614315,  64991, 1459301, 219789, 45501),
    (2025, 'FY', 3, 3724419, 3596400, 128019, 3219762, 504657, 71648);

-- ============================================================
-- xd_balance_report 数据
-- ============================================================
INSERT OR IGNORE INTO xd_balance_report
    (report_year, period, period_index, cash_and_cash_equivalents, contract_liabilities, total_liabilities)
VALUES
    (2021, 'H1',  1, 2464289,  138387, 2492470),
    (2021, 'FY',  3, 3164726,  206642, 2661725),
    (2022, 'H1',  1, 2095935,  276215, 2905321),
    (2022, 'FY',  3, 3098084,  156688, 2890405),
    (2023, 'H1',  1, 3301473,  150788, 2793212),
    (2023, 'FY',  3, 3206821,  180780, 2540691),
    (2024, 'H1',  1, 2163500,  351056, 1449165),
    (2024, 'FY',  3, 2781173,  321872, 1208582),
    (2025, 'H1',  1, 2971628,  288506, 1304001),
    (2025, 'FY',  3, 3689375,  248156, 1173582);

-- ============================================================
-- xd_core_financial_report 数据
-- ============================================================
INSERT OR IGNORE INTO xd_core_financial_report
    (report_year, period, period_index, revenue, gross_profit, gross_profit_margin,
     profit_for_year, profit_for_year_margin,
     profit_attr_to_shareholders, profit_attr_to_shareholders_margin,
     adjusted_profit_for_year, adjusted_profit_for_year_margin,
     adjusted_profit_attr_to_shareholders, adjusted_profit_attr_to_shareholders_margin)
VALUES
    (2021, 'H1', 1, 1378707,  676699, 49.08, -322351, -23.38, -325147, -23.58, -325753, -23.63, -328783, -23.85),
    (2021, 'H2', 2, 1324466,  549544, 41.49, -594937, -44.92, -538664, -40.67, -564592, -42.63, -511189, -38.60),
    (2021, 'FY', 3, 2703173, 1226243, 45.36, -917288, -33.93, -863811, -31.95, -890345, -32.94, -839972, -31.07),
    (2022, 'H1', 1, 1594037,  782915, 49.12, -381395, -23.93, -386056, -24.22, -332732, -20.87, -342502, -21.49),
    (2022, 'H2', 2, 1836899, 1052344, 57.29, -192618, -10.49, -167439,  -9.12, -161524,  -8.79, -139945,  -7.62),
    (2022, 'FY', 3, 3430936, 1835259, 53.49, -574013, -16.73, -553495, -16.13, -494256, -14.41, -482447, -14.06),
    (2023, 'H1', 1, 1753102, 1037261, 59.17, 102788,   5.86,   90194,   5.14,  129647,   7.40,  112979,   6.44),
    (2023, 'H2', 2, 1636042, 1031109, 63.02, -168150, -10.28, -173233, -10.59, -139053,  -8.50, -147097,  -8.99),
    (2023, 'FY', 3, 3389144, 2068370, 61.03, -65362,  -1.93,  -83039,  -2.45,   -9406,  -0.28,  -34118,  -1.01),
    (2024, 'H1', 1, 2220567, 1496811, 67.41, 250579,  11.28,  205102,   9.24,  278811,  12.56,  237290,  10.69),
    (2024, 'H2', 2, 2791540, 1981719, 70.99, 639912,  22.92,  606428,  21.72,  677874,  24.28,  639556,  22.91),
    (2024, 'FY', 3, 5012107, 3478530, 69.40, 890491,  17.77,  811530,  16.19,  956685,  19.09,  876846,  17.49),
    (2025, 'H1', 1, 3081986, 2252758, 73.10, 810596,  26.30,  754856,  24.49,  852855,  27.67,  795650,  25.81),
    (2025, 'H2', 2, 2681753, 2001797, 74.65, 845913,  31.54,  780418,  29.10,  904070,  33.71,  832913,  31.06),
    (2025, 'FY', 3, 5763739, 4254555, 73.82, 1656509,  28.74, 1535274,  26.63, 1756925,  30.48, 1628563,  28.26);

-- ============================================================
-- xd_core_operational_report 数据
-- ============================================================
INSERT OR IGNORE INTO xd_core_operational_report
    (report_year, period, period_index, online_games_mau, online_games_mpu, taptap_china_app_mau, taptap_international_app_mau)
VALUES
    (2021, 'H1', 1, 15690,  811, 28671, 13183),
    (2021, 'H2', 2, 17694, 1143, 34469, 11301),
    (2021, 'FY', 3, 16692,  977, 31570, 12242),
    (2022, 'H1', 1, 15346, 1530, 41730,  8973),
    (2022, 'H2', 2, 17102, 1616, 41172,  9287),
    (2022, 'FY', 3, 16224, 1573, 41451,  9130),
    (2023, 'H1', 1, 13269, 1389, 33967,  7135),
    (2023, 'H2', 2, 11623, 1225, 37653,  4435),
    (2023, 'FY', 3, 12446, 1307, 35810,  5785),
    (2024, 'H1', 1,  9534, 1092, 43242,  5066),
    (2024, 'H2', 2, 18960, 2126, 44850,  4998),
    (2024, 'FY', 3, 14247, 1609, 44046,  5032),
    (2025, 'H1', 1, 11409, 1322, 43625,  5020),
    (2025, 'H2', 2, 11285, 1246, 46323,  3630),
    (2025, 'FY', 3, 11347, 1284, 44974,  4325);

-- ============================================================
-- xd_expense_report 数据
-- ============================================================
INSERT OR IGNORE INTO xd_expense_report
    (report_year, period, period_index,
     revenue,
     selling_and_marketing_expenses, selling_and_marketing_expenses_ratio,
     research_and_development_expenses, research_and_development_expenses_ratio,
     general_and_administrative_expenses, general_and_administrative_expenses_ratio)
VALUES
    (2021, 'H1', 1, 1378707,  344468, 24.98,  575938, 41.77, 111567, 8.09),
    (2021, 'H2', 2, 1324466,  435716, 32.89,  666236, 50.30, 123538, 9.33),
    (2021, 'FY', 3, 2703173,  780184, 28.86, 1242174, 45.95, 235105, 8.70),
    (2022, 'H1', 1, 1594037,  403719, 25.33,  656373, 41.18, 104476, 6.55),
    (2022, 'H2', 2, 1836899,  518964, 28.25,  627451, 34.16, 129372, 7.04),
    (2022, 'FY', 3, 3430936,  922683, 26.89, 1283824, 37.42, 233848, 6.82),
    (2023, 'H1', 1, 1753102,  330402, 18.85,  527784, 30.11, 101785, 5.81),
    (2023, 'H2', 2, 1636042,  534835, 32.69,  487873, 29.82, 122828, 7.51),
    (2023, 'FY', 3, 3389144,  865237, 25.53, 1015657, 29.97, 224613, 6.63),
    (2024, 'H1', 1, 2220567,  695322, 31.31,  419489, 18.89, 138323, 6.23),
    (2024, 'H2', 2, 2791540,  701929, 25.14,  499957, 17.91, 128594, 4.61),
    (2024, 'FY', 3, 5012107, 1397251, 27.88,  919446, 18.34, 266917, 5.33),
    (2025, 'H1', 1, 3081986,  743857, 24.14,  548871, 17.81, 125983, 4.09),
    (2025, 'H2', 2, 2681753,  692074, 25.81,  432529, 16.13,  86656, 3.23),
    (2025, 'FY', 3, 5763739, 1435931, 24.91,  981400, 17.03, 212639, 3.69);
"""

# 所有表名列表
ALL_TABLES = [
    "xd_revenue_report",
    "xd_revenue_game_report",
    "xd_balance_report",
    "xd_core_financial_report",
    "xd_core_operational_report",
    "xd_expense_report",
]


def create_all_tables(pool: Optional[ConnectionPool] = None) -> None:
    """
    创建所有表结构（不插入数据）

    Args:
        pool: 连接池实例，如不提供则使用全局连接池
    """
    if pool is None:
        pool = get_pool()

    with pool.get_connection() as conn:
        conn.executescript(CREATE_TABLES_SQL)
        conn.executescript(CREATE_TRIGGERS_SQL)


def insert_initial_data(pool: Optional[ConnectionPool] = None) -> None:
    """
    插入初始数据（使用 INSERT OR IGNORE，不会重复插入）

    Args:
        pool: 连接池实例，如不提供则使用全局连接池
    """
    if pool is None:
        pool = get_pool()

    with pool.get_connection() as conn:
        conn.executescript(INSERT_DATA_SQL)


def init_database(
    db_path: str = "",
    with_data: bool = True,
    pool: Optional[ConnectionPool] = None,
) -> ConnectionPool:
    """
    初始化数据库：创建表和可选地插入初始数据

    Args:
        db_path: 数据库文件路径，默认为项目根目录下的 xd_financial.db
        with_data: 是否同时插入初始数据，默认 True
        pool: 连接池实例，如不提供则获取或创建全局连接池

    Returns:
        ConnectionPool: 初始化后的连接池实例
    """
    global _initialized

    with _init_lock:
        if pool is None:
            pool = get_pool(db_path=db_path)

        create_all_tables(pool)

        if with_data:
            insert_initial_data(pool)

        _initialized = True

    return pool


def recreate_all_tables(db_path: str = "") -> ConnectionPool:
    """
    删除并重建所有表（含数据）

    WARNING: 这会删除所有现有数据！

    Args:
        db_path: 数据库文件路径

    Returns:
        ConnectionPool: 连接池实例
    """
    pool = get_pool(db_path=db_path)

    with pool.get_connection() as conn:
        # 删除所有表
        for table in ALL_TABLES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        # 删除所有触发器
        for table in ALL_TABLES:
            conn.execute(f"DROP TRIGGER IF EXISTS trg_{table}_update")

    # 重建
    return init_database(db_path=db_path, with_data=True, pool=pool)


def is_initialized() -> bool:
    """检查数据库是否已初始化"""
    return _initialized