from flask import Flask
from .models import db
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.subjects import subjects_bp
from .routes.notes import notes_bp
from .routes.quizzes import quizzes_bp
from .routes.voice import voice_bp
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    db_path = os.path.join(app.instance_path, 'database.db')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key'),
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
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(voice_bp)
    
    # 首頁路由直接綁定在此處
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')
        
    return app
