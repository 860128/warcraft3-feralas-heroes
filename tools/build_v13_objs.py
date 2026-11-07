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
Researchubertip = "被动：获得闪避，且魔音忍者（含分身）每次击杀非建筑单位（分身除外）都会在原地生成一个完全相同的伪英雄分身（上限3/5/7个，不抢经验、不进祭坛）。|n|cffffcc00无相真身：|r当本体受到致命伤害或阵亡时，若场上仍存有分身，本体不会死亡，而是转移至分身继续存活！"
Tip = {
1 = "魔音同化 - [|cffffcc00等级 1|r]",
2 = "魔音同化 - [|cffffcc00等级 2|r]",
3 = "魔音同化 - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "获得15%闪避。击杀任何非分身单位会同化生成一个持续120秒的分身（同化上限3个）。本体受死时会自动移魂至场上的分身，唯有杀尽所有魔音实体才能将其击杀。",
2 = "获得25%闪避。击杀任何非分身单位会同化生成一个持续240秒的分身（同化上限5个）。本体受死时会自动移魂至场上的分身，并恢复30%生命值。",
3 = "获得35%闪避。击杀任何非分身单位会同化生成一个持续600秒的分身（同化上限7个）。本体受死时会自动移魂至场上的分身，并恢复50%生命值。",
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
Researchubertip = "可开关光环：开启后，周围900码范围内所有敌方非建筑单位每秒流失1%/2%/3%最大生命值（最低保留1点生命，无法直接致死）。学习后默认开启，点击可随时开关。"
Tip = {
1 = "竭心光环(开关)(|cffffcc00W|r) - [|cffffcc00等级 1|r]",
2 = "竭心光环(开关)(|cffffcc00W|r) - [|cffffcc00等级 2|r]",
3 = "竭心光环(开关)(|cffffcc00W|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "点击切换光环开关（默认开启）。开启时，周围900码范围内所有敌方非建筑单位每秒流失 |cffffcc001%|r 最大生命值（最低保留1点生命，无法直接致死）。",
2 = "点击切换光环开关（默认开启）。开启时，周围900码范围内所有敌方非建筑单位每秒流失 |cffffcc002%|r 最大生命值（最低保留1点生命，无法直接致死）。",
3 = "点击切换光环开关（默认开启）。开启时，周围900码范围内所有敌方非建筑单位每秒流失 |cffffcc003%|r 最大生命值（最低保留1点生命，无法直接致死）。",
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
Ubertip = "召唤【独断万古·魔音神尊】降临战场，持续180秒。|n|cffffcc00属性：|r3000生命值、160+混沌攻击、英雄护甲、魔法免疫、分裂攻击、暴击与闪避。|n|cffffcc00特性：|r神尊击杀任何单位同样会转化出魔音忍者分身，且在本体受死时可代死移魂！"

[A015]
_parent = "ACev"
Name = "魔音闪避"
hero = 0
levels = 3
DataA = {1 = 0.15, 2 = 0.25, 3 = 0.35}
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNEvasion.blp"
Tip = {
1 = "魔音闪避",
2 = "魔音闪避",
3 = "魔音闪避",
}
Ubertip = {
1 = "有15%的几率闪避敌方的攻击。",
2 = "有25%的几率闪避敌方的攻击。",
3 = "有35%的几率闪避敌方的攻击。",
}
Buttonpos_1 = 2
Buttonpos_2 = 2

[A016]
_parent = "ACev"
Name = "神尊闪避"
hero = 0
levels = 1
DataA = 0.35
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNEvasion.blp"
Tip = "神尊闪避"
Ubertip = "有35%的几率闪避敌方的攻击。"
Buttonpos_1 = 2
Buttonpos_2 = 2

[A017]
_parent = "AOcr"
Name = "致命一击"
hero = 0
levels = 1
DataA = 25.0
DataB = 2.0
DataC = 0.0
DataD = 0.0
DataE = 0
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNCriticalStrike.blp"
Tip = "致命一击"
Ubertip = "给予25%的几率造成2倍伤害。"
Buttonpos_1 = 3
Buttonpos_2 = 1

[A021]
_parent = "ANcl"
Name = "渊潜掠影"
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
Cost = {1 = 50, 2 = 50, 3 = 50}
Cool = {1 = 12.0, 2 = 10.0, 3 = 8.0}
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNCryptFiendBurrow.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNCryptFiendBurrow.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "windwalk", 2 = "windwalk", 3 = "windwalk"}
Order = "windwalk"
Researchtip = "学习 渊潜掠影(|cffffcc00Q|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "遁入地底进入绝对隐匿状态，持续20/25/30秒（再次点击可提前破土而出）。|n|cffffcc00遁地效果：|r移速拉满至522极限，无视单位碰撞，仅在真视视野下可见。|n|cffffcc00破土突袭：|r钻出地面瞬间对周围250码敌军造成0.75秒击飞与高额突袭伤害！"
Tip = {
1 = "渊潜掠影(|cffffcc00Q|r) - [|cffffcc00等级 1|r]",
2 = "渊潜掠影(|cffffcc00Q|r) - [|cffffcc00等级 2|r]",
3 = "渊潜掠影(|cffffcc00Q|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "遁入地底进入绝对隐匿状态，持续20秒（遁地中再次施放可提前破土而出）。|n|cffffcc00遁地效果：|r移速提升至522极限，无视单位碰撞，仅在真视视野下可见。|n|cffffcc00破土突袭：|r破土瞬间对周围250码敌军造成0.75秒击飞，并造成90(+1.5x敏捷)点突袭物理伤害。",
2 = "遁入地底进入绝对隐匿状态，持续25秒（遁地中再次施放可提前破土而出）。|n|cffffcc00遁地效果：|r移速提升至522极限，无视单位碰撞，仅在真视视野下可见。|n|cffffcc00破土突袭：|r破土瞬间对周围250码敌军造成0.75秒击飞，并造成150(+1.5x敏捷)点突袭物理伤害。",
3 = "遁入地底进入绝对隐匿状态，持续30秒（遁地中再次施放可提前破土而出）。|n|cffffcc00遁地效果：|r移速提升至522极限，无视单位碰撞，仅在真视视野下可见。|n|cffffcc00破土突袭：|r破土瞬间对周围250码敌军造成0.75秒击飞，并造成210(+1.5x敏捷)点突袭物理伤害。",
}

[A022]
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
Researchubertip = "撕裂并吞噬生命值低于35%的非魔免单位（敌方英雄需低于28%），或当前生命低于自身最大生命10%的单位（无视生命比例直接满血生吞）！|n吞噬后进入消化期，消化完成后恢复25%生命与法力，并根据猎物类型获得永久属性进化（小兵属性收益随技能等级提升：Lv1=1.0倍 / Lv2=1.25倍 / Lv3=1.5倍）：|n- |cff00ff80近战小兵|r：永久增加最大生命值|n- |cffff6600远程小兵(无魔法)|r：永久增加基础攻击力|n- |cff33ccff魔法单位(有魔法)|r：永久增加最大法力值|n- |cffffcc00敌方英雄(顶端掠食)|r：逐级蚕食其敏捷/力量/智力/血蓝并等额镜像归己，任选其技能掠夺！|n- |cffffcc00真实技能掠夺|r：扫描猎物携带技能基因（可升至3阶）；无技能白板猎物仅提供肉体属性！"
Tip = {
1 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 1|r]",
2 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 2|r]",
3 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "撕裂并吞噬射程250码内生命值低于35%的非魔免单位（敌方英雄需低于28%），或当前生命低于自身最大生命10%的单位（无视生命比例直接满血生吞）！|n吞噬后进入6.5秒消化期，消化完成后恢复25%生命/法力，解锁受害者的【拟态伪装】，并按1.0倍基础收益永久进化属性：|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值（基础+30，每级+10）|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值（基础+25，每级+5）|n- |cffffcc00吞噬敌方英雄|r：4点逐级抽敏/力/智/血蓝并等额镜像归己，任选其技能掠夺！|n- |cffffcc00生吞法则：|r若目标当前生命值低于自身最大生命的10%，可无视其生命比例直接满血生吞！|n|n|cffffcc00冷却时间：20秒|r",
2 = "撕裂并吞噬射程275码内生命值低于35%的非魔免单位（敌方英雄需低于28%），或当前生命低于自身最大生命10%的单位（无视生命比例直接满血生吞）！|n吞噬后进入5.0秒消化期，消化完成后恢复25%生命/法力，解锁受害者的【拟态伪装】，并按1.25倍强化收益永久进化属性：|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值（1.25倍系数）|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加基础攻击力（1.25倍系数）|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值（1.25倍系数）|n- |cffffcc00吞噬敌方英雄|r：4点逐级抽敏/力/智/血蓝并等额镜像归己，任选其技能掠夺！|n- |cffffcc00生吞法则：|r若目标当前生命值低于自身最大生命的10%，可无视其生命比例直接满血生吞！|n|n|cffffcc00冷却时间：15秒|r",
3 = "撕裂并吞噬射程300码内生命值低于35%的非魔免单位（敌方英雄需低于28%），或当前生命低于自身最大生命10%的单位（无视生命比例直接满血生吞）！|n吞噬后进入3.5秒消化期，消化完成后恢复25%生命/法力，解锁受害者的【拟态伪装】，并按1.50倍极限收益永久进化属性：|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值（1.50倍系数）|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加基础攻击力（1.50倍系数）|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值（1.50倍系数）|n- |cffffcc00吞噬敌方英雄|r：4点逐级抽敏/力/智/血蓝并等额镜像归己，任选其技能掠夺！|n- |cffffcc00生吞法则：|r若目标当前生命值低于自身最大生命的10%，可无视其生命比例直接满血生吞！|n|n|cffffcc00冷却时间：10秒|r",
}

