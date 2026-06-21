-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 三大费用及占比表
-- 表名: xd_expense_report
-- 数据来源: 各年业绩公告综合损益表 (2021-2025 H1/FY)
-- 单位: 金额为千元, 占比为百分比(小数)
-- H2 计算公式: FY − H1
-- ============================================================

-- 删除旧表(如存在)
DROP TABLE IF EXISTS xd_expense_report;

-- 建表
CREATE TABLE xd_expense_report (
    id                              INT PRIMARY KEY AUTO_INCREMENT,
    report_year                     YEAR        NOT NULL COMMENT '财年',
    period                          VARCHAR(4)  NOT NULL COMMENT '期间: H1=上半年, H2=下半年, FY=全年',
    revenue                         BIGINT      NOT NULL COMMENT '收入(千元)',
    selling_and_marketing_expenses          BIGINT      NOT NULL COMMENT '销售及营销开支(千元)',
    selling_and_marketing_expenses_ratio    DECIMAL(6,2)        COMMENT '销售及营销开支占比(%)',
    research_and_development_expenses       BIGINT      NOT NULL COMMENT '研发开支(千元)',
    research_and_development_expenses_ratio DECIMAL(6,2)        COMMENT '研发开支占比(%)',
    general_and_administrative_expenses     BIGINT      NOT NULL COMMENT '一般及行政开支(千元)',
    general_and_administrative_expenses_ratio DECIMAL(6,2)      COMMENT '一般及行政开支占比(%)',
    created_at                      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at                      TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_year_period (report_year, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心动公司三大费用及占比表';

-- ============================================================
-- 插入数据 (2021-2025)
-- ============================================================

INSERT INTO xd_expense_report
    (report_year, period,
     revenue,
     selling_and_marketing_expenses, selling_and_marketing_expenses_ratio,
     research_and_development_expenses, research_and_development_expenses_ratio,
     general_and_administrative_expenses, general_and_administrative_expenses_ratio)
VALUES
    -- 2021
    (2021, 'H1',
     1378707,
     344468, 24.98,
     575938, 41.77,
     111567, 8.09),
    (2021, 'H2',
     1324466,
     435716, 32.89,
     666236, 50.30,
     123538, 9.33),
    (2021, 'FY',
     2703173,
     780184, 28.86,
     1242174, 45.95,
     235105, 8.70),

    -- 2022
    (2022, 'H1',
     1594037,
     403719, 25.33,
     656373, 41.18,
     104476, 6.55),
    (2022, 'H2',
     1836899,
     518964, 28.25,
     627451, 34.16,
     129372, 7.04),
    (2022, 'FY',
     3430936,
     922683, 26.89,
     1283824, 37.42,
     233848, 6.82),

    -- 2023
    (2023, 'H1',
     1753102,
     330402, 18.85,
     527784, 30.11,
     101785, 5.81),
    (2023, 'H2',
     1636042,
     534835, 32.69,
     487873, 29.82,
     122828, 7.51),
    (2023, 'FY',
     3389144,
     865237, 25.53,
     1015657, 29.97,
     224613, 6.63),

    -- 2024
    (2024, 'H1',
     2220567,
     695322, 31.31,
     419489, 18.89,
     138323, 6.23),
    (2024, 'H2',
     2791540,
     701929, 25.14,
     499957, 17.91,
     128594, 4.61),
    (2024, 'FY',
     5012107,
     1397251, 27.88,
     919446, 18.34,
     266917, 5.33),

    -- 2025
    (2025, 'H1',
     3081986,
     743857, 24.14,
     548871, 17.81,
     125983, 4.09),
    (2025, 'H2',
     2681753,
     692074, 25.81,
     432529, 16.13,
     86656, 3.23),
    (2025, 'FY',
     5763739,
     1435931, 24.91,
     981400, 17.03,
     212639, 3.69);