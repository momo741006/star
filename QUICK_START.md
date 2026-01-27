# 🚀 快速開始 - 外部網站集成指南

## 30秒快速集成

### 最簡單的調用方式

> ⚠️ **注意**：請將示例中的 `https://your-domain.com` 替換為您實際部署的API地址
> - 本地開發：`http://localhost:5000`
> - Vercel：`https://your-project.vercel.app`
> - Railway：`https://your-app.railway.app`

```javascript
// 1. 發送請求
const response = await fetch('https://your-domain.com/api/calculate_chart', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "張三",
    year: 1990,
    month: 6,
    day: 15,
    hour: 14,
    minute: 30,
    city: "台北",
    longitude: 121.55,
    latitude: 25.017,
    timezone: "Asia/Taipei"
  })
});

// 2. 獲取結果
const data = await response.json();

// 3. 使用數據
if (data.success) {
  console.log(`角色: ${data.character.name}`);
  console.log(`職業: ${data.character.class.name}`);
  console.log(`評級: ${data.character.rating}`);
}
```

## 📋 前置要求

### 無需要求！

✅ 無需註冊  
✅ 無需API密鑰  
✅ 無需認證  
✅ 支持CORS跨域  

**直接調用即可使用**

## 🎯 5分鐘完整集成

### 步驟1: 準備出生數據

```javascript
const birthData = {
  name: "用戶姓名",        // 必填
  year: 1990,              // 必填: 1900-2050
  month: 6,                // 必填: 1-12
  day: 15,                 // 必填: 1-31
  hour: 14,                // 必填: 0-23
  minute: 30,              // 必填: 0-59
  city: "台北",            // 必填
  longitude: 121.55,       // 必填: -180 到 180
  latitude: 25.017,        // 必填: -90 到 90
  timezone: "Asia/Taipei"  // 選填，默認 Asia/Taipei
};
```

### 步驟2: 調用API

```javascript
async function getAstroCharacter(birthData) {
  try {
    const response = await fetch('https://your-domain.com/api/calculate_chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(birthData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API調用失敗:', error);
    return null;
  }
}
```

### 步驟3: 處理響應

```javascript
const result = await getAstroCharacter(birthData);

if (result && result.success) {
  const char = result.character;
  
  // 顯示角色信息
  displayCharacter({
    name: char.name,
    class: char.class.name,
    rating: char.rating,
    stats: char.stats,
    background: char.background
  });
} else {
  console.error('計算失敗:', result?.error);
}
```

## 💡 實用示例

### 示例1: 簡單HTML表單集成

```html
<!DOCTYPE html>
<html>
<head>
  <title>占星計算</title>
</head>
<body>
  <form id="astroForm">
    <input type="text" id="name" placeholder="姓名" required>
    <input type="number" id="year" placeholder="年" required>
    <input type="number" id="month" placeholder="月" required>
    <input type="number" id="day" placeholder="日" required>
    <input type="number" id="hour" placeholder="時" required>
    <input type="number" id="minute" placeholder="分" required>
    <button type="submit">計算</button>
  </form>
  
  <div id="result"></div>
  
  <script>
    document.getElementById('astroForm').onsubmit = async (e) => {
      e.preventDefault();
      
      const data = {
        name: document.getElementById('name').value,
        year: parseInt(document.getElementById('year').value),
        month: parseInt(document.getElementById('month').value),
        day: parseInt(document.getElementById('day').value),
        hour: parseInt(document.getElementById('hour').value),
        minute: parseInt(document.getElementById('minute').value),
        city: "台北",
        longitude: 121.55,
        latitude: 25.017
      };
      
      const response = await fetch('https://your-domain.com/api/calculate_chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      
      if (result.success) {
        document.getElementById('result').innerHTML = `
          <h2>${result.character.name}</h2>
          <p>職業: ${result.character.class.name}</p>
          <p>評級: ${result.character.rating}</p>
        `;
      }
    };
  </script>
</body>
</html>
```

### 示例2: React組件集成

