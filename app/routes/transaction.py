from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app.models import db
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/new', methods=['GET'])
def new_transaction():
    """
    顯示「快速記帳」表單 (transaction/new.html)。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    accounts = Account.get_all_by_user(user_id)
    categories = Category.get_user_categories(user_id)
    
    # 區分收入與支出類別供前端動態切換
    income_categories = [c for c in categories if c.type == 'income']
    expense_categories = [c for c in categories if c.type == 'expense']
    
    return render_template('transaction/new.html', 
                           accounts=accounts, 
                           income_categories=income_categories,
                           expense_categories=expense_categories,
                           today=datetime.now().strftime('%Y-%m-%d'))

@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    """
    處理新增交易邏輯。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    
    # 取得表單資料
    tx_type = request.form.get('tx_type') # 'expense' or 'income'
    amount = request.form.get('amount', type=float)
    category_id = request.form.get('category_id', type=int)
    account_id = request.form.get('account_id', type=int)
    note = request.form.get('note')
    tx_date_str = request.form.get('transaction_date')
    
    if not amount or amount <= 0:
        flash('請輸入大於 0 的金額！', 'danger')
        return redirect(url_for('transaction.new_transaction'))
        
    try:
        tx_date = datetime.strptime(tx_date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        tx_date = datetime.utcnow()

    source_account_id = None
    target_account_id = None

    # 借貸邏輯處理：同步更新帳戶餘額
    account = Account.get_by_id(account_id)
    if not account or account.user_id != user_id:
        flash('請選擇有效的帳戶！', 'danger')
        return redirect(url_for('transaction.new_transaction'))

    if tx_type == 'expense':
        source_account_id = account.id
        # 扣除來源帳戶餘額
        account.update(balance=account.balance - amount)
    elif tx_type == 'income':
        target_account_id = account.id
        # 增加目的帳戶餘額
        account.update(balance=account.balance + amount)
            
    # 建立交易紀錄
    Transaction.create(
        user_id=user_id,
        category_id=category_id,
        amount=amount,
        source_account_id=source_account_id,
        target_account_id=target_account_id,
        note=note,
        transaction_date=tx_date
    )
    
    flash('記帳成功！', 'success')
    return redirect(url_for('dashboard.index'))

@transaction_bp.route('/', methods=['GET'])
def list_transactions():
    pass

@transaction_bp.route('/<int:transaction_id>/edit', methods=['GET'])
def edit_transaction(transaction_id):
    pass

@transaction_bp.route('/<int:transaction_id>/update', methods=['POST'])
def update_transaction(transaction_id):
    pass

@transaction_bp.route('/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction(transaction_id):
    pass
