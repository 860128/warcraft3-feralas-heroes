import os, subprocess, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTORY_TPL = os.path.join(ROOT, "factory_tpl")
PAYLOAD_DIR = os.path.join(ROOT, "payload")
TOOLS_DIR = os.path.join(ROOT, "tools")
HERO_OBJ_V3 = os.path.join(ROOT, "hero_obj_v3.w3x")
EXTRACT_DIR = os.path.join(ROOT, "hero_obj_v3_extract")

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
DataA = {1 = 1, 2 = 2, 3 = 2}
DataB = {1 = 0.50, 2 = 0.75, 3 = 1.00}
DataC = {1 = 2.00, 2 = 1.50, 3 = 1.00}
DataD = {1 = 0.30, 2 = 0.30, 3 = 0.30}
Dur = {1 = 60.0, 2 = 60.0, 3 = 60.0}
HeroDur = {1 = 60.0, 2 = 60.0, 3 = 60.0}
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 25.0, 2 = 22.0, 3 = 18.0}
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNMirrorImage.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNMirrorImage.blp"
Tip = {
1 = "镜像与潜行(|cffffcc00Q|r) - [等级 1]",
2 = "镜像与潜行(|cffffcc00Q|r) - [等级 2]",
3 = "镜像与潜行(|cffffcc00Q|r) - [等级 3]",
}
Ubertip = {
1 = "制造镜像迷惑敌人，并在分身后本体自动进入隐匿潜行状态（获得移速加成），攻击或施法将打破潜行，破隐一击附带背刺额外伤害。|n|n等级 1：制造1个镜像，造成50%伤害，承受200%伤害。破隐一击+60伤害。持续60秒。",
2 = "制造镜像迷惑敌人，并在分身后本体自动进入隐匿潜行状态（获得移速加成），攻击或施法将打破潜行，破隐一击附带背刺额外伤害。|n|n等级 2：制造2个镜像，造成75%伤害，承受150%伤害。破隐一击+100伤害。持续60秒。",
3 = "制造镜像迷惑敌人，并在分身后本体自动进入隐匿潜行状态（获得移速加成），攻击或施法将打破潜行，破隐一击附带背刺额外伤害。|n|n等级 3：制造2个镜像，造成100%伤害，承受100%防御/血量。破隐一击+150伤害。持续60秒。",
}
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNCharm.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNCharm.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 1, 2 = 1, 3 = 1}
DataF = {1 = "charm", 2 = "charm", 3 = "charm"}
Order = "charm"
Rng = {1 = 600.0, 2 = 650.0, 3 = 700.0}
Cost = {1 = 100, 2 = 125, 3 = 150}
Cool = {1 = 45.0, 2 = 40.0, 3 = 35.0}
targs = "air,ground,enemy,neutral,organic,mechanical,structure,invulnerable,vulnerable"
Tip = {
1 = "幻梦奴役(|cffffcc00W|r) - [等级 1]",
2 = "幻梦奴役(|cffffcc00W|r) - [等级 2]",
3 = "幻梦奴役(|cffffcc00W|r) - [等级 3]",
}
Ubertip = {
1 = "侵入目标心智，暂时夺取任何敌军、野怪甚至敌方建筑的操控权。时间到期后操控权归还。若受控英雄阵亡，所有权将在死亡瞬间归还原始玩家，防止祭坛异常复活。|n|n等级 1：控制持续30秒。",
2 = "侵入目标心智，暂时夺取任何敌军、野怪甚至敌方建筑的操控权。时间到期后操控权归还。若受控英雄阵亡，所有权将在死亡瞬间归还原始玩家，防止祭坛异常复活。|n|n等级 2：控制持续2分钟。",
3 = "侵入目标心智，暂时夺取任何敌军、野怪甚至敌方建筑的操控权。时间到期后操控权归还。若受控英雄阵亡，所有权将在死亡瞬间归还原始玩家，防止祭坛异常复活。|n|n等级 3：控制持续10分钟。",
}
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNWand.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNWand.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 2, 2 = 2, 3 = 2}
DataC = {1 = 3, 2 = 3, 3 = 3}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 1, 2 = 1, 3 = 1}
DataF = {1 = "blizzard", 2 = "blizzard", 3 = "blizzard"}
Order = "blizzard"
Area = {1 = 250.0, 2 = 350.0, 3 = 450.0}
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cost = {1 = 120, 2 = 140, 3 = 160}
Cool = {1 = 40.0, 2 = 35.0, 3 = 30.0}
targs = "air,ground"
Tip = {
1 = "万象皆虚(|cffffcc00E|r) - [等级 1]",
2 = "万象皆虚(|cffffcc00E|r) - [等级 2]",
3 = "万象皆虚(|cffffcc00E|r) - [等级 3]",
}
Ubertip = {
1 = "复制选定范围内的所有单位（含农民、小精灵、野怪与英雄）生成100%战力的幻影，持续15分钟。英雄幻影不占左侧图标、阵亡不进祭坛、绝不分薄本体经验！|n|n等级 1：作用范围250码，冷却40秒。",
2 = "复制选定范围内的所有单位（含农民、小精灵、野怪与英雄）生成100%战力的幻影，持续15分钟。英雄幻影不占左侧图标、阵亡不进祭坛、绝不分薄本体经验！|n|n等级 2：作用范围350码，冷却35秒。",
3 = "复制选定范围内的所有单位（含农民、小精灵、野怪与英雄）生成100%战力的幻影，持续15分钟。英雄幻影不占左侧图标、阵亡不进祭坛、绝不分薄本体经验！|n|n等级 3：作用范围450码，冷却30秒。",
}
Researchtip = "学习 万象皆虚(|cffffcc00E|r)"
Researchubertip = "大范围复制所有单位与英雄幻影，持续15分钟，不占左侧英雄栏、不进祭坛、不抢夺本体经验。"

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
DataA = 10
DataB = 10
DataC = 10
DataD = 0
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNBrilliance.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNScepterOfMastery.blp"
Tip = "幻界主宰(|cffffcc00R|r)"
Ubertip = "【神杖级终极机制升华】全属性+10，并使前三个基础技能全面产生机制质变：|n|n·【镜像与潜行】：潜行期间移速提升至极限522，破隐一击伤害提升至250点。|n·【幻梦奴役】：三级奴役变为【永久掌控】。|n·【万象皆虚】：复制范围大幅扩充+100码（Lv3达550码），英雄幻影攻击力提升至130%、承伤降低至80%！"
Researchtip = "学习 幻界主宰(|cffffcc00R|r)"
Researchubertip = "终极被动神杖机制，全属性+10并全面升华前三个小技能！"

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

