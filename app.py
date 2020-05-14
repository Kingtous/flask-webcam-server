import os

# 导入环境变量
from dotenv import load_dotenv

# 必须先导入环境变量
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)  # override=True: 覆写已存在的变量

from flask import Flask

from app_utils import AppUtils

from views.index import index_bp


def set_up_views(app: Flask):
    app.register_blueprint(index_bp)


#
def create_app():
    # 配置 pywsgi
    # dapp = DebuggedApplication(app, evalex=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), dapp)
    # server.serve_forever()
    # 运行 flask
    # 猴子补丁，增加并发

    # monkey.patch_all()

    # 生成app
    app = Flask(__name__)
    # 配置views
    set_up_views(app)
    # 初始化APP
    AppUtils.init(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=True,
        use_reloader=True,
        host="0.0.0.0",
        port=80
    )
