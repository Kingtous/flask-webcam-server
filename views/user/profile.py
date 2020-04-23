import time

from flask import request, g
from flask_restful import Resource

from app_config import auth
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode
from models.models import User


# 修改资料,只能改昵称和头像
class AlterProfile(Resource):

    @auth.login_required
    def post(self):
        field = request.json.get("field", None)
        value = request.json.get("value", None)
        if field is not None and value is not None:
            user = g.user  # 需要重新查找，这个User未绑定sql，无法更新
            session = AppUtils.get_session()
            user = session.query(User).filter_by(id=user.id).first()
            try:
                if field == "nickname":
                    user.nickname = value
                    session.commit()
                    return ResponseClass.ok()
                elif field == "avatar_url":
                    user.avatar_url = value
                    session.commit()
                    return ResponseClass.ok()
            finally:
                session.close()

        return ResponseClass.warn(ResponseCode.FORMAT_ERROR)


# 获取统计数据
class UserStatistic(Resource):

    @auth.login_required
    def get(self, id):
        session = AppUtils.get_session()
        try:
            user = g.user
            if user.id != id:
                # 查询他人的信息
                query_user = session.query(User).filter_by(id=id).first()
                return ResponseClass.ok_with_data(
                    query_user.get_minimal_data()) if query_user is not None else ResponseClass.warn(
                    ResponseCode.USER_NOT_EXIST)
            else:
                ResponseClass.ok_with_data(user.get_self_data())
        finally:
            session.close()


# 资料页点赞
class UserLikeApi(Resource):

    @auth.login_required
    def get(self, user_id):
        t1 = time.clock()
        session = AppUtils.get_session()
        try:
            from models.models import User
            q_user = session.query(User).filter_by(id=user_id).with_for_update().first()
            if q_user is None:
                return ResponseClass.warn(ResponseCode.USER_NOT_EXIST)
            else:
                # 判断是否点过赞，点过赞则警告
                from models.models import UserLikes
                result = session.query(UserLikes).filter_by(user_id=g.user.id,
                                                            like_user=user_id).with_for_update().first()
                if result is None:
                    # 点赞
                    q_user.likes += 1
                    likes = UserLikes()
                    likes.user_id = g.user.id
                    likes.like_user = user_id
                    session.add(likes)
                    return ResponseClass.ok()
                else:
                    # TODO 测试并发量
                    q_user.likes += 1
                    return ResponseClass.warn(ResponseCode.ALREADY_LIKED)
        finally:
            session.commit()
            print("请求时间：%f" % (time.clock() - t1))
            session.close()
