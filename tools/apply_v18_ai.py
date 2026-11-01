import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JASS_PATH = os.path.join(ROOT, "payload", "war3map.j")

with open(JASS_PATH, "r", encoding="utf-8") as f:
    jass = f.read()

# 1. Globals Block
old_globals = """    unit array udg_KarmaUnit
    player array udg_KarmaOwner
    integer array udg_KarmaLevel
    effect array udg_KarmaFx
    integer udg_KarmaCount = 0
endglobals"""

new_globals = """    unit array udg_KarmaUnit
    player array udg_KarmaOwner
    integer array udg_KarmaLevel
    effect array udg_KarmaFx
    integer udg_KarmaCount = 0

    // Test Mode & AI Hero System Globals
    dialog udg_TM_MainDialog = null
    button udg_TM_BtnNormal = null
    button udg_TM_BtnMode1All = null
    button udg_TM_BtnMode2All = null
    button udg_TM_BtnCustom = null

    dialog udg_TM_SlotDialog = null
    button array udg_TM_SlotBtn
    button udg_TM_SlotConfirm = null

    // Per-player AI hero assignment: 0 = Normal Melee AI, 1 = H002 (幻梦大师), 2 = H003 (魔音忍者)
    integer array udg_AI_HeroMode
    unit array udg_AI_CustomHero
    boolean array udg_AI_HeroSpawned
    real array udg_AI_CastCD_Q
    real array udg_AI_CastCD_W
    real array udg_AI_CastCD_E
    real array udg_AI_CastCD_R

    // AI Helper Tracking Globals
    real array udg_AI_DeadTimer
    real array udg_AI_AltarTimer
    real array udg_AI_WaitTimer
    player udg_TM_PromptPlayer = null
endglobals"""

assert old_globals in jass, "old_globals not found in war3map.j"
jass = jass.replace(old_globals, new_globals, 1)

