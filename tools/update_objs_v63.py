# -*- coding: utf-8 -*-
"""
v6.3 对象数据补丁：
- 新增中立建筑 [n005] 暗杀介绍所 · 幽影杀手公会
- 新增 6 类针对性中立杀手单位 [u005]~[u00A]
- 新增 10 个动态目标悬赏槽 [A050]~[A059] 与 1 个情报刷新键 [A05A]
- 更新 factory_tpl/table 后调用 w2l.exe obj 编译并提取至 payload/war3map.w3u 与 payload/war3map.w3a
"""
import os
import re
import subprocess

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
TPL_DIR = os.path.join(ROOT, "factory_tpl")
UNIT_INI = os.path.join(TPL_DIR, "table", "unit.ini")
ABIL_INI = os.path.join(TPL_DIR, "table", "ability.ini")
W2L_EXE = os.path.join(ROOT, "tools", "w3x2lni", "w2l.exe")
STORM_DLL = os.path.join(ROOT, "tools", "StormLibSharp.dll")
PAYLOAD_DIR = os.path.join(ROOT, "payload")

NEW_UNITS = r'''
[n005]
_parent = "halt"
Name = "暗杀介绍所 · 幽影杀手公会"
Ubertip = "【中立全图鉴暗杀机构】实时扫描场上所有敌方英雄与强力Boss，展示目标真实头像、实力等级与动态雇佣报价。|n|n|cffffcc00服务承诺：|r|n- 下单后立即派出【针对目标机制硬克制】的专属中立杀手小队；|n- 杀手不受任何玩家控制，自动追猎目标，途中遭遇任何阻拦或攻击者将顺路毁灭阻碍；|n- 若当前波次杀手遭歼灭，公会将在3秒后自动派出人数更多、属性翻倍的下一波杀手，直到目标彻底死亡为止！"
Art = "ReplaceableTextures\\CommandButtons\\BTNBlackMarket.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNBlackMarket.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNBlackMarket.blp"
file = "buildings\\other\\Marketplace\\Marketplace"
"file:hd" = "buildings\\other\\Marketplace\\Marketplace"
"file:sd" = "buildings\\other\\Marketplace\\Marketplace"
unitSound = "MercenaryCamp"
modelScale = 1.05
HP = 999999
def = 99.0
abilList = "Avul,A050,A051,A052,A053,A054,A055,A056,A057,A058,A059,A05A"
Requires = ""
requirescount = 0
goldcost = 0
lumbercost = 0
bldtm = 1
Revive = 0
Trains = ""
sight = 1400
nsight = 1400

[u005]
_parent = "nbal"
Name = "暗杀专员 · 破法弑神者"
Ubertip = "暗杀介绍所特派【反魔虚罗】专属处决杀手：混乱远程重击，完全穿透魔虚罗一切适应抗性与物理护甲，不触发任何法轮适应与属性成长，附带纯粹真实伤害，可直接破除并泯灭其涅槃金卵！"
Art = "ReplaceableTextures\\CommandButtons\\BTNEvilIllidan.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNEvilIllidan.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNEvilIllidan.blp"
file = "units\\nightelf\\EvilIllidan\\IllidanEvil"
"file:hd" = "units\\nightelf\\EvilIllidan\\IllidanEvil"
"file:sd" = "units\\nightelf\\EvilIllidan\\IllidanEvil"
unitSound = "EvilIllidan"
modelScale = 1.25
HP = 4500
regenHP = 15.0
def = 14.0
defType = "hero"
spd = 460
sight = 1800
nsight = 1800
acquire = 1200.0
weapsOn = 1
atkType1 = "chaos"
weapTp1 = "missile"
Missileart = "Abilities\\Weapons\\DemonHunterMissile\\DemonHunterMissile.mdl"
Missilespeed = 1800
Missilearc = 0.05
MissileHoming = 1
dmgplus1 = 180
dice1 = 2
sides1 = 10
cool1 = 0.80
rangeN1 = 420
targs1 = "ground,structure,debris,air,item,ward"
abilList = "ACmi,A046,Atru"
goldcost = 0
lumbercost = 0
foodCost = 0
bountyplus = 0
bountydice = 0
bountysides = 0
level = 10

[u006]
_parent = "nggr"
Name = "暗杀专员 · 禁魔镇魂石像"
Ubertip = "暗杀介绍所特派【反魔音忍者】专属处决杀手：永久魔免不吃竭心光环、因果必中无视闪避、真视破隐、对分身与召唤物造成10倍毁灭伤害，击中本体强制关闭光环并禁止业火印记复活！"
Art = "ReplaceableTextures\\CommandButtons\\BTNRockGolem.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNRockGolem.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNRockGolem.blp"
file = "units\\creeps\\RockGolem\\RockGolem"
"file:hd" = "units\\creeps\\RockGolem\\RockGolem"
"file:sd" = "units\\creeps\\RockGolem\\RockGolem"
unitSound = "RockGolem"
modelScale = 1.30
HP = 5200
regenHP = 18.0
def = 16.0
defType = "hero"
spd = 435
sight = 1800
nsight = 1800
acquire = 1200.0
weapsOn = 1
atkType1 = "chaos"
weapTp1 = "missile"
Missileart = "Abilities\\Weapons\\RockBoltMissile\\RockBoltMissile.mdl"
Missilespeed = 1600
Missilearc = 0.12
MissileHoming = 1
dmgplus1 = 190
dice1 = 2
sides1 = 10
cool1 = 0.85
rangeN1 = 280
targs1 = "ground,structure,debris,air,item,ward"
abilList = "ACmi,A046,Atru"
goldcost = 0
lumbercost = 0
foodCost = 0
bountyplus = 0
bountydice = 0
bountysides = 0
level = 10

[u007]
_parent = "ngir"
Name = "暗杀专员 · 净世焚虫机甲"
Ubertip = "暗杀介绍所特派【反异种虫皇】专属处决杀手：全机械魔免机体免疫捕食吞噬并反噬灼烧虫皇，破隐真视震出潜地，抵消三阶虫皇吸血并附加高额纯粹火焰真伤！"
Art = "ReplaceableTextures\\CommandButtons\\BTNJunkGolem.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNJunkGolem.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNJunkGolem.blp"
file = "units\\creeps\\IronGolem\\IronGolem"
"file:hd" = "units\\creeps\\IronGolem\\IronGolem"
"file:sd" = "units\\creeps\\IronGolem\\IronGolem"
unitSound = "ClockwerkGoblin"
modelScale = 1.25
HP = 5000
regenHP = 16.0
def = 15.0
defType = "hero"
spd = 450
sight = 1800
nsight = 1800
acquire = 1200.0
weapsOn = 1
atkType1 = "chaos"
weapTp1 = "missile"
Missileart = "Abilities\\Weapons\\FireBallMissile\\FireBallMissile.mdl"
Missilespeed = 1650
Missilearc = 0.08
MissileHoming = 1
dmgplus1 = 195
dice1 = 2
sides1 = 10
cool1 = 0.85
rangeN1 = 360
targs1 = "ground,structure,debris,air,item,ward"
abilList = "ACmi,A046,Atru"
goldcost = 0
lumbercost = 0
foodCost = 0
bountyplus = 0
bountydice = 0
bountysides = 0
level = 10

[u008]
_parent = "hspt"
Name = "暗杀专员 · 猎灵破法裁决者"
Ubertip = "暗杀介绍所特派【反万灵化身】专属处决杀手：550码超远混乱防空射线，对伥鬼军团、精英野怪与召唤兽造成8倍秒杀伤害，无视巨龙魔免直接附加纯粹破灵斩首真伤，且绝不被收编为伥鬼！"
Art = "ReplaceableTextures\\CommandButtons\\BTNSpellBreaker.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNSpellBreaker.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNSpellBreaker.blp"
file = "units\\human\\BloodElfSpellThief\\BloodElfSpellThief"
"file:hd" = "units\\human\\BloodElfSpellThief\\BloodElfSpellThief"
"file:sd" = "units\\human\\BloodElfSpellThief\\BloodElfSpellThief"
unitSound = "SpellBreaker"
modelScale = 1.30
HP = 4600
regenHP = 15.0
def = 14.0
defType = "hero"
spd = 455
sight = 1800
nsight = 1800
acquire = 1200.0
weapsOn = 1
atkType1 = "chaos"
weapTp1 = "missile"
Missileart = "Abilities\\Weapons\\SpellBreakerMissile\\SpellBreakerMissile.mdl"
Missilespeed = 1850
Missilearc = 0.08
MissileHoming = 1
dmgplus1 = 185
dice1 = 2
sides1 = 10
cool1 = 0.80
rangeN1 = 550
targs1 = "ground,structure,debris,air,item,ward"
abilList = "ACmi,A046,Atru"
goldcost = 0
lumbercost = 0
foodCost = 0
bountyplus = 0
bountydice = 0
bountysides = 0
level = 10

[u009]
_parent = "hspt"
Name = "暗杀专员 · 破妄真瞳猎手"
Ubertip = "暗杀介绍所特派【反幻梦大师】专属处决杀手：真视破除一切潜行、免疫幻梦奴役、对幻象与镜像造成10倍一刀清场伤害，并高额真伤直取本体！"
Art = "ReplaceableTextures\\CommandButtons\\BTNHeroDemonHunter.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNHeroDemonHunter.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNHeroDemonHunter.blp"
file = "units\\nightelf\\HeroDemonHunter\\HeroDemonHunter"
"file:hd" = "units\\nightelf\\HeroDemonHunter\\HeroDemonHunter"
"file:sd" = "units\\nightelf\\HeroDemonHunter\\HeroDemonHunter"
unitSound = "HeroDemonHunter"
modelScale = 1.25
HP = 4600
regenHP = 15.0
def = 14.0
defType = "hero"
spd = 465
sight = 1800
nsight = 1800
acquire = 1200.0
weapsOn = 1
atkType1 = "chaos"
weapTp1 = "missile"
Missileart = "Abilities\\Weapons\\DemonHunterMissile\\DemonHunterMissile.mdl"
Missilespeed = 1850
Missilearc = 0.05
MissileHoming = 1
dmgplus1 = 185
dice1 = 2
sides1 = 10
cool1 = 0.78
rangeN1 = 300
targs1 = "ground,structure,debris,air,item,ward"
abilList = "ACmi,A046,Atru"
goldcost = 0
lumbercost = 0
foodCost = 0
bountyplus = 0
bountydice = 0
bountysides = 0
level = 10

[u00A]
_parent = "hkni"
Name = "暗杀专员 · 圣光混乱裁决者"
Ubertip = "暗杀介绍所特派【反恶魔领主/通用Boss】圣光混乱裁决小队：拥有极高混乱圣光灌伤输出，对阿克蒙德等恶魔领主、高级英雄及其护卫召唤物造成毁灭性精准打击！"
Art = "ReplaceableTextures\\CommandButtons\\BTNHeroPaladin.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNHeroPaladin.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNHeroPaladin.blp"
file = "units\\human\\HeroPaladin\\HeroPaladin"
"file:hd" = "units\\human\\HeroPaladin\\HeroPaladin"
"file:sd" = "units\\human\\HeroPaladin\\HeroPaladin"
unitSound = "HeroPaladin"
modelScale = 1.30
HP = 4800
regenHP = 16.0
def = 15.0
defType = "hero"
spd = 450
sight = 1800
nsight = 1800
acquire = 1200.0
weapsOn = 1
atkType1 = "chaos"
weapTp1 = "missile"
Missileart = "Abilities\\Weapons\\HolyBoltMissile\\HolyBoltMissile.mdl"
Missilespeed = 1800
Missilearc = 0.05
MissileHoming = 1
dmgplus1 = 195
dice1 = 2
sides1 = 12
cool1 = 0.85
rangeN1 = 260
targs1 = "ground,structure,debris,air,item,ward"
abilList = "ACmi,A046,Atru"
goldcost = 0
lumbercost = 0
foodCost = 0
bountyplus = 0
bountydice = 0
bountysides = 0
level = 10
'''

