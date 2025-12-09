import pymysql
from dbutils.pooled_db import PooledDB
from contextlib import contextmanager

class Database:
    """数据库连接池管理类"""
    
    _pool = None  # 类级别的连接池（单例模式）
    
    def __init__(self, host, user, password, database, port=3306, 
                 max_connections=10, min_connections=2):
        """
        初始化数据库连接池
        
        Args:
            host: 数据库地址
            user: 用户名
            password: 密码
            database: 数据库名
            port: 端口
            max_connections: 最大连接数（默认10）
            min_connections: 最小连接数（默认2）
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        
        # ✅ 创建连接池（只创建一次）
        if Database._pool is None:
            Database._pool = PooledDB(
                creator=pymysql,          # 使用 pymysql
                maxconnections=max_connections,  # 最大连接数
                mincached=min_connections,       # 初始化时至少创建的空闲连接
                maxcached=5,              # 最多保留的空闲连接
                blocking=True,            # 连接池满时是否阻塞等待
                ping=1,                   # 连接前检查连接是否可用（0=不检查，1=默认检查，2=事务开始前检查）
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True           # 自动提交
            )
            print(f"✅ 数据库连接池已创建 (最小: {min_connections}, 最大: {max_connections})")
    
    def connect(self):
        """
        从连接池获取连接（兼容旧代码）
        
        Returns:
            connection: 数据库连接对象
        """
        return Database._pool.connection()
    
    @contextmanager
    def get_connection(self):
        """
        上下文管理器：自动获取和释放连接
        
        用法:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
        """
        conn = Database._pool.connection()
        try:
            yield conn
        finally:
            conn.close()  # 归还连接到池（不是真正关闭）
    
    def query(self, sql, params=None):
        """
        查询数据（SELECT）
        
        Args:
            sql: SQL 语句
            params: 参数（tuple 或 list）
        
        Returns:
            list: 查询结果（字典列表）
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall()
            cursor.close()
            return result
    
    def execute(self, sql, params=None):
        """
        执行 SQL（INSERT, UPDATE, DELETE）
        
        Args:
            sql: SQL 语句
            params: 参数（tuple 或 list）
        
        Returns:
            dict: {
                'affected_rows': int,  # 受影响的行数
                'last_id': int         # 最后插入的ID
            }
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, params)
                conn.commit()
                affected_rows = cursor.rowcount
                last_id = cursor.lastrowid
                cursor.close()
                return {
                    "affected_rows": affected_rows,
                    "last_id": last_id
                }
            except Exception as e:
                conn.rollback()
                cursor.close()
                raise e
    
    def execute_many(self, sql, params_list):
        """
        批量执行 SQL（提高性能）
        
        Args:
            sql: SQL 语句
            params_list: 参数列表 [(...), (...), ...]
        
        Returns:
            dict: {
                'affected_rows': int,
                'success': bool
            }
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.executemany(sql, params_list)
                conn.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return {
                    "affected_rows": affected_rows,
                    "success": True
                }
            except Exception as e:
                conn.rollback()
                cursor.close()
                raise e
    
    def transaction(self):
        """
        获取事务上下文管理器
        
        用法:
            with db.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(sql1)
                cursor.execute(sql2)
                # 自动 commit，出错自动 rollback
        """
        return self._transaction_context()
    
    @contextmanager
    def _transaction_context(self):
        """事务上下文管理器实现"""
        conn = Database._pool.connection()
        conn.autocommit(False)  # 关闭自动提交
        try:
            yield conn
            conn.commit()  # 提交事务
        except Exception as e:
            conn.rollback()  # 回滚事务
            raise e
        finally:
            conn.autocommit(True)  # 恢复自动提交
            conn.close()
    
    def close(self):
        """
        关闭连接池（通常不需要调用）
        """
        if Database._pool:
            Database._pool.close()
            Database._pool = None
            print("❌ 数据库连接池已关闭")
    
    @staticmethod
    def get_pool_status():
        """
        获取连接池状态（调试用）
        
        Returns:
            dict: 连接池统计信息
        """
        if Database._pool:
            return {
                "pool_exists": True,
                "message": "连接池运行中"
            }
        return {
            "pool_exists": False,
            "message": "连接池未初始化"
        }