# 2. AI Helper Functions & Tactical Loop before DM_CapTimerLoop
ai_funcs_before_loop = """function AI_GetPlayerAltar takes player p returns unit
    local group g = CreateGroup()
    local unit u = null
    local unit altar = null
    local integer uId = 0
    call GroupEnumUnitsOfPlayer(g, p, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        set uId = GetUnitTypeId(u)
        if (uId == 'halt' or uId == 'oalt' or uId == 'uaod' or uId == 'eate') and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
            set altar = u
            call GroupClear(g)
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set u = null
    return altar
endfunction

function AI_GetPlayerTownHall takes player p returns unit
    local group g = CreateGroup()
    local unit u = null
    local unit th = null
    local integer uId = 0
    call GroupEnumUnitsOfPlayer(g, p, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        set uId = GetUnitTypeId(u)
        if (uId == 'htow' or uId == 'hkee' or uId == 'hcas' or uId == 'ogre' or uId == 'ostr' or uId == 'ofrt' or uId == 'unpl' or uId == 'unp1' or uId == 'unp2' or uId == 'etol' or uId == 'etoa' or uId == 'etot') and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
            set th = u
            call GroupClear(g)
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set u = null
    return th
endfunction

function AI_AutoLearnSkills takes unit h returns nothing
    local integer pts = 0
    local integer prevPts = 0
    local integer uId = 0
    if h == null or IsUnitType(h, UNIT_TYPE_DEAD) then
        return
    endif
    set uId = GetUnitTypeId(h)
    set pts = GetHeroSkillPoints(h)
    if pts <= 0 then
        return
    endif

    if uId == 'H002' then
        loop
            exitwhen pts <= 0
            set prevPts = pts
            call SelectHeroSkill(h, 'A004')
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'A003')
            endif
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'A001')
            endif
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'A002')
            endif
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'Aamk')
            endif
            set pts = GetHeroSkillPoints(h)
            if pts == prevPts then
                exitwhen true
            endif
        endloop
    elseif uId == 'H003' then
        loop
            exitwhen pts <= 0
            set prevPts = pts
            call SelectHeroSkill(h, 'A014')
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'A011')
            endif
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'A013')
            endif
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'A012')
            endif
            if GetHeroSkillPoints(h) == prevPts then
                call SelectHeroSkill(h, 'Aamk')
            endif
            set pts = GetHeroSkillPoints(h)
            if pts == prevPts then
                exitwhen true
            endif
        endloop
    endif
endfunction

function AI_SpawnCustomHeroForPlayer takes integer pId, real x, real y, real facing returns unit
    local integer hTypeId = 'H002'
    local unit h = null
    if udg_AI_HeroMode[pId] == 2 then
        set hTypeId = 'H003'
    endif
    set h = CreateUnit(Player(pId), hTypeId, x, y, facing)
    set udg_AI_CustomHero[pId] = h
    set udg_AI_HeroSpawned[pId] = true
    set udg_AI_DeadTimer[pId] = 0.0
    set udg_AI_AltarTimer[pId] = 0.0
    set udg_AI_WaitTimer[pId] = 0.0
    set udg_AI_CastCD_Q[pId] = 0.0
    set udg_AI_CastCD_W[pId] = 0.0
    set udg_AI_CastCD_E[pId] = 0.0
    set udg_AI_CastCD_R[pId] = 0.0

    call UnitAddItemById(h, 'stwp')

    if hTypeId == 'H003' then
        set udg_Ninja_TrueHero[pId] = h
    endif

    call AI_AutoLearnSkills(h)

    call SetPlayerTechMaxAllowed(Player(pId), 'H002', 1)
    call SetPlayerTechMaxAllowed(Player(pId), 'H003', 1)

    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\MassTeleport\\\\MassTeleportTarget.mdl", h, "origin"))

    return h
endfunction

function AI_TacticalLoop takes nothing returns nothing
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

    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] > 0 then
                // Decrement Cooldowns
                if udg_AI_CastCD_Q[i] > 0.0 then
                    set udg_AI_CastCD_Q[i] = udg_AI_CastCD_Q[i] - 1.0
                endif
                if udg_AI_CastCD_W[i] > 0.0 then
                    set udg_AI_CastCD_W[i] = udg_AI_CastCD_W[i] - 1.0
                endif
                if udg_AI_CastCD_E[i] > 0.0 then
                    set udg_AI_CastCD_E[i] = udg_AI_CastCD_E[i] - 1.0
                endif
                if udg_AI_CastCD_R[i] > 0.0 then
                    set udg_AI_CastCD_R[i] = udg_AI_CastCD_R[i] - 1.0
                endif

                // 1. Check if custom hero needs to be spawned / replaced
                if not udg_AI_HeroSpawned[i] then
                    // Case 1: Check if standard hero exists to replace
                    set g = CreateGroup()
                    call GroupEnumUnitsOfPlayer(g, Player(i), null)
                    loop
                        set enumU = FirstOfGroup(g)
                        exitwhen enumU == null
                        call GroupRemoveUnit(g, enumU)
                        if IsUnitType(enumU, UNIT_TYPE_HERO) and GetUnitTypeId(enumU) != 'H002' and GetUnitTypeId(enumU) != 'H003' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                            set hx = GetUnitX(enumU)
                            set hy = GetUnitY(enumU)
                            set d = GetUnitFacing(enumU)
                            call RemoveUnit(enumU)
                            call AI_SpawnCustomHeroForPlayer(i, hx, hy, d)
                            call GroupClear(g)
                        endif
                    endloop
                    call DestroyGroup(g)
                    set g = null

                    // Case 2: Check altar or townhall timing fallback
                    if not udg_AI_HeroSpawned[i] then
                        set altar = AI_GetPlayerAltar(Player(i))
                        if altar != null then
                            set udg_AI_AltarTimer[i] = udg_AI_AltarTimer[i] + 1.0
                            if udg_AI_AltarTimer[i] >= 20.0 then
                                call AI_SpawnCustomHeroForPlayer(i, GetUnitX(altar), GetUnitY(altar) - 150.0, 270.0)
                            endif
                        else
                            set udg_AI_WaitTimer[i] = udg_AI_WaitTimer[i] + 1.0
                            if udg_AI_WaitTimer[i] >= 60.0 then
                                set th = AI_GetPlayerTownHall(Player(i))
                                if th != null then
                                    call AI_SpawnCustomHeroForPlayer(i, GetUnitX(th) + 150.0, GetUnitY(th), 270.0)
                                else
                                    call AI_SpawnCustomHeroForPlayer(i, GetStartLocationX(GetPlayerStartLocation(Player(i))), GetStartLocationY(GetPlayerStartLocation(Player(i))), 270.0)
                                endif
                                set th = null
                            endif
                        endif
                        set altar = null
                    endif
                endif

                // 2. Check Auto-Revive for dead custom hero
                set h = udg_AI_CustomHero[i]
                if h != null and IsUnitType(h, UNIT_TYPE_DEAD) then
                    set altar = AI_GetPlayerAltar(Player(i))
                    if altar != null then
                        set udg_AI_DeadTimer[i] = udg_AI_DeadTimer[i] + 1.0
                        if udg_AI_DeadTimer[i] < 25.0 then
                            call IssueImmediateOrderById(altar, GetUnitTypeId(h))
                            call IssueNeutralImmediateOrderById(Player(i), altar, GetUnitTypeId(h))
                        else
                            call ReviveHero(h, GetUnitX(altar), GetUnitY(altar) - 150.0, true)
                            set udg_AI_DeadTimer[i] = 0.0
                            call AI_AutoLearnSkills(h)
                            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", h, "origin"))
                        endif
                    endif
                    set altar = null
                else
                    set udg_AI_DeadTimer[i] = 0.0
                endif

                // 3. Tactical Brain for living custom hero
                if h != null and not IsUnitType(h, UNIT_TYPE_DEAD) and GetWidgetLife(h) > 0.405 then
                    set hx = GetUnitX(h)
                    set hy = GetUnitY(h)
                    set hTypeId = GetUnitTypeId(h)

                    // Auto-learn skills
                    call AI_AutoLearnSkills(h)

                    // Scan 900.0 range for enemies
                    set enemyCount = 0
                    set bestEnemy = null
                    set bestIsHero = false
                    set bestLife = 0.0
                    set clusterEnemy = null
                    set nearestEnemy = null
                    set minD = 99999999.0

                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 900.0, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, Player(i)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' then
                            set dx = GetUnitX(enumU) - hx
                            set dy = GetUnitY(enumU) - hy
                            set d = dx * dx + dy * dy
                            if nearestEnemy == null or d < minD then
                                set nearestEnemy = enumU
                                set minD = d
                            endif

                            if not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) then
                                set enemyCount = enemyCount + 1
                                if clusterEnemy == null then
                                    set clusterEnemy = enumU
                                endif

                                if IsUnitType(enumU, UNIT_TYPE_HERO) then
                                    if not bestIsHero or GetWidgetLife(enumU) > bestLife then
                                        set bestEnemy = enumU
                                        set bestIsHero = true
                                        set bestLife = GetWidgetLife(enumU)
                                    endif
                                elseif not bestIsHero then
                                    if bestEnemy == null or GetWidgetLife(enumU) > bestLife then
                                        set bestEnemy = enumU
                                        set bestLife = GetWidgetLife(enumU)
                                    endif
                                endif
                            endif
                        endif
                    endloop

                    // Tactical decision tree based on Hero Type
                    if hTypeId == 'H002' then
                        // 幻梦大师 Tactical Brain
                        // Cast E: A003 万象皆虚
                        if GetUnitAbilityLevel(h, 'A003') > 0 and udg_AI_CastCD_E[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 120.0 and enemyCount >= 2 and clusterEnemy != null then
                            call IssuePointOrder(h, "blizzard", GetUnitX(clusterEnemy), GetUnitY(clusterEnemy))
                            set udg_AI_CastCD_E[i] = 30.0
                        // Cast W: A002 幻梦奴役
                        elseif GetUnitAbilityLevel(h, 'A002') > 0 and udg_AI_CastCD_W[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 100.0 and bestEnemy != null then
                            call IssueTargetOrder(h, "charm", bestEnemy)
                            set udg_AI_CastCD_W[i] = 25.0
                        // Cast Q: A001 镜像与潜行
                        elseif GetUnitAbilityLevel(h, 'A001') > 0 and udg_AI_CastCD_Q[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 100.0 and (enemyCount >= 1 or GetWidgetLife(h) < GetUnitState(h, UNIT_STATE_MAX_LIFE) * 0.75) then
                            call IssueImmediateOrder(h, "mirrorimage")
                            set udg_AI_CastCD_Q[i] = 16.0
                        endif

                        // Command nearby clones to fight
                        if nearestEnemy != null then
                            call GroupClear(udg_EnumGroup)
                            call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 1000.0, null)
                            loop
                                set enumU = FirstOfGroup(udg_EnumGroup)
                                exitwhen enumU == null
                                call GroupRemoveUnit(udg_EnumGroup, enumU)
                                if GetOwningPlayer(enumU) == Player(i) and enumU != h and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 then
                                    if IsUnitType(enumU, UNIT_TYPE_SUMMONED) or IsUnitIllusion(enumU) or IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                                        set curOrder = GetUnitCurrentOrder(enumU)
                                        if curOrder == 0 or curOrder == 851972 or curOrder == 851973 then
                                            call IssuePointOrder(enumU, "attack", GetUnitX(nearestEnemy), GetUnitY(nearestEnemy))
                                        endif
                                    endif
                                endif
                            endloop
                        endif

                    elseif hTypeId == 'H003' then
                        // 魔音忍者 Tactical Brain
                        // Ensure Aura is on once A012 is learned
                        if GetUnitAbilityLevel(h, 'A012') > 0 and not udg_Ninja_AuraOn[i] then
                            set udg_Ninja_AuraOn[i] = true
                            if udg_Ninja_AuraFx[i] == null then
                                set udg_Ninja_AuraFx[i] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", h, "origin")
                            endif
                        endif

                        // Cast R: A014 独断万古
                        if GetUnitAbilityLevel(h, 'A014') > 0 and udg_AI_CastCD_R[i] <= 0.0 and GetUnitState(h, UNIT_STATE_MANA) >= 120.0 and enemyCount >= 1 then
                            call IssueImmediateOrder(h, "summongrizzly")
                            set udg_AI_CastCD_R[i] = 60.0
                        endif

                        // Command nearby ninja clones to fight
                        if nearestEnemy != null then
                            call GroupClear(udg_EnumGroup)
                            call GroupEnumUnitsInRange(udg_EnumGroup, hx, hy, 1000.0, null)
                            loop
                                set enumU = FirstOfGroup(udg_EnumGroup)
                                exitwhen enumU == null
                                call GroupRemoveUnit(udg_EnumGroup, enumU)
                                if GetOwningPlayer(enumU) == Player(i) and enumU != h and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 then
                                    if GetUnitTypeId(enumU) == 'u002' or GetUnitTypeId(enumU) == 'u001' or IsUnitType(enumU, UNIT_TYPE_SUMMONED) then
                                        set curOrder = GetUnitCurrentOrder(enumU)
                                        if curOrder == 0 or curOrder == 851972 or curOrder == 851973 then
                                            call IssuePointOrder(enumU, "attack", GetUnitX(nearestEnemy), GetUnitY(nearestEnemy))
                                        endif
                                    endif
                                endif
                            endloop
                        endif
                    endif

                    set h = null
                    set bestEnemy = null
                    set clusterEnemy = null
                    set nearestEnemy = null
                endif
            endif
        endif
        set i = i + 1
    endloop
endfunction

"""

