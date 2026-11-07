# -*- coding: utf-8 -*-
import sys
import re

def apply_patch():
    with open('payload/war3map.j', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Load calibrated templates from tools/verify_tpl_table.py
    import sys, os
    sys.path.insert(0, os.getcwd())
    from tools.verify_tpl_table import tpls
    assert len(tpls) == 90

    tpl_calls = []
    for t in tpls:
        cat, tier, sub, skin, name, hp, mana, dmg, armor, cool, move, rangeN, scale, abil, abilName = t
        btnLabel = f"{name} ({abilName})"
        line = f'    call Wild_SetTpl({cat}, {tier}, {sub}, \'{skin}\', "{name}", "{btnLabel}", {hp}, {mana}, {dmg}, {armor:.1f}, {cool:.2f}, {move:.1f}, {rangeN}, {scale:.2f}, \'{abil}\', "{abilName}")'
        tpl_calls.append(line)
    tpl_block = "\n".join(tpl_calls)

    # Replace Wild_InitCreepTemplates body
    pattern_init = r'function Wild_InitCreepTemplates takes nothing returns nothing\n.*?\nendfunction'
    repl_init = f'function Wild_InitCreepTemplates takes nothing returns nothing\n{tpl_block}\nendfunction'
    content, count = re.subn(pattern_init, lambda m: repl_init, content, flags=re.DOTALL)
    assert count == 1, f"Wild_InitCreepTemplates match count: {count}"
    print("1. Wild_InitCreepTemplates replaced with 90 calibrated templates.")

    # 2. Add Wild_ClearMorphAbil right before Wild_DoMorph
    clear_func = '''function Wild_ClearMorphAbil takes unit u, integer pId returns nothing
    local integer currAbil = udg_Wild_CurrentAbil[pId]
    if u == null then
        return
    endif
    if currAbil != 0 then
        call UnitMakeAbilityPermanent(u, false, currAbil)
        call UnitRemoveAbility(u, currAbil)
        set udg_Wild_CurrentAbil[pId] = 0
    endif
    // Complete sweep of all 23 potential morph abilities to ensure 0 residue
    call UnitMakeAbilityPermanent(u, false, 'ACbl')
    call UnitRemoveAbility(u, 'ACbl')
    call UnitMakeAbilityPermanent(u, false, 'ACls')
    call UnitRemoveAbility(u, 'ACls')
    call UnitMakeAbilityPermanent(u, false, 'ACpu')
    call UnitRemoveAbility(u, 'ACpu')
    call UnitMakeAbilityPermanent(u, false, 'ACct')
    call UnitRemoveAbility(u, 'ACct')
    call UnitMakeAbilityPermanent(u, false, 'ACbh')
    call UnitRemoveAbility(u, 'ACbh')
    call UnitMakeAbilityPermanent(u, false, 'ACev')
    call UnitRemoveAbility(u, 'ACev')
    call UnitMakeAbilityPermanent(u, false, 'ACtb')
    call UnitRemoveAbility(u, 'ACtb')
    call UnitMakeAbilityPermanent(u, false, 'ACro')
    call UnitRemoveAbility(u, 'ACro')
    call UnitMakeAbilityPermanent(u, false, 'ACif')
    call UnitRemoveAbility(u, 'ACif')
    call UnitMakeAbilityPermanent(u, false, 'ACsw')
    call UnitRemoveAbility(u, 'ACsw')
    call UnitMakeAbilityPermanent(u, false, 'AChx')
    call UnitRemoveAbility(u, 'AChx')
    call UnitMakeAbilityPermanent(u, false, 'ACst')
    call UnitRemoveAbility(u, 'ACst')
    call UnitMakeAbilityPermanent(u, false, 'ACsh')
    call UnitRemoveAbility(u, 'ACsh')
    call UnitMakeAbilityPermanent(u, false, 'ACfl')
    call UnitRemoveAbility(u, 'ACfl')
    call UnitMakeAbilityPermanent(u, false, 'ACfn')
    call UnitRemoveAbility(u, 'ACfn')
    call UnitMakeAbilityPermanent(u, false, 'ACf2')
    call UnitRemoveAbility(u, 'ACf2')
    call UnitMakeAbilityPermanent(u, false, 'ACen')
    call UnitRemoveAbility(u, 'ACen')
    call UnitMakeAbilityPermanent(u, false, 'ACrj')
    call UnitRemoveAbility(u, 'ACrj')
    call UnitMakeAbilityPermanent(u, false, 'ACcs')
    call UnitRemoveAbility(u, 'ACcs')
    call UnitMakeAbilityPermanent(u, false, 'ACav')
    call UnitRemoveAbility(u, 'ACav')
    call UnitMakeAbilityPermanent(u, false, 'ACdv')
    call UnitRemoveAbility(u, 'ACdv')
    call UnitMakeAbilityPermanent(u, false, 'A025')
    call UnitRemoveAbility(u, 'A025')
    call UnitMakeAbilityPermanent(u, false, 'A026')
    call UnitRemoveAbility(u, 'A026')
endfunction

function Wild_DoMorph'''

    assert 'function Wild_DoMorph' in content
    content = content.replace('function Wild_DoMorph', clear_func, 1)
    print("2. Wild_ClearMorphAbil inserted before Wild_DoMorph.")

    # 3. In Wild_DoMorph, replace remove old ability with Wild_ClearMorphAbil
    old_remove_morph = '''    // Remove old ability
    if udg_Wild_CurrentAbil[pId] != 0 then
        call UnitRemoveAbility(u, udg_Wild_CurrentAbil[pId])
        set udg_Wild_CurrentAbil[pId] = 0
    endif'''
    new_remove_morph = '''    // Remove old ability and sweep all potential morph abilities
    call Wild_ClearMorphAbil(u, pId)'''
    assert old_remove_morph in content
    content = content.replace(old_remove_morph, new_remove_morph, 1)
    print("3. Wild_DoMorph updated to use Wild_ClearMorphAbil.")

    # 4. Replace Wild_RevertToAvatar with enhanced version that handles dead/alive & sweeps abilities
    pattern_revert = r'function Wild_RevertToAvatar takes unit u returns nothing\n.*?\nendfunction'
    repl_revert = r'''function Wild_RevertToAvatar takes unit u returns nothing
    local player p = null
    local integer pId = 0
    local real oldHP = 0.0
    local real oldMaxHP = 0.0
    local real hpRatio = 1.0
    local real oldMaxMana = 0.0
    local integer heroStr = 0
    local integer heroAgi = 0
    local integer heroInt = 0
    local integer hLv = 0
    local integer baseMaxHP = 0
    local integer baseMaxMana = 0
    local integer baseDmg = 0
    local real baseArmor = 0.0
    local real baseCool = 1.50
    local real baseMove = 310.0
    local integer baseRange = 600
    local integer newCurHP = 1
    local integer newCurMana = 0

    if u == null then
        return
    endif
    set p = GetOwningPlayer(u)
    set pId = GetPlayerId(p)

    if not udg_Wild_IsMorphed[pId] then
        if not IsUnitType(u, UNIT_TYPE_DEAD) and GetPlayerController(p) == MAP_CONTROL_USER then
            call DisplayTimedTextToPlayer(p, 0, 0, 2.0, "|cffffcc00[万灵化身]|r 当前已处于本体神体形态。")
        endif
        set p = null
        return
    endif

    // Remove attached creep ability and sweep residue
    call Wild_ClearMorphAbil(u, pId)

    // Restore skin, name, scale
    call BlzSetUnitSkin(u, 'H005')
    call BlzSetUnitName(u, "万灵化身")
    call SetUnitScale(u, 1.10, 1.10, 1.10)

    // Land back to ground
    call SetUnitFlyHeight(u, 0.0, 800.0)
    call SetUnitPathing(u, true)

    // Restore 600 range missile
    call SetUnitAcquireRange(u, 700.0)
    call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 0, 600.0)
    call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 1, 600.0)
    call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_PROJECTILE_SPEED, 0, 1000.0)
    call BlzSetUnitWeaponStringField(u, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0, "Abilities\\Weapons\\KeeperGroveMissile\\KeeperGroveMissile.mdl")

    set udg_Wild_IsMorphed[pId] = false
    set udg_Wild_CurrentForm[pId] = 0
    set udg_Wild_CurrentFormType[pId] = 0
    set udg_Wild_CurrentFormLevel[pId] = 0

    if not IsUnitType(u, UNIT_TYPE_DEAD) then
        // Ratio preservation
        set oldHP = GetWidgetLife(u)
        set oldMaxHP = I2R(BlzGetUnitMaxHP(u))
        if oldMaxHP > 0.0 then
            set hpRatio = oldHP / oldMaxHP
        else
            set hpRatio = 1.0
        endif
        if hpRatio <= 0.0 then
            set hpRatio = 0.01
        endif
        if hpRatio > 1.0 then
            set hpRatio = 1.0
        endif

        set oldMaxMana = I2R(BlzGetUnitMaxMana(u))
        if oldMaxMana > 0.0 then
            set udg_Wild_StoredManaRatio[pId] = GetUnitState(u, UNIT_STATE_MANA) / oldMaxMana
            if udg_Wild_StoredManaRatio[pId] > 1.0 then
                set udg_Wild_StoredManaRatio[pId] = 1.0
            endif
        endif
        if udg_Wild_StoredManaRatio[pId] <= 0.0 then
            set udg_Wild_StoredManaRatio[pId] = 1.0
        endif

        // Base stats
        set heroStr = GetHeroStr(u, true)
        set heroAgi = GetHeroAgi(u, true)
        set heroInt = GetHeroInt(u, true)
        set hLv = GetHeroLevel(u)

        set baseMaxHP = 550 + heroStr * 22 + hLv * 45
        set baseMaxMana = 250 + heroInt * 15 + hLv * 25
        set baseDmg = 24 + R2I(I2R(heroStr + heroAgi + heroInt) * 0.65)
        set baseArmor = 2.0 + I2R(heroAgi) * 0.25
        set baseCool = 1.50
        set baseMove = 310.0
        set baseRange = 600

        call BlzSetUnitMaxHP(u, baseMaxHP)
        set newCurHP = R2I(I2R(baseMaxHP) * hpRatio)
        if newCurHP < 1 then
            set newCurHP = 1
        endif
        call SetWidgetLife(u, I2R(newCurHP))

        call BlzSetUnitMaxMana(u, baseMaxMana)
        set newCurMana = R2I(I2R(baseMaxMana) * udg_Wild_StoredManaRatio[pId])
        call SetUnitState(u, UNIT_STATE_MANA, I2R(newCurMana))

        call BlzSetUnitBaseDamage(u, baseDmg, 0)
        call BlzSetUnitArmor(u, baseArmor)
        call BlzSetUnitAttackCooldown(u, baseCool, 0)
        call SetUnitMoveSpeed(u, baseMove)

        if GetPlayerController(p) == MAP_CONTROL_USER then
            call DisplayTimedTextToPlayer(p, 0, 0, 3.0, "|cffffcc00[万灵化身]|r 已返璞归真，恢复自然神体！")
        endif
    endif

    set p = null
endfunction'''
    content, count = re.subn(pattern_revert, lambda m: repl_revert, content, flags=re.DOTALL)
    assert count == 1, f"Wild_RevertToAvatar match count: {count}"
    print("4. Wild_RevertToAvatar updated.")

    # 5. Update Wild_InitHero
    old_inithero = '''function Wild_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(h))
    set udg_Wild_Hero[pId] = h
    if GetUnitAbilityLevel(h, 'A034') == 0 then
        call UnitAddAbility(h, 'A034')
    endif
    if udg_Wild_IsMorphed[pId] then
        call Wild_RevertToAvatar(h)
    endif
endfunction'''
    new_inithero = '''function Wild_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(h))
    set udg_Wild_Hero[pId] = h
    if GetUnitAbilityLevel(h, 'A034') == 0 then
        call UnitAddAbility(h, 'A034')
    endif
    if udg_Wild_IsMorphed[pId] then
        call Wild_RevertToAvatar(h)
    else
        call Wild_ClearMorphAbil(h, pId)
    endif
endfunction'''
    assert old_inithero in content
    content = content.replace(old_inithero, new_inithero, 1)
    print("5. Wild_InitHero updated.")

    # 6. Update Wild_ShowSubDialog with dynamic button text
    pattern_subdialog = r'function Wild_ShowSubDialog takes player p, integer cat, integer tierLv returns nothing\n.*?\nendfunction'
    repl_subdialog = '''function Wild_ShowSubDialog takes player p, integer cat, integer tierLv returns nothing
    local integer pId = 0
    local unit u = null
    local string title = ""
    local string btnText = ""
    local integer subIdx = 1
    local integer abilCode = 'A031'
    local integer sLv = 1
    local real mult = 0.55
    local string tplName = ""
    local integer creepHP = 0
    local integer creepDmg = 0
    local integer bonusHP = 0
    local integer bonusDmg = 0
    local integer tplAbil = 0
    local string abilName = ""

    if p == null then
        return
    endif
    set pId = GetPlayerId(p)
    set u = udg_Wild_Hero[pId]
    if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
        return
    endif

    if cat == 2 then
        set abilCode = 'A032'
    elseif cat == 3 then
        set abilCode = 'A033'
    endif
    set sLv = GetUnitAbilityLevel(u, abilCode)
    if sLv < 1 then
        set sLv = 1
    endif
    if sLv == 1 then
        set mult = 0.55
    elseif sLv == 2 then
        set mult = 0.90
    else
        set mult = 1.30
    endif

    call DialogDisplay(p, udg_Wild_MorphDialog, false)
    call DialogClear(udg_Wild_MorphDialog)

    set title = "|cffffcc00[万灵化形 - " + I2S(tierLv) + "级野怪]|r 请选择化形目标:"
    call DialogSetMessage(udg_Wild_MorphDialog, title)

    set subIdx = 1
    loop
        exitwhen subIdx > 3
        set tplName = Wild_GetCreepName(cat, tierLv, subIdx)
        set creepHP = Wild_GetCreepBaseHP(cat, tierLv, subIdx)
        set creepDmg = Wild_GetCreepBaseDmg(cat, tierLv, subIdx)
        set bonusHP = R2I(I2R(creepHP) * mult)
        set bonusDmg = R2I(I2R(creepDmg) * mult)
        set tplAbil = Wild_GetCreepAbil(cat, tierLv, subIdx)
        set abilName = Strain_GetAbilName(tplAbil)

        set btnText = "[" + I2S(subIdx) + "] " + tplName + " (HP:+" + I2S(bonusHP) + " 攻:+" + I2S(bonusDmg) + " | 技能:" + abilName + ")"
        set udg_Wild_SubBtn[subIdx] = DialogAddButton(udg_Wild_MorphDialog, btnText, 48 + subIdx)
        set subIdx = subIdx + 1
    endloop

    set udg_Wild_SubBackBtn = DialogAddButton(udg_Wild_MorphDialog, "[4] 返回上一级 (重选等级)", 52)
    set udg_Wild_SubCancelBtn = DialogAddButton(udg_Wild_MorphDialog, "[0] 取消", 48)

    set udg_Wild_DialogState[pId] = 2
    call DialogDisplay(p, udg_Wild_MorphDialog, true)
endfunction'''
    content, count = re.subn(pattern_subdialog, lambda m: repl_subdialog, content, flags=re.DOTALL)
    assert count == 1, f"Wild_ShowSubDialog match count: {count}"
    print("6. Wild_ShowSubDialog updated to dynamic button text.")

    # 7. Add Wild_OnHeroReviveFinish right after DM_OnHeroRevivable
    target_revivable = '''function DM_OnHeroRevivable takes nothing returns boolean
    local unit rev = GetRevivableUnit()
    if rev != null and (IsUnitInGroup(rev, udg_FakeHeroGroup) or IsUnitIllusion(rev)) then
        call RemoveUnit(rev)
    endif
    set rev = null
    return false
endfunction'''

    new_revive_finish = '''function DM_OnHeroRevivable takes nothing returns boolean
    local unit rev = GetRevivableUnit()
    if rev != null and (IsUnitInGroup(rev, udg_FakeHeroGroup) or IsUnitIllusion(rev)) then
        call RemoveUnit(rev)
    endif
    set rev = null
    return false
endfunction

function Wild_OnHeroReviveFinish takes nothing returns boolean
    local unit rev = GetRevivingUnit()
    local integer pId = 0
    if rev == null then
        set rev = GetTriggerUnit()
    endif
    if rev != null and GetUnitTypeId(rev) == 'H005' then
        set pId = GetPlayerId(GetOwningPlayer(rev))
        call Wild_ClearMorphAbil(rev, pId)
        call Wild_RevertToAvatar(rev)
    endif
    set rev = null
    return false
endfunction'''
    assert target_revivable in content
    content = content.replace(target_revivable, new_revive_finish, 1)
    print("7. Wild_OnHeroReviveFinish added.")

    # 8. Register tReviveFinish in DM_InitTriggers
    target_init_triggers = '''    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()'''
    new_init_triggers = '''    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tReviveFinish = CreateTrigger()'''
    assert target_init_triggers in content
    content = content.replace(target_init_triggers, new_init_triggers, 1)

    target_reg_revive = '''    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))'''
    new_reg_revive = '''    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))

    call TriggerRegisterAnyUnitEventBJ(tReviveFinish, EVENT_PLAYER_HERO_REVIVE_FINISH)
    call TriggerAddCondition(tReviveFinish, Condition(function Wild_OnHeroReviveFinish))'''
    assert target_reg_revive in content
    content = content.replace(target_reg_revive, new_reg_revive, 1)

    target_null_revive = '''    set tRevive = null'''
    new_null_revive = '''    set tRevive = null
    set tReviveFinish = null'''
    assert target_null_revive in content
    content = content.replace(target_null_revive, new_null_revive, 1)
    print("8. tReviveFinish registered in DM_InitTriggers.")

    # 9. In Refuge_ProcessRevives, clean H005 on revive
    target_refuge_revive = '''                    call ReviveHero(u, GetUnitX(ref), GetUnitY(ref) - 150.0, true)
                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", GetUnitX(ref), GetUnitY(ref) - 150.0))'''
    new_refuge_revive = '''                    call ReviveHero(u, GetUnitX(ref), GetUnitY(ref) - 150.0, true)
                    if GetUnitTypeId(u) == 'H005' then
                        call Wild_ClearMorphAbil(u, pId)
                        call Wild_RevertToAvatar(u)
                    endif
                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", GetUnitX(ref), GetUnitY(ref) - 150.0))'''
    assert target_refuge_revive in content
    content = content.replace(target_refuge_revive, new_refuge_revive, 1)

    target_refuge_revive2 = '''                    call ReviveHero(u, GetStartLocationX(GetPlayerStartLocation(Player(pId))), GetStartLocationY(GetPlayerStartLocation(Player(pId))), true)
                    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 6.0, "|cff00ff00[避难所复活]|r 你的英雄已在出生点复活！")'''
    new_refuge_revive2 = '''                    call ReviveHero(u, GetStartLocationX(GetPlayerStartLocation(Player(pId))), GetStartLocationY(GetPlayerStartLocation(Player(pId))), true)
                    if GetUnitTypeId(u) == 'H005' then
                        call Wild_ClearMorphAbil(u, pId)
                        call Wild_RevertToAvatar(u)
                    endif
                    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 6.0, "|cff00ff00[避难所复活]|r 你的英雄已在出生点复活！")'''
    assert target_refuge_revive2 in content
    content = content.replace(target_refuge_revive2, new_refuge_revive2, 1)
    print("9. Refuge_ProcessRevives updated.")

    # 10. In AI_HeroLoop, clean H005 on revive
    target_ai_revive = '''                            call ReviveHero(h, GetUnitX(altar), GetUnitY(altar) - 150.0, true)
                            set udg_AI_DeadTimer[i] = 0.0'''
    new_ai_revive = '''                            call ReviveHero(h, GetUnitX(altar), GetUnitY(altar) - 150.0, true)
                            if GetUnitTypeId(h) == 'H005' then
                                call Wild_ClearMorphAbil(h, i)
                                call Wild_RevertToAvatar(h)
                            endif
                            set udg_AI_DeadTimer[i] = 0.0'''
    assert target_ai_revive in content
    content = content.replace(target_ai_revive, new_ai_revive, 1)

    target_ai_revive2 = '''                            call ReviveHero(h, GetStartLocationX(GetPlayerStartLocation(Player(i))), GetStartLocationY(GetPlayerStartLocation(Player(i))), true)
                            set udg_AI_DeadTimer[i] = 0.0'''
    new_ai_revive2 = '''                            call ReviveHero(h, GetStartLocationX(GetPlayerStartLocation(Player(i))), GetStartLocationY(GetPlayerStartLocation(Player(i))), true)
                            if GetUnitTypeId(h) == 'H005' then
                                call Wild_ClearMorphAbil(h, i)
                                call Wild_RevertToAvatar(h)
                            endif
                            set udg_AI_DeadTimer[i] = 0.0'''
    assert target_ai_revive2 in content
    content = content.replace(target_ai_revive2, new_ai_revive2, 1)
    print("10. AI_HeroLoop updated.")

    # Write patched file
    with open('payload/war3map.j', 'w', encoding='utf-8') as f:
        f.write(content)
    print("All patches successfully written to payload/war3map.j!")

if __name__ == '__main__':
    apply_patch()
