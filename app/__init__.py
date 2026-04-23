from flask import Flask
from .models import db
from .routes import register_blueprints
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    db_path = os.path.join(app.instance_path, 'database.db')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key_for_accounting_book'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # 初始化 Plugins
    db.init_app(app)
    
    # 註冊 Blueprints
    register_blueprints(app)
    
    # 首頁路由直接重導向至儀表板或由 dashboard_bp 接管
    # 因為我們已經把 '/' 註冊在 dashboard_bp 了，所以這裡不需要再寫 @app.route('/')
        
    return app
