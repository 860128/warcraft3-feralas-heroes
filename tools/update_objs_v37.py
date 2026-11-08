# -*- coding: utf-8 -*-
import os, sys

def main():
    p = os.path.join(os.path.dirname(__file__), 'build_v13_objs.py')
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find [A035]
    idx = text.find('[A035]')
    assert idx != -1, "[A035] not found"
    end_idx = text.find('"""\n\nini_unit =', idx)
    assert end_idx != -1, "end of ini_abil not found"

    new_abilities = '''[A035]
_parent = "ANcl"
Name = "众野之怒"
Hotkey = "D"
Researchhotkey = "D"
Buttonpos_1 = 2
Buttonpos_2 = 1
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
levels = 1
hero = 1
reqLevel = 6
Art = "ReplaceableTextures\\\\\\\\CommandButtons\\\\\\\\BTNStampede.blp"
ResearchArt = "ReplaceableTextures\\\\\\\\CommandButtons\\\\\\\\BTNStampede.blp"
DataA = {1 = 0.0}
DataB = {1 = 0}
DataC = {1 = 1}
DataD = {1 = 0.0}
DataE = {1 = 0}
DataF = {1 = "starfall"}
Order = "starfall"
Cost = {1 = 150}
Cool = {1 = 110.0}
Tip = {1 = "众野之怒(|cffffcc00D|r)"}
Ubertip = {1 = "唤醒荒野狂暴大军向敌方核心基地发起不可控推线冲锋！冲锋大军强度随英雄等级进阶：6~7级荒野精锐群兽(冷却110秒)，8~9级高阶巨兽军团(冷却100秒)，10级满级唤醒12头世界级Boss霸主巨浪(冷却90秒)！|n|n冲锋持续90秒。期间万灵化身本体触发【百鬼统帅共鸣】，本体军魂加成翻倍至100%战神状态！"}
Researchtip = "学习 众野之怒(|cffffcc00D|r)"
Researchubertip = "唤醒荒野兽潮，召唤拥有真实战力与血量的不可控荒野大军推线冲锋！【为虎作伥】：兽潮击杀敌方英雄炼化为伪英雄伥鬼（复制装备被动），击杀精锐小兵优胜劣汰收为精锐伥鬼；普通击杀叠加【百鬼军魂】永久强化全体荒野大军属性并在场即时成长！"

[A036]
_parent = "ACdv"
hero = 0
levels = 1
Requires = ""
Buttonpos_1 = 0
Buttonpos_2 = -11
DataA = {1 = 0.0}
Area = {1 = 10.0}
targs = {1 = "self"}
Art = "ReplaceableTextures\\\\\\\\PassiveButtons\\\\\\\\PASBTNCommand.blp"
Name = "百鬼军魂"
Tip = {1 = "百鬼军魂"}
Ubertip = {1 = "已凝聚荒野战魂，强化自身与众野之怒大军。"}

[A037]
_parent = "ANcl"
hero = 0
levels = 3
Requires = ""
Hotkey = "F"
Buttonpos_1 = 0
Buttonpos_2 = 1
Cost = {1 = 50, 2 = 50, 3 = 50}
Cool = {1 = 18.0, 2 = 14.0, 3 = 10.0}
Rng = {1 = 300.0, 2 = 350.0, 3 = 400.0}
Art = "ReplaceableTextures\\\\\\\\CommandButtons\\\\\\\\BTNDevour.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "soulburn", 2 = "soulburn", 3 = "soulburn"}
Order = "soulburn"
targs = "air,ground,enemy,neutral,organic"
Name = "巨龙吞噬"
Tip = {
1 = "巨龙吞噬(|cffffcc00F|r) - [1阶]",
2 = "巨龙吞噬(|cffffcc00F|r) - [2阶]",
3 = "巨龙吞噬(|cffffcc00F|r) - [3阶]",
}
Ubertip = {
1 = "成年巨龙张开毁灭龙口，将目标敌方小兵或野怪瞬间吞入龙腹直接秒杀！为巨龙自身恢复 25% 最大生命值，并获得 +1 层【百鬼军魂】。无法吞噬英雄或建筑。冷却18秒。",
2 = "成年巨龙张开毁灭龙口，将目标敌方小兵或野怪瞬间吞入龙腹直接秒杀！为巨龙自身恢复 35% 最大生命值，并获得 +1 层【百鬼军魂】。无法吞噬英雄或建筑。冷却14秒。",
3 = "成年巨龙张开毁灭龙口，将目标敌方小兵或野怪瞬间吞入龙腹直接秒杀！为巨龙自身恢复 45% 最大生命值，并获得 +1 层【百鬼军魂】。无法吞噬英雄或建筑。冷却10秒。",
}

[ACmi]
_parent = "Amim"
hero = 0
levels = 1
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
Art = "ReplaceableTextures\\\\\\\\PassiveButtons\\\\\\\\PASBTNGenericSpellImmunity.blp"
Name = "霸主魔法免疫"
Tip = {1 = "霸主魔法免疫"}
Ubertip = {1 = "远古霸主神体拥有绝对的抗法能力，免疫所有敌方魔法技能。"}

[ANpi]
_parent = "ANpi"
hero = 0
levels = 1
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Art = "ReplaceableTextures\\\\\\\\PassiveButtons\\\\\\\\PASBTNImmolation.blp"
DataA = {1 = 65.0}
Area = {1 = 260.0}
Name = "地狱烈焰献祭"
Tip = {1 = "地狱烈焰献祭"}
Ubertip = {1 = "对周围敌方地面单位造成每秒 65 点烈焰灼烧伤害。"}'''

    text = text[:idx] + new_abilities + text[end_idx:]

    # Update H005 abilList
    if 'abilList = "AInv,A034,A036"' not in text:
        text = text.replace('abilList = "AInv,A034"', 'abilList = "AInv,A034,A036"', 1)

    # Update verification sym list
    if "b'A036'" not in text:
        text = text.replace("b'ACav', b'ACdv']:", "b'ACav', b'ACdv', b'A036', b'A037', b'ACmi', b'ANpi']:", 1)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    print("build_v13_objs.py successfully updated!")

if __name__ == '__main__':
    main()