[A00I]
_parent = "AIil"
Name = "万象幻影辅助"
item = 0
hero = 0
levels = 1
checkDep = 0
Cost = 0
Cool = 0.0
Cast = 0.0
Rng = 99999.0
Area = 0.0
DataA = 1.00
DataB = 1.00
Dur = 900.0
HeroDur = 900.0
BuffID = "BIil"
targs = "air,ground,friend,enemy,self,neutral,vuln,invu,organic"

[A00J]
_parent = "AIil"
Name = "万象幻影神杖辅助"
item = 0
hero = 0
levels = 1
checkDep = 0
Cost = 0
Cool = 0.0
Cast = 0.0
Rng = 99999.0
Area = 0.0
DataA = 1.30
DataB = 0.80
Dur = 900.0
HeroDur = 900.0
BuffID = "BIil"
targs = "air,ground,friend,enemy,self,neutral,vuln,invu,organic"

[A011]
_parent = "AEev"
Name = "魔音同化"
Hotkey = "Q"
Researchhotkey = "Q"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNHeroWarden.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNHeroWarden.blp"
Buttonpos_1 = 0
Buttonpos_2 = 2
Researchbuttonpos_1 = 0
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
DataA = {1 = 0.15, 2 = 0.25, 3 = 0.35}
Researchtip = "学习 魔音同化(|cffffcc00Q|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "被动：获得闪避，且魔音忍者（含分身）每次击杀非建筑单位都会在原地生成一个完全相同的伪英雄分身（不抢经验、不进祭坛）。|n|cffffcc00无相真身：|r当本体受到致命伤害或阵亡时，若场上仍存有魔音忍者分身，本体不会死亡，而是随机转移至其中一个分身继续存活！"
Tip = {
1 = "魔音同化 - [|cffffcc00等级 1|r]",
2 = "魔音同化 - [|cffffcc00等级 2|r]",
3 = "魔音同化 - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "获得15%闪避。击杀任何单位会同化生成一个持续120秒的魔音忍者伪英雄分身。本体受死时会自动移魂至场上的分身，唯有杀尽场上所有魔音忍者才能将其真正击杀。",
2 = "获得25%闪避。击杀任何单位会同化生成一个持续240秒的魔音忍者伪英雄分身。本体受死时会自动移魂至场上的分身，并恢复30%生命值。",
3 = "获得35%闪避。击杀任何单位会同化生成一个持续600秒的魔音忍者伪英雄分身。本体受死时会自动移魂至场上的分身，并恢复50%生命值。",
}

