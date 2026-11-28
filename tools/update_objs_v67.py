# -*- coding: utf-8 -*-
"""
v6.7 对象数据补丁：
- 新增实验测试小兵单位 [u00B] 实验小兵 · 万象状态师 (步兵模型)
- 新增主动技能 [A060] 万象全 Buff 加持 (9大满级光环 + 9大主动增益，不含魔免)
- 新增主动技能 [A061] 万厄全 Debuff 诅咒 (14重魔兽负面减益)
- 新增隐藏自光环法术书 [A062] 与 9 个仅作用于自身的满级光环 [A063]~[A06B]
- 新增 9 个增益马甲技能 [A06C]~[A074] 与 14 个负面减益马甲技能 [A075]~[A082]
- 调用 w2l.exe obj 编译并提取至 payload/war3map.w3u 与 payload/war3map.w3a
"""
import os
import subprocess

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
TPL_DIR = os.path.join(ROOT, "factory_tpl")
UNIT_INI = os.path.join(TPL_DIR, "table", "unit.ini")
ABIL_INI = os.path.join(TPL_DIR, "table", "ability.ini")
W2L_EXE = os.path.join(ROOT, "tools", "w3x2lni", "w2l.exe")
STORM_DLL = os.path.join(ROOT, "tools", "StormLibSharp.dll")
PAYLOAD_DIR = os.path.join(ROOT, "payload")

NEW_UNITS = r'''
[u00B]
_parent = "hfoo"
Name = "实验小兵 · 万象状态师"
Ubertip = "【实验测试单位】普通步兵模型，专用于测试全Buff与全Debuff叠加的实际战力：|n- |cff00ff80[Q] 万象全Buff加持|r：令目标获得 9 大满级光环 + 9 大主动正面Buff（持续45秒，不含魔免）！|n- |cffff3366[W] 万厄全Debuff诅咒|r：令目标瞬间承受 14 重魔兽负面减益！"
Art = "ReplaceableTextures\\CommandButtons\\BTNFootman.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNFootman.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNFootman.blp"
file = "units\\human\\Footman\\Footman"
"file:hd" = "units\\human\\Footman\\Footman"
"file:sd" = "units\\human\\Footman\\Footman"
unitSound = "Footman"
modelScale = 1.05
HP = 650
regenHP = 2.0
def = 4.0
spd = 320
manaN = 500
mana0 = 500
regenMana = 5.0
dmgplus1 = 16
cool1 = 1.35
foodCost = 0
goldcost = 0
lumbercost = 0
level = 3
abilList = "A060,A061"
'''

