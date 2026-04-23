from flask import Blueprint

# 匯入各個 Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .transaction import transaction_bp
from .report import report_bp
from .settings import settings_bp

def register_blueprints(app):
    """
    將所有的 Blueprint 註冊到 Flask app 中
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp) # 儀表板通常掛在根目錄
    app.register_blueprint(transaction_bp, url_prefix='/transaction')
    app.register_blueprint(report_bp, url_prefix='/report')
    app.register_blueprint(settings_bp, url_prefix='/settings')
