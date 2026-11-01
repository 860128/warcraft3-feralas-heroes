# -*- coding: utf-8 -*-
import sys

def main():
    path = 'payload/war3map.j'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update globals
    old_globals = """    group udg_EnumGroup = null
    group udg_FakeHeroGroup = null
endglobals"""

    new_globals = """    group udg_EnumGroup = null
    group udg_FakeHeroGroup = null

    // Ninja (魔音忍者) globals
    unit array udg_Ninja_TrueHero
    group array udg_Ninja_CloneGroup
    boolean array udg_Ninja_AuraOn
    effect array udg_Ninja_AuraFx
    unit array udg_Ninja_PendingHealUnit
    real array udg_Ninja_PendingHealHP
    integer udg_Ninja_PendingCount = 0

    unit array udg_KarmaUnit
    player array udg_KarmaOwner
    integer array udg_KarmaLevel
    integer udg_KarmaCount = 0
endglobals"""

    assert old_globals in content, "old_globals not found!"
    content = content.replace(old_globals, new_globals, 1)

    # 2. Add Ninja helper functions above DM_GetHeroIndex
    target_pos = "// Dream Master ("
    idx = content.find(target_pos)
    assert idx != -1, "DM header not found!"

    ninja_funcs = """//===========================================================================
// Ninja (魔音忍者) Core System
//===========================================================================

function Ninja_GetTrueHero takes player p returns unit
    local integer pId = GetPlayerId(p)
    local unit u = null
    local group g = null
    if udg_Ninja_TrueHero[pId] != null and GetUnitTypeId(udg_Ninja_TrueHero[pId]) == 'H003' then
        return udg_Ninja_TrueHero[pId]
    endif
    set g = CreateGroup()
    call GroupEnumUnitsOfPlayer(g, p, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        if GetUnitTypeId(u) == 'H003' and not IsUnitInGroup(u, udg_FakeHeroGroup) and not IsUnitIllusion(u) then
            set udg_Ninja_TrueHero[pId] = u
            call DestroyGroup(g)
            set g = null
            return u
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    return null
endfunction

function Ninja_SpawnClone takes player p, real x, real y, real facing returns unit
    local integer pId = GetPlayerId(p)
    local unit trueHero = Ninja_GetTrueHero(p)
    local real dur = 120.0
    local integer lv = 0
    local unit clone = null
    local integer targetLv = 0
    local integer curLv = 0
    local integer itemSlot = 0
    local item itm = null

    if trueHero != null then
        set lv = GetUnitAbilityLevel(trueHero, 'A011')
    endif
    if lv <= 1 then
        set dur = 120.0
    elseif lv == 2 then
        set dur = 240.0
    else
        set dur = 600.0
    endif

    set clone = CreateUnit(p, 'H003', x, y, facing)
    call UnitRemoveType(clone, UNIT_TYPE_HERO)
    call UnitAddType(clone, UNIT_TYPE_SUMMONED)
    call SuspendHeroXP(clone, true)

    if trueHero != null then
        if GetHeroLevel(trueHero) > 1 then
            call SetHeroLevel(clone, GetHeroLevel(trueHero), false)
        endif

        set targetLv = GetUnitAbilityLevel(trueHero, 'A011')
        if targetLv > 0 then
            set curLv = 0
            loop
                exitwhen curLv >= targetLv
                call SelectHeroSkill(clone, 'A011')
                set curLv = curLv + 1
            endloop
            if GetUnitAbilityLevel(clone, 'A011') < targetLv then
                call UnitAddAbility(clone, 'A011')
                call SetUnitAbilityLevel(clone, 'A011', targetLv)
            endif
        endif

        set targetLv = GetUnitAbilityLevel(trueHero, 'A013')
        if targetLv > 0 then
            set curLv = 0
            loop
                exitwhen curLv >= targetLv
                call SelectHeroSkill(clone, 'A013')
                set curLv = curLv + 1
            endloop
            if GetUnitAbilityLevel(clone, 'A013') < targetLv then
                call UnitAddAbility(clone, 'A013')
                call SetUnitAbilityLevel(clone, 'A013', targetLv)
            endif
        endif

        set itemSlot = 0
        loop
            exitwhen itemSlot >= 6
            set itm = UnitItemInSlot(trueHero, itemSlot)
            if itm != null then
                call UnitAddItemById(clone, GetItemTypeId(itm))
            endif
            set itemSlot = itemSlot + 1
        endloop
        set itm = null
    endif

    call GroupAddUnit(udg_FakeHeroGroup, clone)
    if udg_Ninja_CloneGroup[pId] == null then
        set udg_Ninja_CloneGroup[pId] = CreateGroup()
    endif
    call GroupAddUnit(udg_Ninja_CloneGroup[pId], clone)

    call UnitApplyTimedLife(clone, 'BTLF', dur)
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))

    set trueHero = null
    return clone
endfunction

function Ninja_PickLivingClone takes integer pId returns unit
    local group g = udg_Ninja_CloneGroup[pId]
    local group tempG = null
    local unit u = null
    local unit pick = null

    if g == null then
        return null
    endif

    set tempG = CreateGroup()
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
            if pick == null then
                set pick = u
            endif
            call GroupAddUnit(tempG, u)
        endif
    endloop

    loop
        set u = FirstOfGroup(tempG)
        exitwhen u == null
        call GroupRemoveUnit(tempG, u)
        call GroupAddUnit(g, u)
    endloop

    call DestroyGroup(tempG)
    set tempG = null
    set g = null
    return pick
endfunction

function Ninja_FindKarmaIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_KarmaCount
        if udg_KarmaUnit[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    return -1
endfunction

function Ninja_RemoveKarmaIndex takes integer idx returns nothing
    if idx >= 0 and idx < udg_KarmaCount then
        set udg_KarmaUnit[idx] = udg_KarmaUnit[udg_KarmaCount - 1]
        set udg_KarmaOwner[idx] = udg_KarmaOwner[udg_KarmaCount - 1]
        set udg_KarmaLevel[idx] = udg_KarmaLevel[udg_KarmaCount - 1]
        set udg_KarmaUnit[udg_KarmaCount - 1] = null
        set udg_KarmaOwner[udg_KarmaCount - 1] = null
        set udg_KarmaCount = udg_KarmaCount - 1
    endif
endfunction

function Ninja_MarkKarma takes unit killer, player ninjaOwner, integer lv returns nothing
    local integer idx = -1
    if killer == null or IsUnitType(killer, UNIT_TYPE_STRUCTURE) or GetUnitTypeId(killer) == 'u000' then
        return
    endif
    set idx = Ninja_FindKarmaIndex(killer)
    if idx >= 0 then
        set udg_KarmaOwner[idx] = ninjaOwner
        if lv > udg_KarmaLevel[idx] then
            set udg_KarmaLevel[idx] = lv
        endif
    else
        if udg_KarmaCount < 128 then
            set udg_KarmaUnit[udg_KarmaCount] = killer
            set udg_KarmaOwner[udg_KarmaCount] = ninjaOwner
            set udg_KarmaLevel[udg_KarmaCount] = lv
            set udg_KarmaCount = udg_KarmaCount + 1
        endif
    endif
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Curse\\\\CurseTarget.mdl", killer, "overhead"))
endfunction

function Ninja_OnHeroSkill takes nothing returns boolean
    local unit hero = GetTriggerUnit()
    local integer pId = 0
    if GetUnitTypeId(hero) == 'H003' then
        set pId = GetPlayerId(GetOwningPlayer(hero))
        if not IsUnitInGroup(hero, udg_FakeHeroGroup) and not IsUnitIllusion(hero) then
            set udg_Ninja_TrueHero[pId] = hero
        endif
        if GetLearnedSkill() == 'A012' and GetUnitAbilityLevel(hero, 'A012') == 1 then
            set udg_Ninja_AuraOn[pId] = true
            if udg_Ninja_AuraFx[pId] == null then
                set udg_Ninja_AuraFx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", hero, "origin")
            endif
        endif
    endif
    set hero = null
    return false
endfunction

"""
    content = content[:idx] + ninja_funcs + content[idx:]

    # 3. Replace DM_StealthLoop
    old_stealth_loop = """function DM_StealthLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local player p = null
    local unit dummy = null
    local integer hIdx = -1
    local boolean hasAgh = false
    local integer lv = 1
    local real dur = 30.0

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
endfunction"""

    new_stealth_loop = """function DM_StealthLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local player p = null
    local unit dummy = null
    local integer hIdx = -1
    local boolean hasAgh = false
    local integer lv = 1
    local real dur = 30.0

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
endfunction"""

    assert old_stealth_loop in content, "old_stealth_loop not found!"
    content = content.replace(old_stealth_loop, new_stealth_loop, 1)

    # 4. Replace DM_CapTimerLoop
    old_cap_loop = """function DM_CapTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
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
endfunction"""

    new_cap_loop = """function DM_CapTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local integer pId = 0
    local unit th = null
    local unit dmgSrc = null
    local integer aLv = 0
    local real pct = 0.0
    local real drain = 0.0
    local unit enumU = null

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
                            if GetWidgetLife(enumU) > (drain + 1.0) then
                                call SetWidgetLife(enumU, GetWidgetLife(enumU) - drain)
                            else
                                call UnitDamageTarget(dmgSrc, enumU, drain + 100.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_UNIVERSAL, WEAPON_TYPE_WHOKNOWS)
                            endif
                        endif
                    endloop
                endif
            endif
        endif
        set pId = pId + 1
    endloop
endfunction"""

    assert old_cap_loop in content, "old_cap_loop not found!"
    content = content.replace(old_cap_loop, new_cap_loop, 1)

    # 5. Replace DM_OnSpellEffect
    old_spell_effect = """function DM_OnSpellEffect takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer abil = GetSpellAbilityId()

    if abil == 'A001' then
        call DM_OnCastMirror(caster)
    elseif abil == 'A002' then
        call DM_CastPossession(caster, GetSpellTargetUnit())
    elseif abil == 'A003' then
        call DM_CastMassIllusion(caster, GetSpellTargetX(), GetSpellTargetY())
    endif

    set caster = null
    return false
endfunction"""

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
        if udg_Ninja_CloneGroup[pId] == null then
            set udg_Ninja_CloneGroup[pId] = CreateGroup()
        endif
        call GroupAddUnit(udg_Ninja_CloneGroup[pId], ult)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\Vengeance\\\\VengeanceAvenger.mdl", ult, "origin"))
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", GetUnitX(ult), GetUnitY(ult)))
        set ult = null
    endif

    set caster = null
    return false
