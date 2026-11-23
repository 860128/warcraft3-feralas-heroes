# -*- coding: utf-8 -*-
import sys

def apply_patches():
    with open('payload/war3map.j', 'rb') as f:
        content = f.read().decode('utf-8')

    is_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    patches = []

    # 1. Maho_ApplyWheelVisual and updated Maho_AddAntiMahoAdapt
    target_1 = """function Maho_AddAntiMahoAdapt takes integer pId, real amount returns nothing
    local real oldVal = udg_Maho_AntiMahoAdapt[pId]
    local real newVal = RMinBJ(1.0, oldVal + amount)
    set udg_Maho_AntiMahoAdapt[pId] = newVal
    if oldVal < 0.9999 and newVal >= 0.9999 then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 5.0, "|cffffcc00【法轮终极反制 · 破法适应完成！】|r 魔虚罗已完全解析同类的适应法则，此后斩击敌方魔虚罗将 100% 无视其防御免疫！")
    endif
endfunction"""

    replacement_1 = """function Maho_ApplyWheelVisual takes integer pId returns nothing
    local effect fx = udg_Maho_WheelFx[pId]
    local real anti = udg_Maho_AntiMahoAdapt[pId]
    local real baseScale = 0.62
    if fx == null then
        return
    endif
    if udg_Maho_IsWinged[pId] then
        set baseScale = 1.00
    endif
    if anti >= 3.9999 then
        set baseScale = baseScale + 0.15
        call BlzSetSpecialEffectColor(fx, 255, 25, 45)
    elseif anti >= 2.9999 then
        call BlzSetSpecialEffectColor(fx, 65, 225, 255)
    elseif anti >= 1.9999 then
        call BlzSetSpecialEffectColor(fx, 195, 75, 255)
    elseif anti >= 0.9999 then
        call BlzSetSpecialEffectColor(fx, 255, 115, 40)
    else
        call BlzSetSpecialEffectColor(fx, 255, 215, 45)
    endif
    call BlzSetSpecialEffectScale(fx, baseScale)
endfunction

function Maho_AddAntiMahoAdapt takes integer pId, real amount returns nothing
    local real oldVal = udg_Maho_AntiMahoAdapt[pId]
    local real newVal = RMinBJ(4.0, oldVal + amount)
    set udg_Maho_AntiMahoAdapt[pId] = newVal

    if oldVal < 0.9999 and newVal >= 0.9999 then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 5.0, "|cffffcc00【破法升维 · 一阶达成】|r 已彻底瓦解同类防御适应，法轮化为赤金，开始解析其护甲构造！")
        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
    endif
    if oldVal < 1.9999 and newVal >= 1.9999 then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 5.0, "|cffffcc00【破法升维 · 二阶达成】|r 已彻底无视同类物理护甲（拳拳到肉），法轮化为虚空苍紫，开始解析其生命本源！")
        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
    endif
    if oldVal < 2.9999 and newVal >= 2.9999 then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 5.0, "|cffffcc00【破法升维 · 三阶达成】|r 斩击附带 1.5% 最大生命纯粹真伤，法轮化为星界苍蓝，开始解析其涅槃因果！")
        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
    endif
    if oldVal < 3.9999 and newVal >= 3.9999 then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff0033【隐藏彩蛋 · 四阶弑神血轮觉醒！】|r 魔虚罗已彻底看穿同类的涅槃因果，连【无敌凤凰金卵】也能直接一剑斩碎！")
        call Maho_TriggerWheelSpin(pId, 2.50, 3.5)
    endif

    call Maho_ApplyWheelVisual(pId)
endfunction"""
    patches.append(("Maho_ApplyWheelVisual & Maho_AddAntiMahoAdapt 4-stage", target_1, replacement_1))

    # 2. Maho_ApplyAppearance: call Maho_ApplyWheelVisual(pId)
    target_2 = """    set udg_Maho_WheelFx[pId] = AddSpecialEffectTarget("war3mapImported\\\\MahoWheel.mdx", h, "overhead")
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)
    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])"""

    replacement_2 = """    set udg_Maho_WheelFx[pId] = AddSpecialEffectTarget("war3mapImported\\\\MahoWheel.mdx", h, "overhead")
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    call BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)
    call Maho_ApplyWheelVisual(pId)
    call SetUnitMoveSpeed(h, udg_Maho_MoveSpeed[pId])"""
    patches.append(("Maho_ApplyAppearance Maho_ApplyWheelVisual", target_2, replacement_2))

    # 3. Add Maho_FormatAntiMaho and update Maho_UpdateUI
    target_3 = """function Maho_FormatDefPct takes real val returns string
    if val >= 0.9999 then
        return "|cff00ff00100%[免疫]|r"
    elseif val >= 0.95 then
        return R2SW(val * 100.0, 1, 1) + "%"
    else
        return I2S(R2I(val * 100.0)) + "%"
    endif
endfunction

function Maho_UpdateUI takes integer pId returns nothing"""

    replacement_3 = """function Maho_FormatDefPct takes real val returns string
    if val >= 0.9999 then
        return "|cff00ff00100%[免疫]|r"
    elseif val >= 0.95 then
        return R2SW(val * 100.0, 1, 1) + "%"
    else
        return I2S(R2I(val * 100.0)) + "%"
    endif
endfunction

function Maho_FormatAntiMaho takes real anti returns string
    local integer pct = R2I(anti * 100.0)
    local integer p2 = 0
    local real p3 = 0.0
    if anti < 1.0 then
        return "1阶 (" + I2S(pct) + "%/400% | 适应穿透" + I2S(pct) + "%)"
    elseif anti < 2.0 then
        set p2 = R2I((anti - 1.0) * 100.0)
        return "2阶 (" + I2S(pct) + "%/400% | 护甲无视" + I2S(p2) + "%)"
    elseif anti < 3.0 then
        set p3 = (anti - 2.0) * 1.5
        return "3阶 (" + I2S(pct) + "%/400% | 斩魂真伤+" + R2SW(p3, 1, 1) + "%最大生命)"
    elseif anti < 4.0 then
        return "3阶 (" + I2S(pct) + "%/400% | 斩魂真伤+1.5%最大生命)"
    else
        return "|cffff00334阶·弑神觉醒 (400%满阶 | 可直接斩碎凤凰金卵！)|r"
    endif
endfunction

function Maho_UpdateUI takes integer pId returns nothing"""
    patches.append(("Maho_FormatAntiMaho decl", target_3, replacement_3))

    # 4. Update Maho_UpdateUI display
    target_4 = """    if udg_Maho_AntiMahoAdapt[pId] > 0.0 then
        set tip = tip + "- |cffff3366破法穿透·反魔虚罗适应：|r穿透同类防御免疫 " + I2S(R2I(udg_Maho_AntiMahoAdapt[pId] * 100.0)) + "%|n"
    endif"""

    replacement_4 = """    if udg_Maho_AntiMahoAdapt[pId] > 0.0 then
        set tip = tip + "- |cffff3366破法升维：|r" + Maho_FormatAntiMaho(udg_Maho_AntiMahoAdapt[pId]) + "|n"
    endif"""
    patches.append(("Maho_UpdateUI 4-stage display", target_4, replacement_4))

    # 5. Update Maho_PrintOverview display
    target_5 = """    if udg_Maho_AntiMahoAdapt[pId] > 0.0 then
        call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cffff3366[破法穿透·反魔虚罗适应]|r 穿透同类防御免疫: " + I2S(R2I(udg_Maho_AntiMahoAdapt[pId] * 100.0)) + "%")
    endif"""

    replacement_5 = """    if udg_Maho_AntiMahoAdapt[pId] > 0.0 then
        call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cffff3366[破法升维 · 反魔虚罗适应]|r " + Maho_FormatAntiMaho(udg_Maho_AntiMahoAdapt[pId]))
    endif"""
    patches.append(("Maho_PrintOverview 4-stage display", target_5, replacement_5))

    # 6. Maho_ApplyDeathPenalty
    target_6 = """    set udg_Maho_AntiMahoAdapt[pId] = udg_Maho_AntiMahoAdapt[pId] * 0.70

    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 4.0, "|cffff6600[法轮碎裂]|r 魔虚罗真正阵亡，已积累的适应进度回退 30%！")"""

    replacement_6 = """    set udg_Maho_AntiMahoAdapt[pId] = udg_Maho_AntiMahoAdapt[pId] * 0.70
    call Maho_ApplyWheelVisual(pId)

    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 4.0, "|cffff6600[法轮碎裂]|r 魔虚罗真正阵亡，已积累的适应进度回退 30%！")"""
    patches.append(("Maho_ApplyDeathPenalty visual update", target_6, replacement_6))

    # 7. Maho_OnEggComplete
    target_7 = """        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Avatar\\\\AvatarCaster.mdl", h, "origin"))"""

    replacement_7 = """        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
        call Maho_ApplyWheelVisual(pId)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Avatar\\\\AvatarCaster.mdl", h, "origin"))"""
    patches.append(("Maho_OnEggComplete visual update", target_7, replacement_7))

    # 8. Maho_CapTimerLoop winged flight & Q watch
    target_8 = """                        set udg_Maho_IsWinged[pId] = true
                        call Maho_ApplyAppearance(h, pId)
                        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)"""

    replacement_8 = """                        set udg_Maho_IsWinged[pId] = true
                        call Maho_ApplyAppearance(h, pId)
                        call Maho_TriggerWheelSpin(pId, 1.50, 3.0)
                        call Maho_ApplyWheelVisual(pId)"""
    patches.append(("Maho_CapTimerLoop winged visual", target_8, replacement_8))

    target_9 = """                    if GetUnitTypeId(wt) == 'H006' and IsUnitEnemy(wt, Player(pId)) then
                        call Maho_AddAntiMahoAdapt(pId, 0.025)
                    endif"""

    replacement_9 = """                    if GetUnitTypeId(wt) == 'H006' and IsUnitEnemy(wt, Player(pId)) then
                        call Maho_AddAntiMahoAdapt(pId, 0.035)
                    endif"""
    patches.append(("Maho_CapTimerLoop Q watch 3.5%", target_9, replacement_9))

    # 9. Maho_StealthLoop remove SetUnitInvulnerable(egg, true)
    target_10 = """                set egg = CreateUnit(Player(pId), 'u004', GetUnitX(h), GetUnitY(h), 270.0)
                call SetUnitVertexColor(egg, 255, 220, 80, 255)
                call SetUnitInvulnerable(egg, true)
                set udg_Maho_EggUnit[pId] = egg"""

    replacement_10 = """                set egg = CreateUnit(Player(pId), 'u004', GetUnitX(h), GetUnitY(h), 270.0)
                call SetUnitVertexColor(egg, 255, 220, 80, 255)
                set udg_Maho_EggUnit[pId] = egg"""
    patches.append(("Maho_StealthLoop remove invulnerable egg", target_10, replacement_10))

    # 10. Maho_CastW 3%
    target_11 = """    if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(caster)) then
        call Maho_AddAntiMahoAdapt(pId, 0.02)
        call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
    endif"""

    replacement_11 = """    if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(caster)) then
        call Maho_AddAntiMahoAdapt(pId, 0.03)
        call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
    endif"""
    patches.append(("Maho_CastW 3%", target_11, replacement_11))

    # 11. Maho_CastE 8%
    target_12 = """        if GetUnitTypeId(udg_Maho_WatchTarget[pId]) == 'H006' and IsUnitEnemy(udg_Maho_WatchTarget[pId], Player(pId)) then
            call Maho_AddAntiMahoAdapt(pId, 0.06)
        endif"""

    replacement_12 = """        if GetUnitTypeId(udg_Maho_WatchTarget[pId]) == 'H006' and IsUnitEnemy(udg_Maho_WatchTarget[pId], Player(pId)) then
            call Maho_AddAntiMahoAdapt(pId, 0.08)
        endif"""
    patches.append(("Maho_CastE 8%", target_12, replacement_12))

    # 12. DM_OnDamaged locals
    target_13 = """    local integer mahoPid = 0
    local integer srcMahoPid = 0
    local integer cat = 0"""

    replacement_13 = """    local integer mahoPid = 0
    local integer srcMahoPid = 0
    local integer cat = 0
    local real anti = 0.0
    local real p2 = 0.0
    local real p3 = 0.0
    local real tgtArmor = 0.0
    local real armorRed = 0.0
    local integer srcPid = 0"""
    patches.append(("DM_OnDamaged locals", target_13, replacement_13))

    # 13. DM_OnDamaged u004 interception
    target_14 = """    if src != null and tgt != null and GetEventDamage() > 0.0 then
        set dmg = GetEventDamage()

        set hIdx = DM_GetHeroIndex(src)"""

    replacement_14 = """    if src != null and tgt != null and GetEventDamage() > 0.0 then
        set dmg = GetEventDamage()

        // Nirvana Golden Egg [u004] Special Damage Filtering
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
        endif

        set hIdx = DM_GetHeroIndex(src)"""
    patches.append(("DM_OnDamaged u004 interception", target_14, replacement_14))

    # 14. DM_OnDamaged offensive Maho 3%
    target_15 = """                if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                    call Maho_AddAntiMahoAdapt(pId, 0.02)
                    call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
                endif"""

    replacement_15 = """                if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                    call Maho_AddAntiMahoAdapt(pId, 0.03)
                    call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
                endif"""
    patches.append(("DM_OnDamaged offensive Maho 3%", target_15, replacement_15))

    # 15. DM_OnDamaged defensive Maho 4 stages
    target_16 = """            set effResist = RMaxBJ(udg_Maho_DefAdapt[mahoPid * 8 + cat], skillPct)
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

    replacement_16 = """            set effResist = RMaxBJ(udg_Maho_DefAdapt[mahoPid * 8 + cat], skillPct)
            if GetUnitTypeId(src) == 'H006' then
                set srcMahoPid = GetPlayerId(GetOwningPlayer(src))
                set anti = udg_Maho_AntiMahoAdapt[srcMahoPid]

                // Stage 1 (0% ~ 100%): Penetrate defense adaptation
                set effResist = effResist * (1.0 - RMinBJ(1.0, anti))

                // Stage 2 (100% ~ 200%): Ignore target armor (punch-to-the-bone)
                if anti > 1.0 then
                    set p2 = RMinBJ(1.0, anti - 1.0)
                    set tgtArmor = BlzGetUnitArmor(tgt)
                    if tgtArmor > 0.0 then
                        set armorRed = (tgtArmor * 0.06) / (1.0 + tgtArmor * 0.06)
                        if armorRed < 0.95 then
                            set dmg = dmg + (dmg / (1.0 - armorRed) - dmg) * p2
                        endif
                    endif
                endif
            endif

            if effResist >= 0.9999 then
                set finalDmg = 0.0
                set effResist = 1.00
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", tgt, "origin"))
            else
                set finalDmg = dmg * (1.0 - effResist)
            endif

            // Stage 3 (200% ~ 300%): Bonus pure true damage (up to 1.5% target max HP)
            if GetUnitTypeId(src) == 'H006' and anti > 2.0 then
                set p3 = RMinBJ(1.0, anti - 2.0)
                set finalDmg = finalDmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.015 * p3
            endif

            call BlzSetEventDamage(finalDmg)"""
    patches.append(("DM_OnDamaged defensive Maho 4 stages", target_16, replacement_16))

    # 16. DM_OnUnitDeath: golden egg [u004] destroyed
    target_17 = """    // 1. Dream Master Possession Return
    set idx = DM_FindCapIndex(dead)"""

    replacement_17 = """    // Golden Egg [u004] destroyed by 4-Stage Mahoraga
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
    endif

    // 1. Dream Master Possession Return
    set idx = DM_FindCapIndex(dead)"""
    patches.append(("DM_OnUnitDeath egg death listener", target_17, replacement_17))

    # 17. Chat command -anti for testing
    target_18 = """    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    elseif s == "-evo" then"""

    replacement_18 = """    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    elseif s == "-anti" then
        if udg_Maho_Hero[pId] != null and Maho_IsUnitAlive(udg_Maho_Hero[pId]) then
            call Maho_AddAntiMahoAdapt(pId, 1.0)
            call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cffffcc00[测试模式]|r 魔虚罗破法升维 +100% (当前: " + I2S(R2I(udg_Maho_AntiMahoAdapt[pId] * 100.0)) + "%)！")
            call Maho_UpdateUI(pId)
        endif
    elseif s == "-evo" then"""
    patches.append(("Chat command -anti", target_18, replacement_18))

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
    print("All patches successfully applied to payload/war3map.j for v6.0!")

if __name__ == '__main__':
    apply_patches()
