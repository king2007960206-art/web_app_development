from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.subject import Subject
from app.models.quiz import Quiz, QuestionResult
from app.services.ai_service import generate_quiz

quizzes_bp = Blueprint('quizzes', __name__)

@quizzes_bp.before_request
def require_login():
    if 'user_id' not in session:
        flash('請先登入！', 'warning')
        return redirect(url_for('auth.login'))

@quizzes_bp.route('/subjects/<int:subject_id>/quizzes', methods=['GET', 'POST'])
def subject_quizzes(subject_id):
    """
    科目測驗綜覽及產生器。
    GET: 渲染該科目過往各次測驗的清單 quizzes/index.html。
    POST: 透過呼叫 AI 分析此科目/筆記文檔並動態產生一份測驗考題，重導向至測驗答題畫面前。
    """
    subject = Subject.get_by_id(subject_id)
    if not subject or subject.user_id != session['user_id']:
        return redirect(url_for('subjects.index'))
        
    if request.method == 'POST':
        note_id = request.form.get('note_id')
        title = f"自動產生的測驗 ({subject.name})"
        
        # 為了開發初期不會被 API 阻擋進度，實作 Dummy 回傳值供測試。實作 AI 後應移除。
        questions_data = generate_quiz("dummy reference material", num_questions=2)
        if not questions_data:
            questions_data = [
                {"question": "太陽從哪個方向升起？", "correct": "東邊", "explanation": "地球由西向東自轉因此為東邊。"},
                {"question": "Python 的 dict 屬於何種結構？", "correct": "雜湊表 (Hash Map)", "explanation": "Dict 的底層是 Hash 表格設計。"}
            ]
            
        quiz = Quiz.create(subject_id=subject.id, title=title, note_id=note_id if note_id else None, score=0)
        
        if quiz:
            # 建立測驗關聯的試題集
            for q in questions_data:
                QuestionResult.create(
                    quiz_id=quiz.id, 
                    question_text=q['question'], 
                    correct_answer=q['correct'], 
                    is_correct=False, 
                    explanation=q['explanation']
                )
            return redirect(url_for('quizzes.take_quiz', quiz_id=quiz.id))
            
        flash('發生錯誤，無法建立該測驗！', 'error')
        return redirect(url_for('quizzes.subject_quizzes', subject_id=subject_id))
        
    quizzes = Quiz.query.filter_by(subject_id=subject_id).all()
    return render_template('quizzes/index.html', subject=subject, quizzes=quizzes)

@quizzes_bp.route('/quizzes/<int:quiz_id>/take', methods=['GET'])
def take_quiz(quiz_id):
    """渲染 quizzes/take.html 表單，將剛出好的隨機題集拋至前端，供使用者進行實況作答。"""
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz.subject.user_id != session['user_id']:
        return redirect(url_for('dashboard.index'))
        
    return render_template('quizzes/take.html', quiz=quiz)

@quizzes_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    """負責後台對測驗的評分，比對正解與答對選項並逐筆建入 QuestionResult，隨後重導向成績單頁。"""
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz.subject.user_id != session['user_id']:
        return redirect(url_for('dashboard.index'))
        
    correct_count = 0
    total = len(quiz.questions)
    
    # 計算分數與填入各題結果
    for q in quiz.questions:
        # 表單欄位採用 q_ID 做識別
        ans_input = request.form.get(f'q_{q.id}', '')
        is_correct = (ans_input.strip().lower() == q.correct_answer.strip().lower())
        
        if is_correct:
            correct_count += 1
            
        q.update(user_answer=ans_input, is_correct=is_correct)
        
    score = int((correct_count / total) * 100) if total > 0 else 0
    quiz.update(score=score)
    
    flash(f'交卷成功！您的測驗得分為 {score} 分。', 'success')
    return redirect(url_for('quizzes.quiz_detail', quiz_id=quiz.id))

@quizzes_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def quiz_detail(quiz_id):
    """成績單結算畫面，同時於 quizzes/detail.html 完整展示本次所有試題、錯題的詳解。"""
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz.subject.user_id != session['user_id']:
        return redirect(url_for('dashboard.index'))
        
    return render_template('quizzes/detail.html', quiz=quiz)
