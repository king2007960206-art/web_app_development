from datetime import datetime
from . import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False)
    source_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)
    target_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='TWD')
    note = db.Column(db.Text, nullable=True)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    receipt_image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    category = db.relationship('Category')
    source_account = db.relationship('Account', foreign_keys=[source_account_id])
    target_account = db.relationship('Account', foreign_keys=[target_account_id])

    @classmethod
    def create(cls, user_id, category_id, amount, source_account_id=None, target_account_id=None,
               currency='TWD', note=None, transaction_date=None, receipt_image_url=None):
        
        if transaction_date is None:
            transaction_date = datetime.utcnow()

        transaction = cls(
            user_id=user_id,
            category_id=category_id,
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            amount=amount,
            currency=currency,
            note=note,
            transaction_date=transaction_date,
            receipt_image_url=receipt_image_url
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @classmethod
    def get_by_id(cls, transaction_id):
        return cls.query.get(transaction_id)

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.transaction_date.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
