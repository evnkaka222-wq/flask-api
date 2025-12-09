from flask import Blueprint, request
from marshmallow import ValidationError
from utils.database import Database
from utils.schemas import LoginSchema
from utils.response import success, error
from utils.jwt_utils import generate_token,generate_refresh_token,verify_token
from config import DB_CONFIG

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

db = Database(**DB_CONFIG)
db.connect()

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    # 验证数据
    schema = LoginSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return error(message=err.messages)
    
    username = validated_data['username']
    password = validated_data['password']
    
    # 查询用户
    sql = "SELECT id, name,password FROM users WHERE name = %s"
    users = db.query(sql, (username,))
    
    if not users:
       return error(message="用户名或密码错误", code=401)
    
    user = users[0]
    
    # 验证密码（这里简单比对，实际应该用加密）
    if user['password'] != password:
       return error(message="用户名或密码错误", code=401)
    
    # ✅ 生成两种 token
    access_token = generate_token(user['id'], user['name'])
    refresh_token = generate_refresh_token(user['id'], user['name'])
    
    return success(
        data={
            'access_token': access_token,      # ✅ 短期 token
            'refresh_token': refresh_token,    # ✅ 长期 token
            'user_id': user['id'],
            'username': user['name']
        },
        message="登录成功"
    )

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """✅ 刷新 Access Token"""
    data = request.get_json()
    
    if not data or 'refresh_token' not in data:
        return error(message="缺少 refresh_token", code=400)
    
    refresh_token = data['refresh_token']
    
    # 验证 refresh token
    payload = verify_token(refresh_token, token_type='refresh')
    
    if not payload:
        return error(message="无效或过期的 refresh token", code=401)
    
    # 生成新的 access token
    new_access_token = generate_token(payload['user_id'], payload['username'])
    
    return success(
        data={
            'access_token': new_access_token,
            'user_id': payload['user_id'],
            'username': payload['username']
        },
        message="Token 刷新成功"
    )