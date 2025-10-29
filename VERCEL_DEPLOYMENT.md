# Vercel 部署指南

## 問題修復

此專案原本為 Railway/Heroku 設計，現已適配 Vercel serverless 架構。

### 修復的問題
- ✅ 500 錯誤: FUNCTION_INVOCATION_FAILED
- ✅ 檔案日誌寫入問題（serverless 環境不支援）
- ✅ 缺少 Vercel 配置檔案
- ✅ Flask app 未適配 serverless 架構

### 主要變更

1. **vercel.json** - Vercel 部署配置
   - 定義 Python serverless function
   - 設定路由規則
   - 配置環境變數

2. **api/index.py** - Serverless function 入口點
   - WSGI 應用適配器
   - 正確的模組導入路徑

3. **main.py** - 修復日誌配置
   - 移除檔案日誌處理器
   - 僅使用 stdout（適配 serverless）

4. **.vercelignore** - 排除不必要的檔案
   - 減少部署大小
   - 加快部署速度

## 部署步驟

### 1. 連接 GitHub 倉庫到 Vercel

1. 訪問 [Vercel Dashboard](https://vercel.com/dashboard)
2. 點擊 "Add New Project"
3. 選擇此 GitHub 倉庫
4. Vercel 會自動檢測 `vercel.json` 配置

### 2. 配置環境變數（可選）

在 Vercel 專案設定中添加：
```
FLASK_ENV=production
PYTHONPATH=.
```

### 3. 部署

- **自動部署**: 推送到 main 分支會自動觸發部署
- **手動部署**: 在 Vercel Dashboard 點擊 "Deploy"

### 4. 驗證部署

訪問以下端點確認服務正常：

```bash
# 健康檢查
curl https://your-app.vercel.app/api/health

# 測試功能
curl https://your-app.vercel.app/api/test

# 首頁
curl https://your-app.vercel.app/
```

## 技術細節

### Serverless 架構說明

- **冷啟動**: 首次請求可能較慢（1-3秒）
- **執行時間限制**: 
  - Hobby plan: 10秒
  - Pro plan: 60秒
- **記憶體限制**: 
  - Hobby plan: 1GB
  - Pro plan: 3GB

### 占星引擎

系統有兩種模式：

1. **真實引擎模式** (Kerykeion + Swiss Ephemeris)
   - 精確的天文計算
   - 需要較多資源
   - 可能遇到冷啟動延遲

2. **備用模式** (Fallback)
   - 輕量級計算
   - 快速回應
   - 自動啟用（當真實引擎不可用時）

### 故障排除

#### 問題: 500 錯誤仍然發生

**可能原因:**
1. Python 依賴安裝失敗
2. 執行時間超出限制
3. 記憶體不足

**解決方案:**
1. 檢查 Vercel 部署日誌
2. 確認所有依賴都在 requirements.txt 中
3. 考慮升級到 Pro plan（如果是資源限制）

#### 問題: 占星計算失敗

**可能原因:**
- Kerykeion 初始化失敗
- Swiss Ephemeris 資料下載問題

**解決方案:**
- 系統會自動切換到備用模式
- 檢查 `/api/health` 端點的 `real_astro_enabled` 狀態

#### 問題: 首次請求很慢

**原因:**
- Serverless 冷啟動

**解決方案:**
- 這是正常現象
- 後續請求會快很多
- 考慮使用 Vercel 的 "Keep Warm" 功能

## API 端點

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/` | API 文檔頁面 |
| GET | `/api/health` | 健康檢查 |
| GET | `/api/test` | 功能測試 |
| POST | `/api/calculate_chart` | 星盤計算 |

## 本地測試

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動開發伺服器
python api/index.py

# 或使用 Vercel CLI
npm i -g vercel
vercel dev
```

## 監控和日誌

- **Vercel Dashboard**: 查看部署狀態和錯誤
- **Runtime Logs**: 即時查看 serverless function 日誌
- **Analytics**: 追蹤請求量和效能

## 成本考量

### Hobby Plan (免費)
- ✅ 足夠測試和小規模使用
- ✅ 100GB 頻寬/月
- ⚠️ 10秒執行時間限制

### Pro Plan ($20/月)
- ✅ 60秒執行時間
- ✅ 更多記憶體
- ✅ 優先支援

## 相關資源

- [Vercel Python Runtime 文檔](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Flask 部署指南](https://flask.palletsprojects.com/en/latest/deploying/)
- [專案 GitHub](https://github.com/momo741006/star)

---

最後更新: 2025-10-29
