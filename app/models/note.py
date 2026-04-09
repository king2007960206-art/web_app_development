from datetime import datetime
from . import db

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
        note = cls(subject_id=subject_id, title=title, original_content=original_content, ai_summary=ai_summary)
        db.session.add(note)
        db.session.commit()
        return note
        
    @classmethod
    def get_by_id(cls, note_id):
        return cls.query.get(note_id)
        
    @classmethod
    def get_all_by_subject(cls, subject_id):
        return cls.query.filter_by(subject_id=subject_id).all()
        
    def update_summary(self, new_summary):
        self.ai_summary = new_summary
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
