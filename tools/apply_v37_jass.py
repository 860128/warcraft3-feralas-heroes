# -*- coding: utf-8 -*-
import sys
import os
import re

def main():
    jass_path = 'payload/war3map.j'
    with open(jass_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original content length: {len(content)}")

    # 1. Globals declaration: Add udg_Wild_CurrentSubIdx, udg_Wild_HeroSoulHP, udg_Wild_HeroSoulDmg
    target_globals = '''    integer array udg_Wild_CurrentFormLevel
    integer array udg_Wild_CurrentAbil'''
    repl_globals = '''    integer array udg_Wild_CurrentFormLevel
    integer array udg_Wild_CurrentAbil
    integer array udg_Wild_CurrentSubIdx
    integer array udg_Wild_HeroSoulHP
    integer array udg_Wild_HeroSoulDmg'''
    assert target_globals in content, "Target globals not found"
    content = content.replace(target_globals, repl_globals, 1)
    print("1. Globals declared.")

    # 2. Wild_InitCreepTemplates with 90 calibrated templates from verify_tpl_table.py
    sys.path.insert(0, os.getcwd())
    from tools.verify_tpl_table import tpls
    assert len(tpls) == 90, f"Expected 90 templates, got {len(tpls)}"

    tpl_calls = []
    for t in tpls:
        cat, tier, sub, skin, name, hp, mana, dmg, armor, cool, move, rangeN, scale, abil, abilName = t
        btnLabel = f"{name} ({abilName})"
        line = f'    call Wild_SetTpl({cat}, {tier}, {sub}, \'{skin}\', "{name}", "{btnLabel}", {hp}, {mana}, {dmg}, {armor:.1f}, {cool:.2f}, {move:.1f}, {rangeN}, {scale:.2f}, \'{abil}\', "{abilName}")'
        tpl_calls.append(line)
    tpl_block = "\n".join(tpl_calls)

    pattern_init = r'function Wild_InitCreepTemplates takes nothing returns nothing\n.*?\nendfunction'
    repl_init = f'function Wild_InitCreepTemplates takes nothing returns nothing\n{tpl_block}\nendfunction'
    content, count = re.subn(pattern_init, lambda m: repl_init, content, flags=re.DOTALL)
    assert count == 1, f"Wild_InitCreepTemplates match count: {count}"
    print("2. Wild_InitCreepTemplates updated with 90 templates.")

    # 3. Wild_ClearMorphAbil: Add ACmi, ANpi, A037
    target_clear = '''    call UnitMakeAbilityPermanent(u, false, 'A025')
    call UnitRemoveAbility(u, 'A025')
    call UnitMakeAbilityPermanent(u, false, 'A026')
    call UnitRemoveAbility(u, 'A026')'''
    repl_clear = '''    call UnitMakeAbilityPermanent(u, false, 'A025')
    call UnitRemoveAbility(u, 'A025')
    call UnitMakeAbilityPermanent(u, false, 'A026')
    call UnitRemoveAbility(u, 'A026')
    call UnitMakeAbilityPermanent(u, false, 'ACmi')
    call UnitRemoveAbility(u, 'ACmi')
    call UnitMakeAbilityPermanent(u, false, 'ANpi')
    call UnitRemoveAbility(u, 'ANpi')
    call UnitMakeAbilityPermanent(u, false, 'A037')
    call UnitRemoveAbility(u, 'A037')'''
    assert target_clear in content, "Target clear not found"
    content = content.replace(target_clear, repl_clear, 1)
    print("3. Wild_ClearMorphAbil updated.")

    # 4. Add helper functions right before Wild_DoMorph:
    #    Wild_UpdateHeroSoulBonus, Wild_UpdateSoulTooltip, Wild_GetTier10TraitLabel
    helpers = '''function Wild_UpdateHeroSoulBonus takes integer pId returns nothing
    local unit u = null
    local integer stacks = 0
    local integer targetHP = 0
    local integer targetDmg = 0
    local integer diffHP = 0
    local integer diffDmg = 0
    local real curLife = 0.0
    local real maxHP = 0.0

    if pId < 0 or pId > 15 then
        return
    endif
    set u = udg_Wild_Hero[pId]
    if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
        return
    endif

    set stacks = udg_Wild_SoulStacks[pId]
    if udg_Wild_WrathTimer[pId] > 0.0 then
        // 100% Resonance during Wrath of the Wild
        set targetHP = stacks * 4
        set targetDmg = stacks / 2
    else
        // 50% Passive Resonance in normal state
        set targetHP = stacks * 2
        set targetDmg = stacks / 4
    endif

    set diffHP = targetHP - udg_Wild_HeroSoulHP[pId]
    set diffDmg = targetDmg - udg_Wild_HeroSoulDmg[pId]

    set udg_Wild_HeroSoulHP[pId] = targetHP
    set udg_Wild_HeroSoulDmg[pId] = targetDmg

    if diffHP != 0 then
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + diffHP)
        set curLife = GetWidgetLife(u)
        set maxHP = I2R(BlzGetUnitMaxHP(u))
        if diffHP > 0 then
            call SetWidgetLife(u, curLife + I2R(diffHP))
        elseif curLife > maxHP then
            call SetWidgetLife(u, maxHP)
        endif
    endif

    if diffDmg != 0 then
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + diffDmg, 0)
    endif
endfunction

function Wild_UpdateSoulTooltip takes integer pId returns nothing
    local integer stacks = 0
    local integer hCount = 0
    local integer uCount = 0
    local integer armyHP = 0
    local integer armyDmg = 0
    local integer heroHP = 0
    local integer heroDmg = 0
    local string titleD = ""
    local string tipD = ""
    local string tipR = ""
    local string tipBuff = ""

    if pId < 0 or pId > 15 then
        return
    endif

    set stacks = udg_Wild_SoulStacks[pId]
    set hCount = udg_Wild_HeroThrallCount[pId]
    set uCount = udg_Wild_CreepThrallCount[pId]
    set armyHP = stacks * 4
    set armyDmg = stacks / 2
    set heroHP = udg_Wild_HeroSoulHP[pId]
    set heroDmg = udg_Wild_HeroSoulDmg[pId]

    set titleD = "众野之怒 (D) [魂:" + I2S(stacks) + "层 | 英雄:" + I2S(hCount) + "/8 | 巨怪:" + I2S(uCount) + "/12]"
    set tipD = "召唤百鬼大军与奴役的伥鬼向敌方发起疯狂冲锋，持续 90 秒。狂暴冲锋阶数随英雄等级进阶。|n|n|cff00ff00【当前百鬼军魂状态】|r|n- 累计军魂：|cffffcc00" + I2S(stacks) + " 层|r|n- 军团全员加成：|cffffcc00+" + I2S(armyHP) + " 生命 / +" + I2S(armyDmg) + " 攻击|r|n- 英雄常驻共鸣(50%)：|cff00ccff+" + I2S(stacks * 2) + " 生命 / +" + I2S(stacks / 4) + " 攻击|r (大招期间翻倍为100%)|n- 奴役伪英雄：|cffff00ff" + I2S(hCount) + " / 8 位|r|n- 奴役精锐野怪：|cff00ff88" + I2S(uCount) + " / 12 头|r"
    set tipR = "返璞归真 (R)|n解除当前变身形态，回归万灵之躯。|n|n|cff00ff00【百鬼军魂共鸣】|r|n- 军魂层数：|cffffcc00" + I2S(stacks) + " 层|r|n- 英雄生命加成：|cff00ccff+" + I2S(heroHP) + "|r|n- 英雄攻击加成：|cffff6600+" + I2S(heroDmg) + "|r"
    set tipBuff = "百鬼军魂 (被动)|n万灵化身吸收战死亡魂凝聚军魂力量。|n|n|cff00ff00【共鸣收益】|r|n- 军魂层数：|cffffcc00" + I2S(stacks) + " 层|r|n- 当前英雄生命加成：|cff00ccff+" + I2S(heroHP) + "|r|n- 当前英雄攻击加成：|cffff6600+" + I2S(heroDmg) + "|r|n- 大招全员加成：|cffffcc00+" + I2S(armyHP) + " 生命 / +" + I2S(armyDmg) + " 攻击|r|n- 奴役亡魂：|cffff00ff" + I2S(hCount) + "/8 英雄|r | |cff00ff88" + I2S(uCount) + "/12 巨怪|r"

    if GetLocalPlayer() == Player(pId) then
        call BlzSetAbilityTooltip('A035', titleD, 0)
        call BlzSetAbilityExtendedTooltip('A035', tipD, 0)
        call BlzSetAbilityExtendedTooltip('A034', tipR, 0)
        call BlzSetAbilityExtendedTooltip('A036', tipBuff, 0)
    endif
endfunction

function Wild_GetTier10TraitLabel takes integer cat, integer subIdx returns string
    if cat == 1 then
        if subIdx == 1 then
            return "魔免+尖刺反伤+投石"
        elseif subIdx == 2 then
            return "魔免+献祭+践踏"
        elseif subIdx == 3 then
            return "剧毒+战吼+暴击"
        endif
    elseif cat == 2 then
        if subIdx == 1 then
            return "飞行+魔免+巨龙吞噬+霜冻新星"
        elseif subIdx == 2 then
            return "飞行+魔免+巨龙吞噬+极寒吐息"
        elseif subIdx == 3 then
            return "飞行+魔免+巨龙吞噬+狂暴冲击"
        endif
    elseif cat == 3 then
        if subIdx == 1 then
            return "魔免+妖术+献祭+叉状闪电"
        elseif subIdx == 2 then
            return "飞行+魔免+巨龙吞噬+心灵之火"
        elseif subIdx == 3 then
            return "飞行+魔免+巨龙吞噬+闪电护盾"
        endif
    endif
    return ""
endfunction

'''
    target_morph_func = 'function Wild_DoMorph takes unit u, integer cat, integer tierLv, integer subIdx returns nothing'
    assert target_morph_func in content, "Wild_DoMorph not found"
    content = content.replace(target_morph_func, helpers + target_morph_func, 1)
    print("4. Helper functions added before Wild_DoMorph.")

    # 5. Wild_DoMorph:
    # 5a. finalMaxHP / finalDmg calculation with udg_Wild_HeroSoulHP / udg_Wild_HeroSoulDmg
    target_stats_calc = '''    set finalMaxHP = heroOwnHP + R2I(I2R(creepHP) * mult)
    set finalDmg = heroOwnDmg + R2I(I2R(creepDmg) * mult)'''
    repl_stats_calc = '''    set finalMaxHP = heroOwnHP + R2I(I2R(creepHP) * mult) + udg_Wild_HeroSoulHP[pId]
    set finalDmg = heroOwnDmg + R2I(I2R(creepDmg) * mult) + udg_Wild_HeroSoulDmg[pId]'''
    assert target_stats_calc in content, "Target stats calc not found"
    content = content.replace(target_stats_calc, repl_stats_calc, 1)

    # 5b. Tier 10 multi-trait abilities attachment
    target_attach = '''    // Attach creep ability
    if creepAbil != 0 then
        set udg_Wild_CurrentAbil[pId] = creepAbil
        call UnitAddAbility(u, creepAbil)
        call SetUnitAbilityLevel(u, creepAbil, rank)
        call UnitMakeAbilityPermanent(u, true, creepAbil)
    endif'''
    repl_attach = '''    // Attach creep ability
    if creepAbil != 0 then
        set udg_Wild_CurrentAbil[pId] = creepAbil
        call UnitAddAbility(u, creepAbil)
        call SetUnitAbilityLevel(u, creepAbil, rank)
        call UnitMakeAbilityPermanent(u, true, creepAbil)
    endif

    // Tier 10 Boss Multi-Trait Combinations
    if tierLv == 10 then
        if cat == 1 then
            if subIdx == 1 then
                // nggr: Throw Rock (ACtb) + Magic Immunity (ACmi) + Spiked Carapace (A025)
                call UnitAddAbility(u, 'ACmi')
                call UnitMakeAbilityPermanent(u, true, 'ACmi')
                call UnitAddAbility(u, 'A025')
                call SetUnitAbilityLevel(u, 'A025', rank)
                call UnitMakeAbilityPermanent(u, true, 'A025')
            elseif subIdx == 2 then
                // ninf: War Stomp (ACst) + Magic Immunity (ACmi) + Immolation (ANpi)
                call UnitAddAbility(u, 'ACmi')
                call UnitMakeAbilityPermanent(u, true, 'ACmi')
                call UnitAddAbility(u, 'ANpi')
                call SetUnitAbilityLevel(u, 'ANpi', rank)
                call UnitMakeAbilityPermanent(u, true, 'ANpi')
            elseif subIdx == 3 then
                // nhyd: Poison (A026) + Roar (ACro) + Critical Strike (ACct)
                call UnitAddAbility(u, 'ACro')
                call SetUnitAbilityLevel(u, 'ACro', rank)
                call UnitMakeAbilityPermanent(u, true, 'ACro')
                call UnitAddAbility(u, 'ACct')
                call SetUnitAbilityLevel(u, 'ACct', rank)
                call UnitMakeAbilityPermanent(u, true, 'ACct')
            endif
        elseif cat == 2 then
            // Adult Dragons: Flight + Magic Immunity (ACmi) + Dragon Devour (A037)
            call UnitAddAbility(u, 'ACmi')
            call UnitMakeAbilityPermanent(u, true, 'ACmi')
            call UnitAddAbility(u, 'A037')
            call SetUnitAbilityLevel(u, 'A037', rank)
            call UnitMakeAbilityPermanent(u, true, 'A037')
        elseif cat == 3 then
            if subIdx == 1 then
                // nerw: Hex (AChx) + Magic Immunity (ACmi) + Immolation (ANpi) + Forked Lightning (ACfl)
                call UnitAddAbility(u, 'ACmi')
                call UnitMakeAbilityPermanent(u, true, 'ACmi')
                call UnitAddAbility(u, 'ANpi')
                call SetUnitAbilityLevel(u, 'ANpi', rank)
                call UnitMakeAbilityPermanent(u, true, 'ANpi')
                call UnitAddAbility(u, 'ACfl')
                call SetUnitAbilityLevel(u, 'ACfl', rank)
                call UnitMakeAbilityPermanent(u, true, 'ACfl')
            else
                // Adult Dragons (nrwm / nbzw): Flight + Magic Immunity (ACmi) + Dragon Devour (A037)
                call UnitAddAbility(u, 'ACmi')
                call UnitMakeAbilityPermanent(u, true, 'ACmi')
                call UnitAddAbility(u, 'A037')
                call SetUnitAbilityLevel(u, 'A037', rank)
                call UnitMakeAbilityPermanent(u, true, 'A037')
            endif
        endif
    endif'''
    assert target_attach in content, "Target attach not found"
    content = content.replace(target_attach, repl_attach, 1)

    # 5c. State tracking in Wild_DoMorph: record udg_Wild_CurrentSubIdx[pId]
    target_state = '''    set udg_Wild_CurrentFormLevel[pId] = tierLv
    set udg_Wild_MorphCD[pId] = cd'''
    repl_state = '''    set udg_Wild_CurrentFormLevel[pId] = tierLv
    set udg_Wild_CurrentSubIdx[pId] = subIdx
    set udg_Wild_MorphCD[pId] = cd'''
    assert target_state in content, "Target state not found"
    content = content.replace(target_state, repl_state, 1)
    print("5. Wild_DoMorph updated with soul resonance and Tier 10 multi-traits.")

    # 6. Wild_RevertToAvatar:
    # 6a. Reset udg_Wild_CurrentSubIdx[pId] = 0
    target_revert_state = '''    set udg_Wild_CurrentFormLevel[pId] = 0'''
    repl_revert_state = '''    set udg_Wild_CurrentFormLevel[pId] = 0
    set udg_Wild_CurrentSubIdx[pId] = 0'''
    assert target_revert_state in content, "Target revert state not found"
    content = content.replace(target_revert_state, repl_revert_state, 1)

    # 6b. Add udg_Wild_HeroSoulHP and udg_Wild_HeroSoulDmg to avatar base stats
    target_revert_stats = '''        set baseMaxHP = 550 + heroStr * 22 + hLv * 45
        set baseMaxMana = 250 + heroInt * 15 + hLv * 25
        set baseDmg = 24 + R2I(I2R(heroStr + heroAgi + heroInt) * 0.65)'''
    repl_revert_stats = '''        set baseMaxHP = 550 + heroStr * 22 + hLv * 45 + udg_Wild_HeroSoulHP[pId]
        set baseMaxMana = 250 + heroInt * 15 + hLv * 25
        set baseDmg = 24 + R2I(I2R(heroStr + heroAgi + heroInt) * 0.65) + udg_Wild_HeroSoulDmg[pId]'''
    assert target_revert_stats in content, "Target revert stats not found"
    content = content.replace(target_revert_stats, repl_revert_stats, 1)
    print("6. Wild_RevertToAvatar updated with soul resonance stats.")

    # 7. Wild_InitHero: ensure A036 is added, call Wild_UpdateHeroSoulBonus and Wild_UpdateSoulTooltip
    target_inithero = '''function Wild_InitHero takes unit h returns nothing
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
    repl_inithero = '''function Wild_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(h))
    set udg_Wild_Hero[pId] = h
    if GetUnitAbilityLevel(h, 'A034') == 0 then
        call UnitAddAbility(h, 'A034')
    endif
    if GetUnitAbilityLevel(h, 'A036') == 0 then
        call UnitAddAbility(h, 'A036')
    endif
    call Wild_UpdateHeroSoulBonus(pId)
    call Wild_UpdateSoulTooltip(pId)
    if udg_Wild_IsMorphed[pId] then
        call Wild_RevertToAvatar(h)
    else
        call Wild_ClearMorphAbil(h, pId)
    endif
