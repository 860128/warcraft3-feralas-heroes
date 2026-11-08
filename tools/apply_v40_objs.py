# -*- coding: utf-8 -*-
import sys
import os
import re

objs_file = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\build_v13_objs.py"

with open(objs_file, "r", encoding="utf-8") as f:
    text = f.read()

# Notice r'\\\\' gives literal \\\\ in the text written to build_v13_objs.py
new_a022 = r'''[A022]
_parent = "ANcl"
Name = "捕食吞噬"
Hotkey = "W"
Researchhotkey = "W"
Buttonpos_1 = 1
Buttonpos_2 = 2
Researchbuttonpos_1 = 1
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Cost = {1 = 75, 2 = 75, 3 = 75}
Cool = {1 = 20.0, 2 = 15.0, 3 = 10.0}
Rng = {1 = 250.0, 2 = 275.0, 3 = 300.0}
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDevour.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNDevour.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "devour", 2 = "devour", 3 = "devour"}
Order = "devour"
targs = "air,ground,enemy,neutral,organic"
Researchtip = "学习 捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "撕咬吞噬生命低于35%的敌方单位（英雄28%，或目标血量<=自身上限10%保底瞬吞）。|n吞噬后进入消化期（Lv1/2/3为6.5/5.0/3.5秒），恢复25%血蓝，解锁拟态样本，并触发【全维基因吸收】与【四阶蜕壳进化】：|n- |cff00ff80近战兵种|r：永久获得生命、攻击与永久护甲；|n- |cffff6600远程兵种|r：永久获得生命与高额攻击；|n- |cff33ccff魔法兵种|r：永久获得生命、法力与攻击；|n- |cffffcc00敌方英雄|r：抽取 6/8/10 点敏/力/智属性（镜像等额获得）+ 永久掠夺目标 10% 血量上限与 10% 攻击力，英雄计 +3 次蜕壳进度！|n- |cff00ccff四阶蜕壳|r：跳虫(0~7次) -> 紫晶巨蝎(8次) -> 星际刺蛇(18次) -> 始祖虫皇(30次)。"
Tip = {
1 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 1|r]",
2 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 2|r]",
3 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "撕咬吞噬生命值低于 35% 的非魔免敌方单位（英雄为 28%，或目标血量 <= 自身上限 10% 保底瞬吞）。|n消化时间：6.5 秒。消化完毕恢复 25% 血蓝，解锁拟态样本，并吸收复合基因（普通怪计+1次吞噬，英雄计+3次）：|n- |cff00ff80近战猎物|r：永久生命 +67、基础攻击 +3、永久护甲 +0.30 点；|n- |cffff6600远程猎物|r：永久攻击 +7、永久生命 +37；|n- |cff33ccff魔法猎物|r：永久法力 +50、永久生命 +44、永久攻击 +5；|n- |cffffcc00敌方英雄|r：递进抽取 6 点敏/力/智属性（镜像获得）+ 掠夺目标 10% 最大生命与 10% 基础攻击，英雄计 +3 次蜕壳进度！|n|n|cffffcc00冷却时间：20 秒|r",
2 = "撕咬吞噬生命值低于 35% 的非魔免敌方单位（英雄为 28%，或目标血量 <= 自身上限 10% 保底瞬吞）。|n消化时间：5.0 秒。消化完毕恢复 25% 血蓝，解锁拟态样本，并吸收复合基因（普通怪计+1次吞噬，英雄计+3次）：|n- |cff00ff80近战猎物|r：永久生命 +89、基础攻击 +4、永久护甲 +0.60 点；|n- |cffff6600远程猎物|r：永久攻击 +10、永久生命 +49；|n- |cff33ccff魔法猎物|r：永久法力 +65、永久生命 +58、永久攻击 +7；|n- |cffffcc00敌方英雄|r：递进抽取 8 点敏/力/智属性（镜像获得）+ 掠夺目标 10% 最大生命与 10% 基础攻击，英雄计 +3 次蜕壳进度！|n|n|cffffcc00冷却时间：15 秒|r",
3 = "撕咬吞噬生命值低于 35% 的非魔免敌方单位（英雄为 28%，或目标血量 <= 自身上限 10% 保底瞬吞）。|n消化时间：3.5 秒（3阶始祖虫皇极速缩至 1.0 秒）。消化完毕恢复 25% 血蓝，解锁拟态样本，并吸收复合基因（普通怪计+1次吞噬，英雄计+3次）：|n- |cff00ff80近战猎物|r：永久生命 +111、基础攻击 +5、永久护甲 +0.90 点；|n- |cffff6600远程猎物|r：永久攻击 +13、永久生命 +61；|n- |cff33ccff魔法猎物|r：永久法力 +80、永久生命 +72、永久攻击 +9；|n- |cffffcc00敌方英雄|r：递进抽取 10 点敏/力/智属性（镜像获得）+ 掠夺目标 10% 最大生命与 10% 基础攻击，英雄计 +3 次蜕壳进度！|n|n|cffffcc00冷却时间：10 秒（3阶始祖虫皇大幅缩至 4.0 秒）|r",
}'''

