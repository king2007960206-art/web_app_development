from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.subject import Subject
from app.models.quiz import Quiz

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.before_request
def require_login():
    """保護所有 dashboard 下的路由不被未授權者存取"""
    if 'user_id' not in session:
        flash('請先登入！', 'warning')
        return redirect(url_for('auth.login'))

@dashboard_bp.route('/', methods=['GET'])
def index():
    """
    顯示學習主控台。
    渲染 dashboard/index.html，包含總學習時數與近期測驗正確率之儀表板。
    """
    user_id = session['user_id']
    subjects = Subject.get_all_by_user(user_id)
    return render_template('dashboard/index.html', subjects=subjects)

@dashboard_bp.route('/weaknesses', methods=['GET'])
def weaknesses():
    """
    顯示弱點分析結果 (錯題本)。
    收集並過濾 QuestionResult 中 is_correct=False 的資料，渲染至 dashboard/weaknesses.html。
    """
    user_id = session['user_id']
    subjects = Subject.get_all_by_user(user_id)
    
    wrong_answers = []
    for sub in subjects:
        for quiz in sub.quizzes:
            for q in quiz.questions:
                if not q.is_correct:
                    wrong_answers.append({
                        'subject': sub.name,
                        'quiz_title': quiz.title,
                        'question': q.question_text,
                        'your_answer': q.user_answer,
                        'correct_answer': q.correct_answer,
                        'explanation': q.explanation
                    })
    
    return render_template('dashboard/weaknesses.html', wrong_answers=wrong_answers)