endfunction'''
    assert target_inithero in content, "Wild_InitHero target not found"
    content = content.replace(target_inithero, repl_inithero, 1)
    print("7. Wild_InitHero updated.")

    # 8. Wild_ShowSubDialog: Display Tier 10 multi-trait label
    pattern_subdialog_btn = r'set btnText = "\[" \+ I2S\(subIdx\) \+ "\] " \+ tplName \+ " \(HP:\+" \+ I2S\(bonusHP\) \+ " .*?\+ I2S\(bonusDmg\) \+ " \| .*?:" \+ abilName \+ "\)"'
    repl_subdialog_btn = '''        if tierLv == 10 then
            set btnText = "[" + I2S(subIdx) + "] " + tplName + " (HP:+" + I2S(bonusHP) + " 攻:+" + I2S(bonusDmg) + " | " + Wild_GetTier10TraitLabel(cat, subIdx) + ")"
        else
            set btnText = "[" + I2S(subIdx) + "] " + tplName + " (HP:+" + I2S(bonusHP) + " 攻:+" + I2S(bonusDmg) + " | 技:" + abilName + ")"
        endif'''
    content, count = re.subn(pattern_subdialog_btn, repl_subdialog_btn, content)
    assert count == 1, f"Wild_ShowSubDialog btnText match count: {count}"
    print("8. Wild_ShowSubDialog button formatting updated.")

    # 9. Wild_AddSoulStack: update hero soul bonus and live tooltips
    target_addsoul = '''    call GroupClear(udg_EnumGroup)
    call GroupAddGroup(udg_Wild_ArmyGroup, udg_EnumGroup)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if GetOwningPlayer(enumU) == Player(pId) and not IsUnitType(enumU, UNIT_TYPE_DEAD) then
            call BlzSetUnitMaxHP(enumU, BlzGetUnitMaxHP(enumU) + 4)
            call SetWidgetLife(enumU, GetWidgetLife(enumU) + 4.0)
            if isEven then
                call BlzSetUnitBaseDamage(enumU, BlzGetUnitBaseDamage(enumU, 0) + 1, 0)
            endif
        endif
    endloop
    set enumU = null
