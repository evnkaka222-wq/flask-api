from flask import jsonify
from datetime import datetime
import uuid

def success(data=None, message="操作成功", code=200):
    """成功响应"""
    response = {
        "code": code,
        "success": True,
        "message": message,
        "data": data,
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response), code

def error(message="操作失败", code=400, data=None):
    """错误响应"""
    response = {
        "code": code,
        "success": False,
        "message": message,
        "data": data,
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response), code