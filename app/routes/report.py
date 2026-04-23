from flask import Blueprint

report_bp = Blueprint('report', __name__)

@report_bp.route('/', methods=['GET'])
def index():
    """
    顯示財務分析報表頁面 (report/index.html)。
    提供支出佔比圓餅圖與收支趨勢折線圖，支援按週/月/年切換。
    """
    pass

@report_bp.route('/export', methods=['GET'])
def export_report():
    """
    將目前的財務資料匯出為 CSV 格式供使用者下載。
    """
    pass