SLOTS = [
    ("A050", 0, 0, "acidbomb"),
    ("A051", 1, 0, "ambush"),
    ("A052", 2, 0, "ancestralspirit"),
    ("A053", 3, 0, "animatedead"),
    ("A054", 0, 1, "avatar"),
    ("A055", 1, 1, "banish"),
    ("A056", 2, 1, "barkskin"),
    ("A057", 3, 1, "berserk"),
    ("A058", 0, 2, "blackarrow"),
    ("A059", 1, 2, "blizzard"),
]

def build_new_abils():
    blocks = []
    for i, (aid, bx, by, order) in enumerate(SLOTS):
        blocks.append(f'''[{aid}]
_parent = "ANcl"
Name = "暗杀悬赏目标 #{i+1}"
Buttonpos_1 = {bx}
Buttonpos_2 = {by}
levels = 1
hero = 0
item = 0
checkdep = 0
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNSelectHeroOn.blp"
"Art:hd" = "ReplaceableTextures\\\\CommandButtons\\\\BTNSelectHeroOn.blp"
"Art:sd" = "ReplaceableTextures\\\\CommandButtons\\\\BTNSelectHeroOn.blp"
CasterArt = ""
"CasterArt:hd" = ""
"CasterArt:sd" = ""
EffectArt = ""
"EffectArt:hd" = ""
"EffectArt:sd" = ""
TargetArt = ""
"TargetArt:hd" = ""
"TargetArt:sd" = ""
DataA = {{1 = 0.0}}
DataB = {{1 = 0}}
DataC = {{1 = 1}}
DataD = {{1 = 0.0}}
DataE = {{1 = 0}}
DataF = {{1 = "{order}"}}
Order = "{order}"
Cost = {{1 = 0}}
Cool = {{1 = 0.3}}
Cast = {{1 = 0.0}}
Tip = "悬赏槽 #{i+1}：等待探测目标"
Ubertip = "点击聘请幽影杀手公会派出针对性克制杀手小队追杀此目标。"''')

    blocks.append('''[A05A]
_parent = "ANcl"
Name = "刷新悬赏情报 / 查看暗杀进度"
Buttonpos_1 = 3
Buttonpos_2 = 2
levels = 1
hero = 0
item = 0
checkdep = 0
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNReveal.blp"
"Art:hd" = "ReplaceableTextures\\\\CommandButtons\\\\BTNReveal.blp"
"Art:sd" = "ReplaceableTextures\\\\CommandButtons\\\\BTNReveal.blp"
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
DataB = {1 = 0}
DataC = {1 = 1}
DataD = {1 = 0.0}
DataE = {1 = 0}
DataF = {1 = "battleroar"}
Order = "battleroar"
Cost = {1 = 0}
Cool = {1 = 0.5}
Cast = {1 = 0.0}
Tip = "|cffffcc00刷新悬赏情报 & 查看进行中契约|r"
Ubertip = "立即重新扫描全图所有敌方英雄与Boss的实力变化与动态报价，并在屏幕列出所有正在执行中的暗杀契约波次进度。"''')
    return "\n\n".join(blocks)


