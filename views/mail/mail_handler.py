#  Copyright (C) <2020> Kingtous
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#   rights to use,copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#   and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#  　　
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.

#
from random import randrange

from flask import request
from flask_mail import Message
from flask_restful import Resource

import app_config as conf
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode
from models.models import User


class RegisterMail(Resource):

    def post(self):
        email = request.json.get("email", None)
        if email is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        self.send_reset_password_mail(email)
        return ResponseClass.ok()

    def send_reset_password_mail(self, email: str) -> bool:
        try:
            code: str = conf.cache.get(email)
            if code is None:
                code = self.gen_number_codes()
                while conf.cache.get(code) is not None:
                    # 不能使用相同的code在缓存中
                    code = self.gen_number_codes()
            # 不发送重复验证码
            conf.cache.add(email, code, timeout=600)
            # 放入cache
            conf.cache.add(code, email, timeout=600)
            message = Message(
                subject='《Web 实验》注册邮件',
                recipients=[email],
                body='您的注册验证码为：' + code + '，请在10分钟内使用，感谢支持！'
            )
            conf.mail_manager.send(
                message
            )
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def gen_number_codes() -> str:
        code_str = ''
        for i in range(6):
            code_str += str(randrange(0, 10))
        return code_str


class MailHandler(Resource):

    def post(self):
        username = request.json.get("username", None)
        if username is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        try:
            user: User = session.query(User).filter_by(username=username).first()
            if user is None:
                user = session.query(User).filter_by(mail=username).first()
            if user is None:
                return ResponseClass.warn(ResponseCode.USER_NOT_EXIST)
            else:
                # 发送邮件
                if self.send_reset_password_mail(user):
                    return ResponseClass.ok()
                else:
                    # 没发出去，服务器错误
                    return ResponseClass.warn(ResponseCode.SERVER_ERROR)
        finally:
            session.close()

    def send_reset_password_mail(self, user: User) -> bool:
        try:
            code: str = conf.cache.get(user.id)
            if code is None:
                code = self.gen_number_codes()
                while conf.cache.get(code) is not None:
                    # 不能使用相同的code在缓存中
                    code = self.gen_number_codes()
            # 不发送重复验证码
            conf.cache.add(user.id, code, timeout=600)
            # 放入cache
            conf.cache.add(code, user.id, timeout=600)
            message = Message(
                subject='《Web 实验》重置密码邮件',
                recipients=[user.mail],
                body='用户' + user.username + '，您的验证码为：' + code + '，请在10分钟内使用，感谢支持！'
            )
            conf.mail_manager.send(
                message
            )
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def gen_number_codes() -> str:
        code_str = ''
        for i in range(6):
            code_str += str(randrange(0, 10))
        return code_str
