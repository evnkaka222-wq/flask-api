import os
from dotenv import load_dotenv

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST','localhost'),      # 数据库地址
    'user': os.getenv('DB_USER','root'),           # 数据库用户名
    'password': os.getenv('DB_PASSWORD',''),  # 数据库密码
    'database': os.getenv('DB_DATABASE','mydb'),  # 数据库名
    'port': int(os.getenv('DB_PORT','3306')),              # 端口号
    'max_connections': int(os.getenv('DB_MAX_CONNECTIONS','10')),  # 池最大连接数
    'min_connections': int(os.getenv('DB_MIN_CONNECTIONS','2'))    # 池最小连接数
}

# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY','dev-secret-key') # JWT密钥
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS','24')) # token过期时间
REFRESH_TOKEN_EXPIRATION_DAYS = 7 # refresh_token过期时间