# Vercel Serverless Function 修復總結

## 問題描述

錯誤訊息：
```
此無伺服器功能已崩潰。
500：內部伺服器錯誤
代碼：FUNCTION_INVOCATION_FAILED
ID：hkg1::c589q-1761740288234-b088508e870a
```

## 根本原因分析

1. **架構不匹配**: 專案原本設計為 Railway/Heroku 的持久性伺服器，但部署在 Vercel 的 serverless 架構上
2. **缺少配置**: 沒有 `vercel.json` 配置檔案
3. **入口點錯誤**: Vercel 需要特定的 `/api` 目錄結構和 WSGI 應用入口
4. **檔案系統寫入**: 日誌系統嘗試寫入檔案，但 serverless 環境是唯讀的

## 解決方案

### 1. 新增 Vercel 配置檔案 (vercel.json)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "PYTHONPATH": "."
  }
}
```

**作用**:
- 定義 Python serverless function 的建置方式
- 設定所有請求路由到 API 入口點
- 配置環境變數和 Python 路徑

### 2. 建立 Serverless Function 入口點 (api/index.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entry Point
"""

import sys
import os

# 添加父目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 導入 Flask app
from main import app

# Vercel WSGI 應用入口
application = app

# 本地測試支援
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

**作用**:
- 提供 Vercel 需要的 WSGI 應用入口點
- 正確設定模組導入路徑
- 保持本地測試能力

### 3. 修復日誌系統 (main.py)

**修改前**:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log') if os.path.exists('.') else logging.StreamHandler()
    ]
)
```

**修改後**:
```python
# 配置日誌 - 僅使用 stdout，適配 serverless 環境
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
```

**作用**:
- 移除檔案日誌處理器（serverless 環境不支援）
- 所有日誌輸出到 stdout，可在 Vercel 日誌中查看

### 4. 新增 .vercelignore 檔案

排除不必要的檔案，減少部署大小：
- 開發和測試檔案
- 壓縮檔案
- 備份檔案
- 其他平台配置（Railway, Procfile）
- 文檔檔案

### 5. 建立部署文檔 (VERCEL_DEPLOYMENT.md)

提供完整的部署指南和故障排除資訊。

## 技術細節

### Serverless 架構特點

| 特性 | 傳統伺服器 | Vercel Serverless |
|------|-----------|-------------------|
| 運行模式 | 持久性程序 | 按需啟動 |
| 檔案系統 | 可讀寫 | 唯讀 |
| 狀態管理 | 可保持狀態 | 無狀態 |
| 啟動時間 | 一次啟動 | 每次請求可能冷啟動 |
| 執行時間 | 無限制 | 有時間限制 |

### 相容性設計

專案保持雙重相容性：
1. **Vercel Serverless** - 透過 `api/index.py` 入口
2. **傳統部署** - 透過 `main.py` 直接運行（Railway/Heroku）

### 備用機制

系統具有自動降級能力：
- **主模式**: Kerykeion + Swiss Ephemeris（精確占星計算）
- **備用模式**: 簡化計算引擎（當主引擎不可用時自動啟用）

## 驗證步驟

部署後，訪問以下端點驗證：

### 1. 健康檢查
```bash
curl https://your-app.vercel.app/api/health
```

預期回應：
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "engine": "Kerykeion Swiss Ephemeris v4.26.3",
  "real_astro_enabled": true,
  "uptime_seconds": 123,
  "request_count": 1,
  "error_count": 0,
  "success_rate": 100.0,
  "timestamp": "2025-10-29T12:00:00.000Z"
}
```

### 2. 功能測試
```bash
curl https://your-app.vercel.app/api/test
```

應該返回完整的角色生成結果。

### 3. 首頁
```bash
curl https://your-app.vercel.app/
```

應該返回 API 文檔 HTML 頁面。

## 可能的問題和解決方案

### 問題 1: 仍然出現 500 錯誤

**檢查步驟**:
1. 查看 Vercel Dashboard 的部署日誌
2. 檢查 Runtime Logs 中的錯誤訊息
3. 確認 `requirements.txt` 中的依賴都成功安裝

**解決方案**:
- 如果是依賴安裝問題，檢查是否有不相容的套件
- 如果是執行時間超時，考慮升級到 Pro plan
- 如果是記憶體不足，系統會自動使用備用計算引擎

### 問題 2: 占星計算功能不正常

**檢查**:
```bash
curl https://your-app.vercel.app/api/health
```

查看 `real_astro_enabled` 欄位：
- `true`: 真實引擎運作中
- `false`: 使用備用引擎（功能正常但計算較簡化）

**原因**:
- Kerykeion 或 pyswisseph 安裝失敗
- 首次冷啟動時下載天文資料超時

**解決方案**:
- 備用引擎會自動啟用，系統仍可正常運作
- 多次訪問後，真實引擎可能會成功初始化

### 問題 3: 首次請求很慢

**原因**:
- Serverless 冷啟動（正常現象）
- Python 依賴載入需要時間

**解決方案**:
- 這是預期行為
- 後續請求會快很多
- 可考慮使用 Vercel 的保持溫暖功能

## 檔案變更摘要

| 檔案 | 狀態 | 說明 |
|------|------|------|
| vercel.json | 新增 | Vercel 部署配置 |
| api/index.py | 新增 | Serverless function 入口點 |
| .vercelignore | 新增 | 部署時排除的檔案 |
| VERCEL_DEPLOYMENT.md | 新增 | 部署指南 |
| main.py | 修改 | 移除檔案日誌，僅使用 stdout |
| VERCEL_FIX_SUMMARY.md | 新增 | 本檔案 |

## 下一步

1. **重新部署**: 在 Vercel Dashboard 觸發重新部署
2. **測試功能**: 使用上述驗證步驟測試所有端點
3. **監控日誌**: 觀察 Vercel Runtime Logs 確認沒有錯誤
4. **效能優化**: 如需要，考慮：
   - 升級到 Pro plan（更長執行時間）
   - 優化依賴（減少冷啟動時間）
   - 添加快取機制

## 參考資料

- [Vercel Python Runtime 文檔](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Flask WSGI 部署](https://flask.palletsprojects.com/en/latest/deploying/)
- [Serverless Functions 最佳實踐](https://vercel.com/docs/functions/serverless-functions)

---

修復完成時間: 2025-10-29  
修復者: GitHub Copilot  
狀態: ✅ 已完成，等待部署測試
