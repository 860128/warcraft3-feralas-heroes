# -*- coding: utf-8 -*-
import sys
import re

jass_path = 'payload/war3map.j'
with open(jass_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add globals
old_globals = """    integer array udg_Maho_FlyProgress
    boolean array udg_Maho_IsWinged"""

new_globals = """    integer array udg_Maho_FlyProgress
    boolean array udg_Maho_IsWinged
    real array udg_Maho_WheelSpinTimer
    boolean array udg_Maho_HasNeverMiss"""

assert old_globals in content, "Globals anchor not found!"
content = content.replace(old_globals, new_globals, 1)

# 2. Add Maho_TriggerWheelSpin & update Maho_ApplyAppearance
old_appear = """function Maho_ApplyAppearance takes unit h, integer pId returns nothing
    if h == null then
        return
    endif
    if udg_Maho_IsWinged[pId] then
        call BlzSetUnitSkin(h, 'nbal')
        call SetUnitScale(h, 1.25, 1.25, 1.25)
        call SetUnitVertexColor(h, 255, 215, 60, 255)
        call UnitAddAbility(h, 'Amrf')
        call UnitRemoveAbility(h, 'Amrf')
        call SetUnitFlyHeight(h, 240.0, 400.0)
        call SetUnitPathing(h, false)
        if not udg_Maho_AntiAirUnlocked[pId] then
            set udg_Maho_AntiAirUnlocked[pId] = true
            call UnitAddAbility(h, 'A045')
            call UnitMakeAbilityPermanent(h, true, 'A045')
            call SetUnitAcquireRange(h, 650.0)
        endif
    else
        call BlzSetUnitSkin(h, 'H006')
        call SetUnitScale(h, 1.25, 1.25, 1.25)
        call SetUnitVertexColor(h, 255, 215, 60, 255)
        call UnitAddAbility(h, 'Amrf')
        call UnitRemoveAbility(h, 'Amrf')
        call SetUnitFlyHeight(h, 0.0, 400.0)
        call SetUnitPathing(h, true)
    endif
    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
    endif
    set udg_Maho_WheelFx[pId] = AddSpecialEffectTarget("war3mapImported\\\\MahoWheel.mdx", h, "overhead")
    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])
endfunction"""

new_appear = """function Maho_TriggerWheelSpin takes integer pId, real duration, real speed returns nothing
    if udg_Maho_WheelFx[pId] != null then
        call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], speed)
        if duration > udg_Maho_WheelSpinTimer[pId] then
            set udg_Maho_WheelSpinTimer[pId] = duration
        endif
    endif
endfunction

function Maho_ApplyAppearance takes unit h, integer pId returns nothing
    if h == null then
        return
    endif
    if udg_Maho_IsWinged[pId] then
        call BlzSetUnitSkin(h, 'nbal')
        call SetUnitScale(h, 1.25, 1.25, 1.25)
        call SetUnitVertexColor(h, 255, 215, 60, 255)
        call UnitAddAbility(h, 'Amrf')
        call UnitRemoveAbility(h, 'Amrf')
        call SetUnitFlyHeight(h, 240.0, 400.0)
        call SetUnitPathing(h, false)
        if not udg_Maho_AntiAirUnlocked[pId] then
            set udg_Maho_AntiAirUnlocked[pId] = true
            call UnitAddAbility(h, 'A045')
            call UnitMakeAbilityPermanent(h, true, 'A045')
            call SetUnitAcquireRange(h, 650.0)
        endif
    else
        call BlzSetUnitSkin(h, 'H006')
        call SetUnitScale(h, 1.25, 1.25, 1.25)
        call SetUnitVertexColor(h, 255, 215, 60, 255)
        call UnitAddAbility(h, 'Amrf')
        call UnitRemoveAbility(h, 'Amrf')
        call SetUnitFlyHeight(h, 0.0, 400.0)
        call SetUnitPathing(h, true)
    endif
    if udg_Maho_HasNeverMiss[pId] then
        call UnitAddAbility(h, 'A046')
        call UnitMakeAbilityPermanent(h, true, 'A046')
    endif
    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
    endif
    set udg_Maho_WheelFx[pId] = AddSpecialEffectTarget("war3mapImported\\\\MahoWheel.mdx", h, "overhead")
    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0)
    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])
endfunction"""

assert old_appear in content, "Appearance anchor not found!"
content = content.replace(old_appear, new_appear, 1)

# 3. Update Maho_AddDefAdapt to trigger wheel spin
old_def_adapt = """    if cur >= 0.9999 then
        set cur = 1.00
        set udg_Maho_DefAdapt[pId * 8 + cat] = 1.00
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffffcc00【八握剑法轮·绝对免疫达成！】|r 魔虚罗已完全适应【" + Maho_GetCatName(cat) + "攻击】，该类攻击从此对其彻底无效！")
    else
        set udg_Maho_DefAdapt[pId * 8 + cat] = cur
    endif"""

new_def_adapt = """    if cur >= 0.9999 then
        set cur = 1.00
        set udg_Maho_DefAdapt[pId * 8 + cat] = 1.00
        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffffcc00【八握剑法轮·绝对免疫达成！】|r 魔虚罗已完全适应【" + Maho_GetCatName(cat) + "攻击】，该类攻击从此对其彻底无效！")
    else
        set udg_Maho_DefAdapt[pId * 8 + cat] = cur
        call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
    endif"""

assert old_def_adapt in content, "Def adapt anchor not found!"
content = content.replace(old_def_adapt, new_def_adapt, 1)

# 4. Update Maho_AddSkillAdapt to trigger wheel spin
old_skill_adapt = """    if idx >= 0 then
        set udg_Maho_SkillPct[pId * 12 + idx] = RMinBJ(1.00, udg_Maho_SkillPct[pId * 12 + idx] + pctAdd)
    else
        if udg_Maho_SkillCount[pId] < 12 then
            set idx = udg_Maho_SkillCount[pId]
            set udg_Maho_SkillCount[pId] = udg_Maho_SkillCount[pId] + 1
        else
            set idx = minIdx
        endif
        set udg_Maho_SkillId[pId * 12 + idx] = abilId
        set udg_Maho_SkillPct[pId * 12 + idx] = RMinBJ(1.00, pctAdd)
    endif
endfunction"""

new_skill_adapt = """    if idx >= 0 then
        set udg_Maho_SkillPct[pId * 12 + idx] = RMinBJ(1.00, udg_Maho_SkillPct[pId * 12 + idx] + pctAdd)
    else
        if udg_Maho_SkillCount[pId] < 12 then
            set idx = udg_Maho_SkillCount[pId]
            set udg_Maho_SkillCount[pId] = udg_Maho_SkillCount[pId] + 1
        else
            set idx = minIdx
        endif
        set udg_Maho_SkillId[pId * 12 + idx] = abilId
        set udg_Maho_SkillPct[pId * 12 + idx] = RMinBJ(1.00, pctAdd)
    endif

    if pctAdd > 0.0 then
        if udg_Maho_SkillPct[pId * 12 + idx] >= 0.9999 then
            call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
        else
            call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
        endif
    endif
endfunction"""

assert old_skill_adapt in content, "Skill adapt anchor not found!"
content = content.replace(old_skill_adapt, new_skill_adapt, 1)

# 5. Update Maho_Reset
old_reset = """    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
        set udg_Maho_WheelFx[pId] = null
    endif"""

new_reset = """    set udg_Maho_HasNeverMiss[pId] = false
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
        set udg_Maho_WheelFx[pId] = null
    endif"""

assert old_reset in content, "Reset anchor not found!"
content = content.replace(old_reset, new_reset, 1)

# 6. Update Maho_GetSkillName to add passives
old_skillname = """    elseif abilId == 'A014' then
        return "影之多重分身"
    elseif abilId == 'A021' then"""

new_skillname = """    elseif abilId == 'A014' then
        return "影之多重分身"
    elseif abilId == 'A015' then
        return "魔音身法·闪避"
    elseif abilId == 'A016' then
        return "音波破防"
    elseif abilId == 'A017' then
        return "天魔一击·暴击"
    elseif abilId == 'AOcr' then
        return "致命一击"
    elseif abilId == 'AHbh' then
        return "重击"
    elseif abilId == 'AEev' then
        return "闪避"
    elseif abilId == 'AEah' then
        return "荆棘光环"
    elseif abilId == 'AUts' then
        return "尖刺外壳"
    elseif abilId == 'Aspo' then
        return "毒性攻击"
    elseif abilId == 'A046' then
        return "因果必中"
    elseif abilId == 'A021' then"""

assert old_skillname in content, "SkillName anchor not found!"
content = content.replace(old_skillname, new_skillname, 1)

# 7. Add Maho_IsNonHostileSpell and update Maho_OnAnySpellEffect
old_spell_effect = """function Maho_OnAnySpellEffect takes unit caster, integer abil returns nothing
    local integer pId = 0
    local unit maho = null
    local unit tgt = GetSpellTargetUnit()
    local real tx = 0.0
    local real ty = 0.0
    local real dist = 0.0
    local real mx = 0.0
    local real my = 0.0

    if caster == null or abil == 0 or abil == 'A041' or abil == 'A042' or abil == 'A043' or abil == 'A044' then
        return
    endif

    set tx = GetSpellTargetX()
    set ty = GetSpellTargetY()
    if tgt == null and tx == 0.0 and ty == 0.0 then
        set tx = GetUnitX(caster)
        set ty = GetUnitY(caster)
    endif

    set pId = 0
    loop
        exitwhen pId > 7
        set maho = udg_Maho_Hero[pId]
        if maho != null and Maho_IsUnitAlive(maho) and not udg_Maho_InEgg[pId] and IsUnitEnemy(caster, GetOwningPlayer(maho)) then
            if tgt == maho then
                set udg_Maho_LastSkillId[pId] = abil
                set udg_Maho_LastSkillTime[pId] = 2.5
                call Maho_AddSkillAdapt(pId, abil, 0.03)
                call Maho_UpdateUI(pId)
            elseif tx != 0.0 or ty != 0.0 then
                set mx = GetUnitX(maho)
                set my = GetUnitY(maho)
                set dist = SquareRoot((mx - tx) * (mx - tx) + (my - ty) * (my - ty))
                if dist <= 450.0 then
                    set udg_Maho_LastSkillId[pId] = abil
                    set udg_Maho_LastSkillTime[pId] = 2.5
                    call Maho_AddSkillAdapt(pId, abil, 0.03)
                    call Maho_UpdateUI(pId)
                endif
            endif
        endif
        set pId = pId + 1
    endloop
    set maho = null
    set tgt = null
endfunction"""

new_spell_effect = """function Maho_IsNonHostileSpell takes integer abil returns boolean
    if abil == 'Arej' or abil == 'ACrj' or abil == 'Ahea' or abil == 'AOhw' or abil == 'AHhb' then
        return true
    elseif abil == 'ACbl' or abil == 'Ablo' or abil == 'ACif' or abil == 'Ainf' or abil == 'ACf2' or abil == 'Afra' then
        return true
    elseif abil == 'AOwk' or abil == 'AOmi' or abil == 'ACro' or abil == 'Aroa' or abil == 'AUau' or abil == 'AHad' then
        return true
    elseif abil == 'A023' or abil == 'A024' or abil == 'A031' or abil == 'A032' or abil == 'A033' or abil == 'A034' then
        return true
    elseif abil == 'A041' or abil == 'A042' or abil == 'A043' or abil == 'A044' or abil == 'A045' or abil == 'A046' then
        return true
    endif
    return false
endfunction

function Maho_OnAnySpellEffect takes unit caster, integer abil returns nothing
    local integer pId = 0
    local unit maho = null
    local unit tgt = GetSpellTargetUnit()
    local real tx = 0.0
    local real ty = 0.0
    local real dist = 0.0
    local real mx = 0.0
    local real my = 0.0

    if caster == null or abil == 0 or Maho_IsNonHostileSpell(abil) then
        set tgt = null
        return
    endif

    if tgt != null then
        // Single-target spell: ONLY adapt if target IS Mahoraga!
        set pId = 0
        loop
            exitwhen pId > 7
            set maho = udg_Maho_Hero[pId]
            if maho != null and Maho_IsUnitAlive(maho) and not udg_Maho_InEgg[pId] and tgt == maho and IsUnitEnemy(caster, GetOwningPlayer(maho)) then
                set udg_Maho_LastSkillId[pId] = abil
                set udg_Maho_LastSkillTime[pId] = 2.5
                call Maho_AddSkillAdapt(pId, abil, 0.03)
                call Maho_UpdateUI(pId)
            endif
            set pId = pId + 1
        endloop
    else
        // Ground target or point-blank AOE spell
        set tx = GetSpellTargetX()
        set ty = GetSpellTargetY()
        if tx == 0.0 and ty == 0.0 then
            set tx = GetUnitX(caster)
            set ty = GetUnitY(caster)
        endif

        set pId = 0
        loop
            exitwhen pId > 7
            set maho = udg_Maho_Hero[pId]
            if maho != null and Maho_IsUnitAlive(maho) and not udg_Maho_InEgg[pId] and IsUnitEnemy(caster, GetOwningPlayer(maho)) then
                set mx = GetUnitX(maho)
                set my = GetUnitY(maho)
                set dist = SquareRoot((mx - tx) * (mx - tx) + (my - ty) * (my - ty))
                if dist <= 450.0 then
                    set udg_Maho_LastSkillId[pId] = abil
                    set udg_Maho_LastSkillTime[pId] = 2.5
                    call Maho_AddSkillAdapt(pId, abil, 0.03)
                    call Maho_UpdateUI(pId)
                endif
            endif
            set pId = pId + 1
        endloop
    endif

    set maho = null
    set tgt = null
endfunction"""

assert old_spell_effect in content, "Spell effect anchor not found!"
content = content.replace(old_spell_effect, new_spell_effect, 1)

# 8. Update Maho_AnalyzeTargetSkills
old_analyze = """function Maho_AnalyzeTargetSkills takes integer pId, unit wt returns nothing
    local integer uId = 0
    if wt == null then
        return
    endif
    set uId = GetUnitTypeId(wt)

    if GetUnitAbilityLevel(wt, 'AHtb') > 0 or uId == 'Hmkg' then
        call Maho_AddSkillAdapt(pId, 'AHtb', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AHtc') > 0 or uId == 'Hmkg' then
        call Maho_AddSkillAdapt(pId, 'AHtc', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AHhb') > 0 or uId == 'Hpal' then
        call Maho_AddSkillAdapt(pId, 'AHhb', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AHbz') > 0 or uId == 'Hamg' then
        call Maho_AddSkillAdapt(pId, 'AHbz', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOmi') > 0 or uId == 'Obla' then
        call Maho_AddSkillAdapt(pId, 'AOmi', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOcl') > 0 or uId == 'Ofar' then
        call Maho_AddSkillAdapt(pId, 'AOcl', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOhw') > 0 or uId == 'Oshd' then
        call Maho_AddSkillAdapt(pId, 'AOhw', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOs2') > 0 or uId == 'Otch' then
        call Maho_AddSkillAdapt(pId, 'AOs2', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOs1') > 0 or uId == 'Otch' then
        call Maho_AddSkillAdapt(pId, 'AOs1', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEer') > 0 or uId == 'Ekee' then
        call Maho_AddSkillAdapt(pId, 'AEer', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEfn') > 0 or uId == 'Ewar' then
        call Maho_AddSkillAdapt(pId, 'AEfn', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEsh') > 0 or uId == 'Ewar' then
        call Maho_AddSkillAdapt(pId, 'AEsh', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUcs') > 0 or uId == 'Udre' then
        call Maho_AddSkillAdapt(pId, 'AUcs', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUsl') > 0 or uId == 'Udre' then
        call Maho_AddSkillAdapt(pId, 'AUsl', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUfn') > 0 or uId == 'Ulic' then
        call Maho_AddSkillAdapt(pId, 'AUfn', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUim') > 0 or uId == 'Ucrl' then
        call Maho_AddSkillAdapt(pId, 'AUim', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUdc') > 0 or uId == 'Udea' then
        call Maho_AddSkillAdapt(pId, 'AUdc', 0.01)
    endif

    if GetUnitAbilityLevel(wt, 'A001') > 0 or uId == 'H002' then
        call Maho_AddSkillAdapt(pId, 'A001', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A002') > 0 or uId == 'H002' then
        call Maho_AddSkillAdapt(pId, 'A002', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A003') > 0 or uId == 'H002' then
        call Maho_AddSkillAdapt(pId, 'A003', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A011') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A011', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A014') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A014', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A021') > 0 or uId == 'H004' then
        call Maho_AddSkillAdapt(pId, 'A021', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A022') > 0 or uId == 'H004' then
        call Maho_AddSkillAdapt(pId, 'A022', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A031') > 0 or uId == 'H005' then
        call Maho_AddSkillAdapt(pId, 'A031', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A032') > 0 or uId == 'H005' then
        call Maho_AddSkillAdapt(pId, 'A032', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A035') > 0 or uId == 'H005' then
        call Maho_AddSkillAdapt(pId, 'A035', 0.01)
    endif
endfunction"""

new_analyze = """function Maho_AnalyzeTargetSkills takes integer pId, unit wt returns nothing
    local integer uId = 0
    if wt == null then
        return
    endif
    set uId = GetUnitTypeId(wt)

    // Active spells
    if GetUnitAbilityLevel(wt, 'AHtb') > 0 or uId == 'Hmkg' then
        call Maho_AddSkillAdapt(pId, 'AHtb', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AHtc') > 0 or uId == 'Hmkg' then
        call Maho_AddSkillAdapt(pId, 'AHtc', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AHbz') > 0 or uId == 'Hamg' then
        call Maho_AddSkillAdapt(pId, 'AHbz', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOcl') > 0 or uId == 'Ofar' then
        call Maho_AddSkillAdapt(pId, 'AOcl', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOs2') > 0 or uId == 'Otch' then
        call Maho_AddSkillAdapt(pId, 'AOs2', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOs1') > 0 or uId == 'Otch' then
        call Maho_AddSkillAdapt(pId, 'AOs1', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEer') > 0 or uId == 'Ekee' then
        call Maho_AddSkillAdapt(pId, 'AEer', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEfn') > 0 or uId == 'Ewar' then
        call Maho_AddSkillAdapt(pId, 'AEfn', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEsh') > 0 or uId == 'Ewar' then
        call Maho_AddSkillAdapt(pId, 'AEsh', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEmb') > 0 or uId == 'Edem' then
        call Maho_AddSkillAdapt(pId, 'AEmb', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUcs') > 0 or uId == 'Udre' then
        call Maho_AddSkillAdapt(pId, 'AUcs', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUsl') > 0 or uId == 'Udre' then
        call Maho_AddSkillAdapt(pId, 'AUsl', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUfn') > 0 or uId == 'Ulic' then
        call Maho_AddSkillAdapt(pId, 'AUfn', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUim') > 0 or uId == 'Ucrl' then
        call Maho_AddSkillAdapt(pId, 'AUim', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUdc') > 0 or uId == 'Udea' then
        call Maho_AddSkillAdapt(pId, 'AUdc', 0.01)
    endif

    // Hostile Passive Skills (Bash, Crit, Evasion, Thorns/Spikes, Poison)
    if GetUnitAbilityLevel(wt, 'AHbh') > 0 or uId == 'Hmkg' then
        call Maho_AddSkillAdapt(pId, 'AHbh', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'ACbh') > 0 then
        call Maho_AddSkillAdapt(pId, 'ACbh', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AOcr') > 0 or uId == 'Obla' then
        call Maho_AddSkillAdapt(pId, 'AOcr', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'ACct') > 0 then
        call Maho_AddSkillAdapt(pId, 'ACct', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A017') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A017', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEev') > 0 or uId == 'Edem' then
        call Maho_AddSkillAdapt(pId, 'AEev', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A015') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A015', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'ACev') > 0 then
        call Maho_AddSkillAdapt(pId, 'ACev', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AEah') > 0 or uId == 'Ekee' then
        call Maho_AddSkillAdapt(pId, 'AEah', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'AUts') > 0 or uId == 'Ucrl' then
        call Maho_AddSkillAdapt(pId, 'AUts', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A025') > 0 or uId == 'H004' then
        call Maho_AddSkillAdapt(pId, 'A025', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'Aspo') > 0 then
        call Maho_AddSkillAdapt(pId, 'Aspo', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A026') > 0 or uId == 'H004' then
        call Maho_AddSkillAdapt(pId, 'A026', 0.01)
    endif

    // Custom Hostile Hero Skills
    if GetUnitAbilityLevel(wt, 'A002') > 0 or uId == 'H002' then
        call Maho_AddSkillAdapt(pId, 'A002', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A003') > 0 or uId == 'H002' then
        call Maho_AddSkillAdapt(pId, 'A003', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A011') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A011', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A012') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A012', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A013') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A013', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A014') > 0 or uId == 'H003' then
        call Maho_AddSkillAdapt(pId, 'A014', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A021') > 0 or uId == 'H004' then
        call Maho_AddSkillAdapt(pId, 'A021', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A022') > 0 or uId == 'H004' then
        call Maho_AddSkillAdapt(pId, 'A022', 0.01)
    endif
    if GetUnitAbilityLevel(wt, 'A035') > 0 or uId == 'H005' then
        call Maho_AddSkillAdapt(pId, 'A035', 0.01)
    endif
endfunction"""

assert old_analyze in content, "Analyze skills anchor not found!"
content = content.replace(old_analyze, new_analyze, 1)

# 9. Update Maho_StealthLoop for CC check and wheel timer
old_stealth = """        set h = udg_Maho_Hero[pId]
        if h != null and Maho_IsUnitAlive(h) and not udg_Maho_InEgg[pId] then
            set hasCC = false
            if UnitHasBuffBJ(h, 'BPSE') or UnitHasBuffBJ(h, 'BSTN') or UnitHasBuffBJ(h, 'BHtb') or UnitHasBuffBJ(h, 'Bslo') or UnitHasBuffBJ(h, 'Bhex') or UnitHasBuffBJ(h, 'Bens') or UnitHasBuffBJ(h, 'Bweb') or UnitHasBuffBJ(h, 'Bslp') or UnitHasBuffBJ(h, 'Bcy2') or UnitHasBuffBJ(h, 'Bcri') then
                set hasCC = true
            endif

            if hasCC then
                set udg_Maho_CCTimer[pId] = udg_Maho_CCTimer[pId] + 0.05
                set lastSkillPct = 0.0
                if udg_Maho_LastSkillId[pId] != 0 then
                    set lastSkillPct = Maho_GetSkillPct(pId, udg_Maho_LastSkillId[pId])
                endif
                set ccAdapt = RMaxBJ(udg_Maho_DefAdapt[pId * 8 + 6], lastSkillPct)

                if ccAdapt >= 0.99 then"""

new_stealth = """        // Wheel dynamic spin countdown
        if udg_Maho_WheelSpinTimer[pId] > 0.0 then
            set udg_Maho_WheelSpinTimer[pId] = udg_Maho_WheelSpinTimer[pId] - 0.05
            if udg_Maho_WheelSpinTimer[pId] <= 0.0 then
                set udg_Maho_WheelSpinTimer[pId] = 0.0
                if udg_Maho_WheelFx[pId] != null then
                    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0)
                endif
            endif
        endif

        set h = udg_Maho_Hero[pId]
        if h != null and Maho_IsUnitAlive(h) and not udg_Maho_InEgg[pId] then
            set hasCC = false
            if UnitHasBuffBJ(h, 'BPSE') or UnitHasBuffBJ(h, 'BSTN') or UnitHasBuffBJ(h, 'BHtb') or UnitHasBuffBJ(h, 'Bslo') or UnitHasBuffBJ(h, 'Bhex') or UnitHasBuffBJ(h, 'Bens') or UnitHasBuffBJ(h, 'Bweb') or UnitHasBuffBJ(h, 'Bslp') or UnitHasBuffBJ(h, 'Bcy2') or UnitHasBuffBJ(h, 'Bcri') then
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

                if ccAdapt >= 0.99 then"""

assert old_stealth in content, "StealthLoop anchor not found!"
content = content.replace(old_stealth, new_stealth, 1)

# 10. Update Maho_CastE to spin wheel
old_caste = """    set udg_Maho_WheelSpins[pId] = udg_Maho_WheelSpins[pId] + 1
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", caster, "overhead"))"""

new_caste = """    set udg_Maho_WheelSpins[pId] = udg_Maho_WheelSpins[pId] + 1
    call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", caster, "overhead"))"""

assert old_caste in content, "CastE anchor not found!"
content = content.replace(old_caste, new_caste, 1)

# 11. Update Maho_CapTimerLoop to spin wheel on speed growth and Q watch
old_cap_speed = """                    if udg_Maho_MoveSpeed[pId] >= 522.0 then
                        set udg_Maho_MoveSpeed[pId] = 522.0
                        call DisplayTimedTextToPlayer(Player(pId), 0, 0, 4.0, "|cffffcc00【法轮转动·空间适应完成】|r 移速已达522极限！继续奔袭将开启翼化飞升！")
                        call BlzSetUnitAttackCooldown(h, BlzGetUnitAttackCooldown(h, 0) * 0.85, 0)
                        call BlzSetUnitAttackCooldown(h, BlzGetUnitAttackCooldown(h, 1) * 0.85, 1)
                    endif
                    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])"""

new_cap_speed = """                    if udg_Maho_MoveSpeed[pId] >= 522.0 then
                        set udg_Maho_MoveSpeed[pId] = 522.0
                        call DisplayTimedTextToPlayer(Player(pId), 0, 0, 4.0, "|cffffcc00【法轮转动·空间适应完成】|r 移速已达522极限！继续奔袭将开启翼化飞升！")
                        call BlzSetUnitAttackCooldown(h, BlzGetUnitAttackCooldown(h, 0) * 0.85, 0)
                        call BlzSetUnitAttackCooldown(h, BlzGetUnitAttackCooldown(h, 1) * 0.85, 1)
                    endif
                    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])
                    call Maho_TriggerWheelSpin(pId, 0.55, 1.5)"""

assert old_cap_speed in content, "Cap speed anchor not found!"
content = content.replace(old_cap_speed, new_cap_speed, 1)

old_cap_fly = """                    if udg_Maho_FlyProgress[pId] >= 20 then
                        set udg_Maho_IsWinged[pId] = true
                        call Maho_ApplyAppearance(h, pId)
                        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Demon\\\\DarkPortal\\\\DarkPortalTarget.mdl", h, "origin"))
                        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Avatar\\\\AvatarCaster.mdl", h, "origin"))
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffffcc00【法轮终极蜕变 · 翼化神将降临！】|r 魔虚罗突破大地束缚，背生圣金双翼升空翱翔，并彻底掌握制空权！")
                    endif"""

new_cap_fly = """                    if udg_Maho_FlyProgress[pId] >= 20 then
                        set udg_Maho_IsWinged[pId] = true
                        call Maho_ApplyAppearance(h, pId)
                        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
                        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Demon\\\\DarkPortal\\\\DarkPortalTarget.mdl", h, "origin"))
                        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Avatar\\\\AvatarCaster.mdl", h, "origin"))
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffffcc00【法轮终极蜕变 · 翼化神将降临！】|r 魔虚罗突破大地束缚，背生圣金双翼升空翱翔，并彻底掌握制空权！")
                    endif"""

assert old_cap_fly in content, "Cap fly anchor not found!"
content = content.replace(old_cap_fly, new_cap_fly, 1)

# 12. Update Maho_OnEggComplete to spin wheel
old_egg_comp = """        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Avatar\\\\AvatarCaster.mdl", h, "origin"))
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffffcc00【神将重生·破茧成神】|r 魔虚罗完成因果涅槃！抗性跃升，身躯全面升华！")
        call Maho_UpdateUI(pId)"""

new_egg_comp = """        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Avatar\\\\AvatarCaster.mdl", h, "origin"))
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffffcc00【神将重生·破茧成神】|r 魔虚罗完成因果涅槃！抗性跃升，身躯全面升华！")
        call Maho_UpdateUI(pId)"""

assert old_egg_comp in content, "Egg complete anchor not found!"
content = content.replace(old_egg_comp, new_egg_comp, 1)

# 13. Update DM_OnUnitAttacked to track enemy evasion
old_attacked = """function DM_OnUnitAttacked takes nothing returns boolean
    local unit attacker = GetAttacker()
    local unit target = GetTriggerUnit()
    local integer pId = 0
    local integer attTypeId = 0
    local integer crRange = 128
    local real dx = 0.0
    local real dy = 0.0
    local real dist = 0.0"""

new_attacked = """function DM_OnUnitAttacked takes nothing returns boolean
    local unit attacker = GetAttacker()
    local unit target = GetTriggerUnit()
    local integer pId = 0
    local integer attTypeId = 0
    local integer crRange = 128
    local real dx = 0.0
    local real dy = 0.0
    local real dist = 0.0
    local integer evaAbil = 0"""

assert old_attacked in content, "Attacked anchor 1 not found!"
content = content.replace(old_attacked, new_attacked, 1)

old_attacked_h005_end = """                if dist > 160.0 then
                    if Wild_GetCreepMissileArt(BlzGetUnitSkin(attacker)) != "" and Wild_GetCreepMissileArt(BlzGetUnitSkin(attacker)) != null then
                        call DestroyEffect(AddSpecialEffectTarget(Wild_GetCreepMissileArt(BlzGetUnitSkin(attacker)), target, "chest"))
                    endif
                endif
            endif
        endif
    endif

    set attacker = null"""

new_attacked_h005_end = """                if dist > 160.0 then
                    if Wild_GetCreepMissileArt(BlzGetUnitSkin(attacker)) != "" and Wild_GetCreepMissileArt(BlzGetUnitSkin(attacker)) != null then
                        call DestroyEffect(AddSpecialEffectTarget(Wild_GetCreepMissileArt(BlzGetUnitSkin(attacker)), target, "chest"))
                    endif
                endif
            endif
        elseif attTypeId == 'H006' and target != null then
            set pId = GetPlayerId(GetOwningPlayer(attacker))
            set evaAbil = 0
            if GetUnitAbilityLevel(target, 'AEev') > 0 then
                set evaAbil = 'AEev'
            elseif GetUnitAbilityLevel(target, 'A015') > 0 then
                set evaAbil = 'A015'
            elseif GetUnitAbilityLevel(target, 'ACev') > 0 then
                set evaAbil = 'ACev'
            endif
            if evaAbil != 0 then
                call Maho_AddSkillAdapt(pId, evaAbil, 0.04)
                if Maho_GetSkillPct(pId, evaAbil) >= 0.9999 and not udg_Maho_HasNeverMiss[pId] then
                    set udg_Maho_HasNeverMiss[pId] = true
                    call UnitAddAbility(attacker, 'A046')
                    call UnitMakeAbilityPermanent(attacker, true, 'A046')
                    call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
                    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffffcc00【被动无效化·破除闪避】|r 魔虚罗完全解析敌方闪避身法，觉醒【因果必中】，敌方闪避被动对其彻底失效！")
                endif
            endif
        endif
    endif

    set attacker = null"""

assert old_attacked_h005_end in content, "Attacked anchor 2 not found!"
content = content.replace(old_attacked_h005_end, new_attacked_h005_end, 1)

# 14. Update DM_OnDamaged (locals + offensive W passive + defensive passives)
old_damaged_locals = """function DM_OnDamaged takes nothing returns boolean
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
    local integer mahoPid = 0
    local integer cat = 0
    local real effResist = 0.0
    local real skillPct = 0.0
    local real finalDmg = 0.0
    local integer defType = 0
    local real bonus = 0.0
    local real defAdd = 0.0"""

new_damaged_locals = """function DM_OnDamaged takes nothing returns boolean
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
    local integer mahoPid = 0
    local integer cat = 0
    local real effResist = 0.0
    local real skillPct = 0.0
    local real finalDmg = 0.0
    local integer defType = 0
    local real bonus = 0.0
    local real defAdd = 0.0
    local integer critAbil = 0
    local real normalAtk = 0.0
    local real critAdapt = 0.0
    local real critExtra = 0.0
    local integer bashAbil = 0
    local boolean isDemonic = false"""

assert old_damaged_locals in content, "Damaged locals anchor not found!"
content = content.replace(old_damaged_locals, new_damaged_locals, 1)

old_maho_atk = """        // Hero #5: Mahoraga Offensive Damage Adaptation
        if GetUnitTypeId(src) == 'H006' and not udg_Maho_DmgLock and dmg > 0.5 then
            set pId = GetPlayerId(GetOwningPlayer(src))
            set defType = BlzGetUnitIntegerField(tgt, UNIT_IF_DEFENSE_TYPE)
            if defType < 0 or defType > 7 then
                set defType = 0
            endif
            set bonus = udg_Maho_AtkAdapt[pId * 8 + defType]
            call BlzSetEventDamage(dmg * (1.0 + bonus))

            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
            set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
            if udg_Maho_AtkHits[pId] >= 4 then
                set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
                call Maho_AddBaseDamage(src, 1)
            endif
            call Maho_UpdateUI(pId)
        endif"""

new_maho_atk = """        // Hero #5: Mahoraga Offensive Damage Adaptation & Exorcism Blade (W Passive)
        if GetUnitTypeId(src) == 'H006' and not udg_Maho_DmgLock and dmg > 0.5 then
            set pId = GetPlayerId(GetOwningPlayer(src))
            set defType = BlzGetUnitIntegerField(tgt, UNIT_IF_DEFENSE_TYPE)
            if defType < 0 or defType > 7 then
                set defType = 0
            endif
            set bonus = udg_Maho_AtkAdapt[pId * 8 + defType]
            set isDemonic = false
            if IsUnitIllusion(tgt) or IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitType(tgt, UNIT_TYPE_UNDEAD) or IsUnitInGroup(tgt, udg_FakeHeroGroup) or GetUnitTypeId(tgt) == 'u001' or GetUnitTypeId(tgt) == 'u002' or GetUnitTypeId(tgt) == 'u003' then
                set isDemonic = true
            endif

            if isDemonic then
                call BlzSetEventDamage(dmg * (1.0 + bonus) * 1.5)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\HolyBolt\\\\HolyBoltSpecialArt.mdl", tgt, "origin"))
            else
                call BlzSetEventDamage(dmg * (1.0 + bonus))
            endif

            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
            call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
            set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
            if udg_Maho_AtkHits[pId] >= 4 then
                set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
                call Maho_AddBaseDamage(src, 1)
            endif
            call Maho_UpdateUI(pId)
        endif"""

assert old_maho_atk in content, "Maho atk anchor not found!"
content = content.replace(old_maho_atk, new_maho_atk, 1)

old_maho_def = """            // Anti-air adaptation check
            if IsUnitType(src, UNIT_TYPE_FLYING) and not udg_Maho_AntiAirUnlocked[mahoPid] then
                set udg_Maho_AirHits[mahoPid] = udg_Maho_AirHits[mahoPid] + 1
                if udg_Maho_AirHits[mahoPid] >= 6 or udg_Maho_IsWinged[mahoPid] then
                    set udg_Maho_AntiAirUnlocked[mahoPid] = true
                    call UnitAddAbility(tgt, 'A045')
                    call UnitMakeAbilityPermanent(tgt, true, 'A045')
                    call SetUnitAcquireRange(tgt, 650.0)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\MarkOfChaos\\\\MarkOfChaosTarget.mdl", tgt, "origin"))
                    call DisplayTimedTextToPlayer(Player(mahoPid), 0, 0, 5.0, "|cffffcc00【法轮转动 · 对空适应完成】|r 魔虚罗已解析制空法则，挥舞破空剑气可直接远程斩击空中单位！")
                endif
            endif

            set cat = Maho_GetCatFromDamage(BlzGetEventAttackType(), BlzGetEventDamageType(), BlzGetEventIsAttack())"""

new_maho_def = """            // Anti-air adaptation check
            if IsUnitType(src, UNIT_TYPE_FLYING) and not udg_Maho_AntiAirUnlocked[mahoPid] then
                set udg_Maho_AirHits[mahoPid] = udg_Maho_AirHits[mahoPid] + 1
                if udg_Maho_AirHits[mahoPid] >= 6 or udg_Maho_IsWinged[mahoPid] then
                    set udg_Maho_AntiAirUnlocked[mahoPid] = true
                    call UnitAddAbility(tgt, 'A045')
                    call UnitMakeAbilityPermanent(tgt, true, 'A045')
                    call SetUnitAcquireRange(tgt, 650.0)
                    call Maho_TriggerWheelSpin(mahoPid, 1.50, 3.0)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\MarkOfChaos\\\\MarkOfChaosTarget.mdl", tgt, "origin"))
                    call DisplayTimedTextToPlayer(Player(mahoPid), 0, 0, 5.0, "|cffffcc00【法轮转动 · 对空适应完成】|r 魔虚罗已解析制空法则，挥舞破空剑气可直接远程斩击空中单位！")
                else
                    call Maho_TriggerWheelSpin(mahoPid, 0.55, 1.5)
                endif
            endif

            // Check enemy Critical Strike passive: 'AOcr', 'ACct', 'A017'
            if BlzGetEventIsAttack() and (GetUnitAbilityLevel(src, 'AOcr') > 0 or GetUnitAbilityLevel(src, 'ACct') > 0 or GetUnitAbilityLevel(src, 'A017') > 0) then
                set critAbil = 0
                if GetUnitAbilityLevel(src, 'AOcr') > 0 then
                    set critAbil = 'AOcr'
                elseif GetUnitAbilityLevel(src, 'A017') > 0 then
                    set critAbil = 'A017'
                else
                    set critAbil = 'ACct'
                endif
                set normalAtk = I2R(BlzGetUnitBaseDamage(src, 0)) + 15.0
                if IsUnitType(src, UNIT_TYPE_HERO) then
                    set normalAtk = normalAtk + I2R(R2I(RMaxBJ(I2R(GetHeroStr(src, true)), RMaxBJ(I2R(GetHeroAgi(src, true)), I2R(GetHeroInt(src, true))))))
                endif
                if dmg > normalAtk * 1.45 then
                    call Maho_AddSkillAdapt(mahoPid, critAbil, 0.06)
                    set critAdapt = Maho_GetSkillPct(mahoPid, critAbil)
                    set critExtra = dmg - normalAtk
                    if critExtra > 0.0 then
                        set dmg = dmg - critExtra * critAdapt
                        if dmg < normalAtk then
                            set dmg = normalAtk
                        endif
                    endif
                endif
            endif

            // Check enemy Bash passive: 'AHbh', 'ACbh'
            if BlzGetEventIsAttack() and (GetUnitAbilityLevel(src, 'AHbh') > 0 or GetUnitAbilityLevel(src, 'ACbh') > 0) then
                set bashAbil = 'AHbh'
                if GetUnitAbilityLevel(src, 'AHbh') > 0 then
                    set bashAbil = 'AHbh'
                else
                    set bashAbil = 'ACbh'
                endif
                if UnitHasBuffBJ(tgt, 'BPSE') or UnitHasBuffBJ(tgt, 'BSTN') then
                    call Maho_AddSkillAdapt(mahoPid, bashAbil, 0.08)
                else
                    call Maho_AddSkillAdapt(mahoPid, bashAbil, 0.05)
                endif
            endif

            // Check enemy Thorns / Spikes: 'AEah', 'AUts', 'A025'
            if GetUnitAbilityLevel(src, 'AEah') > 0 then
                call Maho_AddSkillAdapt(mahoPid, 'AEah', 0.03)
            endif
            if GetUnitAbilityLevel(src, 'AUts') > 0 then
                call Maho_AddSkillAdapt(mahoPid, 'AUts', 0.03)
            endif
            if GetUnitAbilityLevel(src, 'A025') > 0 then
                call Maho_AddSkillAdapt(mahoPid, 'A025', 0.03)
            endif

            set cat = Maho_GetCatFromDamage(BlzGetEventAttackType(), BlzGetEventDamageType(), BlzGetEventIsAttack())"""

assert old_maho_def in content, "Maho def anchor not found!"
content = content.replace(old_maho_def, new_maho_def, 1)

# 15. Update AI_TacticalLoop to remove W cripple
old_ai_w = """                        // 3. Cast W (A042 退魔之剑·破界斩) on nearest enemy
                        if udg_AI_CastCD_W[i] <= 0.0 and nearestEnemy != null and minD <= 320.0 and GetUnitState(h, UNIT_STATE_MANA) >= 40.0 then
                            if IssueTargetOrder(h, "cripple", nearestEnemy) then
                                set udg_AI_CastCD_W[i] = 8.0
                            endif
                        endif"""

new_ai_w = """                        // W (A042 退魔之剑) is now passive (1.5x damage against demonic/summons/undead)"""

assert old_ai_w in content, "AI W anchor not found!"
content = content.replace(old_ai_w, new_ai_w, 1)

# 16. Remove A042 from DM_OnSpellEffect
old_spell_a042 = """    elseif abil == 'A042' then
        call Maho_CastW(caster, GetSpellTargetUnit())"""

assert old_spell_a042 in content, "Spell A042 anchor not found!"
content = content.replace(old_spell_a042, "", 1)

# 17. Update Maho_UpdateUI & Maho_PrintOverview for Never Miss
old_ui_anti_air = """    if udg_Maho_AntiAirUnlocked[pId] then
        set tip = tip + "- 对空制空：|cff00ff00已解锁破空剑气|r|n"
    else
        set tip = tip + "- 对空制空：解析中(" + I2S(udg_Maho_AirHits[pId]) + "/6)|n"
    endif"""

new_ui_anti_air = """    if udg_Maho_AntiAirUnlocked[pId] then
        set tip = tip + "- 对空制空：|cff00ff00已解锁破空剑气|r|n"
    else
        set tip = tip + "- 对空制空：解析中(" + I2S(udg_Maho_AirHits[pId]) + "/6)|n"
    endif
    if udg_Maho_HasNeverMiss[pId] then
        set tip = tip + "- 因果必中：|cff00ff00已觉醒(敌方闪避彻底无效)|r|n"
    endif"""

assert old_ui_anti_air in content, "UI anti-air anchor not found!"
content = content.replace(old_ui_anti_air, new_ui_anti_air, 1)

old_print_anti_air = """    if udg_Maho_AntiAirUnlocked[pId] then
        set s = "|cffffff00[空战演化]|r 对空剑气: |cff00ff00已解锁 (破空远程斩击)|r"
    else
        set s = "|cffffff00[空战演化]|r 对空剑气: |cffffcc00解析中 (" + I2S(udg_Maho_AirHits[pId]) + "/6)|r"
    endif"""

new_print_anti_air = """    if udg_Maho_AntiAirUnlocked[pId] then
        set s = "|cffffff00[空战演化]|r 对空剑气: |cff00ff00已解锁 (破空远程斩击)|r"
    else
        set s = "|cffffff00[空战演化]|r 对空剑气: |cffffcc00解析中 (" + I2S(udg_Maho_AirHits[pId]) + "/6)|r"
    endif
    if udg_Maho_HasNeverMiss[pId] then
        set s = s + " | 必中法则: |cff00ff00因果必中 (敌方闪避彻底失效)|r"
    endif"""

assert old_print_anti_air in content, "Print anti-air anchor not found!"
content = content.replace(old_print_anti_air, new_print_anti_air, 1)

with open(jass_path, 'wb') as f:
    f.write(content.encode('utf-8'))

print("Successfully applied all v5.7 JASS updates!")
