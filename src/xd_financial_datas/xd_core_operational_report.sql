-- ============================================================
-- 心动公司 (XD Inc.) 2021-2025 运营指标表
-- 表名: xd_core_operational_report
-- 数据来源: 各年业绩公告 (2021-2025 H1/FY)
-- 单位: 千人
-- H2 计算公式: (FY × 12 − H1 × 6) / 6
-- ============================================================

-- 删除旧表(如存在)
DROP TABLE IF EXISTS xd_core_operational_report;

-- 建表
CREATE TABLE xd_core_operational_report (
    id                          INT PRIMARY KEY AUTO_INCREMENT,
    report_year                 YEAR        NOT NULL COMMENT '财年',
    period                      VARCHAR(4)  NOT NULL COMMENT '期间: H1=上半年, H2=下半年, FY=全年',
    online_games_mau            INT         NOT NULL COMMENT '网络游戏平均月活跃用户(千人)',
    online_games_mpu            INT         NOT NULL COMMENT '网络游戏平均月付费用户(千人)',
    taptap_china_app_mau        INT         NOT NULL COMMENT 'TapTap中国版App平均月活跃用户(千人)',
    taptap_international_app_mau INT        NOT NULL COMMENT 'TapTap国际版App平均月活跃用户(千人)',
    created_at                  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    updated_at                  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_year_period (report_year, period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心动公司运营指标表';

-- ============================================================
-- 插入数据 (2021-2025)
-- ============================================================

INSERT INTO xd_core_operational_report
    (report_year, period, online_games_mau, online_games_mpu, taptap_china_app_mau, taptap_international_app_mau)
VALUES
    -- 2021
    (2021, 'H1',  15690,   811, 28671, 13183),
    (2021, 'H2',  17694,  1143, 34469, 11301),
    (2021, 'FY',  16692,   977, 31570, 12242),

    -- 2022
    (2022, 'H1',  15346,  1530, 41730,  8973),
    (2022, 'H2',  17102,  1616, 41172,  9287),
    (2022, 'FY',  16224,  1573, 41451,  9130),

    -- 2023
    (2023, 'H1',  13269,  1389, 33967,  7135),
    (2023, 'H2',  11623,  1225, 37653,  4435),
    (2023, 'FY',  12446,  1307, 35810,  5785),

    -- 2024
    (2024, 'H1',   9534,  1092, 43242,  5066),
    (2024, 'H2',  18960,  2126, 44850,  4998),
    (2024, 'FY',  14247,  1609, 44046,  5032),

    -- 2025
    (2025, 'H1',  11409,  1322, 43625,  5020),
    (2025, 'H2',  11285,  1246, 46323,  3630),
    (2025, 'FY',  11347,  1284, 44974,  4325);