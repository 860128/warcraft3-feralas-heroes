import os

war3map_j_path = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j'

with open(war3map_j_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add globals
old_globals = """    // AI Helper Tracking Globals
    real array udg_AI_DeadTimer
    real array udg_AI_AltarTimer
    real array udg_AI_WaitTimer
    player udg_TM_PromptPlayer = null
endglobals"""

new_globals = """    // AI Helper Tracking Globals
    real array udg_AI_DeadTimer
    real array udg_AI_AltarTimer
    real array udg_AI_WaitTimer
    player udg_TM_PromptPlayer = null

    // AI Strategic Army Commander Globals
    integer udg_AI_CommandTick = 0
    real udg_AI_TargetX = 0.0
    real udg_AI_TargetY = 0.0
    boolean udg_AI_TargetFound = false
    integer udg_AI_CombatCount = 0
    group udg_AI_ArmyGroup = null
    group udg_AI_CombatGroup = null
endglobals"""

assert old_globals in content, "Failed to find old_globals target"
content = content.replace(old_globals, new_globals, 1)

# 2. Add AI_HasEnemyInRange, AI_FindStrategicTarget, AI_CommandArmyForPlayer above AI_TacticalLoop
functions_code = """function AI_HasEnemyInRange takes player p, real x, real y, real radius returns boolean
    local unit enumU = null
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

function AI_FindStrategicTarget takes integer pId, real hx, real hy returns nothing
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

    if h != null and not IsUnitType(h, UNIT_TYPE_DEAD) and GetWidgetLife(h) > 0.405 then
        set hLv = GetHeroLevel(h)
    endif

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

    if (hLv < 3 and udg_AI_CombatCount < 6) and bestCreep != null then
        set targetU = bestCreep
    elseif bestPlayerEnemy != null then
        set targetU = bestPlayerEnemy
    elseif bestCreep != null then
        set targetU = bestCreep
    elseif bestAnyEnemy != null then
        set targetU = bestAnyEnemy
    endif

    if targetU != null then
        set udg_AI_TargetFound = true
        set udg_AI_TargetX = GetUnitX(targetU)
        set udg_AI_TargetY = GetUnitY(targetU)
    else
        set udg_AI_TargetFound = false
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
    local real dx = 0.0
    local real dy = 0.0
    local real distSq = 0.0
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

    // Find strategic target
    call AI_FindStrategicTarget(pId, hx, hy)

    if udg_AI_TargetFound then
        // 1. Hero Order
        if heroAlive then
            set ord = GetUnitCurrentOrder(h)
            // Only if h is NOT currently casting our custom spells (852089 blizzard, 852579 charm, 852123 mirrorimage, 852594 summongrizzly)
            if not (ord == 852089 or ord == 852579 or ord == 852123 or ord == 852594) then
                // NOT fleeing at low HP (GetWidgetLife(h) > MaxLife * 0.25 or H003)
                if (GetWidgetLife(h) > GetUnitState(h, UNIT_STATE_MAX_LIFE) * 0.25 or GetUnitTypeId(h) == 'H003') then
                    // If ord is idle (0), stop (851972), hold (851993), patrol (851990), OR no enemies within 700.0 range
                    if (ord == 0 or ord == 851972 or ord == 851993 or ord == 851990) or not AI_HasEnemyInRange(p, hx, hy, 700.0) then
                        call IssuePointOrder(h, "attack", udg_AI_TargetX, udg_AI_TargetY)
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
                set uOrd = GetUnitCurrentOrder(enumU)
                // Exclude lumber harvesters (e.g. ghouls: 852018 harvest, 852020 returnresources)
                if uOrd != 852018 and uOrd != 852020 then
                    set ux = GetUnitX(enumU)
                    set uy = GetUnitY(enumU)
                    if uOrd == 0 or not AI_HasEnemyInRange(p, ux, uy, 600.0) then
                        if heroAlive then
                            set dx = ux - hx
                            set dy = uy - hy
                            set distSq = dx * dx + dy * dy
                            if distSq > 810000.0 then // 900.0 * 900.0
                                call IssuePointOrder(enumU, "attack", hx, hy)
                            else
                                call IssuePointOrder(enumU, "attack", udg_AI_TargetX, udg_AI_TargetY)
                            endif
                        else
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

function AI_TacticalLoop takes nothing returns nothing"""

assert "function AI_TacticalLoop takes nothing returns nothing" in content, "Failed to find AI_TacticalLoop"
content = content.replace("function AI_TacticalLoop takes nothing returns nothing", functions_code, 1)

# 3. Update AI_TacticalLoop locals and execution
old_tactical_top = """function AI_TacticalLoop takes nothing returns nothing
    local integer i = 0
    local unit h = null
    local integer hTypeId = 0
    local real hx = 0.0
    local real hy = 0.0
    local integer enemyCount = 0
    local unit bestEnemy = null
    local boolean bestIsHero = false
    local real bestLife = 0.0
    local unit clusterEnemy = null
    local unit nearestEnemy = null
    local real minD = 99999999.0
    local real dx = 0.0
    local real dy = 0.0
    local real d = 0.0
    local unit enumU = null
    local group g = null
    local unit altar = null
    local unit th = null
    local integer curOrder = 0

    set i = 0"""

new_tactical_top = """function AI_TacticalLoop takes nothing returns nothing
    local integer i = 0
    local unit h = null
    local integer hTypeId = 0
    local real hx = 0.0
    local real hy = 0.0
    local integer enemyCount = 0
    local unit bestEnemy = null
    local boolean bestIsHero = false
    local real bestLife = 0.0
    local unit clusterEnemy = null
    local unit nearestEnemy = null
    local real minD = 99999999.0
    local real dx = 0.0
    local real dy = 0.0
    local real d = 0.0
    local unit enumU = null
    local group g = null
    local unit altar = null
    local unit th = null
    local integer curOrder = 0
    local boolean doCommand = false

    set udg_AI_CommandTick = udg_AI_CommandTick + 1
    if udg_AI_CommandTick >= 4 then
        set udg_AI_CommandTick = 0
        set doCommand = true
    endif

    set i = 0"""

assert old_tactical_top in content, "Failed to find old_tactical_top"
content = content.replace(old_tactical_top, new_tactical_top, 1)

# 4. Insert call AI_CommandArmyForPlayer(i) inside if udg_AI_HeroMode[i] > 0
old_tactical_bottom = """                    set h = null
                    set bestEnemy = null
                    set clusterEnemy = null
                    set nearestEnemy = null
                endif
            endif
        endif
        set i = i + 1"""

new_tactical_bottom = """                    set h = null
                    set bestEnemy = null
                    set clusterEnemy = null
                    set nearestEnemy = null
                endif

                // 4. Strategic Army Commander (Every 4.0 seconds)
                if doCommand then
                    call AI_CommandArmyForPlayer(i)
                endif
            endif
        endif
        set i = i + 1"""

assert old_tactical_bottom in content, "Failed to find old_tactical_bottom"
content = content.replace(old_tactical_bottom, new_tactical_bottom, 1)

# 5. Initialize groups in DM_InitTriggers
old_groups_init = """    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()"""

new_groups_init = """    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()
    set udg_AI_ArmyGroup = CreateGroup()
    set udg_AI_CombatGroup = CreateGroup()"""

assert old_groups_init in content, "Failed to find old_groups_init"
content = content.replace(old_groups_init, new_groups_init, 1)

with open(war3map_j_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched war3map.j with AI Strategic Army Commander!")
