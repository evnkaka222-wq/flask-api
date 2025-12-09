import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY, JWT_EXPIRATION_HOURS

def generate_token(user_id, username):
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),  # 过期时间
        'iat': datetime.utcnow()  # 签发时间
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """验证JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload  # 返回用户信息
    except jwt.ExpiredSignatureError:
        return None  # token过期
    except jwt.InvalidTokenError:
        return None  # token无效