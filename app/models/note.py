import logging
from datetime import datetime
from . import db

logger = logging.getLogger(__name__)

class Note(db.Model):
    __tablename__ = 'note'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    original_content = db.Column(db.Text)
    ai_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    quizzes = db.relationship('Quiz', backref='note', lazy=True)
    
    @classmethod
    def create(cls, subject_id, title, original_content=None, ai_summary=None):
        """新增一筆筆記記錄"""
        try:
            note = cls(subject_id=subject_id, title=title, original_content=original_content, ai_summary=ai_summary)
            db.session.add(note)
            db.session.commit()
            return note
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating note: {e}")
            return None
            
    @classmethod
    def get_all(cls):
        """取得所有筆記記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"Error getting all notes: {e}")
            return []
            
    @classmethod
    def get_by_id(cls, note_id):
        """取得單筆筆記記錄"""
        try:
            return cls.query.get(note_id)
        except Exception as e:
            logger.error(f"Error getting note by id: {e}")
            return None
            
    @classmethod
    def get_all_by_subject(cls, subject_id):
        """取得隸屬特定科目的所有筆記"""
        try:
            return cls.query.filter_by(subject_id=subject_id).all()
        except Exception as e:
            logger.error(f"Error getting notes by subject: {e}")
            return []
            
    def update(self, **kwargs):
        """更新筆記記錄"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating note: {e}")
            return False
            
    def delete(self):
        """刪除筆記記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting note: {e}")
            return False
