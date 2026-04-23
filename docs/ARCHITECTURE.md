# 系統架構設計 - 個人記帳簿系統

本文件根據 [PRD.md](PRD.md) 的需求，規劃了「個人記帳簿系統」的技術架構、資料夾結構與系統元件關係。這將作為開發團隊實作時的技術指南。

---

## 1. 技術架構說明

為了符合 PRD 中的技術限制與快速開發的需求，我們選用以下技術棧：

- **後端框架：Python + Flask**
  - **原因**：Flask 輕量、靈活，非常適合作為中小型專案的後端框架。由於我們不需要建立複雜的微服務架構，Flask 足以完美支撐個人記帳系統的 API 與邏輯處理。
- **模板引擎：Jinja2**
  - **原因**：內建於 Flask 中，支援直接從後端將資料注入 HTML 進行伺服器端渲染 (SSR)。本專案不採用前後端分離，統一由 Flask 與 Jinja2 處理頁面渲染，降低開發與維護成本。
- **資料庫：SQLite（搭配 SQLAlchemy ORM）**
  - **原因**：個人記帳系統資料量不大且以本機或單一部署為主，SQLite 足以應付。引入 SQLAlchemy (ORM) 則能讓我們用 Python 物件導向的方式操作資料庫，不僅寫法直觀，也方便處理「帳戶」、「交易」、「類別」等複雜關聯。

### Flask MVC 模式說明
本專案會遵循經典的 MVC (Model-View-Controller) 設計模式：
- **Model（模型）**：負責與 SQLite 溝通，定義資料結構與會計邏輯（如「交易紀錄」、「資產帳戶」）。
- **View（視圖）**：負責呈現畫面，由 Jinja2 HTML 模板結合 CSS/JS 組成，打造清爽無廣告的介面。
- **Controller（控制器）**：由 Flask Route 擔任，負責接收瀏覽器的請求，呼叫 Model 取得資料，並將資料傳遞給 Jinja2 渲染後回傳給使用者。

---

## 2. 專案資料夾結構

本系統採用藍圖（Blueprints）與清晰分層的模組化結構，以確保程式碼容易擴展與維護。

```text
personal_accounting_book/
│
├── app/                      ← 應用程式核心資料夾
│   ├── __init__.py           ← 初始化 Flask 實例與擴充套件 (如 SQLAlchemy)
│   │
│   ├── models/               ← 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── user.py           ← 使用者模型 (儲存密碼設定與個資)
│   │   ├── account.py        ← 帳戶模型 (現金、銀行存款、信用卡等)
│   │   ├── transaction.py    ← 交易紀錄模型 (收支、轉帳、借貸邏輯)
│   │   ├── category.py       ← 收支類別與標籤模型
│   │   └── budget.py         ← 預算與儲蓄目標模型
│   │
│   ├── routes/               ← Flask 路由模組 (Controller)
│   │   ├── __init__.py
│   │   ├── auth.py           ← 登入、解鎖與隱私驗證路由
│   │   ├── dashboard.py      ← 首頁儀表板 (快速記帳、資產淨值摘要)
│   │   ├── transaction.py    ← 交易紀錄的新增、修改與刪除
│   │   ├── report.py         ← 圓餅圖、折線圖與報表匯出邏輯
│   │   └── settings.py       ← 帳戶管理、類別自定義與預算設定
│   │
│   ├── templates/            ← Jinja2 HTML 模板 (View)
│   │   ├── base.html         ← 共用模板 (導覽列、頁尾、基礎排版)
│   │   ├── dashboard.html    ← 首頁儀表板視圖
│   │   ├── transaction/      ← 記帳與歷史明細相關視圖
│   │   ├── report/           ← 報表與圖表呈現視圖
│   │   └── auth/             ← 密碼解鎖/登入視圖
│   │
│   └── static/               ← 靜態資源
│       ├── css/              ← 樣式表 (打造清爽簡約風格)
│       ├── js/               ← 前端互動邏輯 (圖表繪製、表單動態驗證)
│       └── images/           ← 圖片與圖標資源
│
├── instance/                 ← 運行時自動生成的安全資料夾
│   └── database.db           ← SQLite 實體資料庫檔案 (不進版控)
│
├── docs/                     ← 專案說明文件
│   ├── PRD.md                ← 產品需求文件
│   └── ARCHITECTURE.md       ← 系統架構設計文件 (本文件)
│
├── config.py                 ← 全域設定檔 (金鑰、資料庫路徑等設定)
├── requirements.txt          ← Python 依賴套件清單 (Flask, SQLAlchemy 等)
└── run.py                    ← 啟動整個應用程式的入口檔案
```

