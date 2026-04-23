from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so they are registered with SQLAlchemy
from .user import User
from .account import Account
from .category import Category
from .transaction import Transaction
from .budget import Budget
from .savings_goal import SavingsGoal
