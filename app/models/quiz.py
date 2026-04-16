import logging
from datetime import datetime
from . import db

logger = logging.getLogger(__name__)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('QuestionResult', backref='quiz', lazy=True, cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, subject_id, title, note_id=None, score=None):
        """新增一筆測驗記錄"""
        try:
            quiz = cls(subject_id=subject_id, title=title, note_id=note_id, score=score)
            db.session.add(quiz)
            db.session.commit()
            return quiz
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating quiz: {e}")
            return None
            
    @classmethod
    def get_all(cls):
        """取得所有測驗記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"Error getting all quizzes: {e}")
            return []
            
    @classmethod
    def get_by_id(cls, quiz_id):
        """取得單筆測驗記錄"""
        try:
            return cls.query.get(quiz_id)
        except Exception as e:
            logger.error(f"Error getting quiz by id: {e}")
            return None
            
    def update(self, **kwargs):
        """更新測驗記錄"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating quiz: {e}")
            return False
            
    def delete(self):
        """刪除測驗記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting quiz: {e}")
            return False

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
        """新增一筆作答結果記錄"""
        try:
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
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating question result: {e}")
            return None
            
    @classmethod
    def get_all(cls):
        """取得所有作答結果記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"Error getting all question results: {e}")
            return []
            
    @classmethod
    def get_by_id(cls, qr_id):
        """取得單筆作答結果記錄"""
        try:
            return cls.query.get(qr_id)
        except Exception as e:
            logger.error(f"Error getting question result by id: {e}")
            return None
            
    def update(self, **kwargs):
        """更新作答結果記錄"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating question result: {e}")
            return False
            
    def delete(self):
        """刪除作答結果記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting question result: {e}")
            return False
