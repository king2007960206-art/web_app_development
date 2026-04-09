from datetime import datetime
from . import db

class Subject(db.Model):
    __tablename__ = 'subject'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    notes = db.relationship('Note', backref='subject', lazy=True)
    quizzes = db.relationship('Quiz', backref='subject', lazy=True)
    
    @classmethod
    def create(cls, user_id, name, description=None):
        subject = cls(user_id=user_id, name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        return subject
        
    @classmethod
    def get_by_id(cls, subject_id):
        return cls.query.get(subject_id)
        
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
