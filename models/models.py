from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer

import app_config as conf

db = conf.database
auth = HTTPBasicAuth()

expiration = 3600
s = Serializer(conf.secret_key, expires_in=expiration)


# 用户表
class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(50), default="Fresh Coder")
    mail = db.Column(db.String(128), unique=True, nullable=False, index=True)
    avatar_url = db.Column(db.String(255),
                           default="http://hbimg.b0.upaiyun.com/5ecab4b5752dea92f62f472cdea1a387f806b43a85b7-4O5QSj_fw236")
    password_hash = db.Column(db.String(128))
    credits = Column(Integer, default=0)  # 积分
    likes = Column(Integer, default=0)  # 点赞数
    # TODO 职责
    role = Column(Integer, default=conf.USER_ROLE_USER)  # 职责

    @staticmethod
    def password_illigal(password):
        # TODO
        return True

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password_only(self, password):
        return pwd_context.verify(password, self.password_hash)

    def get_self_data(self):
        return {"id": self.id, "username": self.username, "token": self.generate_auth_token(), "credits": self.credits,
                "avatar_url": self.avatar_url, "nickname": self.nickname}

    # 用于其他访问的数据
    def get_minimal_data(self):
        return {"id": self.id, "username": self.username, "avatar_url": self.avatar_url, "nickname": self.nickname}

    @staticmethod
    @conf.auth.verify_password
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        # t1 = time.clock()
        user = User.verify_auth_token(username_or_token)
        if not user:
            # 现在不支持用户名密码登录，严重影响时间
            # try to authenticate with username/password
            # user = User.query.filter_by(username=username_or_token).first()
            # if not user or not user.verify_password_only(password):
            #     # print("鉴权花费：%f" % (time.clock() - t1))
            #     return False
            return False
        g.user = user
        # print("鉴权花费：%f" % (time.clock() - t1))
        return True

    def generate_auth_token(self):
        return s.dumps({'id': self.id, 'username': self.username}).decode()

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(conf.secret_key)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
