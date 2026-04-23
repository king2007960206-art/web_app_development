from flask import Blueprint, render_template, session, redirect, url_for
from app.models.account import Account
from app.models.transaction import Transaction

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    """
    顯示首頁儀表板。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    
    # 取得使用者所有的帳戶，並計算總資產淨值
    accounts = Account.get_all_by_user(user_id)
    total_net_worth = sum(account.balance for account in accounts)
    
    # 取得最近 5 筆交易
    recent_transactions = Transaction.get_all_by_user(user_id)[:5]
    
    return render_template('dashboard/index.html', 
                           total_net_worth=total_net_worth, 
                           accounts=accounts, 
                           recent_transactions=recent_transactions)
