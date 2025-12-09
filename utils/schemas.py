from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """用户登录数据验证模式"""
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class UserSchema(Schema):
    """用户数据验证模式"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    mobile = fields.Str(validate=validate.Regexp('^[0-9]+$'))
    userid = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class UserUpdateSchema(Schema):
    """用户更新数据验证模式（字段都是可选的）"""
    name = fields.Str(validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    mobile = fields.Str(validate=validate.Regexp('^[0-9]+$'))