assert "function DM_CapTimerLoop takes nothing returns nothing" in jass
jass = jass.replace("function DM_CapTimerLoop takes nothing returns nothing", ai_funcs_before_loop + "function DM_CapTimerLoop takes nothing returns nothing", 1)

# 3. Call AI_TacticalLoop in DM_CapTimerLoop
old_cap_end = """        set u = null
        set i = i + 1
    endloop
endfunction"""

new_cap_end = """        set u = null
        set i = i + 1
    endloop

    // 4. Custom Hero AI Tactical Loop
    call AI_TacticalLoop()
endfunction"""

assert old_cap_end in jass, "old_cap_end not found in war3map.j"
jass = jass.replace(old_cap_end, new_cap_end, 1)

# 4. DM_CloneOneUnit: command computer-owned clones immediately
old_clone_hero = """            call GroupAddUnit(udg_FakeHeroGroup, clone)
            call UnitApplyTimedLife(clone, 'BTLF', 900.0)
            call SetUnitVertexColor(clone, 100, 150, 255, 180)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
            set clone = null"""

new_clone_hero = """            call GroupAddUnit(udg_FakeHeroGroup, clone)
            call UnitApplyTimedLife(clone, 'BTLF', 900.0)
            call SetUnitVertexColor(clone, 100, 150, 255, 180)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
            if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
                call IssuePointOrder(clone, "attack", GetUnitX(orig), GetUnitY(orig))
            endif
            set clone = null"""