endfunction"""

    assert old_spell_effect in content, "old_spell_effect not found!"
    content = content.replace(old_spell_effect, new_spell_effect, 1)

    # 6. Replace DM_OnDamaged
    old_damaged = """function DM_OnDamaged takes nothing returns boolean
    local unit src = GetEventDamageSource()
    local unit tgt = GetTriggerUnit()
    local integer hIdx = -1
    if src != null and tgt != null and GetEventDamage() > 0.0 then
        set hIdx = DM_GetHeroIndex(src)
        if hIdx >= 0 and udg_DM_InStealth[hIdx] then
            call DM_BreakInvisibility(src, tgt)
        endif
    endif
    set src = null
    set tgt = null
    return false
endfunction"""

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

    if src != null and tgt != null and GetEventDamage() > 0.0 then
        set hIdx = DM_GetHeroIndex(src)
        if hIdx >= 0 and udg_DM_InStealth[hIdx] then
            call DM_BreakInvisibility(src, tgt)
        endif

        // 魔音同化 (A011) - 真身不死转移 (Pre-lethal swap)
        if GetUnitTypeId(tgt) == 'H003' and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and not IsUnitIllusion(tgt) then
            set pId = GetPlayerId(GetOwningPlayer(tgt))
            set udg_Ninja_TrueHero[pId] = tgt
            if GetEventDamage() >= (GetWidgetLife(tgt) - 1.0) then
                set c = Ninja_PickLivingClone(pId)
                if c != null then
                    // 他化自在 (A013) 记录凶手
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

    assert old_damaged in content, "old_damaged not found!"
    content = content.replace(old_damaged, new_damaged, 1)

    # 7. Replace DM_OnUnitDeath
    old_death = """function DM_OnUnitDeath takes nothing returns boolean
    local unit dead = GetTriggerUnit()
    local integer idx = DM_FindCapIndex(dead)
    if idx >= 0 then
        call SetUnitOwner(dead, udg_CapOrigOwner[idx], true)
        call DM_RemoveCapIndex(idx)
    endif
    if IsUnitInGroup(dead, udg_FakeHeroGroup) then
        call GroupRemoveUnit(udg_FakeHeroGroup, dead)
        call SetUnitOwner(dead, Player(PLAYER_NEUTRAL_PASSIVE), false)
        call SetUnitExploded(dead, true)
        call RemoveUnit(dead)
    endif
    set dead = null
    return false
