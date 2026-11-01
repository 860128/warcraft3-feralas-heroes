import os, subprocess

ini_ability = """[A001]
_parent = "AOmi"
Name = "镜像与潜行"
Hotkey = "Q"
Researchhotkey = "Q"
Buttonpos_1 = 0
Buttonpos_2 = 2
Researchbuttonpos_1 = 0
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
DataA = {1, 2, 2}
DataB = {0.50, 0.75, 1.00}
DataC = {2.00, 1.50, 1.00}
DataD = {0.30, 0.30, 0.30}
Dur = {60.0, 60.0, 60.0}
HeroDur = {60.0, 60.0, 60.0}
Cost = {100, 100, 100}
Cool = {25.0, 22.0, 18.0}
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNMirrorImage.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNMirrorImage.blp"
Tip = "镜像与潜行(|cffffcc00Q|r) - [|cffffcc00等级 1|r]","镜像与潜行(|cffffcc00Q|r) - [|cffffcc00等级 2|r]","镜像与潜行(|cffffcc00Q|r) - [|cffffcc00等级 3|r]"
Ubertip = "制造镜像迷惑敌人，并在分身后本体自动进入隐匿潜行状态（获得移速加成），攻击或施法将打破潜行，破隐一击附带背刺额外伤害。|n|n等级 1：制造1个镜像，造成50%伤害，承受200%伤害。破隐一击+60伤害。持续60秒。","制造镜像迷惑敌人，并在分身后本体自动进入隐匿潜行状态（获得移速加成），攻击或施法将打破潜行，破隐一击附带背刺额外伤害。|n|n等级 2：制造2个镜像，造成75%伤害，承受150%伤害。破隐一击+100伤害。持续60秒。","制造镜像迷惑敌人，并在分身后本体自动进入隐匿潜行状态（获得移速加成），攻击或施法将打破潜行，破隐一击附带背刺额外伤害。|n|n等级 3：制造2个镜像，造成100%伤害，承受100%防御/血量。破隐一击+150伤害。持续60秒。"
Researchtip = "学习 镜像与潜行(|cffffcc00Q|r)"
Researchubertip = "制造与本体战力相同的幻象，并在分裂完成后使本体潜入暗影，攻击附带破隐背刺爆发。"

[A002]
_parent = "ANcl"
Name = "幻梦奴役"
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDarkSummoning.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNDarkSummoning.blp"
DataA = {0.0, 0.0, 0.0}
DataB = {1, 1, 1}
DataC = {1, 1, 1}
DataD = {0.0, 0.0, 0.0}
DataE = {1, 1, 1}
DataF = "charm,charm,charm"
Order = "charm"
Rng = {600.0, 650.0, 700.0}
Cost = {100, 125, 150}
Cool = {45.0, 40.0, 35.0}
targs = "air,ground,enemy,neutral,organic,mechanical,structure,invulnerable,vulnerable"
Tip = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 1|r]","幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 2|r]","幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 3|r]"
Ubertip = "侵入目标心智，暂时夺取任何敌军、野怪甚至敌方建筑的操控权。时间到期后操控权归还。若受控英雄阵亡，所有权将在死亡瞬间归还原始玩家，防止祭坛异常复活。|n|n等级 1：控制持续30秒。","侵入目标心智，暂时夺取任何敌军、野怪甚至敌方建筑的操控权。时间到期后操控权归还。若受控英雄阵亡，所有权将在死亡瞬间归还原始玩家，防止祭坛异常复活。|n|n等级 2：控制持续2分钟。","侵入目标心智，暂时夺取任何敌军、野怪甚至敌方建筑的操控权。时间到期后操控权归还。若受控英雄阵亡，所有权将在死亡瞬间归还原始玩家，防止祭坛异常复活。|n|n等级 3：控制持续10分钟。"
Researchtip = "学习 幻梦奴役(|cffffcc00W|r)"
Researchubertip = "侵入目标心智，暂时夺取任何敌军、野怪甚至建筑的操控权。"

[A003]
_parent = "ANcl"
Name = "万象皆虚"
Hotkey = "E"
Researchhotkey = "E"
Buttonpos_1 = 2
Buttonpos_2 = 2
Researchbuttonpos_1 = 2
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDisruption.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNDisruption.blp"
DataA = {0.0, 0.0, 0.0}
DataB = {2, 2, 2}
DataC = {3, 3, 3}
DataD = {0.0, 0.0, 0.0}
DataE = {1, 1, 1}
DataF = "blizzard,blizzard,blizzard"
Order = "blizzard"
Area = {250.0, 350.0, 450.0}
Rng = {700.0, 750.0, 800.0}
Cost = {120, 140, 160}
Cool = {40.0, 35.0, 30.0}
targs = "air,ground"
Tip = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 1|r]","万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 2|r]","万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 3|r]"
Ubertip = "复制选定范围内的所有单位生成真实幻象（拥有全套主动技能与装备），持续15分钟。幻象消灭敌人正常提供经验，且移除英雄经验判定，绝不分薄本体经验！|n|n等级 1：作用范围250码，冷却40秒。","复制选定范围内的所有单位生成真实幻象（拥有全套主动技能与装备），持续15分钟。幻象消灭敌人正常提供经验，且移除英雄经验判定，绝不分薄本体经验！|n|n等级 2：作用范围350码，冷却35秒。","复制选定范围内的所有单位生成真实幻象（拥有全套主动技能与装备），持续15分钟。幻象消灭敌人正常提供经验，且移除英雄经验判定，绝不分薄本体经验！|n|n等级 3：作用范围450码，冷却30秒。"
Researchtip = "学习 万象皆虚(|cffffcc00E|r)"
Researchubertip = "大范围复制所有单位真实幻象，可使用技能物品且绝不抢夺本体经验。"

[A004]
_parent = "Aamk"
Name = "幻界主宰"
Hotkey = "R"
Researchhotkey = "R"
Buttonpos_1 = 3
Buttonpos_2 = 2
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
levels = 1
hero = 1
reqLevel = 6
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNArcaniteArchitecture.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNArcaniteArchitecture.blp"
Tip = "幻界主宰(|cffffcc00R|r)"
Ubertip = "【神杖级终极机制升华】领悟幻术终极奥义，使前三个基础技能全面产生机制质变：|n|n·【镜像与潜行】：潜行期间移速提升至极限522，破隐一击伤害提升至250点并附带眩晕，镜像持续时间与承伤全面优化。|n·【幻梦奴役】：三级奴役变为【永久掌控】，技能冷却时间缩短至25秒。|n·【万象皆虚】：复制范围大幅扩充+100码（Lv3达550码），所有幻象获得+30%攻速与+20%额外伤害！"
Researchtip = "学习 幻界主宰(|cffffcc00R|r)"
Researchubertip = "终极被动神杖机制，全面升华前三个小技能！"

[A00V]
_parent = "Aivs"
Name = "隐匿潜行辅助"
Cost = 0
Cool = 0.0
Cast = 0.0
Rng = 99999.0
DataA = 0.0
Dur = 40.0
HeroDur = 40.0
BuffID = "Binv"
targs = "air,ground,friend,self,organic,neutral,vuln,invu"
"""