[A023]
_parent = "ANcl"
Name = "拟态伪装"
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
Cost = {1 = 0, 2 = 0, 3 = 0}
Cool = {1 = 2.0, 2 = 2.0, 3 = 2.0}
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNPolymorph.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNPolymorph.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "ambush", 2 = "ambush", 3 = "ambush"}
Order = "ambush"
Researchtip = "学习 拟态伪装(|cffffcc00E|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "消化猎物后，点击可拟态伪装为受害者的模型与阵营颜色！|n|cffffcc00间谍效果：|r外表与阵营颜色完全同步为受害者，野怪将视你为中立生物不主动攻击。|n|cffffcc00破隐暴击：|r发动普攻、施放伤害技能或被真视照射时伪装碎裂，破隐第一击造成150%/175%/200%暴击伤害！"
Tip = {
1 = "拟态伪装(|cffffcc00E|r) - [|cffffcc00等级 1|r]",
2 = "拟态伪装(|cffffcc00E|r) - [|cffffcc00等级 2|r]",
3 = "拟态伪装(|cffffcc00E|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "点击拟态伪装为最近消化的猎物模型与阵营颜色（再次点击或攻击/施法解除）。|n|cffffcc00间谍特性：|r野怪视你为中立生物不主动攻击。|n|cffffcc00破隐暴击：|r解除伪装的第一击造成150%伤害暴击。",
2 = "点击拟态伪装为最近消化的猎物模型与阵营颜色（再次点击或攻击/施法解除）。|n|cffffcc00间谍特性：|r野怪视你为中立生物不主动攻击。|n|cffffcc00破隐暴击：|r解除伪装的第一击造成175%伤害暴击。",
3 = "点击拟态伪装为最近消化的猎物模型与阵营颜色（再次点击或攻击/施法解除）。|n|cffffcc00间谍特性：|r野怪视你为中立生物不主动攻击。|n|cffffcc00破隐暴击：|r解除伪装的第一击造成200%伤害暴击。",
}