NEW_ABILS = r'''
[A060]
_parent = "ANcl"
Name = "万象全 Buff 加持"
Hotkey = "Q"
Buttonpos_1 = 0
Buttonpos_2 = 2
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Art = "ReplaceableTextures\\CommandButtons\\BTNBloodLust.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNBloodLust.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNBloodLust.blp"
CasterArt = ""
"CasterArt:hd" = ""
"CasterArt:sd" = ""
EffectArt = ""
"EffectArt:hd" = ""
"EffectArt:sd" = ""
TargetArt = ""
"TargetArt:hd" = ""
"TargetArt:sd" = ""
DataA = {1 = 0.0}
DataB = {1 = 1}
DataC = {1 = 1}
DataD = {1 = 0.0}
DataE = {1 = 0}
DataF = {1 = "holybolt"}
Order = "holybolt"
Rng = {1 = 900.0}
Cost = {1 = 0}
Cool = {1 = 3.0}
Cast = {1 = 0.0}
targs = {1 = "air,ground,friend,self,enemy,neutral,organic,mechanical"}
Tip = "|cff00ff80万象全 Buff 加持|r(|cffffcc00Q|r)"
Ubertip = "实验性全正面强化（|cffffcc00不含魔免|r，不外泄给周围单位）：|n- |cff00ffcc9 大满级自身光环（45秒）|r：专注/辉煌/耐久/邪恶/吸血/荆棘/强击/命令/科多战鼓；|n- |cff00ff809 大经典主动增益|r：嗜血、心灵之火、邪恶狂热、霜冻护甲、咆哮、返老还童、闪电护盾、灵魂链、隐身术。"

[A061]
_parent = "ANcl"
Name = "万厄全 Debuff 诅咒"
Hotkey = "W"
Buttonpos_1 = 1
Buttonpos_2 = 2
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Art = "ReplaceableTextures\\CommandButtons\\BTNCripple.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNCripple.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNCripple.blp"
CasterArt = ""
"CasterArt:hd" = ""
"CasterArt:sd" = ""
EffectArt = ""
"EffectArt:hd" = ""
"EffectArt:sd" = ""
TargetArt = ""
"TargetArt:hd" = ""
"TargetArt:sd" = ""
DataA = {1 = 0.0}
DataB = {1 = 1}
DataC = {1 = 1}
DataD = {1 = 0.0}
DataE = {1 = 0}
DataF = {1 = "cripple"}
Order = "cripple"
Rng = {1 = 900.0}
Cost = {1 = 0}
Cool = {1 = 3.0}
Cast = {1 = 0.0}
targs = {1 = "air,ground,enemy,friend,self,neutral,organic,mechanical"}
Tip = "|cffff3366万厄全 Debuff 诅咒|r(|cffffcc00W|r)"
Ubertip = "实验性全负面减益（省略吹风/沉睡/放逐以保证仍可被攻击测试）：|n令目标瞬间同时承受 |cffff664414 重经典 Debuff|r：残废、减速、诅咒、精灵之火、酸液炸弹、恐怖嚎叫、醉酒云雾、沉默术、灵魂燃烧、暗影突袭、纠缠根须、寒冰霜冻、诱捕网、妖术！"

[A062]
_parent = "Aspb"
Name = "万象全光环隐藏书"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
DataA = {1 = "A063,A064,A065,A066,A067,A068,A069,A06A,A06B"}
DataB = {1 = 0}
DataC = {1 = 9}
DataD = {1 = 9}
DataE = {1 = "spellbook"}

[A063]
_parent = "AHad"
Name = "实验光环 · 满级专注光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BHad"}
DataA = {1 = 4.5}
DataB = {1 = 0}

[A064]
_parent = "AHab"
Name = "实验光环 · 满级辉煌光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BHab"}
DataA = {1 = 2.25}
DataB = {1 = 0}

[A065]
_parent = "AOae"
Name = "实验光环 · 满级耐久光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BOae"}
DataA = {1 = 0.30}
DataB = {1 = 0.15}

[A066]
_parent = "AUau"
Name = "实验光环 · 满级邪恶光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BUau"}
DataA = {1 = 0.30}
DataB = {1 = 2.0}
DataC = {1 = 0}

[A067]
_parent = "AUav"
Name = "实验光环 · 满级吸血光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BUav"}
DataA = {1 = 0.45}

[A068]
_parent = "AEah"
Name = "实验光环 · 满级荆棘光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BEah"}
DataA = {1 = 0.30}
DataB = {1 = 1}

[A069]
_parent = "AEar"
Name = "实验光环 · 满级强击光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BEar"}
DataA = {1 = 0.30}
DataB = {1 = 0}
DataC = {1 = 1}
DataD = {1 = 0}

[A06A]
_parent = "ACac"
Name = "实验光环 · 满级命令光环"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "BOac"}
DataA = {1 = 0.20}
DataB = {1 = 1}
DataC = {1 = 1}
DataD = {1 = 0}

[A06B]
_parent = "Aakb"
Name = "实验光环 · 满级科多战鼓"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Area = {1 = 50.0}
targs = {1 = "self"}
BuffID = {1 = "Bakb"}
DataA = {1 = 0.10}
DataB = {1 = 1}
DataC = {1 = 1}
DataD = {1 = 0}
DataE = {1 = 1}

[A06C]
_parent = "Ablo"
Name = "实验增益 · 嗜血术"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 45.0}
HeroDur = {1 = 45.0}
DataA = {1 = 0.40}
DataB = {1 = 0.25}
DataC = {1 = 0.25}
targs = {1 = "air,ground,friend,self,neutral,organic,mechanical"}

[A06D]
_parent = "Ainf"
Name = "实验增益 · 心灵之火"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 45.0}
HeroDur = {1 = 45.0}
DataA = {1 = 0.10}
DataB = {1 = 5}
DataC = {1 = 500.0}
DataD = {1 = 1.5}
targs = {1 = "air,ground,friend,self,neutral,organic,mechanical"}

[A06E]
_parent = "Auhf"
Name = "实验增益 · 邪恶狂热"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 45.0}
HeroDur = {1 = 45.0}
DataA = {1 = 0.75}
DataB = {1 = 2.0}
targs = {1 = "air,ground,friend,self,enemy,neutral,organic,mechanical"}

[A06F]
_parent = "AUfa"
Name = "实验增益 · 霜冻护甲"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 5.0}
HeroDur = {1 = 3.0}
DataA = {1 = 45.0}
DataB = {1 = 7}
targs = {1 = "air,ground,friend,self,neutral,organic,mechanical"}

[A070]
_parent = "Aroa"
Name = "实验增益 · 咆哮"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 64.0}
Dur = {1 = 45.0}
HeroDur = {1 = 45.0}
DataA = {1 = 0.25}
targs = {1 = "air,ground,friend,self"}

[A071]
_parent = "Arej"
Name = "实验增益 · 返老还童"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 12.0}
HeroDur = {1 = 12.0}
DataA = {1 = 400.0}
DataB = {1 = 0.0}
DataC = {1 = 3}
targs = {1 = "air,ground,friend,self,vuln,invu,neutral,organic,mechanical"}

[A072]
_parent = "Alsh"
Name = "实验增益 · 闪电护盾"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 160.0}
Dur = {1 = 20.0}
HeroDur = {1 = 20.0}
DataA = {1 = 20.0}
targs = {1 = "air,ground,friend,self,enemy,neutral,organic,mechanical"}

[A073]
_parent = "Aspl"
Name = "实验增益 · 灵魂链"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 500.0}
Dur = {1 = 45.0}
HeroDur = {1 = 45.0}
DataA = {1 = 0.50}
DataB = {1 = 4}
targs = {1 = "air,ground,friend,self,organic,mechanical"}

[A074]
_parent = "Aivs"
Name = "实验增益 · 隐身术"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 45.0}
HeroDur = {1 = 45.0}
DataA = {1 = 0.0}
targs = {1 = "air,ground,friend,self,neutral,organic,mechanical"}

[A075]
_parent = "Acri"
Name = "实验诅咒 · 残废"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 30.0}
HeroDur = {1 = 10.0}
DataA = {1 = 0.75}
DataB = {1 = 0.50}
DataC = {1 = 0.50}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A076]
_parent = "Aslo"
Name = "实验诅咒 · 减速"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 30.0}
HeroDur = {1 = 10.0}
DataA = {1 = 0.60}
DataB = {1 = 0.25}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A077]
_parent = "Acrs"
Name = "实验诅咒 · 诅咒"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 45.0}
HeroDur = {1 = 20.0}
DataA = {1 = 0.33}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A078]
_parent = "Afae"
Name = "实验诅咒 · 精灵之火"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 45.0}
HeroDur = {1 = 20.0}
DataA = {1 = 4}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A079]
_parent = "ANab"
Name = "实验诅咒 · 酸液炸弹"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 1.0}
Dur = {1 = 15.0}
HeroDur = {1 = 15.0}
DataA = {1 = 0}
DataB = {1 = 0}
DataC = {1 = 5}
DataD = {1 = 8.0}
DataE = {1 = 5.0}
DataF = {1 = 1.0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A07A]
_parent = "ANht"
Name = "实验诅咒 · 恐怖嚎叫"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 64.0}
Dur = {1 = 15.0}
HeroDur = {1 = 15.0}
DataA = {1 = 0.50}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A07B]
_parent = "ANdh"
Name = "实验诅咒 · 醉酒云雾"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 1.0}
Dur = {1 = 12.0}
HeroDur = {1 = 5.0}
DataA = {1 = 0}
DataB = {1 = 0.65}
DataC = {1 = 0.50}
DataD = {1 = 0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A07C]
_parent = "ANsi"
Name = "实验诅咒 · 沉默术"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 64.0}
Dur = {1 = 16.0}
HeroDur = {1 = 8.0}
DataA = {1 = 8}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A07D]
_parent = "ANso"
Name = "实验诅咒 · 灵魂燃烧"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 14.0}
HeroDur = {1 = 6.0}
DataA = {1 = 10.0}
DataB = {1 = 1.0}
DataC = {1 = 0.50}
DataD = {1 = 0}
DataE = {1 = 0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A07E]
_parent = "AEsh"
Name = "实验诅咒 · 暗影突袭"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 15.1}
HeroDur = {1 = 15.1}
DataA = {1 = 12.0}
DataB = {1 = 0.50}
DataC = {1 = 0.0}
DataD = {1 = 3.0}
DataE = {1 = 15.0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A07F]
_parent = "AEer"
Name = "实验诅咒 · 纠缠根须"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 9.0}
HeroDur = {1 = 3.0}
DataA = {1 = 10.0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A080]
_parent = "AUfn"
Name = "实验诅咒 · 寒冰霜冻"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Area = {1 = 1.0}
Dur = {1 = 8.0}
HeroDur = {1 = 4.0}
DataA = {1 = 5.0}
DataB = {1 = 5.0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A081]
_parent = "Aens"
Name = "实验诅咒 · 诱捕网"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 10.0}
HeroDur = {1 = 3.0}
DataA = {1 = 0.60}
DataB = {1 = 200.0}
DataC = {1 = 128.0}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}

[A082]
_parent = "AOhx"
Name = "实验诅咒 · 妖术"
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Cost = {1 = 0}
Cool = {1 = 0.0}
Cast = {1 = 0.0}
Rng = {1 = 9999.0}
Dur = {1 = 12.0}
HeroDur = {1 = 4.0}
DataA = {1 = 99}
targs = {1 = "air,ground,enemy,neutral,organic,mechanical"}
'''


