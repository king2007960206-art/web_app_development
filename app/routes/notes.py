from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.subject import Subject
from app.models.note import Note
from app.services.ai_service import generate_note_summary

notes_bp = Blueprint('notes', __name__)

@notes_bp.before_request
def require_login():
    if 'user_id' not in session:
        flash('請先登入！', 'warning')
        return redirect(url_for('auth.login'))

@notes_bp.route('/subjects/<int:subject_id>/notes', methods=['GET'])
def list_notes(subject_id):
    """取得且顯示位於特定 subject 內的筆記列表，渲染 notes/index.html。"""
    subject = Subject.get_by_id(subject_id)
    if not subject or subject.user_id != session['user_id']:
        flash('找不到該科目或無權限。', 'error')
        return redirect(url_for('subjects.index'))
        
    notes = Note.get_all_by_subject(subject_id)
    return render_template('notes/index.html', subject=subject, notes=notes)

@notes_bp.route('/subjects/<int:subject_id>/notes/upload', methods=['GET', 'POST'])
def upload_note(subject_id):
    """
    上傳新講義並自動讓 AI 產生摘要。
    GET: 渲染 files 上傳表單 notes/upload.html。
    POST: 解析文件內容、呼叫 AI 生成摘要並存為 Note Model 紀錄，完成後重導向單筆筆記讀取頁。
    """
    subject = Subject.get_by_id(subject_id)
    if not subject or subject.user_id != session['user_id']:
        return redirect(url_for('subjects.index'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        # 在 MVP 中，我們讓使用者直接貼上長文來暫代 PDF 文件解析，較為穩健
        content = request.form.get('content')
        
        if not title or not content:
            flash('標題與內文不能留白！', 'error')
            return redirect(url_for('notes.upload_note', subject_id=subject_id))
            
        ai_summary = generate_note_summary(content)
        if not ai_summary:
            # 加入替換防呆
            ai_summary = "目前 AI 暫時無法產出摘要，請您稍後再試或是聯絡管理員。"
            
        note = Note.create(subject_id, title, content, ai_summary)
        if note:
            flash('筆記與摘要建立成功！', 'success')
            return redirect(url_for('notes.note_detail', note_id=note.id))
        else:
            flash('伺服器發生異常，無法儲存筆記。', 'error')
            return redirect(url_for('notes.list_notes', subject_id=subject_id))

    return render_template('notes/upload.html', subject=subject)

@notes_bp.route('/notes/<int:note_id>', methods=['GET'])
def note_detail(note_id):
    """閱讀單獨的筆記細節以及自動化擷取的段落結構，渲染 notes/detail.html。"""
    note = Note.get_by_id(note_id)
    if not note or note.subject.user_id != session['user_id']:
        flash('找不到該篇筆記或是您無權存取。', 'error')
        return redirect(url_for('dashboard.index'))
        
    return render_template('notes/detail.html', note=note)

@notes_bp.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """刪除筆記"""
    note = Note.get_by_id(note_id)
    if note and note.subject.user_id == session['user_id']:
        subject_id = note.subject_id
        note.delete()
        flash('筆記刪除成功！', 'success')
        return redirect(url_for('notes.list_notes', subject_id=subject_id))
    return redirect(url_for('dashboard.index'))
