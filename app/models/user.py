from datetime import datetime
from . import db

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
        new_user = cls(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
        
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
