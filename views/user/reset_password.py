from flask import request
from flask_restful import Resource

from app_config import cache
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode
from models.models import User


class UserResetPassword(Resource):

    def post(self):
        code = request.json.get('code', None)
        new_password = request.json.get('new_password', None)
        if code is None or new_password is None or not User.password_illigal(new_password):
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        else:
            user_id = cache.get(code)
            if user_id is None:
                return ResponseClass.warn(ResponseCode.SERVER_FORBIDDEN)
            session = AppUtils.get_session()
            try:
                user = session.query(User).filter_by(id=user_id).first()
                if user is None:
                    return ResponseClass.warn(ResponseCode.USER_NOT_EXIST)
                user.hash_password(new_password)
                session.commit()
                cache.delete(code)
                cache.delete(user_id)
                return ResponseClass.ok_with_data(user.get_self_data())
            finally:
                session.close()
