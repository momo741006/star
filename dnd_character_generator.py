#!/usr/bin/env python3
"""
D&D職業角色生成系統
基於占星星盤配置生成龍與地下城角色
"""

import json
import random
from typing import Dict, List, Tuple
from astro_consultant import ProfessionalAstrologer

class DnDCharacterGenerator:
    """
    D&D角色生成器
    根據占星星盤配置判定最適合的D&D職業並生成角色
    """
    
    def __init__(self):
        """初始化D&D角色生成器"""
        
        # D&D職業定義
        self.dnd_classes = {
            'barbarian': {
                'name': '野蠻人',
                'description': '原始力量的化身，在戰鬥中狂暴無比',
                'primary_stats': ['strength', 'constitution'],
                'personality_traits': ['勇猛', '直覺', '自然親和', '情緒強烈']
            },
            'bard': {
                'name': '吟遊詩人', 
                'description': '魅力四射的表演者，以音樂和故事施展魔法',
                'primary_stats': ['charisma', 'dexterity'],
                'personality_traits': ['魅力', '創意', '社交', '多才多藝']
            },
            'cleric': {
                'name': '牧師',
                'description': '神聖力量的代言人，治療與保護的守護者',
                'primary_stats': ['wisdom', 'constitution'],
                'personality_traits': ['虔誠', '治療', '保護', '智慧']
            },
            'druid': {
                'name': '德魯伊',
                'description': '自然的守護者，能變形並操控自然力量',
                'primary_stats': ['wisdom', 'constitution'],
                'personality_traits': ['自然親和', '變化', '平衡', '直覺']
            },
            'fighter': {
                'name': '戰士',
                'description': '訓練有素的戰鬥專家，精通各種武器和戰術',
                'primary_stats': ['strength', 'constitution'],
                'personality_traits': ['勇敢', '紀律', '領導', '堅韌']
            },
            'monk': {
                'name': '武僧',
                'description': '內在力量的修行者，以氣功和武術戰鬥',
                'primary_stats': ['dexterity', 'wisdom'],
                'personality_traits': ['自律', '平衡', '內省', '和諧']
            },
            'paladin': {
                'name': '聖騎士',
                'description': '正義的戰士，以神聖誓言為力量源泉',
                'primary_stats': ['strength', 'charisma'],
                'personality_traits': ['正義', '保護', '領導', '犧牲']
            },
            'ranger': {
                'name': '遊俠',
                'description': '荒野的守護者，精通追蹤和遠程戰鬥',
                'primary_stats': ['dexterity', 'wisdom'],
                'personality_traits': ['獨立', '自然親和', '警覺', '保護']
            },
            'rogue': {
                'name': '盜賊',
                'description': '陰影中的專家，擅長潛行和精準打擊',
                'primary_stats': ['dexterity', 'intelligence'],
                'personality_traits': ['機敏', '靈活', '狡猾', '獨立']
            },
            'sorcerer': {
                'name': '術士',
                'description': '天生的魔法使用者，魔法在血脈中流淌',
                'primary_stats': ['charisma', 'constitution'],
                'personality_traits': ['直覺', '情緒化', '天賦', '不可預測']
            },
            'warlock': {
                'name': '邪術師',
                'description': '與超自然存在締結契約的魔法使用者',
                'primary_stats': ['charisma', 'constitution'],
                'personality_traits': ['野心', '神秘', '交易', '力量渴望']
            },
            'wizard': {
                'name': '法師',
                'description': '學識淵博的魔法學者，通過研究掌握魔法',
                'primary_stats': ['intelligence', 'constitution'],
                'personality_traits': ['學者', '理性', '好奇', '準備充分']
            }
        }
        
        # 星座對應的D&D屬性加成
        self.sign_stat_modifiers = {
            'Ari': {'strength': 3, 'constitution': 2, 'dexterity': 1, 'charisma': 2},  # 牡羊座
            'Tau': {'constitution': 3, 'strength': 2, 'wisdom': 1, 'charisma': 1},     # 金牛座
            'Gem': {'intelligence': 3, 'dexterity': 2, 'charisma': 2, 'wisdom': 0},   # 雙子座
            'Can': {'wisdom': 3, 'constitution': 2, 'charisma': 1, 'intelligence': 1}, # 巨蟹座
            'Leo': {'charisma': 3, 'strength': 2, 'constitution': 1, 'dexterity': 1},  # 獅子座
            'Vir': {'intelligence': 3, 'wisdom': 2, 'dexterity': 2, 'constitution': 0}, # 處女座
            'Lib': {'charisma': 3, 'dexterity': 2, 'intelligence': 1, 'wisdom': 1},   # 天秤座
            'Sco': {'wisdom': 3, 'constitution': 2, 'intelligence': 2, 'charisma': 0}, # 天蠍座
            'Sag': {'wisdom': 3, 'dexterity': 2, 'charisma': 2, 'strength': 0},       # 射手座
            'Cap': {'constitution': 3, 'strength': 2, 'wisdom': 2, 'intelligence': 0}, # 摩羯座
            'Aqu': {'intelligence': 3, 'charisma': 2, 'dexterity': 1, 'wisdom': 1},   # 水瓶座
            'Pis': {'wisdom': 3, 'charisma': 2, 'constitution': 1, 'intelligence': 1}  # 雙魚座
        }
        
        # 行星對職業的影響權重
        self.planet_class_weights = {
            'sun': {  # 核心職業傾向
                'Ari': {'barbarian': 0.3, 'fighter': 0.2, 'paladin': 0.2},
                'Tau': {'druid': 0.3, 'ranger': 0.2, 'fighter': 0.2},
                'Gem': {'bard': 0.3, 'rogue': 0.2, 'wizard': 0.2},
                'Can': {'cleric': 0.3, 'druid': 0.2, 'paladin': 0.2},
                'Leo': {'paladin': 0.3, 'bard': 0.2, 'sorcerer': 0.2},
                'Vir': {'monk': 0.3, 'cleric': 0.2, 'wizard': 0.2},
                'Lib': {'bard': 0.3, 'paladin': 0.2, 'cleric': 0.2},
                'Sco': {'warlock': 0.3, 'rogue': 0.2, 'sorcerer': 0.2},
                'Sag': {'ranger': 0.3, 'bard': 0.2, 'druid': 0.2},
                'Cap': {'fighter': 0.3, 'paladin': 0.2, 'monk': 0.2},
                'Aqu': {'wizard': 0.3, 'warlock': 0.2, 'sorcerer': 0.2},
                'Pis': {'cleric': 0.3, 'druid': 0.2, 'sorcerer': 0.2}
            },
            'mars': {  # 戰鬥風格
                'Ari': {'barbarian': 0.2, 'fighter': 0.15},
                'Tau': {'fighter': 0.2, 'paladin': 0.15},
                'Gem': {'rogue': 0.2, 'ranger': 0.15},
                'Can': {'paladin': 0.2, 'cleric': 0.15},
                'Leo': {'paladin': 0.2, 'fighter': 0.15},
                'Vir': {'monk': 0.2, 'ranger': 0.15},
                'Lib': {'paladin': 0.2, 'bard': 0.15},
                'Sco': {'rogue': 0.2, 'warlock': 0.15},
                'Sag': {'ranger': 0.2, 'fighter': 0.15},
                'Cap': {'fighter': 0.2, 'monk': 0.15},
                'Aqu': {'fighter': 0.2, 'wizard': 0.15},
                'Pis': {'cleric': 0.2, 'druid': 0.15}
            },
            'mercury': {  # 技能和知識
                'Gem': {'wizard': 0.15, 'bard': 0.1, 'rogue': 0.1},
                'Vir': {'wizard': 0.15, 'monk': 0.1, 'cleric': 0.1},
                'Aqu': {'wizard': 0.15, 'warlock': 0.1}
            },
            'venus': {  # 社交和魅力
                'Tau': {'bard': 0.1, 'druid': 0.1},
                'Lib': {'bard': 0.15, 'paladin': 0.1},
                'Pis': {'bard': 0.1, 'cleric': 0.1}
            },
            'jupiter': {  # 智慧和成長
                'Sag': {'ranger': 0.1, 'druid': 0.1, 'cleric': 0.1},
                'Pis': {'cleric': 0.15, 'druid': 0.1}
            }
        }
        
        # 宮位對職業的影響
        self.house_class_modifiers = {
            1: {'fighter': 0.1, 'barbarian': 0.1, 'paladin': 0.1},  # 自我表現
            2: {'fighter': 0.05, 'ranger': 0.05},                   # 資源和價值
            3: {'bard': 0.1, 'rogue': 0.05},                        # 溝通和學習
            4: {'cleric': 0.1, 'druid': 0.1},                       # 家庭和根基
            5: {'bard': 0.1, 'sorcerer': 0.1, 'paladin': 0.05},    # 創意和表現
            6: {'monk': 0.1, 'cleric': 0.05, 'ranger': 0.05},      # 服務和健康
            7: {'bard': 0.05, 'paladin': 0.05},                     # 關係和合作
            8: {'warlock': 0.15, 'rogue': 0.1, 'sorcerer': 0.05},  # 轉化和神秘
            9: {'cleric': 0.1, 'wizard': 0.1, 'ranger': 0.05},     # 哲學和探索
            10: {'paladin': 0.1, 'fighter': 0.05},                  # 事業和聲望
            11: {'wizard': 0.05, 'bard': 0.05},                     # 友誼和理想
            12: {'monk': 0.1, 'cleric': 0.1, 'druid': 0.05}        # 靈性和潛意識
        }
    
    def calculate_character_stats(self, chart_data: Dict) -> Dict:
        """
        根據星盤計算D&D角色屬性
        
        Args:
            chart_data: 星盤數據
            
        Returns:
            包含六大屬性的字典
        """
        planets = chart_data['planets']
        
        # 基礎屬性值 (8-15的範圍)
        base_stats = {
            'strength': 10,
            'dexterity': 10, 
            'constitution': 10,
            'intelligence': 10,
            'wisdom': 10,
            'charisma': 10
        }
        
        # 根據主要行星的星座加成
        important_planets = ['sun', 'moon', 'mars', 'mercury', 'venus']
        
        for planet_key in important_planets:
            if planet_key in planets:
                planet = planets[planet_key]
                sign = planet['sign_code']
                
                if sign in self.sign_stat_modifiers:
                    modifiers = self.sign_stat_modifiers[sign]
                    weight = 1.0 if planet_key == 'sun' else 0.7 if planet_key == 'moon' else 0.5
                    
                    for stat, modifier in modifiers.items():
                        base_stats[stat] += int(modifier * weight)
        
        # 添加隨機變化 (-2 到 +2)
        for stat in base_stats:
            base_stats[stat] += random.randint(-2, 2)
            # 確保屬性在合理範圍內 (8-18)
            base_stats[stat] = max(8, min(18, base_stats[stat]))
        
        return base_stats
    
    def determine_dnd_class(self, chart_data: Dict) -> Tuple[str, float]:
        """
        根據星盤確定最適合的D&D職業
        
        Args:
            chart_data: 星盤數據
            
        Returns:
            (職業key, 匹配度分數)
        """
        planets = chart_data['planets']
        houses = chart_data['houses']
        
        # 初始化職業分數
        class_scores = {class_key: 0.0 for class_key in self.dnd_classes.keys()}
        
        # 根據行星星座計算分數
        for planet_key, planet_data in planets.items():
            if planet_key in self.planet_class_weights:
                sign = planet_data['sign_code']
                planet_weights = self.planet_class_weights[planet_key]
                
                if sign in planet_weights:
                    for class_key, weight in planet_weights[sign].items():
                        class_scores[class_key] += weight
        
        # 根據行星宮位計算分數
        for planet_key, planet_data in planets.items():
            house_num = planet_data['house']
            if house_num in self.house_class_modifiers:
                house_modifiers = self.house_class_modifiers[house_num]
                
                # 太陽和火星的宮位影響更重要
                weight = 1.0 if planet_key in ['sun', 'mars'] else 0.5
                
                for class_key, modifier in house_modifiers.items():
                    class_scores[class_key] += modifier * weight
        
        # 找出得分最高的職業
        best_class = max(class_scores.items(), key=lambda x: x[1])
        
        return best_class[0], best_class[1]
    
    def generate_character_background(self, chart_data: Dict, dnd_class: str, stats: Dict) -> str:
        """
        生成150字的角色背景故事
        
        Args:
            chart_data: 星盤數據
            dnd_class: D&D職業
            stats: 角色屬性
            
        Returns:
            150字的角色背景故事
        """
        planets = chart_data['planets']
        name = chart_data['birth_info']['name']
        class_info = self.dnd_classes[dnd_class]
        
        # 提取關鍵星座信息
        sun_sign = planets['sun']['sign']
        moon_sign = planets['moon']['sign'] 
        mars_sign = planets['mars']['sign']
        
        # 根據星座組合生成背景元素
        background_elements = self._generate_background_elements(
            sun_sign, moon_sign, mars_sign, class_info
        )
        
        # 構建背景故事（簡化版150字）
        background = f"""
{name}是一位{class_info['name']}，{class_info['description']}。

{background_elements['origin']}在{background_elements['environment']}中成長，從小展現{sun_sign}的{background_elements['sun_trait']}特質。{background_elements['calling']}這份{moon_sign}式的{background_elements['moon_trait']}，讓{name}走上{class_info['name']}之路。

在戰鬥中展現{mars_sign}的{background_elements['mars_trait']}風格。憑藉{stats['strength']}點力量、{stats['dexterity']}點敏捷和{stats['wisdom']}點智慧，{name}已成為{background_elements['reputation']}的冒險者，準備書寫屬於自己的傳奇。
        """.strip()
        
        # 確保字數控制在150字左右
        if len(background) > 180:
            background = background[:177] + "..."
        
        return background
    
    def _generate_background_elements(self, sun_sign: str, moon_sign: str, 
                                    mars_sign: str, class_info: Dict) -> Dict:
        """生成背景故事元素"""
        
        # 太陽星座對應的核心特質
        sun_traits = {
            '牡羊座': {'trait': '勇敢無畏', 'origin': '出生在戰士家族', 'environment': '邊境要塞'},
            '金牛座': {'trait': '堅韌不拔', 'origin': '來自農牧世家', 'environment': '肥沃平原'},
            '雙子座': {'trait': '機智靈活', 'origin': '生於商人家庭', 'environment': '繁華商港'},
            '巨蟹座': {'trait': '保護本能', 'origin': '出身守護者血脈', 'environment': '古老聖地'},
            '獅子座': {'trait': '天生領袖', 'origin': '貴族世家後裔', 'environment': '輝煌王都'},
            '處女座': {'trait': '完美主義', 'origin': '學者世家傳人', 'environment': '知識聖殿'},
            '天秤座': {'trait': '追求平衡', 'origin': '外交官家族', 'environment': '和平城邦'},
            '天蠍座': {'trait': '洞察深邃', 'origin': '神秘組織成員', 'environment': '隱秘山谷'},
            '射手座': {'trait': '自由探索', 'origin': '遊牧民族後代', 'environment': '廣闊草原'},
            '摩羯座': {'trait': '堅定意志', 'origin': '工匠世家子弟', 'environment': '山地要塞'},
            '水瓶座': {'trait': '創新思維', 'origin': '發明家後裔', 'environment': '魔法學院'},
            '雙魚座': {'trait': '直覺敏銳', 'origin': '預言者血脈', 'environment': '神聖湖泊'}
        }
        
        # 月亮星座對應的內在動機
        moon_motivations = {
            '牡羊座': {'trait': '內在火焰', 'calling': '內心燃燒的正義之火'},
            '金牛座': {'trait': '穩定渴望', 'calling': '對安全與穩定的深層需求'},
            '雙子座': {'trait': '知識渴求', 'calling': '對知識與真理的無盡追求'},
            '巨蟹座': {'trait': '保護慾望', 'calling': '保護弱者的強烈使命感'},
            '獅子座': {'trait': '榮耀追求', 'calling': '對榮耀與認可的渴望'},
            '處女座': {'trait': '服務精神', 'calling': '為他人服務的純真願望'},
            '天秤座': {'trait': '和諧需求', 'calling': '對公正與和諧的執著'},
            '天蠍座': {'trait': '轉化力量', 'calling': '內在的轉化與重生力量'},
            '射手座': {'trait': '智慧追尋', 'calling': '對智慧與真理的探索'},
            '摩羯座': {'trait': '成就動機', 'calling': '建立持久成就的雄心'},
            '水瓶座': {'trait': '改革理想', 'calling': '改變世界的理想主義'},
            '雙魚座': {'trait': '靈性連結', 'calling': '與更高存在的靈性連結'}
        }
        
        # 火星星座對應的戰鬥風格
        mars_styles = {
            '牡羊座': {'trait': '直接衝鋒', 'style': '總是第一個衝向敵人'},
            '金牛座': {'trait': '穩健防守', 'style': '如山岳般穩固的防禦'},
            '雙子座': {'trait': '靈活戰術', 'style': '變化多端的戰術運用'},
            '巨蟹座': {'trait': '保護戰法', 'style': '優先保護隊友的戰鬥方式'},
            '獅子座': {'trait': '英勇表現', 'style': '在戰場上展現英勇氣概'},
            '處女座': {'trait': '精準打擊', 'style': '每一擊都精確計算'},
            '天秤座': {'trait': '平衡攻防', 'style': '攻守平衡的戰鬥藝術'},
            '天蠍座': {'trait': '致命一擊', 'style': '等待時機給予致命打擊'},
            '射手座': {'trait': '遠程精準', 'style': '精準的遠程攻擊'},
            '摩羯座': {'trait': '持久作戰', 'style': '持久而有條理的戰鬥'},
            '水瓶座': {'trait': '創新戰法', 'style': '運用創新的戰鬥技巧'},
            '雙魚座': {'trait': '直覺戰鬥', 'style': '憑藉直覺進行戰鬥'}
        }
        
        sun_info = sun_traits.get(sun_sign, sun_traits['牡羊座'])
        moon_info = moon_motivations.get(moon_sign, moon_motivations['牡羊座'])
        mars_info = mars_styles.get(mars_sign, mars_styles['牡羊座'])
        
        return {
            'origin': sun_info['origin'],
            'environment': sun_info['environment'],
            'sun_trait': sun_info['trait'],
            'childhood': f"童年時期就顯露出與眾不同的{sun_info['trait']}。",
            'calling': moon_info['calling'],
            'moon_trait': moon_info['trait'],
            'training': f"經過嚴格的訓練，{class_info['name']}的技藝日臻完善。",
            'mars_trait': mars_info['trait'],
            'combat_style': mars_info['style'] + "。",
            'reputation': '備受尊敬',
            'motivation': f"懷著{moon_info['calling']}的信念，"
        }
    
    def generate_complete_character(self, chart_data: Dict) -> Dict:
        """
        生成完整的D&D角色
        
        Args:
            chart_data: 星盤數據
            
        Returns:
            完整的角色數據
        """
        # 計算屬性
        stats = self.calculate_character_stats(chart_data)
        
        # 確定職業
        dnd_class, class_score = self.determine_dnd_class(chart_data)
        class_info = self.dnd_classes[dnd_class]
        
        # 生成背景故事
        background = self.generate_character_background(chart_data, dnd_class, stats)
        
        # 計算總屬性分數和評級
        total_stats = sum(stats.values())
        if total_stats >= 75:
            rating = 'S'
        elif total_stats >= 70:
            rating = 'A'
        elif total_stats >= 65:
            rating = 'B'
        elif total_stats >= 60:
            rating = 'C'
        else:
            rating = 'D'
        
        return {
            'name': chart_data['birth_info']['name'],
            'class': {
                'key': dnd_class,
                'name': class_info['name'],
                'description': class_info['description'],
                'match_score': round(class_score, 2)
            },
            'stats': stats,
            'total_stats': total_stats,
            'rating': rating,
            'background': background,
            'personality_traits': class_info['personality_traits'],
            'primary_stats': class_info['primary_stats'],
            'birth_chart': {
                'sun': f"{chart_data['planets']['sun']['sign']} 第{chart_data['planets']['sun']['house']}宮",
                'moon': f"{chart_data['planets']['moon']['sign']} 第{chart_data['planets']['moon']['house']}宮",
                'ascendant': chart_data['angles']['ascendant']['sign']
            }
        }

# 測試函數
def test_dnd_generator():
    """測試D&D角色生成器"""
    astrologer = ProfessionalAstrologer()
    generator = DnDCharacterGenerator()
    
    # 計算星盤
    chart_data = astrologer.calculate_natal_chart(
        "艾莉亞", 1989, 9, 23, 12, 30, "台北",
        121.5654, 25.033, "Asia/Taipei"
    )
    
    # 生成D&D角色
    character = generator.generate_complete_character(chart_data)
    
    print("🎲 D&D角色生成測試")
    print("=" * 50)
    print(f"角色名稱: {character['name']}")
    print(f"職業: {character['class']['name']} ({character['class']['description']})")
    print(f"匹配度: {character['class']['match_score']}")
    print(f"評級: {character['rating']}級")
    print(f"總屬性: {character['total_stats']}")
    
    print("\n📊 屬性分配:")
    for stat, value in character['stats'].items():
        print(f"  {stat.capitalize()}: {value}")
    
    print(f"\n📜 角色背景:\n{character['background']}")
    
    return character

if __name__ == "__main__":
    test_dnd_generator()

