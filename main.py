#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌟 虹靈御所占星主角生成系統 v2.0
Enhanced Railway Deployment Version

增強功能：
- 完整的API文檔
- 改進的錯誤處理 
- 增強的日誌記錄
- 更好的效能監控
- 健康檢查端點
"""

import os
import sys
import time
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
import traceback

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log') if os.path.exists('.') else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=['*'])

# Railway端口配置
port = int(os.environ.get("PORT", 5000))

# 應用配置
app.config.update({
    'JSON_AS_ASCII': False,
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
})

# 全域變數
app_start_time = datetime.now()
request_count = 0
error_count = 0

# 嘗試導入真實的占星計算引擎
try:
    from astro_consultant import ProfessionalAstrologer
    from dnd_character_generator import DnDCharacterGenerator

    astrologer = ProfessionalAstrologer()
    dnd_generator = DnDCharacterGenerator()
    USE_REAL_ASTRO = True
    ENGINE_STATUS = "Kerykeion Swiss Ephemeris v4.26.3"
    logger.info("✅ 真實占星計算引擎載入成功")

except ImportError as e:
    logger.warning(f"⚠️ 無法載入真實占星引擎: {e}")
    logger.info("🔄 使用備用計算方案")
    USE_REAL_ASTRO = False
    ENGINE_STATUS = "備用計算引擎 v1.0"

    # 導入備用模組
    import random
    from datetime import datetime

# 請求計數中間件
@app.before_request
def before_request():
    global request_count
    request_count += 1

    # 記錄API請求
    if request.path.startswith('/api/'):
        logger.info(f"API請求: {request.method} {request.path} - IP: {request.remote_addr}")

# 錯誤處理中間件
@app.after_request
def after_request(response):
    # 添加安全標頭
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY' 
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # 記錄回應狀態
    if response.status_code >= 400:
        global error_count
        error_count += 1
        logger.warning(f"錯誤回應: {response.status_code} - {request.path}")

    return response

# 全域錯誤處理器
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404錯誤: {request.path}")
    return jsonify({
        'success': False,
        'error': '請求的資源不存在',
        'error_code': 'RESOURCE_NOT_FOUND',
        'timestamp': datetime.now().isoformat(),
        'path': request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"內部服務器錯誤: {str(error)}")
    return jsonify({
        'success': False,
        'error': '內部服務器錯誤',
        'error_code': 'INTERNAL_ERROR',
        'timestamp': datetime.now().isoformat()
    }), 500

@app.errorhandler(413)
def request_too_large(error):
    return jsonify({
        'success': False,
        'error': '請求資料過大',
        'error_code': 'REQUEST_TOO_LARGE',
        'max_size': '16MB'
    }), 413

# ==================== API端點 ====================

@app.route('/')
def index():
    """
    🏠 主頁面 - API文檔和系統狀態
    """
    uptime = datetime.now() - app_start_time
    hours = uptime.total_seconds() // 3600
    minutes = (uptime.total_seconds() % 3600) // 60

    api_docs = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌟 虹靈御所 API 文檔</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6; 
                margin: 0; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .header { text-align: center; margin-bottom: 2rem; }
            .status { 
                background: rgba(255,255,255,0.1); 
                padding: 1rem; 
                border-radius: 8px; 
                margin: 1rem 0; 
            }
            .endpoint { 
                background: rgba(255,255,255,0.05); 
                margin: 1rem 0; 
                padding: 1rem; 
                border-radius: 8px;
                border-left: 4px solid #6366f1;
            }
            .method { 
                padding: 0.3rem 0.8rem; 
                border-radius: 4px; 
                font-weight: bold; 
                display: inline-block;
                margin-right: 1rem;
            }
            .get { background-color: #10b981; }
            .post { background-color: #f59e0b; }
            .code { 
                background: rgba(0,0,0,0.3); 
                padding: 1rem; 
                border-radius: 4px; 
                overflow-x: auto;
                font-family: 'Courier New', monospace;
            }
            h1, h2, h3 { color: #ffffff; }
            a { color: #60a5fa; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌟 虹靈御所占星主角生成系統</h1>
                <p>Professional Astrology API & D&D Character Generator</p>
                <p><strong>版本:</strong> v2.0.0 | <strong>狀態:</strong> ✅ 運行中</p>
            </div>

            <div class="status">
                <h2>📊 系統狀態</h2>
                <ul>
                    <li><strong>計算引擎:</strong> {{ engine_status }}</li>
                    <li><strong>部署平台:</strong> Railway/Heroku Compatible</li>
                    <li><strong>運行時間:</strong> {{ hours }}小時 {{ minutes }}分鐘</li>
                    <li><strong>請求總數:</strong> {{ request_count }}</li>
                    <li><strong>錯誤次數:</strong> {{ error_count }}</li>
                    <li><strong>成功率:</strong> {{ success_rate }}%</li>
                </ul>
            </div>

            <div class="status">
                <h2>🚀 快速開始</h2>
                <div class="code">
# 健康檢查
curl {{ base_url }}/api/health

# 角色生成範例  
curl -X POST {{ base_url }}/api/calculate_chart \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
                </div>
            </div>

            <h2>📡 API 端點</h2>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/health</strong>
                <p>系統健康檢查，返回服務狀態和基本資訊</p>
                <div class="code">
{
  "status": "healthy",
  "engine": "Kerykeion Swiss Ephemeris",
  "version": "2.0.0",
  "uptime_seconds": 3600,
  "request_count": 150
}
                </div>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/test</strong>
                <p>系統功能測試，使用預設資料測試占星計算和角色生成</p>
            </div>

            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/calculate_chart</strong>
                <p>主要功能 - 根據出生資訊計算星盤並生成D&D角色</p>

                <h4>📝 請求參數</h4>
                <div class="code">
{
  "name": "string",        // 必填 - 姓名
  "year": "integer",       // 必填 - 出生年份 (1900-2050)
  "month": "integer",      // 必填 - 出生月份 (1-12)
  "day": "integer",        // 必填 - 出生日期 (1-31)
  "hour": "integer",       // 必填 - 出生時間-時 (0-23)
  "minute": "integer",     // 必填 - 出生時間-分 (0-59)
  "city": "string",        // 必填 - 出生城市
  "longitude": "float",    // 必填 - 經度 (-180 to 180)
  "latitude": "float",     // 必填 - 緯度 (-90 to 90)
  "timezone": "string"     // 選填 - 時區 (預設: Asia/Taipei)
}
                </div>

                <h4>✅ 成功回應</h4>
                <div class="code">
{
  "success": true,
  "character": {
    "name": "測試用戶",
    "class": {
      "name": "聖騎士",
      "description": "正義的戰士...",
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
    "background": "150字角色背景故事...",
    "birth_chart": {
      "sun": "雙子座 第10宮",
      "moon": "天蠍座 第3宮",
      "ascendant": "處女座"
    }
  },
  "astro_data": {
    "planets": { /* 詳細行星數據 */ },
    "houses": { /* 宮位資訊 */ }
  },
  "metadata": {
    "calculation_time": 0.156,
    "engine": "Kerykeion",
    "timestamp": "2025-08-25T01:00:00Z"
  }
}
                </div>

                <h4>❌ 錯誤回應</h4>
                <div class="code">
{
  "success": false,
  "error": "錯誤訊息",
  "error_code": "VALIDATION_ERROR",
  "details": {
    "field": "year",
    "message": "年份必須在1900-2050之間"
  }
}
                </div>
            </div>

            <div class="status">
                <h2>🔧 技術規格</h2>
                <ul>
                    <li><strong>框架:</strong> Flask 3.1.1</li>
                    <li><strong>占星引擎:</strong> Kerykeion 4.26.3 + Swiss Ephemeris</li>
                    <li><strong>CORS:</strong> ✅ 支援跨域請求</li>
                    <li><strong>速率限制:</strong> 無限制 (建議合理使用)</li>
                    <li><strong>資料格式:</strong> JSON</li>
                    <li><strong>字元編碼:</strong> UTF-8</li>
                    <li><strong>最大請求大小:</strong> 16MB</li>
                </ul>
            </div>

            <div class="status">
                <h2>🛡️ 錯誤碼對照</h2>
                <ul>
                    <li><code>VALIDATION_ERROR</code> - 輸入資料驗證失敗</li>
                    <li><code>CALCULATION_ERROR</code> - 占星計算過程錯誤</li>
                    <li><code>INTERNAL_ERROR</code> - 內部服務器錯誤</li>
                    <li><code>RESOURCE_NOT_FOUND</code> - 請求的資源不存在</li>
                    <li><code>REQUEST_TOO_LARGE</code> - 請求資料過大</li>
                </ul>
            </div>

            <div class="status">
                <h2>📞 支援資訊</h2>
                <p>
                    <strong>開發團隊:</strong> 虹靈御所<br>
                    <strong>技術支援:</strong> <a href="https://github.com/rainbow-spirit/astro-character">GitHub Repository</a><br>
                    <strong>文檔更新:</strong> {{ current_time }}
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    success_rate = round(((request_count - error_count) / max(request_count, 1)) * 100, 1)

    return render_template_string(api_docs,
        engine_status=ENGINE_STATUS,
        hours=int(hours),
        minutes=int(minutes),
        request_count=request_count,
        error_count=error_count,
        success_rate=success_rate,
        base_url=request.url_root.rstrip('/'),
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/api/health')
def health_check():
    """
    🏥 健康檢查端點
    返回系統狀態和運行資訊
    """
    try:
        uptime_seconds = (datetime.now() - app_start_time).total_seconds()

        health_data = {
            'status': 'healthy',
            'version': '2.0.0',
            'engine': ENGINE_STATUS,
            'real_astro_enabled': USE_REAL_ASTRO,
            'uptime_seconds': round(uptime_seconds),
            'request_count': request_count,
            'error_count': error_count,
            'success_rate': round(((request_count - error_count) / max(request_count, 1)) * 100, 1),
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'python_version': sys.version,
                'platform': sys.platform,
                'port': port
            }
        }

        logger.info("健康檢查完成")
        return jsonify(health_data)

    except Exception as e:
        logger.error(f"健康檢查失敗: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/calculate_chart', methods=['POST'])
def calculate_chart():
    """
    🎲 主要功能 - 計算星盤並生成D&D角色
    """
    start_time = time.time()

    try:
        # 驗證請求格式
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': '請求必須是JSON格式',
                'error_code': 'INVALID_CONTENT_TYPE'
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '請求body不能為空',
                'error_code': 'EMPTY_REQUEST'
            }), 400

        # 驗證必填欄位
        required_fields = ['name', 'year', 'month', 'day', 'hour', 'minute', 'city', 'longitude', 'latitude']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'缺少必填欄位: {", ".join(missing_fields)}',
                'error_code': 'MISSING_REQUIRED_FIELDS',
                'missing_fields': missing_fields
            }), 400

        # 資料類型和範圍驗證
        validation_errors = []

        # 年份驗證
        try:
            year = int(data['year'])
            if not (1900 <= year <= 2050):
                validation_errors.append('年份必須在1900-2050之間')
        except (ValueError, TypeError):
            validation_errors.append('年份必須是數字')

        # 月份驗證  
        try:
            month = int(data['month'])
            if not (1 <= month <= 12):
                validation_errors.append('月份必須在1-12之間')
        except (ValueError, TypeError):
            validation_errors.append('月份必須是數字')

        # 日期驗證
        try:
            day = int(data['day'])
            if not (1 <= day <= 31):
                validation_errors.append('日期必須在1-31之間')
        except (ValueError, TypeError):
            validation_errors.append('日期必須是數字')

        # 時間驗證
        try:
            hour = int(data['hour'])
            if not (0 <= hour <= 23):
                validation_errors.append('小時必須在0-23之間')
        except (ValueError, TypeError):
            validation_errors.append('小時必須是數字')

        try:
            minute = int(data['minute'])
            if not (0 <= minute <= 59):
                validation_errors.append('分鐘必須在0-59之間')
        except (ValueError, TypeError):
            validation_errors.append('分鐘必須是數字')

        # 經緯度驗證
        try:
            longitude = float(data['longitude'])
            if not (-180 <= longitude <= 180):
                validation_errors.append('經度必須在-180到180之間')
        except (ValueError, TypeError):
            validation_errors.append('經度必須是數字')

        try:
            latitude = float(data['latitude'])
            if not (-90 <= latitude <= 90):
                validation_errors.append('緯度必須在-90到90之間')
        except (ValueError, TypeError):
            validation_errors.append('緯度必須是數字')

        if validation_errors:
            return jsonify({
                'success': False,
                'error': '資料驗證失敗',
                'error_code': 'VALIDATION_ERROR',
                'validation_errors': validation_errors
            }), 400

        # 執行計算
        logger.info(f"開始為用戶 {data['name']} 計算星盤和角色")

        if USE_REAL_ASTRO:
            result = calculate_with_real_engine(data)
        else:
            result = calculate_with_backup_engine(data)

        calculation_time = time.time() - start_time

        # 添加元數據
        result['metadata'] = {
            'calculation_time': round(calculation_time, 3),
            'engine': ENGINE_STATUS,
            'timestamp': datetime.now().isoformat(),
            'request_id': f"{int(time.time())}-{hash(data['name']) % 1000:03d}"
        }

        logger.info(f"角色生成完成，用時 {calculation_time:.3f}秒")
        return jsonify(result)

    except Exception as e:
        calculation_time = time.time() - start_time
        error_msg = str(e)
        logger.error(f"角色生成失敗: {error_msg}")
        logger.error(f"錯誤詳情: {traceback.format_exc()}")

        return jsonify({
            'success': False,
            'error': '角色生成過程中發生錯誤',
            'error_code': 'CALCULATION_ERROR',
            'details': error_msg if app.debug else '內部錯誤',
            'calculation_time': round(calculation_time, 3),
            'timestamp': datetime.now().isoformat()
        }), 500

def calculate_with_real_engine(data):
    """使用真實占星引擎進行計算"""
    # 計算星盤
    chart_data = astrologer.calculate_natal_chart(
        data['name'], 
        int(data['year']), 
        int(data['month']), 
        int(data['day']),
        int(data['hour']), 
        int(data['minute']), 
        data['city'],
        float(data['longitude']), 
        float(data['latitude']), 
        data.get('timezone', 'Asia/Taipei')
    )

    # 生成D&D角色
    character = dnd_generator.generate_complete_character(chart_data)

    return {
        'success': True,
        'character': character,
        'astro_data': {
            'planets': chart_data['planets'],
            'houses': chart_data['houses'],
            'angles': chart_data['angles']
        }
    }

def calculate_with_backup_engine(data):
    """使用備用計算引擎"""
    # 實作備用計算邏輯
    # (這部分可以保持原有的備用邏輯)
    pass

@app.route('/api/test')
def test_system():
    """
    🧪 系統測試端點
    使用預設資料測試系統功能
    """
    try:
        test_data = {
            "name": "系統測試用戶",
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

        logger.info("執行系統測試")
        start_time = time.time()

        if USE_REAL_ASTRO:
            result = calculate_with_real_engine(test_data)
        else:
            result = calculate_with_backup_engine(test_data)

        test_time = time.time() - start_time

        result['test_info'] = {
            'test_passed': True,
            'test_time': round(test_time, 3),
            'engine_used': ENGINE_STATUS,
            'test_timestamp': datetime.now().isoformat()
        }

        logger.info(f"系統測試完成，用時 {test_time:.3f}秒")
        return jsonify(result)

    except Exception as e:
        logger.error(f"系統測試失敗: {str(e)}")
        return jsonify({
            'success': False,
            'test_passed': False,
            'error': '系統測試失敗',
            'error_details': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# 靜態檔案支援 (如果需要)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    logger.info(f"🌟 虹靈御所占星系統 v2.0 啟動中...")
    logger.info(f"🔧 計算引擎: {ENGINE_STATUS}")
    logger.info(f"🌐 端口: {port}")
    logger.info(f"📱 CORS: 已啟用")

    try:
        app.run(
            host="0.0.0.0", 
            port=port, 
            debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true"
        )
    except Exception as e:
        logger.error(f"應用啟動失敗: {str(e)}")
        sys.exit(1)    
    # 基於星盤的屬性生成
    stats = {}
    for stat in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
        base_value = 8 + (hash(f"{stat}{data.get('name', 'default')}{month}{day}") % 11)
        stats[stat] = base_value
    
    total_stats = sum(stats.values())
    
    # 評級
    if total_stats >= 100:
        rating = "SS"
    elif total_stats >= 90:
        rating = "S"
    elif total_stats >= 80:
        rating = "A"
    elif total_stats >= 70:
        rating = "B"
    elif total_stats >= 60:
        rating = "C"
    else:
        rating = "D"
    
    # 技能
    all_skills = [
        "運動", "欺瞞", "歷史", "洞察", "威嚇", "調查",
        "醫療", "自然", "察覺", "表演", "說服", "宗教",
        "巧手", "隱匿", "求生", "動物馴養", "奧秘", "特技"
    ]
    
    skill_count = 3 + (hash(f"skills{data.get('name', 'default')}") % 4)
    skills = random.sample(all_skills, skill_count)
    
    # 背景故事
    name = data.get('name', '冒險者')
    sun_sign = planets['sun']['sign']
    
    backgrounds = [
        f"{name}是一位{class_choice['name']}，{class_choice['description']}。",
        f"出生在{sun_sign}的影響下，{name}展現出獨特的個性特質。",
        f"從小就對冒險充滿渴望，{name}踏上了成為英雄的道路。",
        f"憑藉著{random.choice(['勇氣', '智慧', '魅力', '堅韌'])}，{name}在各種挑戰中脫穎而出。",
        f"如今，{name}已經成為一位經驗豐富的冒險者，準備面對更大的挑戰。"
    ]
    
    background = "".join(backgrounds)
    
    return {
        'birth_chart': {
            'planets': planets,
            'houses': {f'house_{i}': ZODIAC_SIGNS[(i-1) % 12] for i in range(1, 13)}
        },
        'dnd_character': {
            'name': name,
            'class': class_choice,
            'stats': stats,
            'total_stats': total_stats,
            'rating': rating,
            'skills': skills,
            'background': background
        }
    }

@app.route('/')
def index():
    """主頁面"""
    engine_info = "Kerykeion Swiss Ephemeris" if USE_REAL_ASTRO else "備用計算引擎"
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>虹靈御所占星系統 API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #ffd700; text-align: center; }
        .endpoint { background: #16213e; padding: 20px; margin: 20px 0; border-radius: 8px; }
        .method { color: #4CAF50; font-weight: bold; }
        .url { color: #2196F3; font-family: monospace; }
        .description { margin: 10px 0; }
        .example { background: #0f3460; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .status { background: #2d5a27; padding: 10px; border-radius: 4px; margin: 20px 0; }
        pre { overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 虹靈御所占星系統 API</h1>
        
        <div class="status">
            <h3>🚀 系統狀態</h3>
            <p><strong>計算引擎:</strong> {{ engine_info }}</p>
            <p><strong>部署平台:</strong> Railway</p>
            <p><strong>服務狀態:</strong> ✅ 運行中</p>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/api/calculate_chart</span></h3>
            <div class="description">計算完整星盤並生成D&D角色</div>
            <div class="example">
                <strong>請求參數:</strong>
                <pre>{
  "name": "角色名稱",
  "year": 1985,
  "month": 10,
  "day": 6,
  "hour": 19,
  "minute": 30,
  "city": "台北",
  "longitude": 121.55,
  "latitude": 25.017,
  "timezone": "Asia/Taipei"
}</pre>
            </div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/health</span></h3>
            <div class="description">檢查API健康狀態</div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/api/test</span></h3>
            <div class="description">測試系統功能</div>
        </div>
        
        <p style="text-align: center; margin-top: 40px; color: #888;">
            Powered by Flask & Professional Astrology
        </p>
    </div>
</body>
</html>
    """, engine_info=engine_info)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'message': '虹靈御所占星系統運行正常',
        'version': '1.0.0',
        'engine': 'Kerykeion Swiss Ephemeris' if USE_REAL_ASTRO else '備用計算引擎',
        'platform': 'Railway',
        'port': port
    })

