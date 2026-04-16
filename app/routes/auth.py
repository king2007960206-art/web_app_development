from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染 auth/register.html 顯示表單。
    POST: 接收表單資源，雜湊密碼並建立新 User，成功後重導向至登入頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('所有欄位皆為必填！', 'error')
            return redirect(url_for('auth.register'))
            
        if User.get_by_email(email):
            flash('此信箱已被註冊！', 'error')
            return redirect(url_for('auth.register'))
            
        hashed = generate_password_hash(password)
        new_user = User.create(username, email, hashed)
        
        if new_user:
            flash('註冊成功，請登入！', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('系統發生錯誤導致註冊失敗', 'error')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染 auth/login.html 顯示表單。
    POST: 驗證帳密並將狀態寫入 session，成功後重導向至 dashboard 主控台。
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('請輸入信箱與密碼！', 'error')
            return redirect(url_for('auth.login'))
            
        user = User.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            # 建立 session 驗證使用者的連線
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功！', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('信箱或密碼錯誤！', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """清除 session 中的登入狀態並重導向至首頁。"""
    session.clear()
    flash('您已登出。', 'info')
    return redirect(url_for('index'))
