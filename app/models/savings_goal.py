from datetime import datetime
from . import db

class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    deadline_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, name, target_amount, current_amount=0.0, deadline_date=None):
        goal = cls(
            user_id=user_id, 
            name=name, 
            target_amount=target_amount, 
            current_amount=current_amount, 
            deadline_date=deadline_date
        )
        db.session.add(goal)
        db.session.commit()
        return goal

    @classmethod
    def get_by_id(cls, goal_id):
        return cls.query.get(goal_id)

    @classmethod
    def get_user_goals(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
