#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虹靈御所占星API - 集成測試腳本
演示如何從外部程序調用API
"""

import requests
import json
import sys
import os

# API基礎URL（可通過環境變量配置）
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000")

def test_health_check():
    """測試健康檢查端點"""
    print("=" * 60)
    print("測試1: 健康檢查")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ API狀態: {data['status']}")
        print(f"✅ 版本: {data['version']}")
        print(f"✅ 計算引擎: {data['engine']}")
        print(f"✅ 成功率: {data['success_rate']}%")
        print(f"✅ 請求總數: {data['request_count']}")
        
        return True
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return False

def test_system_test():
    """測試系統測試端點"""
    print("\n" + "=" * 60)
    print("測試2: 系統測試")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/test", timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('success'):
            print(f"✅ 系統測試通過")
            print(f"✅ 測試時間: {data['test_info']['test_time']}秒")
            print(f"✅ 使用引擎: {data['test_info']['engine_used']}")
            
            character = data.get('character', {})
            print(f"\n角色信息:")
            print(f"  - 名稱: {character.get('name')}")
            print(f"  - 職業: {character['class']['name']}")
            print(f"  - 評級: {character.get('rating')}")
            print(f"  - 總屬性: {character.get('total_stats')}")
            
            return True
        else:
            print(f"❌ 系統測試失敗: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 系統測試失敗: {e}")
        return False

def test_calculate_chart():
    """測試星盤計算端點"""
    print("\n" + "=" * 60)
    print("測試3: 星盤計算與角色生成")
    print("=" * 60)
    
    # 測試數據
    birth_data = {
        "name": "集成測試用戶",
        "year": 1995,
        "month": 8,
        "day": 20,
        "hour": 10,
        "minute": 30,
        "city": "台北",
        "longitude": 121.55,
        "latitude": 25.017,
        "timezone": "Asia/Taipei"
    }
    
    print(f"出生信息: {birth_data['year']}/{birth_data['month']}/{birth_data['day']} "
          f"{birth_data['hour']}:{birth_data['minute']} {birth_data['city']}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/calculate_chart",
            headers={"Content-Type": "application/json"},
            json=birth_data,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('success'):
            character = data['character']
            astro_data = data['astro_data']
            metadata = data['metadata']
            
            print(f"\n✅ 計算成功！")
            print(f"\n【角色信息】")
            print(f"  名稱: {character['name']}")
            print(f"  職業: {character['class']['name']}")
            print(f"  描述: {character['class']['description']}")
            print(f"  評級: {character['rating']}")
            print(f"  總屬性: {character['total_stats']}")
            
            print(f"\n【六大屬性】")
            stats_zh = {
                'strength': '力量',
                'dexterity': '敏捷',
                'constitution': '體質',
                'intelligence': '智力',
                'wisdom': '智慧',
                'charisma': '魅力'
            }
            for stat, value in character['stats'].items():
                print(f"  {stats_zh.get(stat, stat)}: {value}")
            
            print(f"\n【星盤信息】")
            birth_chart = character['birth_chart']
            print(f"  太陽: {birth_chart['sun']}")
            print(f"  月亮: {birth_chart['moon']}")
            print(f"  上升: {birth_chart['ascendant']}")
            
            print(f"\n【計算信息】")
            print(f"  計算時間: {metadata['calculation_time']}秒")
            print(f"  計算引擎: {metadata['engine']}")
            print(f"  請求ID: {metadata['request_id']}")
            
            print(f"\n【角色背景】")
            print(f"  {character['background']}")
            
            return True
        else:
            print(f"❌ 計算失敗: {data.get('error')}")
            if 'validation_errors' in data:
                print(f"驗證錯誤: {data['validation_errors']}")
            return False
            
    except Exception as e:
        print(f"❌ 計算失敗: {e}")
        return False

def test_error_handling():
    """測試錯誤處理"""
    print("\n" + "=" * 60)
    print("測試4: 錯誤處理")
    print("=" * 60)
    
    # 測試無效數據
    invalid_data = {
        "name": "錯誤測試",
        "year": 2100,  # 超出範圍
        "month": 13,   # 無效月份
        "day": 15,
        "hour": 14,
        "minute": 30,
        "city": "台北",
        "longitude": 121.55,
        "latitude": 25.017
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/calculate_chart",
            headers={"Content-Type": "application/json"},
            json=invalid_data,
            timeout=30
        )
        
        data = response.json()
        
        if response.status_code == 400:
            print(f"✅ 正確返回錯誤狀態碼: {response.status_code}")
            print(f"✅ 錯誤信息: {data.get('error')}")
            print(f"✅ 錯誤碼: {data.get('error_code')}")
            
            if 'validation_errors' in data:
                print(f"✅ 驗證錯誤:")
                for error in data['validation_errors']:
                    print(f"   - {error}")
            
            return True
        else:
            print(f"❌ 未返回預期的錯誤狀態碼")
            return False
            
    except Exception as e:
        print(f"❌ 錯誤處理測試失敗: {e}")
        return False

def test_cors():
    """測試CORS設置"""
    print("\n" + "=" * 60)
    print("測試5: CORS跨域支持")
    print("=" * 60)
    
    try:
        # 發送帶Origin頭的請求
        headers = {
            "Origin": "http://example.com",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/calculate_chart",
            headers=headers,
            json={
                "name": "CORS測試",
                "year": 1990,
                "month": 6,
                "day": 15,
                "hour": 14,
                "minute": 30,
                "city": "台北",
                "longitude": 121.55,
                "latitude": 25.017
            },
            timeout=30
        )
        
        # 檢查CORS頭
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        
        if cors_header:
            print(f"✅ CORS已啟用")
            print(f"✅ Access-Control-Allow-Origin: {cors_header}")
            return True
        else:
            print(f"❌ CORS頭未找到")
            return False
            
    except Exception as e:
        print(f"❌ CORS測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("\n" + "=" * 60)
    print("🌟 虹靈御所占星API - 集成測試")
    print("=" * 60)
    print(f"API地址: {API_BASE_URL}")
    print()
    
    results = []
    
    # 執行所有測試
    results.append(("健康檢查", test_health_check()))
    results.append(("系統測試", test_system_test()))
    results.append(("星盤計算", test_calculate_chart()))
    results.append(("錯誤處理", test_error_handling()))
    results.append(("CORS支持", test_cors()))
    
    # 總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"總計: {len(results)} 個測試")
    print(f"通過: {passed} 個")
    print(f"失敗: {failed} 個")
    print(f"成功率: {(passed/len(results)*100):.1f}%")
    print("=" * 60)
    
    # 返回退出碼
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
