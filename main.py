#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虹靈御所占星系統 - Railway部署版本
適配Railway環境的Flask應用
"""

import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import traceback

app = Flask(__name__)
CORS(app)

# Railway端口配置
port = int(os.environ.get("PORT", 5000))

# 嘗試導入真實的占星計算，如果失敗則使用備用方案
try:
    from astro_consultant import ProfessionalAstrologer
    from dnd_character_generator import DnDCharacterGenerator
    
    # 初始化占星師和角色生成器
    astrologer = ProfessionalAstrologer()
    dnd_generator = DnDCharacterGenerator()
    USE_REAL_ASTRO = True
    print("✅ 使用真實占星計算引擎")
    
except ImportError as e:
    print(f"⚠️ 無法載入真實占星引擎: {e}")
    print("🔄 使用備用計算方案")
    USE_REAL_ASTRO = False
    
    # 備用的占星計算
    import random
    from datetime import datetime
    
    # 星座列表
    ZODIAC_SIGNS = [
        "牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座",
        "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座"
    ]
    
    # 行星列表
    PLANETS = {
        "sun": "太陽",
        "moon": "月亮", 
        "mercury": "水星",
        "venus": "金星",
        "mars": "火星",
        "jupiter": "木星",
        "saturn": "土星",
        "uranus": "天王星",
        "neptune": "海王星",
        "pluto": "冥王星"
    }
    
    # D&D職業列表
    DND_CLASSES = [
        {"name": "聖騎士", "description": "正義的戰士，以神聖力量守護弱者"},
        {"name": "法師", "description": "掌握奧術魔法的智者"},
        {"name": "盜賊", "description": "靈活敏捷的暗影行者"},
        {"name": "戰士", "description": "勇敢的近戰專家"},
        {"name": "牧師", "description": "神聖的治療者和引導者"},
        {"name": "遊俠", "description": "自然的守護者和追蹤專家"},
        {"name": "野蠻人", "description": "原始力量的化身"},
        {"name": "吟遊詩人", "description": "魅力四射的表演者和魔法使用者"},
        {"name": "術士", "description": "天生的魔法天才"},
        {"name": "邪術師", "description": "與異界存在締結契約的魔法使用者"}
    ]

def backup_calculate_chart(data):
    """備用的星盤計算方案"""
    # 基於出生月份的基礎計算
    month = data.get('month', 1)
    day = data.get('day', 1)
    
    # 計算太陽星座（簡化版）
    sun_sign_index = (month - 1) % 12
    
    planets = {}
    for planet_key, planet_name in PLANETS.items():
        if planet_key == 'sun':
            # 太陽星座基於出生月份
            sign = ZODIAC_SIGNS[sun_sign_index]
            position = (day - 1) * 30 / 31  # 簡化的度數計算
        else:
            # 其他行星隨機但有一定邏輯
            sign_offset = hash(f"{planet_key}{data.get('year', 1990)}{month}") % 12
            sign = ZODIAC_SIGNS[sign_offset]
            position = (hash(f"{planet_key}{day}") % 3000) / 100
        
        planets[planet_key] = {
            "name": planet_name,
            "sign": sign,
            "position": round(position, 2),
            "house": ((hash(f"{planet_key}{data.get('hour', 12)}") % 12) + 1),
            "retrograde": (hash(f"{planet_key}retro{data.get('minute', 0)}") % 4) == 0
        }
    
    # 生成D&D角色
    class_choice = random.choice(DND_CLASSES)
    
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

