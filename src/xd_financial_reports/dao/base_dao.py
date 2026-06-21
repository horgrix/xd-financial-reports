"""
基础 DAO 抽象类

提供通用的 CRUD 操作模板，包括：
- get_by_id: 根据主键 id 查询单条记录
- get_all: 查询所有记录
- get_by_condition: 根据条件查询记录列表
- insert: 插入一条记录
- update_by_id: 根据 id 更新一条记录
- delete_by_id: 根据 id 删除一条记录
- count: 统计记录数
- truncate: 清空表数据

子类只需要设置 table_name、pk_field 和 columns 即可。
"""
import sqlite3
from typing import Any, Optional

from ..db.connection import ConnectionPool, get_pool


class BaseDAO:
    """
    DAO 基类，提供泛化的 CRUD 操作

    使用方式:
        class MyTableDAO(BaseDAO):
            table_name = "my_table"
            pk_field = "id"
            columns = ["id", "name", "value", "created_at", "updated_at"]
    """

    # 子类必须覆盖以下属性
    table_name: str = ""
    pk_field: str = "id"
    # 需要返回的所有字段名列表
    columns: list[str] = []
    # 插入时不需要自动生成的字段
    auto_generated_fields: set[str] = {"id", "created_at", "updated_at"}

    def __init__(self, pool: Optional[ConnectionPool] = None):
        """
        初始化 DAO

        Args:
            pool: 连接池实例，如不提供则使用全局连接池
        """
        self._pool = pool or get_pool()
        self._validate()

    def _validate(self):
        """验证子类配置"""
        if not self.table_name:
            raise ValueError(f"{self.__class__.__name__}: table_name 不能为空")
        if not self.columns:
            raise ValueError(f"{self.__class__.__name__}: columns 不能为空")

    def _get_conn(self) -> sqlite3.Connection:
        """获取数据库连接"""
        return self._pool.get_connection()

    # ============================================================
    # 查询操作
    # ============================================================

    def get_by_id(self, pk_value: Any) -> Optional[sqlite3.Row]:
        """
        根据主键查询单条记录

        Args:
            pk_value: 主键值

        Returns:
            sqlite3.Row 或 None
        """
        columns_str = ", ".join(self.columns)
        sql = f"SELECT {columns_str} FROM {self.table_name} WHERE {self.pk_field} = ?"
        with self._get_conn() as conn:
            row = conn.execute(sql, (pk_value,)).fetchone()
            return row

    def get_all(self, order_by: str = "", limit: int = 0, offset: int = 0) -> list[sqlite3.Row]:
        """
        查询所有记录

        Args:
            order_by: 排序字段，如 "id DESC"
            limit: 限制返回条数，0 表示不限制
            offset: 偏移量

        Returns:
            sqlite3.Row 列表
        """
        columns_str = ", ".join(self.columns)
        sql = f"SELECT {columns_str} FROM {self.table_name}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit > 0:
            sql += f" LIMIT {limit}"
            if offset > 0:
                sql += f" OFFSET {offset}"
        with self._get_conn() as conn:
            rows = conn.execute(sql).fetchall()
            return rows

    def get_by_condition(
        self,
        where: str = "",
        params: tuple = (),
        order_by: str = "",
        limit: int = 0,
        offset: int = 0,
    ) -> list[sqlite3.Row]:
        """
        根据条件查询记录

        Args:
            where: WHERE 子句（不含 WHERE 关键字），使用 ? 占位符，如 "report_year = ? AND period = ?"
            params: 占位符对应的参数元组
            order_by: 排序字段
            limit: 限制返回条数
            offset: 偏移量

        Returns:
            sqlite3.Row 列表
        """
        columns_str = ", ".join(self.columns)
        sql = f"SELECT {columns_str} FROM {self.table_name}"
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit > 0:
            sql += f" LIMIT {limit}"
            if offset > 0:
                sql += f" OFFSET {offset}"
        with self._get_conn() as conn:
            rows = conn.execute(sql, params).fetchall()
            return rows

    def get_one_by_condition(
        self, where: str, params: tuple = ()
    ) -> Optional[sqlite3.Row]:
        """
        根据条件查询单条记录

        Args:
            where: WHERE 子句
            params: 参数元组

        Returns:
            sqlite3.Row 或 None
        """
        columns_str = ", ".join(self.columns)
        sql = f"SELECT {columns_str} FROM {self.table_name} WHERE {where} LIMIT 1"
        with self._get_conn() as conn:
            row = conn.execute(sql, params).fetchone()
            return row

    def exists(self, where: str, params: tuple = ()) -> bool:
        """
        检查记录是否存在

        Args:
            where: WHERE 子句
            params: 参数元组

        Returns:
            True 如果存在
        """
        sql = f"SELECT 1 FROM {self.table_name} WHERE {where} LIMIT 1"
        with self._get_conn() as conn:
            row = conn.execute(sql, params).fetchone()
            return row is not None

    # ============================================================
    # 插入操作
    # ============================================================

    def insert(self, **kwargs) -> int:
        """
        插入一条记录

        Args:
            **kwargs: 字段名=值的键值对，不需要包含自增主键和自动生成字段

        Returns:
            新插入记录的 id

        Raises:
            ValueError: 如果提供了自增字段
        """
        # 过滤掉自动生成字段
        insert_data = {
            k: v for k, v in kwargs.items()
            if k not in self.auto_generated_fields
        }
        if not insert_data:
            raise ValueError("没有可插入的字段数据")

        columns = list(insert_data.keys())
        placeholders = ", ".join(["?" for _ in columns])
        values = tuple(insert_data.values())
        columns_str = ", ".join(columns)

        sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
        with self._get_conn() as conn:
            cursor = conn.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

    def insert_or_replace(self, **kwargs) -> int:
        """
        插入或替换一条记录（根据唯一约束）

        Args:
            **kwargs: 字段名=值的键值对

        Returns:
            记录的 id
        """
        insert_data = {
            k: v for k, v in kwargs.items()
            if k not in self.auto_generated_fields
        }
        columns = list(insert_data.keys())
        placeholders = ", ".join(["?" for _ in columns])
        values = tuple(insert_data.values())
        columns_str = ", ".join(columns)

        sql = f"INSERT OR REPLACE INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
        with self._get_conn() as conn:
            cursor = conn.execute(sql, values)
            conn.commit()
            return cursor.lastrowid

    def insert_batch(self, rows: list[dict]) -> int:
        """
        批量插入记录

        Args:
            rows: 字典列表，每个字典是字段名=值的键值对

        Returns:
            插入的行数
        """
        if not rows:
            return 0

        # 从第一行推断列（过滤掉自动生成字段）
        first_row = {
            k: v for k, v in rows[0].items()
            if k not in self.auto_generated_fields
        }
        columns = list(first_row.keys())
        placeholders = ", ".join(["?" for _ in columns])
        columns_str = ", ".join(columns)

        sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"

        values_list = [
            tuple(row.get(c) for c in columns if c not in self.auto_generated_fields)
            for row in rows
        ]

        with self._get_conn() as conn:
            conn.executemany(sql, values_list)
            conn.commit()
            return len(rows)

    # ============================================================
    # 更新操作
    # ============================================================

    def update_by_id(self, pk_value: Any, **kwargs) -> bool:
        """
        根据主键更新记录

        Args:
            pk_value: 主键值
            **kwargs: 要更新的字段名=值

        Returns:
            True 如果更新成功
        """
        # 过滤掉自动生成字段和主键
        update_data = {
            k: v for k, v in kwargs.items()
            if k not in self.auto_generated_fields and k != self.pk_field
        }
        if not update_data:
            return False

        set_clause = ", ".join([f"{col} = ?" for col in update_data.keys()])
        values = tuple(update_data.values()) + (pk_value,)

        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.pk_field} = ?"
        with self._get_conn() as conn:
            cursor = conn.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0

    def update_by_condition(self, where: str, params: tuple, **kwargs) -> int:
        """
        根据条件更新记录

        Args:
            where: WHERE 子句
            params: WHERE 参数元组
            **kwargs: 要更新的字段名=值

        Returns:
            受影响的行数
        """
        update_data = {
            k: v for k, v in kwargs.items()
            if k not in self.auto_generated_fields
        }
        if not update_data:
            return 0

        set_clause = ", ".join([f"{col} = ?" for col in update_data.keys()])
        values = tuple(update_data.values()) + params

        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {where}"
        with self._get_conn() as conn:
            cursor = conn.execute(sql, values)
            conn.commit()
            return cursor.rowcount

    # ============================================================
    # 删除操作
    # ============================================================

    def delete_by_id(self, pk_value: Any) -> bool:
        """
        根据主键删除记录

        Args:
            pk_value: 主键值

        Returns:
            True 如果成功删除
        """
        sql = f"DELETE FROM {self.table_name} WHERE {self.pk_field} = ?"
        with self._get_conn() as conn:
            cursor = conn.execute(sql, (pk_value,))
            conn.commit()
            return cursor.rowcount > 0

    def delete_by_condition(self, where: str, params: tuple = ()) -> int:
        """
        根据条件删除记录

        Args:
            where: WHERE 子句
            params: 参数元组

        Returns:
            删除的行数
        """
        sql = f"DELETE FROM {self.table_name} WHERE {where}"
        with self._get_conn() as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.rowcount

    # ============================================================
    # 聚合操作
    # ============================================================

    def count(self, where: str = "", params: tuple = ()) -> int:
        """
        统计记录数

        Args:
            where: 可选的 WHERE 子句
            params: 参数元组

        Returns:
            记录总数
        """
        sql = f"SELECT COUNT(*) FROM {self.table_name}"
        if where:
            sql += f" WHERE {where}"
        with self._get_conn() as conn:
            row = conn.execute(sql, params).fetchone()
            return row[0] if row else 0

    def truncate(self) -> None:
        """清空表所有数据"""
        sql = f"DELETE FROM {self.table_name}"
        with self._get_conn() as conn:
            conn.execute(sql)
            conn.commit()

    # ============================================================
    # 工具方法
    # ============================================================

    @staticmethod
    def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[dict]:
        """将 sqlite3.Row 转换为 dict"""
        if row is None:
            return None
        return dict(row)

    @classmethod
    def rows_to_dicts(cls, rows: list[sqlite3.Row]) -> list[dict]:
        """将 sqlite3.Row 列表转换为 dict 列表"""
        return [dict(row) for row in rows]