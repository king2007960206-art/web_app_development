from datetime import datetime
from . import db

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    period_month = db.Column(db.String(7), nullable=False) # e.g. "2026-04"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    category = db.relationship('Category')

    @classmethod
    def create(cls, user_id, amount, period_month, category_id=None):
        budget = cls(user_id=user_id, amount=amount, period_month=period_month, category_id=category_id)
        db.session.add(budget)
        db.session.commit()
        return budget

    @classmethod
    def get_by_id(cls, budget_id):
        return cls.query.get(budget_id)

    @classmethod
    def get_user_budgets(cls, user_id, period_month=None):
        query = cls.query.filter_by(user_id=user_id)
        if period_month:
            query = query.filter_by(period_month=period_month)
        return query.all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