[A024]
_parent = "ANcl"
Name = "异种进化：基因掠夺"
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
Researchtip = "学习 异种进化：双基因掠夺(|cffffcc00R|r)"
Researchubertip = "点击呼出【异种进化与基因控制台】，实时查看吞噬小兵累计进化的生命、攻击、法力属性，以及管理掠夺的敌方英雄技能！|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值|n- |cffffcc00吞噬敌方英雄(Apex Harvest)|r：永久夺取 4 点敏捷属性，并4选1掠夺其英雄技能；重复吞噬敌方英雄可叠加【基因超载】层数强化技能，释放技能时触发酸液爆发与法力返还！"
Tip = "异种进化：双基因掠夺(|cffffcc00R|r)"
Ubertip = "点击打开【异种进化控制台】：查看当前吞噬累计增加的生命值、基础攻击力与最大法力值，以及保留或遗忘已掠夺的敌方英雄技能。|n- |cff00ff80近战小兵|r：永久提升最大生命值|n- |cffff6600远程小兵(无魔法)|r：永久提升 1~2 点基础攻击力|n- |cff33ccff魔法单位(有魔法)|r：永久提升最大法力值|n- |cffffcc00敌方英雄|r：永久夺取 4 点敏捷属性 + 4选1掠夺技能 + 基因超载强化！"

[A025]
_parent = "AUts"
hero = 0
levels = 3
Name = "异种甲壳进化"
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNThornShield.blp"
Buttonpos_1 = 1
Buttonpos_2 = 1
DataA = {1 = 0.25, 2 = 0.50, 3 = 0.85}
DataB = {1 = 0.75, 2 = 0.50, 3 = 0.15}
DataC = {1 = 5.0, 2 = 10.0, 3 = 18.0}
Tip = {
1 = "异种甲壳进化 - [|cffffcc001阶|r]",
2 = "异质精钢壳 - [|cffffcc002阶|r]",
3 = "异质反射盾 - [|cffffcc003阶终极|r]",
}
Ubertip = {
1 = "受到坚硬甲壳保护，护甲提升5点，并反弹25%近战伤害。",
2 = "甲壳质变为精钢结构，护甲提升10点，并反弹50%近战伤害。",
3 = "基因突变生成终极异质反射盾，护甲提升18点，反弹85%近战伤害并大幅偏斜冲击！",
}

[A026]
_parent = "Aspo"
hero = 0
levels = 3
Name = "异种剧毒进化"
Art = "ReplaceableTextures\\\\PassiveButtons\\\\PASBTNSlowPoison.blp"
Buttonpos_1 = 2
Buttonpos_2 = 1
DataA = {1 = 8.0, 2 = 16.0, 3 = 30.0}
DataB = {1 = 0.50, 2 = 0.60, 3 = 0.70}
DataC = {1 = 0.25, 2 = 0.40, 3 = 0.60}
Dur = {1 = 5.0, 2 = 5.0, 3 = 5.0}
HeroDur = {1 = 1.0, 2 = 2.0, 3 = 3.0}
targs = "air,ground,organic"
Tip = {
1 = "异种剧毒 - [|cffffcc001阶|r]",
2 = "双重剧毒 - [|cffffcc002阶|r]",
3 = "群体扩散剧毒 - [|cffffcc003阶终极|r]",
}
Ubertip = {
1 = "普攻附带神经毒素，每秒造成8点毒性伤害，降低目标50%移速与25%攻速，持续5秒（英雄1秒）。",
2 = "毒素浓度翻倍，每秒造成16点伤害，降低目标60%移速与40%攻速，持续5秒（英雄2秒）。",
3 = "终极异种群体毒素，每秒造成30点剧毒伤害，降低目标70%移速与60%攻速，持续5秒（英雄3秒）！",
}

[A027]
_parent = "Apiv"
hero = 0
levels = 1
Name = "异种潜伏隐匿"
Dur = 0.05
HeroDur = 0.05
DataA = 0
[ACbl]
_parent = "ACbl"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 1
Buttonpos_2 = 1
Cost = {1 = 75, 2 = 75, 3 = 75}
Cool = {1 = 8.0, 2 = 6.0, 3 = 4.0}
DataA = {1 = 0.40, 2 = 0.65, 3 = 0.90}
DataB = {1 = 0.25, 2 = 0.35, 3 = 0.45}
Tip = {
1 = "嗜血术 [一级]",
2 = "嗜血术 [二级]",
3 = "嗜血术 [顶级]",
}
Ubertip = {
1 = "增加目标单位40%的攻击速度和25%的移动速度。",
2 = "增加目标单位65%的攻击速度和35%的移动速度。",
3 = "增加目标单位90%的攻击速度和45%的移动速度。",
}

[ACls]
_parent = "ACls"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 12.0, 2 = 10.0, 3 = 8.0}
DataA = {1 = 20.0, 2 = 35.0, 3 = 55.0}
Tip = {
1 = "闪电护盾 [一级]",
2 = "闪电护盾 [二级]",
3 = "闪电护盾 [顶级]",
}
Ubertip = {
1 = "在目标周围形成电盾，对其周围单位造成每秒20点伤害。",
2 = "在目标周围形成强力电盾，对其周围单位造成每秒35点伤害。",
3 = "在目标周围形成高压电盾，对其周围单位造成每秒55点伤害。",
}