endfunction'''
    repl_addsoul = '''    call GroupClear(udg_EnumGroup)
    call GroupAddGroup(udg_Wild_ArmyGroup, udg_EnumGroup)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if GetOwningPlayer(enumU) == Player(pId) and not IsUnitType(enumU, UNIT_TYPE_DEAD) then
            call BlzSetUnitMaxHP(enumU, BlzGetUnitMaxHP(enumU) + 4)
            call SetWidgetLife(enumU, GetWidgetLife(enumU) + 4.0)
            if isEven then
                call BlzSetUnitBaseDamage(enumU, BlzGetUnitBaseDamage(enumU, 0) + 1, 0)
            endif
        endif
    endloop
    set enumU = null

    // Real-time soul resonance bonus for hero and UI tooltips
    call Wild_UpdateHeroSoulBonus(pId)
    call Wild_UpdateSoulTooltip(pId)
endfunction'''
    assert target_addsoul in content, "Wild_AddSoulStack target not found"
    content = content.replace(target_addsoul, repl_addsoul, 1)
    print("9. Wild_AddSoulStack updated.")

    # 10. Wild_EnslaveHero & Creep thralls: call Wild_UpdateSoulTooltip(pId)
    pattern_enslave = r'(function Wild_EnslaveHero takes integer pId, unit deadHero returns nothing.*?\n)(endfunction)'
    content, count = re.subn(pattern_enslave, r'\1    call Wild_UpdateSoulTooltip(pId)\n\2', content, flags=re.DOTALL)
    assert count == 1, f"Wild_EnslaveHero match count: {count}"

    pattern_creep_thrall = r'(function Wild_EnslaveCreep takes integer pId, unit deadCreep returns nothing.*?\n)(endfunction)'
    content, count = re.subn(pattern_creep_thrall, r'\1    call Wild_UpdateSoulTooltip(pId)\n\2', content, flags=re.DOTALL)
    assert count == 1, f"Wild_EnslaveCreep match count: {count}"
    print("10. Thrall capture tooltips updated.")

    # 11. Wild_CastWrath: scale rank & cd by hero level, call Wild_UpdateHeroSoulBonus/Tooltip
    pattern_wrath_header = r'function Wild_CastWrath takes unit caster returns nothing\n.*?\n    set udg_Wild_WrathTimer\[pId\] = 90\.0'
    repl_wrath_header = '''function Wild_CastWrath takes unit caster returns nothing
    local player p = null
    local integer pId = 0
    local integer dRank = 1
    local integer hLv = 1
    local real cd = 110.0
    local real cx = 0.0
    local real cy = 0.0
    local unit c = null
    local unit thrall = null
    local integer s = 0
    local integer idx = 0
    local integer finalHP = 0
    local integer finalDmg = 0
    local integer itId = 0
    local item it = null
    local integer i = 0
    local integer cIdx = 0
    local integer tType = 0
    local integer bonusHP = 0
    local integer bonusDmg = 0

    if caster == null or IsUnitType(caster, UNIT_TYPE_DEAD) then
        return
    endif
    set p = GetOwningPlayer(caster)
    set pId = GetPlayerId(p)
    set hLv = GetHeroLevel(caster)

    // Dynamic Rank & CD scaling based on Hero Level
    if hLv < 8 then
        set dRank = 1
        set cd = 110.0
    elseif hLv < 10 then
        set dRank = 2
        set cd = 100.0
    else
        set dRank = 3
        set cd = 90.0
    endif
    call BlzStartUnitAbilityCooldown(caster, 'A035', cd)

    set cx = GetUnitX(caster)
    set cy = GetUnitY(caster)

    set udg_Wild_WrathTimer[pId] = 90.0
    call Wild_UpdateHeroSoulBonus(pId)
    call Wild_UpdateSoulTooltip(pId)'''
    content, count = re.subn(pattern_wrath_header, lambda m: repl_wrath_header, content, flags=re.DOTALL)
    assert count == 1, f"Wild_CastWrath header match count: {count}"
    print("11. Wild_CastWrath updated.")

    # 12. Dragon Devour implementation: Wild_CastDragonDevour
    devour_func = '''function Wild_CastDragonDevour takes unit caster, unit target returns nothing
    local player p = null
    local integer pId = 0
    local integer aLv = 1
    local real maxHP = 0.0
    local real heal = 0.0
    local real curLife = 0.0

    if caster == null or target == null then
        return
    endif
    if IsUnitType(caster, UNIT_TYPE_DEAD) or IsUnitType(target, UNIT_TYPE_DEAD) then
        return
    endif
    set p = GetOwningPlayer(caster)
    set pId = GetPlayerId(p)

    if not IsUnitEnemy(target, p) then
        return
    endif
    if IsUnitType(target, UNIT_TYPE_HERO) or IsUnitType(target, UNIT_TYPE_STRUCTURE) or GetUnitTypeId(target) == 'u000' then
        return
    endif

    set aLv = GetUnitAbilityLevel(caster, 'A037')
    if aLv < 1 then
        set aLv = 1
    endif
    // Heal: 25% (Lv 1) / 35% (Lv 2) / 45% (Lv 3) Max HP
    set maxHP = I2R(BlzGetUnitMaxHP(caster))
    set heal = maxHP * (0.15 + I2R(aLv) * 0.10)
    set curLife = GetWidgetLife(caster)
    if curLife + heal > maxHP then
        call SetWidgetLife(caster, maxHP)
    else
        call SetWidgetLife(caster, curLife + heal)
    endif

    // Visual FX
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\DeathPact\\\\DeathPactTarget.mdl", caster, "origin"))
    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Other\\\\Incinerate\\\\IncinerateBuff.mdl", GetUnitX(target), GetUnitY(target)))

    // Instant kill
    call SetUnitExploded(target, true)
    call KillUnit(target)

    // Soul stack gain & status update
    call Wild_AddSoulStack(pId)

    if GetPlayerController(p) == MAP_CONTROL_USER then
        call DisplayTimedTextToPlayer(p, 0, 0, 3.0, "|cffffcc00[巨龙吞噬]|r 吞噬了目标，恢复生命并获得 1 层百鬼军魂！")
    endif
    set p = null