assert old_clone_hero in jass, "old_clone_hero not found"
jass = jass.replace(old_clone_hero, new_clone_hero, 1)

old_clone_nonhero = """        call UnitAddType(clone, UNIT_TYPE_SUMMONED)
        call UnitApplyTimedLife(clone, 'BTLF', 900.0)
        call SetUnitVertexColor(clone, 100, 150, 255, 180)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
        set clone = null"""

new_clone_nonhero = """        call UnitAddType(clone, UNIT_TYPE_SUMMONED)
        call UnitApplyTimedLife(clone, 'BTLF', 900.0)
        call SetUnitVertexColor(clone, 100, 150, 255, 180)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            call IssuePointOrder(clone, "attack", GetUnitX(orig), GetUnitY(orig))
        endif
        set clone = null"""

assert old_clone_nonhero in jass, "old_clone_nonhero not found"
jass = jass.replace(old_clone_nonhero, new_clone_nonhero, 1)

# 5. Test Mode UI & Logic functions before DM_InitTriggers
tm_ui_funcs = """function TM_ApplyAIConfig takes nothing returns nothing
    local integer i = 0
    local group g = null
    local unit u = null
    local boolean hasCustom = false

    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] > 0 then
                set hasCustom = true
                if not udg_AI_HeroSpawned[i] then
                    set g = CreateGroup()
                    call GroupEnumUnitsOfPlayer(g, Player(i), null)
                    loop
                        set u = FirstOfGroup(g)
                        exitwhen u == null
                        call GroupRemoveUnit(g, u)
                        if IsUnitType(u, UNIT_TYPE_HERO) and GetUnitTypeId(u) != 'H002' and GetUnitTypeId(u) != 'H003' and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
                            call AI_SpawnCustomHeroForPlayer(i, GetUnitX(u), GetUnitY(u), GetUnitFacing(u))
                            call RemoveUnit(u)
                            call GroupClear(g)
                        endif
                    endloop
                    call DestroyGroup(g)
                    set g = null
                endif
            endif
        endif
        set i = i + 1
    endloop
endfunction

function TM_ShowSlotDialog takes player p returns nothing
    local integer i = 0
    local string lbl = ""
    set udg_TM_PromptPlayer = p
    call DialogClear(udg_TM_SlotDialog)
    call DialogSetMessage(udg_TM_SlotDialog, "点击切换各电脑英雄（确认后生效）")
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] == 1 then
                set lbl = "电脑 " + I2S(i + 1) + "：【幻梦大师】 (点击切换)"
            elseif udg_AI_HeroMode[i] == 2 then
                set lbl = "电脑 " + I2S(i + 1) + "：【魔音忍者】 (点击切换)"
            else
                set lbl = "电脑 " + I2S(i + 1) + "：原版默认英雄 (点击切换)"
            endif
            set udg_TM_SlotBtn[i] = DialogAddButton(udg_TM_SlotDialog, lbl, 0)
        else
            set udg_TM_SlotBtn[i] = null
        endif
        set i = i + 1
    endloop
    set udg_TM_SlotConfirm = DialogAddButton(udg_TM_SlotDialog, "【确认配置并开始】", 0)
    call DialogDisplay(p, udg_TM_SlotDialog, true)
endfunction

function TM_ShowMainDialog takes player p returns nothing
    set udg_TM_PromptPlayer = p
    call DialogDisplay(p, udg_TM_MainDialog, true)
endfunction

function TM_OnMainDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if b == udg_TM_BtnNormal then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 0
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 已选择正常模式：所有电脑使用原版默认英雄。")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode1All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 已选择测试模式一：全部电脑出【幻梦大师】！")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode2All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 2
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 已选择测试模式二：全部电脑出【魔音忍者】！")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnCustom then
        call TM_ShowSlotDialog(p)
    endif

    set b = null
    set p = null
endfunction

function TM_OnSlotDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if b == udg_TM_SlotConfirm then
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 电脑英雄精细配置已确认并生效！")
        call TM_ApplyAIConfig()
    else
        set i = 0
        loop
            exitwhen i > 7
            if b == udg_TM_SlotBtn[i] then
                if udg_AI_HeroMode[i] == 0 then
                    set udg_AI_HeroMode[i] = 1
                elseif udg_AI_HeroMode[i] == 1 then
                    set udg_AI_HeroMode[i] = 2
                else
                    set udg_AI_HeroMode[i] = 0
                endif
                call TM_ShowSlotDialog(p)
                set b = null
                set p = null
                return
            endif
            set i = i + 1
        endloop
    endif

    set b = null
    set p = null
endfunction

function TM_GetFirstHumanPlayer takes nothing returns player
    local integer i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER then
            return Player(i)
        endif
        set i = i + 1
    endloop
    return null
endfunction

function TM_OnStartTimer takes nothing returns nothing
    local player p = TM_GetFirstHumanPlayer()
    if p != null then
        call TM_ShowMainDialog(p)
    endif
    set p = null
    call DestroyTimer(GetExpiredTimer())
endfunction

function AI_OnUnitTrainFinish takes nothing returns boolean
    local unit trained = GetTrainedUnit()
    local player p = null
    local integer pId = 0
    local real hx = 0.0
    local real hy = 0.0
    local real hf = 0.0

    if trained != null then
        set p = GetOwningPlayer(trained)
        set pId = GetPlayerId(p)
        if GetPlayerController(p) == MAP_CONTROL_COMPUTER and udg_AI_HeroMode[pId] > 0 and not udg_AI_HeroSpawned[pId] then
            if IsUnitType(trained, UNIT_TYPE_HERO) and GetUnitTypeId(trained) != 'H002' and GetUnitTypeId(trained) != 'H003' and not IsUnitIllusion(trained) and not IsUnitInGroup(trained, udg_FakeHeroGroup) then
                set hx = GetUnitX(trained)
                set hy = GetUnitY(trained)
                set hf = GetUnitFacing(trained)
                call RemoveUnit(trained)
                call AI_SpawnCustomHeroForPlayer(pId, hx, hy, hf)
            endif
        endif
    endif

    set trained = null
    set p = null
    return false
endfunction

"""