[ACpu]
_parent = "ACpu"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
Cost = {1 = 75, 2 = 75, 3 = 75}
Cool = {1 = 10.0, 2 = 7.0, 3 = 4.0}
DataC = {1 = 400.0, 2 = 650.0, 3 = 950.0}
Tip = {
1 = "净化 [一级]",
2 = "净化 [二级]",
3 = "净化 [顶级]",
}
Ubertip = {
1 = "驱散目标魔法并减速，对召唤物造成400点伤害。冷却10秒。",
2 = "驱散目标魔法并减速，对召唤物造成650点伤害。冷却7秒。",
3 = "驱散目标魔法并减速，对召唤物造成950点伤害。冷却4秒。",
}

[ACct]
_parent = "ACct"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
DataA = {1 = 20.0, 2 = 28.0, 3 = 35.0}
DataB = {1 = 2.0, 2 = 2.5, 3 = 3.0}
Tip = {
1 = "致命一击 [一级]",
2 = "致命一击 [二级]",
3 = "致命一击 [顶级]",
}
Ubertip = {
1 = "给予20%的几率造成2.0倍暴击伤害。",
2 = "给予28%的几率造成2.5倍暴击伤害。",
3 = "给予35%的几率造成3.0倍暴击伤害。",
}

[ACbh]
_parent = "ACbh"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
DataA = {1 = 15.0, 2 = 25.0, 3 = 35.0}
DataC = {1 = 25.0, 2 = 45.0, 3 = 70.0}
Dur = {1 = 1.5, 2 = 2.0, 3 = 2.5}
HeroDur = {1 = 0.5, 2 = 1.0, 3 = 1.5}
Tip = {
1 = "重击 [一级]",
2 = "重击 [二级]",
3 = "重击 [顶级]",
}
Ubertip = {
1 = "攻击时有15%几率附加25点伤害并击晕目标1.5秒（英雄0.5秒）。",
2 = "攻击时有25%几率附加45点伤害并击晕目标2.0秒（英雄1.0秒）。",
3 = "攻击时有35%几率附加70点伤害并击晕目标2.5秒（英雄1.5秒）。",
}

[ACev]
_parent = "ACev"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
DataA = {1 = 0.15, 2 = 0.25, 3 = 0.35}
Tip = {
1 = "闪避 [一级]",
2 = "闪避 [二级]",
3 = "闪避 [顶级]",
}
Ubertip = {
1 = "给予15%的几率避开敌人的物理攻击。",
2 = "给予25%的几率避开敌人的物理攻击。",
3 = "给予35%的几率避开敌人的物理攻击。",
}

[ACtb]
_parent = "ACtb"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 1
Buttonpos_2 = 1
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 10.0, 2 = 8.0, 3 = 6.0}
DataA = {1 = 100.0, 2 = 185.0, 3 = 280.0}
Dur = {1 = 2.0, 2 = 2.5, 3 = 3.2}
HeroDur = {1 = 1.0, 2 = 1.5, 3 = 2.0}
Tip = {
1 = "投掷巨石 [一级]",
2 = "投掷巨石 [二级]",
3 = "投掷巨石 [顶级]",
}
Ubertip = {
1 = "投掷巨石造成100点伤害并昏晕目标2.0秒（英雄1.0秒）。",
2 = "投掷巨石造成185点伤害并昏晕目标2.5秒（英雄1.5秒）。",
3 = "投掷巨石造成280点伤害并昏晕目标3.2秒（英雄2.0秒）。",
}

[ACro]
_parent = "ACro"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 20.0, 2 = 18.0, 3 = 15.0}
DataA = {1 = 0.25, 2 = 0.40, 3 = 0.60}
Tip = {
1 = "战吼咆哮 [一级]",
2 = "战吼咆哮 [二级]",
3 = "战吼咆哮 [顶级]",
}
Ubertip = {
1 = "增加周围友军25%的攻击力，持续45秒。",
2 = "增加周围友军40%的攻击力，持续45秒。",
3 = "增加周围友军60%的攻击力，持续45秒。",
}

[ACif]
_parent = "ACif"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 1
Buttonpos_2 = 1
Cost = {1 = 35, 2 = 35, 3 = 35}
Cool = {1 = 1.0, 2 = 1.0, 3 = 1.0}
DataA = {1 = 0.10, 2 = 0.20, 3 = 0.35}
DataB = {1 = 5.0, 2 = 9.0, 3 = 14.0}
Tip = {
1 = "心灵之火 [一级]",
2 = "心灵之火 [二级]",
3 = "心灵之火 [顶级]",
}
Ubertip = {
1 = "增加友军10%攻击力与5点护甲。",
2 = "增加友军20%攻击力与9点护甲。",
3 = "增加友军35%攻击力与14点护甲。",
}

[ACsw]
_parent = "ACsw"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Cost = {1 = 50, 2 = 50, 3 = 50}
Cool = {1 = 1.0, 2 = 1.0, 3 = 1.0}
DataA = {1 = 0.50, 2 = 0.65, 3 = 0.80}
DataB = {1 = 0.25, 2 = 0.35, 3 = 0.50}
Tip = {
1 = "减速 [一级]",
2 = "减速 [二级]",
3 = "减速 [顶级]",
}
Ubertip = {
1 = "减慢目标50%移动速度和25%攻击速度。",
2 = "减慢目标65%移动速度和35%攻击速度。",
3 = "减慢目标80%移动速度和50%攻击速度。",
}

[AChx]
_parent = "AChx"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
Cost = {1 = 70, 2 = 70, 3 = 70}
Cool = {1 = 15.0, 2 = 11.0, 3 = 7.0}
Dur = {1 = 4.0, 2 = 6.0, 3 = 8.0}
HeroDur = {1 = 2.0, 2 = 3.0, 3 = 4.0}
Tip = {
1 = "妖术 [一级]",
2 = "妖术 [二级]",
3 = "妖术 [顶级]",
}
Ubertip = {
1 = "将目标变成小动物4秒（英雄2秒），冷却15秒。",
2 = "将目标变成小动物6秒（英雄3秒），冷却11秒。",
3 = "将目标变成小动物8秒（英雄4秒），冷却7秒。",
}

