# -*- coding: utf-8 -*-
"""Update generate_all.py for v1.2 with Apiv stealth, Channel targeting image for E, and test hero."""
import os

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
TABLE = os.path.join(ROOT, "factory_tpl", "table")
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
DataA = {1 = 2, 2 = 2, 3 = 3}
DataB = {1 = 0.40, 2 = 0.70, 3 = 1.00}
DataC = {1 = 1.80, 2 = 1.40, 3 = 1.00}
DataD = {1 = 0.50, 2 = 0.50, 3 = 0.50}
Dur = {1 = 60.0, 2 = 60.0, 3 = 60.0}
HeroDur = {1 = 60.0, 2 = 60.0, 3 = 60.0}
Cool = {1 = 12.0, 2 = 12.0, 3 = 12.0}
Cost = {1 = 100, 2 = 110, 3 = 120}
Tip = {1 = "镜像(|cffffcc00Q|r) - [|cffffcc00等级 1|r]", 2 = "镜像(|cffffcc00Q|r) - [|cffffcc00等级 2|r]", 3 = "镜像(|cffffcc00Q|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "制造 2 个迷惑敌人的幻梦镜像。镜像拥有本体 40% 的攻击力，承受 180% 的伤害。施法后本体自动隐身并获得移速加成，攻击打破隐身并造成破隐一击。持续 60 秒。", 2 = "制造 2 个迷惑敌人的幻梦镜像。镜像拥有本体 70% 的攻击力，承受 140% 的伤害。施法后本体自动隐身，持续 60 秒。", 3 = "制造 3 个完全镜像！镜像拥有本体 100% 的攻击力、100% 的防御力与 100% 的真实血量承受！施法后本体自动隐身，持续 60 秒。"}
Researchtip = "学习 镜像(|cffffcc00Q|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "制造分身迷惑敌人，最高级拥有 100% 攻防与血量，施法瞬间本体自动隐身。"

[A00V]
_parent = "Apiv"
Name = "幻梦真实潜行"
levels = 1
hero = 0
item = 0
checkdep = 0
Dur = {1 = 0.0}
HeroDur = {1 = 0.0}
DataA = {1 = 0}

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
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "charm", 2 = "charm", 3 = "charm"}
Order = "charm"
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cool = {1 = 30.0, 2 = 25.0, 3 = 20.0}
Cost = {1 = 100, 2 = 125, 3 = 150}
checkdep = 0
targs = {1 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward", 2 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward", 3 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward"}
Tip = {1 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 1|r]", 2 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 2|r]", 3 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "将目标单位、野怪或建筑的心智拖入幻梦，强行夺取其绝对操控权，持续 30 秒。持续时间结束后归还所属权。若控制敌方英雄，英雄阵亡前必定归还给原主，绝不在己方祭坛复活。", 2 = "强行夺取目标单位、野怪或建筑的操控权，持续 2 分钟 (120 秒)。到期归还，阵亡英雄归还原主。", 3 = "强行夺取目标单位、野怪或建筑的操控权，持续 10 分钟 (600 秒)！到期归还，阵亡英雄归还原主。"}
Researchtip = "学习 幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "操控任何单位、野怪甚至敌方建筑与英雄。1级持续30秒，2级2分钟，3级10分钟。"

