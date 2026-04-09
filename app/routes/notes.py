from flask import Blueprint, render_template, request, redirect, url_for, flash

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/subjects/<int:subject_id>/notes', methods=['GET'])
def list_notes(subject_id):
    """取得且顯示位於特定 subject 內的筆記列表，渲染 notes/index.html。"""
    pass

@notes_bp.route('/subjects/<int:subject_id>/notes/upload', methods=['GET', 'POST'])
def upload_note(subject_id):
    """
    上傳新講義並自動讓 AI 產生摘要。
    GET: 渲染 files 上傳表單 notes/upload.html。
    POST: 解析文件內容、呼叫 AI 生成摘要並存為 Note Model 紀錄，完成後重導向單筆筆記讀取頁。
    """
    pass

@notes_bp.route('/notes/<int:note_id>', methods=['GET'])
def note_detail(note_id):
    """閱讀單獨的筆記細節以及自動化擷取的段落結構，渲染 notes/detail.html。"""
    pass
