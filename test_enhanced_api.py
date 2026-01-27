#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試增強後的占星API
"""

from astro_consultant import ProfessionalAstrologer
import json

def test_enhanced_calculations():
    """測試增強後的計算功能"""
    
    astrologer = ProfessionalAstrologer()
    
    # 使用問題陳述中的出生數據
    chart_data = astrologer.calculate_natal_chart(
        name="測試用戶",
        year=1985,
        month=10,
        day=6,
        hour=19,
        minute=30,
        city="台北",
        longitude=121.55,
        latitude=25.017,
        timezone="Asia/Taipei"
    )
    
    print("=" * 80)
    print("增強型占星計算測試結果")
    print("=" * 80)
    
    # 測試行星數據
    print("\n【行星位置】（帶度分秒格式）")
    print("-" * 80)
    for key in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
        if key in chart_data['planets']:
            planet = chart_data['planets'][key]
            retro_symbol = "℞" if planet['retrograde'] else ""
            print(f"{planet['name']:<6} {planet['sign']:<8} {planet['position_dms']:<15} {planet['house']:>2}宮 {retro_symbol}")
    
    # 測試額外點位
    print("\n【額外點位】")
    print("-" * 80)
    if 'additional_points' in chart_data:
        for key, point in chart_data['additional_points'].items():
            retro_symbol = "℞" if point.get('retrograde', False) else ""
            print(f"{point['name']:<6} {point['sign']:<8} {point['position_dms']:<15} {point['house']:>2}宮 {retro_symbol}")
    
    # 測試四軸點位
    print("\n【四軸點位】")
    print("-" * 80)
    for key in ['ascendant', 'midheaven', 'descendant', 'imum_coeli']:
        if key in chart_data['angles']:
            angle = chart_data['angles'][key]
            print(f"{angle['name']:<6} {angle['sign']:<8} {angle['position_dms']:<15} {angle['house']:>2}宮")
    
    # 測試相位
    aspects = chart_data.get('aspects', [])
    print(f"\n【相位】（共{len(aspects)}個，顯示前15個）")
    print("-" * 80)
    for i, aspect in enumerate(aspects[:15]):
        applying = "入相" if aspect.get('applying', False) else "出相"
        print(f"{i+1:2}. {aspect['planet1']:<8} {aspect['aspect']:<10} {aspect['planet2']:<8} "
              f"(容許度: {aspect['orb']:>5.2f}° - {applying})")
    
    # 統計信息
    print("\n【統計信息】")
    print("-" * 80)
    print(f"行星數量: {len(chart_data['planets'])}")
    print(f"額外點位: {len(chart_data.get('additional_points', {}))}")
    print(f"四軸點位: {len(chart_data['angles'])}")
    print(f"相位數量: {len(aspects)}")
    
    # 驗證數據完整性
    print("\n【數據驗證】")
    print("-" * 80)
    
    checks = [
        ("行星包含度分秒格式", all('position_dms' in p for p in chart_data['planets'].values())),
        ("額外點位存在", 'additional_points' in chart_data and len(chart_data['additional_points']) > 0),
        ("凱龍點位存在", 'chiron' in chart_data.get('additional_points', {})),
        ("北交點位存在", 'north_node' in chart_data.get('additional_points', {})),
        ("南交點位存在", 'south_node' in chart_data.get('additional_points', {})),
        ("四軸完整", len(chart_data['angles']) >= 4),
        ("相位計算成功", len(aspects) > 0),
        ("上升點存在", 'ascendant' in chart_data['angles']),
        ("天頂點存在", 'midheaven' in chart_data['angles']),
        ("下降點存在", 'descendant' in chart_data['angles']),
        ("天底點存在", 'imum_coeli' in chart_data['angles']),
    ]
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{check_name:<30} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ 所有測試通過！增強功能正常運作。")
    else:
        print("❌ 部分測試失敗，請檢查實現。")
    print("=" * 80)
    
    return all_passed

if __name__ == "__main__":
    success = test_enhanced_calculations()
    exit(0 if success else 1)
