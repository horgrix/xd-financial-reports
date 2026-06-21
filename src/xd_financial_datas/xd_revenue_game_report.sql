-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 游戏收入构成细分表
-- 表名: xd_revenue_game_report
-- 数据来源: 各年业绩公告收入构成分析表 (2021-2025 H1/FY)
-- 单位: 千元
-- H2 计算公式: FY − H1
-- ============================================================

-- 删除旧表(如存在)
DROP TABLE IF EXISTS xd_revenue_game_report;

-- 建表
CREATE TABLE xd_revenue_game_report (
    id                              INT PRIMARY KEY AUTO_INCREMENT,
    report_year                     YEAR        NOT NULL COMMENT '财年',
    period                          VARCHAR(4)  NOT NULL COMMENT '期间: H1=上半年, H2=下半年, FY=全年',
    game_operation_revenue          BIGINT      NOT NULL COMMENT '游戏运营收入(千元)',
    online_game_revenue             BIGINT      NOT NULL COMMENT '网络游戏收入(千元)',
    paid_game_revenue               BIGINT      NOT NULL COMMENT '付费游戏收入(千元)',
    gross_basis_revenue             BIGINT      NOT NULL COMMENT '按总额基准确认的收入(千元)',
    net_basis_revenue               BIGINT      NOT NULL COMMENT '按净额基准确认的收入(千元)',
    other_game_revenue              BIGINT      NOT NULL COMMENT '其他(游戏内营销及推广)(千元)',
    created_at                      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at                      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_year_period (report_year, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心动公司游戏收入构成细分表';

-- ============================================================
-- 插入数据 (2021-2025)
-- ============================================================

INSERT INTO xd_revenue_game_report
    (report_year, period,
     game_operation_revenue, online_game_revenue, paid_game_revenue,
     gross_basis_revenue, net_basis_revenue, other_game_revenue)
VALUES
    -- 2021
    (2021, 'H1',
     1028557,  939995,  88562,
      811587,  216970,  14428),
    (2021, 'H2',
      959442,  844037, 115405,
      818214,  141228,   8393),
    (2021, 'FY',
     1987999, 1784032, 203967,
     1629801,  358198,  22821),

    -- 2022
    (2022, 'H1',
     1114697, 1042055,  72642,
      971753,  142944,  11590),
    (2022, 'H2',
     1319712, 1268702,  51010,
     1206979,  112733,   6707),
    (2022, 'FY',
     2434409, 2310757, 123652,
     2178732,  255677,  18297),

    -- 2023
    (2023, 'H1',
     1144657, 1080122,  64535,
     1044393,  100264,   5213),
    (2023, 'H2',
      937394,  881347,  56047,
      858440,   78954,   4421),
    (2023, 'FY',
     2082051, 1961469, 120582,
     1902833,  179218,   9634),

    -- 2024
    (2024, 'H1',
     1481074, 1425896,  55178,
     1413438,   67636,   5183),
    (2024, 'H2',
     1946446, 1890893,  55553,
     1866690,   79756,   1358),
    (2024, 'FY',
     3427520, 3316789, 110731,
     3280128,  147392,   6541),

    -- 2025
    (2025, 'H1',
     2045113, 1982085,  63028,
     1760461,  284652,  26147),
    (2025, 'H2',
     1679306, 1614315,  64991,
     1459301,  219789,  45501),
    (2025, 'FY',
     3724419, 3596400, 128019,
     3219762,  504657,  71648);