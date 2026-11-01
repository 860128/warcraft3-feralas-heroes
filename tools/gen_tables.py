# -*- coding: utf-8 -*-
"""Generate factory/table/unit.ini, ability.ini, misc.ini for Feralas map."""
import os

TABLE = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\factory_tpl\table"
os.makedirs(TABLE, exist_ok=True)

# ------------------------------------------------------------------ unit.ini
unit_txt = '''[H002]
_parent = "Obla"
Name = "幻梦大师"
Propernames = "莫菲斯,索姆纳斯,幻蝶,虚妄之影,梦行者,幽幻"
Tip = "召唤幻梦大师(|cffffcc00D|r)"
Ubertip = "擅长操纵梦境与幻象的敏捷型神秘英雄。能制造拥有完全战力的本体镜像并隐匿身形，暂时夺取任何敌军、野怪或建筑的操控权，召唤大范围敌军的真实幻象，并能领悟【幻界主宰】使所有幻术产生机制质变。"
Revivetip = "复活幻梦大师(|cffffcc00D|r)"
Awakentip = "唤醒幻梦大师(|cffffcc00D|r)"
Hotkey = "D"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNHeroBlademaster.blp"
file = "units\\\\orc\\\\HeroBladeMaster\\\\HeroBladeMaster"
"file:hd" = "units\\\\orc\\\\HeroBladeMaster\\\\HeroBladeMaster"
"file:sd" = "units\\\\orc\\\\HeroBladeMaster\\\\HeroBladeMaster"
unitSound = "HeroBladeMaster"
primary = "AGI"
STR = 22
STRplus = 2.40
AGI = 25
AGIplus = 2.80
INT = 20
INTplus = 2.20
HP = 650
regenHP = 2.50
manaN = 300
mana0 = 300
regenMana = 2.00
spd = 320
def = 4.0
dmgplus1 = 28
dice1 = 2
sides1 = 8
cool1 = 1.65
fused = 5
goldcost = 425
lumbercost = 100
bldtm = 55
heroAbilList = "A001,A002,A003,A004"
abilList = "AInv"
requirescount = 0
requires1 = ""
requires2 = ""

[u00D]
_parent = "ewsp"
Name = "幻梦辅助马甲"
abilList = "Aloc,Avul"
movetp = "fly"
spd = 0
HP = 1000
sight = 0
nsight = 0
modelScale = 0.01
Art = ""

[halt]
_parent = "halt"
Trains = "Hamg,Hmkg,Hpal,Hblm,H002"

[oalt]
_parent = "oalt"
Trains = "Obla,Ofar,Otch,Oshd,H002"

[uaod]
_parent = "uaod"
Trains = "Udea,Udre,Ulic,Ucrl,H002"

[eate]
_parent = "eate"
Trains = "Edem,Ekee,Emoo,Ewar,H002"
'''

with open(os.path.join(TABLE, "unit.ini"), "w", encoding="utf-8", newline="\r\n") as f:
    f.write(unit_txt)
print("[ok] unit.ini written")

