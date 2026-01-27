# 星盤計算 API 增強功能

## 新增功能概述

此更新為占星API添加了完整的專業級星盤計算功能，包括：

### 1. 詳細的行星位置信息

所有行星現在包含以下信息：
- **位置（十進制）**: 精確到小數點後兩位
- **位置（度分秒）**: 傳統格式，例如 `13°09'12"`
- **星座**: 中文星座名稱
- **宮位**: 所在宮位（1-12）
- **逆行狀態**: 是否逆行（℞ 符號）

支持的行星：
- 太陽、月亮、水星、金星、火星、木星、土星、天王星、海王星、冥王星

### 2. 額外占星點位

#### 凱龍星 (Chiron)
- 小行星，代表療癒與創傷
- 包含完整位置和逆行信息

#### 月交點 (Lunar Nodes)
- **北交點 (True North Node)**: 代表靈魂成長方向
- **南交點 (True South Node)**: 代表過去經驗

### 3. 四軸點位（Four Angles）

完整的四軸信息：
- **上升點 (Ascendant)**: 第1宮起點
- **天頂 (Midheaven/MC)**: 第10宮起點
- **下降點 (Descendant)**: 第7宮起點
- **天底 (IC)**: 第4宮起點

### 4. 相位計算 (Aspects)

自動計算所有重要相位，包括：
- **合相 (Conjunction)**: 0°
- **對分相 (Opposition)**: 180°
- **三分相 (Trine)**: 120°
- **四分相 (Square)**: 90°
- **六分相 (Sextile)**: 60°
- 其他次要相位

每個相位包含：
- 涉及的兩個星體（中文名稱）
- 相位類型
- 容許度（實際角度與理論角度的差異）
- 入相/出相狀態

## API 端點

### 1. `/api/calculate_chart` (POST)

主要計算端點，返回完整的星盤數據和D&D角色。

**請求示例：**
```json
{
  "name": "測試用戶",
  "year": 1985,
  "month": 10,
  "day": 6,
  "hour": 19,
  "minute": 30,
  "city": "台北",
  "longitude": 121.55,
  "latitude": 25.017,
  "timezone": "Asia/Taipei"
}
```

**回應示例：**
```json
{
  "success": true,
  "character": { ... },
  "astro_data": {
    "planets": {
      "sun": {
        "name": "太陽",
        "sign": "天秤座",
        "position": 13.15,
        "position_dms": "13°09'12\"",
        "house": 6,
        "retrograde": false
      },
      ...
    },
    "additional_points": {
      "chiron": {
        "name": "凱龍",
        "sign": "雙子座",
        "position_dms": "14°31'32\"",
        "house": 1,
        "retrograde": true
      },
      "north_node": { ... },
      "south_node": { ... }
    },
    "angles": {
      "ascendant": { ... },
      "midheaven": { ... },
      "descendant": { ... },
      "imum_coeli": { ... }
    },
    "aspects": [
      {
        "planet1": "太陽",
        "planet2": "水星",
        "aspect": "合相",
        "orb": 10.0,
        "applying": false
      },
      ...
    ]
  }
}
```

### 2. `/api/formatted_chart` (POST)

返回格式化的文字報告，便於閱讀和顯示。

**回應示例：**
```json
{
  "success": true,
  "formatted_text": "星盤報告...",
  "data": { ... },
  "metadata": {
    "calculation_time": 0.123,
    "engine": "Kerykeion Swiss Ephemeris v4.26.3"
  }
}
```

## 使用示例

### Python

```python
import requests

response = requests.post(
    'http://localhost:5000/api/calculate_chart',
    json={
        "name": "張三",
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "city": "台北",
        "longitude": 121.55,
        "latitude": 25.017,
        "timezone": "Asia/Taipei"
    }
)

data = response.json()
if data['success']:
    # 訪問行星數據
    sun = data['astro_data']['planets']['sun']
    print(f"太陽位置: {sun['sign']} {sun['position_dms']}")
    
    # 訪問相位
    for aspect in data['astro_data']['aspects'][:5]:
        print(f"{aspect['planet1']} {aspect['aspect']} {aspect['planet2']}")
```

### JavaScript

```javascript
fetch('http://localhost:5000/api/calculate_chart', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: "李四",
    year: 1995,
    month: 8,
    day: 20,
    hour: 10,
    minute: 30,
    city: "台北",
    longitude: 121.55,
    latitude: 25.017,
    timezone: "Asia/Taipei"
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    // 訪問星盤數據
    console.log('行星位置:', data.astro_data.planets);
    console.log('相位:', data.astro_data.aspects);
  }
});
```

## 測試

運行測試以驗證功能：

```bash
python3 test_enhanced_api.py
```

## 技術細節

### 計算引擎
- **Kerykeion 4.26.3**: Python 占星計算庫
- **Swiss Ephemeris**: 高精度天文曆表

### 精確度
- 行星位置精確到秒（約 0.0003°）
- 使用真實北交點（不是平均值）
- 考慮所有主要和次要相位

### 性能
- 平均計算時間: 0.01-0.05秒
- 包含完整相位計算: 0.02-0.15秒
- 支持並發請求

## 更新歷史

### v2.1.0 (2025-01)
- ✅ 添加度分秒格式支持
- ✅ 添加凱龍星位置
- ✅ 添加月交點（北交/南交）
- ✅ 添加完整四軸點位
- ✅ 添加相位計算
- ✅ 添加格式化輸出端點

### v2.0.0
- 基礎占星計算
- D&D角色生成
- PWA支援

## 問題回報

如有任何問題或建議，請提交 Issue。
