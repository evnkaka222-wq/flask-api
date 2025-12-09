import pymysql

class Database:
    def __init__(self, host, user, password, database, port=3306):
        """初始化数据库连接参数"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            cursorclass=pymysql.cursors.DictCursor  # 返回字典格式
        )
        return self.connection
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
    
    def query(self, sql, params=None):
        """查询数据（SELECT）"""
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def execute(self, sql, params=None):
        """执行SQL（INSERT, UPDATE, DELETE）"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            self.connection.commit()
            affected_rows = cursor.rowcount  # 受影响的行数
            last_id = cursor.lastrowid  # 最后插入的ID（INSERT时有值，UPDATE/DELETE时为0）
            cursor.close()
            return {"affected_rows": affected_rows, "last_id": last_id}
        except Exception as e:
            self.connection.rollback()
            raise e