from flask import Blueprint, jsonify, request
from utils.database import Database
from config import DB_CONFIG
from marshmallow import ValidationError
from utils.schemas import UserSchema,UserUpdateSchema
from utils.response import success, error
from utils.decorators import token_required

# 创建用户蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# 创建数据库实例
db = Database(**DB_CONFIG)
db.connect()

@user_bp.route('/list', methods=['GET'])
@token_required # 新增：需要token才能访问
def get_users(current_user): # 新增参数：可以获取当前登录用户信息
    """获取用户列表"""
    sql = "SELECT id,name FROM users where status = 1"
    users = db.query(sql)

    return success(data=users,message="获取用户列表成功")

@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required # 新增：需要token才能访问
def get_user(current_user,user_id):
    """获取单个用户"""
    sql = "SELECT * FROM users WHERE id = %s"
    user = db.query(sql, (user_id,))
    if user:
        return success(data=user[0],message="获取用户成功")
    return error(message="用户不存在")

@user_bp.route('/add', methods=['POST'])
@token_required # 新增：需要token才能访问
def add_user(current_user):
    """添加用户"""
    data = request.get_json()
    if not data:
        return error(message="没有提供数据")
    
    # 验证数据
    schema = UserSchema()
    try:
        validated_data = schema.load(data)  # 验证并返回合法数据
    except ValidationError as err:
        return error(message=err.messages)
    
    # 动态构建SQL
    fields = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    values = tuple(data.values())
    
    sql = f"INSERT INTO users ({fields}) VALUES ({placeholders})"
    result = db.execute(sql, values)

    # 验证是否插入成功
    if result['affected_rows'] > 0:
        # 获取新增的id
        return success(
            data={"id": result['last_id']}, 
            message="用户添加成功"
        )
    else:
        return error(message="用户添加失败", code=500)

@user_bp.route('/update/<int:user_id>', methods=['PUT'])
@token_required # 新增：需要token才能访问
def update_user(current_user,user_id):
    """更新用户"""
    data = request.get_json()
    if not data:
        return error(message="没有提供数据")
    
    # 验证数据
    schema = UserUpdateSchema()
    try:
        validated_data = schema.load(data)  # 验证并返回合法数据
    except ValidationError as err:
        return error(message=err.messages)
    
    # 查询数据是否存在
    sql = "SELECT * FROM users WHERE id = %s"
    user = db.query(sql, (user_id,))
    if not user:
        return error(message="用户不存在")
    
    # 动态构建SQL
    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key}=%s")
        values.append(value)
    
    # 添加user_id到参数列表
    values.append(user_id)
    
    sql = f"UPDATE users SET {', '.join(fields)} WHERE id=%s"
    result = db.execute(sql, tuple(values))

    if result['affected_rows'] > 0:
        return success(message="用户更新成功")
    else:
        return error(message="用户更新失败", code=500)

@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@token_required # 新增：需要token才能访问
def delete_user(current_user,user_id):
    """删除用户"""
    # 查询数据是否存在
    sql = "SELECT * FROM users WHERE id = %s"
    user = db.query(sql, (user_id,))
    if not user:
        return error(message="用户不存在")
    
    sql = "UPDATE users SET status = 7 WHERE id=%s"
    result = db.execute(sql, (user_id,))

    if result['affected_rows'] > 0:
        return success(message="用户删除成功")
    else:
        return error(message="用户删除失败", code=500)