[ACst]
_parent = "ACst"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 1
Buttonpos_2 = 1
Cost = {1 = 90, 2 = 90, 3 = 90}
Cool = {1 = 10.0, 2 = 8.0, 3 = 6.0}
DataA = {1 = 90.0, 2 = 165.0, 3 = 260.0}
Dur = {1 = 2.0, 2 = 3.0, 3 = 4.0}
HeroDur = {1 = 1.0, 2 = 1.5, 3 = 2.0}
Tip = {
1 = "战争践踏 [一级]",
2 = "战争践踏 [二级]",
3 = "战争践踏 [顶级]",
}
Ubertip = {
1 = "猛踏地面造成90点范围伤害并击晕敌人2秒（英雄1秒）。",
2 = "猛踏地面造成165点范围伤害并击晕敌人3秒（英雄1.5秒）。",
3 = "猛踏地面造成260点范围伤害并击晕敌人4秒（英雄2秒）。",
}

[ACsh]
_parent = "ACsh"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 10.0, 2 = 8.0, 3 = 6.0}
DataA = {1 = 110.0, 2 = 190.0, 3 = 280.0}
Tip = {
1 = "震荡波 [一级]",
2 = "震荡波 [二级]",
3 = "震荡波 [顶级]",
}
Ubertip = {
1 = "发出一条震荡波，对一条线上的敌方单位造成110点伤害。",
2 = "发出一条强力震荡波，对一条线上的敌方单位造成190点伤害。",
3 = "发出一条毁灭震荡波，对一条线上的敌方单位造成280点伤害。",
}

[ACfl]
_parent = "ACfl"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 10.0, 2 = 8.0, 3 = 6.0}
DataA = {1 = 110.0, 2 = 185.0, 3 = 270.0}
Tip = {
1 = "叉状闪电 [一级]",
2 = "叉状闪电 [二级]",
3 = "叉状闪电 [顶级]",
}
Ubertip = {
1 = "释放电光打击多个敌方目标，造成110点伤害。",
2 = "释放强电光打击多个敌方目标，造成185点伤害。",
3 = "释放高压电光打击多个敌方目标，造成270点伤害。",
}

[ACfn]
_parent = "ACfn"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 1
Buttonpos_2 = 1
Cost = {1 = 125, 2 = 125, 3 = 125}
Cool = {1 = 10.0, 2 = 8.0, 3 = 6.0}
DataA = {1 = 50.0, 2 = 90.0, 3 = 140.0}
DataB = {1 = 100.0, 2 = 150.0, 3 = 210.0}
Tip = {
1 = "霜冻新星 [一级]",
2 = "霜冻新星 [二级]",
3 = "霜冻新星 [顶级]",
}
Ubertip = {
1 = "对主目标造成100点伤害，对周围造成50点冰霜伤害并减速。",
2 = "对主目标造成150点伤害，对周围造成90点冰霜伤害并减速。",
3 = "对主目标造成210点伤害，对周围造成140点冰霜伤害并减速。",
}

[ACf2]
_parent = "ACf2"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Cost = {1 = 40, 2 = 40, 3 = 40}
Cool = {1 = 2.0, 2 = 2.0, 3 = 2.0}
DataB = {1 = 3.0, 2 = 6.0, 3 = 10.0}
Tip = {
1 = "霜冻护甲 [一级]",
2 = "霜冻护甲 [二级]",
3 = "霜冻护甲 [顶级]",
}
Ubertip = {
1 = "增加友军目标3点护甲，近战攻击者会被减速。",
2 = "增加友军目标6点护甲，近战攻击者会被减速。",
3 = "增加友军目标10点护甲，近战攻击者会被减速。",
}

[ACen]
_parent = "ACen"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
Cost = {1 = 75, 2 = 75, 3 = 75}
Cool = {1 = 15.0, 2 = 11.0, 3 = 7.0}
Dur = {1 = 8.0, 2 = 11.0, 3 = 14.0}
HeroDur = {1 = 3.0, 2 = 4.0, 3 = 5.0}
Tip = {
1 = "诱捕 [一级]",
2 = "诱捕 [二级]",
3 = "诱捕 [顶级]",
}
Ubertip = {
1 = "束缚目标单位使其无法移动8秒（英雄3秒），冷却15秒。",
2 = "束缚目标单位使其无法移动11秒（英雄4秒），冷却11秒。",
3 = "束缚目标单位使其无法移动14秒（英雄5秒），冷却7秒。",
}

[ACrj]
_parent = "ACrj"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 1
Buttonpos_2 = 1
Cost = {1 = 100, 2 = 100, 3 = 100}
Cool = {1 = 10.0, 2 = 8.0, 3 = 6.0}
DataA = {1 = 400.0, 2 = 650.0, 3 = 950.0}
Tip = {
1 = "生命恢复 [一级]",
2 = "生命恢复 [二级]",
3 = "生命恢复 [顶级]",
}
Ubertip = {
1 = "在12秒内为友方目标恢复400点生命值。",
2 = "在12秒内为友方目标恢复650点生命值。",
3 = "在12秒内为友方目标恢复950点生命值。",
}

[ACcs]
_parent = "ACcs"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 2
Buttonpos_2 = 1
Cost = {1 = 40, 2 = 40, 3 = 40}
Cool = {1 = 1.0, 2 = 1.0, 3 = 1.0}
DataA = {1 = 0.33, 2 = 0.45, 3 = 0.60}
Tip = {
1 = "诅咒 [一级]",
2 = "诅咒 [二级]",
3 = "诅咒 [顶级]",
}
Ubertip = {
1 = "诅咒一个敌人，使其攻击有33%几率落空。",
2 = "诅咒一个敌人，使其攻击有45%几率落空。",
3 = "诅咒一个敌人，使其攻击有60%几率落空。",
}