new_a024 = r'''[A024]
_parent = "ANcl"
Name = "异种进化"
Hotkey = "R"
Researchhotkey = "R"
Buttonpos_1 = 3
Buttonpos_2 = 2
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
levels = 1
hero = 1
reqLevel = 1
Cost = 0
Cool = 1.0
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNLocustSwarm.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNLocustSwarm.blp"
DataA = 0.0
DataB = 0
DataC = 1
DataD = 0.0
DataE = 0
DataF = "ancestralspirit"
Order = "ancestralspirit"
Researchtip = "学习 异种进化控制台(|cffffcc00R|r)"
Researchubertip = "激活星际虫族四阶蜕壳进化与基因控制台：|n- 【0阶 幼体·星际跳虫】(0~7次吞噬)：近战撕咬(128码)，体型1.15；|n- 【1阶 紫晶重装巨蝎】(8~17次)：移速+45，攻速+20%，+300 HP，+25 攻击，+4 护甲，破壳毒爆；|n- 【2阶 星际虫族刺蛇】(18~29次)：500码远程强酸骨刺弹道，每秒自动恢复2.5%最大生命再生甲壳，+600 HP，+45 攻击，+6 护甲；|n- 【3阶 终极·始祖利维坦虫皇】(30+次)：体型1.65，始祖暗紫金甲，永久魔法免疫('ACmi')，25%物理深渊吸血，终极【深渊饕餮】(4秒CD与1秒极速消化)，+1200 HP，+80 攻击，+10 护甲。|n随时按 R 可打开控制台查看吸收属性或遗忘管理技能槽。"
Tip = "异种进化控制台(|cffffcc00R|r)"
Ubertip = "激活星际虫族四阶蜕壳进化与基因控制台：|n- 【0阶 幼体·星际跳虫】(0~7次吞噬)：近战撕咬(128码)，体型1.15；|n- 【1阶 紫晶重装巨蝎】(8~17次)：移速+45，攻速+20%，+300 HP，+25 攻击，+4 护甲，破壳毒爆；|n- 【2阶 星际虫族刺蛇】(18~29次)：500码远程强酸骨刺弹道，每秒自动恢复2.5%最大生命再生甲壳，+600 HP，+45 攻击，+6 护甲；|n- 【3阶 终极·始祖利维坦虫皇】(30+次)：体型1.65，始祖暗紫金甲，永久魔法免疫('ACmi')，25%物理深渊吸血，终极【深渊饕餮】(4秒CD与1秒极速消化)，+1200 HP，+80 攻击，+10 护甲。|n随时按 R 可打开控制台查看吸收属性或遗忘管理技能槽。"'''

# Replace A022 block
pattern22 = r'\[A022\].*?(?=\n\[A023\])'
m22 = re.search(pattern22, text, re.DOTALL)
if not m22:
    print("Error: [A022] block not found")
    sys.exit(1)

text = text[:m22.start()] + new_a022 + "\n\n" + text[m22.end():]

# Replace A024 block
pattern24 = r'\[A024\].*?(?=\n\[A025\])'
m24 = re.search(pattern24, text, re.DOTALL)
if not m24:
    print("Error: [A024] block not found")
    sys.exit(1)

text = text[:m24.start()] + new_a024.strip() + "\n\n" + text[m24.end():]

with open(objs_file, "w", encoding="utf-8") as f:
    f.write(text)

print("build_v13_objs.py updated successfully!")