[A012]
_parent = "ANcl"
Name = "竭心光环"
Hotkey = "W"
Researchhotkey = "W"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNUnholyAura.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNUnholyAura.blp"
Buttonpos_1 = 1
Buttonpos_2 = 2
Researchbuttonpos_1 = 1
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Cost = {1 = 0, 2 = 0, 3 = 0}
Cool = {1 = 1.0, 2 = 1.0, 3 = 1.0}
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "roar", 2 = "roar", 3 = "roar"}
Order = "roar"
Researchtip = "学习 竭心光环(|cffffcc00W|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "可开关光环：开启后，地图上所有敌方非建筑单位每秒流失1%/2%/3%最大生命值。学习后默认开启，点击可随时开关。"
Tip = {
1 = "竭心光环(开关)(|cffffcc00W|r) - [|cffffcc00等级 1|r]",
2 = "竭心光环(开关)(|cffffcc00W|r) - [|cffffcc00等级 2|r]",
3 = "竭心光环(开关)(|cffffcc00W|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "点击切换光环开关（默认开启）。开启时，全图所有敌方非建筑单位每秒流失 |cffffcc001%|r 最大生命值。",
2 = "点击切换光环开关（默认开启）。开启时，全图所有敌方非建筑单位每秒流失 |cffffcc002%|r 最大生命值。",
3 = "点击切换光环开关（默认开启）。开启时，全图所有敌方非建筑单位每秒流失 |cffffcc003%|r 最大生命值。",
}

[A013]
_parent = "AOcr"
Name = "他化自在"
Hotkey = "E"
Researchhotkey = "E"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNPossession.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNPossession.blp"
Buttonpos_1 = 2
Buttonpos_2 = 2
Researchbuttonpos_1 = 2
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
DataA = {1 = 15.0, 2 = 25.0, 3 = 35.0}
DataB = {1 = 2.0, 2 = 2.0, 3 = 2.5}
Researchtip = "学习 他化自在(|cffffcc00E|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "被动：任何击杀了魔音忍者（含分身）的敌方单位都会被种下【他化自在】因果印记；当该凶手死亡时，会直接转化为一个新的魔音忍者分身！同时被动提升暴击率。"
Tip = {
1 = "他化自在 - [|cffffcc00等级 1|r]",
2 = "他化自在 - [|cffffcc00等级 2|r]",
3 = "他化自在 - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "获得15%几率2倍暴击。任何击杀魔音忍者（或分身）的敌方单位将被种下印记，该单位死后会转化为1个新的魔音忍者伪英雄分身。",
2 = "获得25%几率2倍暴击。任何击杀魔音忍者（或分身）的敌方单位将被种下印记（每秒额外流失1%生命），死后转化为1个新的魔音忍者伪英雄分身。",
3 = "获得35%几率2.5倍暴击。任何击杀魔音忍者（或分身）的敌方单位将被种下印记（每秒额外流失2%生命），死后直接转化为2个新的魔音忍者伪英雄分身！",
}

[A014]
_parent = "ANcl"
Name = "独断万古"
Hotkey = "R"
Researchhotkey = "R"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNSpiritOfVengeance.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNSpiritOfVengeance.blp"
Buttonpos_1 = 3
Buttonpos_2 = 2
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
levels = 1
hero = 1
reqLevel = 6
Cost = 120
Cool = 60.0
DataA = 0.0
DataB = 0
DataC = 1
DataE = 0
DataF = "summongrizzly"
Order = "summongrizzly"
Researchtip = "学习 独断万古(|cffffcc00R|r)"
Researchubertip = "终极技能：召唤一尊【独断万古·魔音神尊】（魔音忍者的终极强化形态，拥有3000生命、混沌攻击、暴击、闪避、分裂与魔法免疫），持续180秒。神尊击杀敌人同样会生成魔音忍者分身，且可作为不死替身！"
Tip = "独断万古(|cffffcc00R|r)"
Ubertip = "召唤【独断万古·魔音神尊】降临战场，持续180秒。|n|cffffcc00属性：|r3000生命值、160+混沌攻击、神圣护甲、魔法免疫、分裂攻击、暴击与闪避。|n|cffffcc00特性：|r神尊击杀任何单位同样会转化出魔音忍者分身，且在本体受死时可代死移魂！"