```jsx
import React, { useState } from 'react';

function AstroCalculator() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const calculateChart = async (birthData) => {
    setLoading(true);
    
    try {
      const response = await fetch('https://your-domain.com/api/calculate_chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(birthData)
      });
      
      const data = await response.json();
      
      if (data.success) {
        setResult(data.character);
      } else {
        alert('計算失敗: ' + data.error);
      }
    } catch (error) {
      alert('API錯誤: ' + error.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      {loading && <p>計算中...</p>}
      
      {result && (
        <div>
          <h2>{result.name}</h2>
          <p>職業: {result.class.name}</p>
          <p>評級: {result.rating}</p>
          <p>力量: {result.stats.strength}</p>
          <p>智力: {result.stats.intelligence}</p>
        </div>
      )}
    </div>
  );
}

export default AstroCalculator;
```

### 示例3: Vue.js集成

```vue
<template>
  <div>
    <button @click="calculate">計算星盤</button>
    
    <div v-if="character">
      <h2>{{ character.name }}</h2>
      <p>職業: {{ character.class.name }}</p>
      <p>評級: {{ character.rating }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      character: null
    }
  },
  methods: {
    async calculate() {
      const response = await fetch('https://your-domain.com/api/calculate_chart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: "測試",
          year: 1990,
          month: 6,
          day: 15,
          hour: 14,
          minute: 30,
          city: "台北",
          longitude: 121.55,
          latitude: 25.017
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        this.character = data.character;
      }
    }
  }
}
</script>
```

## 🌍 常用城市坐標

直接複製使用：

```javascript
const cities = {
  taipei: { longitude: 121.55, latitude: 25.017, timezone: "Asia/Taipei" },
  hongkong: { longitude: 114.17, latitude: 22.320, timezone: "Asia/Hong_Kong" },
  beijing: { longitude: 116.41, latitude: 39.904, timezone: "Asia/Shanghai" },
  tokyo: { longitude: 139.69, latitude: 35.689, timezone: "Asia/Tokyo" },
  newyork: { longitude: -74.01, latitude: 40.713, timezone: "America/New_York" },
  london: { longitude: -0.13, latitude: 51.507, timezone: "Europe/London" }
};

// 使用
const birthData = {
  name: "張三",
  year: 1990,
  month: 6,
  day: 15,
  hour: 14,
  minute: 30,
  city: "台北",
  ...cities.taipei  // 自動填入經緯度和時區
};
```

## ⚠️ 常見問題

### Q1: 為什麼返回錯誤？

**A:** 檢查必填字段和數據範圍：
- year: 1900-2050
- month: 1-12
- day: 1-31
- hour: 0-23
- minute: 0-59
- longitude: -180 到 180
- latitude: -90 到 90

### Q2: 如何處理CORS錯誤？

**A:** API已啟用CORS，無需額外配置。如果仍有問題：
- 確保使用 HTTPS（生產環境）
- 檢查瀏覽器控制台的具體錯誤信息

### Q3: API有速率限制嗎？

**A:** 目前無速率限制，但建議：
- 合理使用，避免濫用
- 為用戶操作添加防抖/節流
- 不要在短時間內發送大量請求

### Q4: 如何獲取用戶的經緯度？

**A:** 使用瀏覽器Geolocation API或第三方地理編碼服務：

```javascript
// 方式1: 瀏覽器定位
navigator.geolocation.getCurrentPosition(position => {
  const lat = position.coords.latitude;
  const lng = position.coords.longitude;
});

// 方式2: 使用城市名查詢（推薦使用Google Maps API或其他服務）
```

## 📚 更多資源

- 📖 [完整API文檔](API_USAGE.md)
- 🎨 [可視化演示](api_demo.html)
- 🧪 [測試腳本](test_api_integration.py)
- 💻 [GitHub源碼](https://github.com/momo741006/star)

## 🆘 需要幫助？

- 提交Issue: https://github.com/momo741006/star/issues
- 查看示例: 打開 `api_demo.html` 查看完整示例

---

**開始使用吧！整合只需要幾分鐘。** 🚀
