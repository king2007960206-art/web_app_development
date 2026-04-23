from datetime import datetime
from . import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True) # NULL means default category
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., income, expense
    icon = db.Column(db.String(100), nullable=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, name, type, user_id=None, icon=None, is_default=False):
        category = cls(name=name, type=type, user_id=user_id, icon=icon, is_default=is_default)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_by_id(cls, category_id):
        return cls.query.get(category_id)

    @classmethod
    def get_user_categories(cls, user_id):
        return cls.query.filter((cls.user_id == user_id) | (cls.is_default == True)).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
