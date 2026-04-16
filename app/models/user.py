import logging
from datetime import datetime
from . import db

logger = logging.getLogger(__name__)

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subjects = db.relationship('Subject', backref='user', lazy=True)
    
    @classmethod
    def create(cls, username, email, password_hash):
        """新增一筆使用者記錄"""
        try:
            new_user = cls(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {e}")
            return None
            
    @classmethod
    def get_all(cls):
        """取得所有使用者記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
            
    @classmethod
    def get_by_id(cls, user_id):
        """取得單筆使用者記錄"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            logger.error(f"Error getting user by id: {e}")
            return None
            
    @classmethod
    def get_by_email(cls, email):
        """透過信箱取得使用者記錄"""
        try:
            return cls.query.filter_by(email=email).first()
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
            
    def update(self, **kwargs):
        """更新使用者記錄"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating user: {e}")
            return False
            
    def delete(self):
        """刪除使用者記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting user: {e}")
            return False
