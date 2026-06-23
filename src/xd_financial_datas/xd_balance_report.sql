-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 现金、合约负债及负债总额表
-- 表名: xd_balance_report
-- 数据来源: 各年业绩公告综合财务状况表 (2021-2025 H1/FY)
-- 单位: 千元
-- 注: H1 = 6月30日时点数，FY = 12月31日时点数
-- ============================================================

-- 删除旧表(如存在)
DROP TABLE IF EXISTS xd_balance_report;

-- 建表
CREATE TABLE xd_balance_report (
    id                          INT PRIMARY KEY AUTO_INCREMENT,
    report_year                 YEAR        NOT NULL COMMENT '财年',
    period                      VARCHAR(4)  NOT NULL COMMENT '期间: H1=6月30日, FY=12月31日',
    cash_and_cash_equivalents   BIGINT      NOT NULL COMMENT '现金及现金等价物(千元)',
    contract_liabilities        BIGINT      NOT NULL COMMENT '合约负债(千元)',
    total_liabilities           BIGINT      NOT NULL COMMENT '负债总额(千元)',
    created_at                  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at                  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_year_period (report_year, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心动公司资产负债关键指标表';

-- ============================================================
-- 插入数据 (2021-2025)
-- ============================================================

INSERT INTO xd_balance_report
    (report_year, period, cash_and_cash_equivalents, contract_liabilities, total_liabilities)
VALUES
    -- 2021
    (2021, 'H1',  2464289,  138387, 2492470),
    (2021, 'FY',  3164726,  206642, 2661725),

    -- 2022
    (2022, 'H1',  2095935,  276215, 2905321),
    (2022, 'FY',  3098084,  156688, 2890405),

    -- 2023
    (2023, 'H1',  3301473,  150788, 2793212),
    (2023, 'FY',  3206821,  180780, 2540691),

    -- 2024
    (2024, 'H1',  2163500,  351056, 1449165),
    (2024, 'FY',  2781173,  321872, 1208582),

    -- 2025
    (2025, 'H1',  2971628,  288506, 1304001),
    (2025, 'FY',  3689375,  248156, 1173582);