@app.route('/api/calculate_chart', methods=['POST'])
def calculate_chart():
    """計算星盤並生成D&D角色"""
    try:
        data = request.get_json()
        
        # 驗證必要參數
        required_fields = ['name', 'year', 'month', 'day', 'hour', 'minute']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必要參數: {field}'
                }), 400
        
        print(f"🌟 計算星盤: {data['name']} - {data['year']}/{data['month']}/{data['day']} {data['hour']}:{data['minute']}")
        
        if USE_REAL_ASTRO:
            # 使用真實占星計算
            chart_data = astrologer.calculate_natal_chart(
                name=data['name'],
                year=int(data['year']),
                month=int(data['month']),
                day=int(data['day']),
                hour=int(data['hour']),
                minute=int(data['minute']),
                city=data.get('city', '台北'),
                longitude=float(data.get('longitude', 121.55)),
                latitude=float(data.get('latitude', 25.017)),
                timezone=data.get('timezone', 'Asia/Taipei')
            )
            
            psychology = astrologer.analyze_chart_psychology(chart_data)
            dnd_character = dnd_generator.generate_complete_character(chart_data)
            
            # 移除不能序列化的對象
            if 'chart_object' in chart_data:
                del chart_data['chart_object']
            
            result_data = {
                'birth_chart': chart_data,
                'psychological_analysis': psychology,
                'dnd_character': dnd_character
            }
        else:
            # 使用備用計算
            result_data = backup_calculate_chart(data)
        
        print("✅ 計算完成")
        
        return jsonify({
            'success': True,
            'data': result_data,
            'engine': 'real' if USE_REAL_ASTRO else 'backup'
        })
        
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        print(f"📋 詳細錯誤: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    """測試API功能"""
    try:
        # 使用測試數據
        test_data = {
            'name': '測試冒險者',
            'year': 1985,
            'month': 10,
            'day': 6,
            'hour': 19,
            'minute': 30,
            'city': '台北',
            'longitude': 121.55,
            'latitude': 25.017,
            'timezone': 'Asia/Taipei'
        }
        
        print("🧪 開始API測試...")
        
        if USE_REAL_ASTRO:
            chart_data = astrologer.calculate_natal_chart(**test_data)
            dnd_character = dnd_generator.generate_complete_character(chart_data)
            
            if 'chart_object' in chart_data:
                del chart_data['chart_object']
        else:
            result = backup_calculate_chart(test_data)
            dnd_character = result['dnd_character']
        
        print("✅ 測試完成")
        
        return jsonify({
            'success': True,
            'message': 'API測試成功',
            'engine': 'real' if USE_REAL_ASTRO else 'backup',
            'test_result': {
                'character_name': dnd_character['name'],
                'dnd_class': dnd_character['class']['name'],
                'rating': dnd_character['rating'],
                'total_stats': dnd_character.get('total_stats', 'N/A')
            }
        })
        
    except Exception as e:
        print(f"❌ 測試失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    print("🌟 啟動虹靈御所占星系統 API (Railway版)...")
    print(f"📍 端口: {port}")
    print(f"🔧 計算引擎: {'真實Kerykeion' if USE_REAL_ASTRO else '備用方案'}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

