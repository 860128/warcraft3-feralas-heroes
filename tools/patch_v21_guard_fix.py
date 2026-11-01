import os

war3map_j_path = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j'

with open(war3map_j_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update globals
old_globals = """    // AI Strategic Army Commander Globals
    integer udg_AI_CommandTick = 0
    real udg_AI_TargetX = 0.0
    real udg_AI_TargetY = 0.0
    boolean udg_AI_TargetFound = false
    integer udg_AI_CombatCount = 0
    group udg_AI_ArmyGroup = null
    group udg_AI_CombatGroup = null
endglobals"""

new_globals = """    // AI Strategic Army Commander Globals
    integer udg_AI_CommandTick = 0
    real udg_AI_TargetX = 0.0
    real udg_AI_TargetY = 0.0
    boolean udg_AI_TargetFound = false
    boolean udg_AI_TargetChanged = false
    integer udg_AI_CombatCount = 0
    group udg_AI_ArmyGroup = null
    group udg_AI_CombatGroup = null
    unit array udg_AI_LockedTarget
endglobals"""

assert old_globals in content, "Failed to find old_globals"
content = content.replace(old_globals, new_globals, 1)

# 2. Update Ninja_SpawnClone with RemoveGuardPosition
old_ninja_clone = """    set clone = CreateUnit(p, 'u002', x, y, facing)
    call UnitAddType(clone, UNIT_TYPE_SUMMONED)"""

new_ninja_clone = """    set clone = CreateUnit(p, 'u002', x, y, facing)
    call RemoveGuardPosition(clone)
    call UnitAddType(clone, UNIT_TYPE_SUMMONED)"""

assert old_ninja_clone in content, "Failed to find old_ninja_clone"
content = content.replace(old_ninja_clone, new_ninja_clone, 1)

# 3. Update AI_SpawnCustomHeroForPlayer with RemoveGuardPosition
old_ai_spawn_hero = """    set h = CreateUnit(Player(pId), hTypeId, x, y, facing)
    set udg_AI_CustomHero[pId] = h"""

new_ai_spawn_hero = """    set h = CreateUnit(Player(pId), hTypeId, x, y, facing)
    call RemoveGuardPosition(h)
    set udg_AI_CustomHero[pId] = h"""

assert old_ai_spawn_hero in content, "Failed to find old_ai_spawn_hero"
content = content.replace(old_ai_spawn_hero, new_ai_spawn_hero, 1)

# 4. Update DM_CloneOneUnit with RemoveGuardPosition in both places
old_dm_clone1 = """            set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
            call UnitRemoveType(clone, UNIT_TYPE_HERO)"""

new_dm_clone1 = """            set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
            call RemoveGuardPosition(clone)
            call UnitRemoveType(clone, UNIT_TYPE_HERO)"""

assert old_dm_clone1 in content, "Failed to find old_dm_clone1"
content = content.replace(old_dm_clone1, new_dm_clone1, 1)

old_dm_clone2 = """        set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
        call UnitAddType(clone, UNIT_TYPE_SUMMONED)"""

new_dm_clone2 = """        set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
        call RemoveGuardPosition(clone)
        call UnitAddType(clone, UNIT_TYPE_SUMMONED)"""

assert old_dm_clone2 in content, "Failed to find old_dm_clone2"
content = content.replace(old_dm_clone2, new_dm_clone2, 1)

# 5. Update AI_FindStrategicTarget and AI_CommandArmyForPlayer
start_marker = "function AI_FindStrategicTarget takes integer pId, real hx, real hy returns nothing"
end_marker = "function AI_TacticalLoop takes nothing returns nothing"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)
assert start_idx != -1 and end_idx != -1, "Failed to find strategic target block"

