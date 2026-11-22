# 全球 AA／AAA 單機遊戲上市年曆

以 2026/11/22 的 **54 筆使用者精選清單**為基礎，保留原互動式月曆、年覽、季度／季節預定及下方年份追蹤區。

## GitHub Pages 上線（約 5–10 分鐘）

1. 登入 GitHub，新建 **Public** repository，例如 `aaa-game-calendar`。
2. 將本資料夾**內部所有檔案**（包括 `.github/workflows/`）上傳到 repository 根目錄。可使用網頁 Upload files，注意隱藏的 `.github` 目錄也要上傳。
3. 在 **Settings → Pages → Build and deployment → Source** 選 **Deploy from a branch**，Branch 選 `main`，Folder 選 `/(root)`，按 Save。
4. 網站網址通常為 `https://<你的帳號>.github.io/aaa-game-calendar/`。等待首次部署完成。
5. 在 **Actions** 頁面啟用 workflows，開啟 **Daily game-news discovery**，按 **Run workflow** 測試。
6. 如遇 `git push` 權限問題，至 **Settings → Actions → General → Workflow permissions** 選 **Read and write permissions**。組織政策可能限制此選項。

> 這份 ZIP 是可部署專案，並未代替你登入 GitHub、建立 repository 或公開網站。上線需要你自行操作或提供可操作的 GitHub 連線。

## 檔案結構

- `index.html`：網站，讀取 `data/games.json`，每次重新整理取得共用資料。
- `data/games.json`：54 筆正式顯示資料（26 筆有日期、28 筆預定／追蹤）。**這些日期、平台仍保留原清單的待核實狀態**。
- `data/review_queue.json`：每日搜尋結果、錯誤及候選新聞。
- `scripts/daily_check.py`：每日搜尋近期官方網域相關新聞的程式，使用 Google News RSS 搜尋索引，非官方 API；可能受索引延遲或 RSS 服務變動影響。
- `.github/workflows/daily-check.yml`：每日台灣時間 09:00 觸發；GitHub 排程可能延遲、停用或偶爾漏跑。

## 每日更新的實際範圍（重要）

**已自動化**：每天搜尋 Nintendo、PlayStation、Xbox、Square Enix、Capcom、SEGA 官方網域的近期新聞；依現有遊戲名稱初步匹配；寫入候選清單與最近查核時間，並提交 GitHub。

**未自動化**：無法僅憑 RSS 標題可靠判斷「首次上市」、AA／AAA、跨區時差或平台差異。因此**不會自動改寫**正式上市日期、平台、遊戲清單。需管理者核對來源後手動編輯 `data/games.json` 並提交；網站隨 GitHub Pages 更新。新增大作的自動發現亦非全面覆蓋。

查核候選可直接在 GitHub 開啟 `data/review_queue.json`。資料更新與查核成功是不同概念。網站顯示查核時間，不代表 54 款遊戲都已核實。

## 如何維護遊戲

直接在 GitHub 編輯 `data/games.json`：

- `events`：有 `date` (`YYYY-MM-DD`) 的遊戲，放在指定日期。
- `watch`：`period: "2027-05"`、`quarter: "2027-Q1"` 或 `season: "2027-春季"`，顯示於月份／季度／季節預定區；僅 `releaseYear` 或完全未定則顯示在下方。
- 保留 `id`，不要重複；填寫 `name`、`company`、`platform`、`status`、`url`、`note`。
- 新聞候選必須先開啟**官方原始公告**確認日期與平台，不可直接將搜尋摘要當成正式消息。
- 原則：只收 AA／AAA 或重大知名 IP 的**首次上市**；已上市作品的 Switch 2／其他平台移植版不納入。

## 已知限制

- 網站是公開唯讀的共用資料展示。舊 HTML 的編輯彈窗仍可能允許在頁面上暫時編輯，但**不會寫回 GitHub**；重整即恢復共用資料。管理者請直接修改 JSON。
- 公開 repository 的遊戲資料與候選清單可被任何人檢視，勿放公司內部機密。
- Google News RSS 是第三方搜尋索引，不保證完整涵蓋所有官方公告，無法保證每天必有更新；部分文章會回傳 Google News 轉址連結。
- 54 筆是沿用先前清單，不代表已完成逐筆外部驗證；**尤其不應把原清單中的日期視為全部官方確認**。
- 直接用 `file://` 開啟 `index.html` 可能因瀏覽器跨來源限制無法載入 JSON。測試可在專案目錄執行 `python -m http.server 8000`，再開啟 `http://localhost:8000/`。