[A015]
_parent = "ACev"
Name = "魔音闪避"
levels = 3
DataA = {1 = 0.15, 2 = 0.25, 3 = 0.35}

[A016]
_parent = "ACev"
Name = "神尊闪避"
levels = 1
DataA = 0.35
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
bpx = 0
bpy = 2
Buttonpos_1 = 0
Buttonpos_2 = 2
fused = 5
goldcost = 425
lumbercost = 100
bldtm = 55
heroAbilList = "A001,A002,A003,A004"
abilList = "AInv"
requirescount = 0
requires1 = ""
requires2 = ""

[H003]
_parent = "Ewar"
Name = "魔音忍者"
Propernames = "魔音之影,无相忍尊,天魔琴师"
Tip = "召唤 魔音忍者(|cffffcc00M|r)"
Ubertip = "诡谲无相的暗影刺客。没有固定本体，击杀任何单位都会将其同化为自己的伪英雄分身；本体受死时只要场上仍有分身便可移魂转生。|n|n|cffffcc00技能：|r|n- 魔音同化 (Q)|n- 竭心光环 (W)|n- 他化自在 (E)|n- 独断万古 (R)"
Revivetip = "复活 魔音忍者(|cffffcc00M|r)"
Awakentip = "唤醒 魔音忍者(|cffffcc00M|r)"
Hotkey = "M"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNHeroWarden.blp"
file = "units\\\\nightelf\\\\herowarden\\\\herowarden"
"file:hd" = "units\\\\nightelf\\\\herowarden\\\\herowarden"
"file:sd" = "units\\\\nightelf\\\\herowarden\\\\herowarden"
unitSound = "HeroWarden"
Primary = "AGI"
primary = "AGI"
STR = 20
AGI = 26
INT = 18
STRplus = 2.20
AGIplus = 3.20
INTplus = 1.80
spd = 320
dmgplus1 = 28
cool1 = 1.50
bpx = 1
bpy = 2
Buttonpos_1 = 1
Buttonpos_2 = 2
fused = 5
goldcost = 425
lumbercost = 100
bldtm = 55
heroAbilList = "A011,A012,A013,A014"
abilList = "AInv"
requirescount = 0
requires1 = ""
requires2 = ""

[u000]
_parent = "ewsp"
Name = "Dummy Caster"
file = ""
"file:hd" = ""
"file:sd" = ""
Art = ""
Specialart = ""
unitSound = ""
Builds = ""
upgrades = ""
type = ""
fused = 0
fmade = 0
castbsw = 0.0
castpt = 0.0
abilList = "Aloc,Avul"
collision = 0.0
sight = 0
nsight = 0
movetp = "fly"
spd = 522
turnRate = 3.0
HP = 1000
manaN = 10000
mana0 = 10000
regenMana = 100.0
hideOnMinimap = 1

[u001]
_parent = "nbal"
Name = "独断万古·魔音神尊"
file = "units\\\\nightelf\\\\herowarden\\\\herowarden.mdl"
"file:hd" = "units\\\\nightelf\\\\herowarden\\\\herowarden.mdl"
"file:sd" = "units\\\\nightelf\\\\herowarden\\\\herowarden.mdl"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNSpiritOfVengeance.blp"
unitSound = "HeroWarden"
modelScale = 1.65
red = 180
green = 100
blue = 255
HP = 3000
regenHP = 25.0
def = 15.0
defType = "divine"
spd = 400
atkType1 = "chaos"
dmgplus1 = 160
dice1 = 2
sides1 = 15
cool1 = 1.10
rangeN1 = 150
weapTp1 = "normal"
abilList = "ACct,A016,ACce,Amim"
fused = 0
foodCost = 0
level = 10