def strip_old_section(text, start_marker):
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
    u_txt = strip_old_section(u_txt, "n005")
    u_txt = u_txt.rstrip() + "\n" + NEW_UNITS.strip() + "\n"
    with open(UNIT_INI, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(u_txt)

    with open(ABIL_INI, "r", encoding="utf-8") as f:
        a_txt = f.read().replace("\r\n", "\n")
    a_txt = strip_old_section(a_txt, "A050")
    a_txt = a_txt.rstrip() + "\n\n" + build_new_abils().strip() + "\n"
    with open(ABIL_INI, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(a_txt)

    tmp_w3x = os.path.join(ROOT, "tmp_v63_objs.w3x")
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

    ps = rf'''
$ErrorActionPreference = 'Stop'
$asm = [Reflection.Assembly]::LoadFrom('{STORM_DLL}')
$mpq = New-Object StormLibSharp.MpqArchive('{tmp_w3x}', [System.IO.FileAccess]::Read)
$mpq.ExtractFile('war3map.w3u', '{os.path.join(PAYLOAD_DIR, "war3map.w3u")}')
$mpq.ExtractFile('war3map.w3a', '{os.path.join(PAYLOAD_DIR, "war3map.w3a")}')
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

    print(
        f"[ok] Compiled & extracted v6.3 objs: w3u={os.path.getsize(os.path.join(PAYLOAD_DIR, 'war3map.w3u'))} B, "
        f"w3a={os.path.getsize(os.path.join(PAYLOAD_DIR, 'war3map.w3a'))} B"
    )


if __name__ == "__main__":
    main()
