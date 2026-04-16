import logging
from datetime import datetime
from . import db

logger = logging.getLogger(__name__)

class Subject(db.Model):
    __tablename__ = 'subject'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    notes = db.relationship('Note', backref='subject', lazy=True, cascade="all, delete-orphan")
    quizzes = db.relationship('Quiz', backref='subject', lazy=True, cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, user_id, name, description=None):
        """新增一筆科目記錄"""
        try:
            subject = cls(user_id=user_id, name=name, description=description)
            db.session.add(subject)
            db.session.commit()
            return subject
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating subject: {e}")
            return None
            
    @classmethod
    def get_all(cls):
        """取得所有科目記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"Error getting all subjects: {e}")
            return []
            
    @classmethod
    def get_by_id(cls, subject_id):
        """取得單筆科目記錄"""
        try:
            return cls.query.get(subject_id)
        except Exception as e:
            logger.error(f"Error getting subject by id: {e}")
            return None
            
    @classmethod
    def get_all_by_user(cls, user_id):
        """取得特定使用者的所有科目"""
        try:
            return cls.query.filter_by(user_id=user_id).all()
        except Exception as e:
            logger.error(f"Error getting subjects by user: {e}")
            return []
            
    def update(self, **kwargs):
        """更新科目記錄"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating subject: {e}")
            return False
            
    def delete(self):
        """刪除科目記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting subject: {e}")
            return False