[ACav]
_parent = "ACav"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
DataA = {1 = 0.15, 2 = 0.25, 3 = 0.35}
Tip = {
1 = "统御光环 [一级]",
2 = "统御光环 [二级]",
3 = "统御光环 [顶级]",
}
Ubertip = {
1 = "增加周围友军15%的基础攻击力。",
2 = "增加周围友军25%的基础攻击力。",
3 = "增加周围友军35%的基础攻击力。",
}

[ACdv]
_parent = "ACdv"
hero = 0
levels = 3
Requires = ""
Buttonpos_1 = 3
Buttonpos_2 = 1
DataA = {1 = 3.0, 2 = 5.0, 3 = 8.0}
Tip = {
1 = "专注光环 [一级]",
2 = "专注光环 [二级]",
3 = "专注光环 [顶级]",
}
Ubertip = {
1 = "增加周围友方单位3点护甲。",
2 = "增加周围友方单位5点护甲。",
3 = "增加周围友方单位8点护甲。",
}

[A031]
_parent = "ANcl"
Name = "狂野巨力"
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNBearForm.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNBearForm.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "taunt", 2 = "taunt", 3 = "taunt"}
Order = "taunt"
Cost = {1 = 0, 2 = 0, 3 = 0}
Cool = {1 = 0.5, 2 = 0.5, 3 = 0.5}
Tip = {
1 = "狂野巨力(|cffffcc00Q|r) - [等级 1]",
2 = "狂野巨力(|cffffcc00Q|r) - [等级 2]",
3 = "狂野巨力(|cffffcc00Q|r) - [等级 3]",
}
Ubertip = {
1 = "呼出近战/力量野怪二级化形菜单。【初阶融合】：以英雄自身面板为基准底子，额外叠加+55%野怪生命、攻击与护甲！攻速提升5%，赋予1阶特技，变身冷却10秒。永久保留英雄攻防与三维。",
2 = "呼出近战/力量野怪二级化形菜单。【深度融合】：以英雄自身面板为基准底子，额外叠加+90%野怪生命、攻击与护甲！攻速提升12%，赋予2阶特技，变身冷却8秒。永久保留英雄攻防与三维。",
3 = "呼出近战/力量野怪二级化形菜单。【完美共鸣】：以英雄自身面板为基准底子，额外叠加+130%野怪生命、攻击与护甲！攻速狂暴提升20%，赋予3阶顶级特技，变身冷却缩短至6秒！永久保留英雄攻防与三维。",
}
Researchtip = "学习 狂野巨力(|cffffcc00Q|r)"
Researchubertip = "开启近战力量野怪二级化形菜单。提升技能等级可提高野怪模板面板（1.00x/1.35x/1.70x）与特技阶数，并缩短变身冷却（10s/8s/6s）；升至3级时触发【野怪+英雄双面板叠加共鸣】！"

[A032]
_parent = "ANcl"
Name = "诡诈迅影"
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNSpiritWolf.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNSpiritWolf.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "parasite", 2 = "parasite", 3 = "parasite"}
Order = "parasite"
Cost = {1 = 0, 2 = 0, 3 = 0}
Cool = {1 = 0.5, 2 = 0.5, 3 = 0.5}
Tip = {
1 = "诡诈迅影(|cffffcc00W|r) - [等级 1]",
2 = "诡诈迅影(|cffffcc00W|r) - [等级 2]",
3 = "诡诈迅影(|cffffcc00W|r) - [等级 3]",
}
Ubertip = {
1 = "呼出远程/敏捷野怪二级化形菜单。【初阶融合】：以英雄自身面板为基准底子，额外叠加+55%野怪面板（获得500~600远程射程）！攻速提升5%，飞行怪升空并无视地面碰撞！变身冷却10秒。",
2 = "呼出远程/敏捷野怪二级化形菜单。【深度融合】：以英雄自身面板为基准底子，额外叠加+90%野怪面板（获得500~600远程射程）！攻速提升12%，飞行怪升空并无视地面碰撞！变身冷却8秒。",
3 = "呼出远程/敏捷野怪二级化形菜单。【完美共鸣】：以英雄自身面板为基准底子，额外叠加+130%野怪面板（获得500~600远程射程）！攻速狂暴提升20%，飞行怪升空并无视地面碰撞！变身冷却缩短至6秒。",
}
Researchtip = "学习 诡诈迅影(|cffffcc00W|r)"
Researchubertip = "开启远程敏捷野怪二级化形菜单。提升技能等级可提高野怪模板面板（1.00x/1.35x/1.70x）与特技阶数，并缩短变身冷却（10s/8s/6s）；升至3级时触发【野怪+英雄双面板叠加共鸣】！"

[A033]
_parent = "ANcl"
Name = "万相灵音"
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNRejuvenation.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNRejuvenation.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "autodispel", 2 = "autodispel", 3 = "autodispel"}
Order = "autodispel"
Cost = {1 = 0, 2 = 0, 3 = 0}
Cool = {1 = 0.5, 2 = 0.5, 3 = 0.5}
Tip = {
1 = "万相灵音(|cffffcc00E|r) - [等级 1]",
2 = "万相灵音(|cffffcc00E|r) - [等级 2]",
3 = "万相灵音(|cffffcc00E|r) - [等级 3]",
}
Ubertip = {
1 = "呼出法术/智力野怪二级化形菜单。【初阶融合】：以英雄自身面板为基准底子，额外叠加+55%野怪面板！攻速提升5%，附带1阶法术，血蓝比例双向继承，飞行怪升空并无视地面碰撞！冷却10秒。",
2 = "呼出法术/智力野怪二级化形菜单。【深度融合】：以英雄自身面板为基准底子，额外叠加+90%野怪面板！攻速提升12%，附带2阶强化法术，血蓝比例双向继承，飞行怪升空并无视地面碰撞！冷却8秒。",
3 = "呼出法术/智力野怪二级化形菜单。【完美共鸣】：以英雄自身面板为基准底子，额外叠加+130%野怪面板！攻速狂暴提升20%，附带3阶顶级法术，血蓝比例双向继承，飞行怪升空并无视地面碰撞！冷却缩短至6秒。",
}
Researchtip = "学习 万相灵音(|cffffcc00E|r)"
Researchubertip = "开启法术智力野怪二级化形菜单。提升技能等级可提高野怪模板面板（1.00x/1.35x/1.70x）与法术阶数，并缩短变身冷却（10s/8s/6s）；升至3级时触发【野怪+英雄双面板叠加共鸣】！"