[A003]
_parent = "ANcl"
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
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 2, 2 = 2, 3 = 2}
DataC = {1 = 3, 2 = 3, 3 = 3}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "blizzard", 2 = "blizzard", 3 = "blizzard"}
Order = "blizzard"
Area = {1 = 250.0, 2 = 350.0, 3 = 450.0}
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cool = {1 = 35.0, 2 = 30.0, 3 = 25.0}
Cost = {1 = 120, 2 = 140, 3 = 160}
checkdep = 0
TargetArt = "Abilities\\\\Spells\\\\Other\\\\Silence\\\\SilenceAreaBirth.mdl"
EffectArt = "Abilities\\\\Spells\\\\Other\\\\Silence\\\\SilenceAreaBirth.mdl"
Tip = {1 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 1|r]", 2 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 2|r]", 3 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "选定 250 码范围，将其内所有单位的灵魂具现化为真实幻象！召唤的幻象几乎可视为本体，能完整使用全部主动技能与魔法，不抢英雄经验，不占人口，持续长达 15 分钟 (900 秒)！", 2 = "召唤 350 码范围内所有单位的真实幻象，可使用主动技能，不分薄经验，持续 15 分钟。", 3 = "召唤 450 码范围内所有单位的真实幻象，大军成型，持续 15 分钟！"}
Researchtip = "学习 万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "在指定范围内召唤所有单位的真实幻象，显示清晰范围圈且无任何沉默负面效果，幻象能自由使用主动技能，不分薄经验，持续 15 分钟。"

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
Ubertip = {1 = "被动【阿哈利姆神杖质变】：唤醒梦境至高权柄，使前三个技能获得质的飞跃：|n|cffffcc001. 镜像质变【真幻同生 & 破隐一击】|r：隐身移速达到极限522；破隐第一击附加 200 点致命暗影爆发伤害；镜像消亡时产生【幻象反冲】，自爆造成 200 点范围伤害与减速。|n|cffffcc002. 幻梦奴役质变【狂乱梦噬 & 杀戮延时】|r：被控制目标获得狂暴祝福（+40%移速、+50%攻速，每秒恢复 3% 最大生命）；且被控制单位每击杀一个敌军，控制时间自动延长 15 秒！若控制的是建筑，其攻速与自愈速度翻倍。|n|cffffcc003. 万象皆虚质变【梦魇剥离 & 幻体反哺】|r：施法瞬间使范围内所有敌军陷入 3 秒梦魇昏睡；召唤出的所有幻象部队，其攻击与技能伤害的 25% 将源源不断地转化为生命值反哺幻梦大师！"}
Researchtip = "领悟 幻界主宰(|cffffcc00R|r)"
Researchubertip = "被动终极技能：类似阿哈利姆神杖，全面颠覆与进化前三个技能的实战机制。"
'''

with open(os.path.join(TABLE, "ability.ini"), "w", encoding="utf-8", newline="\r\n") as f:
    f.write(abil_txt)

# ------------------------------------------------------------------ JASS Logic
jass_code = '''//===========================================================================
// Dream Master System Implementation (v1.2 Fixed: Apiv Stealth + Range Circle)
//===========================================================================

