# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : token.py
# @Author: Kingtous
# @Date  : 2020-01-23
# @Desc  : 用户登录注册


from flask import g
from flask_restful import Resource

from app_config import auth
from common.constants.response_code import ResponseClass


class GetToken(Resource):

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return ResponseClass.ok_with_data({'token': token})
