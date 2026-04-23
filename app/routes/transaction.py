from flask import Blueprint

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/new', methods=['GET'])
def new_transaction():
    """
    顯示「快速記帳」表單 (transaction/new.html)。
    """
    pass

@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    """
    處理新增交易邏輯。
    接收表單資料，驗證後呼叫 Transaction.create() 存入資料庫，成功後重導向至首頁。
    """
    pass

@transaction_bp.route('/', methods=['GET'])
def list_transactions():
    """
    顯示歷史明細列表 (transaction/list.html)。
    支援日期或分類的過濾與分頁功能。
    """
    pass

@transaction_bp.route('/<int:transaction_id>/edit', methods=['GET'])
def edit_transaction(transaction_id):
    """
    顯示特定交易紀錄的編輯表單 (transaction/edit.html)。
    """
    pass

@transaction_bp.route('/<int:transaction_id>/update', methods=['POST'])
def update_transaction(transaction_id):
    """
    處理交易更新邏輯。
    接收表單資料，更新資料庫，重導向至歷史明細列表。
    """
    pass

@transaction_bp.route('/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction(transaction_id):
    """
    處理刪除交易邏輯。
    刪除資料庫中的該筆紀錄，並重導向至歷史明細列表。
    """
    pass