function DM_GetHeroIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_DM_HeroCount
        if udg_DM_Hero[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    if udg_DM_HeroCount < 32 then
        set udg_DM_Hero[udg_DM_HeroCount] = u
        set udg_DM_Backstab[udg_DM_HeroCount] = false
        set udg_DM_InvisTimer[udg_DM_HeroCount] = 0
        set udg_DM_HeroCount = udg_DM_HeroCount + 1
        return udg_DM_HeroCount - 1
    endif
    return -1
endfunction

function DM_FindCapIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_CapCount
        if udg_CapUnit[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    return -1
endfunction

function DM_RemoveCapIndex takes integer idx returns nothing
    if idx >= 0 and idx < udg_CapCount then
        set udg_CapUnit[idx] = udg_CapUnit[udg_CapCount - 1]
        set udg_CapOrigOwner[idx] = udg_CapOrigOwner[udg_CapCount - 1]
        set udg_CapDuration[idx] = udg_CapDuration[udg_CapCount - 1]
        set udg_CapCaster[idx] = udg_CapCaster[udg_CapCount - 1]
        set udg_CapIsHero[idx] = udg_CapIsHero[udg_CapCount - 1]
        set udg_CapAghBuff[idx] = udg_CapAghBuff[udg_CapCount - 1]
        set udg_CapUnit[udg_CapCount - 1] = null
        set udg_CapOrigOwner[udg_CapCount - 1] = null
        set udg_CapCaster[udg_CapCount - 1] = null
        set udg_CapCount = udg_CapCount - 1
    endif
endfunction

function DM_RestoreControl takes integer idx returns nothing
    local unit u = udg_CapUnit[idx]
    local player p = udg_CapOrigOwner[idx]
    if u != null and p != null then
        call SetUnitOwner(u, p, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", u, "origin"))
    endif
    call DM_RemoveCapIndex(idx)
    set u = null
    set p = null
endfunction

// 解除潜行与恢复移速、透明度
function DM_BreakInvisibility takes unit u returns nothing
    local integer hIdx = DM_GetHeroIndex(u)
    if hIdx >= 0 then
        set udg_DM_InvisTimer[hIdx] = 0
    endif
    call UnitRemoveAbility(u, 'A00V')
    call SetUnitVertexColor(u, 255, 255, 255, 255)
    call SetUnitMoveSpeed(u, 320.0)
endfunction

// 一技能：镜像分裂完成后的真实潜行激活（延时0.35秒，绝不打断镜像分身生成）
function DM_OnMirrorImage_Timer takes nothing returns nothing
    local unit u = udg_DM_WW_Caster
    local integer lv = udg_DM_WW_Level
    local integer hIdx = 0
    local boolean hasAgh = false
    local real spd = 450.0
    
    if u != null and GetUnitState(u, UNIT_STATE_LIFE) > 0.405 then
        set hIdx = DM_GetHeroIndex(u)
        set hasAgh = GetUnitAbilityLevel(u, 'A004') > 0
        
        // 赋予真实隐形能力（Apiv底层瞬发被动隐匿，敌军绝对不可视）
        call UnitAddAbility(u, 'A00V')
        
        // 幽光半透明外观，给玩家清晰可见的潜行反馈
        call SetUnitVertexColor(u, 140, 140, 255, 120)
        
        if hasAgh then
            set spd = 522.0
        endif
        call SetUnitMoveSpeed(u, spd)
        
        if hIdx >= 0 then
            set udg_DM_Backstab[hIdx] = true
            set udg_DM_InvisTimer[hIdx] = 30 + lv * 15
        endif
        
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\WindWalk\\\\WindWalkTarget.mdl", u, "origin"))
    endif
    
    set udg_DM_WW_Caster = null
    call DestroyTimer(GetExpiredTimer())
endfunction

function DM_CastMirrorImage takes unit caster returns nothing
    local timer t = CreateTimer()
    set udg_DM_WW_Caster = caster
    set udg_DM_WW_Level = GetUnitAbilityLevel(caster, 'A001')
    call TimerStart(t, 0.35, false, function DM_OnMirrorImage_Timer)
    set t = null
endfunction

// 二技能：幻梦奴役
function DM_CastPossession takes unit caster, unit target returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A002')
    local player casterPlayer = GetOwningPlayer(caster)
    local player origPlayer = GetOwningPlayer(target)
    local real dur = 30.0
    local integer idx = 0
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    if target == null or origPlayer == casterPlayer then
        return
    endif
    
    if lv == 2 then
        set dur = 120.0
    elseif lv >= 3 then
        set dur = 600.0
    endif
    
    set idx = DM_FindCapIndex(target)
    if idx >= 0 then
        set udg_CapDuration[idx] = dur
        set udg_CapCaster[idx] = caster
        set udg_CapAghBuff[idx] = hasAgh
        return
    endif
    
    if udg_CapCount < 128 then
        set udg_CapUnit[udg_CapCount] = target
        set udg_CapOrigOwner[udg_CapCount] = origPlayer
        set udg_CapDuration[udg_CapCount] = dur
        set udg_CapCaster[udg_CapCount] = caster
        set udg_CapIsHero[udg_CapCount] = IsUnitType(target, UNIT_TYPE_HERO)
        set udg_CapAghBuff[udg_CapCount] = hasAgh
        set udg_CapCount = udg_CapCount + 1
        
        call SetUnitOwner(target, casterPlayer, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Possession\\\\PossessionTarget.mdl", target, "overhead"))
        
        if hasAgh and not IsUnitType(target, UNIT_TYPE_STRUCTURE) then
            call SetUnitMoveSpeed(target, GetUnitMoveSpeed(target) * 1.40)
        endif
    endif
endfunction

// 三技能：万象皆虚（召唤指定范围内所有单位的真实幻象，不沉默，不分薄经验，带范围圈指示）
function DM_CastMassIllusion takes unit caster, real cx, real cy returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A003')
    local player p = GetOwningPlayer(caster)
    local real radius = 250.0
    local unit t = null
    local unit clone = null
    local integer utid = 0
    local integer oldFood = 0
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    if lv == 2 then
        set radius = 350.0
    elseif lv >= 3 then
        set radius = 450.0
    endif
    
    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Other\\\\Silence\\\\SilenceAreaBirth.mdl", cx, cy))
    
    call GroupEnumUnitsInRange(udg_EnumGroup, cx, cy, radius, null)
    loop
        set t = FirstOfGroup(udg_EnumGroup)
        exitwhen t == null
        call GroupRemoveUnit(udg_EnumGroup, t)
        
        if GetUnitState(t, UNIT_STATE_LIFE) > 0.405 and not IsUnitType(t, UNIT_TYPE_STRUCTURE) and not IsUnitType(t, UNIT_TYPE_DEAD) then
            set utid = GetUnitTypeId(t)
            
            // 复制前记录人口，复制后重置人口消耗（绝不卡死人口上限）
            set oldFood = GetPlayerState(p, PLAYER_STATE_RESOURCE_FOOD_USED)
            set clone = CreateUnit(p, utid, GetUnitX(t), GetUnitY(t), GetUnitFacing(t))
            call SetPlayerState(p, PLAYER_STATE_RESOURCE_FOOD_USED, oldFood)
            
            if clone != null then
                call UnitApplyTimedLife(clone, 'BTLF', 900.0)
                call UnitAddType(clone, UNIT_TYPE_SUMMONED)
                
                call SetUnitVertexColor(clone, 90, 130, 255, 175)
                call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", GetUnitX(clone), GetUnitY(clone)))
                
                // 彻底剥除英雄标志，绝不分薄本体经验！
                if IsUnitType(t, UNIT_TYPE_HERO) then
                    call SetHeroLevel(clone, GetHeroLevel(t), false)
                    call UnitRemoveType(clone, UNIT_TYPE_HERO)
                    call SuspendHeroXP(clone, true)
                    call GroupAddUnit(udg_CloneHeroGroup, clone)
                endif
                
                if hasAgh then
                    call GroupAddUnit(udg_AghCloneGroup, clone)
                endif
            endif
            
            if hasAgh and IsUnitEnemy(t, p) then
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Sleep\\\\SleepTarget.mdl", t, "overhead"))
            endif
        endif
    endloop
    
    set t = null
    set clone = null
endfunction

function DM_OnSpellEffect takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer abil = GetSpellAbilityId()
    
    // 施放非镜像技能时，自然打破潜行
    if abil != 'A001' and GetUnitAbilityLevel(caster, 'A00V') > 0 then
        call DM_BreakInvisibility(caster)
    endif
    
    if abil == 'A001' then
        call DM_CastMirrorImage(caster)
    elseif abil == 'A002' then
        call DM_CastPossession(caster, GetSpellTargetUnit())
    elseif abil == 'A003' then
        call DM_CastMassIllusion(caster, GetSpellTargetX(), GetSpellTargetY())
    endif
    
    set caster = null
    return false
endfunction

function DM_OnDamaged takes nothing returns boolean
    local unit victim = GetTriggerUnit()
    local unit attacker = GetEventDamageSource()
    local real dmg = GetEventDamage()
    local integer idx = 0
    local integer hIdx = 0
    
    // 1. 奴役目标濒死保护
    set idx = DM_FindCapIndex(victim)
    if idx >= 0 then
        if dmg >= GetWidgetLife(victim) then
            call DM_RestoreControl(idx)
        endif
    endif
    
    // 2. 破隐一击（解除隐形，附加暗影伤害）
    set hIdx = DM_GetHeroIndex(attacker)
    if hIdx >= 0 and udg_DM_Backstab[hIdx] then
        set udg_DM_Backstab[hIdx] = false
        call DM_BreakInvisibility(attacker)
        if GetUnitAbilityLevel(attacker, 'A004') > 0 then
            call UnitDamageTarget(attacker, victim, 200.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_MAGIC, WEAPON_TYPE_WHOKNOWS)
        else
            call UnitDamageTarget(attacker, victim, 50.0 + I2R(GetUnitAbilityLevel(attacker, 'A001')) * 40.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_MAGIC, WEAPON_TYPE_WHOKNOWS)
        endif
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\ShadowHunter\\\\ShadowHunterMissile.mdl", victim, "chest"))
    endif
    
    // 3. 神杖反哺
    if IsUnitInGroup(attacker, udg_AghCloneGroup) and dmg > 0.0 then
        set hIdx = 0
        loop
            exitwhen hIdx >= udg_DM_HeroCount
            if GetOwningPlayer(udg_DM_Hero[hIdx]) == GetOwningPlayer(attacker) and GetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE) > 0.405 then
                call SetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE, GetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE) + dmg * 0.25)
            endif
            set hIdx = hIdx + 1
        endloop
    endif
    
    set victim = null
    set attacker = null
    return false
endfunction

function DM_OnDeath takes nothing returns boolean
    local unit dying = GetDyingUnit()
    local unit killer = GetKillingUnit()
    local integer idx = 0
    local group g = null
    local unit enumU = null
    
    set idx = DM_FindCapIndex(dying)
    if idx >= 0 then
        call DM_RestoreControl(idx)
    endif
    
    if IsUnitInGroup(dying, udg_CloneHeroGroup) then
        call GroupRemoveUnit(udg_CloneHeroGroup, dying)
        call RemoveUnit(dying)
    endif
    
    if killer != null then
        set idx = DM_FindCapIndex(killer)
        if idx >= 0 and udg_CapAghBuff[idx] then
            set udg_CapDuration[idx] = udg_CapDuration[idx] + 15.0
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Bloodlust\\\\BloodlustTarget.mdl", killer, "origin"))
        endif
    endif
    
    // 镜像消亡自爆
    if IsUnitIllusion(dying) and GetUnitTypeId(dying) == 'H002' then
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", GetUnitX(dying), GetUnitY(dying)))
        set g = CreateGroup()
        call GroupEnumUnitsInRange(g, GetUnitX(dying), GetUnitY(dying), 400.0, null)
        loop
            set enumU = FirstOfGroup(g)
            exitwhen enumU == null
            call GroupRemoveUnit(g, enumU)
            if IsUnitEnemy(enumU, GetOwningPlayer(dying)) and GetUnitState(enumU, UNIT_STATE_LIFE) > 0.405 then
                call UnitDamageTarget(dying, enumU, 200.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_MAGIC, WEAPON_TYPE_WHOKNOWS)
            endif
        endloop
        call DestroyGroup(g)
        set g = null
    endif
    
    set dying = null
    set killer = null
    return false
endfunction

function DM_PeriodicLoop takes nothing returns nothing
    local integer i = udg_CapCount - 1
    local unit u = null
    local real maxHP = 0.0
    
    loop
        exitwhen i < 0
        set u = udg_CapUnit[i]
        
        if u == null or GetUnitState(u, UNIT_STATE_LIFE) <= 0.405 then
            call DM_RestoreControl(i)
        else
            set udg_CapDuration[i] = udg_CapDuration[i] - 1.0
            
            if udg_CapAghBuff[i] and not IsUnitType(u, UNIT_TYPE_STRUCTURE) then
                set maxHP = GetUnitState(u, UNIT_STATE_MAX_LIFE)
                call SetUnitState(u, UNIT_STATE_LIFE, GetUnitState(u, UNIT_STATE_LIFE) + maxHP * 0.03)
            endif
            
            if udg_CapDuration[i] <= 0.0 then
                call DM_RestoreControl(i)
            endif
        endif
        
        set i = i - 1
    endloop
    
    // 隐形倒计时维护
    set i = 0
    loop
        exitwhen i >= udg_DM_HeroCount
        set u = udg_DM_Hero[i]
        if u != null then
            if udg_DM_InvisTimer[i] > 0 then
                set udg_DM_InvisTimer[i] = udg_DM_InvisTimer[i] - 1
                if udg_DM_InvisTimer[i] <= 0 then
                    call DM_BreakInvisibility(u)
                endif
            endif
        endif
        set i = i + 1
    endloop
    
    set u = null
endfunction

// 开局放置 10 级幻梦大师供玩家直接测试
function DM_SpawnTestHero takes nothing returns nothing
    local unit dm = CreateUnit(Player(0), 'H002', -6656.0, 5376.0, 270.0)
    call SetHeroLevel(dm, 10, false)
    call SelectUnitForPlayerSingle(dm, Player(0))
    set dm = null
endfunction

function Init_DreamMasterSystem takes nothing returns nothing
    local trigger tSpell = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local timer tTimer = CreateTimer()
    local integer i = 0
    
    set udg_EnumGroup = CreateGroup()
    set udg_CloneHeroGroup = CreateGroup()
    set udg_AghCloneGroup = CreateGroup()
    set udg_MirrorGroup = CreateGroup()
    
    loop
        exitwhen i >= 16
        call TriggerRegisterPlayerUnitEvent(tSpell, Player(i), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
        call TriggerRegisterPlayerUnitEvent(tDamage, Player(i), EVENT_PLAYER_UNIT_DAMAGED, null)
        call TriggerRegisterPlayerUnitEvent(tDeath, Player(i), EVENT_PLAYER_UNIT_DEATH, null)
        set i = i + 1
    endloop
    
    call TriggerRegisterPlayerUnitEvent(tSpell, Player(24), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
    call TriggerRegisterPlayerUnitEvent(tDamage, Player(24), EVENT_PLAYER_UNIT_DAMAGED, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(24), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tSpell, Player(25), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
    call TriggerRegisterPlayerUnitEvent(tDamage, Player(25), EVENT_PLAYER_UNIT_DAMAGED, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(25), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(26), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(27), EVENT_PLAYER_UNIT_DEATH, null)
    
    call TriggerAddCondition(tSpell, Condition(function DM_OnSpellEffect))
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))
    call TriggerAddCondition(tDeath, Condition(function DM_OnDeath))
    
    call TimerStart(tTimer, 1.00, true, function DM_PeriodicLoop)
    
    // 生成测试英雄
    call DM_SpawnTestHero()
endfunction
'''

RAW_J = os.path.join(ROOT, "raw", "war3map.j")
PAYLOAD_DIR = os.path.join(ROOT, "payload")
OUT_J = os.path.join(PAYLOAD_DIR, "war3map.j")

GLOBALS = '''    // [Dream Master globals]
    unit array udg_CapUnit
    player array udg_CapOrigOwner
    real array udg_CapDuration
    unit array udg_CapCaster
    boolean array udg_CapIsHero
    boolean array udg_CapAghBuff
    integer udg_CapCount = 0
    group udg_EnumGroup = null
    group udg_CloneHeroGroup = null
    group udg_AghCloneGroup = null
    group udg_MirrorGroup = null
    unit array udg_DM_Hero
    boolean array udg_DM_Backstab
    integer array udg_DM_InvisTimer
    integer udg_DM_HeroCount = 0
    unit udg_DM_WW_Caster = null
    integer udg_DM_WW_Level = 1
'''

with open(RAW_J, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

pos_endglobals = text.find("endglobals")
text = text[:pos_endglobals] + GLOBALS + text[pos_endglobals:]

pos_main = text.find("function main takes nothing returns nothing")
text = text[:pos_main] + jass_code + text[pos_main:]

pos_main = text.find("function main takes nothing returns nothing")
pos_endmain = text.find("endfunction", pos_main)
text = text[:pos_endmain] + "    call Init_DreamMasterSystem()\n" + text[pos_endmain:]

with open(OUT_J, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(text)
print("[ok] payload/war3map.j generated")
