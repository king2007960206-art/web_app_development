# 路由與頁面設計文件 - AI 學習助理平台

基於前置的 PRD、架構與資料庫設計，以下詳述本專案的所有 URL 路由、對應到的 Jinja2 模板，以及資料流向。本專案採伺服器端渲染 (SSR)，多數以表單方式發送請求。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 網站首頁 | GET | `/` | `index.html` | 登陸首頁 |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 寫入 User，重導至登入 |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳密，建立 Session |
| 登出 | GET | `/auth/logout` | — | 清除 Session，重導至首頁 |
| 主控台 | GET | `/dashboard/` | `dashboard/index.html` | 學習時數、進度概覽 |
| 弱點分析 | GET | `/dashboard/weaknesses` | `dashboard/weaknesses.html` | 錯題本與複習建議 |
| 科目列表 | GET | `/subjects/` | `subjects/index.html` | 顯示使用者的所有科目 |
| 新增科目頁面 | GET | `/subjects/new` | `subjects/new.html` | 顯示新增科目表單 |
| 建立科目 | POST | `/subjects/` | — | 寫入 Subject，重導至列表 |
| 某科筆記清單 | GET | `/subjects/<subject_id>/notes` | `notes/index.html` | 顯示該科的所有筆記 |
| 上傳筆記頁面 | GET | `/subjects/<subject_id>/notes/upload`| `notes/upload.html` | 顯示檔案上傳表單 |
| 處理上傳生成 | POST | `/subjects/<subject_id>/notes/upload`| — | 呼叫 AI 生摘要，存入 Note |
| 檢視單筆筆記 | GET | `/notes/<note_id>` | `notes/detail.html` | 顯示 AI 結構化摘要 |
| 某科測驗列表 | GET | `/subjects/<subject_id>/quizzes` | `quizzes/index.html` | 顯示該科目的測驗紀錄 |
| 產生測驗 | POST | `/subjects/<subject_id>/quizzes` | — | 呼叫 AI 出題，建立 Quiz，重導至作答 |
| 進行測驗頁面 | GET | `/quizzes/<quiz_id>/take` | `quizzes/take.html` | 顯示測驗題目與答題表單 |
| 提交測驗 | POST | `/quizzes/<quiz_id>/submit` | — | 批改與紀錄 QuestionResult |
| 測驗結果解析 | GET | `/quizzes/<quiz_id>` | `quizzes/detail.html` | 顯示得分與錯題詳解 |
| 語音問答畫面 | GET | `/voice/qa` | `voice/qa.html` | 包含語音存取的聊天介面 |
| 語音問答 API | POST | `/api/voice/ask` | — (回傳 JSON) | 接收前端文字，回傳 AI 答覆 |

## 2. 每個路由的詳細說明

以下針對三個最核心的路由功能詳述操作邏輯。

### 2.1 筆記上傳與摘要產生 (`POST /subjects/<subject_id>/notes/upload`)
- **輸入**: HTML Form，包含檔案上傳欄位與選擇性的 `title` 欄位。
- **處理邏輯**: 
  1. 擷取檔案內容並轉為純文字 (純文字擋或 PDF 解析)。
  2. 呼叫底層機制 `ai_service.generate_note_summary(text)`。
  3. 實例化 `Note` 並將原始內文與 AI 摘要存入 SQLite 資料庫。
- **輸出**: HTTP 302 重導向至 `GET /notes/<note_id>`。
- **錯誤處理**: 無效檔案或 API 超時則 `flash` 錯誤訊息，重新渲染上傳頁面。

### 2.2 提交測驗與批改 (`POST /quizzes/<quiz_id>/submit`)
- **輸入**: HTML Form (使用者的答題選項陣列，例如 `<input name="q_1">`)。
- **處理邏輯**:
  1. 向後端取回原本存於記憶體或 DB 中的正確答案配置。
  2. 逐題比對作答情形，累加得分，更新 `Quiz` 資料表記錄。
  3. 針對每題，透過 `QuestionResult.create(...)` 寫入答題紀錄、標示 `is_correct` 以及加入詳解。
- **輸出**:重導向至測驗結果頁面 `GET /quizzes/<quiz_id>`。

### 2.3 語音串接互動 (`POST /api/voice/ask`)
- **輸入**: JSON 格式中的使用者發話文本內容。
- **處理邏輯**: 直接調用 `ai_service.ask_question(prompt)` 詢問 LLM 並獲得回傳。
- **輸出**: 回傳 JSON `{ "answer": "這裡為 AI 回應"，"status": "success" }` 給前端透過 Web Speech API 進行有聲播放與文字渲染。

## 3. Jinja2 模板清單

所有網頁將統一繼承此專案樣板 `base.html`，以達成全局排版 (Header、Sidebar、Footer 等) 重用最佳化。

- `base.html` 基礎公用佈局
- `auth/` 登入 (`login.html`)、註冊 (`register.html`)
- `dashboard/` 總覽 (`index.html`)、錯題本 (`weaknesses.html`)
- `subjects/` 科目列表 (`index.html`)、建表單 (`new.html`)
- `notes/` 筆記列表 (`index.html`)、上傳表單 (`upload.html`)、單篇筆記 (`detail.html`)
- `quizzes/` 測驗歷程 (`index.html`)、實戰作答 (`take.html`)、得分與解析 (`detail.html`)
- `voice/` 語音輸入畫面 (`qa.html`)

## 4. 路由骨架程式碼
相關 Controller (Route) 程式碼皆已於 `app/routes/` 下以 Blueprint 建置。
