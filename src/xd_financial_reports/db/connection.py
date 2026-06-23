"""
SQLite 连接池模块

提供线程安全的 SQLite 连接池，支持连接复用和自动管理。
"""
import sqlite3
import threading
from pathlib import Path
from typing import Optional

# 默认数据库路径
DEFAULT_DB_PATH = Path(__file__).parent.parent.parent.parent / "xd_financial_1.2.db"
DEFAULT_POOL_SIZE = 5


class ConnectionPool:
    """
    SQLite 连接池

    线程安全的连接池实现，每个线程获取一个专用连接。
    由于 SQLite 本身对多线程的限制，实际采用 thread-local 策略：
    每个线程维护自己的连接，避免跨线程共享。

    使用方式:
        pool = ConnectionPool("path/to/db.db")
        with pool.get_connection() as conn:
            conn.execute("SELECT ...")
    """

    def __init__(self, db_path: str = "", pool_size: int = DEFAULT_POOL_SIZE):
        """
        初始化连接池

        Args:
            db_path: 数据库文件路径，默认为项目根目录下的 xd_financial.db
            pool_size: 连接池大小（保留参数，用于兼容性）
        """
        if not db_path:
            db_path = str(DEFAULT_DB_PATH)
        self.db_path = db_path
        self.pool_size = pool_size
        self._lock = threading.Lock()
        self._connections: list[sqlite3.Connection] = []
        self._in_use: set[int] = set()
        self._closed = False

    def _create_connection(self) -> sqlite3.Connection:
        """创建并配置一个新的 SQLite 连接"""
        conn = sqlite3.connect(
            self.db_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def get_connection(self) -> sqlite3.Connection:
        """
        获取一个数据库连接

        Returns:
            sqlite3.Connection: 配置好的数据库连接对象

        Raises:
            RuntimeError: 如果连接池已关闭
        """
        if self._closed:
            raise RuntimeError("ConnectionPool is closed")

        with self._lock:
            if self._connections:
                conn = self._connections.pop()
            else:
                conn = self._create_connection()
            conn_id = id(conn)
            self._in_use.add(conn_id)

        # 包装连接，使其在 close 时归还到池中
        return _PooledConnection(conn, self)

    def release_connection(self, conn: sqlite3.Connection):
        """
        归还连接到连接池

        Args:
            conn: 要归还的连接对象
        """
        conn_id = id(conn)
        with self._lock:
            if conn_id in self._in_use:
                self._in_use.discard(conn_id)
                if len(self._connections) < self.pool_size:
                    self._connections.append(conn)
                else:
                    # 池已满，关闭多余的连接
                    try:
                        conn.close()
                    except sqlite3.Error:
                        pass

    def close_all(self):
        """关闭连接池中的所有连接"""
        with self._lock:
            self._closed = True
            for conn in self._connections:
                try:
                    conn.close()
                except sqlite3.Error:
                    pass
            self._connections.clear()
            self._in_use.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()


class _PooledConnection:
    """
    包装 sqlite3.Connection，使其在上下文退出时自动归还到连接池。

    支持两种使用方式：
    1. 作为上下文管理器:
        with pool.get_connection() as conn:
            conn.execute(...)

    2. 手动管理:
        conn = pool.get_connection()
        try:
            conn.execute(...)
        finally:
            conn.release()
    """

    def __init__(self, conn: sqlite3.Connection, pool: ConnectionPool):
        self._conn = conn
        self._pool = pool
        self._released = False

    def __getattr__(self, name):
        # 委托所有属性访问到原始连接
        return getattr(self._conn, name)

    def release(self):
        """手动归还连接到池中"""
        if not self._released:
            self._released = True
            self._pool.release_connection(self._conn)

    def close(self):
        """关闭连接（归还到池中）"""
        self.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False


# 全局连接池实例
_pool: Optional[ConnectionPool] = None
_pool_lock = threading.Lock()


def get_pool(db_path: str = "", pool_size: int = DEFAULT_POOL_SIZE) -> ConnectionPool:
    """
    获取全局连接池单例

    Args:
        db_path: 数据库文件路径
        pool_size: 连接池大小

    Returns:
        ConnectionPool: 全局连接池实例
    """
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = ConnectionPool(db_path=db_path, pool_size=pool_size)
    return _pool


def reset_pool():
    """重置全局连接池（主要用于测试）"""
    global _pool
    if _pool is not None:
        _pool.close_all()
        _pool = None