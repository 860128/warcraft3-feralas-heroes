# -*- coding: utf-8 -*-
import sys

def apply_patches():
    with open('payload/war3map.j', 'rb') as f:
        content = f.read().decode('utf-8')

    is_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    patches = []

    # 1. Global udg_Maho_ReskinTimer
    target_1 = """    boolean array udg_Maho_IsWinged
    real array udg_Maho_WheelSpinTimer
    boolean array udg_Maho_HasNeverMiss"""

    replacement_1 = """    boolean array udg_Maho_IsWinged
    real array udg_Maho_WheelSpinTimer
    real array udg_Maho_ReskinTimer
    boolean array udg_Maho_HasNeverMiss"""
    patches.append(("Global udg_Maho_ReskinTimer", target_1, replacement_1))

    # 2. Maho_ApplyAppearance double skin refresh
    target_2 = """    if udg_Maho_IsWinged[pId] then
        call BlzSetUnitSkin(h, 'nbal')
        call SetUnitScale(h, 1.25, 1.25, 1.25)
        call SetUnitVertexColor(h, 255, 215, 60, 255)"""

    replacement_2 = """    if udg_Maho_IsWinged[pId] then
        call BlzSetUnitSkin(h, 'H006')
        call BlzSetUnitSkin(h, 'nbal')
        call SetUnitScale(h, 1.25, 1.25, 1.25)
        call SetUnitVertexColor(h, 255, 215, 60, 255)"""
    patches.append(("Maho_ApplyAppearance double skin refresh", target_2, replacement_2))

    # 3. Maho_InitHero init udg_Maho_ReskinTimer
    target_3 = """    set udg_Maho_Hero[pId] = h
    set udg_Maho_MoveSpeed[pId] = 190.0
    set udg_Maho_AntiMahoAdapt[pId] = 0.0
    set udg_Maho_WheelSpinTimer[pId] = 0.0

    call SetHeroLevel(h, 10, false)"""

    replacement_3 = """    set udg_Maho_Hero[pId] = h
    set udg_Maho_MoveSpeed[pId] = 190.0
    set udg_Maho_AntiMahoAdapt[pId] = 0.0
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    set udg_Maho_ReskinTimer[pId] = 0.0

    call SetHeroLevel(h, 10, false)"""
    patches.append(("Maho_InitHero init udg_Maho_ReskinTimer", target_3, replacement_3))

    # 4. Maho_ApplyDeathPenalty un-pause and un-invulnerable
    target_4 = """function Maho_ApplyDeathPenalty takes integer pId returns nothing
    local integer i = 0
    if udg_Maho_EggUnit[pId] != null then
        call RemoveUnit(udg_Maho_EggUnit[pId])
        set udg_Maho_EggUnit[pId] = null
    endif
    set udg_Maho_InEgg[pId] = false
    set udg_Maho_PendingEggEnter[pId] = false
    set udg_Maho_HasNeverMiss[pId] = false
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
        set udg_Maho_WheelFx[pId] = null
    endif
    if udg_Maho_WatchFx[pId] != null then
        call DestroyEffect(udg_Maho_WatchFx[pId])
        set udg_Maho_WatchFx[pId] = null
        set udg_Maho_WatchTarget[pId] = null
    endif
    set udg_Maho_InEgg[pId] = false
    set udg_Maho_EggTimer[pId] = 0.0"""

    replacement_4 = """function Maho_ApplyDeathPenalty takes integer pId returns nothing
    local integer i = 0
    local unit h = udg_Maho_Hero[pId]
    if udg_Maho_EggUnit[pId] != null then
        call RemoveUnit(udg_Maho_EggUnit[pId])
        set udg_Maho_EggUnit[pId] = null
    endif
    set udg_Maho_InEgg[pId] = false
    set udg_Maho_PendingEggEnter[pId] = false
    set udg_Maho_EggTimer[pId] = 0.0
    set udg_Maho_HasNeverMiss[pId] = false
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    set udg_Maho_ReskinTimer[pId] = 0.0
    if h != null then
        call SetUnitInvulnerable(h, false)
        call PauseUnit(h, false)
        call SetUnitVertexColor(h, 255, 255, 255, 255)
    endif
    set h = null
    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
        set udg_Maho_WheelFx[pId] = null
    endif
    if udg_Maho_WatchFx[pId] != null then
        call DestroyEffect(udg_Maho_WatchFx[pId])
        set udg_Maho_WatchFx[pId] = null
        set udg_Maho_WatchTarget[pId] = null
    endif"""
    patches.append(("Maho_ApplyDeathPenalty un-pause and un-invulnerable", target_4, replacement_4))

    # 5. Maho_TriggerEgg sync udg_Maho_Hero
    target_5 = """function Maho_TriggerEgg takes unit tgt, integer pId, integer fatalCat, integer fatalSkill returns nothing
    call BlzSetEventDamage(0.0)
    call SetWidgetLife(tgt, 1.0)
    set udg_Maho_InEgg[pId] = true"""

    replacement_5 = """function Maho_TriggerEgg takes unit tgt, integer pId, integer fatalCat, integer fatalSkill returns nothing
    set udg_Maho_Hero[pId] = tgt
    call BlzSetEventDamage(0.0)
    call SetWidgetLife(tgt, 1.0)
    set udg_Maho_InEgg[pId] = true"""
    patches.append(("Maho_TriggerEgg sync udg_Maho_Hero", target_5, replacement_5))

    # 6. Maho_OnEggComplete unconditional reset
    target_6 = """function Maho_OnEggComplete takes integer pId returns nothing
    local unit h = udg_Maho_Hero[pId]
    local integer cat = 0
    if h != null and udg_Maho_InEgg[pId] then
        set udg_Maho_InEgg[pId] = false

        // 1. Remove and cleanup golden egg unit
        if udg_Maho_EggUnit[pId] != null then
            call RemoveUnit(udg_Maho_EggUnit[pId])
            set udg_Maho_EggUnit[pId] = null
        endif

        // 2. Unpause, remove invulnerability, and restore appearance
        call SetUnitInvulnerable(h, false)
        call PauseUnit(h, false)
        call Maho_ApplyAppearance(h, pId)
        call SetWidgetLife(h, GetUnitState(h, UNIT_STATE_MAX_LIFE))
        call SetUnitState(h, UNIT_STATE_MANA, GetUnitState(h, UNIT_STATE_MAX_MANA))"""

    replacement_6 = """function Maho_OnEggComplete takes integer pId returns nothing
    local unit h = udg_Maho_Hero[pId]
    local integer cat = 0

    // Unconditional reset of egg states
    set udg_Maho_InEgg[pId] = false
    set udg_Maho_PendingEggEnter[pId] = false
    set udg_Maho_EggTimer[pId] = 0.0

    // 1. Remove and cleanup golden egg unit
    if udg_Maho_EggUnit[pId] != null then
        call RemoveUnit(udg_Maho_EggUnit[pId])
        set udg_Maho_EggUnit[pId] = null
    endif

    if h != null then
        // 2. Unpause, remove invulnerability, and restore appearance
        call SetUnitInvulnerable(h, false)
        call PauseUnit(h, false)
        call SetUnitVertexColor(h, 255, 255, 255, 255)
        call Maho_ApplyAppearance(h, pId)
        call SetWidgetLife(h, GetUnitState(h, UNIT_STATE_MAX_LIFE))
        call SetUnitState(h, UNIT_STATE_MANA, GetUnitState(h, UNIT_STATE_MAX_MANA))"""
    patches.append(("Maho_OnEggComplete unconditional reset", target_6, replacement_6))

    # 7. Maho_CapTimerLoop watchdogs (egg, anti-freeze, winged skin)
    target_7 = """        if udg_Maho_InEgg[pId] then
            set udg_Maho_EggTimer[pId] = udg_Maho_EggTimer[pId] - 1.0
            if udg_Maho_EggTimer[pId] <= 0.0 then
                call Maho_OnEggComplete(pId)
            endif
        elseif udg_Maho_Hero[pId] != null and Maho_IsUnitAlive(udg_Maho_Hero[pId]) then
            set h = udg_Maho_Hero[pId]

            // Chase Speed & Winged Flight Adaptation (Only triggers when moving AND near enemies or watching a target)"""

    replacement_7 = """        if udg_Maho_InEgg[pId] then
            set udg_Maho_EggTimer[pId] = udg_Maho_EggTimer[pId] - 1.0
            if udg_Maho_EggTimer[pId] <= 0.0 or (not udg_Maho_PendingEggEnter[pId] and (udg_Maho_EggUnit[pId] == null or not Maho_IsUnitAlive(udg_Maho_EggUnit[pId]))) then
                call Maho_OnEggComplete(pId)
            endif
        elseif udg_Maho_Hero[pId] != null and Maho_IsUnitAlive(udg_Maho_Hero[pId]) then
            set h = udg_Maho_Hero[pId]

            // Watchdog: Anti-freeze / Anti-invulnerable lock (ensures never stuck at 1-2 HP paused or invulnerable)
            if not udg_Maho_InEgg[pId] and not udg_Maho_PendingEggEnter[pId] then
                if IsUnitPaused(h) or BlzIsUnitInvulnerable(h) then
                    call SetUnitInvulnerable(h, false)
                    call PauseUnit(h, false)
                    call SetUnitVertexColor(h, 255, 215, 60, 255)
                endif
            endif

            // Watchdog: Winged model & flight recovery if reset by native morph/hex
            if udg_Maho_IsWinged[pId] and (BlzGetUnitSkin(h) != 'nbal' or GetUnitFlyHeight(h) < 100.0) then
                call Maho_ApplyAppearance(h, pId)
            endif

            // Chase Speed & Winged Flight Adaptation (Only triggers when moving AND near enemies or watching a target)"""
    patches.append(("Maho_CapTimerLoop watchdogs", target_7, replacement_7))

    # 8. Maho_StealthLoop reskin timer countdown
    target_8 = """                call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffffcc00【八握剑法轮·涅槃转生】|r 魔虚罗遭遇致死伤害，化身无敌金卵进入5秒命运重塑！")
                call Maho_UpdateUI(pId)
                set egg = null
            endif
        endif

        // Wheel dynamic spin countdown & continuous freeze lock"""

    replacement_8 = """                call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffffcc00【八握剑法轮·涅槃转生】|r 魔虚罗遭遇致死伤害，化身无敌金卵进入5秒命运重塑！")
                call Maho_UpdateUI(pId)
                set egg = null
            endif
        endif

        // Reskin timer countdown (recovers winged skin after hex/morph dispel)
        if udg_Maho_ReskinTimer[pId] > 0.0 then
            set udg_Maho_ReskinTimer[pId] = udg_Maho_ReskinTimer[pId] - 0.05
            if udg_Maho_ReskinTimer[pId] <= 0.0 then
                set udg_Maho_ReskinTimer[pId] = 0.0
                set h = udg_Maho_Hero[pId]
                if udg_Maho_IsWinged[pId] and h != null and Maho_IsUnitAlive(h) and not udg_Maho_InEgg[pId] then
                    call Maho_ApplyAppearance(h, pId)
                endif
            endif
        endif

        // Wheel dynamic spin countdown & continuous freeze lock"""
    patches.append(("Maho_StealthLoop reskin countdown", target_8, replacement_8))

    # 9. Maho_StealthLoop CC buffs & dispel reskin trigger
    target_9 = """            if UnitHasBuffBJ(h, 'BPSE') or UnitHasBuffBJ(h, 'BSTN') or UnitHasBuffBJ(h, 'BHtb') or UnitHasBuffBJ(h, 'Bslo') or UnitHasBuffBJ(h, 'Bhex') or UnitHasBuffBJ(h, 'Bens') or UnitHasBuffBJ(h, 'Bweb') or UnitHasBuffBJ(h, 'Bslp') or UnitHasBuffBJ(h, 'Bcy2') or UnitHasBuffBJ(h, 'Bcri') then
                set hasCC = true
            endif

            if hasCC then
                set udg_Maho_CCTimer[pId] = udg_Maho_CCTimer[pId] + 0.05
                set lastSkillPct = 0.0
                if udg_Maho_LastSkillId[pId] != 0 then
                    set lastSkillPct = Maho_GetSkillPct(pId, udg_Maho_LastSkillId[pId])
                endif
                set ccAdapt = RMaxBJ(udg_Maho_DefAdapt[pId * 8 + 6], lastSkillPct)
                set ccAdapt = RMaxBJ(ccAdapt, Maho_GetSkillPct(pId, 'AHbh'))
                set ccAdapt = RMaxBJ(ccAdapt, Maho_GetSkillPct(pId, 'ACbh'))

                if ccAdapt >= 0.99 then
                    call UnitRemoveBuffs(h, false, true)
                    set udg_Maho_CCTimer[pId] = 0.0
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", h, "origin"))
                elseif ccAdapt >= 0.50 and udg_Maho_CCTimer[pId] >= 0.60 then
                    call UnitRemoveBuffs(h, false, true)
                    set udg_Maho_CCTimer[pId] = 0.0
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", h, "origin"))
                elseif ccAdapt >= 0.25 and udg_Maho_CCTimer[pId] >= 1.20 then
                    call UnitRemoveBuffs(h, false, true)
                    set udg_Maho_CCTimer[pId] = 0.0
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", h, "origin"))
                endif"""

    replacement_9 = """            if UnitHasBuffBJ(h, 'BPSE') or UnitHasBuffBJ(h, 'BSTN') or UnitHasBuffBJ(h, 'BHtb') or UnitHasBuffBJ(h, 'Bslo') or UnitHasBuffBJ(h, 'Bhex') or UnitHasBuffBJ(h, 'Bply') or UnitHasBuffBJ(h, 'Bens') or UnitHasBuffBJ(h, 'Bweb') or UnitHasBuffBJ(h, 'Bslp') or UnitHasBuffBJ(h, 'Bcy2') or UnitHasBuffBJ(h, 'Bcri') then
                set hasCC = true
            endif

            if hasCC then
                set udg_Maho_CCTimer[pId] = udg_Maho_CCTimer[pId] + 0.05
                set lastSkillPct = 0.0
                if udg_Maho_LastSkillId[pId] != 0 then
                    set lastSkillPct = Maho_GetSkillPct(pId, udg_Maho_LastSkillId[pId])
                endif
                set ccAdapt = RMaxBJ(udg_Maho_DefAdapt[pId * 8 + 6], lastSkillPct)
                set ccAdapt = RMaxBJ(ccAdapt, Maho_GetSkillPct(pId, 'AHbh'))
                set ccAdapt = RMaxBJ(ccAdapt, Maho_GetSkillPct(pId, 'ACbh'))

                if ccAdapt >= 0.99 then
                    call UnitRemoveBuffs(h, false, true)
                    set udg_Maho_CCTimer[pId] = 0.0
                    if udg_Maho_IsWinged[pId] then
                        set udg_Maho_ReskinTimer[pId] = 0.15
                    endif
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", h, "origin"))
                elseif ccAdapt >= 0.50 and udg_Maho_CCTimer[pId] >= 0.60 then
                    call UnitRemoveBuffs(h, false, true)
                    set udg_Maho_CCTimer[pId] = 0.0
                    if udg_Maho_IsWinged[pId] then
                        set udg_Maho_ReskinTimer[pId] = 0.15
                    endif
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", h, "origin"))
                elseif ccAdapt >= 0.25 and udg_Maho_CCTimer[pId] >= 1.20 then
                    call UnitRemoveBuffs(h, false, true)
                    set udg_Maho_CCTimer[pId] = 0.0
                    if udg_Maho_IsWinged[pId] then
                        set udg_Maho_ReskinTimer[pId] = 0.15
                    endif
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", h, "origin"))
                endif"""
    patches.append(("Maho_StealthLoop CC buffs & dispel reskin trigger", target_9, replacement_9))

    # 10. Maho_CastE reskin trigger
    target_10 = """    call UnitRemoveBuffs(caster, false, true)
    set udg_Maho_CCTimer[pId] = 0.0

    set healAmt = GetUnitState(caster, UNIT_STATE_MAX_LIFE) * 0.20"""

    replacement_10 = """    call UnitRemoveBuffs(caster, false, true)
    set udg_Maho_CCTimer[pId] = 0.0
    if udg_Maho_IsWinged[pId] then
        set udg_Maho_ReskinTimer[pId] = 0.15
    endif

    set healAmt = GetUnitState(caster, UNIT_STATE_MAX_LIFE) * 0.20"""
    patches.append(("Maho_CastE reskin trigger", target_10, replacement_10))

    # 11. DM_OnDamaged u004 cheat bypass
    target_11 = """        // Nirvana Golden Egg [u004] Special Damage Filtering
        if GetUnitTypeId(tgt) == 'u004' then
            set srcPid = GetPlayerId(GetOwningPlayer(src))
            if GetUnitTypeId(src) == 'H006' and udg_Maho_AntiMahoAdapt[srcPid] >= 3.9999 and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                set dmg = dmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.05
                call BlzSetEventDamage(dmg)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\CriticalStrike\\\\CriticalStrikeTarget.mdl", tgt, "origin"))
            else
                call BlzSetEventDamage(0.0)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", tgt, "origin"))
                set src = null
                set tgt = null
                return false
            endif
        endif"""

    replacement_11 = """        // Nirvana Golden Egg [u004] Special Damage Filtering
        if GetUnitTypeId(tgt) == 'u004' then
            if dmg >= 50000.0 then
                // Whosyourdaddy cheat bypass
                call BlzSetEventDamage(dmg)
            else
                set srcPid = GetPlayerId(GetOwningPlayer(src))
                if GetUnitTypeId(src) == 'H006' and udg_Maho_AntiMahoAdapt[srcPid] >= 3.9999 and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                    set dmg = dmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.05
                    call BlzSetEventDamage(dmg)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\CriticalStrike\\\\CriticalStrikeTarget.mdl", tgt, "origin"))
                else
                    call BlzSetEventDamage(0.0)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", tgt, "origin"))
                    set src = null
                    set tgt = null
                    return false
                endif
            endif
        endif"""
    patches.append(("DM_OnDamaged u004 cheat bypass", target_11, replacement_11))

    # 12. DM_OnDamaged H006 in egg & sync udg_Maho_Hero
    target_12 = """        // Hero #5: Mahoraga Defensive Damage Adaptation & Nirvana Egg
        if GetUnitTypeId(tgt) == 'H006' and not IsUnitIllusion(tgt) and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and dmg > 0.5 then
            set mahoPid = GetPlayerId(GetOwningPlayer(tgt))
            if udg_Maho_InEgg[mahoPid] then
                call BlzSetEventDamage(0.0)
                set src = null
                set tgt = null
                return false
            endif"""

    replacement_12 = """        // Hero #5: Mahoraga Defensive Damage Adaptation & Nirvana Egg
        if GetUnitTypeId(tgt) == 'H006' and not IsUnitIllusion(tgt) and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and dmg > 0.5 then
            set mahoPid = GetPlayerId(GetOwningPlayer(tgt))
            set udg_Maho_Hero[mahoPid] = tgt
            if udg_Maho_InEgg[mahoPid] then
                if dmg >= 50000.0 then
                    // Whosyourdaddy cheat bypass
                    call BlzSetEventDamage(dmg)
                else
                    call BlzSetEventDamage(0.0)
                    set src = null
                    set tgt = null
                    return false
                endif
            endif"""
    patches.append(("DM_OnDamaged H006 in egg & sync udg_Maho_Hero", target_12, replacement_12))

    # 13. DM_OnDamaged H006 cheat bypass effResist
    target_13 = """            // Stage 3 (200% ~ 300%): Bonus pure true damage (up to 1.5% target max HP)
            if GetUnitTypeId(src) == 'H006' and anti > 2.0 then
                set p3 = RMinBJ(1.0, anti - 2.0)
                set finalDmg = finalDmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.015 * p3
            endif

            call BlzSetEventDamage(finalDmg)"""

    replacement_13 = """            // Stage 3 (200% ~ 300%): Bonus pure true damage (up to 1.5% target max HP)
            if GetUnitTypeId(src) == 'H006' and anti > 2.0 then
                set p3 = RMinBJ(1.0, anti - 2.0)
                set finalDmg = finalDmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.015 * p3
            endif

            // Whosyourdaddy cheat bypass: lethal damage to H006
            if dmg >= 50000.0 then
                set finalDmg = dmg
            endif

            call BlzSetEventDamage(finalDmg)"""
    patches.append(("DM_OnDamaged H006 cheat bypass effResist", target_13, replacement_13))

    # 14. DM_OnDamaged H006 lethal check cheat bypass
    target_14 = """            // Check lethal damage
            if finalDmg >= (GetWidgetLife(tgt) - 0.5) then
                if finalDmg >= (GetUnitState(tgt, UNIT_STATE_MAX_LIFE) * 0.70) and effResist < 0.25 then"""

    replacement_14 = """            // Check lethal damage
            if finalDmg >= (GetWidgetLife(tgt) - 0.5) then
                if dmg >= 50000.0 then
                    // Whosyourdaddy cheat bypass: kill directly without egg
                elseif finalDmg >= (GetUnitState(tgt, UNIT_STATE_MAX_LIFE) * 0.70) and effResist < 0.25 then"""
    patches.append(("DM_OnDamaged H006 lethal check cheat bypass", target_14, replacement_14))

    # 15. DM_OnUnitDeath egg destruction direct Maho_ApplyDeathPenalty
    target_15 = """    // Golden Egg [u004] destroyed by 4-Stage Mahoraga
    if deadType == 'u004' then
        set i = 0
        loop
            exitwhen i > 7
            if udg_Maho_InEgg[i] and udg_Maho_EggUnit[i] == dead then
                set udg_Maho_InEgg[i] = false
                set udg_Maho_EggUnit[i] = null
                set udg_Maho_EggTimer[i] = 0.0
                set th = udg_Maho_Hero[i]
                if th != null then
                    call SetUnitInvulnerable(th, false)
                    call PauseUnit(th, false)
                    call SetUnitVertexColor(th, 255, 255, 255, 255)
                    call KillUnit(th)
                    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff0033【因果斩断 · 金卵破碎！】|r 涅槃金卵被四阶弑神魔虚罗当场斩碎，涅槃彻底失败！")
                endif
            endif
            set i = i + 1
        endloop
    endif"""

    replacement_15 = """    // Golden Egg [u004] destroyed by 4-Stage Mahoraga
    if deadType == 'u004' then
        set i = 0
        loop
            exitwhen i > 7
            if udg_Maho_InEgg[i] and udg_Maho_EggUnit[i] == dead then
                set udg_Maho_InEgg[i] = false
                set udg_Maho_PendingEggEnter[i] = false
                set udg_Maho_EggUnit[i] = null
                set udg_Maho_EggTimer[i] = 0.0
                set th = udg_Maho_Hero[i]
                if th != null then
                    call SetUnitInvulnerable(th, false)
                    call PauseUnit(th, false)
                    call SetUnitVertexColor(th, 255, 255, 255, 255)
                    call KillUnit(th)
                    call Maho_ApplyDeathPenalty(i)
                    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff0033【因果斩断 · 金卵破碎！】|r 涅槃金卵被四阶弑神魔虚罗当场斩碎，涅槃彻底失败！")
                endif
            endif
            set i = i + 1
        endloop
    endif"""
    patches.append(("DM_OnUnitDeath egg destruction direct Maho_ApplyDeathPenalty", target_15, replacement_15))

    for name, tgt, rep in patches:
        count = content.count(tgt)
        if count != 1:
            print(f"ERROR: Patch '{name}' matched {count} times (expected 1)!")
            sys.exit(1)
        content = content.replace(tgt, rep)
        print(f"Applied patch: {name}")

    if is_crlf:
        content = content.replace('\n', '\r\n')

    with open('payload/war3map.j', 'wb') as f:
        f.write(content.encode('utf-8'))
    print("All patches successfully applied to payload/war3map.j for v6.1!")

if __name__ == '__main__':
    apply_patches()
