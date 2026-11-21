# -*- coding: utf-8 -*-
import sys

def apply_patches():
    with open('payload/war3map.j', 'rb') as f:
        content = f.read().decode('utf-8')
    
    is_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    patches = []

    # 1. Globals
    target_1 = """    real array udg_Maho_WheelSpinTimer
    boolean array udg_Maho_HasNeverMiss
    button udg_TM_BtnMode5All = null"""
    replacement_1 = """    real array udg_Maho_WheelSpinTimer
    boolean array udg_Maho_HasNeverMiss
    real array udg_Maho_AntiMahoAdapt
    button udg_TM_BtnMode5All = null"""
    patches.append(("Globals", target_1, replacement_1))

    # 2. Maho_TriggerWheelSpin & Maho_AddAntiMahoAdapt
    target_2 = """function Maho_TriggerWheelSpin takes integer pId, real duration, real speed returns nothing
    if udg_Maho_WheelFx[pId] != null then
        call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], speed)
        if duration > udg_Maho_WheelSpinTimer[pId] then
            set udg_Maho_WheelSpinTimer[pId] = duration
        endif
    endif
endfunction"""
    replacement_2 = """function Maho_TriggerWheelSpin takes integer pId, real duration, real speed returns nothing
    if udg_Maho_WheelFx[pId] != null then
        if duration <= 0.0 then
            set udg_Maho_WheelSpinTimer[pId] = 0.0
            call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)
        else
            call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], speed)
            if duration > udg_Maho_WheelSpinTimer[pId] then
                set udg_Maho_WheelSpinTimer[pId] = duration
            endif
        endif
    endif
endfunction

function Maho_AddAntiMahoAdapt takes integer pId, real amount returns nothing
    local real oldVal = udg_Maho_AntiMahoAdapt[pId]
    local real newVal = RMinBJ(1.0, oldVal + amount)
    set udg_Maho_AntiMahoAdapt[pId] = newVal
    if oldVal < 0.9999 and newVal >= 0.9999 then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 5.0, "|cffffcc00【法轮终极反制 · 破法适应完成！】|r 魔虚罗已完全解析同类的适应法则，此后斩击敌方魔虚罗将 100% 无视其防御免疫！")
    endif
endfunction"""
    patches.append(("Maho_TriggerWheelSpin & Maho_AddAntiMahoAdapt", target_2, replacement_2))

    # 3. Maho_ApplyAppearance
    target_3 = """    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
    endif
    set udg_Maho_WheelFx[pId] = AddSpecialEffectTarget("war3mapImported\\\\MahoWheel.mdx", h, "overhead")
    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0)
    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])"""
    replacement_3 = """    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
    endif
    set udg_Maho_WheelFx[pId] = AddSpecialEffectTarget("war3mapImported\\\\MahoWheel.mdx", h, "overhead")
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)
    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])"""
    patches.append(("Maho_ApplyAppearance", target_3, replacement_3))

    # 4. Maho_UpdateUI
    target_4 = """    if udg_Maho_IsWinged[pId] then
        set tip = tip + "- 翼化升维：|cff00ff00圣金末日神将·真飞行|r|n"
    else
        set tip = tip + "- 翼化升维：蓄力中(" + I2S(udg_Maho_FlyProgress[pId]) + "/20)|n"
    endif
    set tip = tip + "|cff99ccff点击此技能在屏幕上打印完整适应档案。|r\""""
    replacement_4 = """    if udg_Maho_IsWinged[pId] then
        set tip = tip + "- 翼化升维：|cff00ff00圣金末日神将·真飞行|r|n"
    else
        set tip = tip + "- 翼化升维：蓄力中(" + I2S(udg_Maho_FlyProgress[pId]) + "/20)|n"
    endif
    if udg_Maho_AntiMahoAdapt[pId] > 0.0 then
        set tip = tip + "- |cffff3366破法穿透·反魔虚罗适应：|r穿透同类防御免疫 " + I2S(R2I(udg_Maho_AntiMahoAdapt[pId] * 100.0)) + "%|n"
    endif
    set tip = tip + "|cff99ccff点击此技能在屏幕上打印完整适应档案。|r\""""
    patches.append(("Maho_UpdateUI", target_4, replacement_4))

    # 5. Maho_PrintOverview
    target_5 = """    if udg_Maho_IsWinged[pId] then
        set s = s + " | 翼化飞行: |cff00ff00已升维 (圣金末日神将·真高空飞行)|r"
    else
        set s = s + " | 翼化飞行: |cffffcc00蓄力中 (" + I2S(udg_Maho_FlyProgress[pId]) + "/20)|r"
    endif
    call DisplayTimedTextToPlayer(p, 0, 0, 8.0, s)

    if udg_Maho_SkillCount[pId] > 0 then"""
    replacement_5 = """    if udg_Maho_IsWinged[pId] then
        set s = s + " | 翼化飞行: |cff00ff00已升维 (圣金末日神将·真高空飞行)|r"
    else
        set s = s + " | 翼化飞行: |cffffcc00蓄力中 (" + I2S(udg_Maho_FlyProgress[pId]) + "/20)|r"
    endif
    call DisplayTimedTextToPlayer(p, 0, 0, 8.0, s)

    if udg_Maho_AntiMahoAdapt[pId] > 0.0 then
        call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cffff3366[破法穿透·反魔虚罗适应]|r 穿透同类防御免疫: " + I2S(R2I(udg_Maho_AntiMahoAdapt[pId] * 100.0)) + "%")
    endif

    if udg_Maho_SkillCount[pId] > 0 then"""
    patches.append(("Maho_PrintOverview", target_5, replacement_5))

    # 6. Maho_InitHero
    target_6 = """function Maho_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(h))
    set udg_Maho_Hero[pId] = h
    set udg_Maho_MoveSpeed[pId] = 190.0"""
    replacement_6 = """function Maho_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(h))
    set udg_Maho_Hero[pId] = h
    set udg_Maho_MoveSpeed[pId] = 190.0
    set udg_Maho_AntiMahoAdapt[pId] = 0.0
    set udg_Maho_WheelSpinTimer[pId] = 0.0"""
    patches.append(("Maho_InitHero", target_6, replacement_6))

    # 7. Maho_ApplyDeathPenalty
    target_7 = """    set i = 0
    loop
        exitwhen i > 11
        set udg_Maho_SkillPct[pId * 12 + i] = udg_Maho_SkillPct[pId * 12 + i] * 0.70
        set i = i + 1
    endloop

    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 4.0, "|cffff6600[法轮碎裂]|r 魔虚罗真正阵亡，已积累的适应进度回退 30%！")"""
    replacement_7 = """    set i = 0
    loop
        exitwhen i > 11
        set udg_Maho_SkillPct[pId * 12 + i] = udg_Maho_SkillPct[pId * 12 + i] * 0.70
        set i = i + 1
    endloop

    set udg_Maho_AntiMahoAdapt[pId] = udg_Maho_AntiMahoAdapt[pId] * 0.70

    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 4.0, "|cffff6600[法轮碎裂]|r 魔虚罗真正阵亡，已积累的适应进度回退 30%！")"""
    patches.append(("Maho_ApplyDeathPenalty", target_7, replacement_7))

    # 8. Maho_HasEnemyNearby & Maho_CapTimerLoop
    target_8 = """    if GetUnitAbilityLevel(wt, 'A035') > 0 or uId == 'H005' then
        call Maho_AddSkillAdapt(pId, 'A035', 0.01)
    endif
endfunction

function Maho_CapTimerLoop takes nothing returns nothing
    local integer pId = 0
    local unit h = null
    local unit wt = null
    local integer atkCat = 0
    local integer defType = 0
    local real hx = 0.0
    local real hy = 0.0
    local real tx = 0.0
    local real ty = 0.0
    local real dist = 0.0

    set pId = 0
    loop
        exitwhen pId > 7
        set udg_Maho_LastSkillTime[pId] = RMaxBJ(0.0, udg_Maho_LastSkillTime[pId] - 1.0)
        if udg_Maho_EggCD[pId] > 0.0 then
            set udg_Maho_EggCD[pId] = RMaxBJ(0.0, udg_Maho_EggCD[pId] - 1.0)
        endif

        if udg_Maho_InEgg[pId] then
            set udg_Maho_EggTimer[pId] = udg_Maho_EggTimer[pId] - 1.0
            if udg_Maho_EggTimer[pId] <= 0.0 then
                call Maho_OnEggComplete(pId)
            endif
        elseif udg_Maho_Hero[pId] != null and Maho_IsUnitAlive(udg_Maho_Hero[pId]) then
            set h = udg_Maho_Hero[pId]

            // Chase Speed & Winged Flight Adaptation
            if GetUnitCurrentOrder(h) != 0 then"""
    replacement_8 = """    if GetUnitAbilityLevel(wt, 'A035') > 0 or uId == 'H005' then
        call Maho_AddSkillAdapt(pId, 'A035', 0.01)
    endif
endfunction

function Maho_HasEnemyNearby takes player p, real x, real y, real radius returns boolean
    local unit enumU = null
    if udg_EnumGroup == null then
        set udg_EnumGroup = CreateGroup()
    endif
    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRange(udg_EnumGroup, x, y, radius, null)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if IsUnitEnemy(enumU, p) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' and not IsUnitInvisible(enumU, p) then
            call GroupClear(udg_EnumGroup)
            set enumU = null
            return true
        endif
    endloop
    set enumU = null
    return false
endfunction

function Maho_CapTimerLoop takes nothing returns nothing
    local integer pId = 0
    local unit h = null
    local unit wt = null
    local integer atkCat = 0
    local integer defType = 0
    local real hx = 0.0
    local real hy = 0.0
    local real tx = 0.0
    local real ty = 0.0
    local real dist = 0.0

    set pId = 0
    loop
        exitwhen pId > 7
        set udg_Maho_LastSkillTime[pId] = RMaxBJ(0.0, udg_Maho_LastSkillTime[pId] - 1.0)
        if udg_Maho_EggCD[pId] > 0.0 then
            set udg_Maho_EggCD[pId] = RMaxBJ(0.0, udg_Maho_EggCD[pId] - 1.0)
        endif

        if udg_Maho_InEgg[pId] then
            set udg_Maho_EggTimer[pId] = udg_Maho_EggTimer[pId] - 1.0
            if udg_Maho_EggTimer[pId] <= 0.0 then
                call Maho_OnEggComplete(pId)
            endif
        elseif udg_Maho_Hero[pId] != null and Maho_IsUnitAlive(udg_Maho_Hero[pId]) then
            set h = udg_Maho_Hero[pId]

            // Chase Speed & Winged Flight Adaptation (Only triggers when moving AND near enemies or watching a target)
            if GetUnitCurrentOrder(h) != 0 and (Maho_HasEnemyNearby(Player(pId), GetUnitX(h), GetUnitY(h), 1600.0) or (udg_Maho_WatchTarget[pId] != null and Maho_IsUnitAlive(udg_Maho_WatchTarget[pId]))) then"""
    patches.append(("Maho_HasEnemyNearby & Maho_CapTimerLoop chase speed", target_8, replacement_8))

    # 9. Q watch anti-maho analysis in Maho_CapTimerLoop
    target_9 = """                    set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
                    call Maho_AnalyzeTargetSkills(pId, wt)

                    call BlzSetUnitMaxHP(h, BlzGetUnitMaxHP(h) + 3)"""
    replacement_9 = """                    set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
                    call Maho_AnalyzeTargetSkills(pId, wt)

                    if GetUnitTypeId(wt) == 'H006' and IsUnitEnemy(wt, Player(pId)) then
                        call Maho_AddAntiMahoAdapt(pId, 0.025)
                    endif

                    call BlzSetUnitMaxHP(h, BlzGetUnitMaxHP(h) + 3)"""
    patches.append(("Q watch anti-maho analysis", target_9, replacement_9))

    # 10. Maho_StealthLoop wheel freeze
    target_10 = """        // Wheel dynamic spin countdown
        if udg_Maho_WheelSpinTimer[pId] > 0.0 then
            set udg_Maho_WheelSpinTimer[pId] = udg_Maho_WheelSpinTimer[pId] - 0.05
            if udg_Maho_WheelSpinTimer[pId] <= 0.0 then
                set udg_Maho_WheelSpinTimer[pId] = 0.0
                if udg_Maho_WheelFx[pId] != null then
                    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0)
                endif
            endif
        endif"""
    replacement_10 = """        // Wheel dynamic spin countdown & continuous freeze lock
        if udg_Maho_WheelSpinTimer[pId] > 0.0 then
            set udg_Maho_WheelSpinTimer[pId] = udg_Maho_WheelSpinTimer[pId] - 0.05
            if udg_Maho_WheelSpinTimer[pId] <= 0.0 then
                set udg_Maho_WheelSpinTimer[pId] = 0.0
                if udg_Maho_WheelFx[pId] != null then
                    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)
                endif
            endif
        else
            if udg_Maho_WheelFx[pId] != null then
                call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)
            endif
        endif"""
    patches.append(("Maho_StealthLoop wheel freeze lock", target_10, replacement_10))

    # 11. Maho_CastW anti-maho adapt
    target_11 = """    set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
    set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
    if udg_Maho_AtkHits[pId] >= 4 then
        set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
        call Maho_AddBaseDamage(caster, 1)
    endif
    call Maho_UpdateUI(pId)"""
    replacement_11 = """    set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
    set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
    if udg_Maho_AtkHits[pId] >= 4 then
        set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
        call Maho_AddBaseDamage(caster, 1)
    endif
    if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(caster)) then
        call Maho_AddAntiMahoAdapt(pId, 0.02)
        call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
    endif
    call Maho_UpdateUI(pId)"""
    patches.append(("Maho_CastW anti-maho adapt", target_11, replacement_11))

    # 12. Maho_CastE anti-maho adapt
    target_12 = """    if udg_Maho_WatchTarget[pId] != null and Maho_IsUnitAlive(udg_Maho_WatchTarget[pId]) then
        set defType = BlzGetUnitIntegerField(udg_Maho_WatchTarget[pId], UNIT_IF_DEFENSE_TYPE)
        if defType >= 0 and defType <= 7 then
            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.05
        endif
    endif"""
    replacement_12 = """    if udg_Maho_WatchTarget[pId] != null and Maho_IsUnitAlive(udg_Maho_WatchTarget[pId]) then
        set defType = BlzGetUnitIntegerField(udg_Maho_WatchTarget[pId], UNIT_IF_DEFENSE_TYPE)
        if defType >= 0 and defType <= 7 then
            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.05
        endif
        if GetUnitTypeId(udg_Maho_WatchTarget[pId]) == 'H006' and IsUnitEnemy(udg_Maho_WatchTarget[pId], Player(pId)) then
            call Maho_AddAntiMahoAdapt(pId, 0.06)
        endif
    endif"""
    patches.append(("Maho_CastE anti-maho adapt", target_12, replacement_12))

    # 13. DM_OnDamaged declaration of srcMahoPid
    target_13 = """    local integer mahoPid = 0
    local integer cat = 0"""
    replacement_13 = """    local integer mahoPid = 0
    local integer srcMahoPid = 0
    local integer cat = 0"""
    patches.append(("DM_OnDamaged srcMahoPid decl", target_13, replacement_13))

    # 14. DM_OnDamaged offensive anti-maho adapt
    target_14 = """            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
            call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
            set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
            if udg_Maho_AtkHits[pId] >= 4 then
                set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
                call Maho_AddBaseDamage(src, 1)
            endif
            call Maho_UpdateUI(pId)"""
    replacement_14 = """            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
            call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
            set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
            if udg_Maho_AtkHits[pId] >= 4 then
                set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
                call Maho_AddBaseDamage(src, 1)
            endif
            if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                call Maho_AddAntiMahoAdapt(pId, 0.02)
                call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
            endif
            call Maho_UpdateUI(pId)"""
    patches.append(("DM_OnDamaged offensive anti-maho adapt", target_14, replacement_14))

    # 15. DM_OnDamaged defensive anti-maho adapt
    target_15 = """            set effResist = RMaxBJ(udg_Maho_DefAdapt[mahoPid * 8 + cat], skillPct)
            if effResist >= 0.9999 then
                set finalDmg = 0.0
                set effResist = 1.00
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", tgt, "origin"))
            else
                set finalDmg = dmg * (1.0 - effResist)
            endif
            call BlzSetEventDamage(finalDmg)"""
    replacement_15 = """            set effResist = RMaxBJ(udg_Maho_DefAdapt[mahoPid * 8 + cat], skillPct)
            if GetUnitTypeId(src) == 'H006' then
                set srcMahoPid = GetPlayerId(GetOwningPlayer(src))
                set effResist = effResist * (1.0 - udg_Maho_AntiMahoAdapt[srcMahoPid])
            endif

            if effResist >= 0.9999 then
                set finalDmg = 0.0
                set effResist = 1.00
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", tgt, "origin"))
            else
                set finalDmg = dmg * (1.0 - effResist)
            endif
            call BlzSetEventDamage(finalDmg)"""
    patches.append(("DM_OnDamaged defensive anti-maho adapt", target_15, replacement_15))

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
    print("All patches successfully applied to payload/war3map.j!")

if __name__ == '__main__':
    apply_patches()