endfunction

'''
    target_before_dm = 'function DM_CloneOneUnit takes unit caster, unit orig, real tx, real ty returns nothing'
    assert target_before_dm in content, "DM_CloneOneUnit not found"
    content = content.replace(target_before_dm, devour_func + target_before_dm, 1)
    print("12. Wild_CastDragonDevour added.")

    # 13. AI_LearnSkillForWild: A035 1 level only
    pattern_ai_learn = r'// 1\. Ultimate D \(A035[^\n]*\n.*?if hLv >= 6 and dLv < 1 then\n\s+return AI_ForceLearnSkill\(h, \'A035\', 3, false\)\n\s+endif'
    repl_ai_learn = '''    // 1. Ultimate D (A035 众野之怒) at Lv 6 (1-level skill)
    if hLv >= 6 and dLv < 1 then
        return AI_ForceLearnSkill(h, 'A035', 1, false)
    endif'''
    content, count = re.subn(pattern_ai_learn, repl_ai_learn, content, flags=re.DOTALL)
    assert count == 1, f"AI_LearnSkillForWild match count: {count}"
    print("13. AI_LearnSkillForWild updated.")

    # 14. Wrath Duration countdown timer loop: update soul bonus and tooltip when timer reaches 0
    target_timer_loop = '''    // 3.9. Process Wild Wrath Duration Countdown
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Wild_WrathTimer[pId] > 0.0 then
            set udg_Wild_WrathTimer[pId] = udg_Wild_WrathTimer[pId] - 1.0
        endif
        set pId = pId + 1
    endloop'''
    repl_timer_loop = '''    // 3.9. Process Wild Wrath Duration Countdown
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Wild_WrathTimer[pId] > 0.0 then
            set udg_Wild_WrathTimer[pId] = udg_Wild_WrathTimer[pId] - 1.0
            if udg_Wild_WrathTimer[pId] <= 0.0 then
                set udg_Wild_WrathTimer[pId] = 0.0
                call Wild_UpdateHeroSoulBonus(pId)
                call Wild_UpdateSoulTooltip(pId)
            endif
        endif
        set pId = pId + 1
    endloop'''
    assert target_timer_loop in content, "Timer loop target not found"
    content = content.replace(target_timer_loop, repl_timer_loop, 1)
    print("14. Duration countdown timer loop updated.")

    # 15. DM_OnSpellEffect: hook A037
    target_spell_effect = '''    elseif abil == 'A035' then
        call Wild_CastWrath(caster)
    endif'''
    repl_spell_effect = '''    elseif abil == 'A035' then
        call Wild_CastWrath(caster)
    elseif abil == 'A037' then
        call Wild_CastDragonDevour(caster, GetSpellTargetUnit())
    endif'''
    assert target_spell_effect in content, "Spell effect target not found"
    content = content.replace(target_spell_effect, repl_spell_effect, 1)
    print("15. DM_OnSpellEffect hooked A037.")

    # 16. Test Mode Command: update soul bonus & tooltip on reset
    target_test_mode = '''        if GetUnitAbilityLevel(udg_Wild_Hero[pId], 'A035') == 0 then
            call UnitAddAbility(udg_Wild_Hero[pId], 'A035')
        endif'''
    repl_test_mode = '''        if GetUnitAbilityLevel(udg_Wild_Hero[pId], 'A035') == 0 then
            call UnitAddAbility(udg_Wild_Hero[pId], 'A035')
        endif
        call Wild_UpdateHeroSoulBonus(pId)
        call Wild_UpdateSoulTooltip(pId)'''
    assert target_test_mode in content, "Test mode target not found"
    content = content.replace(target_test_mode, repl_test_mode, 1)
    print("16. Test mode command updated.")

    with open(jass_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"All 16 steps applied successfully! New length: {len(content)}")

if __name__ == '__main__':
    main()
