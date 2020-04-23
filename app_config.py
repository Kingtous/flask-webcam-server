import os
from typing import Union

from flask_cache import Cache
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail
# 可执行二进制文件配置
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session

# 全局配置
base_url = os.environ.get("base_url")
base_mysql_connection_url = os.environ.get("base_mysql_connection_url")
upload_path = os.path.join(os.path.dirname(__file__), 'uploaded')
secret_key = os.environ.get("secret_key")
# 初始化全局变量
auth = HTTPBasicAuth()  # 可以同时支持token和用户名密码的认证
database: SQLAlchemy = Union[SQLAlchemy]
SQLBase: DeclarativeMeta = Union[DeclarativeMeta]
SQLEngine: Engine = Union[Engine]
SQLSessionMaker: sessionmaker = Union[sessionmaker]
SQLSession: scoped_session = Union[scoped_session]
# 邮件系统配置
mail_manager: Mail = Union[None, Mail]
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT: int = int(os.environ.get("MAIL_PORT"))
MAIL_USE_TLS: bool = True if os.environ.get("MAIL_USE_TLS") == 'True' else False
MAIL_USE_SSL: bool = True if os.environ.get("MAIL_USE_SSL") == 'True' else False
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
# 缓存
cache: Cache = Union[None, Cache]
# 用户role
USER_ROLE_USER = 0
USER_ROLE_ADMIN = 1
