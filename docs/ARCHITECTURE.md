# 系統架構文件 - AI 學習助理平台

這份文件基於 `docs/PRD.md` 的功能需求，規劃「AI 學習助理平台」的系統架構與專案結構。

## 1. 技術架構說明

### 選用技術與原因
本專案不採用前後端分離架構，而是傳統的伺服器端渲染 (SSR, Server-Side Rendering) 模式，以求快速開發與簡化部署。
- **後端框架：Python + Flask**
  輕量級且富有彈性的微框架，適合結合 AI Prompt 的開發邏輯，且 Python 生態系擁有豐富的 AI 和 NLP 擴充套件。
- **視圖層 (前端模板)：Jinja2**
  Jinja2 直接與 Flask 無縫整合，有利於將後端處理好的資料（如 AI 摘要、選擇題解答）快速嵌入 HTML 進行渲染。
- **資料庫：SQLite**
  無需架設獨立的資料庫伺服器，資料儲存在單一檔案 (`.db`) 中，十分適合 MVP 階段快速開發與環境架設。

### Flask MVC 模式說明
雖然 Flask 本身不強制要求 MVC（Model-View-Controller），但為了便於維護，我們採用類似 MVC 的設計邏輯：
- **Model (模型)**：負責定義資料結構（如：User、Note、Quiz、Progress），處理與 SQLite 資料庫的存取與操作（預計可採用 Flask-SQLAlchemy）。
- **View (視圖)**：以 `templates/` 資料夾內的 Jinja2 HTML 樣板為主，負責資料的呈現；並搭配 `static/` 處理簡單的樣式與互動腳本。
- **Controller (控制器)**：對應到 Flask 的 `routes/` 或 Blueprints，負責接收來自瀏覽器的 HTTP 請求，調用對應的 AI 服務或 Model 取出資料，最後把資料拋給 View 來渲染。

## 2. 專案資料夾結構

以下為此專案的資料夾與檔案結構規劃：

```text
ai_learning_assistant/
│
├── app/                  # 應用程式主要資料夾
│   ├── __init__.py       # 初始化 Flask App 與設定，註冊 Blueprints
│   ├── models/           # 模型層 (Data Models)
│   │   ├── __init__.py
│   │   ├── user.py       # 使用者模型
│   │   ├── subject.py    # 科目資訊模型
│   │   ├── note.py       # 筆記與 AI 摘要模型
│   │   └── quiz.py       # 測驗與錯誤紀錄模型
│   │
│   ├── routes/           # 路由層 (Controllers - 以 Blueprint 拆分)
│   │   ├── __init__.py
│   │   ├── auth.py       # 註冊登入相關路由
│   │   ├── dashboard.py  # 主控台、學習進度與弱點分析
│   │   ├── notes.py      # 上傳資料與產生筆記摘要
│   │   ├── quizzes.py    # 測驗與 AI 出題
│   │   └── voice.py      # 語音問答相關路由
│   │
│   ├── templates/        # 視圖層 (Jinja2 HTML Templates)
│   │   ├── base.html     # 共用版型 (Header/Sidebar/Footer)
│   │   ├── index.html    # 首頁 (Landing Page)
│   │   ├── auth/         # 登入與註冊頁
│   │   ├── dashboard/    # 主控台與儀表板分析
│   │   ├── notes/        # 上傳講義與檢視摘要頁
│   │   └── quizzes/      # 測驗進行與解析頁
│   │
│   ├── static/           # 靜態資源檔案
│   │   ├── css/          # 樣式表 (可考慮 TailwindCDN 或純 CSS)
│   │   ├── js/           # 前端互動腳本 (例如語音輸入解析、圖表渲染)
│   │   └── images/       # 圖片與圖示
│   │
│   └── services/         # 封裝外部核心服務邏輯
│       └── ai_service.py # 處理呼叫大語言模型 (LLM) 以產生摘要與出題
│
├── instance/             # 存放不進版控、運行時生成的檔案 
│   └── database.db       # SQLite 資料庫檔案
│
├── docs/                 # 專案文件
│   ├── PRD.md            # 產品需求文件
│   └── ARCHITECTURE.md   # 系統架構文件
│
├── app.py                # 應用程式啟動入口
├── requirements.txt      # Python 依賴套件清單
└── .env                  # 環境變數 (API 金鑰、Secret Key 等)
```

## 3. 元件關係圖

透過下方流程圖可暸解系統各元件的互動流程：

```mermaid
flowchart TD
    Browser[瀏覽器 Browser]
    
    subgraph "Flask 應用程式"
        Router[Flask Route\n(Controller)]
        AIService[AI Service\n(外部 LLM API)]
        Model[Database Model\n(SQLAlchemy)]
        Template[Jinja2 Template\n(View)]
    end
    
    DB[(SQLite)]
    
    Browser -- "1. HTTP 請求\n(例如：上傳講義)" --> Router
    Router -- "2. 查詢/儲存" --> Model
    Model -- "3. 讀寫操作" --> DB
    DB -- "4. 回傳數據" --> Model
    Model -- "5. 模型物件" --> Router
    
    Router -- "6. 提供文本要求 AI 處理" --> AIService
    AIService -- "7. 回傳 AI 產出\n(摘要/題目)" --> Router
    
    Router -- "8. 傳遞內容與變數" --> Template
    Template -- "9. 渲染出完整 HTML" --> Router
    Router -- "10. HTTP 回應\n(顯示頁面)" --> Browser
```

## 4. 關鍵設計決策

1. **整合 AI 邏輯獨立為 Service 層**
   **決策與原因**：將呼叫大型語言模型 (LLM) 產生筆記與出題的複雜 Prompt 與呼叫邏輯，獨立放在 `app/services/ai_service.py` 之中。
   **好處**：確保路由模組 (Controllers) 乾淨好維護；未來若需更換底層模型（例如從 OpenAI GPT 轉移到 Gemini 或內部模型），只需要改動該 Service 即可。

2. **透過 Flask Blueprints 實現路由模組化**
   **決策與原因**：MVP 階段雖不複雜，但由於 6 大功能明確，我們將路由依據功能（Auth, Dashboard, Notes, Quizzes 等）拆分多個 `Blueprint` 檔案。
   **好處**：避免所有業務邏輯與路由全部集中在 `app.py` 中，日後修改不會牽一髮動全身，也方便多人分工開發。

3. **部分採用 Ajax 非同步提升體驗 (如語音問答與 AI 載入)**
   **決策與原因**：雖整體架構不是前後端分離，但對於「語音對話」或「AI 正在產生題目中」這類較耗時或需要即時無縫體驗的功能，會採用前端 JS (fetch) 搭配後端回傳 JSON 的方式輔助。
   **好處**：可做到頁面不重新整理即可看見回覆，同時可展示轉圈圈 Progress 介面，大幅提升使用者體驗 (UX)。

4. **使用 SQLite 作為單一資料來源**
   **決策與原因**：目前資料結構多屬關聯性質（使用者 → 科目 → 筆記 → 測驗），故仍透過關聯式結構建立，但不需要大費周章裝 MySQL。
   **好處**：利用 `instance/database.db` 單一檔案部署與備份都極為方便，符合開發敏捷精神。
