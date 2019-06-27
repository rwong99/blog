import os

from flask import Flask
from App.views import blue
from App.admin_views import blue2
from App.exts import init_exts

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def create_app():
    app = Flask(__name__)

    # 配置static和template
    # static_folder=os.path.join(BASE_DIR,'/blog/static')
    # template_folder=os.path.join(BASE_DIR,'/blog/templates')
    # app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

    # 配置数据库
    # mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pytest@localhost:3306/blog'
    # 可视化连接时Pycharm2019，URL添加时区：
    #  jdbc:mysql://localhost:3306/flaskdb?serverTimezone=UTC

    # 禁止‘追踪修改’
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 修改成开发环境
    app.config['ENV'] = 'development'

    # 配置session的 'SECRET_KEY'
    app.config['SECRET_KEY'] = "ace34de5678ba"

    # 注册蓝图
    app.register_blueprint(blue)
    app.register_blueprint(blue2)

    # 初始化插件
    init_exts(app)

    return app