---

## 3. 元件關係圖

以下展示使用者從瀏覽器操作時，系統內部的資料流動與元件互動關係。

```mermaid
flowchart TD
    %% 定義節點
    Browser[瀏覽器 (Client)]
    Route["Flask Route (Controller)"]
    Model["Model (SQLAlchemy)"]
    DB[("(SQLite 資料庫)")]
    Template["Jinja2 Template (View)"]

    %% 定義互動流程
    Browser -- "1. 發送 HTTP 請求 (GET/POST)" --> Route
    Route -- "2. 操作/查詢資料 (ORM)" --> Model
    Model -- "3. 執行 SQL 語法" --> DB
    DB -. "4. 回傳資料庫結果" .-> Model
    Model -. "5. 將物件回傳給路由" .-> Route
    
    Route -- "6. 結合資料與模板" --> Template
    Template -. "7. 生成最終 HTML 頁面" .-> Route
    Route -. "8. 返回 HTTP 回應" .-> Browser

    %% 添加背景色以區分層次
    classDef client fill:#f9f,stroke:#333,stroke-width:2px;
    classDef backend fill:#bbf,stroke:#333,stroke-width:2px;
    classDef db fill:#bfb,stroke:#333,stroke-width:2px;
    
    class Browser client;
    class Route,Model,Template backend;
    class DB db;
```

---

## 4. 關鍵設計決策

以下為針對 PRD 需求所做出的幾個關鍵架構設計：

1. **以 Blueprint 進行模組化拆分**
   - **原因**：為了避免所有的路由邏輯全擠在一個 `app.py` 中，我們使用 Flask 的 Blueprints 功能，將路由依照功能拆分為 `auth` (驗證)、`dashboard` (首頁)、`transaction` (交易)、`report` (報表) 與 `settings` (設定)。這讓各模組職責清晰，方便團隊並行開發。
2. **隱含「借貸法則」的資料模型設計**
   - **原因**：PRD 要求能精準計算資產淨值並支援多帳戶。因此，在 `Transaction` 模型中，我們不只是單純記錄「花費」，而是採用來源帳戶 (`source_account_id`) 與目的帳戶 (`target_account_id`) 的設計。這樣一來，「轉帳」、「提款」或是「信用卡繳款」都能透過資金在兩個帳戶間的流動來記錄，完美實現會計的借貸邏輯。
3. **ORM 技術選型與依賴**
   - **原因**：直接寫 SQL 語法在維護上較為困難。使用 SQLAlchemy ORM，能讓我們以 Python 類別 (Class) 來定義資料表，將「交易」與「帳戶」、「類別」建立外鍵關聯。未來若需要擴充共同記帳的欄位，只需修改模型類別即可。
4. **前端不分離的 SSR 策略與簡約風格實踐**
   - **原因**：本專案由 Jinja2 處理視圖，能減少前端與後端溝通的 API 開發時間。靜態資源夾 (`static/css`, `static/js`) 中，我們將避免使用過於龐大的前端框架，而是以原生的 CSS 或輕量級 CSS 框架來打造 PRD 所要求的「清爽簡約風」及「3秒快速記帳」的互動體驗。
5. **資料庫檔案的安全隔離**
   - **原因**：PRD 非常重視隱私保護。我們將 SQLite 的 `.db` 檔案放置於 `instance/` 資料夾下，並在 `.gitignore` 中排除該資料夾。這樣即使程式碼上傳到雲端儲存庫，使用者的真實財務資料也不會外洩。