new_strategic_block = """function AI_FindStrategicTarget takes integer pId, real hx, real hy returns nothing
    local player p = Player(pId)
    local unit h = udg_AI_CustomHero[pId]
    local integer hLv = 0
    local unit enumU = null
    local unit bestCreep = null
    local real minCreepD = 999999999.0
    local unit bestPlayerEnemy = null
    local real minPlayerD = 999999999.0
    local unit bestAnyEnemy = null
    local real minAnyD = 999999999.0
    local unit targetU = null
    local real dx = 0.0
    local real dy = 0.0
    local real d = 0.0
    local integer ownerId = 0

    set udg_AI_TargetChanged = false

    if h != null and not IsUnitType(h, UNIT_TYPE_DEAD) and GetWidgetLife(h) > 0.405 then
        set hLv = GetHeroLevel(h)
    endif

    // 1. Check if existing locked target is still alive and an enemy
    if udg_AI_LockedTarget[pId] != null then
        if not IsUnitType(udg_AI_LockedTarget[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_AI_LockedTarget[pId]) > 0.405 and IsUnitEnemy(udg_AI_LockedTarget[pId], p) then
            set udg_AI_TargetFound = true
            set udg_AI_TargetX = GetUnitX(udg_AI_LockedTarget[pId])
            set udg_AI_TargetY = GetUnitY(udg_AI_LockedTarget[pId])
            set p = null
            set h = null
            return
        else
            set udg_AI_LockedTarget[pId] = null
        endif
    endif

    // 2. Target died or was null: scan map for new target
    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRect(udg_EnumGroup, bj_mapInitialPlayableArea, null)
    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)
        if IsUnitEnemy(enumU, p) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' and not IsUnitInvisible(enumU, p) then
            set dx = GetUnitX(enumU) - hx
            set dy = GetUnitY(enumU) - hy
            set d = dx * dx + dy * dy
            if d < minAnyD then
                set bestAnyEnemy = enumU
                set minAnyD = d
            endif

            set ownerId = GetPlayerId(GetOwningPlayer(enumU))
            if ownerId == PLAYER_NEUTRAL_AGGRESSIVE then
                // Creep candidate within 4500.0 range (4500^2 = 20250000.0)
                if d <= 20250000.0 and d < minCreepD then
                    set bestCreep = enumU
                    set minCreepD = d
                endif
            else
                // Living enemy player unit or building
                if d < minPlayerD then
                    set bestPlayerEnemy = enumU
                    set minPlayerD = d
                endif
            endif
        endif
    endloop

    // 3. Selection Priority:
    // Prioritize enemy player units/structures whenever combat units >= 4 OR hero level >= 2
    if (hLv >= 2 or udg_AI_CombatCount >= 4) and bestPlayerEnemy != null then
        set targetU = bestPlayerEnemy
    elseif bestCreep != null then
        set targetU = bestCreep
    elseif bestPlayerEnemy != null then
        set targetU = bestPlayerEnemy
    elseif bestAnyEnemy != null then
        set targetU = bestAnyEnemy
    endif

    if targetU != null then
        set udg_AI_LockedTarget[pId] = targetU
        set udg_AI_TargetFound = true
        set udg_AI_TargetChanged = true
        set udg_AI_TargetX = GetUnitX(targetU)
        set udg_AI_TargetY = GetUnitY(targetU)
    else
        set udg_AI_LockedTarget[pId] = null
        set udg_AI_TargetFound = false
        set udg_AI_TargetChanged = false
        set udg_AI_TargetX = 0.0
        set udg_AI_TargetY = 0.0
    endif

    set p = null
    set h = null
    set enumU = null
    set bestCreep = null
    set bestPlayerEnemy = null
    set bestAnyEnemy = null
    set targetU = null
endfunction

function AI_CommandArmyForPlayer takes integer pId returns nothing
    local player p = Player(pId)
    local unit h = udg_AI_CustomHero[pId]
    local real hx = 0.0
    local real hy = 0.0
    local unit th = null
    local unit enumU = null
    local integer ord = 0
    local integer uOrd = 0
    local real ux = 0.0
    local real uy = 0.0
    local boolean heroAlive = false
    local boolean canOrderArmy = false

    if h != null and not IsUnitType(h, UNIT_TYPE_DEAD) and GetWidgetLife(h) > 0.405 then
        set heroAlive = true
        set hx = GetUnitX(h)
        set hy = GetUnitY(h)
    else
        set th = AI_GetPlayerTownHall(p)
        if th != null then
            set hx = GetUnitX(th)
            set hy = GetUnitY(th)
            set th = null
        else
            set hx = GetStartLocationX(GetPlayerStartLocation(p))
            set hy = GetStartLocationY(GetPlayerStartLocation(p))
        endif
    endif

    // Count combat units and populate udg_AI_CombatGroup
    call GroupClear(udg_AI_ArmyGroup)
    call GroupClear(udg_AI_CombatGroup)
    call GroupEnumUnitsOfPlayer(udg_AI_ArmyGroup, p, null)
    set udg_AI_CombatCount = 0

    loop
        set enumU = FirstOfGroup(udg_AI_ArmyGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_AI_ArmyGroup, enumU)
        if not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and not IsUnitType(enumU, UNIT_TYPE_PEON) and GetUnitTypeId(enumU) != 'u000' then
            if enumU != h then
                set udg_AI_CombatCount = udg_AI_CombatCount + 1
                call GroupAddUnit(udg_AI_CombatGroup, enumU)
            endif
        endif
    endloop

    // Find strategic target (updates udg_AI_LockedTarget and udg_AI_TargetChanged)
    call AI_FindStrategicTarget(pId, hx, hy)

    if udg_AI_TargetFound then
        // Strip all AI guard positions for computer player p
        call RemoveAllGuardPositions(p)

        // 1. Hero Order
        if heroAlive then
            call RemoveGuardPosition(h)
            set ord = GetUnitCurrentOrder(h)
            // Only if h is NOT currently casting our custom spells (852089 blizzard, 852579 charm, 852123 mirrorimage, 852594 summongrizzly)
            if not (ord == 852089 or ord == 852579 or ord == 852123 or ord == 852594) then
                // NOT fleeing at low HP (GetWidgetLife(h) > MaxLife * 0.25 or H003)
                if (GetWidgetLife(h) > GetUnitState(h, UNIT_STATE_MAX_LIFE) * 0.25 or GetUnitTypeId(h) == 'H003') then
                    // Only issue order if not fighting AND (not already attacking OR target changed)
                    if not AI_HasEnemyInRange(p, hx, hy, 650.0) then
                        if ord != 851983 or udg_AI_TargetChanged then
                            call IssuePointOrder(h, "attack", udg_AI_TargetX, udg_AI_TargetY)
                        endif
                    endif
                endif
            endif
        endif

        // 2. Combat Army & Clones Order
        // Whenever the computer has >= 3 combat units (or h is alive and marching)
        set canOrderArmy = (udg_AI_CombatCount >= 3) or heroAlive
        if canOrderArmy then
            loop
                set enumU = FirstOfGroup(udg_AI_CombatGroup)
                exitwhen enumU == null
                call GroupRemoveUnit(udg_AI_CombatGroup, enumU)
                call RemoveGuardPosition(enumU)
                set uOrd = GetUnitCurrentOrder(enumU)
                // Exclude lumber harvesters (e.g. ghouls: 852018 harvest, 852020 returnresources)
                if uOrd != 852018 and uOrd != 852020 then
                    set ux = GetUnitX(enumU)
                    set uy = GetUnitY(enumU)
                    // Only issue order if not in active combat
                    if not AI_HasEnemyInRange(p, ux, uy, 650.0) then
                        if uOrd != 851983 or udg_AI_TargetChanged then
                            call IssuePointOrder(enumU, "attack", udg_AI_TargetX, udg_AI_TargetY)
                        endif
                    endif
                endif
            endloop
        endif
    endif

    call GroupClear(udg_AI_CombatGroup)
    set p = null
    set h = null
    set enumU = null
endfunction

"""

content = content[:start_idx] + new_strategic_block + content[end_idx:]

# 6. Update AI_OnUnitTrainFinish to call RemoveGuardPosition(trained)
old_train_finish = """        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            if GetUnitTypeId(trained) == 'H003' then"""

new_train_finish = """        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[pId] > 0 and not IsUnitType(trained, UNIT_TYPE_PEON) then
                call RemoveGuardPosition(trained)
            endif
            if GetUnitTypeId(trained) == 'H003' then"""

assert old_train_finish in content, "Failed to find old_train_finish"
content = content.replace(old_train_finish, new_train_finish, 1)

# 7. Update DM_InitTriggers loop to initialize udg_AI_LockedTarget[i] = null
old_init_loop = """        // Initialize AI variables
        set udg_AI_HeroMode[i] = 0
        set udg_AI_CustomHero[i] = null"""

new_init_loop = """        // Initialize AI variables
        set udg_AI_HeroMode[i] = 0
        set udg_AI_CustomHero[i] = null
        set udg_AI_LockedTarget[i] = null"""

assert old_init_loop in content, "Failed to find old_init_loop"
content = content.replace(old_init_loop, new_init_loop, 1)

with open(war3map_j_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied v2.1 AI guard position & target locking patch!")
