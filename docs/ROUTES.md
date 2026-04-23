# 路由設計 - 個人記帳簿系統

本文件基於 PRD、架構設計與資料庫 Schema，規劃了系統的 Flask 路由 (Routes)。採用 Blueprint 機制將路由拆分為 `auth`、`dashboard`、`transaction`、`report` 與 `settings` 五個主要模組。

---

## 1. 路由總覽表格

| 模組 (Blueprint) | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **auth** | 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入或密碼解鎖表單 |
| **auth** | 登入驗證 | POST | `/auth/login` | — | 驗證密碼，寫入 session，成功重導向至首頁 |
| **auth** | 登出 | GET/POST | `/auth/logout` | — | 清除 session，重導向至登入頁 |
| **dashboard** | 首頁儀表板 | GET | `/` 或 `/dashboard` | `dashboard/index.html` | 顯示總資產淨值、快速記帳按鈕與近期交易 |
| **transaction** | 新增交易表單 | GET | `/transaction/new` | `transaction/new.html` | 顯示「快速記帳」輸入表單 |
| **transaction** | 建立交易 | POST | `/transaction/` | — | 處理表單資料存入 DB，重導向至首頁 |
| **transaction** | 歷史明細列表 | GET | `/transaction/` | `transaction/list.html` | 顯示分頁與過濾後的歷史紀錄 |
| **transaction** | 編輯交易表單 | GET | `/transaction/<id>/edit` | `transaction/edit.html` | 顯示特定交易的編輯表單 |
| **transaction** | 更新交易 | POST | `/transaction/<id>/update` | — | 接收更新，寫入 DB，重導向至明細頁 |
| **transaction** | 刪除交易 | POST | `/transaction/<id>/delete` | — | 刪除特定紀錄，重導向至明細頁 |
| **report** | 財務分析報表 | GET | `/report/` | `report/index.html` | 顯示圓餅圖與折線圖 (可切換年月) |
| **report** | 匯出報表 | GET | `/report/export` | — | 回傳 CSV 檔案供下載 |
| **settings** | 設定首頁 | GET | `/settings/` | `settings/index.html` | 設定選單總覽 (帳戶、分類、預算) |
| **settings** | 帳戶列表 | GET | `/settings/accounts` | `settings/accounts.html` | 列出所有資金帳戶 |
| **settings** | 新增/編輯帳戶 | POST | `/settings/accounts` | — | 處理新增或修改帳戶邏輯 |
| **settings** | 分類列表 | GET | `/settings/categories` | `settings/categories.html`| 列出收支分類 (含預設與自定義) |
| **settings** | 新增分類 | POST | `/settings/categories` | — | 處理新增自定義分類 |
| **settings** | 預算設定 | GET | `/settings/budgets` | `settings/budgets.html` | 顯示並設定預算進度 |
| **settings** | 更新預算 | POST | `/settings/budgets` | — | 處理預算設定與變更 |

---

## 2. 每個路由的詳細說明 (節錄核心功能)

### 快速記帳 (Create Transaction)
- **輸入**：表單包含 `amount` (金額), `category_id` (分類), `source_account_id` (來源), `target_account_id` (目的), `transaction_date` (日期), `note` (備註)。
- **處理邏輯**：呼叫 `Transaction.create()`。驗證 `amount > 0`。
- **輸出**：成功後呼叫 `redirect(url_for('dashboard.index'))` 回到首頁。
- **錯誤處理**：如果必填欄位遺失，使用 `flash()` 顯示錯誤訊息，並重新渲染 `transaction/new.html`。

### 首頁儀表板 (Dashboard)
- **輸入**：(無)，若有日期篩選則透過 GET 參數 `?month=YYYY-MM`。
- **處理邏輯**：
  1. 從 `Session` 獲取 `user_id`。
  2. 呼叫 `Account.get_all_by_user()` 計算總資產淨值。
  3. 呼叫 `Transaction.get_all_by_user()` 取得最近 5 筆交易。
- **輸出**：渲染 `dashboard/index.html` 並帶入算好的變數。

---

## 3. Jinja2 模板清單

所有的模板將繼承自一個主版面 (Base Template) 以維持風格統一：
- `base.html`：包含 `<head>` (CSS/JS 引入)、全局導覽列 (Navbar)、頁尾 (Footer)、Flash 訊息顯示區塊。

需建立的子頁面清單：
1. `auth/login.html`：簡約的解鎖登入畫面。
2. `dashboard/index.html`：大字體的淨值顯示與醒目的「快速記帳」按鈕。
3. `transaction/new.html`：表單頁面，強調 3 秒輸入體驗。
4. `transaction/list.html`：清單列表，支援過濾與分頁。
5. `transaction/edit.html`：供修改過往紀錄的表單。
6. `report/index.html`：載入 Chart.js 繪製圓餅圖與折線圖的容器頁面。
7. `settings/index.html`：設定功能的總目錄。
8. `settings/accounts.html`：帳戶清單與新增彈窗。
9. `settings/categories.html`：分類清單。
10. `settings/budgets.html`：顯示預算設定進度條。
