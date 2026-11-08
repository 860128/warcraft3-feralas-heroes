# -*- coding: utf-8 -*-
import sys
import os

def main():
    jass_path = 'payload/war3map.j'
    with open(jass_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original content length: {len(content)}")

    # 1. Globals declaration: Add udg_Wild_TargetX, udg_Wild_TargetY, udg_Wild_TargetFound
    target_globals = '''    group udg_Wild_ArmyGroup = null
    timer udg_Wild_ArmyTimer = null'''
    repl_globals = '''    group udg_Wild_ArmyGroup = null
    timer udg_Wild_ArmyTimer = null
    real udg_Wild_TargetX = 0.0
    real udg_Wild_TargetY = 0.0
    boolean udg_Wild_TargetFound = false'''
    assert target_globals in content, "target_globals not found"
    content = content.replace(target_globals, repl_globals, 1)
    print("1. Globals declared.")

    # 2. Wild_SpawnArmyCreep: RemoveGuardPosition on newly created unit
    target_spawn_full = '''function Wild_SpawnArmyCreep takes player p, integer unitTypeId, real x, real y, integer bonusHP, integer bonusDmg returns unit
    local unit u = CreateUnit(p, unitTypeId, x, y, 0.0)
    local integer maxHP = 0
    local integer baseDmg = 0'''
    repl_spawn_full = '''function Wild_SpawnArmyCreep takes player p, integer unitTypeId, real x, real y, integer bonusHP, integer bonusDmg returns unit
    local unit u = CreateUnit(p, unitTypeId, x, y, 0.0)
    local integer maxHP = 0
    local integer baseDmg = 0
    call RemoveGuardPosition(u)'''
    assert target_spawn_full in content, "target_spawn_full not found"
    content = content.replace(target_spawn_full, repl_spawn_full, 1)
    print("2. Wild_SpawnArmyCreep RemoveGuardPosition added.")

    # 3. Replace Wild_GetTargetBaseX and Wild_GetTargetBaseY with Refuge_IsInvulnerable + AI_HasEnemyInRange + Wild_FindArmyTarget
    target_bases = '''function Wild_GetTargetBaseX takes player p returns real
    local integer pId = GetPlayerId(p)
    local integer targetId = 0
    if pId >= 0 and pId <= 3 then
        set targetId = 4
    else
        set targetId = 0
    endif
    return GetStartLocationX(targetId)
endfunction

function Wild_GetTargetBaseY takes player p returns real
    local integer pId = GetPlayerId(p)
    local integer targetId = 0
    if pId >= 0 and pId <= 3 then
        set targetId = 4
    else
        set targetId = 0
    endif
    return GetStartLocationY(targetId)
endfunction'''
    repl_bases = '''function Refuge_IsInvulnerable takes unit u returns boolean
    if u == null then
        return false
    endif
    return GetUnitAbilityLevel(u, 'Avul') > 0 or BlzIsUnitInvulnerable(u) or GetUnitTypeId(u) == 'n003'
endfunction

function AI_HasEnemyInRange takes player p, real x, real y, real radius returns boolean
    local unit enumU = null
    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRange(udg_EnumGroup, x, y, radius, null)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if IsUnitEnemy(enumU, p) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' and not IsUnitInvisible(enumU, p) and not Refuge_IsInvulnerable(enumU) then
            call GroupClear(udg_EnumGroup)
            set enumU = null
            return true
        endif
    endloop
    set enumU = null
    return false
endfunction

function Wild_FindArmyTarget takes player p, real fromX, real fromY returns nothing
    local unit enumU = null
    local unit bestPlayerEnemy = null
    local real minPlayerD = 999999999.0
    local unit bestCreep = null
    local real minCreepD = 999999999.0
    local unit bestAnyEnemy = null
    local real minAnyD = 999999999.0
    local unit targetU = null
    local real dx = 0.0
    local real dy = 0.0
    local real d = 0.0
    local integer ownerId = 0

    set udg_Wild_TargetFound = false
    set udg_Wild_TargetX = 0.0
    set udg_Wild_TargetY = 0.0

    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRect(udg_EnumGroup, bj_mapInitialPlayableArea, null)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if IsUnitEnemy(enumU, p) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' and not IsUnitInvisible(enumU, p) and not Refuge_IsInvulnerable(enumU) then
            set dx = GetUnitX(enumU) - fromX
            set dy = GetUnitY(enumU) - fromY
            set d = dx * dx + dy * dy

            if d < minAnyD then
                set bestAnyEnemy = enumU
                set minAnyD = d
            endif

            set ownerId = GetPlayerId(GetOwningPlayer(enumU))
            if ownerId <= 7 then
                // Priority 1: Living enemy player unit, hero or building
                if d < minPlayerD then
                    set bestPlayerEnemy = enumU
                    set minPlayerD = d
                endif
            elseif ownerId == PLAYER_NEUTRAL_AGGRESSIVE then
                // Priority 2: Neutral aggressive creep
                if d < minCreepD then
                    set bestCreep = enumU
                    set minCreepD = d
                endif
            endif
        endif
    endloop

    if bestPlayerEnemy != null then
        set targetU = bestPlayerEnemy
    elseif bestCreep != null then
        set targetU = bestCreep
    elseif bestAnyEnemy != null then
        set targetU = bestAnyEnemy
    endif

    if targetU != null then
        set udg_Wild_TargetFound = true
        set udg_Wild_TargetX = GetUnitX(targetU)
        set udg_Wild_TargetY = GetUnitY(targetU)
    endif

    set enumU = null
    set bestPlayerEnemy = null
    set bestCreep = null
    set bestAnyEnemy = null
    set targetU = null
endfunction'''
    assert target_bases in content, "target_bases not found"
    content = content.replace(target_bases, repl_bases, 1)
    print("3. Refuge_IsInvulnerable, Wild_FindArmyTarget and early AI_HasEnemyInRange added, Wild_GetTargetBaseX/Y removed.")

    # 4. Remove original AI_HasEnemyInRange definition (which was right before AI_FindStrategicTarget)
    target_old_enemy = '''function AI_HasEnemyInRange takes player p, real x, real y, real radius returns boolean
    local unit enumU = null
    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRange(udg_EnumGroup, x, y, radius, null)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if IsUnitEnemy(enumU, p) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' and not IsUnitInvisible(enumU, p) and not Refuge_IsInvulnerable(enumU) then
            call GroupClear(udg_EnumGroup)
            set enumU = null
            return true
        endif
    endloop
    set enumU = null
    return false
endfunction

function AI_FindStrategicTarget takes integer pId, real hx, real hy returns nothing'''
    repl_old_enemy = '''function AI_FindStrategicTarget takes integer pId, real hx, real hy returns nothing'''
    assert target_old_enemy in content, "target_old_enemy not found"
    content = content.replace(target_old_enemy, repl_old_enemy, 1)
    print("4. Old AI_HasEnemyInRange removed from later section.")

    # 5. Remove original Refuge_IsInvulnerable definition from later section
    target_old_refuge = '''function Refuge_IsInvulnerable takes unit u returns boolean
    if u == null then
        return false
    endif
    return GetUnitAbilityLevel(u, 'Avul') > 0 or BlzIsUnitInvulnerable(u) or GetUnitTypeId(u) == 'n003'
endfunction

function Refuge_InitForPlayer takes player p returns nothing'''
    repl_old_refuge = '''function Refuge_InitForPlayer takes player p returns nothing'''
    assert target_old_refuge in content, "target_old_refuge not found"
    content = content.replace(target_old_refuge, repl_old_refuge, 1)
    print("5. Old Refuge_IsInvulnerable removed from later section.")

    # 6. Wild_CastWrath: RemoveGuardPosition on u003 hero thrall
    target_thrall_guard = '''        set thrall = CreateUnit(p, 'u003', cx + GetRandomReal(-150.0, 150.0), cy + GetRandomReal(-150.0, 150.0), 0.0)
        call UnitApplyTimedLife(thrall, 'BTLF', 90.0)'''
    repl_thrall_guard = '''        set thrall = CreateUnit(p, 'u003', cx + GetRandomReal(-150.0, 150.0), cy + GetRandomReal(-150.0, 150.0), 0.0)
        call RemoveGuardPosition(thrall)
        call UnitApplyTimedLife(thrall, 'BTLF', 90.0)'''
    assert target_thrall_guard in content, "target_thrall_guard not found"
    content = content.replace(target_thrall_guard, repl_thrall_guard, 1)
    print("6. Hero thrall RemoveGuardPosition added.")

    # 7. Wild_CastWrath: Immediate first-round push order right after all units spawned
    target_wrath_end = '''    set c = null
    set thrall = null
    set it = null
    set p = null
endfunction'''
    repl_wrath_end = '''    // Immediate first-round push order right at spawn
    call Wild_FindArmyTarget(p, cx, cy)
    if udg_Wild_TargetFound then
        call GroupClear(udg_EnumGroup)
        call GroupAddGroup(udg_Wild_ArmyGroup, udg_EnumGroup)
        loop
            set c = FirstOfGroup(udg_EnumGroup)
            exitwhen c == null
            call GroupRemoveUnit(udg_EnumGroup, c)
            if GetOwningPlayer(c) == p and not IsUnitType(c, UNIT_TYPE_DEAD) then
                call IssuePointOrder(c, "attack", udg_Wild_TargetX, udg_Wild_TargetY)
            endif
        endloop
    endif

    set c = null
    set thrall = null
    set it = null
    set p = null
endfunction'''
    assert target_wrath_end in content, "target_wrath_end not found"
    content = content.replace(target_wrath_end, repl_wrath_end, 1)
    print("7. Wild_CastWrath immediate attack order added.")

    # 8. Upgrade Wild_ArmyPushLoop: dynamic target finding + non-combat check
    target_push_loop = '''function Wild_ArmyPushLoop takes nothing returns nothing
    local unit enumU = null
    local group tempG = CreateGroup()
    local real tx = 0.0
    local real ty = 0.0

    call GroupAddGroup(udg_Wild_ArmyGroup, tempG)
    loop
        set enumU = FirstOfGroup(tempG)
        exitwhen enumU == null
        call GroupRemoveUnit(tempG, enumU)
        if IsUnitType(enumU, UNIT_TYPE_DEAD) or GetUnitTypeId(enumU) == 0 then
            call GroupRemoveUnit(udg_Wild_ArmyGroup, enumU)
        else
            if GetUnitCurrentOrder(enumU) == 0 then
                set tx = Wild_GetTargetBaseX(GetOwningPlayer(enumU))
                set ty = Wild_GetTargetBaseY(GetOwningPlayer(enumU))
                call IssuePointOrder(enumU, "attack", tx, ty)
            endif
        endif
    endloop
    call DestroyGroup(tempG)
    set tempG = null
endfunction'''
    repl_push_loop = '''function Wild_ArmyPushLoop takes nothing returns nothing
    local unit enumU = null
    local group tempG = CreateGroup()
    local player p = null
    local real ux = 0.0
    local real uy = 0.0

    call GroupAddGroup(udg_Wild_ArmyGroup, tempG)
    loop
        set enumU = FirstOfGroup(tempG)
        exitwhen enumU == null
        call GroupRemoveUnit(tempG, enumU)
        if IsUnitType(enumU, UNIT_TYPE_DEAD) or GetUnitTypeId(enumU) == 0 then
            call GroupRemoveUnit(udg_Wild_ArmyGroup, enumU)
        else
            call RemoveGuardPosition(enumU)
            set p = GetOwningPlayer(enumU)
            set ux = GetUnitX(enumU)
            set uy = GetUnitY(enumU)
            if not AI_HasEnemyInRange(p, ux, uy, 600.0) and GetUnitCurrentOrder(enumU) == 0 then
                call Wild_FindArmyTarget(p, ux, uy)
                if udg_Wild_TargetFound then
                    call IssuePointOrder(enumU, "attack", udg_Wild_TargetX, udg_Wild_TargetY)
                endif
            endif
        endif
    endloop
    call DestroyGroup(tempG)
    set tempG = null
    set enumU = null
    set p = null
endfunction'''
    assert target_push_loop in content, "target_push_loop not found"
    content = content.replace(target_push_loop, repl_push_loop, 1)
    print("8. Wild_ArmyPushLoop upgraded with dynamic target search and combat check.")

    with open(jass_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"All 8 v3.8 JASS modifications applied successfully! New length: {len(content)}")

if __name__ == '__main__':
    main()
