import os

path = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize to LF for matching
is_crlf = '\r\n' in content
if is_crlf:
    content = content.replace('\r\n', '\n')

# 1. Update Ninja_SpawnClone
t1 = """    if trueHero != null then
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

    if trueHero != null and lv > 0 then
        call UnitAddAbility(clone, 'A015')
        call SetUnitAbilityLevel(clone, 'A015', lv)
    endif"""

r1 = """    if trueHero != null then
        set lv = GetUnitAbilityLevel(trueHero, 'A011')
    endif
    if lv <= 0 and (GetPlayerController(p) == MAP_CONTROL_COMPUTER or trueHero == null) then
        set lv = 1
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

    if lv > 0 then
        call UnitAddAbility(clone, 'A015')
        call SetUnitAbilityLevel(clone, 'A015', lv)
    endif"""

assert t1 in content, "Target 1 not found"
content = content.replace(t1, r1, 1)
print("Applied replacement 1")

# 2. Update AI_AutoLearnSkills
t2 = """function AI_AutoLearnSkills takes unit h returns nothing
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
endfunction"""

r2 = r"""function AI_ForceLearnSkill takes unit h, integer abilId, integer maxLv, boolean isUlt returns boolean
    local integer pts = GetHeroSkillPoints(h)
    local integer hLv = GetHeroLevel(h)
    local integer curLv = GetUnitAbilityLevel(h, abilId)
    local integer reqLv = 1
    local integer pId = 0
    local group g = null
    local unit u = null

    if pts <= 0 then
        return false
    endif
    if curLv >= maxLv then
        return false
    endif

    if isUlt then
        set reqLv = 6
    elseif abilId == 'Aamk' then
        set reqLv = 1
    else
        set reqLv = curLv * 2 + 1
    endif

    if hLv < reqLv then
        return false
    endif

    call SelectHeroSkill(h, abilId)

    if GetUnitAbilityLevel(h, abilId) == curLv then
        if curLv == 0 then
            call UnitAddAbility(h, abilId)
        else
            call SetUnitAbilityLevel(h, abilId, curLv + 1)
        endif
        call UnitModifySkillPoints(h, -1)
    endif

    if GetUnitAbilityLevel(h, abilId) <= curLv then
        return false
    endif

    set pId = GetPlayerId(GetOwningPlayer(h))
    if abilId == 'A012' then
        if not udg_Ninja_AuraOn[pId] then
            set udg_Ninja_AuraOn[pId] = true
            if udg_Ninja_AuraFx[pId] == null then
                set udg_Ninja_AuraFx[pId] = AddSpecialEffectTarget("Abilities\\Spells\\Other\\GeneralAuraTarget\\GeneralAuraTarget.mdl", h, "origin")
            endif
        endif
    elseif abilId == 'A011' then
        if udg_Ninja_CloneGroup[pId] != null then
            set g = CreateGroup()
            call GroupAddGroup(udg_Ninja_CloneGroup[pId], g)
            loop
                set u = FirstOfGroup(g)
                exitwhen u == null
                call GroupRemoveUnit(g, u)
                if GetUnitTypeId(u) == 'u002' and not IsUnitType(u, UNIT_TYPE_DEAD) then
                    if GetUnitAbilityLevel(u, 'A015') == 0 then
                        call UnitAddAbility(u, 'A015')
                    endif
                    call SetUnitAbilityLevel(u, 'A015', GetUnitAbilityLevel(h, 'A011'))
                endif
            endloop
            call DestroyGroup(g)
            set g = null
        endif
    endif

    return true
endfunction

function AI_LearnSkillForNinja takes unit h returns boolean
    local integer hLv = GetHeroLevel(h)
    local integer qLv = GetUnitAbilityLevel(h, 'A011')
    local integer eLv = GetUnitAbilityLevel(h, 'A013')
    local integer wLv = GetUnitAbilityLevel(h, 'A012')
    local integer rLv = GetUnitAbilityLevel(h, 'A014')

    // 1. Ultimate at Lv 6+
    if hLv >= 6 and rLv == 0 then
        return AI_ForceLearnSkill(h, 'A014', 1, true)
    endif

    // 2. Primary skill Q (A011) at Lv 1, 3, 5
    if qLv < 3 and hLv >= (qLv * 2 + 1) then
        if not (hLv == 2 and eLv == 0) and not (hLv == 4 and wLv == 0) then
            return AI_ForceLearnSkill(h, 'A011', 3, false)
        endif
    endif

    // 3. Learn unlearned basic skills (E at Lv 2, W at Lv 4)
    if eLv == 0 then
        return AI_ForceLearnSkill(h, 'A013', 3, false)
    endif
    if wLv == 0 then
        return AI_ForceLearnSkill(h, 'A012', 3, false)
    endif

    // 4. Max Q if still available
    if qLv < 3 and hLv >= (qLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A011', 3, false)
    endif

    // 5. Upgrade E
    if eLv < 3 and hLv >= (eLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A013', 3, false)
    endif

    // 6. Upgrade W
    if wLv < 3 and hLv >= (wLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A012', 3, false)
    endif

    // 7. Stat bonus
    return AI_ForceLearnSkill(h, 'Aamk', 10, false)
endfunction

function AI_LearnSkillForDreamMaster takes unit h returns boolean
    local integer hLv = GetHeroLevel(h)
    local integer qLv = GetUnitAbilityLevel(h, 'A001')
    local integer wLv = GetUnitAbilityLevel(h, 'A002')
    local integer eLv = GetUnitAbilityLevel(h, 'A003')
    local integer rLv = GetUnitAbilityLevel(h, 'A004')

    // 1. Ultimate at Lv 6+
    if hLv >= 6 and rLv == 0 then
        return AI_ForceLearnSkill(h, 'A004', 1, true)
    endif

    // 2. Primary skill E (A003) at Lv 1, 3, 5
    if eLv < 3 and hLv >= (eLv * 2 + 1) then
        if not (hLv == 2 and qLv == 0) and not (hLv == 4 and wLv == 0) then
            return AI_ForceLearnSkill(h, 'A003', 3, false)
        endif
    endif

    // 3. Learn unlearned basic skills (Q at Lv 2, W at Lv 4)
    if qLv == 0 then
        return AI_ForceLearnSkill(h, 'A001', 3, false)
    endif
    if wLv == 0 then
        return AI_ForceLearnSkill(h, 'A002', 3, false)
    endif

    // 4. Max E if still available
    if eLv < 3 and hLv >= (eLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A003', 3, false)
    endif

    // 5. Upgrade Q
    if qLv < 3 and hLv >= (qLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A001', 3, false)
    endif

    // 6. Upgrade W
    if wLv < 3 and hLv >= (wLv * 2 + 1) then
        return AI_ForceLearnSkill(h, 'A002', 3, false)
    endif

    // 7. Stat bonus
    return AI_ForceLearnSkill(h, 'Aamk', 10, false)
endfunction

function AI_AutoLearnSkills takes unit h returns nothing
    local integer uId = 0
    local boolean learned = false

    if h == null or IsUnitType(h, UNIT_TYPE_DEAD) then
        return
    endif
    set uId = GetUnitTypeId(h)
    if GetHeroSkillPoints(h) <= 0 then
        return
    endif

    loop
        exitwhen GetHeroSkillPoints(h) <= 0
        set learned = false
        if uId == 'H002' then
            set learned = AI_LearnSkillForDreamMaster(h)
        elseif uId == 'H003' then
            set learned = AI_LearnSkillForNinja(h)
        endif
        if not learned then
            exitwhen true
        endif
    endloop
endfunction"""

