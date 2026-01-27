# 🌟 虹靈御所占星API - 外部調用指南

## 📖 簡介

虹靈御所占星API提供專業的占星計算和D&D角色生成服務，可供任何網站或應用程序調用。本API基於Kerykeion和Swiss Ephemeris天文引擎，提供高精度的星盤計算。

## 🚀 快速開始

### API 基礎信息

- **API 基礎URL**: `https://your-domain.com/api` 
  
  > ⚠️ **重要**：請將 `your-domain.com` 替換為您實際部署的域名
  > 
  > - 本地開發：`http://localhost:5000/api`
  > - Vercel部署：`https://your-project.vercel.app/api`
  > - Railway部署：`https://your-app.railway.app/api`

- **支持格式**: JSON
- **字符編碼**: UTF-8
- **CORS**: ✅ 已啟用，支持跨域請求
- **認證**: 無需認證（公開API）
- **速率限制**: 建議合理使用

## 📡 API 端點

### 1. 健康檢查

檢查API服務狀態

**端點**: `GET /api/health`

**請求示例**:
```bash
curl https://your-domain.com/api/health
```

**響應示例**:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "engine": "Kerykeion Swiss Ephemeris v4.26.3",
  "real_astro_enabled": true,
  "uptime_seconds": 3600,
  "request_count": 150,
  "success_rate": 99.5
}
```

### 2. 星盤計算與角色生成

根據出生信息計算星盤並生成D&D角色

**端點**: `POST /api/calculate_chart`

**請求參數**:

| 參數 | 類型 | 必填 | 說明 | 範圍/格式 |
|------|------|------|------|-----------|
| name | string | 是 | 姓名 | 任意字符串 |
| year | integer | 是 | 出生年份 | 1900-2050 |
| month | integer | 是 | 出生月份 | 1-12 |
| day | integer | 是 | 出生日期 | 1-31 |
| hour | integer | 是 | 出生小時 | 0-23 |
| minute | integer | 是 | 出生分鐘 | 0-59 |
| city | string | 是 | 出生城市 | 任意字符串 |
| longitude | float | 是 | 經度 | -180 到 180 |
| latitude | float | 是 | 緯度 | -90 到 90 |
| timezone | string | 否 | 時區 | 默認: "Asia/Taipei" |

**請求示例 (cURL)**:
```bash
curl -X POST https://your-domain.com/api/calculate_chart \
  -H "Content-Type: application/json" \
  -d '{
    "name": "張三",
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "city": "台北",
    "longitude": 121.55,
    "latitude": 25.017,
    "timezone": "Asia/Taipei"
  }'
```

**成功響應** (HTTP 200):
```json
{
  "success": true,
  "character": {
    "name": "張三",
    "class": {
      "name": "聖騎士",
      "description": "正義的戰士，以神聖之力守護盟友",
      "match_score": 0.85
    },
    "stats": {
      "strength": 16,
      "dexterity": 12,
      "constitution": 15,
      "intelligence": 13,
      "wisdom": 14,
      "charisma": 17
    },
    "total_stats": 87,
    "rating": "A",
    "background": "你是一位天生的領袖...",
    "birth_chart": {
      "sun": "雙子座 第10宮",
      "moon": "天蠍座 第3宮",
      "ascendant": "天秤座"
    }
  },
  "astro_data": {
    "planets": {
      "sun": {
        "sign": "雙子座",
        "degree": 24.5,
        "house": 10,
        "retrograde": false
      },
      "moon": {...},
      "mercury": {...}
    },
    "houses": {...},
    "angles": {...}
  },
  "metadata": {
    "calculation_time": 0.156,
    "engine": "Kerykeion Swiss Ephemeris v4.26.3",
    "timestamp": "2026-01-27T10:00:00Z",
    "request_id": "1706353200-123"
  }
}
```

**錯誤響應** (HTTP 400/500):
```json
{
  "success": false,
  "error": "錯誤描述",
  "error_code": "VALIDATION_ERROR",
  "validation_errors": [
    "年份必須在1900-2050之間"
  ]
}
```

### 3. 系統測試

使用預設數據測試API功能

**端點**: `GET /api/test`

**請求示例**:
```bash
curl https://your-domain.com/api/test
```

## 💻 代碼示例

### JavaScript / Fetch API

```javascript
async function calculateAstroChart(birthData) {
  try {
    const response = await fetch('https://your-domain.com/api/calculate_chart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: birthData.name,
        year: birthData.year,
        month: birthData.month,
        day: birthData.day,
        hour: birthData.hour,
        minute: birthData.minute,
        city: birthData.city,
        longitude: birthData.longitude,
        latitude: birthData.latitude,
        timezone: birthData.timezone || 'Asia/Taipei'
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.success) {
      console.log('角色名稱:', data.character.name);
      console.log('職業:', data.character.class.name);
      console.log('屬性:', data.character.stats);
      console.log('評級:', data.character.rating);
      return data;
    } else {
      console.error('計算失敗:', data.error);
      return null;
    }
  } catch (error) {
    console.error('API調用錯誤:', error);
    return null;
  }
}

