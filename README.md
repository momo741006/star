# 🌟 虹靈御所占星系統 - Railway部署版本

## 📋 部署說明

這是專為Railway平台優化的虹靈御所占星系統版本。

## 🚀 部署步驟

1. **上傳文件到Railway**：
   - 將所有文件上傳到您的Railway項目

2. **自動部署**：
   - Railway會自動檢測到`requirements.txt`和`Procfile`
   - 系統會自動安裝依賴並啟動應用

3. **檢查狀態**：
   - 訪問 `/api/health` 檢查服務狀態
   - 訪問 `/api/test` 測試功能

## 📁 文件說明

- `main.py` - 主應用程序（適配Railway環境）
- `requirements.txt` - Python依賴（簡化版）
- `Procfile` - Railway啟動配置
- `astro_consultant.py` - 占星計算引擎（可選）
- `dnd_character_generator.py` - D&D角色生成器（可選）

## 🔧 智能降級機制

系統具有智能降級機制：
- **優先使用**：真實的Kerykeion占星計算
- **備用方案**：如果Kerykeion無法載入，自動切換到備用計算引擎
- **保證可用**：無論環境如何，系統都能正常運行

## 📊 API端點

- `GET /` - API文檔頁面
- `GET /api/health` - 健康檢查
- `GET /api/test` - 功能測試
- `POST /api/calculate_chart` - 星盤計算

## ⚙️ 環境變量

- `PORT` - 服務端口（Railway自動設置）

## 🎯 特色功能

✅ **自動適配**：根據環境自動選擇最佳計算引擎
✅ **錯誤處理**：完善的錯誤處理和日誌記錄
✅ **CORS支持**：支持跨域請求
✅ **Railway優化**：專為Railway平台優化

---
*Railway部署版本 - 確保在任何環境下都能穩定運行*