[A034]
_parent = "ANcl"
Name = "返璞归真"
Hotkey = "R"
Buttonpos_1 = 3
Buttonpos_2 = 2
levels = 1
hero = 0
Cost = 0
Cool = 0.5
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNMetamorphosis.blp"
DataA = 0.0
DataB = 0
DataC = 1
DataD = 0.0
DataE = 0
DataF = "recharge"
Order = "recharge"
Tip = "返璞归真(|cffffcc00R|r)"
Ubertip = "一键解除当前的野怪化形形态，重塑为万灵化身神体！无损平滑还原英雄生命、法力、攻防面板并恢复自然法相。冷却0.5秒。"

[A035]
_parent = "ANcl"
Name = "众野之怒"
Hotkey = "D"
Researchhotkey = "D"
Buttonpos_1 = 2
Buttonpos_2 = 1
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 6
levelSkip = 2
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNStampede.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNStampede.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 0, 2 = 0, 3 = 0}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "starfall", 2 = "starfall", 3 = "starfall"}
Order = "starfall"
Cost = {1 = 150, 2 = 175, 3 = 200}
Cool = {1 = 110.0, 2 = 100.0, 3 = 90.0}
Tip = {
1 = "众野之怒(|cffffcc00D|r) - [等级 1]",
2 = "众野之怒(|cffffcc00D|r) - [等级 2]",
3 = "众野之怒(|cffffcc00D|r) - [等级 3]",
}
Ubertip = {
1 = "唤醒荒野兽潮，召唤10头真实血量的精锐部队发起冲锋推线！【为虎作伥】：兽潮击杀敌方英雄永久炼化为伪英雄伥鬼（复制装备与被动，至多8位）；击杀>=3级非工人精锐单位收为精锐伥鬼（至多12头，高阶自动替换低阶）；击杀普通单位永久累加【百鬼军魂】（每层全体召唤物+4生命，每2层+1攻击，在场部队即时成长）。开大时全体伥鬼共享军魂全副武装随军出征！持续90秒。冷却110秒。",
2 = "唤醒荒野兽潮，召唤10头强化高阶荒野巨兽军团冲锋推线！【为虎作伥】：击杀敌方英雄永久炼化为伪英雄伥鬼（至多8位），击杀精锐单位优胜劣汰炼化为精锐伥鬼（至多12头），击杀普通单位每层全军+4生命/+0.5攻击！开大时全体伥鬼共享军魂随军出征！持续90秒。冷却100秒。",
3 = "唤醒终极荒野世界Boss巨浪（远古黑龙/花岗岩傀儡/远古红龙/艾瑞达术士/战争魔像）强推敌阵！【为虎作伥】：所有被奴役的伪英雄与精锐伥鬼大军共享百鬼军魂成长（每层全军+4生命/+0.5攻击，在场实时成长）全副武装随主力大军出征！持续90秒。冷却90秒。",
}
Researchtip = "学习 众野之怒(|cffffcc00D|r)"
Researchubertip = "唤醒荒野兽潮，召唤拥有真实战力与血量的不可控荒野大军推线冲锋！【为虎作伥】：兽潮击杀敌方英雄炼化为伪英雄伥鬼（复制装备被动），击杀精锐小兵优胜劣汰收为精锐伥鬼；普通击杀叠加【百鬼军魂】永久强化全体荒野大军属性并在场即时成长！"
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
defType = "hero"
spd = 400
atkType1 = "chaos"
dmgplus1 = 160
dice1 = 2
sides1 = 15
cool1 = 1.10
rangeN1 = 150
weapTp1 = "normal"
abilList = "A017,ACce,Amim"
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
abilList = "A017,AInv"
foodCost = 0
level = 5

[u003]
_parent = "ogru"
Name = "荒野伥鬼"
file = "units\\\\orc\\\\Grunt\\\\Grunt.mdl"
"file:hd" = "units\\\\orc\\\\Grunt\\\\Grunt.mdl"
"file:sd" = "units\\\\orc\\\\Grunt\\\\Grunt.mdl"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNGrunt.blp"
unitSound = "Grunt"
modelScale = 1.0
HP = 1000
regenHP = 3.0
def = 5.0
defType = "hero"
spd = 320
atkType1 = "hero"
weapTp1 = "normal"
dmgplus1 = 50
dice1 = 2
sides1 = 6
cool1 = 1.40
rangeN1 = 128
abilList = "AInv"
foodCost = 0
level = 6

