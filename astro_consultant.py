#!/usr/bin/env python3
"""
專業占星諮詢師系統
基於榮格心理學的賦能型占星解讀
"""

import kerykeion as kr
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class ProfessionalAstrologer:
    """
    賦能型占星諮詢師
    基於榮格心理學洞察與敘事治療技巧的現代占星諮詢師
    """
    
    def __init__(self):
        """初始化占星諮詢師"""
        self.sign_names = {
            'Ari': '牡羊座', 'Tau': '金牛座', 'Gem': '雙子座', 'Can': '巨蟹座',
            'Leo': '獅子座', 'Vir': '處女座', 'Lib': '天秤座', 'Sco': '天蠍座',
            'Sag': '射手座', 'Cap': '摩羯座', 'Aqu': '水瓶座', 'Pis': '雙魚座'
        }
        
        self.planet_names = {
            'Sun': '太陽', 'Moon': '月亮', 'Mercury': '水星', 'Venus': '金星',
            'Mars': '火星', 'Jupiter': '木星', 'Saturn': '土星',
            'Uranus': '天王星', 'Neptune': '海王星', 'Pluto': '冥王星'
        }
        
        # 星座元素和性質
        self.elements = {
            'Ari': '火', 'Leo': '火', 'Sag': '火',
            'Tau': '土', 'Vir': '土', 'Cap': '土',
            'Gem': '風', 'Lib': '風', 'Aqu': '風',
            'Can': '水', 'Sco': '水', 'Pis': '水'
        }
        
        self.qualities = {
            'Ari': '開創', 'Can': '開創', 'Lib': '開創', 'Cap': '開創',
            'Tau': '固定', 'Leo': '固定', 'Sco': '固定', 'Aqu': '固定',
            'Gem': '變動', 'Vir': '變動', 'Sag': '變動', 'Pis': '變動'
        }
    
    def calculate_natal_chart(self, name: str, year: int, month: int, day: int, 
                            hour: int, minute: int, city: str, 
                            longitude: float, latitude: float, timezone: str) -> Dict:
        """
        計算本命星盤
        
        Args:
            name: 姓名
            year, month, day: 出生年月日
            hour, minute: 出生時分
            city: 出生城市
            longitude: 經度
            latitude: 緯度
            timezone: 時區
            
        Returns:
            完整的星盤數據字典
        """
        try:
            # 使用AstrologicalSubject API創建占星主體
            # 直接使用經緯度和時區，避免網路查詢
            chart = kr.AstrologicalSubject(
                name=name, 
                year=year, 
                month=month, 
                day=day, 
                hour=hour, 
                minute=minute,
                lng=longitude,
                lat=latitude,
                tz_str=timezone,
                city=city
            )
            
            # 提取行星數據
            planets_data = {}
            planets = [
                ('sun', chart.sun), ('moon', chart.moon), ('mercury', chart.mercury),
                ('venus', chart.venus), ('mars', chart.mars), ('jupiter', chart.jupiter),
                ('saturn', chart.saturn), ('uranus', chart.uranus), 
                ('neptune', chart.neptune), ('pluto', chart.pluto)
            ]
            
            for planet_key, planet_data in planets:
                planets_data[planet_key] = {
                    'name': self.planet_names.get(planet_data.name, planet_data.name),
                    'sign': self.sign_names.get(planet_data.sign, planet_data.sign),
                    'sign_code': planet_data.sign,
                    'house': self._get_house_number(planet_data.house),
                    'position': round(planet_data.position, 2),
                    'retrograde': planet_data.retrograde,
                    'element': self.elements.get(planet_data.sign, '未知'),
                    'quality': self.qualities.get(planet_data.sign, '未知')
                }
            
            # 提取宮位數據
            houses_data = {}
            houses = [
                ('1st', chart.first_house), ('2nd', chart.second_house),
                ('3rd', chart.third_house), ('4th', chart.fourth_house),
                ('5th', chart.fifth_house), ('6th', chart.sixth_house),
                ('7th', chart.seventh_house), ('8th', chart.eighth_house),
                ('9th', chart.ninth_house), ('10th', chart.tenth_house),
                ('11th', chart.eleventh_house), ('12th', chart.twelfth_house)
            ]
            
            for house_key, house_data in houses:
                houses_data[house_key] = {
                    'sign': self.sign_names.get(house_data.sign, house_data.sign),
                    'sign_code': house_data.sign,
                    'position': round(house_data.position, 2),
                    'element': self.elements.get(house_data.sign, '未知'),
                    'quality': self.qualities.get(house_data.sign, '未知')
                }
            
            # 計算重要點位
            angles = {
                'ascendant': {
                    'sign': self.sign_names.get(chart.ascendant.sign, chart.ascendant.sign),
                    'position': round(chart.ascendant.position, 2)
                },
                'midheaven': {
                    'sign': self.sign_names.get(chart.medium_coeli.sign, chart.medium_coeli.sign),
                    'position': round(chart.medium_coeli.position, 2)
                }
            }
            
            return {
                'birth_info': {
                    'name': name,
                    'datetime': f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
                    'location': city,
                    'coordinates': f"{latitude:.3f}°N, {longitude:.3f}°E",
                    'timezone': timezone
                },
                'planets': planets_data,
                'houses': houses_data,
                'angles': angles,
                'chart_object': chart
            }
            
        except Exception as e:
            raise Exception(f"星盤計算失敗: {str(e)}")
    
    def _get_house_number(self, house_enum) -> int:
        """將宮位枚舉轉換為數字"""
        house_mapping = {
            'First_House': 1, 'Second_House': 2, 'Third_House': 3, 'Fourth_House': 4,
            'Fifth_House': 5, 'Sixth_House': 6, 'Seventh_House': 7, 'Eighth_House': 8,
            'Ninth_House': 9, 'Tenth_House': 10, 'Eleventh_House': 11, 'Twelfth_House': 12
        }
        return house_mapping.get(str(house_enum), 0)
    
    def analyze_chart_psychology(self, chart_data: Dict) -> Dict:
        """
        心理學導向的星盤分析
        基於榮格原型理論和現代心理占星學
        """
        planets = chart_data['planets']
        houses = chart_data['houses']
        
        # 核心人格分析（太陽、月亮、上升）
        sun_analysis = self._analyze_sun_psychology(planets['sun'])
        moon_analysis = self._analyze_moon_psychology(planets['moon'])
        ascendant_analysis = self._analyze_ascendant_psychology(chart_data['angles']['ascendant'])
        
        # 溝通與思維模式（水星）
        mercury_analysis = self._analyze_mercury_psychology(planets['mercury'])
        
        # 價值觀與關係模式（金星）
        venus_analysis = self._analyze_venus_psychology(planets['venus'])
        
        # 行動力與動機（火星）
        mars_analysis = self._analyze_mars_psychology(planets['mars'])
        
        # 成長與擴展（木星）
        jupiter_analysis = self._analyze_jupiter_psychology(planets['jupiter'])
        
        # 責任與限制（土星）
        saturn_analysis = self._analyze_saturn_psychology(planets['saturn'])
        
        # 創新與變革（天王星）
        uranus_analysis = self._analyze_uranus_psychology(planets['uranus'])
        
        # 靈性與直覺（海王星）
        neptune_analysis = self._analyze_neptune_psychology(planets['neptune'])
        
        # 轉化與重生（冥王星）
        pluto_analysis = self._analyze_pluto_psychology(planets['pluto'])
        
        return {
            'core_personality': {
                'sun': sun_analysis,
                'moon': moon_analysis,
                'ascendant': ascendant_analysis
            },
            'mental_functions': {
                'mercury': mercury_analysis,
                'venus': venus_analysis,
                'mars': mars_analysis
            },
            'growth_patterns': {
                'jupiter': jupiter_analysis,
                'saturn': saturn_analysis
            },
            'transformation_potential': {
                'uranus': uranus_analysis,
                'neptune': neptune_analysis,
                'pluto': pluto_analysis
            }
        }
    
    def _analyze_sun_psychology(self, sun_data: Dict) -> Dict:
        """太陽心理分析 - 核心自我與生命目的"""
        sign = sun_data['sign_code']
        house = sun_data['house']
        
        # 基於星座的核心特質
        sign_traits = {
            'Ari': {'drive': '開拓精神', 'challenge': '學習耐心與合作'},
            'Tau': {'drive': '穩定建構', 'challenge': '擁抱變化與彈性'},
            'Gem': {'drive': '知識探索', 'challenge': '深化專注與承諾'},
            'Can': {'drive': '情感滋養', 'challenge': '建立健康界限'},
            'Leo': {'drive': '創意表達', 'challenge': '平衡自我與他人'},
            'Vir': {'drive': '完善服務', 'challenge': '接受不完美'},
            'Lib': {'drive': '和諧平衡', 'challenge': '堅持個人立場'},
            'Sco': {'drive': '深度轉化', 'challenge': '學習信任與開放'},
            'Sag': {'drive': '智慧追尋', 'challenge': '腳踏實地執行'},
            'Cap': {'drive': '成就建立', 'challenge': '平衡工作與生活'},
            'Aqu': {'drive': '創新改革', 'challenge': '重視個人情感'},
            'Pis': {'drive': '靈性連結', 'challenge': '建立現實界限'}
        }
        
        traits = sign_traits.get(sign, {'drive': '自我實現', 'challenge': '平衡發展'})
        
        return {
            'core_drive': traits['drive'],
            'life_challenge': traits['challenge'],
            'expression_area': f"第{house}宮生活領域",
            'empowerment_message': f"你的{sun_data['name']}在{sun_data['sign']}，賦予你{traits['drive']}的天賦。透過在{traits['challenge']}方面的成長，你能更充分地發揮這份潛能。"
        }
    
    def _analyze_moon_psychology(self, moon_data: Dict) -> Dict:
        """月亮心理分析 - 情感需求與內在安全感"""
        sign = moon_data['sign_code']
        house = moon_data['house']
        
        emotional_needs = {
            'Ari': '獨立自主與即時回應',
            'Tau': '穩定安全與感官滿足',
            'Gem': '智性刺激與多樣變化',
            'Can': '情感連結與歸屬感',
            'Leo': '認可讚賞與創意表達',
            'Vir': '秩序條理與實用價值',
            'Lib': '和諧美感與公平正義',
            'Sco': '深度連結與情感真實',
            'Sag': '自由探索與意義追尋',
            'Cap': '成就認同與結構安全',
            'Aqu': '獨特性與群體歸屬',
            'Pis': '靈性連結與無條件愛'
        }
        
        need = emotional_needs.get(sign, '情感平衡與內在和諧')
        
        return {
            'emotional_need': need,
            'nurturing_style': f"{moon_data['sign']}式的關懷方式",
            'comfort_zone': f"第{house}宮相關的生活領域",
            'empowerment_message': f"你的情感本質需要{need}。理解並滿足這些需求，能幫助你建立更穩固的內在安全感。"
        }
    
    def _analyze_ascendant_psychology(self, asc_data: Dict) -> Dict:
        """上升星座心理分析 - 外在表現與人生面具"""
        sign = asc_data['sign']
        
        return {
            'outer_expression': f"{sign}式的外在表現",
            'life_approach': f"以{sign}的方式面對世界",
            'empowerment_message': f"你的上升{sign}是你與世界互動的天然方式。擁抱這個面向，同時記住它只是你完整自我的一部分。"
        }
    
    def _analyze_mercury_psychology(self, mercury_data: Dict) -> Dict:
        """水星心理分析 - 思維模式與溝通風格"""
        sign = mercury_data['sign_code']
        retrograde = mercury_data['retrograde']
        
        thinking_styles = {
            'Ari': '直覺快速的思維',
            'Tau': '實用穩健的思考',
            'Gem': '靈活多元的思維',
            'Can': '情感導向的思考',
            'Leo': '創意戲劇的表達',
            'Vir': '分析細緻的思維',
            'Lib': '平衡協調的思考',
            'Sco': '深度洞察的思維',
            'Sag': '哲學宏觀的思考',
            'Cap': '結構實務的思維',
            'Aqu': '創新獨特的思考',
            'Pis': '直覺詩意的思維'
        }
        
        style = thinking_styles.get(sign, '獨特的思維方式')
        retrograde_note = "你的內在思考過程可能比外在表達更豐富" if retrograde else ""
        
        return {
            'thinking_style': style,
            'communication_gift': f"{mercury_data['sign']}式的溝通天賦",
            'retrograde_insight': retrograde_note,
            'empowerment_message': f"你擁有{style}的天賦。{retrograde_note}信任你的思維過程，它是你獨特的智慧表達。"
        }
    
    def _analyze_venus_psychology(self, venus_data: Dict) -> Dict:
        """金星心理分析 - 價值觀與關係模式"""
        sign = venus_data['sign_code']
        
        love_styles = {
            'Ari': '熱情直接的愛',
            'Tau': '穩定感官的愛',
            'Gem': '智性交流的愛',
            'Can': '滋養保護的愛',
            'Leo': '浪漫慷慨的愛',
            'Vir': '實用服務的愛',
            'Lib': '和諧平等的愛',
            'Sco': '深度轉化的愛',
            'Sag': '自由探索的愛',
            'Cap': '承諾負責的愛',
            'Aqu': '友誼獨立的愛',
            'Pis': '無條件犧牲的愛'
        }
        
        style = love_styles.get(sign, '獨特的愛的表達')
        
        return {
            'love_style': style,
            'value_system': f"{venus_data['sign']}式的價值觀",
            'empowerment_message': f"你以{style}的方式給予和接受愛。尊重你的愛的語言，同時保持開放學習其他表達方式。"
        }
    
    def _analyze_mars_psychology(self, mars_data: Dict) -> Dict:
        """火星心理分析 - 行動力與動機驅動"""
        sign = mars_data['sign_code']
        
        action_styles = {
            'Ari': '直接果斷的行動',
            'Tau': '穩步持續的行動',
            'Gem': '靈活多變的行動',
            'Can': '保護性的行動',
            'Leo': '創意領導的行動',
            'Vir': '精確有效的行動',
            'Lib': '合作平衡的行動',
            'Sco': '策略深度的行動',
            'Sag': '冒險探索的行動',
            'Cap': '有組織的行動',
            'Aqu': '創新改革的行動',
            'Pis': '直覺流動的行動'
        }
        
        style = action_styles.get(sign, '獨特的行動方式')
        
        return {
            'action_style': style,
            'motivation_source': f"{mars_data['sign']}式的動機驅動",
            'empowerment_message': f"你的行動力表現為{style}。信任你的天然動機模式，它是你實現目標的最佳方式。"
        }
    
    def _analyze_jupiter_psychology(self, jupiter_data: Dict) -> Dict:
        """木星心理分析 - 成長機會與智慧發展"""
        sign = jupiter_data['sign_code']
        
        growth_areas = {
            'Ari': '領導力與開創精神',
            'Tau': '實用智慧與資源管理',
            'Gem': '知識整合與溝通技巧',
            'Can': '情感智慧與照護能力',
            'Leo': '創意表達與自信建立',
            'Vir': '服務精神與完善技能',
            'Lib': '關係智慧與美感培養',
            'Sco': '心理洞察與轉化能力',
            'Sag': '哲學思維與文化理解',
            'Cap': '組織能力與權威建立',
            'Aqu': '創新思維與社會意識',
            'Pis': '靈性發展與同理心'
        }
        
        area = growth_areas.get(sign, '個人智慧與成長')
        
        return {
            'growth_opportunity': area,
            'wisdom_path': f"透過{jupiter_data['sign']}的方式擴展視野",
            'empowerment_message': f"你的成長機會在於發展{area}。這是你天然的智慧發展方向。"
        }
    
    def _analyze_saturn_psychology(self, saturn_data: Dict) -> Dict:
        """土星心理分析 - 責任課題與成熟發展"""
        sign = saturn_data['sign_code']
        
        mastery_areas = {
            'Ari': '學習耐心與自律',
            'Tau': '建立彈性與開放',
            'Gem': '深化專注與承諾',
            'Can': '建立健康界限',
            'Leo': '平衡自我與謙遜',
            'Vir': '接受不完美與放鬆',
            'Lib': '堅持立場與決斷',
            'Sco': '學習信任與釋放',
            'Sag': '腳踏實地與實踐',
            'Cap': '平衡工作與情感',
            'Aqu': '重視傳統與個人',
            'Pis': '建立界限與結構'
        }
        
        area = mastery_areas.get(sign, '個人成熟與責任')
        
        return {
            'mastery_challenge': area,
            'maturity_path': f"透過{saturn_data['sign']}學習人生課題",
            'empowerment_message': f"你的成熟之路在於{area}。這些挑戰是你建立真正力量的機會。"
        }
    
    def _analyze_uranus_psychology(self, uranus_data: Dict) -> Dict:
        """天王星心理分析 - 創新潛能與獨特性"""
        sign = uranus_data['sign_code']
        
        return {
            'innovation_style': f"{uranus_data['sign']}式的創新方式",
            'uniqueness_expression': f"在{uranus_data['sign']}領域展現獨特性",
            'empowerment_message': f"你的天王星在{uranus_data['sign']}，賦予你獨特的創新視角。擁抱你的與眾不同。"
        }
    
    def _analyze_neptune_psychology(self, neptune_data: Dict) -> Dict:
        """海王星心理分析 - 靈性直覺與夢想"""
        sign = neptune_data['sign_code']
        
        return {
            'spiritual_path': f"{neptune_data['sign']}式的靈性發展",
            'intuitive_gift': f"在{neptune_data['sign']}領域的直覺天賦",
            'empowerment_message': f"你的海王星在{neptune_data['sign']}，連結你與更高的靈性智慧。信任你的直覺。"
        }
    
    def _analyze_pluto_psychology(self, pluto_data: Dict) -> Dict:
        """冥王星心理分析 - 轉化力量與深層潛能"""
        sign = pluto_data['sign_code']
        
        return {
            'transformation_power': f"{pluto_data['sign']}式的轉化能力",
            'deep_potential': f"在{pluto_data['sign']}領域的深層力量",
            'empowerment_message': f"你的冥王星在{pluto_data['sign']}，擁有深度轉化的力量。擁抱變化，它是你重生的機會。"
        }

# 測試函數
def test_professional_astrologer():
    """測試專業占星諮詢師"""
    astrologer = ProfessionalAstrologer()
    
    # 測試星盤計算
    chart_data = astrologer.calculate_natal_chart(
        "測試用戶", 1989, 9, 23, 12, 30, "台北",
        121.5654, 25.033, "Asia/Taipei"
    )
    
    print("🔮 專業占星諮詢師測試")
    print("=" * 50)
    print(f"姓名: {chart_data['birth_info']['name']}")
    print(f"出生: {chart_data['birth_info']['datetime']}")
    print(f"地點: {chart_data['birth_info']['location']}")
    
    # 心理分析
    psychology = astrologer.analyze_chart_psychology(chart_data)
    
    print("\n🌟 核心人格分析:")
    print(f"太陽: {psychology['core_personality']['sun']['empowerment_message']}")
    print(f"月亮: {psychology['core_personality']['moon']['empowerment_message']}")
    
    return chart_data, psychology

if __name__ == "__main__":
    test_professional_astrologer()