assert t2 in content, "Target 2 not found"
content = content.replace(t2, r2, 1)
print("Applied replacement 2")

# 3. Update AI_OnUnitTrainFinish & AI_OnHeroLevel
t3 = """function AI_OnUnitTrainFinish takes nothing returns boolean
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
endfunction"""

r3 = """function AI_OnHeroLevel takes nothing returns boolean
    local unit h = GetLevelingUnit()
    if h != null and (GetUnitTypeId(h) == 'H002' or GetUnitTypeId(h) == 'H003') and GetPlayerController(GetOwningPlayer(h)) == MAP_CONTROL_COMPUTER then
        call AI_AutoLearnSkills(h)
    endif
    set h = null
    return false
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
        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            if GetUnitTypeId(trained) == 'H003' then
                set udg_Ninja_TrueHero[pId] = trained
                set udg_AI_CustomHero[pId] = trained
                set udg_AI_HeroSpawned[pId] = true
                call AI_AutoLearnSkills(trained)
            elseif GetUnitTypeId(trained) == 'H002' then
                set udg_AI_CustomHero[pId] = trained
                set udg_AI_HeroSpawned[pId] = true
                call AI_AutoLearnSkills(trained)
            elseif udg_AI_HeroMode[pId] > 0 and not udg_AI_HeroSpawned[pId] and IsUnitType(trained, UNIT_TYPE_HERO) and not IsUnitIllusion(trained) and not IsUnitInGroup(trained, udg_FakeHeroGroup) then
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
endfunction"""

