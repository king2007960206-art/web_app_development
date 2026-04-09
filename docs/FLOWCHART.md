# 流程圖文件 - AI 學習助理平台

這份文件基於產品需求文件 (PRD) 與系統架構文件 (ARCHITECTURE)，透過視覺化的方式呈現使用者的完整操作路徑、系統內部處理資料的流程，並梳理出系統初期的路由對照表。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者在平台上進行主要操作（如上傳筆記、進行測驗與語音問答）時的頁面跳轉與決策路徑。

```mermaid
flowchart LR
    A([使用者造訪平台]) --> B{是否有帳號？}
    B -->|否| C[註冊頁面]
    C --> D[登入頁面]
    B -->|是| D
    
    D --> E[Dashboard 學習主控台]
    
    E --> F{選擇要進行的動作}
    
    %% 主控台功能
    F -->|查看總覽| G[查看學習進度與時數]
    F -->|弱點分析| H[查看常錯題型清單與複習建議]
    
    %% 科目與筆記功能
    F -->|科目管理| I[選擇或新增學習科目]
    I --> J{選擇科目內的動作}
    J -->|上傳新筆記| K[上傳講義/資料]
    K --> L[系統使用 AI 自動生成摘要]
    L --> M[檢視並保存智慧筆記]
    
    J -->|歷史筆記| M
    
    %% 測驗功能
    J -->|進行測驗| N[系統根據筆記生成選擇題]
    N --> O[使用者作答]
    O --> P[提交表單：即時批改並紀錄錯題]
    P --> Q[檢視測驗測驗解析]
    Q --> E
    
    %% 語音問答功能
    F -->|語音問答| R[進入語音聊天畫面]
    R --> S[點擊麥克風發問]
    S --> T[AI 即時回答解決疑問]
    T --> R
```

## 2. 系統序列圖 (Sequence Diagram)

這裡我們以 **「上傳筆記並生成 AI 摘要」** 為例，描繪系統後端與資料庫、AI 服務層之間的詳細互動序列。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (Frontend)
    participant Route as Flask Route (notes.py)
    participant AIService as AI 服務層 (ai_service.py)
    participant DB as SQLite 資料庫 (models)

    User->>Browser: 在特定科目下選擇講義檔案並點擊「上傳產生摘要」
    Browser->>Route: POST /subjects/{id}/notes/upload (上傳檔案內容)
    
    activate Route
    Route->>Route: 驗證檔案格式與使用者權限
    Route->>AIService: 傳遞整理需求 Prompt 與講義文字內容
    
    activate AIService
    AIService->>AIService: 呼叫外部 LLM API (例如 OpenAI)
    AIService-->>Route: 回傳產出之結構化摘要 (Markdown / JSON)
    deactivate AIService
    
    Route->>DB: INSERT INTO notes (寫入原始檔案儲存路徑與 AI 摘要內容)
    activate DB
    DB-->>Route: 寫入成功，回傳 Note ID
    deactivate DB
    
    Route-->>Browser: HTTP 302 Redirect (重導向至該筆記檢視頁面)
    deactivate Route
    
    Browser->>User: 顯示自動整理好的精美筆記
```

## 3. 功能清單對照表

以下為平台核心功能的 URL 路由對應。設計上依循 RESTful 風格，以資源標的（如 auth, dashboard, subjects, notes）作為區分，實作時這些路由可被註冊在不同的 Flask Blueprints 之下。

| 功能模組 | 操作描述 | URL 路徑 | HTTP 方法 | 對應角色 |
| --- | --- | --- | --- | --- |
| **首頁與認證** | 平台登陸介紹頁 | `/` | GET | 訪客 |
| | 使用者註冊 | `/auth/register` | GET / POST | 訪客 |
| | 使用者登入 | `/auth/login` | GET / POST | 訪客 |
| **學習主控台** | 總覽學習進度與時數 | `/dashboard` | GET | 已登入使用者 |
| | 檢視弱點分析與錯題本 | `/dashboard/weaknesses` | GET | 已登入使用者 |
| **科目與筆記** | 檢視所有科目 | `/subjects` | GET | 已登入使用者 |
| | 新增單一科目 | `/subjects/create` | GET / POST | 已登入使用者 |
| | 檢視特定科目下的筆記清單 | `/subjects/<id>/notes` | GET | 已登入使用者 |
| | 上傳講義與生成 AI 摘要 | `/subjects/<id>/notes/upload` | GET / POST | 已登入使用者 |
| | 閱讀/編輯單篇筆記摘要 | `/notes/<note_id>` | GET / POST | 已登入使用者 |
| **自動測驗** | 特定科目的測驗紀錄 | `/subjects/<id>/quizzes` | GET | 已登入使用者 |
| | 開始測驗（AI 出題與交卷） | `/subjects/<id>/quizzes/start` | GET / POST | 已登入使用者 |
| | 查看測驗解析與分數 | `/quizzes/<quiz_id>` | GET | 已登入使用者 |
| **語音互動** | 進入語音問答聊天頁面 | `/voice/qa` | GET | 已登入使用者 |
| | 供前端發送語音轉文字做非同步問答 | `/api/voice/ask` | POST | 內部 API (JS Fetch) |
