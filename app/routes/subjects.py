from flask import Blueprint, render_template, request, redirect, url_for

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')

@subjects_bp.route('/', methods=['GET', 'POST'])
def index():
    """
    處理科目列表檢視與建立。
    GET: 透過關聯 user_id，查詢並渲染 subjects/index.html 顯示所有科目。
    POST: 接收新科目資訊，寫入 DB 後重導向回列表頁。
    """
    pass

@subjects_bp.route('/new', methods=['GET'])
def new():
    """渲染 subjects/new.html 顯示新增自訂科目的表單介面。"""
    pass