// 使用示例
const birthData = {
  name: "測試用戶",
  year: 1990,
  month: 6,
  day: 15,
  hour: 14,
  minute: 30,
  city: "台北",
  longitude: 121.55,
  latitude: 25.017,
  timezone: "Asia/Taipei"
};

calculateAstroChart(birthData).then(result => {
  if (result) {
    console.log('完整結果:', result);
  }
});
```

### JavaScript / jQuery

```javascript
function calculateAstroChart(birthData) {
  $.ajax({
    url: 'https://your-domain.com/api/calculate_chart',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(birthData),
    success: function(data) {
      if (data.success) {
        console.log('角色:', data.character);
        // 處理成功響應
        displayCharacter(data.character);
      } else {
        console.error('計算失敗:', data.error);
      }
    },
    error: function(xhr, status, error) {
      console.error('API錯誤:', error);
    }
  });
}

// 使用示例
calculateAstroChart({
  name: "測試用戶",
  year: 1990,
  month: 6,
  day: 15,
  hour: 14,
  minute: 30,
  city: "台北",
  longitude: 121.55,
  latitude: 25.017,
  timezone: "Asia/Taipei"
});
```

### Python / Requests

```python
import requests
import json

def calculate_astro_chart(birth_data):
    """
    調用占星API計算星盤
    
    Args:
        birth_data (dict): 出生信息
        
    Returns:
        dict: API響應數據
    """
    url = 'https://your-domain.com/api/calculate_chart'
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, json=birth_data, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('success'):
            print(f"角色名稱: {data['character']['name']}")
            print(f"職業: {data['character']['class']['name']}")
            print(f"屬性: {data['character']['stats']}")
            print(f"評級: {data['character']['rating']}")
            return data
        else:
            print(f"計算失敗: {data.get('error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"API調用錯誤: {e}")
        return None

# 使用示例
birth_data = {
    "name": "測試用戶",
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "city": "台北",
    "longitude": 121.55,
    "latitude": 25.017,
    "timezone": "Asia/Taipei"
}

result = calculate_astro_chart(birth_data)
if result:
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

### PHP / cURL

```php
<?php

function calculateAstroChart($birthData) {
    $url = 'https://your-domain.com/api/calculate_chart';
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json'
    ));
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($birthData));
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode == 200) {
        $data = json_decode($response, true);
        
        if ($data['success']) {
            echo "角色名稱: " . $data['character']['name'] . "\n";
            echo "職業: " . $data['character']['class']['name'] . "\n";
            echo "評級: " . $data['character']['rating'] . "\n";
            return $data;
        } else {
            echo "計算失敗: " . $data['error'] . "\n";
            return null;
        }
    } else {
        echo "HTTP錯誤: " . $httpCode . "\n";
        return null;
    }
}

// 使用示例
$birthData = array(
    "name" => "測試用戶",
    "year" => 1990,
    "month" => 6,
    "day" => 15,
    "hour" => 14,
    "minute" => 30,
    "city" => "台北",
    "longitude" => 121.55,
    "latitude" => 25.017,
    "timezone" => "Asia/Taipei"
);

$result = calculateAstroChart($birthData);
if ($result) {
    print_r($result);
}
?>
```

## 🛡️ 錯誤處理

### 錯誤碼對照表

| 錯誤碼 | 說明 | 解決方案 |
|--------|------|----------|
| VALIDATION_ERROR | 輸入數據驗證失敗 | 檢查所有必填字段和數據範圍 |
| MISSING_REQUIRED_FIELDS | 缺少必填字段 | 確保提供所有必填參數 |
| CALCULATION_ERROR | 計算過程錯誤 | 檢查輸入數據的有效性 |
| INTERNAL_ERROR | 服務器內部錯誤 | 聯繫技術支持 |
| RESOURCE_NOT_FOUND | 資源不存在 | 檢查API端點URL |
| REQUEST_TOO_LARGE | 請求數據過大 | 減小請求體積（最大16MB）|
| INVALID_CONTENT_TYPE | 無效的內容類型 | 使用 application/json |

### 錯誤處理最佳實踐

```javascript
async function safeApiCall(birthData) {
  try {
    const response = await fetch('https://your-domain.com/api/calculate_chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(birthData)
    });

    const data = await response.json();

    if (!response.ok) {
      // HTTP錯誤處理
      switch (response.status) {
        case 400:
          console.error('請求錯誤:', data.error);
          if (data.validation_errors) {
            console.error('驗證錯誤:', data.validation_errors);
          }
          break;
        case 500:
          console.error('服務器錯誤:', data.error);
          break;
        default:
          console.error('未知錯誤:', data.error);
      }
      return null;
    }

    if (!data.success) {
      // 業務邏輯錯誤
      console.error('計算失敗:', data.error);
      console.error('錯誤碼:', data.error_code);
      return null;
    }

    return data;

  } catch (error) {
    // 網絡錯誤或JSON解析錯誤
    console.error('API調用異常:', error.message);
    return null;
  }
}
```

## 🔒 安全建議

1. **HTTPS**: 生產環境請使用HTTPS協議
2. **輸入驗證**: 在客戶端也進行數據驗證，減少無效請求
3. **錯誤處理**: 妥善處理所有可能的錯誤情況
4. **超時設置**: 設置合理的請求超時時間（建議30秒）
5. **速率限制**: 避免短時間內大量請求

## 📊 常見城市坐標參考

| 城市 | 經度 | 緯度 |
|------|------|------|
| 台北 | 121.55 | 25.017 |
| 台中 | 120.68 | 24.147 |
| 高雄 | 120.31 | 22.620 |
| 香港 | 114.17 | 22.320 |
| 北京 | 116.41 | 39.904 |
| 上海 | 121.47 | 31.230 |
| 東京 | 139.69 | 35.689 |
| 首爾 | 126.98 | 37.566 |
| 新加坡 | 103.82 | 1.352 |
| 紐約 | -74.01 | 40.713 |
| 倫敦 | -0.13 | 51.507 |
| 巴黎 | 2.35 | 48.857 |

## 🌍 時區參考

常用時區字符串：
- 台灣: `Asia/Taipei`
- 香港: `Asia/Hong_Kong`
- 中國: `Asia/Shanghai`
- 日本: `Asia/Tokyo`
- 韓國: `Asia/Seoul`
- 新加坡: `Asia/Singapore`
- 美國東部: `America/New_York`
- 美國西部: `America/Los_Angeles`
- 英國: `Europe/London`
- 法國: `Europe/Paris`

完整時區列表: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## 📞 技術支持

- **GitHub**: https://github.com/momo741006/star
- **問題報告**: https://github.com/momo741006/star/issues
- **API文檔**: 訪問API根路徑查看完整文檔

## 📝 使用條款

本API免費提供使用，請遵守以下條款：

1. 合理使用，避免濫用或惡意請求
2. 不得用於非法用途
3. 建議在應用中註明數據來源
4. API可能會有更新，請關注文檔變更

## 🔄 版本歷史

### v2.0.0 (當前版本)
- 完整的星盤計算功能
- D&D角色生成系統
- CORS跨域支持
- 詳細的錯誤處理
- 性能優化

---

**祝您使用愉快！如有任何問題，歡迎提交Issue。**
