import os
import shutil
import sys

import pyfiglet
from flask import jsonify
from flask_cache import Cache
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from wtforms import ValidationError

import app_config as conf
from common.constants.response_code import ResponseCode


# 全局Utils
class AppUtils:

    @staticmethod
    def init(flask_app):
        # 增加CORS跨域支持
        CORS(flask_app)
        # APP Server Banner
        print(pyfiglet.figlet_format("Kingtous Web"))
        print("Web Exp By Kingtous")
        # 初始化secret_key
        flask_app.config['SECRET_KEY'] = conf.secret_key
        # 防范CSRF攻击
        flask_app.config["CSRF_ENABLED"] = True
        # 初始化数据库
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = conf.base_mysql_connection_url
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        flask_app.config["SQLALCHEMY_ECHO"] = False
        db = SQLAlchemy(flask_app)
        conf.database = db
        conf.SQLBase = declarative_base()
        conf.SQLEngine = create_engine(conf.base_mysql_connection_url,
                                       pool_recycle=7200,
                                       pool_size=100,
                                       echo=False)
        conf.SQLSessionMaker = sessionmaker(bind=conf.SQLEngine)
        conf.SQLSession = scoped_session(conf.SQLSessionMaker)  # scoped_session保证线程安全
        # 必须import database_models初始化数据库各类!
        import models.models
        try:
            conf.database.create_all()
        except Exception as e:
            sys.stderr.write('Database Connect Error: %s\n' % e.args[0])
            exit(0)

        # 未登录回调
        @conf.auth.error_handler
        def unauthorized():
            return jsonify(code=ResponseCode.LOGIN_REQUIRED)

        # 启动缓存
        # TODO simple只是用dict保存，后期使用redis替换
        conf.cache = Cache(flask_app, config={'CACHE_TYPE': 'simple'})
        # 初始化完成，回调
        AppUtils.on_init_success(flask_app)

    # 初始化成功
    @staticmethod
    def on_init_success(flask_app):
        with flask_app.app_context():
            # message = Message(subject='Code Running Server服务变更',
            #                   recipients=['kingtous@qq.com'],
            #                   body='服务已启动通知')
            # Cf.mail_manager.send(message)
            # print("已发送测试邮件")
            pass

    @staticmethod
    def get_network_url(local_url):
        return local_url.replace(os.path.dirname(__file__), conf.base_url)

    @staticmethod
    def get_local_path(network_url):
        return network_url.replace(conf.base_url, os.path.dirname(__file__))

    @staticmethod
    def validate_username(username):
        from models.models import User
        session = AppUtils.get_session()
        user = session.query(User).filter_by(username=username).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def serialize(model):
        from sqlalchemy.orm import class_mapper
        columns = [c.key for c in class_mapper(model.__class__).columns]
        return dict((c, getattr(model, c)) for c in columns)

    @staticmethod
    def get_session() -> Session:
        return conf.SQLSession()

    @staticmethod
    def copy_file(src, dst):
        try:
            shutil.copyfile(src, dst)
            return dst
        except IOError:
            return None
