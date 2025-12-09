import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY, JWT_EXPIRATION_HOURS,REFRESH_TOKEN_EXPIRATION_DAYS

def generate_token(user_id, username):
    """生成 Access Token（短期）"""
    payload = {
        'user_id': user_id,
        'username': username,
        'type': 'access',  # ✅ 确保有这一行
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),  # 过期时间
        'iat': datetime.utcnow()  # 签发时间
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def generate_refresh_token(user_id, username):
    """生成 Refresh Token（长期）"""
    payload = {
        'user_id': user_id,
        'username': username,
        'type': 'refresh',  # 标记为 refresh token
        'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token, token_type='access'):
    """验证JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

        # ✅ 验证 token 类型
        if payload.get('type') != token_type:
            return None
        
        return payload  # 返回用户信息
    except jwt.ExpiredSignatureError:
        return None  # token过期
    except jwt.InvalidTokenError:
        return None  # token无效