assert t3 in content, "Target 3 not found"
content = content.replace(t3, r3, 1)
print("Applied replacement 3")

# 4. Update DM_InitTriggers
t4_decl = """    local trigger tSkill = CreateTrigger()
    local trigger tTrain = CreateTrigger()
    local trigger tMainDialog = CreateTrigger()"""

r4_decl = """    local trigger tSkill = CreateTrigger()
    local trigger tTrain = CreateTrigger()
    local trigger tLevel = CreateTrigger()
    local trigger tMainDialog = CreateTrigger()"""

assert t4_decl in content, "Target 4 decl not found"
content = content.replace(t4_decl, r4_decl, 1)

t4_reg = """    call TriggerRegisterAnyUnitEventBJ(tTrain, EVENT_PLAYER_UNIT_TRAIN_FINISH)
    call TriggerAddCondition(tTrain, Condition(function AI_OnUnitTrainFinish))"""

r4_reg = """    call TriggerRegisterAnyUnitEventBJ(tTrain, EVENT_PLAYER_UNIT_TRAIN_FINISH)
    call TriggerAddCondition(tTrain, Condition(function AI_OnUnitTrainFinish))

    call TriggerRegisterAnyUnitEventBJ(tLevel, EVENT_PLAYER_HERO_LEVEL)
    call TriggerAddCondition(tLevel, Condition(function AI_OnHeroLevel))"""

assert t4_reg in content, "Target 4 reg not found"
content = content.replace(t4_reg, r4_reg, 1)

t4_cleanup = """    set tSkill = null
    set tTrain = null
    set tMainDialog = null"""

r4_cleanup = """    set tSkill = null
    set tTrain = null
    set tLevel = null
    set tMainDialog = null"""

assert t4_cleanup in content, "Target 4 cleanup not found"
content = content.replace(t4_cleanup, r4_cleanup, 1)
print("Applied replacement 4")

# 5. Update DM_OnUnitDeath
t5 = """    // 4. 魔音同化 (A011) - 击杀单位生成伪英雄分身
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'H003' and not isFakeHero and not isIllusion and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u002' or GetUnitTypeId(killer) == 'u001') then
        set kp = GetOwningPlayer(killer)
        set th = Ninja_GetTrueHero(kp)
        if GetUnitAbilityLevel(killer, 'A011') > 0 or (th != null and GetUnitAbilityLevel(th, 'A011') > 0) or GetUnitTypeId(killer) == 'u001' then
            call Ninja_SpawnClone(kp, deadX, deadY, deadFacing)
        endif
        set kp = null
        set th = null
    endif"""

r5 = """    // 4. 魔音同化 (A011) - 击杀单位生成伪英雄分身
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'H003' and not isFakeHero and not isIllusion and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u002' or GetUnitTypeId(killer) == 'u001') then
        set kp = GetOwningPlayer(killer)
        set th = Ninja_GetTrueHero(kp)
        if GetUnitAbilityLevel(killer, 'A011') > 0 or (th != null and GetUnitAbilityLevel(th, 'A011') > 0) or GetPlayerController(kp) == MAP_CONTROL_COMPUTER or GetUnitTypeId(killer) == 'u001' then
            call Ninja_SpawnClone(kp, deadX, deadY, deadFacing)
        endif
        set kp = null
        set th = null
    endif"""

assert t5 in content, "Target 5 not found"
content = content.replace(t5, r5, 1)
print("Applied replacement 5")

if is_crlf:
    content = content.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Successfully patched war3map.j")
