from functools import wraps
from flask import request
from utils.response import error
from utils.jwt_utils import verify_token

def token_required(f):
    """JWT认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取token
        token = request.headers.get('Authorization')
        
        if not token:
            return error(message="缺少token，请先登录", code=401)
        
        # 去掉 "Bearer " 前缀（如果有）
        if token.startswith('Bearer '):
            token = token[7:]
        
        # 验证token
        payload = verify_token(token,token_type='access')
        
        if not payload:
            return error(message="token无效或已过期，请重新登录", code=401)
        
        # 将用户信息传递给接口
        kwargs['current_user'] = payload
        
        return f(payload,*args, **kwargs)
    
    return decorated_function