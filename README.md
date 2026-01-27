# 🌟 虹靈御所占星主角生成系統

> **專業占星計算 × D&D角色生成 × 自我探索工具**

[![GitHub Pages](https://img.shields.io/badge/demo-GitHub%20Pages-brightgreen)](https://your-username.github.io/rainbow-spirit-astro-character/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PWA Ready](https://img.shields.io/badge/PWA-Ready-purple.svg)](#pwa-功能)

## 📖 系統概述

虹靈御所占星主角生成系統是一個革命性的生命敘事工具，以西洋占星為基礎，結合角色扮演遊戲（RPG）概念，讓每個人透過星盤數據清楚理解個人潛能、人格特質與生命方向。

### 🎯 核心理念

傳統占星解讀的困境：
- ❌ 資訊複雜抽象，難以直觀理解
- ❌ 缺乏互動感與實際應用場景  
- ❌ 使用者只能被動接受資訊

虹靈御所的解決方案：
- ✅ 清晰易懂的技能數值化呈現
- ✅ 鼓勵使用者主動探索與互動
- ✅ 加強使用者的代入感與實際應用性

## 🚀 在線演示

| 環境 | 鏈接 | 狀態 |
|------|------|------|
| 🌐 **前端演示** | [GitHub Pages](https://your-username.github.io/rainbow-spirit-astro-character/) | ![Status](https://img.shields.io/website?url=https://your-username.github.io/rainbow-spirit-astro-character/) |
| 🔧 **API 文檔** | [Railway Deploy](https://rainbow-spirit-api.railway.app/api/health) | ![API Status](https://img.shields.io/website?url=https://rainbow-spirit-api.railway.app/api/health) |

## ✨ 功能特色

### 🌟 真實占星計算引擎
- **精確天文計算**：基於 Kerykeion + Swiss Ephemeris
- **10大行星支援**：位置精確到小數點後兩位
- **12宮位系統**：完整的宮位計算
- **逆行狀態檢測**：自動識別行星逆行
- **多時區支援**：全球任意地點計算

### 🎲 D&D角色生成系統
- **六大屬性**：力量、敏捷、體質、智力、智慧、魅力
- **10種職業**：時空守護者、元素法師、心靈治療師等
- **評級系統**：SS、S、A、B、C、D 六個等級
- **專精技能**：根據星盤自動分配技能點
- **角色背景**：150字個性化背景故事生成

### 🌐 開放API供外部調用
- **RESTful API**：標準JSON格式，易於集成
- **跨域支持**：CORS已啟用，支持任何網站調用
- **完整文檔**：提供詳細的API使用文檔和代碼示例
- **多語言示例**：JavaScript、Python、PHP等調用範例
- **無需認證**：公開API，方便快速集成
- **演示頁面**：提供完整的API調用演示

### 📱 PWA 支援
- **離線瀏覽**：無網路時查看已生成內容
- **手機安裝**：可安裝為手機 App
- **推送通知**：個人化占星提醒
- **快速啟動**：桌面快捷方式

### 🎨 現代化 UI/UX
- **響應式設計**：完美支援桌面、平板、手機
- **星空主題**：沉浸式的視覺體驗
- **流暢動畫**：載入動畫與互動效果
- **無障礙設計**：支援螢幕閱讀器

## 🏗️ 技術架構

### 前端技術棧
```
🎨 Frontend
├── HTML5 + CSS3 + JavaScript ES6+
├── PWA (Progressive Web App)
├── Service Worker (離線支援)
├── Responsive Design (響應式設計)
└── Google Fonts (字體優化)
```

### 後端技術棧
```
⚙️ Backend
├── Python 3.9+
├── Flask (Web 框架)
├── Kerykeion (占星計算)
├── Swiss Ephemeris (天文數據)
└── CORS 支援 (跨域請求)
```

### 部署架構
```
🚀 Deployment
├── Frontend: GitHub Pages
├── Backend: Railway / Render / Heroku
├── CDN: CloudFlare (可選)
└── Monitoring: Google Analytics
```

## 📁 文件結構

```
rainbow-spirit-astro-character/
├── 📄 index.html                    # 前端主頁面 (優化版)
├── 📱 site.webmanifest              # PWA 配置
├── 🔧 sw.js                         # Service Worker
├── 🌐 offline.html                  # 離線頁面
├── 📦 assets/                       # 前端資源
│   ├── index-*.css                  # 樣式文件
│   └── index-*.js                   # JavaScript 文件
├── ⚙️ backend/                      # 後端系統
│   ├── astro_web_api.py             # Flask API 服務器
│   ├── astro_consultant.py          # 占星計算引擎
│   ├── dnd_character_generator.py   # D&D角色生成器
│   └── requirements.txt             # Python 依賴
├── 🎨 icons/                        # PWA 圖標
├── 🚀 .github/workflows/deploy.yml  # GitHub Actions
├── 📝 package.json                  # 項目配置
├── 🔧 build.sh                      # 構建腳本
├── 🙈 .gitignore                    # Git 忽略文件
└── 📖 README.md                     # 說明文件
```

## 🚀 快速開始

### 📋 系統要求

- **Python**: 3.8 或更高版本
- **瀏覽器**: Chrome 60+, Firefox 55+, Safari 11+
- **網路**: 初次使用需要網路連接下載天文數據

### 🔧 安裝與運行

#### 1️⃣ 克隆專案
```bash
git clone https://github.com/your-username/rainbow-spirit-astro-character.git
cd rainbow-spirit-astro-character
```

#### 2️⃣ 安裝後端依賴
```bash
cd backend
pip install -r requirements.txt
```

#### 3️⃣ 啟動後端 API
```bash
python astro_web_api.py
```
> 🌐 後端將在 http://localhost:5000 運行

#### 4️⃣ 開啟前端
在瀏覽器中打開 `index.html` 或使用本地服務器：
```bash
# 使用 Python 本地服務器
python -m http.server 8080

# 使用 Node.js live-server (如果已安裝)
npx live-server
```

#### 5️⃣ 開始使用
1. 填寫出生資訊（姓名、日期、時間、地點）
2. 點擊「生成角色」按鈕
3. 等待占星計算完成
4. 查看你的專屬 D&D 角色！

## 🧪 系統測試

### ✅ 內建測試功能

#### 健康檢查
```bash
curl http://localhost:5000/api/health
```

#### 測試數據驗證
```bash
curl http://localhost:5000/api/test
```

### 🔍 真實數據驗證

系統已通過真實占星數據驗證：

**測試案例**：趙偉辰 (1985/10/6 19:30 台北)
- ✅ 太陽: 天秤座 13.15°
- ✅ 月亮: 巨蟹座 4.83°  
- ✅ 所有行星位置與專業占星軟體高度一致

## 📊 API 文檔

### 🌐 供外部網站調用

本系統提供開放的REST API，**任何網站都可以調用**本API進行占星計算和角色生成。

#### 🚀 快速集成

**API基礎URL**：`https://your-domain.com/api`（請替換為實際部署地址）

**特點**：
- ✅ 已啟用CORS，支持跨域請求
- ✅ 無需API密鑰或認證
- ✅ 標準JSON格式
- ✅ 完整錯誤處理

#### 📖 詳細文檔

- 📄 [完整API使用指南](API_USAGE.md) - 包含多語言代碼示例
- 🎨 [API演示頁面](api_demo.html) - 可視化調用示例
- 🏥 API健康檢查：`GET /api/health`
- 🧪 API測試端點：`GET /api/test`

### 🔗 端點列表

| 方法 | 端點 | 描述 |
|------|------|------|
| `GET` | `/api/health` | 健康檢查 |
| `GET` | `/api/test` | 測試功能 |
| `POST` | `/api/calculate_chart` | 星盤計算與角色生成 |

### 📝 請求範例

#### 星盤計算
```javascript
const response = await fetch('/api/calculate_chart', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: "張三",
    year: 1990,
    month: 5,
    day: 15,
    hour: 14,
    minute: 30,
    city: "台北",
    longitude: 121.55,
    latitude: 25.017,
    timezone: "Asia/Taipei"
  })
});

const data = await response.json();
```

#### 回應格式
```json
{
  "success": true,
  "character": {
    "name": "張三",
    "attributes": {
      "strength": 15,
      "dexterity": 13,
      "constitution": 16,
      "intelligence": 14,
      "wisdom": 17,
      "charisma": 18
    },
    "profession": "心靈治療師",
    "rating": "A",
    "background": "你是一位天生的治療者..."
  },
  "astro_data": {
    "sun": {"sign": "金牛座", "degree": 24.35},
    "moon": {"sign": "巨蟹座", "degree": 8.42}
  }
}
```

## 🔥 PWA 功能

### 📱 安裝為 App

**Android / Chrome:**
1. 開啟網站
2. 點擊瀏覽器選單
3. 選擇「新增至主畫面」

**iOS / Safari:**
1. 開啟網站  
2. 點擊分享按鈕
3. 選擇「加入主畫面」

### 🔔 推送通知 (規劃中)
- 每日運勢提醒
- 重要天象通知
- 個人化占星指引

## 🚀 部署指南

### 🌐 前端部署 (GitHub Pages)

#### 自動部署
推送到 `main` 分支會自動觸發 GitHub Actions 部署

#### 手動部署
```bash
# 1. 構建優化
./build.sh

# 2. 推送到 GitHub
git add .
git commit -m "🚀 部署更新"
git push origin main

# 3. 在 GitHub 設置中啟用 Pages
```

### ⚙️ 後端部署

#### Railway 部署 (推薦)
```bash
npm install -g @railway/cli
railway login
cd backend
railway deploy
```

#### Render 部署
1. 連接 GitHub 倉庫
2. 設置構建命令：`cd backend && pip install -r requirements.txt`
3. 設置啟動命令：`cd backend && python astro_web_api.py`

#### Docker 部署
```bash
docker-compose up -d
```

## 🎨 自定義與擴展

### 🔧 修改 API 端點
在 `index.html` 中更新配置：
```javascript
window.RAINBOW_SPIRIT_CONFIG = {
    API_BASE_URL: 'https://your-backend-url.com'
};
```

### 🎨 自定義主題
修改 CSS 變量：
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### 📦 添加新功能
- 在 `backend/dnd_character_generator.py` 中添加新職業
- 在 `backend/astro_consultant.py` 中擴展占星計算
- 在前端添加新的互動元素

## 🐛 故障排除

### ❓ 常見問題

#### Q: API 連接失敗
A: 檢查後端是否在 `localhost:5000` 運行，確認防火牆設置

#### Q: 占星計算錯誤  
A: 確認已安裝所有 Python 依賴，特別是 `kerykeion`

#### Q: PWA 無法安裝
A: 檢查 `site.webmanifest` 文件是否存在，確認使用 HTTPS

#### Q: 離線模式不工作
A: 確認 Service Worker 已註冊，檢查瀏覽器支援

### 🔧 調試模式

開啟瀏覽器開發者工具查看詳細錯誤信息：
```javascript
// 在控制台中啟用調試模式
window.RAINBOW_SPIRIT_CONFIG.DEBUG = true;
```

## 🤝 貢獻指南

### 💡 如何貢獻

1. **Fork** 本項目
2. **創建**功能分支：`git checkout -b feature/AmazingFeature`
3. **提交**更改：`git commit -m 'Add some AmazingFeature'`
4. **推送**到分支：`git push origin feature/AmazingFeature`
5. **開啟** Pull Request

### 🐛 報告問題

使用 [GitHub Issues](https://github.com/your-username/rainbow-spirit-astro-character/issues) 報告：
- 🐛 Bug 回報
- 💡 功能建議
- 📖 文檔改進
- ❓ 使用問題

### 💬 討論社群

- 💬 [GitHub Discussions](https://github.com/your-username/rainbow-spirit-astro-character/discussions)
- 📧 Email: contact@rainbow-spirit.tw
- 🌐 官網: https://rainbow-spirit.tw

## 📄 授權條款

本項目採用 [MIT License](LICENSE) 授權。

```
MIT License

Copyright (c) 2025 虹靈御所團隊

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 👥 開發團隊

### 🌟 核心團隊

- **項目創始人**: [虹靈御所團隊](https://rainbow-spirit.tw)
- **技術架構**: AI + 人類協作開發
- **UI/UX 設計**: 星空主題設計師
- **占星顧問**: 專業占星師團隊

### 🙏 特別感謝

- [Kerykeion](https://github.com/g-battaglia/kerykeion) - 占星計算引擎
- [Swiss Ephemeris](https://www.astro.com/swisseph/) - 天文數據
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- 所有貢獻者和測試用戶

## 📊 專案統計

![GitHub stars](https://img.shields.io/github/stars/your-username/rainbow-spirit-astro-character?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-username/rainbow-spirit-astro-character?style=social)
![GitHub issues](https://img.shields.io/github/issues/your-username/rainbow-spirit-astro-character)
![GitHub license](https://img.shields.io/github/license/your-username/rainbow-spirit-astro-character)

## 🗺️ 發展路線圖

### 🎯 已完成 (v1.0.0)
- ✅ 基礎占星計算引擎
- ✅ D&D 角色生成系統  
- ✅ PWA 支援
- ✅ 響應式設計
- ✅ GitHub Pages 部署

### 🚧 進行中 (v1.1.0)
- 🔄 推送通知系統
- 🔄 多語言支援 (英文)
- 🔄 用戶帳戶系統
- 🔄 角色收藏功能

### 🔮 規劃中 (v2.0.0)
- 🔮 AI 輔助解讀
- 🔮 社群分享功能
- 🔮 付費進階功能
- 🔮 移動 App 版本

## 📈 使用統計 (模擬數據)

| 指標 | 數值 |
|------|------|
| 💫 總計算次數 | 10,000+ |
| 👥 活躍用戶 | 2,500+ |
| 🌍 支援國家 | 50+ |
| ⭐ 用戶評分 | 4.8/5 |

---

<div align="center">

### 🌟 虹靈御所 - 讓占星成為你的人生遊戲升級系統

**認識自己，不需要靠運氣**

[🌐 立即體驗](https://your-username.github.io/rainbow-spirit-astro-character/) | [📖 查看文檔](https://github.com/your-username/rainbow-spirit-astro-character/wiki) | [💬 加入討論](https://github.com/your-username/rainbow-spirit-astro-character/discussions)

Made with ❤️ by [虹靈御所團隊](https://rainbow-spirit.tw)

</div>- **保證可用**：無論環境如何，系統都能正常運行

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

