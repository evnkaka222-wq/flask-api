from flask import jsonify
from marshmallow import ValidationError

def register_error_handlers(app):
    """注册全局错误处理"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """400错误"""
        return jsonify({
            'status': 'error',
            'message': '请求参数错误'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """404错误"""
        return jsonify({
            'status': 'error',
            'message': '资源不存在'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误"""
        return jsonify({
            'status': 'error',
            'message': '服务器内部错误'
        }), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        """数据验证错误"""
        return jsonify({
            'status': 'error',
            'message': error.messages
        }), 400
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """捕获所有未处理的异常"""
        return jsonify({
            'status': 'error',
            'message': str(error)
        }), 500