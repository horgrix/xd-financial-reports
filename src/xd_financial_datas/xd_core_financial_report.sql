-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 核心财务指标表
-- 表名: xd_core_financial_report
-- 数据来源: 各年业绩公告 (2021-2025 H1/FY)
-- 单位: 金额为千元, 比率为百分比(小数)
-- ============================================================

-- 删除旧表(如存在)
DROP TABLE IF EXISTS xd_core_financial_report;

-- 建表
CREATE TABLE xd_core_financial_report (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    report_year         YEAR        NOT NULL COMMENT '财年',
    period              VARCHAR(4)  NOT NULL COMMENT '期间: H1=上半年, H2=下半年, FY=全年',
    period_index        INT         NOT NULL COMMENT 'H1=1, H2=2, FY=3',
    revenue             BIGINT      NOT NULL COMMENT '收入(千元)',
    gross_profit        BIGINT      NOT NULL COMMENT '毛利(千元)',
    gross_profit_margin DECIMAL(6,2)        COMMENT '毛利率(%)',
    profit_for_year             BIGINT      NOT NULL COMMENT '年内溢利(千元)',
    profit_for_year_margin      DECIMAL(6,2)        COMMENT '年内溢利率(%)',
    profit_attr_to_shareholders         BIGINT      NOT NULL COMMENT '本公司权益持有人应占溢利(千元)',
    profit_attr_to_shareholders_margin  DECIMAL(6,2)        COMMENT '本公司权益持有人应占溢利率(%)',
    adjusted_profit_for_year            BIGINT      NOT NULL COMMENT '年内经调整溢利(千元)',
    adjusted_profit_for_year_margin     DECIMAL(6,2)        COMMENT '年内经调整溢利率(%)',
    adjusted_profit_attr_to_shareholders         BIGINT      NOT NULL COMMENT '本公司权益持有人应占经调整溢利(千元)',
    adjusted_profit_attr_to_shareholders_margin  DECIMAL(6,2)        COMMENT '本公司权益持有人应占经调整溢利率(%)',
    created_at          TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_year_period (report_year, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心动公司核心财务指标表';

-- ============================================================
-- 插入数据 (2021-2025)
-- ============================================================

INSERT INTO xd_core_financial_report
    (report_year, period, revenue, gross_profit, gross_profit_margin,
     profit_for_year, profit_for_year_margin,
     profit_attr_to_shareholders, profit_attr_to_shareholders_margin,
     adjusted_profit_for_year, adjusted_profit_for_year_margin,
     adjusted_profit_attr_to_shareholders, adjusted_profit_attr_to_shareholders_margin)
VALUES
    -- 2021
    (2021, 'H1',  1, 1378707,  676699, 49.08,
     -322351, -23.38,
     -325147, -23.58,
     -325753, -23.63,
     -328783, -23.85),
    (2021, 'H2',  2, 1324466,  549544, 41.49,
     -594937, -44.92,
     -538664, -40.67,
     -564592, -42.63,
     -511189, -38.60),
    (2021, 'FY',  3, 2703173, 1226243, 45.36,
     -917288, -33.93,
     -863811, -31.95,
     -890345, -32.94,
     -839972, -31.07),

    -- 2022
    (2022, 'H1',  1, 1594037,  782915, 49.12,
     -381395, -23.93,
     -386056, -24.22,
     -332732, -20.87,
     -342502, -21.49),
    (2022, 'H2',  2, 1836899, 1052344, 57.29,
     -192618, -10.49,
     -167439,  -9.12,
     -161524,  -8.79,
     -139945,  -7.62),
    (2022, 'FY',  3, 3430936, 1835259, 53.49,
     -574013, -16.73,
     -553495, -16.13,
     -494256, -14.41,
     -482447, -14.06),

    -- 2023
    (2023, 'H1',  1, 1753102, 1037261, 59.17,
      102788,   5.86,
       90194,   5.14,
      129647,   7.40,
      112979,   6.44),
    (2023, 'H2',  2, 1636042, 1031109, 63.02,
     -168150, -10.28,
     -173233, -10.59,
     -139053,  -8.50,
     -147097,  -8.99),
    (2023, 'FY',  3, 3389144, 2068370, 61.03,
      -65362,  -1.93,
      -83039,  -2.45,
       -9406,  -0.28,
      -34118,  -1.01),

    -- 2024
    (2024, 'H1',  1, 2220567, 1496811, 67.41,
      250579,  11.28,
      205102,   9.24,
      278811,  12.56,
      237290,  10.69),
    (2024, 'H2',  2, 2791540, 1981719, 70.99,
      639912,  22.92,
      606428,  21.72,
      677874,  24.28,
      639556,  22.91),
    (2024, 'FY',  3, 5012107, 3478530, 69.40,
      890491,  17.77,
      811530,  16.19,
      956685,  19.09,
      876846,  17.49),

    -- 2025
    (2025, 'H1',  1, 3081986, 2252758, 73.10,
      810596,  26.30,
      754856,  24.49,
      852855,  27.67,
      795650,  25.81),
    (2025, 'H2',  2, 2681753, 2001797, 74.65,
      845913,  31.54,
      780418,  29.10,
      904070,  33.71,
      832913,  31.06),
    (2025, 'FY',  3, 5763739, 4254555, 73.82,
     1656509,  28.74,
     1535274,  26.63,
     1756925,  30.48,
     1628563,  28.26);