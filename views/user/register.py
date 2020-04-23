from flask import request, jsonify
from flask_restful import Resource

from app_config import cache
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode


class Register(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        code = request.json.get('code', None)
        mail = request.json.get('mail', None)
        if username is None or password is None or code is None or mail is None or not re.match(
                r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+', mail):
            return jsonify(code=ResponseCode.FORMAT_ERROR, msg="用户名密码格式错误")
        cache_email = cache.get(code)
        if cache_email != mail:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        else:
            cache.delete(code)
            cache.delete(mail)
        session = AppUtils.get_session()
        try:
            # 验证用户名
            AppUtils.validate_username(username)
            from models.models import User
            user = User()
            user.username = username
            user.mail = mail
            user.hash_password(password)
            user.credits = 0
            session.add(user)
            session.commit()
            # 数据库
            from app_config import SQLSession
            return jsonify(code=0, data=user.get_self_data())
        except Exception as e:
            return jsonify(code=-1, msg=e.args[0])
        finally:
            session.close()
