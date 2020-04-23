from flask import request, jsonify
from flask_restful import Resource

from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode
from models.models import User


class Login(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username is None or password is None:
            return jsonify(code=ResponseCode.FORMAT_ERROR)
        # 查找用户
        session = AppUtils.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                user = session.query(User).filter_by(mail=username).first()
            if user is None:
                return jsonify(code=ResponseCode.USER_NOT_EXIST)
            if not user.verify_password_only(password):
                return jsonify(code=ResponseCode.PASSWORD_ERROR)
            # 用户验证成功
            return ResponseClass.ok_with_data(
                user.get_self_data()
            )
        finally:
            session.close()
