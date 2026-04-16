from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.subject import Subject

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')

@subjects_bp.before_request
def require_login():
    if 'user_id' not in session:
        flash('請先登入！', 'warning')
        return redirect(url_for('auth.login'))

@subjects_bp.route('/', methods=['GET', 'POST'])
def index():
    """
    處理科目列表檢視與建立。
    GET: 透過關聯 user_id，查詢並渲染 subjects/index.html 顯示所有科目。
    POST: 接收新科目資訊，寫入 DB 後重導向回列表頁。
    """
    user_id = session['user_id']
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        if not name:
            flash('科目名稱為必填！', 'error')
            return redirect(url_for('subjects.index'))
            
        subject = Subject.create(user_id, name, description)
        if subject:
            flash('科目新增成功！', 'success')
        else:
            flash('新增失敗！', 'error')
        return redirect(url_for('subjects.index'))
        
    subjects = Subject.get_all_by_user(user_id)
    return render_template('subjects/index.html', subjects=subjects)

@subjects_bp.route('/new', methods=['GET'])
def new():
    """渲染 subjects/new.html 顯示新增自訂科目的表單介面。"""
    return render_template('subjects/new.html')

@subjects_bp.route('/<int:subject_id>/delete', methods=['POST'])
def delete(subject_id):
    """刪除指定科目"""
    subject = Subject.get_by_id(subject_id)
    if subject and subject.user_id == session['user_id']:
        subject.delete()
        flash('科目已刪除！', 'success')
    else:
        flash('無權限或找不到科目！', 'error')
    return redirect(url_for('subjects.index'))
