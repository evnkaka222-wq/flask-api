from dotenv import load_dotenv
import os

# 🔥 加载 .env 文件
load_dotenv()

from flask import Flask,request
from utils.database import Database
from config import DB_CONFIG
from routes.user import user_bp
from utils.error_handler import register_error_handlers
from routes.auth import auth_bp  # JWT鉴权
from flask_cors import CORS 

app = Flask(__name__)

# CORS 配置
CORS(app)

# 创建数据库实例
db = Database(**DB_CONFIG)
db.connect()

# 在所有响应后添加 CORS 头（最保险的方法）
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ['http://localhost:5173', 'http://127.0.0.1:5173']:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRF-Token'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '3600'
    return response

# 处理 OPTIONS 预检请求
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'http://127.0.0.1:5173']:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRF-Token'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '3600'
        return response

# 注册错误处理
register_error_handlers(app)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)