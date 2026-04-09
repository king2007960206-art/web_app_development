from flask import Blueprint, render_template, request, jsonify

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/voice/qa', methods=['GET'])
def qa_page():
    """提供使用者用語音問答交流的聊天室畫面，主要會載入相關的 Web API 控制腳本於 voice/qa.html。"""
    pass

@voice_bp.route('/api/voice/ask', methods=['POST'])
def api_voice_ask():
    """
    供前端非同步 Fetch 存取的內部 API 端點。
    接收夾帶使用者對話字串的 JSON，呼叫外部 AI 後，回傳含有答覆文的 JSON 以供 TTS 發聲。
    """
    pass