assert "function DM_InitTriggers takes nothing returns nothing" in jass
jass = jass.replace("function DM_InitTriggers takes nothing returns nothing", tm_ui_funcs + "function DM_InitTriggers takes nothing returns nothing", 1)

# 6. Replace DM_InitTriggers implementation
old_init_triggers = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tSkill = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()
    local integer i = 0

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()

    set i = 0
    loop
        exitwhen i > 15
        set udg_Ninja_CloneGroup[i] = CreateGroup()
        set udg_Ninja_AuraOn[i] = false
        set udg_Ninja_AuraFx[i] = null
        set udg_Ninja_TrueHero[i] = null
        set i = i + 1
    endloop

    call TriggerRegisterAnyUnitEventBJ(tEffect, EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddCondition(tEffect, Condition(function DM_OnSpellEffect))

    call TriggerRegisterAnyUnitEventBJ(tCast, EVENT_PLAYER_UNIT_SPELL_CAST)
    call TriggerAddCondition(tCast, Condition(function DM_OnSpellCast))

    call TriggerRegisterAnyUnitEventBJ(tDeath, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddCondition(tDeath, Condition(function DM_OnUnitDeath))

    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))

    call TriggerRegisterAnyUnitEventBJ(tDamage, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))

    call TriggerRegisterAnyUnitEventBJ(tSkill, EVENT_PLAYER_HERO_SKILL)
    call TriggerAddCondition(tSkill, Condition(function Ninja_OnHeroSkill))

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tSkill = null
    set tmrCap = null
    set tmrStealth = null
