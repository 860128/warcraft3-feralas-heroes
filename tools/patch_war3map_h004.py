# -*- coding: utf-8 -*-
import sys
import re

J_PATH = 'payload/war3map.j'

# Read clean backup
with open(J_PATH + '.bak_v22', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_func(src, func_name, new_code):
    pattern = rf'function {func_name} takes[^\n]*\n.*?endfunction'
    m = re.search(pattern, src, flags=re.DOTALL)
    if not m:
        raise ValueError(f"Function {func_name} not found in content!")
    return src[:m.start()] + new_code.strip() + src[m.end():]

print("Starting patch on war3map.j, original length:", len(content))

# 1. Globals patch
globals_strain = """    // Hero #3: The Primordial Strain (H004) Globals
    boolean array udg_Strain_Burrowed
    real array udg_Strain_BurrowTimer
    unit array udg_Strain_KnockUnit
    real array udg_Strain_KnockTimer
    integer udg_Strain_KnockCount = 0

    real array udg_Strain_DigestTimer
    integer array udg_Strain_DigestType
    player array udg_Strain_DigestOwner
    boolean array udg_Strain_DigestIsHero
    effect array udg_Strain_DigestFx

    boolean array udg_Strain_MimicActive
    integer array udg_Strain_MimicType
    player array udg_Strain_MimicOwner
    unit array udg_Strain_MimicActor

    // Gene Evolution State per player (0..7)
    // GeneCat: 0=None, 1=Shield(步兵举盾/反射), 2=Poison(小鹿剧毒/扩散), 3=Bloodlust(萨满/野怪嗜血), 4=Thunder(法系/巨兽雷击), 5=StolenHeroSkill(英雄技能)
    integer array udg_Strain_GeneCat
    integer array udg_Strain_EvoTier
    integer array udg_Strain_StolenHeroAbil
    integer array udg_Strain_CandidateAbil0
    integer array udg_Strain_CandidateAbil1
    integer array udg_Strain_CandidateAbil2
    integer array udg_Strain_CandidateAbil3

    dialog udg_Strain_GeneDialog = null
    button udg_Strain_BtnKeep = null
    button udg_Strain_BtnDiscard = null

    dialog udg_Strain_HeroDialog = null
    button array udg_Strain_HeroSkillBtn

    unit array udg_Strain_Hero
    button udg_TM_BtnMode3All = null
    boolean udg_Strain_DamageLock = false
"""

target_globals = "    group udg_FakeHeroGroup = null\n"
assert target_globals in content, "target_globals not found"
content = content.replace(target_globals, target_globals + "\n" + globals_strain + "\n", 1)

# 2. Hero #3 core functions before DM_StealthLoop
strain_core_funcs = """//===========================================================================
// Hero #3: The Primordial Strain (异种之源 H004) System
//===========================================================================

function Strain_InitHero takes unit h returns nothing
    if h == null then
        return
    endif
    if GetUnitAbilityLevel(h, 'A024') == 0 then
        call UnitAddAbility(h, 'A024')
    endif
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Burrow\\\\BurrowTarget.mdl", h, "origin"))
endfunction

function Strain_BreakMimicry takes unit u, integer pId returns nothing
    if not udg_Strain_MimicActive[pId] then
        return
    endif
    set udg_Strain_MimicActive[pId] = false
    if udg_Strain_MimicActor[pId] != null then
        call RemoveUnit(udg_Strain_MimicActor[pId])
        set udg_Strain_MimicActor[pId] = null
    endif
    if u != null then
        call SetUnitVertexColor(u, 255, 255, 255, 255)
        call SetUnitColor(u, GetPlayerColor(GetOwningPlayer(u)))
        call SetPlayerAllianceStateBJ(Player(PLAYER_NEUTRAL_AGGRESSIVE), GetOwningPlayer(u), bj_ALLIANCE_UNALLIED)
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageDeathCaster.mdl", GetUnitX(u), GetUnitY(u)))
    endif
endfunction

function Strain_Unburrow takes unit u, integer pId returns nothing
    local unit enumU = null
    local real dmg = 0.0
    if u == null then
        return
    endif
    set udg_Strain_Burrowed[pId] = false
    set udg_Strain_BurrowTimer[pId] = 0.0
    call UnitRemoveBuffBJ('Binv', u)
    call UnitRemoveAbility(u, 'A00V')
    call SetUnitPathing(u, true)
    if udg_Strain_GeneCat[pId] == 1 and udg_Strain_EvoTier[pId] >= 2 then
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 65.0)
    elseif udg_Strain_GeneCat[pId] == 3 and udg_Strain_EvoTier[pId] >= 2 then
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 60.0)
    else
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))
    endif
    call SetUnitVertexColor(u, 255, 255, 255, 255)
    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Undead\\\\Impale\\\\ImpaleHitTarget.mdl", GetUnitX(u), GetUnitY(u)))
    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", GetUnitX(u), GetUnitY(u)))

    set dmg = 60.0 + 60.0 * I2R(GetUnitAbilityLevel(u, 'A021')) + 1.5 * I2R(GetHeroAgi(u, true))
    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRange(udg_EnumGroup, GetUnitX(u), GetUnitY(u), 250.0, null)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if IsUnitEnemy(enumU, GetOwningPlayer(u)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
            call UnitDamageTarget(u, enumU, dmg, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
            call UnitAddAbility(enumU, 'Amrf')
            call UnitRemoveAbility(enumU, 'Amrf')
            call SetUnitFlyHeight(enumU, 260.0, 650.0)
            if udg_Strain_KnockCount < 64 then
                set udg_Strain_KnockUnit[udg_Strain_KnockCount] = enumU
                set udg_Strain_KnockTimer[udg_Strain_KnockCount] = 0.75
                set udg_Strain_KnockCount = udg_Strain_KnockCount + 1
            endif
        endif
    endloop
    set enumU = null
endfunction

function Strain_ClearCurrentGene takes unit u, integer pId returns nothing
    if u != null then
        call UnitRemoveAbility(u, 'A025')
        call UnitRemoveAbility(u, 'A026')
        if udg_Strain_StolenHeroAbil[pId] != 0 then
            call UnitRemoveAbility(u, udg_Strain_StolenHeroAbil[pId])
        endif
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))
        call SetUnitScale(u, 1.25, 1.25, 1.25)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 3.0, "|cffffcc00[异种进化]|r 基因槽已清空，可吸收新种类猎物！")
    endif
    set udg_Strain_GeneCat[pId] = 0
    set udg_Strain_EvoTier[pId] = 0
    set udg_Strain_StolenHeroAbil[pId] = 0
endfunction

function Strain_GetUnitArchetype takes integer uId returns integer
    // Cat 1: 盾卫反射系
    if uId == 'hfoo' or uId == 'hkni' or uId == 'hmil' or uId == 'ogru' or uId == 'otau' or uId == 'ugho' or uId == 'uabo' or uId == 'esen' or uId == 'emtg' or uId == 'ngnv' or uId == 'ngns' or uId == 'nogr' or uId == 'nomg' or uId == 'nftr' or uId == 'nftb' then
        return 1
    endif
    // Cat 2: 剧毒游侠系
    if uId == 'edry' or uId == 'earc' or uId == 'hrif' or uId == 'ohun' or uId == 'owyv' or uId == 'ucry' or uId == 'ugar' or uId == 'echm' or uId == 'nspr' or uId == 'nspg' or uId == 'nass' or uId == 'nmrl' or uId == 'ngna' then
        return 2
    endif
    // Cat 3: 狂暴嗜血系
    if uId == 'oshm' or uId == 'odoc' or uId == 'ospw' or uId == 'eorc' or uId == 'hmpr' or uId == 'hsor' or uId == 'nwlt' or uId == 'nwlg' or uId == 'nfrl' or uId == 'nfrb' then
        return 3
    endif
    // Cat 4: 巨兽雷霆系
    return 4
endfunction

function Strain_ApplyStolenHeroSkill takes unit u, integer pId, integer abilId returns nothing
    if u == null or abilId == 0 then
        return
    endif
    if udg_Strain_StolenHeroAbil[pId] != 0 and udg_Strain_StolenHeroAbil[pId] != abilId then
        call UnitRemoveAbility(u, udg_Strain_StolenHeroAbil[pId])
        set udg_Strain_EvoTier[pId] = 1
    else
        if udg_Strain_GeneCat[pId] != 5 then
            call Strain_ClearCurrentGene(u, pId)
            set udg_Strain_EvoTier[pId] = 1
        else
            set udg_Strain_EvoTier[pId] = udg_Strain_EvoTier[pId] + 1
        endif
    endif
    set udg_Strain_GeneCat[pId] = 5
    set udg_Strain_StolenHeroAbil[pId] = abilId
    call UnitAddAbility(u, abilId)
    call SetUnitAbilityLevel(u, abilId, IMinBJ(3, udg_Strain_EvoTier[pId]))
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
    call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5.0, "|cff00ff00[基因掠夺成功]|r 融合技能：" + GetObjectName(abilId) + " (当前强化阶数：" + I2S(udg_Strain_EvoTier[pId]) + ")")
endfunction

function Strain_ShowHeroSkillDialog takes player p, integer pId returns nothing
    if p == null then
        return
    endif
    call DialogDisplay(p, udg_Strain_HeroDialog, false)
    call DialogClear(udg_Strain_HeroDialog)
    call DialogSetMessage(udg_Strain_HeroDialog, "【基因掠夺】选择掠夺融入的英雄技能：")
    set udg_Strain_HeroSkillBtn[0] = DialogAddButton(udg_Strain_HeroDialog, "[1] " + GetObjectName(udg_Strain_CandidateAbil0[pId]), 49)
    set udg_Strain_HeroSkillBtn[1] = DialogAddButton(udg_Strain_HeroDialog, "[2] " + GetObjectName(udg_Strain_CandidateAbil1[pId]), 50)
    set udg_Strain_HeroSkillBtn[2] = DialogAddButton(udg_Strain_HeroDialog, "[3] " + GetObjectName(udg_Strain_CandidateAbil2[pId]), 51)
    set udg_Strain_HeroSkillBtn[3] = DialogAddButton(udg_Strain_HeroDialog, "[4] " + GetObjectName(udg_Strain_CandidateAbil3[pId]), 52)
    call DialogDisplay(p, udg_Strain_HeroDialog, true)
endfunction

function Strain_OnHeroDialogClick takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer pId = 0
    local unit u = null
    local group g = null
    local unit enumU = null
    if p == null then
        set b = null
        return
    endif
    set pId = GetPlayerId(p)
    set u = udg_Strain_Hero[pId]
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif
    if u == null then
        set g = CreateGroup()
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set enumU = FirstOfGroup(g)
            exitwhen enumU == null
            call GroupRemoveUnit(g, enumU)
            if GetUnitTypeId(enumU) == 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                set u = enumU
                set udg_Strain_Hero[pId] = enumU
                exitwhen true
            endif
        endloop
        call DestroyGroup(g)
        set g = null
    endif
    call DialogDisplay(p, udg_Strain_HeroDialog, false)
    if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) then
        if b == udg_Strain_HeroSkillBtn[0] then
            call Strain_ApplyStolenHeroSkill(u, pId, udg_Strain_CandidateAbil0[pId])
        elseif b == udg_Strain_HeroSkillBtn[1] then
            call Strain_ApplyStolenHeroSkill(u, pId, udg_Strain_CandidateAbil1[pId])
        elseif b == udg_Strain_HeroSkillBtn[2] then
            call Strain_ApplyStolenHeroSkill(u, pId, udg_Strain_CandidateAbil2[pId])
        elseif b == udg_Strain_HeroSkillBtn[3] then
            call Strain_ApplyStolenHeroSkill(u, pId, udg_Strain_CandidateAbil3[pId])
        endif
    endif
    set b = null
    set p = null
    set u = null
endfunction

function Strain_ShowGeneDialog takes player p, integer pId returns nothing
    local string msg = "【异种之源 - 基因掠夺控制台】"
    if p == null then
        return
    endif
    if udg_Strain_GeneCat[pId] == 1 then
        set msg = msg + " - 当前基因：盾卫反射系 (阶数: " + I2S(udg_Strain_EvoTier[pId]) + "/3)"
    elseif udg_Strain_GeneCat[pId] == 2 then
        set msg = msg + " - 当前基因：剧毒游侠系 (阶数: " + I2S(udg_Strain_EvoTier[pId]) + "/3)"
    elseif udg_Strain_GeneCat[pId] == 3 then
        set msg = msg + " - 当前基因：狂暴嗜血系 (阶数: " + I2S(udg_Strain_EvoTier[pId]) + "/3)"
    elseif udg_Strain_GeneCat[pId] == 4 then
        set msg = msg + " - 当前基因：巨兽雷霆系 (阶数: " + I2S(udg_Strain_EvoTier[pId]) + "/3)"
    elseif udg_Strain_GeneCat[pId] == 5 then
        set msg = msg + " - 当前基因：掠夺英雄技能 - " + GetObjectName(udg_Strain_StolenHeroAbil[pId]) + " (阶数: " + I2S(udg_Strain_EvoTier[pId]) + "/3)"
    else
        set msg = msg + " - 当前基因槽：空（吞噬不同猎物可解锁对应基因）"
    endif
    call DialogDisplay(p, udg_Strain_GeneDialog, false)
    call DialogClear(udg_Strain_GeneDialog)
    call DialogSetMessage(udg_Strain_GeneDialog, msg)
    set udg_Strain_BtnKeep = DialogAddButton(udg_Strain_GeneDialog, "[1] 保留当前基因（继续吞噬同类可叠层进化）", 49)
    set udg_Strain_BtnDiscard = DialogAddButton(udg_Strain_GeneDialog, "[2] 舍弃当前基因（清空基因槽以吸收新种类猎物）", 50)
    call DialogDisplay(p, udg_Strain_GeneDialog, true)
endfunction

function Strain_OnGeneDialogClick takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer pId = 0
    local unit u = null
    local group g = null
    local unit enumU = null
    if p == null then
        set b = null
        return
    endif
    set pId = GetPlayerId(p)
    set u = udg_Strain_Hero[pId]
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif
    if u == null then
        set g = CreateGroup()
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set enumU = FirstOfGroup(g)
            exitwhen enumU == null
            call GroupRemoveUnit(g, enumU)
            if GetUnitTypeId(enumU) == 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                set u = enumU
                set udg_Strain_Hero[pId] = enumU
                exitwhen true
            endif
        endloop
        call DestroyGroup(g)
        set g = null
    endif
    call DialogDisplay(p, udg_Strain_GeneDialog, false)
    if b == udg_Strain_BtnDiscard then
        if u != null then
            call Strain_ClearCurrentGene(u, pId)
        endif
    endif
    set b = null
    set p = null
    set u = null
endfunction

function Strain_OnDigestComplete takes unit u, integer pId returns nothing
    local integer cat = 0
    local integer tier = 0
    local integer tgtType = 0
    if u == null then
        return
    endif
    set tgtType = udg_Strain_DigestType[pId]

    if udg_Strain_DigestIsHero[pId] then
        // Apex Harvest: Hero Devoured!
        call SetHeroAgi(u, GetHeroAgi(u, false) + 4, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff00ff00[顶端掠食]|r 成功吞噬敌方英雄，永久夺取 +4 点敏捷！")

        if tgtType == 'H002' then
            set udg_Strain_CandidateAbil0[pId] = 'A001'
            set udg_Strain_CandidateAbil1[pId] = 'A002'
            set udg_Strain_CandidateAbil2[pId] = 'A003'
            set udg_Strain_CandidateAbil3[pId] = 'A004'
        elseif tgtType == 'H003' then
            set udg_Strain_CandidateAbil0[pId] = 'A011'
            set udg_Strain_CandidateAbil1[pId] = 'A012'
            set udg_Strain_CandidateAbil2[pId] = 'A013'
            set udg_Strain_CandidateAbil3[pId] = 'A014'
        elseif tgtType == 'Hamg' then
            set udg_Strain_CandidateAbil0[pId] = 'AHbz'
            set udg_Strain_CandidateAbil1[pId] = 'AHwe'
            set udg_Strain_CandidateAbil2[pId] = 'AHab'
            set udg_Strain_CandidateAbil3[pId] = 'AHmt'
        elseif tgtType == 'Hmkg' then
            set udg_Strain_CandidateAbil0[pId] = 'AHtb'
            set udg_Strain_CandidateAbil1[pId] = 'AHtc'
            set udg_Strain_CandidateAbil2[pId] = 'AHbh'
            set udg_Strain_CandidateAbil3[pId] = 'AHav'
        elseif tgtType == 'Hpal' then
            set udg_Strain_CandidateAbil0[pId] = 'AHhb'
            set udg_Strain_CandidateAbil1[pId] = 'AHds'
            set udg_Strain_CandidateAbil2[pId] = 'AHad'
            set udg_Strain_CandidateAbil3[pId] = 'AHre'
        elseif tgtType == 'Hblm' then
            set udg_Strain_CandidateAbil0[pId] = 'AHfs'
            set udg_Strain_CandidateAbil1[pId] = 'AHbn'
            set udg_Strain_CandidateAbil2[pId] = 'AHdr'
            set udg_Strain_CandidateAbil3[pId] = 'AHpx'
        elseif tgtType == 'Obla' then
            set udg_Strain_CandidateAbil0[pId] = 'AOwk'
            set udg_Strain_CandidateAbil1[pId] = 'AOmi'
            set udg_Strain_CandidateAbil2[pId] = 'AOcr'
            set udg_Strain_CandidateAbil3[pId] = 'AOww'
        elseif tgtType == 'Ofar' then
            set udg_Strain_CandidateAbil0[pId] = 'AOcl'
            set udg_Strain_CandidateAbil1[pId] = 'AOfs'
            set udg_Strain_CandidateAbil2[pId] = 'AOsf'
            set udg_Strain_CandidateAbil3[pId] = 'AOeq'
        elseif tgtType == 'Otch' then
            set udg_Strain_CandidateAbil0[pId] = 'AOsh'
            set udg_Strain_CandidateAbil1[pId] = 'AOws'
            set udg_Strain_CandidateAbil2[pId] = 'AOae'
            set udg_Strain_CandidateAbil3[pId] = 'AOre'
        elseif tgtType == 'Oshd' then
            set udg_Strain_CandidateAbil0[pId] = 'AOhw'
            set udg_Strain_CandidateAbil1[pId] = 'AOhx'
            set udg_Strain_CandidateAbil2[pId] = 'AOsw'
            set udg_Strain_CandidateAbil3[pId] = 'AOvd'
        elseif tgtType == 'Edem' then
            set udg_Strain_CandidateAbil0[pId] = 'AEmb'
            set udg_Strain_CandidateAbil1[pId] = 'AEim'
            set udg_Strain_CandidateAbil2[pId] = 'AEev'
            set udg_Strain_CandidateAbil3[pId] = 'AEme'
        elseif tgtType == 'Ekee' then
            set udg_Strain_CandidateAbil0[pId] = 'AEer'
            set udg_Strain_CandidateAbil1[pId] = 'AEfn'
            set udg_Strain_CandidateAbil2[pId] = 'AEah'
            set udg_Strain_CandidateAbil3[pId] = 'AEtq'
        elseif tgtType == 'Emoo' then
            set udg_Strain_CandidateAbil0[pId] = 'AHfa'
            set udg_Strain_CandidateAbil1[pId] = 'AEst'
            set udg_Strain_CandidateAbil2[pId] = 'AEar'
            set udg_Strain_CandidateAbil3[pId] = 'AEsf'
        elseif tgtType == 'Ewar' then
            set udg_Strain_CandidateAbil0[pId] = 'AEfk'
            set udg_Strain_CandidateAbil1[pId] = 'AEbl'
            set udg_Strain_CandidateAbil2[pId] = 'AEsh'
            set udg_Strain_CandidateAbil3[pId] = 'AEsv'
        elseif tgtType == 'Udea' then
            set udg_Strain_CandidateAbil0[pId] = 'AUdc'
            set udg_Strain_CandidateAbil1[pId] = 'AUdp'
            set udg_Strain_CandidateAbil2[pId] = 'AUau'
            set udg_Strain_CandidateAbil3[pId] = 'AUan'
        elseif tgtType == 'Ulic' then
            set udg_Strain_CandidateAbil0[pId] = 'AUfn'
            set udg_Strain_CandidateAbil1[pId] = 'AUfu'
            set udg_Strain_CandidateAbil2[pId] = 'AUdr'
            set udg_Strain_CandidateAbil3[pId] = 'AUdd'
        elseif tgtType == 'Udre' then
            set udg_Strain_CandidateAbil0[pId] = 'AUcs'
            set udg_Strain_CandidateAbil1[pId] = 'AUsl'
            set udg_Strain_CandidateAbil2[pId] = 'AUva'
            set udg_Strain_CandidateAbil3[pId] = 'AUin'
        else
            set udg_Strain_CandidateAbil0[pId] = 'AUim'
            set udg_Strain_CandidateAbil1[pId] = 'AUts'
            set udg_Strain_CandidateAbil2[pId] = 'AUcb'
            set udg_Strain_CandidateAbil3[pId] = 'AUls'
        endif

        if GetPlayerController(GetOwningPlayer(u)) == MAP_CONTROL_USER then
            call Strain_ShowHeroSkillDialog(GetOwningPlayer(u), pId)
        else
            call Strain_ApplyStolenHeroSkill(u, pId, udg_Strain_CandidateAbil0[pId])
        endif
    else
        // Normal Unit / Creep Devoured
        set cat = Strain_GetUnitArchetype(tgtType)
        if udg_Strain_GeneCat[pId] == 0 or udg_Strain_GeneCat[pId] == cat then
            set udg_Strain_GeneCat[pId] = cat
            if udg_Strain_EvoTier[pId] < 3 then
                set udg_Strain_EvoTier[pId] = udg_Strain_EvoTier[pId] + 1
            endif
            set tier = udg_Strain_EvoTier[pId]

            if cat == 1 then
                // Cat 1: 盾卫系
                if GetUnitAbilityLevel(u, 'A025') == 0 then
                    call UnitAddAbility(u, 'A025')
                endif
                call SetUnitAbilityLevel(u, 'A025', tier)
                if tier >= 2 then
                    call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 65.0)
                endif
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Defend\\\\DefendCaster.mdl", u, "origin"))
            elseif cat == 2 then
                // Cat 2: 剧毒系
                if GetUnitAbilityLevel(u, 'A026') == 0 then
                    call UnitAddAbility(u, 'A026')
                endif
                call SetUnitAbilityLevel(u, 'A026', tier)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Weapons\\\\PoisonSting\\\\PoisonStingTarget.mdl", u, "origin"))
            elseif cat == 3 then
                // Cat 3: 嗜血系
                if tier >= 2 then
                    call SetUnitScale(u, 1.45, 1.45, 1.45)
                    call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 60.0)
                endif
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Bloodlust\\\\BloodlustTarget.mdl", u, "origin"))
            elseif cat == 4 then
                // Cat 4: 雷霆系
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\Monsoon\\\\MonsoonBoltTarget.mdl", u, "origin"))
            endif

            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff00ff00[异种进化]|r 猎物基因已吸收融合！当前阶数：" + I2S(tier) + " 阶")
        else
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5.0, "|cffffcc00[基因冲突]|r 当前已激活其他种类基因！按R打开面板可随时舍弃当前基因以切换种类。")
        endif
    endif
endfunction
"""

target_stealth_loop = "function DM_StealthLoop takes nothing returns nothing"
assert target_stealth_loop in content, "target_stealth_loop not found"
content = content.replace(target_stealth_loop, strain_core_funcs + "\n" + target_stealth_loop, 1)

# 3. Replace DM_StealthLoop
new_stealth_loop = """function DM_StealthLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local player p = null
    local unit dummy = null
    local integer hIdx = -1
    local boolean hasAgh = false
    local integer lv = 1
    local real dur = 30.0
    local unit enumU = null
    local integer pId = 0

    // 1. Process pending stealth queue
    set i = 0
    loop
        exitwhen i >= udg_DM_StealthCount
        set udg_DM_StealthTimer[i] = udg_DM_StealthTimer[i] - 0.05
        if udg_DM_StealthTimer[i] <= 0.0 then
            set u = udg_DM_StealthUnit[i]
            set udg_DM_StealthUnit[i] = udg_DM_StealthUnit[udg_DM_StealthCount - 1]
            set udg_DM_StealthTimer[i] = udg_DM_StealthTimer[udg_DM_StealthCount - 1]
            set udg_DM_StealthUnit[udg_DM_StealthCount - 1] = null
            set udg_DM_StealthCount = udg_DM_StealthCount - 1
            set i = i - 1

            if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) then
                set p = GetOwningPlayer(u)
                set dummy = CreateUnit(p, 'u000', GetUnitX(u), GetUnitY(u), 0.0)
                call UnitAddAbility(dummy, 'A00V')
                call IssueTargetOrder(dummy, "invisibility", u)
                call UnitApplyTimedLife(dummy, 'BTLF', 1.0)
                set dummy = null
                set p = null

                call SetUnitVertexColor(u, 130, 150, 255, 120)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\WindWalk\\\\WindWalkTarget.mdl", u, "origin"))

                set hIdx = DM_GetHeroIndex(u)
                set hasAgh = GetUnitAbilityLevel(u, 'A004') > 0
                set lv = GetUnitAbilityLevel(u, 'A001')
                set dur = 30.0 + I2R(lv) * 5.0

                if hasAgh then
                    call SetUnitMoveSpeed(u, 522.0)
                else
                    call SetUnitMoveSpeed(u, 400.0)
                endif

                if hIdx >= 0 then
                    set udg_DM_InStealth[hIdx] = true
                    set udg_DM_Backstab[hIdx] = true
                    set udg_DM_StealthDuration[hIdx] = dur
                endif
            endif
            set u = null
        endif
        set i = i + 1
    endloop

    // 2. Check active stealth duration
    set i = 0
    loop
        exitwhen i >= udg_DM_HeroCount
        if udg_DM_InStealth[i] then
            set udg_DM_StealthDuration[i] = udg_DM_StealthDuration[i] - 0.05
            if udg_DM_StealthDuration[i] <= 0.0 or IsUnitType(udg_DM_Hero[i], UNIT_TYPE_DEAD) then
                call DM_BreakInvisibility(udg_DM_Hero[i], null)
            endif
        endif
        set i = i + 1
    endloop

    // 3. Process Ninja pending heal
    set i = 0
    loop
        exitwhen i >= udg_Ninja_PendingCount
        if udg_Ninja_PendingHealUnit[i] != null and not IsUnitType(udg_Ninja_PendingHealUnit[i], UNIT_TYPE_DEAD) then
            call SetWidgetLife(udg_Ninja_PendingHealUnit[i], udg_Ninja_PendingHealHP[i])
        endif
        set udg_Ninja_PendingHealUnit[i] = null
        set i = i + 1
    endloop
    set udg_Ninja_PendingCount = 0

    // 4. Hero #3 Knockup Timer Loop
    set i = 0
    loop
        exitwhen i >= udg_Strain_KnockCount
        set udg_Strain_KnockTimer[i] = udg_Strain_KnockTimer[i] - 0.05
        set enumU = udg_Strain_KnockUnit[i]
        if enumU == null or IsUnitType(enumU, UNIT_TYPE_DEAD) or udg_Strain_KnockTimer[i] <= 0.0 then
            if enumU != null and not IsUnitType(enumU, UNIT_TYPE_DEAD) then
                call SetUnitFlyHeight(enumU, GetUnitDefaultFlyHeight(enumU), 750.0)
            endif
            set udg_Strain_KnockUnit[i] = udg_Strain_KnockUnit[udg_Strain_KnockCount - 1]
            set udg_Strain_KnockTimer[i] = udg_Strain_KnockTimer[udg_Strain_KnockCount - 1]
            set udg_Strain_KnockUnit[udg_Strain_KnockCount - 1] = null
            set udg_Strain_KnockCount = udg_Strain_KnockCount - 1
            set i = i - 1
        elseif udg_Strain_KnockTimer[i] <= 0.36 and udg_Strain_KnockTimer[i] >= 0.30 then
            call SetUnitFlyHeight(enumU, GetUnitDefaultFlyHeight(enumU), 750.0)
        endif
        set enumU = null
        set i = i + 1
    endloop

    // 5. Hero #3 Burrow Movement & Dust Loop
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_Burrowed[pId] then
            set u = udg_Strain_Hero[pId]
            if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
                set udg_Strain_Burrowed[pId] = false
                set udg_Strain_BurrowTimer[pId] = 0.0
            else
                set udg_Strain_BurrowTimer[pId] = udg_Strain_BurrowTimer[pId] - 0.05
                call SetUnitMoveSpeed(u, 522.0)
                if (R2I(udg_Strain_BurrowTimer[pId] * 20.0) - (R2I(udg_Strain_BurrowTimer[pId] * 20.0) / 6) * 6) == 0 then
                    call DestroyEffect(AddSpecialEffect("Objects\\\\Spawnmodels\\\\Undead\\\\ImpaleTargetDust\\\\ImpaleTargetDust.mdl", GetUnitX(u), GetUnitY(u)))
                endif
                if udg_Strain_BurrowTimer[pId] <= 0.0 then
                    call Strain_Unburrow(u, pId)
                endif
            endif
            set u = null
        endif
        set pId = pId + 1
    endloop

    // 6. Hero #3 Mimicry Actor Position Sync Loop
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_MimicActive[pId] then
            set u = udg_Strain_Hero[pId]
            set enumU = udg_Strain_MimicActor[pId]
            if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
                call Strain_BreakMimicry(u, pId)
            elseif enumU != null and not IsUnitType(enumU, UNIT_TYPE_DEAD) then
                call SetUnitX(enumU, GetUnitX(u))
                call SetUnitY(enumU, GetUnitY(u))
                call SetUnitFacing(enumU, GetUnitFacing(u))
            endif
            set u = null
            set enumU = null
        endif
        set pId = pId + 1
    endloop
endfunction"""
content = replace_func(content, 'DM_StealthLoop', new_stealth_loop)

# 4. Insert AI_LearnSkillForStrain before AI_AutoLearnSkills
strain_learn_func = """function AI_LearnSkillForStrain takes unit h returns boolean
    local integer hLv = GetHeroLevel(h)
    local integer qLv = GetUnitAbilityLevel(h, 'A021')
    local integer wLv = GetUnitAbilityLevel(h, 'A022')
    local integer eLv = GetUnitAbilityLevel(h, 'A023')
    local integer rLv = GetUnitAbilityLevel(h, 'A024')

    if rLv == 0 then
        call UnitAddAbility(h, 'A024')
    endif

    // 1. Primary skill Q (A021) at Lv 1, 3, 5
    if qLv < 3 and hLv >= (qLv * 2 + 1) then
        if not (hLv == 2 and wLv == 0) and not (hLv == 4 and eLv == 0) then
            return AI_ForceLearnSkill(h, 'A021', 3, false)
        endif
    endif

    // 2. Learn unlearned basic skills (W at Lv 2, E at Lv 4)
    if wLv == 0 then
        return AI_ForceLearnSkill(h, 'A022', 3, false)
    endif
    if eLv == 0 then
        return AI_ForceLearnSkill(h, 'A023', 3, false)
    endif

    // 3. Max Q
    if qLv < 3 and hLv >= (qLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A021', 3, false)
    endif

    // 4. Max W
    if wLv < 3 and hLv >= (wLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A022', 3, false)
    endif

    // 5. Max E
    if eLv < 3 and hLv >= (eLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A023', 3, false)
    endif

    // 6. Stat bonus
    return AI_ForceLearnSkill(h, 'Aamk', 10, false)
endfunction
"""

target_auto_learn_decl = "function AI_AutoLearnSkills takes unit h returns nothing"
assert target_auto_learn_decl in content, "target_auto_learn_decl not found"
content = content.replace(target_auto_learn_decl, strain_learn_func + "\n" + target_auto_learn_decl, 1)

# 5. Replace AI_AutoLearnSkills
new_auto_learn = """function AI_AutoLearnSkills takes unit h returns nothing
    local integer uId = 0
    local boolean learned = false

    if h == null or IsUnitType(h, UNIT_TYPE_DEAD) then
        return
    endif
    set uId = GetUnitTypeId(h)
    if GetHeroSkillPoints(h) <= 0 then
        return
    endif

    loop
        exitwhen GetHeroSkillPoints(h) <= 0
        set learned = false
        if uId == 'H002' then
            set learned = AI_LearnSkillForDreamMaster(h)
        elseif uId == 'H003' then
            set learned = AI_LearnSkillForNinja(h)
        elseif uId == 'H004' then
            set learned = AI_LearnSkillForStrain(h)
        endif
        if not learned then
            exitwhen true
        endif
    endloop
endfunction"""
content = replace_func(content, 'AI_AutoLearnSkills', new_auto_learn)

# 6. Replace AI_SpawnCustomHeroForPlayer
new_spawn_hero = """function AI_SpawnCustomHeroForPlayer takes integer pId, real x, real y, real facing returns unit
    local integer hTypeId = 'H002'
    local unit h = null
    if udg_AI_HeroMode[pId] == 2 then
        set hTypeId = 'H003'
    elseif udg_AI_HeroMode[pId] == 3 then
        set hTypeId = 'H004'
    endif
    set h = CreateUnit(Player(pId), hTypeId, x, y, facing)
    call RemoveGuardPosition(h)
    set udg_AI_CustomHero[pId] = h
    set udg_AI_HeroSpawned[pId] = true
    set udg_AI_DeadTimer[pId] = 0.0
    set udg_AI_AltarTimer[pId] = 0.0
    set udg_AI_WaitTimer[pId] = 0.0
    set udg_AI_CastCD_Q[pId] = 0.0
    set udg_AI_CastCD_W[pId] = 0.0
    set udg_AI_CastCD_E[pId] = 0.0
    set udg_AI_CastCD_R[pId] = 0.0

    call UnitAddItemById(h, 'stwp')

    if hTypeId == 'H003' then
        set udg_Ninja_TrueHero[pId] = h
    elseif hTypeId == 'H004' then
        set udg_Strain_Hero[pId] = h
        call Strain_InitHero(h)
    endif

    call AI_AutoLearnSkills(h)

    call SetPlayerTechMaxAllowed(Player(pId), 'H002', 1)
    call SetPlayerTechMaxAllowed(Player(pId), 'H003', 1)
    call SetPlayerTechMaxAllowed(Player(pId), 'H004', 1)

    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\MassTeleport\\\\MassTeleportTarget.mdl", h, "origin"))

    return h
endfunction"""
content = replace_func(content, 'AI_SpawnCustomHeroForPlayer', new_spawn_hero)

# 7 & 8. Replace AI_TacticalLoop
new_tactical_loop = """function AI_TacticalLoop takes nothing returns nothing
    local integer i = 0
    local unit h = null
    local integer hTypeId = 0
    local real hx = 0.0
    local real hy = 0.0
    local integer enemyCount = 0
    local unit bestEnemy = null
    local boolean bestIsHero = false
    local real bestLife = 0.0
    local unit clusterEnemy = null
    local unit nearestEnemy = null
    local real minD = 99999999.0
    local real dx = 0.0
    local real dy = 0.0
    local real d = 0.0
    local unit enumU = null
    local group g = null
    local unit altar = null
    local unit th = null
    local integer curOrder = 0
    local boolean doCommand = false

    set udg_AI_CommandTick = udg_AI_CommandTick + 1
    if udg_AI_CommandTick >= 4 then
        set udg_AI_CommandTick = 0
        set doCommand = true
    endif

    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] > 0 then
                // Decrement Cooldowns
                if udg_AI_CastCD_Q[i] > 0.0 then
                    set udg_AI_CastCD_Q[i] = udg_AI_CastCD_Q[i] - 1.0
                endif
                if udg_AI_CastCD_W[i] > 0.0 then
                    set udg_AI_CastCD_W[i] = udg_AI_CastCD_W[i] - 1.0
                endif
                if udg_AI_CastCD_E[i] > 0.0 then
                    set udg_AI_CastCD_E[i] = udg_AI_CastCD_E[i] - 1.0
                endif
                if udg_AI_CastCD_R[i] > 0.0 then
                    set udg_AI_CastCD_R[i] = udg_AI_CastCD_R[i] - 1.0
                endif

                // 1. Check if custom hero needs to be spawned / replaced
                if not udg_AI_HeroSpawned[i] then
                    // Case 1: Check if standard hero exists to replace
                    set g = CreateGroup()
                    call GroupEnumUnitsOfPlayer(g, Player(i), null)
                    loop
                        set enumU = FirstOfGroup(g)
                        exitwhen enumU == null
                        call GroupRemoveUnit(g, enumU)
                        if IsUnitType(enumU, UNIT_TYPE_HERO) and GetUnitTypeId(enumU) != 'H002' and GetUnitTypeId(enumU) != 'H003' and GetUnitTypeId(enumU) != 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                            set hx = GetUnitX(enumU)
                            set hy = GetUnitY(enumU)
                            set d = GetUnitFacing(enumU)
                            call RemoveUnit(enumU)
                            call AI_SpawnCustomHeroForPlayer(i, hx, hy, d)
                            call GroupClear(g)
                        endif
                    endloop
                    call DestroyGroup(g)
                    set g = null

                    // Case 2: Check altar or townhall timing fallback
                    if not udg_AI_HeroSpawned[i] then
                        set altar = AI_GetPlayerAltar(Player(i))
                        if altar != null then
                            set udg_AI_AltarTimer[i] = udg_AI_AltarTimer[i] + 1.0
                            if udg_AI_AltarTimer[i] >= 20.0 then
                                call AI_SpawnCustomHeroForPlayer(i, GetUnitX(altar), GetUnitY(altar) - 150.0, 270.0)
                            endif
                        else
                            set udg_AI_WaitTimer[i] = udg_AI_WaitTimer[i] + 1.0
                            if udg_AI_WaitTimer[i] >= 60.0 then
                                set th = AI_GetPlayerTownHall(Player(i))
                                if th != null then
                                    call AI_SpawnCustomHeroForPlayer(i, GetUnitX(th) + 150.0, GetUnitY(th), 270.0)
                                else
                                    call AI_SpawnCustomHeroForPlayer(i, GetStartLocationX(GetPlayerStartLocation(Player(i))), GetStartLocationY(GetPlayerStartLocation(Player(i))), 270.0)
                                endif
                                set th = null
                            endif
                        endif
                        set altar = null
                    endif
                endif

                // 2. Check if hero is dead & manage revival
                set h = udg_AI_CustomHero[i]
                if h != null and (IsUnitType(h, UNIT_TYPE_DEAD) or GetWidgetLife(h) <= 0.405) then
                    set udg_AI_DeadTimer[i] = udg_AI_DeadTimer[i] + 1.0
                    set altar = AI_GetPlayerAltar(Player(i))
                    if altar != null then
                        if udg_AI_DeadTimer[i] >= 25.0 then
                            call ReviveHero(h, GetUnitX(altar), GetUnitY(altar) - 150.0, true)
                            set udg_AI_DeadTimer[i] = 0.0
                            call AI_AutoLearnSkills(h)
                        endif
                    else
                        if udg_AI_DeadTimer[i] >= 35.0 then
                            call ReviveHero(h, GetStartLocationX(GetPlayerStartLocation(Player(i))), GetStartLocationY(GetPlayerStartLocation(Player(i))), true)
                            set udg_AI_DeadTimer[i] = 0.0
                            call AI_AutoLearnSkills(h)
                        endif
                    endif
                    set altar = null
                endif

                // 3. Tactical combat decisions when hero is alive
                if h != null and not IsUnitType(h, UNIT_TYPE_DEAD) and GetWidgetLife(h) > 0.405 then
                    set hTypeId = GetUnitTypeId(h)
                    set hx = GetUnitX(h)
                    set hy = GetUnitY(h)
                    set enemyCount = 0
                    set bestEnemy = null
                    set bestIsHero = false
                    set bestLife = 0.0
                    set clusterEnemy = null
                    set nearestEnemy = null
                    set minD = 99999999.0

                    call AI_AutoLearnSkills(h)

                    // Scan for enemies in combat range (800.0)
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 800.0, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, Player(i)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                            set enemyCount = enemyCount + 1
                            set dx = GetUnitX(enumU) - hx
                            set dy = GetUnitY(enumU) - hy
                            set d = SquareRoot(dx * dx + dy * dy)
                            if d < minD then
                                set minD = d
                                set nearestEnemy = enumU
                            endif

                            if clusterEnemy == null and d <= 600.0 then
                                set clusterEnemy = enumU
                            endif

                            if bestEnemy == null then
                                set bestEnemy = enumU
                                set bestIsHero = IsUnitType(enumU, UNIT_TYPE_HERO)
                                set bestLife = GetUnitState(enumU, UNIT_STATE_MAX_LIFE)
                            else
                                if IsUnitType(enumU, UNIT_TYPE_HERO) and not bestIsHero then
                                    set bestEnemy = enumU
                                    set bestIsHero = true
                                    set bestLife = GetUnitState(enumU, UNIT_STATE_MAX_LIFE)
                                elseif (IsUnitType(enumU, UNIT_TYPE_HERO) == bestIsHero) and (GetUnitState(enumU, UNIT_STATE_MAX_LIFE) > bestLife) then
                                    set bestEnemy = enumU
                                    set bestLife = GetUnitState(enumU, UNIT_STATE_MAX_LIFE)
                                endif
                            endif
                        endif
                    endloop

                    if hTypeId == 'H002' then
                        // Dream Master Tactical Brain
                        // Cast E: A003 Mass Illusion
                        if GetUnitAbilityLevel(h, 'A003') > 0 and udg_AI_CastCD_E[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 80.0 and clusterEnemy != null then
                            call IssuePointOrder(h, "cloudoffog", GetUnitX(clusterEnemy), GetUnitY(clusterEnemy))
                            set udg_AI_CastCD_E[i] = 14.0
                        endif

                        // Cast W: A002 Possession
                        if GetUnitAbilityLevel(h, 'A002') > 0 and udg_AI_CastCD_W[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 70.0 and bestEnemy != null then
                            call IssueTargetOrder(h, "charm", bestEnemy)
                            set udg_AI_CastCD_W[i] = 18.0
                        endif

                        // Cast Q: A001 Mirror Image
                        if GetUnitAbilityLevel(h, 'A001') > 0 and udg_AI_CastCD_Q[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 100.0 and (enemyCount >= 1 or GetWidgetLife(h) < GetUnitState(h, UNIT_STATE_MAX_LIFE) * 0.75) then
                            call IssueImmediateOrder(h, "mirrorimage")
                            set udg_AI_CastCD_Q[i] = 16.0
                        endif

                        // Command nearby clones to fight
                        if nearestEnemy != null then
                            call GroupClear(udg_EnumGroup)
                            call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 1000.0, null)
                            loop
                                set enumU = FirstOfGroup(udg_EnumGroup)
                                exitwhen enumU == null
                                call GroupRemoveUnit(udg_EnumGroup, enumU)
                                if GetOwningPlayer(enumU) == Player(i) and enumU != h and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 then
                                    if IsUnitType(enumU, UNIT_TYPE_SUMMONED) or IsUnitIllusion(enumU) or IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                                        set curOrder = GetUnitCurrentOrder(enumU)
                                        if curOrder == 0 or curOrder == 851972 or curOrder == 851973 then
                                            call IssuePointOrder(enumU, "attack", GetUnitX(nearestEnemy), GetUnitY(nearestEnemy))
                                        endif
                                    endif
                                endif
                            endloop
                        endif

                    elseif hTypeId == 'H003' then
                        // Ninja Tactical Brain
                        if GetUnitAbilityLevel(h, 'A012') > 0 and not udg_Ninja_AuraOn[i] then
                            set udg_Ninja_AuraOn[i] = true
                            if udg_Ninja_AuraFx[i] == null then
                                set udg_Ninja_AuraFx[i] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", h, "origin")
                            endif
                        endif

                        // Cast R: A014
                        if GetUnitAbilityLevel(h, 'A014') > 0 and udg_AI_CastCD_R[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 120.0 and enemyCount >= 1 then
                            call IssueImmediateOrder(h, "summongrizzly")
                            set udg_AI_CastCD_R[i] = 60.0
                        endif

                        // Command nearby ninja clones to fight
                        if nearestEnemy != null then
                            call GroupClear(udg_EnumGroup)
                            call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 1000.0, null)
                            loop
                                set enumU = FirstOfGroup(udg_EnumGroup)
                                exitwhen enumU == null
                                call GroupRemoveUnit(udg_EnumGroup, enumU)
                                if GetOwningPlayer(enumU) == Player(i) and enumU != h and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 then
                                    if GetUnitTypeId(enumU) == 'u002' or GetUnitTypeId(enumU) == 'u001' or IsUnitType(enumU, UNIT_TYPE_SUMMONED) then
                                        set curOrder = GetUnitCurrentOrder(enumU)
                                        if curOrder == 0 or curOrder == 851972 or curOrder == 851973 then
                                            call IssuePointOrder(enumU, "attack", GetUnitX(nearestEnemy), GetUnitY(nearestEnemy))
                                        endif
                                    endif
                                endif
                            endloop
                        endif

                    elseif hTypeId == 'H004' then
                        // Hero #3 Primordial Strain Tactical Brain
                        // 1. If burrowed and enemy is close: unburrow to knockup and strike!
                        if udg_Strain_Burrowed[i] then
                            if nearestEnemy != null and minD <= 220.0 then
                                call IssueImmediateOrder(h, "windwalk")
                            endif
                        else
                            // 2. Cast W (A022 捕食吞噬) on low-HP target
                            if udg_AI_CastCD_W[i] <= 0.0 and GetUnitAbilityLevel(h, 'A022') > 0 and udg_Strain_DigestTimer[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 75.0 then
                                call GroupClear(udg_EnumGroup)
                                call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 300.0, null)
                                loop
                                    set enumU = FirstOfGroup(udg_EnumGroup)
                                    exitwhen enumU == null
                                    call GroupRemoveUnit(udg_EnumGroup, enumU)
                                    if IsUnitEnemy(enumU, Player(i)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                                        if IsUnitType(enumU, UNIT_TYPE_HERO) or IsHeroUnitId(GetUnitTypeId(enumU)) then
                                            if GetWidgetLife(enumU) <= (GetUnitState(enumU, UNIT_STATE_MAX_LIFE) * 0.28) then
                                                set bestEnemy = enumU
                                                exitwhen true
                                            endif
                                        else
                                            if GetWidgetLife(enumU) <= (GetUnitState(enumU, UNIT_STATE_MAX_LIFE) * 0.35) then
                                                set bestEnemy = enumU
                                            endif
                                        endif
                                    endif
                                endloop
                                if bestEnemy != null then
                                    call IssueTargetOrder(h, "devour", bestEnemy)
                                    set udg_AI_CastCD_W[i] = 8.0
                                endif
                            endif

                            // 3. Cast Q (A021 渊潜掠影) in combat or when low HP
                            if udg_AI_CastCD_Q[i] <= 0.0 and GetUnitAbilityLevel(h, 'A021') > 0 and GetUnitState(h, UNIT_STATE_MANA) >= 50.0 and (enemyCount >= 1 or GetWidgetLife(h) < (GetUnitState(h, UNIT_STATE_MAX_LIFE) * 0.50)) then
                                call IssueImmediateOrder(h, "windwalk")
                                set udg_AI_CastCD_Q[i] = 12.0
                            endif

                            // 4. Cast E (A023 拟态伪装) when out of combat to prepare ambush
                            if udg_AI_CastCD_E[i] <= 0.0 and GetUnitAbilityLevel(h, 'A023') > 0 and not udg_Strain_MimicActive[i] and udg_Strain_MimicType[i] != 0 and enemyCount == 0 then
                                call IssueImmediateOrder(h, "berserk")
                                set udg_AI_CastCD_E[i] = 20.0
                            endif

                            // 5. Cast Stolen Hero Ability (Cat 5)
                            if udg_Strain_GeneCat[i] == 5 and udg_Strain_StolenHeroAbil[i] != 0 and udg_AI_CastCD_R[i] <= 0.0 and enemyCount >= 1 and nearestEnemy != null then
                                if udg_Strain_StolenHeroAbil[i] == 'AOwk' then
                                    call IssueImmediateOrder(h, "windwalk")
                                elseif udg_Strain_StolenHeroAbil[i] == 'AHtb' then
                                    call IssueTargetOrder(h, "thunderbolt", nearestEnemy)
                                elseif udg_Strain_StolenHeroAbil[i] == 'AHtc' then
                                    call IssueImmediateOrder(h, "stomp")
                                elseif udg_Strain_StolenHeroAbil[i] == 'AOcl' then
                                    call IssueTargetOrder(h, "chainlightning", nearestEnemy)
                                elseif udg_Strain_StolenHeroAbil[i] == 'AUdc' then
                                    call IssueTargetOrder(h, "deathcoil", nearestEnemy)
                                elseif udg_Strain_StolenHeroAbil[i] == 'AUim' then
                                    call IssuePointOrder(h, "impale", GetUnitX(nearestEnemy), GetUnitY(nearestEnemy))
                                elseif udg_Strain_StolenHeroAbil[i] == 'A001' then
                                    call IssueImmediateOrder(h, "mirrorimage")
                                elseif udg_Strain_StolenHeroAbil[i] == 'A014' then
                                    call IssueImmediateOrder(h, "summongrizzly")
                                endif
                                set udg_AI_CastCD_R[i] = 8.0
                            endif
                        endif
                    endif

                    set h = null
                    set bestEnemy = null
                    set clusterEnemy = null
                    set nearestEnemy = null
                endif

                // 4. Strategic Army Commander (Every 4.0 seconds)
                if doCommand then
                    call AI_CommandArmyForPlayer(i)
                endif
            endif
        endif
        set i = i + 1
    endloop
endfunction"""
content = replace_func(content, 'AI_TacticalLoop', new_tactical_loop)

# 9. Replace DM_CapTimerLoop
new_cap_timer = """function DM_CapTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local integer pId = 0
    local unit th = null
    local unit dmgSrc = null
    local integer aLv = 0
    local real pct = 0.0
    local real drain = 0.0
    local real curHP = 0.0
    local unit enumU = null
    local integer kLv = 0
    local player ko = null

    // 1. Process Dream Master possession duration
    loop
        exitwhen i >= udg_CapCount
        set udg_CapDuration[i] = udg_CapDuration[i] - 1.0
        set u = udg_CapUnit[i]
        if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
            if u != null and udg_CapOrigOwner[i] != null then
                call SetUnitOwner(u, udg_CapOrigOwner[i], true)
            endif
            call DM_RemoveCapIndex(i)
            set i = i - 1
        elseif udg_CapDuration[i] <= 0.0 then
            call SetUnitOwner(u, udg_CapOrigOwner[i], true)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", u, "origin"))
            call DM_RemoveCapIndex(i)
            set i = i - 1
        endif
        set u = null
        set i = i + 1
    endloop

    // 2. Process Ninja Aura (A012)
    set pId = 0
    loop
        exitwhen pId > 7
        set th = udg_Ninja_TrueHero[pId]
        if th != null and udg_Ninja_AuraOn[pId] then
            set dmgSrc = null
            if not IsUnitType(th, UNIT_TYPE_DEAD) then
                set dmgSrc = th
            else
                set dmgSrc = Ninja_PickLivingClone(pId)
            endif
            if dmgSrc != null then
                set aLv = GetUnitAbilityLevel(th, 'A012')
                if aLv > 0 then
                    set pct = 0.01 * I2R(aLv)
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRect(udg_EnumGroup, bj_mapInitialPlayableArea, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, Player(pId)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
                            set drain = GetUnitState(enumU, UNIT_STATE_MAX_LIFE) * pct
                            set curHP = GetWidgetLife(enumU)
                            if curHP > 1.5 then
                                if curHP - drain > 1.0 then
                                    call SetWidgetLife(enumU, curHP - drain)
                                else
                                    call SetWidgetLife(enumU, 1.0)
                                endif
                            endif
                        endif
                    endloop
                endif
            endif
        endif
        set pId = pId + 1
    endloop

    // 3. Process Karma Curse Drain (A013 Lv2 & Lv3)
    set i = 0
    loop
        exitwhen i >= udg_KarmaCount
        set u = udg_KarmaUnit[i]
        if u == null or IsUnitType(u, UNIT_TYPE_DEAD) or GetWidgetLife(u) <= 0.405 then
            call Ninja_RemoveKarmaIndex(i)
            set i = i - 1
        else
            set kLv = udg_KarmaLevel[i]
            if kLv >= 2 then
                if kLv == 2 then
                    set pct = 0.01
                else
                    set pct = 0.02
                endif
                set drain = GetUnitState(u, UNIT_STATE_MAX_LIFE) * pct
                set curHP = GetWidgetLife(u)
                if curHP > 1.5 then
                    if curHP - drain > 1.0 then
                        call SetWidgetLife(u, curHP - drain)
                    else
                        call SetWidgetLife(u, 1.0)
                    endif
                endif
            endif
        endif
        set u = null
        set i = i + 1
    endloop

    // 3.5. Process Hero #3 Digestion Timer Countdown
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_DigestTimer[pId] > 0.0 then
            set udg_Strain_DigestTimer[pId] = udg_Strain_DigestTimer[pId] - 1.0
            if udg_Strain_DigestTimer[pId] <= 0.0 then
                if udg_Strain_DigestFx[pId] != null then
                    call DestroyEffect(udg_Strain_DigestFx[pId])
                    set udg_Strain_DigestFx[pId] = null
                endif
                set u = udg_Strain_Hero[pId]
                if u == null then
                    set u = udg_AI_CustomHero[pId]
                endif
                if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) then
                    call SetWidgetLife(u, GetWidgetLife(u) + GetUnitState(u, UNIT_STATE_MAX_LIFE) * 0.25)
                    call SetUnitState(u, UNIT_STATE_MANA, GetUnitState(u, UNIT_STATE_MANA) + GetUnitState(u, UNIT_STATE_MAX_MANA) * 0.25)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIhe\\\\AIheTarget.mdl", u, "origin"))
                    set udg_Strain_MimicType[pId] = udg_Strain_DigestType[pId]
                    set udg_Strain_MimicOwner[pId] = udg_Strain_DigestOwner[pId]
                    call Strain_OnDigestComplete(u, pId)
                endif
                set u = null
            endif
        endif
        set pId = pId + 1
    endloop

    // 4. Custom Hero AI Tactical Loop
    call AI_TacticalLoop()
endfunction"""
content = replace_func(content, 'DM_CapTimerLoop', new_cap_timer)

# 10. Replace DM_OnSpellEffect
new_spell_effect = """function DM_OnSpellEffect takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer abil = GetSpellAbilityId()
    local integer pId = 0
    local unit ult = null

    if abil == 'A001' then
        call DM_OnCastMirror(caster)
    elseif abil == 'A002' then
        call DM_CastPossession(caster, GetSpellTargetUnit())
    elseif abil == 'A003' then
        call DM_CastMassIllusion(caster, GetSpellTargetX(), GetSpellTargetY())
    elseif abil == 'A012' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set udg_Ninja_TrueHero[pId] = Ninja_GetTrueHero(GetOwningPlayer(caster))
        set udg_Ninja_AuraOn[pId] = not udg_Ninja_AuraOn[pId]
        if udg_Ninja_AuraOn[pId] then
            if udg_Ninja_AuraFx[pId] == null then
                set udg_Ninja_AuraFx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", caster, "origin")
            endif
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\DeathPact\\\\DeathPactTarget.mdl", caster, "origin"))
        else
            if udg_Ninja_AuraFx[pId] != null then
                call DestroyEffect(udg_Ninja_AuraFx[pId])
                set udg_Ninja_AuraFx[pId] = null
            endif
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\DeathPact\\\\DeathPactTarget.mdl", caster, "origin"))
        endif
    elseif abil == 'A014' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set ult = CreateUnit(GetOwningPlayer(caster), 'u001', GetUnitX(caster) + 70.0, GetUnitY(caster) + 70.0, GetUnitFacing(caster))
        call UnitAddType(ult, UNIT_TYPE_SUMMONED)
        call UnitApplyTimedLife(ult, 'BTLF', 180.0)
        call UnitAddAbility(ult, 'A015')
        call SetUnitAbilityLevel(ult, 'A015', 3)
        if udg_Ninja_CloneGroup[pId] == null then
            set udg_Ninja_CloneGroup[pId] = CreateGroup()
        endif
        call GroupAddUnit(udg_Ninja_CloneGroup[pId], ult)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\Vengeance\\\\VengeanceAvenger.mdl", ult, "origin"))
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", GetUnitX(ult), GetUnitY(ult)))
        set ult = null
    elseif abil == 'A021' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set udg_Strain_Hero[pId] = caster
        if udg_Strain_Burrowed[pId] then
            call Strain_Unburrow(caster, pId)
        else
            if udg_Strain_MimicActive[pId] then
                call Strain_BreakMimicry(caster, pId)
            endif
            set udg_Strain_Burrowed[pId] = true
            set udg_Strain_BurrowTimer[pId] = 15.0 + 5.0 * I2R(GetUnitAbilityLevel(caster, 'A021'))
            call SetUnitPathing(caster, false)
            call SetUnitMoveSpeed(caster, 522.0)
            call SetUnitVertexColor(caster, 120, 95, 65, 110)
            set ult = CreateUnit(GetOwningPlayer(caster), 'u000', GetUnitX(caster), GetUnitY(caster), 0.0)
            call UnitAddAbility(ult, 'A00V')
            call IssueTargetOrder(ult, "invisibility", caster)
            call UnitApplyTimedLife(ult, 'BTLF', 1.0)
            set ult = null
            call DestroyEffect(AddSpecialEffect("Objects\\\\Spawnmodels\\\\Undead\\\\ImpaleTargetDust\\\\ImpaleTargetDust.mdl", GetUnitX(caster), GetUnitY(caster)))
        endif
    elseif abil == 'A022' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set ult = GetSpellTargetUnit()
        set udg_Strain_Hero[pId] = caster
        if ult != null then
            set udg_Strain_DigestType[pId] = GetUnitTypeId(ult)
            set udg_Strain_DigestOwner[pId] = GetOwningPlayer(ult)
            set udg_Strain_DigestIsHero[pId] = IsUnitType(ult, UNIT_TYPE_HERO) or IsHeroUnitId(GetUnitTypeId(ult))
            set udg_Strain_DigestTimer[pId] = 8.0 - 1.5 * I2R(GetUnitAbilityLevel(caster, 'A022'))
            call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\Devour\\\\DevourEffectArt.mdl", GetUnitX(ult), GetUnitY(ult)))
            call DestroyEffect(AddSpecialEffect("Objects\\\\Spawnmodels\\\\Human\\\\HumanLargeDeathExplode\\\\HumanLargeDeathExplode.mdl", GetUnitX(ult), GetUnitY(ult)))
            call SetUnitExploded(ult, true)
            call UnitDamageTarget(caster, ult, 999999.0, true, false, ATTACK_TYPE_CHAOS, DAMAGE_TYPE_UNIVERSAL, WEAPON_TYPE_WHOKNOWS)
            if udg_Strain_DigestFx[pId] != null then
                call DestroyEffect(udg_Strain_DigestFx[pId])
            endif
            set udg_Strain_DigestFx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\CorrosiveBreath\\\\ChimaeraAcidTargetArt.mdl", caster, "origin")
            set ult = null
        endif
    elseif abil == 'A023' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set udg_Strain_Hero[pId] = caster
        if udg_Strain_MimicActive[pId] then
            call Strain_BreakMimicry(caster, pId)
        else
            if udg_Strain_MimicType[pId] == 0 then
                call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 3.0, "|cffffcc00[拟态伪装]|r 尚未消化任何猎物样本，请先使用W【捕食吞噬】！")
            else
                if udg_Strain_Burrowed[pId] then
                    call Strain_Unburrow(caster, pId)
                endif
                set udg_Strain_MimicActive[pId] = true
                call SetUnitVertexColor(caster, 255, 255, 255, 0)
                set ult = CreateUnit(GetOwningPlayer(caster), udg_Strain_MimicType[pId], GetUnitX(caster), GetUnitY(caster), GetUnitFacing(caster))
                if IsUnitType(ult, UNIT_TYPE_HERO) or IsHeroUnitId(udg_Strain_MimicType[pId]) then
                    call UnitRemoveType(ult, UNIT_TYPE_HERO)
                    call UnitAddType(ult, UNIT_TYPE_SUMMONED)
                    call SuspendHeroXP(ult, true)
                    call GroupAddUnit(udg_FakeHeroGroup, ult)
                endif
                call UnitAddAbility(ult, 'Aloc')
                call UnitAddAbility(ult, 'Avul')
                call SetUnitPathing(ult, false)
                if udg_Strain_MimicOwner[pId] != null then
                    call SetUnitColor(ult, GetPlayerColor(udg_Strain_MimicOwner[pId]))
                    call SetUnitColor(caster, GetPlayerColor(udg_Strain_MimicOwner[pId]))
                endif
                set udg_Strain_MimicActor[pId] = ult
                set ult = null
                call SetPlayerAllianceStateBJ(Player(PLAYER_NEUTRAL_AGGRESSIVE), GetOwningPlayer(caster), bj_ALLIANCE_NEUTRAL)
                call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", GetUnitX(caster), GetUnitY(caster)))
            endif
        endif
    elseif abil == 'A024' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set udg_Strain_Hero[pId] = caster
        call Strain_ShowGeneDialog(GetOwningPlayer(caster), pId)
    endif

    // Hero #3 Stolen Hero Skill Resonance Overload
    set pId = GetPlayerId(GetOwningPlayer(caster))
    if GetUnitTypeId(caster) == 'H004' and udg_Strain_GeneCat[pId] == 5 and abil == udg_Strain_StolenHeroAbil[pId] then
        if udg_Strain_EvoTier[pId] >= 2 then
            call SetUnitState(caster, UNIT_STATE_MANA, GetUnitState(caster, UNIT_STATE_MANA) + 60.0)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIre\\\\AIreTarget.mdl", caster, "origin"))
            call GroupClear(udg_EnumGroup)
            call GroupEnumUnitsInRange(udg_EnumGroup, GetUnitX(caster), GetUnitY(caster), 350.0, null)
            loop
                set ult = FirstOfGroup(udg_EnumGroup)
                exitwhen ult == null
                call GroupRemoveUnit(udg_EnumGroup, ult)
                if IsUnitEnemy(ult, GetOwningPlayer(caster)) and not IsUnitType(ult, UNIT_TYPE_DEAD) and not IsUnitType(ult, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(ult) != 'u000' then
                    call UnitDamageTarget(caster, ult, I2R(GetHeroAgi(caster, true)) * 2.0 * I2R(udg_Strain_EvoTier[pId]), true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\CorrosiveBreath\\\\ChimaeraAcidTargetArt.mdl", ult, "chest"))
                endif
            endloop
            set ult = null
        endif
    endif

    set caster = null
    return false
endfunction"""
content = replace_func(content, 'DM_OnSpellEffect', new_spell_effect)

# 11. Replace DM_OnSpellCast
new_spell_cast = """function DM_OnSpellCast takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer hIdx = DM_GetHeroIndex(caster)
    local integer abilId = GetSpellAbilityId()
    local integer pId = 0
    local unit tgt = null
    local real maxHP = 0.0
    local real curHP = 0.0
    local boolean isHero = false

    if hIdx >= 0 and udg_DM_InStealth[hIdx] then
        if abilId != 'A001' then
            call DM_BreakInvisibility(caster, null)
        endif
    endif

    if abilId == 'A022' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        set tgt = GetSpellTargetUnit()
        if udg_Strain_DigestTimer[pId] > 0.0 then
            call IssueImmediateOrder(caster, "stop")
            call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 3.0, "|cffffcc00[捕食吞噬]|r 正在消化猎物中，请等待消化完成！")
        elseif tgt != null then
            set maxHP = GetUnitState(tgt, UNIT_STATE_MAX_LIFE)
            set curHP = GetWidgetLife(tgt)
            set isHero = IsUnitType(tgt, UNIT_TYPE_HERO) or IsHeroUnitId(GetUnitTypeId(tgt))
            if (isHero and curHP > (maxHP * 0.28)) or (not isHero and curHP > (maxHP * 0.35)) then
                call IssueImmediateOrder(caster, "stop")
                if GetPlayerController(GetOwningPlayer(caster)) == MAP_CONTROL_USER then
                    call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 3.0, "|cffffcc00[捕食吞噬]|r 目标生命值过高（普通单位需低于35%，英雄需低于28%）！")
                endif
            endif
        endif
        set tgt = null
    endif

    if GetUnitTypeId(caster) == 'H004' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        if udg_Strain_Burrowed[pId] and abilId != 'A021' then
            call Strain_Unburrow(caster, pId)
        endif
    endif

    set caster = null
    return false
endfunction"""
content = replace_func(content, 'DM_OnSpellCast', new_spell_cast)

# 12. Replace DM_OnDamaged
new_damaged = """function DM_OnDamaged takes nothing returns boolean
    local unit src = GetEventDamageSource()
    local unit tgt = GetTriggerUnit()
    local integer hIdx = -1
    local integer pId = 0
    local unit c = null
    local real oldX = 0.0
    local real oldY = 0.0
    local real nx = 0.0
    local real ny = 0.0
    local real nf = 0.0
    local real nhp = 0.0
    local real maxHP = 0.0
    local integer qLv = 0
    local real dmg = 0.0
    local integer eLv = 0
    local integer tier = 0
    local unit enumU = null

    if udg_Strain_DamageLock then
        return false
    endif

    if src != null and tgt != null and GetEventDamage() > 0.0 then
        set dmg = GetEventDamage()

        set hIdx = DM_GetHeroIndex(src)
        if hIdx >= 0 and udg_DM_InStealth[hIdx] then
            call DM_BreakInvisibility(src, tgt)
        endif

        // Hero #3: The Primordial Strain (H004) Damage Interactions
        if GetUnitTypeId(src) == 'H004' then
            set pId = GetPlayerId(GetOwningPlayer(src))
            set udg_Strain_Hero[pId] = src

            // Unburrow if attacking
            if udg_Strain_Burrowed[pId] then
                call Strain_Unburrow(src, pId)
            endif

            set udg_Strain_DamageLock = true

            // Ambush Critical Strike from Mimicry
            if udg_Strain_MimicActive[pId] then
                call Strain_BreakMimicry(src, pId)
                set eLv = GetUnitAbilityLevel(src, 'A023')
                if eLv == 1 then
                    call UnitDamageTarget(src, tgt, dmg * 0.50, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                elseif eLv == 2 then
                    call UnitDamageTarget(src, tgt, dmg * 0.75, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                else
                    call UnitDamageTarget(src, tgt, dmg * 1.00, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                endif
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\CriticalStrike\\\\CriticalStrike.mdl", tgt, "overhead"))
            endif

            // Gene On-Attack Effects
            set tier = udg_Strain_EvoTier[pId]
            if udg_Strain_GeneCat[pId] == 2 then
                // Cat 2: Poison
                if tier == 2 then
                    call UnitDamageTarget(src, tgt, 30.0, false, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Weapons\\\\PoisonSting\\\\PoisonStingTarget.mdl", tgt, "chest"))
                elseif tier >= 3 then
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRange(udg_EnumGroup, GetUnitX(tgt), GetUnitY(tgt), 300.0, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, GetOwningPlayer(src)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
                            call UnitDamageTarget(src, enumU, 55.0 + 1.0 * I2R(GetHeroAgi(src, true)), false, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Weapons\\\\PoisonSting\\\\PoisonStingTarget.mdl", enumU, "chest"))
                        endif
                    endloop
                    set enumU = null
                endif
            elseif udg_Strain_GeneCat[pId] == 3 then
                // Cat 3: Bloodlust Lifesteal + Bonus Damage + Visual + AoE Ally Heal
                call SetWidgetLife(src, GetWidgetLife(src) + 0.15 * I2R(tier) * dmg)
                call UnitDamageTarget(src, tgt, 20.0 * I2R(tier), false, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Bloodlust\\\\BloodlustTarget.mdl", src, "origin"))
                if tier >= 3 then
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRange(udg_EnumGroup, GetUnitX(src), GetUnitY(src), 450.0, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if not IsUnitEnemy(enumU, GetOwningPlayer(src)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
                            call SetWidgetLife(enumU, GetWidgetLife(enumU) + 0.10 * dmg)
                            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIhe\\\\AIheTarget.mdl", enumU, "origin"))
                        endif
                    endloop
                    set enumU = null
                endif
            elseif udg_Strain_GeneCat[pId] == 4 then
                // Cat 4: Lightning Strike + Thunderclap AoE
                call UnitDamageTarget(src, tgt, 35.0 * I2R(tier), false, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\Monsoon\\\\MonsoonBoltTarget.mdl", tgt, "chest"))
                if tier >= 3 then
                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", GetUnitX(src), GetUnitY(src)))
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRange(udg_EnumGroup, GetUnitX(src), GetUnitY(src), 300.0, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, GetOwningPlayer(src)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
                            call UnitDamageTarget(src, enumU, 250.0, false, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                        endif
                    endloop
                    set enumU = null
                endif
            endif

            set udg_Strain_DamageLock = false
        endif

        // When H004 takes damage: Cat 1 Shield Damage Reflection
        if GetUnitTypeId(tgt) == 'H004' then
            set pId = GetPlayerId(GetOwningPlayer(tgt))
            if udg_Strain_GeneCat[pId] == 1 and udg_Strain_EvoTier[pId] >= 3 and src != null then
                set udg_Strain_DamageLock = true
                call UnitDamageTarget(tgt, src, dmg * 0.50, false, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Defend\\\\DefendCaster.mdl", tgt, "origin"))
                set udg_Strain_DamageLock = false
            endif
        endif

        // Ninja (A011) - Pre-lethal swap
        if GetUnitTypeId(tgt) == 'H003' and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and not IsUnitIllusion(tgt) then
            set pId = GetPlayerId(GetOwningPlayer(tgt))
            set udg_Ninja_TrueHero[pId] = tgt
            if GetEventDamage() >= (GetWidgetLife(tgt) - 1.0) then
                set c = Ninja_PickLivingClone(pId)
                if c != null then
                    if GetUnitAbilityLevel(tgt, 'A013') > 0 and src != null then
                        call Ninja_MarkKarma(src, GetOwningPlayer(tgt), GetUnitAbilityLevel(tgt, 'A013'))
                    endif

                    set oldX = GetUnitX(tgt)
                    set oldY = GetUnitY(tgt)
                    set nx = GetUnitX(c)
                    set ny = GetUnitY(c)
                    set nf = GetUnitFacing(c)
                    set nhp = GetWidgetLife(c)

                    call GroupRemoveUnit(udg_Ninja_CloneGroup[pId], c)
                    call GroupRemoveUnit(udg_FakeHeroGroup, c)
                    call RemoveUnit(c)
                    set c = null

                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageDeathCaster.mdl", oldX, oldY))
                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\NightElf\\\\Blink\\\\BlinkCaster.mdl", oldX, oldY))

                    set maxHP = GetUnitState(tgt, UNIT_STATE_MAX_LIFE)
                    set qLv = GetUnitAbilityLevel(tgt, 'A011')
                    if qLv == 2 and nhp < (maxHP * 0.30) then
                        set nhp = maxHP * 0.30
                    elseif qLv >= 3 and nhp < (maxHP * 0.50) then
                        set nhp = maxHP * 0.50
                    endif

                    call SetWidgetLife(tgt, maxHP)
                    if udg_Ninja_PendingCount < 32 then
                        set udg_Ninja_PendingHealUnit[udg_Ninja_PendingCount] = tgt
                        set udg_Ninja_PendingHealHP[udg_Ninja_PendingCount] = RMaxBJ(nhp, maxHP * 0.35)
                        set udg_Ninja_PendingCount = udg_Ninja_PendingCount + 1
                    endif

                    call SetUnitX(tgt, nx)
                    call SetUnitY(tgt, ny)
                    call SetUnitFacing(tgt, nf)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\Blink\\\\BlinkTarget.mdl", tgt, "origin"))
                endif
            endif
        endif
    endif

    set src = null
    set tgt = null
    return false
endfunction"""
content = replace_func(content, 'DM_OnDamaged', new_damaged)

# 13. Replace DM_OnUnitDeath
new_death = """function DM_OnUnitDeath takes nothing returns boolean
    local unit dead = GetTriggerUnit()
    local unit killer = GetKillingUnit()
    local player deadOwner = GetOwningPlayer(dead)
    local integer deadPId = GetPlayerId(deadOwner)
    local integer deadType = GetUnitTypeId(dead)
    local real deadX = GetUnitX(dead)
    local real deadY = GetUnitY(dead)
    local real deadFacing = GetUnitFacing(dead)
    local boolean isFakeHero = IsUnitInGroup(dead, udg_FakeHeroGroup)
    local boolean isIllusion = IsUnitIllusion(dead)
    local integer idx = -1
    local integer kIdx = -1
    local player ko = null
    local integer klv = 0
    local boolean hasLivingNinja = false
    local player kp = null
    local unit th = null
    local integer eLv = 0
    local unit c = null
    local real nx = 0.0
    local real ny = 0.0
    local real nhp = 0.0

    // 1. Dream Master Possession Return
    set idx = DM_FindCapIndex(dead)
    if idx >= 0 then
        call SetUnitOwner(dead, udg_CapOrigOwner[idx], true)
        call DM_RemoveCapIndex(idx)
    endif

    // 1.5. Clean up Hero #3 state on death
    if deadType == 'H004' then
        if udg_Strain_Burrowed[deadPId] then
            call Strain_Unburrow(dead, deadPId)
        endif
        if udg_Strain_MimicActive[deadPId] then
            call Strain_BreakMimicry(dead, deadPId)
        endif
        if udg_Strain_DigestFx[deadPId] != null then
            call DestroyEffect(udg_Strain_DigestFx[deadPId])
            set udg_Strain_DigestFx[deadPId] = null
            set udg_Strain_DigestTimer[deadPId] = 0.0
        endif
    endif

    // 2. Ninja Karma Mark
    if (deadType == 'H003' or deadType == 'u002' or deadType == 'u001') and killer != null and IsUnitEnemy(killer, deadOwner) then
        set th = Ninja_GetTrueHero(deadOwner)
        set eLv = GetUnitAbilityLevel(dead, 'A013')
        if th != null and GetUnitAbilityLevel(th, 'A013') > eLv then
            set eLv = GetUnitAbilityLevel(th, 'A013')
        endif
        if eLv > 0 then
            call Ninja_MarkKarma(killer, deadOwner, eLv)
        endif
    endif

    // 3. Ninja Karma Rebirth
    set kIdx = Ninja_FindKarmaIndex(dead)
    if kIdx >= 0 then
        set ko = udg_KarmaOwner[kIdx]
        set klv = udg_KarmaLevel[kIdx]
        call Ninja_RemoveKarmaIndex(kIdx)

        set th = Ninja_GetTrueHero(ko)
        set hasLivingNinja = false
        if th != null and not IsUnitType(th, UNIT_TYPE_DEAD) and GetWidgetLife(th) > 0.405 then
            set hasLivingNinja = true
        elseif Ninja_PickLivingClone(GetPlayerId(ko)) != null then
            set hasLivingNinja = true
        endif

        if not hasLivingNinja and th != null then
            call ReviveHero(th, deadX, deadY, true)
            call SetUnitFacing(th, deadFacing)
            call SetWidgetLife(th, GetUnitState(th, UNIT_STATE_MAX_LIFE))
            call SetUnitState(th, UNIT_STATE_MANA, GetUnitState(th, UNIT_STATE_MAX_MANA))
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\Blink\\\\BlinkTarget.mdl", th, "origin"))
            if GetLocalPlayer() == ko then
                call SelectUnit(th, true)
            endif
        else
            call Ninja_SpawnClone(ko, deadX, deadY, deadFacing)
            if klv >= 3 then
                call Ninja_SpawnClone(ko, deadX + 45.0, deadY + 45.0, deadFacing)
            endif
        endif
        set ko = null
    endif

    // 4. Ninja Clone on Kill
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'H003' and not isFakeHero and not isIllusion and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u002' or GetUnitTypeId(killer) == 'u001') then
        set kp = GetOwningPlayer(killer)
        set th = Ninja_GetTrueHero(kp)
        if GetUnitAbilityLevel(killer, 'A011') > 0 or (th != null and GetUnitAbilityLevel(th, 'A011') > 0) or GetPlayerController(kp) == MAP_CONTROL_COMPUTER or GetUnitTypeId(killer) == 'u001' then
            call Ninja_SpawnClone(kp, deadX, deadY, deadFacing)
        endif
        set kp = null
        set th = null
    endif

    // 5. Ninja Clone Swap Fallback
    if deadType == 'H003' and not isFakeHero and not isIllusion then
        set c = Ninja_PickLivingClone(deadPId)
        if c != null then
            set nx = GetUnitX(c)
            set ny = GetUnitY(c)
            set nhp = GetWidgetLife(c)
            call GroupRemoveUnit(udg_Ninja_CloneGroup[deadPId], c)
            call GroupRemoveUnit(udg_FakeHeroGroup, c)
            call RemoveUnit(c)
            set c = null

            call ReviveHero(dead, nx, ny, false)
            call SetWidgetLife(dead, RMaxBJ(nhp, GetUnitState(dead, UNIT_STATE_MAX_LIFE) * 0.35))
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\Blink\\\\BlinkTarget.mdl", dead, "origin"))
            if GetLocalPlayer() == deadOwner then
                call SelectUnit(dead, true)
            endif
        endif
    endif

    // 6. Cleanup Fake Hero / Clone
    if isFakeHero or deadType == 'u002' or deadType == 'u001' then
        if udg_Ninja_CloneGroup[deadPId] != null then
            call GroupRemoveUnit(udg_Ninja_CloneGroup[deadPId], dead)
        endif
        call GroupRemoveUnit(udg_FakeHeroGroup, dead)
        if deadType == 'u002' then
            call SetUnitOwner(dead, Player(PLAYER_NEUTRAL_PASSIVE), false)
            call SetUnitExploded(dead, true)
            call RemoveUnit(dead)
        endif
    endif

    set dead = null
    set killer = null
    set deadOwner = null
    return false
endfunction"""
content = replace_func(content, 'DM_OnUnitDeath', new_death)

# 14. Replace TM_ApplyAIConfig
new_apply_ai = """function TM_ApplyAIConfig takes nothing returns nothing
    local integer i = 0
    local group g = null
    local unit u = null
    local boolean hasCustom = false

    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] > 0 then
                set hasCustom = true
                if not udg_AI_HeroSpawned[i] then
                    set g = CreateGroup()
                    call GroupEnumUnitsOfPlayer(g, Player(i), null)
                    loop
                        set u = FirstOfGroup(g)
                        exitwhen u == null
                        call GroupRemoveUnit(g, u)
                        if IsUnitType(u, UNIT_TYPE_HERO) and GetUnitTypeId(u) != 'H002' and GetUnitTypeId(u) != 'H003' and GetUnitTypeId(u) != 'H004' and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
                            call AI_SpawnCustomHeroForPlayer(i, GetUnitX(u), GetUnitY(u), GetUnitFacing(u))
                            call RemoveUnit(u)
                            call GroupClear(g)
                        endif
                    endloop
                    call DestroyGroup(g)
                    set g = null
                endif
            endif
        endif
        set i = i + 1
    endloop
endfunction"""
content = replace_func(content, 'TM_ApplyAIConfig', new_apply_ai)

# 15. Replace TM_ShowMainDialog
new_show_main = """function TM_ShowMainDialog takes player p returns nothing
    if p == null then
        return
    endif
    set udg_TM_PromptPlayer = p
    call DialogDisplay(p, udg_TM_MainDialog, false)
    call DialogClear(udg_TM_MainDialog)
    call DialogSetMessage(udg_TM_MainDialog, "【测试模式选择】(鼠标点击或按数字键1-5)")
    set udg_TM_BtnNormal = DialogAddButton(udg_TM_MainDialog, "[1] 正常模式（使用原有英雄）", 49)
    set udg_TM_BtnMode1All = DialogAddButton(udg_TM_MainDialog, "[2] 测试模式一：全部电脑出【幻梦大师】", 50)
    set udg_TM_BtnMode2All = DialogAddButton(udg_TM_MainDialog, "[3] 测试模式二：全部电脑出【魔音忍者】", 51)
    set udg_TM_BtnMode3All = DialogAddButton(udg_TM_MainDialog, "[4] 测试模式三：全部电脑出【异种之源】", 52)
    set udg_TM_BtnCustom = DialogAddButton(udg_TM_MainDialog, "[5] 精细配置：指定玩家的英雄...", 53)
    call DialogDisplay(p, udg_TM_MainDialog, true)
endfunction"""
content = replace_func(content, 'TM_ShowMainDialog', new_show_main)

# 16. Replace TM_ShowSlotDialog
new_show_slot = """function TM_ShowSlotDialog takes player p returns nothing
    local integer i = 0
    local string lbl = ""
    if p == null then
        return
    endif
    set udg_TM_PromptPlayer = p
    call DialogDisplay(p, udg_TM_SlotDialog, false)
    call DialogClear(udg_TM_SlotDialog)
    call DialogSetMessage(udg_TM_SlotDialog, "【精细配置】点击切换英雄 (确定后生效)")
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] == 1 then
                set lbl = "玩家 " + I2S(i + 1) + "：【幻梦大师】 (点击切换)"
            elseif udg_AI_HeroMode[i] == 2 then
                set lbl = "玩家 " + I2S(i + 1) + "：【魔音忍者】 (点击切换)"
            elseif udg_AI_HeroMode[i] == 3 then
                set lbl = "玩家 " + I2S(i + 1) + "：【异种之源】 (点击切换)"
            else
                set lbl = "玩家 " + I2S(i + 1) + "：【常规默认英雄】 (点击切换)"
            endif
            set udg_TM_SlotBtn[i] = DialogAddButton(udg_TM_SlotDialog, lbl, 0)
        else
            set udg_TM_SlotBtn[i] = null
        endif
        set i = i + 1
    endloop
    set udg_TM_SlotConfirm = DialogAddButton(udg_TM_SlotDialog, "[9] 确定配置并开始", 57)
    set udg_TM_SlotBack = DialogAddButton(udg_TM_SlotDialog, "[0] 返回上一菜单", 48)
    call DialogDisplay(p, udg_TM_SlotDialog, true)
endfunction"""
content = replace_func(content, 'TM_ShowSlotDialog', new_show_slot)

# 17. Replace TM_OnMainDialogClicked
new_main_click = """function TM_OnMainDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    call DialogDisplay(p, udg_TM_MainDialog, false)

    if b == udg_TM_BtnNormal then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 0
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 正常模式：使用原有英雄 (随时输入 -test 可重选)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode1All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式一：全部电脑出【幻梦大师】！(随时输入 -test 可重选)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode2All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 2
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式二：全部电脑出【魔音忍者】！(随时输入 -test 可重选)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode3All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 3
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式三：全部电脑出【异种之源】！(随时输入 -test 可重选)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnCustom then
        call TM_ShowSlotDialog(p)
    endif

    set b = null
    set p = null
endfunction"""
content = replace_func(content, 'TM_OnMainDialogClicked', new_main_click)

# 18. Replace TM_OnSlotDialogClicked
new_slot_click = """function TM_OnSlotDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if b == udg_TM_SlotConfirm then
        call DialogDisplay(p, udg_TM_SlotDialog, false)
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 英雄配置精细设定已生效！(随时输入 -test 可重选)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_SlotBack then
        call DialogDisplay(p, udg_TM_SlotDialog, false)
        call TM_ShowMainDialog(p)
    else
        set i = 0
        loop
            exitwhen i > 7
            if b == udg_TM_SlotBtn[i] then
                if udg_AI_HeroMode[i] == 0 then
                    set udg_AI_HeroMode[i] = 1
                elseif udg_AI_HeroMode[i] == 1 then
                    set udg_AI_HeroMode[i] = 2
                elseif udg_AI_HeroMode[i] == 2 then
                    set udg_AI_HeroMode[i] = 3
                else
                    set udg_AI_HeroMode[i] = 0
                endif
                call TM_ShowSlotDialog(p)
                set b = null
                set p = null
                return
            endif
            set i = i + 1
        endloop
    endif

    set b = null
    set p = null
endfunction"""
content = replace_func(content, 'TM_OnSlotDialogClicked', new_slot_click)

# 19. Insert TM_SpawnSandboxTargets before TM_OnChatCommand
sandbox_func = """function TM_SpawnSandboxTargets takes player p returns nothing
    local group g = CreateGroup()
    local unit u = null
    local real hx = 0.0
    local real hy = 0.0
    local unit targetU = null

    if p == null then
        return
    endif

    call GroupEnumUnitsOfPlayer(g, p, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        if IsUnitType(u, UNIT_TYPE_HERO) and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
            set hx = GetUnitX(u)
            set hy = GetUnitY(u)
            set u = null
            exitwhen true
        endif
    endloop
    call DestroyGroup(g)
    set g = null

    if hx == 0.0 and hy == 0.0 then
        set hx = GetStartLocationX(GetPlayerStartLocation(p))
        set hy = GetStartLocationY(GetPlayerStartLocation(p))
    endif

    // 1. Footman (hfoo) - Shield evolution
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'hfoo', hx + 180.0, hy, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 2. Dryad (edry) - Poison evolution
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'edry', hx + 180.0, hy + 90.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 3. Shaman (oshm) - Bloodlust evolution
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'oshm', hx + 180.0, hy - 90.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 4. Rock Golem (ngst) - Thunder bash evolution
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'ngst', hx + 180.0, hy + 180.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 5. Blademaster (Obla) - Hero 4-choice steal & +4 Agi
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'Obla', hx + 180.0, hy - 180.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    set targetU = null
    call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cff00ff00[沙盒测试]|r 已生成5个20%残血测试靶子（步兵/小鹿/萨满/石头人/敌方英雄），可直接用W【捕食吞噬】测试进化！")
endfunction
"""

target_chat_decl = "function TM_OnChatCommand takes nothing returns nothing"
assert target_chat_decl in content, "target_chat_decl not found"
content = content.replace(target_chat_decl, sandbox_func + "\n" + target_chat_decl, 1)

# 20. Replace TM_OnChatCommand
new_chat_command = """function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if s == "-test" or s == "-mode" then
        call TM_ShowMainDialog(p)
    elseif s == "-m0" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 0
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 正常模式：使用原有默认英雄。")
        call TM_ApplyAIConfig()
    elseif s == "-m1" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式一：全部电脑出【幻梦大师】！")
        call TM_ApplyAIConfig()
    elseif s == "-m2" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 2
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式二：全部电脑出【魔音忍者】！")
        call TM_ApplyAIConfig()
    elseif s == "-m3" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 3
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式三：全部电脑出【异种之源】！")
        call TM_ApplyAIConfig()
    elseif s == "-spawn" then
        call TM_SpawnSandboxTargets(p)
    endif

    set p = null
endfunction"""
content = replace_func(content, 'TM_OnChatCommand', new_chat_command)

# 21. Replace AI_OnHeroLevel
new_hero_level = """function AI_OnHeroLevel takes nothing returns boolean
    local unit h = GetLevelingUnit()
    if h != null and (GetUnitTypeId(h) == 'H002' or GetUnitTypeId(h) == 'H003' or GetUnitTypeId(h) == 'H004') then
        call AI_AutoLearnSkills(h)
    endif
    set h = null
    return false
endfunction"""
content = replace_func(content, 'AI_OnHeroLevel', new_hero_level)

# 22. Replace AI_OnUnitTrainFinish
new_train_finish = """function AI_OnUnitTrainFinish takes nothing returns boolean
    local unit trained = GetTrainedUnit()
    local player p = null
    local integer pId = 0
    local real hx = 0.0
    local real hy = 0.0
    local real hf = 0.0

    if trained != null then
        set p = GetOwningPlayer(trained)
        set pId = GetPlayerId(p)
        if GetUnitTypeId(trained) == 'H004' then
            set udg_Strain_Hero[pId] = trained
            call Strain_InitHero(trained)
        endif
        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[pId] > 0 and not IsUnitType(trained, UNIT_TYPE_PEON) then
                call RemoveGuardPosition(trained)
            endif
            if GetUnitTypeId(trained) == 'H004' then
                set udg_AI_CustomHero[pId] = trained
                set udg_AI_HeroSpawned[pId] = true
                call AI_AutoLearnSkills(trained)
            elseif GetUnitTypeId(trained) == 'H003' then
                set udg_Ninja_TrueHero[pId] = trained
                set udg_AI_CustomHero[pId] = trained
                set udg_AI_HeroSpawned[pId] = true
                call AI_AutoLearnSkills(trained)
            elseif GetUnitTypeId(trained) == 'H002' then
                set udg_AI_CustomHero[pId] = trained
                set udg_AI_HeroSpawned[pId] = true
                call AI_AutoLearnSkills(trained)
            elseif udg_AI_HeroMode[pId] > 0 and not udg_AI_HeroSpawned[pId] and IsUnitType(trained, UNIT_TYPE_HERO) and not IsUnitIllusion(trained) and not IsUnitInGroup(trained, udg_FakeHeroGroup) then
                set hx = GetUnitX(trained)
                set hy = GetUnitY(trained)
                set hf = GetUnitFacing(trained)
                call RemoveUnit(trained)
                call AI_SpawnCustomHeroForPlayer(pId, hx, hy, hf)
            endif
        endif
    endif

    set trained = null
    set p = null
    return false
endfunction"""
content = replace_func(content, 'AI_OnUnitTrainFinish', new_train_finish)

# 23. Replace DM_InitTriggers
new_init_triggers = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tSkill = CreateTrigger()
    local trigger tTrain = CreateTrigger()
    local trigger tLevel = CreateTrigger()
    local trigger tMainDialog = CreateTrigger()
    local trigger tSlotDialog = CreateTrigger()
    local trigger tChat = CreateTrigger()
    local trigger tGeneDialog = CreateTrigger()
    local trigger tHeroDialog = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()
    local timer tmrStart = CreateTimer()
    local integer i = 0

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()
    set udg_AI_ArmyGroup = CreateGroup()
    set udg_AI_CombatGroup = CreateGroup()

    set i = 0
    loop
        exitwhen i > 15
        set udg_Ninja_CloneGroup[i] = CreateGroup()
        set udg_Ninja_AuraOn[i] = false
        set udg_Ninja_AuraFx[i] = null
        set udg_Ninja_TrueHero[i] = null

        // Initialize AI variables
        set udg_AI_HeroMode[i] = 0
        set udg_AI_CustomHero[i] = null
        set udg_AI_LockedTarget[i] = null
        set udg_AI_HeroSpawned[i] = false
        set udg_AI_CastCD_Q[i] = 0.0
        set udg_AI_CastCD_W[i] = 0.0
        set udg_AI_CastCD_E[i] = 0.0
        set udg_AI_CastCD_R[i] = 0.0
        set udg_AI_DeadTimer[i] = 0.0
        set udg_AI_AltarTimer[i] = 0.0
        set udg_AI_WaitTimer[i] = 0.0
        set udg_TM_SlotBtn[i] = null

        // Initialize Strain variables
        set udg_Strain_Burrowed[i] = false
        set udg_Strain_BurrowTimer[i] = 0.0
        set udg_Strain_DigestTimer[i] = 0.0
        set udg_Strain_DigestType[i] = 0
        set udg_Strain_DigestOwner[i] = null
        set udg_Strain_DigestIsHero[i] = false
        set udg_Strain_DigestFx[i] = null
        set udg_Strain_MimicActive[i] = false
        set udg_Strain_MimicType[i] = 0
        set udg_Strain_MimicOwner[i] = null
        set udg_Strain_MimicActor[i] = null
        set udg_Strain_GeneCat[i] = 0
        set udg_Strain_EvoTier[i] = 0
        set udg_Strain_StolenHeroAbil[i] = 0
        set udg_Strain_CandidateAbil0[i] = 0
        set udg_Strain_CandidateAbil1[i] = 0
        set udg_Strain_CandidateAbil2[i] = 0
        set udg_Strain_CandidateAbil3[i] = 0
        set udg_Strain_Hero[i] = null

        set i = i + 1
    endloop

    // Initialize Test Mode Dialogs
    set udg_TM_MainDialog = DialogCreate()
    set udg_TM_SlotDialog = DialogCreate()

    call TriggerRegisterDialogEvent(tMainDialog, udg_TM_MainDialog)
    call TriggerAddAction(tMainDialog, function TM_OnMainDialogClicked)

    call TriggerRegisterDialogEvent(tSlotDialog, udg_TM_SlotDialog)
    call TriggerAddAction(tSlotDialog, function TM_OnSlotDialogClicked)

    // Initialize Strain Dialogs
    set udg_Strain_GeneDialog = DialogCreate()
    set udg_Strain_HeroDialog = DialogCreate()

    call TriggerRegisterDialogEvent(tGeneDialog, udg_Strain_GeneDialog)
    call TriggerAddAction(tGeneDialog, function Strain_OnGeneDialogClick)

    call TriggerRegisterDialogEvent(tHeroDialog, udg_Strain_HeroDialog)
    call TriggerAddAction(tHeroDialog, function Strain_OnHeroDialogClick)

    set i = 0
    loop
        exitwhen i > 7
        call TriggerRegisterPlayerChatEvent(tChat, Player(i), "-", false)
        set i = i + 1
    endloop
    call TriggerAddAction(tChat, function TM_OnChatCommand)

    call TriggerRegisterAnyUnitEventBJ(tEffect, EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddCondition(tEffect, Condition(function DM_OnSpellEffect))

    call TriggerRegisterAnyUnitEventBJ(tCast, EVENT_PLAYER_UNIT_SPELL_CAST)
    call TriggerAddCondition(tCast, Condition(function DM_OnSpellCast))

    call TriggerRegisterAnyUnitEventBJ(tDeath, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddCondition(tDeath, Condition(function DM_OnUnitDeath))

    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))

    call TriggerRegisterAnyUnitEventBJ(tDamage, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))

    call TriggerRegisterAnyUnitEventBJ(tSkill, EVENT_PLAYER_HERO_SKILL)
    call TriggerAddCondition(tSkill, Condition(function Ninja_OnHeroSkill))

    call TriggerRegisterAnyUnitEventBJ(tTrain, EVENT_PLAYER_UNIT_TRAIN_FINISH)
    call TriggerAddCondition(tTrain, Condition(function AI_OnUnitTrainFinish))

    call TriggerRegisterAnyUnitEventBJ(tLevel, EVENT_PLAYER_HERO_LEVEL)
    call TriggerAddCondition(tLevel, Condition(function AI_OnHeroLevel))

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)
    call TimerStart(tmrStart, 1.00, false, function TM_OnStartTimer)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tSkill = null
    set tTrain = null
    set tLevel = null
    set tMainDialog = null
    set tSlotDialog = null
    set tChat = null
    set tGeneDialog = null
    set tHeroDialog = null
    set tmrCap = null
    set tmrStealth = null
    set tmrStart = null
endfunction"""
content = replace_func(content, 'DM_InitTriggers', new_init_triggers)

with open(J_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully! New length:", len(content))