# ------------------------------------------------------------------ ability.ini
abil_txt = '''[A001]
_parent = "AOmi"
Name = "镜像"
Hotkey = "Q"
Researchhotkey = "Q"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNMirrorImage.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNMirrorImage.blp"
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Buttonpos_1 = 0
Buttonpos_2 = 2
Researchbuttonpos_1 = 0
Researchbuttonpos_2 = 0
DataA = {1 = 1, 2 = 2, 3 = 3}
DataB = {1 = 0.40, 2 = 0.70, 3 = 1.00}
DataC = {1 = 1.80, 2 = 1.40, 3 = 1.00}
DataD = {1 = 0.50, 2 = 0.50, 3 = 0.50}
Dur = {1 = 60.0, 2 = 60.0, 3 = 60.0}
HeroDur = {1 = 60.0, 2 = 60.0, 3 = 60.0}
Cool = {1 = 12.0, 2 = 12.0, 3 = 12.0}
Cost = {1 = 100, 2 = 110, 3 = 120}
Tip = {1 = "镜像(|cffffcc00Q|r) - [|cffffcc00等级 1|r]", 2 = "镜像(|cffffcc00Q|r) - [|cffffcc00等级 2|r]", 3 = "镜像(|cffffcc00Q|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "制造 1 个迷惑敌人的幻梦镜像。镜像拥有本体 40% 的攻击力，承受 180% 的伤害。施法瞬间本体自动进入疾风步隐身状态，移动并潜行，攻击或施法将打破隐身。持续 60 秒。", 2 = "制造 2 个迷惑敌人的幻梦镜像。镜像拥有本体 70% 的攻击力，承受 140% 的伤害。施法瞬间本体自动进入疾风步隐身状态，持续 60 秒。", 3 = "制造 3 个完全镜像！镜像拥有本体 100% 的攻击力、100% 的防御力与 100% 的真实血量承受！施法瞬间本体自动进入疾风步隐身状态，持续 60 秒。"}
Researchtip = "学习 镜像(|cffffcc00Q|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "制造分身迷惑敌人，最高级拥有 100% 攻防与血量，施法瞬间本体自动隐身。"

[A00W]
_parent = "AOwk"
Name = "幻梦隐形"
levels = 3
hero = 0
item = 0
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0.20, 2 = 0.35, 3 = 0.50}
DataC = {1 = 50.0, 2 = 80.0, 3 = 120.0}
Dur = {1 = 30.0, 2 = 45.0, 3 = 60.0}
HeroDur = {1 = 30.0, 2 = 45.0, 3 = 60.0}
Cost = {1 = 0, 2 = 0, 3 = 0}
Cool = {1 = 0.0, 2 = 0.0, 3 = 0.0}

[A002]
_parent = "ANcl"
Name = "幻梦奴役"
Hotkey = "W"
Researchhotkey = "W"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNPossession.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNPossession.blp"
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Buttonpos_1 = 1
Buttonpos_2 = 2
Researchbuttonpos_1 = 1
Researchbuttonpos_2 = 0
DataA = {1 = 1.0, 2 = 1.0, 3 = 1.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 0, 2 = 0, 3 = 0}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 1, 2 = 1, 3 = 1}
DataF = {1 = "charm", 2 = "charm", 3 = "charm"}
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cool = {1 = 30.0, 2 = 25.0, 3 = 20.0}
Cost = {1 = 100, 2 = 125, 3 = 150}
targs = {1 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward", 2 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward", 3 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward"}
Tip = {1 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 1|r]", 2 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 2|r]", 3 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "将目标单位、野怪或建筑的心智拖入幻梦，强行夺取其绝对操控权，持续 30 秒。持续时间结束后归还所属权。若控制敌方英雄，英雄阵亡前必定归还给原主，绝不在己方祭坛复活。", 2 = "强行夺取目标单位、野怪或建筑的操控权，持续 2 分钟 (120 秒)。到期归还，阵亡英雄归还原主。", 3 = "强行夺取目标单位、野怪或建筑的操控权，持续 10 分钟 (600 秒)！到期归还，阵亡英雄归还原主。"}
Researchtip = "学习 幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "操控任何单位、野怪甚至敌方建筑与英雄。1级持续30秒，2级2分钟，3级10分钟。"

[A003]
_parent = "ACsi"
Name = "万象皆虚"
Hotkey = "E"
Researchhotkey = "E"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNWand.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNWand.blp"
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Buttonpos_1 = 2
Buttonpos_2 = 2
Researchbuttonpos_1 = 2
Researchbuttonpos_2 = 0
Area = {1 = 250.0, 2 = 350.0, 3 = 450.0}
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cool = {1 = 35.0, 2 = 30.0, 3 = 25.0}
Cost = {1 = 120, 2 = 140, 3 = 160}
Dur = {1 = 0.0, 2 = 0.0, 3 = 0.0}
HeroDur = {1 = 0.0, 2 = 0.0, 3 = 0.0}
targs = {1 = "air,ground,enemy,neutral,friend", 2 = "air,ground,enemy,neutral,friend", 3 = "air,ground,enemy,neutral,friend"}
Tip = {1 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 1|r]", 2 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 2|r]", 3 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "选定 250 码范围，将其内所有单位的灵魂具现化为真实幻象！召唤的幻象几乎可视为本体，能完整使用全部主动技能与魔法，不占人口，持续长达 15 分钟 (900 秒)！", 2 = "召唤 350 码范围内所有单位的真实幻象，可使用主动技能，持续 15 分钟。", 3 = "召唤 450 码范围内所有单位的真实幻象，大军成型，持续 15 分钟！"}
Researchtip = "学习 万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "在指定范围内召唤所有单位的真实幻象，甚至连主动技能都能自由使用，持续 15 分钟。"

[A004]
_parent = "AEev"
Name = "幻界主宰"
Hotkey = "R"
Researchhotkey = "R"
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNEvasion.blp"
ResearchArt = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNEvasion.blp"
levels = 1
hero = 1
reqLevel = 6
Buttonpos_1 = 3
Buttonpos_2 = 2
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
DataA = {1 = 0.0}
Tip = {1 = "幻界主宰(|cffffcc00R|r) - [终极被动]"}
Ubertip = {1 = "被动【阿哈利姆神杖质变】：唤醒梦境至高权柄，使前三个技能获得质的飞跃：|n|cffffcc001. 镜像质变【真幻同生 & 破隐一击】|r：隐身移速达到极限522且无视碰撞体积；破隐一击附加 200 点致命暗影伤害与 1.5 秒晕眩；镜像消亡时产生【幻象反冲】，自爆造成 200 点范围伤害与减速。|n|cffffcc002. 幻梦奴役质变【狂乱梦噬 & 杀戮延时】|r：被控制目标获得狂暴祝福（+40%移速、+50%攻速，每秒恢复 3% 最大生命）；且被控制单位每击杀一个敌军，控制时间自动延长 15 秒！若控制的是建筑，其攻速与自愈速度翻倍。|n|cffffcc003. 万象皆虚质变【梦魇剥离 & 幻体反哺】|r：施法瞬间使范围内所有敌军陷入 3 秒梦魇昏睡与沉默；召唤出的所有幻象部队，其攻击与技能伤害的 25% 将源源不断地转化为生命值反哺幻梦大师！"}
Researchtip = "领悟 幻界主宰(|cffffcc00R|r)"
Researchubertip = "被动终极技能：类似阿哈利姆神杖，全面颠覆与进化前三个技能的实战机制。"
'''

with open(os.path.join(TABLE, "ability.ini"), "w", encoding="utf-8", newline="\r\n") as f:
    f.write(abil_txt)
print("[ok] ability.ini written")
