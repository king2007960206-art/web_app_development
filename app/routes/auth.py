from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染 auth/register.html 顯示表單。
    POST: 接收表單資源，雜湊密碼並建立新 User，成功後重導向至登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染 auth/login.html 顯示表單。
    POST: 驗證帳密並將狀態寫入 session，成功後重導向至 dashboard 主控台。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """清除 session 中的登入狀態並重導向至首頁。"""
    pass
