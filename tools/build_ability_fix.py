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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDarkSummoning.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNDarkSummoning.blp"
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
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDisruption.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNDisruption.blp"
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
1 = "复制选定范围内的所有单位生成真实幻象（拥有全套主动技能与装备），持续15分钟。幻象消灭敌人正常提供经验，且移除英雄经验判定，绝不分薄本体经验！|n|n等级 1：作用范围250码，冷却40秒。",
2 = "复制选定范围内的所有单位生成真实幻象（拥有全套主动技能与装备），持续15分钟。幻象消灭敌人正常提供经验，且移除英雄经验判定，绝不分薄本体经验！|n|n等级 2：作用范围350码，冷却35秒。",
3 = "复制选定范围内的所有单位生成真实幻象（拥有全套主动技能与装备），持续15分钟。幻象消灭敌人正常提供经验，且移除英雄经验判定，绝不分薄本体经验！|n|n等级 3：作用范围450码，冷却30秒。",
}
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

with open("factory_tpl/table/ability.ini", "w", encoding="utf-8") as f:
    f.write(ini_ability)

w2l = os.path.abspath('tools/w3x2lni/w2l.exe')
src = os.path.abspath('factory_tpl')
dst = os.path.abspath('hero_obj_v3.w3x')
if os.path.exists(dst): os.remove(dst)

p = subprocess.run([w2l, 'obj', src, dst, '-s'], cwd=os.path.dirname(w2l), capture_output=True)
print("RC:", p.returncode)
print("STDOUT:", p.stdout.decode('utf-8', 'replace'))
print("STDERR:", p.stderr.decode('utf-8', 'replace'))
print("Exists:", os.path.exists(dst), os.path.getsize(dst) if os.path.exists(dst) else 0)
