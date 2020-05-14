import os

# 导入环境变量
from dotenv import load_dotenv

# 必须先导入环境变量
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)  # override=True: 覆写已存在的变量

from flask import Flask
from gevent import pywsgi, monkey

monkey.patch_all()

from app_utils import AppUtils

from views.index import index_bp


def set_up_views(app: Flask):
    app.register_blueprint(index_bp)


#
def create_app():

    # 生成app
    app = Flask(__name__)
    # 配置views
    set_up_views(app)
    # 初始化APP
    AppUtils.init(app)

    return app


if __name__ == '__main__':
    # 配置 pywsgi
    app = create_app()
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()