[H004]
_parent = "Ucrl"
Name = "异种之源"
Propernames = "太古原虫,深渊母体,基因掠夺者"
Tip = "召唤 异种之源(|cffffcc00P|r)"
Ubertip = "来自远古地底的终极捕食者与欺诈潜伏者。擅长极速潜地突袭、斩杀吞噬残血猎物并获得永久生命/攻击/法力进化、拟态伪装成受害者混入敌阵，并通过基因掠夺夺取敌方英雄的核心技能！|n|n|cffffcc00技能：|r|n- 渊潜掠影 (Q)|n- 捕食吞噬 (W)|n- 拟态伪装 (E)|n- 异种进化：基因掠夺 (R)"
Revivetip = "复活 异种之源(|cffffcc00P|r)"
Awakentip = "唤醒 异种之源(|cffffcc00P|r)"
Hotkey = "P"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNArachnathid.blp"
file = "Units\\\\Creeps\\\\Archnathid\\\\Archnathid"
"file:hd" = "Units\\\\Creeps\\\\Archnathid\\\\Archnathid"
"file:sd" = "Units\\\\Creeps\\\\Archnathid\\\\Archnathid"
unitSound = "Arachnathid"
modelScale = 1.25
scale = 1.25
Primary = "AGI"
primary = "AGI"
STR = 21
AGI = 25
INT = 17
STRplus = 2.40
AGIplus = 3.30
INTplus = 1.80
spd = 315
dmgplus1 = 26
dice1 = 2
sides1 = 8
cool1 = 1.45
rangeN1 = 128
bpx = 2
bpy = 2
Buttonpos_1 = 2
Buttonpos_2 = 2
fused = 5
goldcost = 425
lumbercost = 100
bldtm = 55
heroAbilList = "A021,A022,A023,A024"
abilList = "AInv"
requires = ""
requirescount = 0
requires1 = ""
requires2 = ""

[H005]
_parent = "Ekee"
Name = "万灵化身"
Propernames = "荒野千面,万兽之主,千相德鲁伊,盖亚化身"
Tip = "召唤 万灵化身(|cffffcc00V|r)"
Ubertip = "掌控天地万灵百态的自然主宰。可随意化身为大千世界的各种野怪形态，完美保留英雄三维与攻击护甲属性，兼具极速无损血蓝换算，并在6级号令狂暴野怪大军推平敌阵！|n|n|cffffcc00技能：|r|n- 狂野巨力 (Q)|n- 诡诈迅影 (W)|n- 万相灵音 (E)|n- 返璞归真 (R)|n- 众野之怒 (D)"
Revivetip = "复活 万灵化身(|cffffcc00V|r)"
Awakentip = "唤醒 万灵化身(|cffffcc00V|r)"
Hotkey = "V"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNFurion.blp"
file = "units\\\\nightelf\\\\MalFurion\\\\MalFurion"
"file:hd" = "units\\\\nightelf\\\\MalFurion\\\\MalFurion"
"file:sd" = "units\\\\nightelf\\\\MalFurion\\\\MalFurion"
unitSound = "Furion"
modelScale = 1.15
scale = 1.15
Primary = "STR"
primary = "STR"
STR = 22
AGI = 22
INT = 22
STRplus = 2.60
AGIplus = 2.60
INTplus = 2.60
spd = 310
dmgplus1 = 25
dice1 = 2
sides1 = 6
cool1 = 1.50
rangeN1 = 600
weapTp1 = "missile"
Missileart = "Abilities\\\\Weapons\\\\KeeperGroveMissile\\\\KeeperGroveMissile.mdl"
Missilespeed = 1000
bpx = 3
bpy = 2
Buttonpos_1 = 3
Buttonpos_2 = 2
fused = 5
goldcost = 425
lumbercost = 100
bldtm = 55
heroAbilList = "A031,A032,A033,A035"
abilList = "AInv,A034"
requires = ""
requirescount = 0
requires1 = ""
requires2 = ""

[halt]
_parent = "halt"
Trains = "Hamg,Hmkg,Hpal,Hblm,H002,H003,H004,H005"

[oalt]
_parent = "oalt"
Trains = "Obla,Ofar,Otch,Oshd,H002,H003,H004,H005"

[uaod]
_parent = "uaod"
Trains = "Udea,Ulic,Udre,Ucrl,H002,H003,H004,H005"

[eate]
_parent = "eate"
Trains = "Edem,Ekee,Emoo,Ewar,H002,H003,H004,H005"

[n003]
_parent = "halt"
Name = "测试酒馆·无敌避难所"
Ubertip = "人类玩家专属无敌避难所：自身绝对无敌，只要存在玩家绝不会被判负，并可在此复活全阵营阵亡英雄。"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNTavern.blp"
file = "buildings\\\\other\\\\Tavern\\\\Tavern"
"file:hd" = "buildings\\\\other\\\\Tavern\\\\Tavern"
"file:sd" = "buildings\\\\other\\\\Tavern\\\\Tavern"
unitSound = "AltarOfKings"
HP = 99999
def = 99.0
abilList = "Arev,Avul"
Requires = ""
requirescount = 0
goldcost = 0
lumbercost = 0
bldtm = 1
Revive = 1
Trains = "Hamg,Hmkg,Hpal,Hblm,Obla,Ofar,Otch,Oshd,Edem,Ekee,Emoo,Ewar,Udea,Ulic,Udre,Ucrl,H002,H003,H004,H005"
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
for sym in [b'H002', b'H003', b'H004', b'H005', b'u000', b'u001', b'u002', b'u003', b'halt', b'oalt', b'uaod', b'eate', b'n003']:
    print(f"w3u contains {sym.decode('ascii')}: {sym in w3u_data}")

with open(os.path.join(PAYLOAD_DIR, "war3map.w3a"), "rb") as f:
    w3a_data = f.read()
for sym in [b'A001', b'A002', b'A003', b'A004', b'A00V', b'A011', b'A012', b'A013', b'A014', b'A015', b'A016', b'A017', b'A021', b'A022', b'A023', b'A024', b'A025', b'A026', b'A027', b'A031', b'A032', b'A033', b'A034', b'A035', b'ACbl', b'ACls', b'ACpu', b'ACct', b'ACbh', b'ACev', b'ACtb', b'ACro', b'ACif', b'ACsw', b'AChx', b'ACst', b'ACsh', b'ACfl', b'ACfn', b'ACf2', b'ACen', b'ACrj', b'ACcs', b'ACav', b'ACdv']:
    print(f"w3a contains {sym.decode('ascii')}: {sym in w3a_data}")
