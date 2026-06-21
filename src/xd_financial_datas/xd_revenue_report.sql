-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 分业务收入/成本/毛利/毛利率表
-- 表名: xd_revenue_report
-- 数据来源: 各年业绩公告分部资料 (2021-2025 H1/FY)
-- 单位: 金额为千元, 毛利率为百分比(小数)
-- H2 计算公式: FY − H1
-- ============================================================

-- 删除旧表(如存在)
DROP TABLE IF EXISTS xd_revenue_report;

-- 建表
CREATE TABLE xd_revenue_report (
    id                              INT PRIMARY KEY AUTO_INCREMENT,
    report_year                     YEAR        NOT NULL COMMENT '财年',
    period                          VARCHAR(4)  NOT NULL COMMENT '期间: H1=上半年, H2=下半年, FY=全年',
    game_revenue                    BIGINT      NOT NULL COMMENT '遊戲收入(千元)',
    game_cost                       BIGINT      NOT NULL COMMENT '遊戲成本(千元)',
    game_gross_profit               BIGINT      NOT NULL COMMENT '遊戲毛利(千元)',
    game_gross_profit_margin        DECIMAL(6,2)        COMMENT '遊戲毛利率(%)',
    taptap_platform_revenue         BIGINT      NOT NULL COMMENT 'TapTap平台收入(千元)',
    taptap_platform_cost            BIGINT      NOT NULL COMMENT 'TapTap平台成本(千元)',
    taptap_platform_gross_profit    BIGINT      NOT NULL COMMENT 'TapTap平台毛利(千元)',
    taptap_platform_gross_profit_margin DECIMAL(6,2)    COMMENT 'TapTap平台毛利率(%)',
    created_at                      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at                      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_year_period (report_year, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心动公司分业务收入成本毛利表';

-- ============================================================
-- 插入数据 (2021-2025)
-- ============================================================

INSERT INTO xd_revenue_report
    (report_year, period,
     game_revenue, game_cost, game_gross_profit, game_gross_profit_margin,
     taptap_platform_revenue, taptap_platform_cost, taptap_platform_gross_profit, taptap_platform_gross_profit_margin)
VALUES
    -- 2021
    (2021, 'H1',
     1042985, 636105, 406880, 39.01,
     335722, 65903, 269819, 80.37),
    (2021, 'H2',
      967835, 647658, 320177, 33.08,
      356631, 127264, 229367, 64.31),
    (2021, 'FY',
     2010820, 1283763, 727057, 36.16,
      692353, 193167, 499186, 72.10),

    -- 2022
    (2022, 'H1',
     1126287, 674263, 452024, 40.13,
      467750, 136859, 330891, 70.74),
    (2022, 'H2',
     1326419, 664076, 662343, 49.93,
      510480, 120479, 390001, 76.39),
    (2022, 'FY',
     2452706, 1338339, 1114367, 45.43,
      978230, 257338, 720892, 73.69),

    -- 2023
    (2023, 'H1',
     1149870, 606367, 543503, 47.27,
      603232, 109474, 493758, 81.85),
    (2023, 'H2',
      941815, 509180, 432635, 45.94,
      694227, 95753, 598474, 86.21),
    (2023, 'FY',
     2091685, 1115547, 976138, 46.67,
     1297459, 205227, 1092232, 84.18),

    -- 2024
    (2024, 'H1',
     1486257, 595409, 890848, 59.94,
      734310, 128347, 605963, 82.52),
    (2024, 'H2',
     1947804, 690467, 1257337, 64.55,
      843736, 119354, 724382, 85.85),
    (2024, 'FY',
     3434061, 1285876, 2148185, 62.56,
     1578046, 247701, 1330345, 84.31),

    -- 2025
    (2025, 'H1',
     2071260, 663812, 1407448, 67.95,
     1010726, 165416, 845310, 83.63),
    (2025, 'H2',
     1724807, 573335, 1151472, 66.76,
      956946, 106621, 850325, 88.86),
    (2025, 'FY',
     3796067, 1237147, 2558920, 67.41,
     1967672, 272037, 1695635, 86.18);