from flask import Blueprint, render_template, request, redirect, url_for

quizzes_bp = Blueprint('quizzes', __name__)

@quizzes_bp.route('/subjects/<int:subject_id>/quizzes', methods=['GET', 'POST'])
def subject_quizzes(subject_id):
    """
    科目測驗綜覽及產生器。
    GET: 渲染該科目過往各次測驗的清單 quizzes/index.html。
    POST: 透過呼叫 AI 分析此科目/筆記文檔並動態產生一份測驗考題，重導向至測驗答題畫面前。
    """
    pass

@quizzes_bp.route('/quizzes/<int:quiz_id>/take', methods=['GET'])
def take_quiz(quiz_id):
    """渲染 quizzes/take.html 表單，將剛出好的隨機題集拋至前端，供使用者進行實況作答。"""
    pass

@quizzes_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    """負責後台對測驗的評分，比對正解與答對選項並逐筆建入 QuestionResult，隨後重導向成績單頁。"""
    pass

@quizzes_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def quiz_detail(quiz_id):
    """成績單結算畫面，同時於 quizzes/detail.html 完整展示本次所有試題、錯題的詳解。"""
    pass
