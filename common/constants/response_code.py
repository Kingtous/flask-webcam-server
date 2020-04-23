#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : response_code.py
# @Author: Kingtous
# @Date  : 2020-01-25
# @Desc  : 存储响应的Code类型
from flask import jsonify


class ResponseCode:
    # 正常返回
    NOT_ROOT = 1015  # 无权限
    NO_ENOUGH_CREDITS = 1014  # 没有足够的积分
    OPERATION_TOO_FAST = 1013  # 操作太快
    ITEM_NOT_FOUND = 1012  # 购物车物品不存在
    SERVER_FORBIDDEN = 1011  # 服务器拒绝
    ALREADY_LIKED = 1010  # 已经点过赞了
    COMMENT_NOT_FOUND = 1009  # 评论不存在
    ALREADY_SIGN_IN = 1008  # 已经签过到了
    THREAD_NOT_EXIST = 1007  # 帖子不存在
    USER_ALREADY_EXIST = 1004  # 用户名不可用
    OK_RESPONSE = 0  # 正常返回
    # 不正常的返回值
    LOGIN_REQUIRED = 1000  # 需要登录/token过期
    USER_NOT_EXIST = 1001  # 用户名不存在
    FORMAT_ERROR = 1002  # 格式错误
    PASSWORD_ERROR = 1003  # 密码错误
    SUBMIT_ERROR = 1004  # 提交错误
    FILE_NOT_EXIST = 1005  # 文件不存在
    SERVER_ERROR = 1006  # 服务器故障


class ResponseClass:

    @staticmethod
    def ok():
        return jsonify(code=ResponseCode.OK_RESPONSE)

    @staticmethod
    def ok_with_data(data):
        return jsonify(code=ResponseCode.OK_RESPONSE, data=data)

    @staticmethod
    def warn(code_int):
        return jsonify(code=code_int)
