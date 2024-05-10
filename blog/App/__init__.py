# __init__.py ：初始化文件，创建Flask应用

from flask import Flask
from .views.views import blog
from .exts import init_exts
from .views.views_admin import admin

def create_app():
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(blueprint=blog) #前端页面
    app.register_blueprint(blueprint=admin) #后台管理

    # 配置数据库

    db_uri = 'mysql+pymysql://root:123456@localhost:3306/blogdb'  # mysql的配置
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止对象追踪修改

    # 初始化插件
    init_exts(app=app)

    return app