ini_unit = """[H002]
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

[u000]
_parent = "ewsp"
Name = "Dummy Caster"
modelpath = ""
Art = ""
abilList = "Aloc,Avul"
collision = 0.0
sight = 0
nsight = 0
movementType = ""
spd = 0
HP = 1000
manaN = 10000
mana0 = 10000
regenMana = 100.0

[halt]
_parent = "halt"
Trains = "Hamg,Hmkg,Hpal,Hblm,H002"

[oalt]
_parent = "oalt"
Trains = "Obla,Ofar,Otch,Oshd,H002"

[uaod]
_parent = "uaod"
Trains = "Udea,Ulic,Udre,Ucrl,H002"

[eate]
_parent = "eate"
Trains = "Edem,Ekee,Emoo,Ewar,H002"
"""

with open("factory_tpl/table/ability.ini", "w", encoding="utf-8") as f:
    f.write(ini_ability)

with open("factory_tpl/table/unit.ini", "w", encoding="utf-8") as f:
    f.write(ini_unit)

res = subprocess.run(["tools/w3x2lni/w2l.exe", "obj", "factory_tpl", "hero_obj_v3.w3x"], capture_output=True, text=True)
print("w2l obj return code:", res.returncode)
if res.returncode != 0:
    print("w2l error:", res.stderr, res.stdout)
else:
    print("w2l success!")
    # extract slk/raw to get war3map.w3a and war3map.w3u
    res2 = subprocess.run(["tools/w3x2lni/w2l.exe", "slk", "hero_obj_v3.w3x", "hero_obj_v3_raw"], capture_output=True, text=True)
    print("w2l slk return code:", res2.returncode)
