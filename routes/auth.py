from flask import Blueprint, request
from marshmallow import ValidationError
from utils.database import Database
from utils.schemas import LoginSchema
from utils.response import success, error
from utils.jwt_utils import generate_token
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
    # sql = "SELECT id, name FROM work_users_test WHERE name = %s"
    # users = db.query(sql, (username,))
    
    # if not users:
    #    return error(message="用户名或密码错误", code=401)
    
    # user = users[0]
    
    # 验证密码（这里简单比对，实际应该用加密）
    #if user['password'] != password:
    #    return error(message="用户名或密码错误", code=401)
    
    # 生成token
    # token = generate_token(user['id'], user['name'])

    if username != 'kaka' or password != 'kaka22_jj':
        return error(message="用户名或密码错误", code=401)
    user = {}
    user['id'] = 266
    user['name'] = 'kaka'
    token = generate_token(user['id'], user['name'])
    
    return success(
        data={
            'token': token,
            'user_id': user['id'],
            'username': user['name']
        },
        message="登录成功"
    )