endfunction"""

new_init_triggers = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tSkill = CreateTrigger()
    local trigger tTrain = CreateTrigger()
    local trigger tMainDialog = CreateTrigger()
    local trigger tSlotDialog = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()
    local timer tmrStart = CreateTimer()
    local integer i = 0

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()

    set i = 0
    loop
        exitwhen i > 15
        set udg_Ninja_CloneGroup[i] = CreateGroup()
        set udg_Ninja_AuraOn[i] = false
        set udg_Ninja_AuraFx[i] = null
        set udg_Ninja_TrueHero[i] = null

        // Initialize AI variables
        set udg_AI_HeroMode[i] = 0
        set udg_AI_CustomHero[i] = null
        set udg_AI_HeroSpawned[i] = false
        set udg_AI_CastCD_Q[i] = 0.0
        set udg_AI_CastCD_W[i] = 0.0
        set udg_AI_CastCD_E[i] = 0.0
        set udg_AI_CastCD_R[i] = 0.0
        set udg_AI_DeadTimer[i] = 0.0
        set udg_AI_AltarTimer[i] = 0.0
        set udg_AI_WaitTimer[i] = 0.0
        set udg_TM_SlotBtn[i] = null
        set i = i + 1
    endloop

    // Initialize Test Mode Dialogs
    set udg_TM_MainDialog = DialogCreate()
    call DialogSetMessage(udg_TM_MainDialog, "【测试模式选择】(可扩展AI测试框架)")
    set udg_TM_BtnNormal = DialogAddButton(udg_TM_MainDialog, "正常模式：电脑使用原版随机英雄", 0)
    set udg_TM_BtnMode1All = DialogAddButton(udg_TM_MainDialog, "测试模式一：全部电脑出【幻梦大师】", 0)
    set udg_TM_BtnMode2All = DialogAddButton(udg_TM_MainDialog, "测试模式二：全部电脑出【魔音忍者】", 0)
    set udg_TM_BtnCustom = DialogAddButton(udg_TM_MainDialog, "精细配置：逐个指定各家电脑出什么英雄...", 0)

    set udg_TM_SlotDialog = DialogCreate()

    call TriggerRegisterDialogEvent(tMainDialog, udg_TM_MainDialog)
    call TriggerAddAction(tMainDialog, function TM_OnMainDialogClicked)

    call TriggerRegisterDialogEvent(tSlotDialog, udg_TM_SlotDialog)
    call TriggerAddAction(tSlotDialog, function TM_OnSlotDialogClicked)

    call TriggerRegisterAnyUnitEventBJ(tEffect, EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddCondition(tEffect, Condition(function DM_OnSpellEffect))

    call TriggerRegisterAnyUnitEventBJ(tCast, EVENT_PLAYER_UNIT_SPELL_CAST)
    call TriggerAddCondition(tCast, Condition(function DM_OnSpellCast))

    call TriggerRegisterAnyUnitEventBJ(tDeath, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddCondition(tDeath, Condition(function DM_OnUnitDeath))

    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))

    call TriggerRegisterAnyUnitEventBJ(tDamage, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))

    call TriggerRegisterAnyUnitEventBJ(tSkill, EVENT_PLAYER_HERO_SKILL)
    call TriggerAddCondition(tSkill, Condition(function Ninja_OnHeroSkill))

    call TriggerRegisterAnyUnitEventBJ(tTrain, EVENT_PLAYER_UNIT_TRAIN_FINISH)
    call TriggerAddCondition(tTrain, Condition(function AI_OnUnitTrainFinish))

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)
    call TimerStart(tmrStart, 0.50, false, function TM_OnStartTimer)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tSkill = null
    set tTrain = null
    set tMainDialog = null
    set tSlotDialog = null
    set tmrCap = null
    set tmrStealth = null
    set tmrStart = null
endfunction"""

assert old_init_triggers in jass, "old_init_triggers not found"
jass = jass.replace(old_init_triggers, new_init_triggers, 1)

# Write updated war3map.j
with open(JASS_PATH, "w", encoding="utf-8") as f:
    f.write(jass)

print("war3map.j updated successfully.")