endfunction"""

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

    // 2. 他化自在 (A013) - 击杀魔音忍者者被烙印因果
    if deadType == 'H003' and killer != null and IsUnitEnemy(killer, deadOwner) then
        set th = Ninja_GetTrueHero(deadOwner)
        set eLv = GetUnitAbilityLevel(dead, 'A013')
        if th != null and GetUnitAbilityLevel(th, 'A013') > eLv then
            set eLv = GetUnitAbilityLevel(th, 'A013')
        endif
        if eLv > 0 then
            call Ninja_MarkKarma(killer, deadOwner, eLv)
        endif
    endif

    // 3. 他化自在 (A013) - 因果单位死亡化为魔音忍者
    set kIdx = Ninja_FindKarmaIndex(dead)
    if kIdx >= 0 then
        set ko = udg_KarmaOwner[kIdx]
        set klv = udg_KarmaLevel[kIdx]
        call Ninja_RemoveKarmaIndex(kIdx)
        call Ninja_SpawnClone(ko, deadX, deadY, deadFacing)
        if klv >= 3 then
            call Ninja_SpawnClone(ko, deadX + 45.0, deadY + 45.0, deadFacing)
        endif
        set ko = null
    endif

    // 4. 魔音同化 (A011) - 击杀单位生成伪英雄分身
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and deadType != 'u000' and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u001') then
        set kp = GetOwningPlayer(killer)
        set th = Ninja_GetTrueHero(kp)
        if GetUnitAbilityLevel(killer, 'A011') > 0 or (th != null and GetUnitAbilityLevel(th, 'A011') > 0) or GetUnitTypeId(killer) == 'u001' then
            call Ninja_SpawnClone(kp, deadX, deadY, deadFacing)
        endif
        set kp = null
        set th = null
    endif

    // 5. 魔音同化 (A011) - 真身死亡 Fallback
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
    if isFakeHero then
        if udg_Ninja_CloneGroup[deadPId] != null then
            call GroupRemoveUnit(udg_Ninja_CloneGroup[deadPId], dead)
        endif
        call GroupRemoveUnit(udg_FakeHeroGroup, dead)
        call SetUnitOwner(dead, Player(PLAYER_NEUTRAL_PASSIVE), false)
        call SetUnitExploded(dead, true)
        call RemoveUnit(dead)
    endif

    set dead = null
    set killer = null
    set deadOwner = null
    return false
endfunction"""

    assert old_death in content, "old_death not found!"
    content = content.replace(old_death, new_death, 1)

    # 8. Replace DM_InitTriggers
    old_init = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()

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

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tmrCap = null
    set tmrStealth = null
endfunction"""

    new_init = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tSkill = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()
    local integer i = 0

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()

    set i = 0
    loop
        exitwhen i > 15
        set udg_Ninja_CloneGroup[i] = CreateGroup()
        set udg_Ninja_AuraOn[i] = false
        set udg_Ninja_AuraFx[i] = null
        set udg_Ninja_TrueHero[i] = null
        set i = i + 1
    endloop

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

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tSkill = null
    set tmrCap = null
    set tmrStealth = null
endfunction"""

    assert old_init in content, "old_init not found!"
    content = content.replace(old_init, new_init, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully updated payload/war3map.j!")

if __name__ == '__main__':
    main()
