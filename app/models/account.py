from datetime import datetime
from . import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., cash, bank, credit, mobile_pay
    balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='TWD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, name, type, balance=0.0, currency='TWD'):
        account = cls(user_id=user_id, name=name, type=type, balance=balance, currency=currency)
        db.session.add(account)
        db.session.commit()
        return account

    @classmethod
    def get_by_id(cls, account_id):
        return cls.query.get(account_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
