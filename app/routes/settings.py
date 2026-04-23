from flask import Blueprint

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/', methods=['GET'])
def index():
    """
    顯示設定總覽頁面 (settings/index.html)。
    """
    pass

@settings_bp.route('/accounts', methods=['GET', 'POST'])
def manage_accounts():
    """
    管理資金帳戶。
    GET: 顯示帳戶列表 (settings/accounts.html)。
    POST: 處理新增或修改帳戶邏輯。
    """
    pass

@settings_bp.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    """
    管理收支分類與標籤。
    GET: 顯示分類列表 (settings/categories.html)。
    POST: 處理新增自定義分類邏輯。
    """
    pass

@settings_bp.route('/budgets', methods=['GET', 'POST'])
def manage_budgets():
    """
    管理預算與儲蓄目標。
    GET: 顯示預算設定與進度條 (settings/budgets.html)。
    POST: 處理更新預算限制。
    """
    pass