def strip_old_section(text: str, start_marker: str) -> str:
    idx = text.find(f"\n[{start_marker}]")
    if idx < 0:
        if text.startswith(f"[{start_marker}]"):
            idx = 0
        else:
            return text
    return text[:idx].rstrip() + "\n"


def main():
    with open(UNIT_INI, "r", encoding="utf-8") as f:
        u_txt = f.read().replace("\r\n", "\n")
    assert "[u00A]" in u_txt and "[n005]" in u_txt, "Missing existing v6.3 units in unit.ini!"
    u_txt = strip_old_section(u_txt, "u00B")
    u_txt = u_txt.rstrip() + "\n\n" + NEW_UNITS.strip() + "\n"
    with open(UNIT_INI, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(u_txt)

    with open(ABIL_INI, "r", encoding="utf-8") as f:
        a_txt = f.read().replace("\r\n", "\n")
    assert "[A05A]" in a_txt and "[A050]" in a_txt, "Missing existing v6.3 abilities in ability.ini!"
    a_txt = strip_old_section(a_txt, "A060")
    a_txt = a_txt.rstrip() + "\n\n" + NEW_ABILS.strip() + "\n"
    with open(ABIL_INI, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(a_txt)

    tmp_w3x = os.path.join(ROOT, "tmp_v67_objs.w3x")
    if os.path.exists(tmp_w3x):
        os.remove(tmp_w3x)
    res = subprocess.run(
        [W2L_EXE, "obj", TPL_DIR, tmp_w3x],
        cwd=os.path.dirname(W2L_EXE),
        input=b"y\ny\n",
        capture_output=True,
        timeout=30,
    )
    if res.returncode != 0 or not os.path.exists(tmp_w3x):
        raise RuntimeError(
            f"w2l obj failed rc={res.returncode}: "
            f"{res.stdout.decode('utf-8','replace')} | {res.stderr.decode('utf-8','replace')}"
        )

    w3u_out = os.path.join(PAYLOAD_DIR, "war3map.w3u")
    w3a_out = os.path.join(PAYLOAD_DIR, "war3map.w3a")
    ps = rf'''
$ErrorActionPreference = 'Stop'
$asm = [Reflection.Assembly]::LoadFrom('{STORM_DLL}')
$mpq = New-Object StormLibSharp.MpqArchive('{tmp_w3x}', [System.IO.FileAccess]::Read)
$mpq.ExtractFile('war3map.w3u', '{w3u_out}')
$mpq.ExtractFile('war3map.w3a', '{w3a_out}')
$mpq.Dispose()
'''
    ps_res = subprocess.run(
        [r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe", "-NoProfile", "-Command", ps],
        capture_output=True, text=True, timeout=20,
    )
    if ps_res.returncode != 0:
        raise RuntimeError(f"Extract failed: {ps_res.stderr}")
    if os.path.exists(tmp_w3x):
        os.remove(tmp_w3x)

    w3u_sz = os.path.getsize(w3u_out)
    w3a_sz = os.path.getsize(w3a_out)
    assert w3u_sz > 13652, f"Expected w3u > 13652 B, got {w3u_sz}"
    assert w3a_sz > 65533, f"Expected w3a > 65533 B, got {w3a_sz}"
    print(f"[ok] Compiled & extracted v6.7 objs: w3u={w3u_sz} B, w3a={w3a_sz} B")


if __name__ == "__main__":
    main()
