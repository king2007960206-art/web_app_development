from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/', methods=['GET'])
def index():
    """
    顯示學習主控台。
    渲染 dashboard/index.html，包含總學習時數與近期測驗正確率之儀表板。
    """
    pass

@dashboard_bp.route('/weaknesses', methods=['GET'])
def weaknesses():
    """
    顯示弱點分析結果 (錯題本)。
    收集並過濾 QuestionResult 中 is_correct=False 的資料，渲染至 dashboard/weaknesses.html。
    """
    pass