[u002]
_parent = "ogru"
Name = "魔音忍者"
file = "units\\\\nightelf\\\\herowarden\\\\herowarden.mdl"
"file:hd" = "units\\\\nightelf\\\\herowarden\\\\herowarden.mdl"
"file:sd" = "units\\\\nightelf\\\\herowarden\\\\herowarden.mdl"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNHeroWarden.blp"
unitSound = "HeroWarden"
modelScale = 1.0
HP = 850
regenHP = 5.0
def = 6.0
defType = "hero"
spd = 320
atkType1 = "hero"
weapTp1 = "normal"
dmgplus1 = 52
dice1 = 2
sides1 = 8
cool1 = 1.4
rangeN1 = 128
abilList = "ACct,AInv"
foodCost = 0
level = 5

[halt]
_parent = "halt"
Trains = "Hamg,Hmkg,Hpal,Hblm,H002,H003"

[oalt]
_parent = "oalt"
Trains = "Obla,Ofar,Otch,Oshd,H002,H003"

[uaod]
_parent = "uaod"
Trains = "Udea,Ulic,Udre,Ucrl,H002,H003"

[eate]
_parent = "eate"
Trains = "Edem,Ekee,Emoo,Ewar,H002,H003"
"""

# 1. Write ini files to factory_tpl/table
ability_ini_path = os.path.join(FACTORY_TPL, "table", "ability.ini")
unit_ini_path = os.path.join(FACTORY_TPL, "table", "unit.ini")

with open(ability_ini_path, "w", encoding="utf-8") as f:
    f.write(ini_ability)
print("Updated:", ability_ini_path)

with open(unit_ini_path, "w", encoding="utf-8") as f:
    f.write(ini_unit)
print("Updated:", unit_ini_path)

# 2. Run w3x2lni to compile hero_obj_v3.w3x
w2l = os.path.join(TOOLS_DIR, "w3x2lni", "w2l.exe")
if os.path.exists(HERO_OBJ_V3):
    os.remove(HERO_OBJ_V3)

p = subprocess.run([w2l, 'obj', FACTORY_TPL, HERO_OBJ_V3, '-s'], cwd=os.path.dirname(w2l), capture_output=True)
print("w2l obj RC:", p.returncode)
print("w2l obj STDOUT:", p.stdout.decode('utf-8', 'replace'))
print("w2l obj STDERR:", p.stderr.decode('utf-8', 'replace'))
print("hero_obj_v3.w3x Exists:", os.path.exists(HERO_OBJ_V3), os.path.getsize(HERO_OBJ_V3) if os.path.exists(HERO_OBJ_V3) else 0)
if p.returncode != 0:
    raise RuntimeError("w2l obj failed!")

# 3. Extract war3map.w3u and war3map.w3a from hero_obj_v3.w3x using 32-bit powershell and mpq_extract_all.ps1
ps_exe = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
if not os.path.exists(ps_exe):
    ps_exe = "powershell.exe"

mpq_script = os.path.join(TOOLS_DIR, "mpq_extract_all.ps1")
p_extract = subprocess.run([ps_exe, "-ExecutionPolicy", "Bypass", "-File", mpq_script, HERO_OBJ_V3, EXTRACT_DIR], capture_output=True)
print("Extract RC:", p_extract.returncode)
if p_extract.returncode != 0:
    print("Extract STDERR:", p_extract.stderr.decode('gbk', 'replace'))
    raise RuntimeError("MPQ extraction failed!")

# 4. Copy war3map.w3u and war3map.w3a into payload/
os.makedirs(PAYLOAD_DIR, exist_ok=True)
for fn in ["war3map.w3u", "war3map.w3a"]:
    src_file = os.path.join(EXTRACT_DIR, fn)
    dst_file = os.path.join(PAYLOAD_DIR, fn)
    shutil.copyfile(src_file, dst_file)
    print(f"Copied {src_file} -> {dst_file} (Size: {os.path.getsize(dst_file)} bytes)")

# 5. Verification
print("\n--- Verifying compiled payload files ---")
with open(os.path.join(PAYLOAD_DIR, "war3map.w3u"), "rb") as f:
    w3u_data = f.read()
for sym in [b'H002', b'H003', b'u000', b'u001', b'u002', b'halt', b'oalt', b'uaod', b'eate']:
    print(f"w3u contains {sym.decode('ascii')}: {sym in w3u_data}")

with open(os.path.join(PAYLOAD_DIR, "war3map.w3a"), "rb") as f:
    w3a_data = f.read()
for sym in [b'A001', b'A002', b'A003', b'A004', b'A00V', b'A011', b'A012', b'A013', b'A014', b'A015', b'A016']:
    print(f"w3a contains {sym.decode('ascii')}: {sym in w3a_data}")
