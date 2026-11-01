# -*- coding: utf-8 -*-
import os

path = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Ninja_SpawnClone
old_spawn = """function Ninja_SpawnClone takes player p, real x, real y, real facing returns unit
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
endfunction"""

new_spawn = """function Ninja_SpawnClone takes player p, real x, real y, real facing returns unit
    local integer pId = GetPlayerId(p)
    local unit trueHero = Ninja_GetTrueHero(p)
    local real dur = 120.0
    local integer lv = 0
    local unit clone = null
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

    set clone = CreateUnit(p, 'u002', x, y, facing)
    call UnitAddType(clone, UNIT_TYPE_SUMMONED)

    if trueHero != null then
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
endfunction"""

# Normalize \r\n to \n for replacement
has_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')
old_spawn_lf = old_spawn.replace('\r\n', '\n')
new_spawn_lf = new_spawn.replace('\r\n', '\n')

assert old_spawn_lf in content_lf, "old_spawn not found in war3map.j!"
content_lf = content_lf.replace(old_spawn_lf, new_spawn_lf, 1)

# 2. In DM_OnUnitDeath:
# Section 2: 他化自在
old_death_s2 = """    // 2. 他化自在 (A013) - 击杀魔音忍者者被烙印因果
    if deadType == 'H003' and killer != null and IsUnitEnemy(killer, deadOwner) then"""

new_death_s2 = """    // 2. 他化自在 (A013) - 击杀魔音忍者者被烙印因果
    if (deadType == 'H003' or deadType == 'u002') and killer != null and IsUnitEnemy(killer, deadOwner) then"""

assert old_death_s2 in content_lf, "old_death_s2 not found!"
content_lf = content_lf.replace(old_death_s2, new_death_s2, 1)

# Section 4: 魔音同化
old_death_s4 = """    // 4. 魔音同化 (A011) - 击杀单位生成伪英雄分身
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and deadType != 'u000' and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u001') then"""

new_death_s4 = """    // 4. 魔音同化 (A011) - 击杀单位生成伪英雄分身
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'H003' and not isFakeHero and not isIllusion and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u002' or GetUnitTypeId(killer) == 'u001') then"""

assert old_death_s4 in content_lf, "old_death_s4 not found!"
content_lf = content_lf.replace(old_death_s4, new_death_s4, 1)

# Section 6: Cleanup Fake Hero / Clone
old_death_s6 = """    // 6. Cleanup Fake Hero / Clone
    if isFakeHero then"""

new_death_s6 = """    // 6. Cleanup Fake Hero / Clone
    if isFakeHero or deadType == 'u002' then"""

assert old_death_s6 in content_lf, "old_death_s6 not found!"
content_lf = content_lf.replace(old_death_s6, new_death_s6, 1)

# Restore CRLF if needed
if has_crlf:
    out_content = content_lf.replace('\n', '\r\n')
else:
    out_content = content_lf

with open(path, 'w', encoding='utf-8') as f:
    f.write(out_content)

print("Successfully patched payload/war3map.j for v1.6!")
