from datetime import datetime
from . import db

class Quiz(db.Model):
    __tablename__ = 'quiz'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('QuestionResult', backref='quiz', lazy=True)
    
    @classmethod
    def create(cls, subject_id, title, note_id=None, score=0):
        quiz = cls(subject_id=subject_id, title=title, note_id=note_id, score=score)
        db.session.add(quiz)
        db.session.commit()
        return quiz
        
    @classmethod
    def get_by_id(cls, quiz_id):
        return cls.query.get(quiz_id)


class QuestionResult(db.Model):
    __tablename__ = 'question_result'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    user_answer = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    explanation = db.Column(db.Text)
    
    @classmethod
    def create(cls, quiz_id, question_text, correct_answer, is_correct, user_answer=None, explanation=None):
        qr = cls(
            quiz_id=quiz_id, 
            question_text=question_text, 
            correct_answer=correct_answer, 
            is_correct=is_correct, 
            user_answer=user_answer, 
            explanation=explanation
        )
        db.session.add(qr)
        db.session.commit()
        return qr
