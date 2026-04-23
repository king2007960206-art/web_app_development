from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入與密碼解鎖。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請輸入帳號與密碼！', 'warning')
            return redirect(url_for('auth.login'))
            
        user = User.get_by_username(username)
        if user:
            # 帳號存在，檢查密碼
            if check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                flash('登入成功！', 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('密碼錯誤，請重試。', 'danger')
        else:
            # 找不到帳號，為了測試方便，直接幫他註冊
            hashed_pw = generate_password_hash(password)
            new_user = User.create(username=username, password_hash=hashed_pw)
            session['user_id'] = new_user.id
            flash('找不到此帳號，已自動為您註冊並登入！', 'success')
            return redirect(url_for('dashboard.index'))
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    處理使用者登出。
    """
    session.pop('user_id', None)
    flash('您已成功登出。', 'info')
    return redirect(url_for('auth.login'))
