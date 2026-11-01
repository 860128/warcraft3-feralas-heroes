import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JASS_PATH = os.path.join(ROOT, "payload", "war3map.j")

with open(JASS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Globals: Add udg_KarmaFx
old_globals = """    unit array udg_KarmaUnit
    player array udg_KarmaOwner
    integer array udg_KarmaLevel
    integer udg_KarmaCount = 0"""

new_globals = """    unit array udg_KarmaUnit
    player array udg_KarmaOwner
    integer array udg_KarmaLevel
    effect array udg_KarmaFx
    integer udg_KarmaCount = 0"""

assert old_globals in content, "old_globals not found in war3map.j"
content = content.replace(old_globals, new_globals, 1)

# 2. Ninja_SpawnClone: Add A015 evasion ability based on true hero's A011 level
old_spawn = """    set clone = CreateUnit(p, 'u002', x, y, facing)
    call UnitAddType(clone, UNIT_TYPE_SUMMONED)

    if trueHero != null then"""

new_spawn = """    set clone = CreateUnit(p, 'u002', x, y, facing)
    call UnitAddType(clone, UNIT_TYPE_SUMMONED)

    if trueHero != null and lv > 0 then
        call UnitAddAbility(clone, 'A015')
        call SetUnitAbilityLevel(clone, 'A015', lv)
    endif

    if trueHero != null then"""

assert old_spawn in content, "old_spawn not found in war3map.j"
content = content.replace(old_spawn, new_spawn, 1)

# 3. Ninja_RemoveKarmaIndex & Ninja_MarkKarma
old_karma_funcs = """function Ninja_RemoveKarmaIndex takes integer idx returns nothing
    if idx >= 0 and idx < udg_KarmaCount then
        set udg_KarmaUnit[idx] = udg_KarmaUnit[udg_KarmaCount - 1]
        set udg_KarmaOwner[idx] = udg_KarmaOwner[udg_KarmaCount - 1]
        set udg_KarmaLevel[idx] = udg_KarmaLevel[udg_KarmaCount - 1]
        set udg_KarmaUnit[udg_KarmaCount - 1] = null
        set udg_KarmaOwner[udg_KarmaCount - 1] = null
        set udg_KarmaCount = udg_KarmaCount - 1
    endif
endfunction

function Ninja_MarkKarma takes unit killer, player ninjaOwner, integer lv returns nothing
    local integer idx = -1
    if killer == null or IsUnitType(killer, UNIT_TYPE_STRUCTURE) or GetUnitTypeId(killer) == 'u000' then
        return
    endif
    set idx = Ninja_FindKarmaIndex(killer)
    if idx >= 0 then
        set udg_KarmaOwner[idx] = ninjaOwner
        if lv > udg_KarmaLevel[idx] then
            set udg_KarmaLevel[idx] = lv
        endif
    else
        if udg_KarmaCount < 128 then
            set udg_KarmaUnit[udg_KarmaCount] = killer
            set udg_KarmaOwner[udg_KarmaCount] = ninjaOwner
            set udg_KarmaLevel[udg_KarmaCount] = lv
            set udg_KarmaCount = udg_KarmaCount + 1
        endif
    endif
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Curse\\\\CurseTarget.mdl", killer, "overhead"))
endfunction"""

new_karma_funcs = """function Ninja_RemoveKarmaIndex takes integer idx returns nothing
    if idx >= 0 and idx < udg_KarmaCount then
        if udg_KarmaFx[idx] != null then
            call DestroyEffect(udg_KarmaFx[idx])
            set udg_KarmaFx[idx] = null
        endif
        if udg_KarmaUnit[idx] != null then
            call SetUnitVertexColor(udg_KarmaUnit[idx], 255, 255, 255, 255)
        endif
        set udg_KarmaUnit[idx] = udg_KarmaUnit[udg_KarmaCount - 1]
        set udg_KarmaOwner[idx] = udg_KarmaOwner[udg_KarmaCount - 1]
        set udg_KarmaLevel[idx] = udg_KarmaLevel[udg_KarmaCount - 1]
        set udg_KarmaFx[idx] = udg_KarmaFx[udg_KarmaCount - 1]
        set udg_KarmaUnit[udg_KarmaCount - 1] = null
        set udg_KarmaOwner[udg_KarmaCount - 1] = null
        set udg_KarmaFx[udg_KarmaCount - 1] = null
        set udg_KarmaCount = udg_KarmaCount - 1
    endif
endfunction

function Ninja_MarkKarma takes unit killer, player ninjaOwner, integer lv returns nothing
    local integer idx = -1
    if killer == null or IsUnitType(killer, UNIT_TYPE_STRUCTURE) or GetUnitTypeId(killer) == 'u000' then
        return
    endif
    set idx = Ninja_FindKarmaIndex(killer)
    if idx >= 0 then
        set udg_KarmaOwner[idx] = ninjaOwner
        if lv > udg_KarmaLevel[idx] then
            set udg_KarmaLevel[idx] = lv
        endif
        if udg_KarmaFx[idx] == null then
            set udg_KarmaFx[idx] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Curse\\\\CurseTarget.mdl", killer, "overhead")
        endif
    else
        if udg_KarmaCount < 128 then
            set udg_KarmaUnit[udg_KarmaCount] = killer
            set udg_KarmaOwner[udg_KarmaCount] = ninjaOwner
            set udg_KarmaLevel[udg_KarmaCount] = lv
            set udg_KarmaFx[udg_KarmaCount] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Curse\\\\CurseTarget.mdl", killer, "overhead")
            set udg_KarmaCount = udg_KarmaCount + 1
        endif
    endif
    call SetUnitVertexColor(killer, 255, 140, 255, 255)
endfunction"""

assert old_karma_funcs in content, "old_karma_funcs not found in war3map.j"
content = content.replace(old_karma_funcs, new_karma_funcs, 1)

# 4. Ninja_OnHeroSkill: Auto-sync A015 level to existing living clones when A011 is learned
old_skill_func = """function Ninja_OnHeroSkill takes nothing returns boolean
    local unit hero = GetTriggerUnit()
    local integer pId = 0
    if GetUnitTypeId(hero) == 'H003' then
        set pId = GetPlayerId(GetOwningPlayer(hero))
        if not IsUnitInGroup(hero, udg_FakeHeroGroup) and not IsUnitIllusion(hero) then
            set udg_Ninja_TrueHero[pId] = hero
        endif
        if GetLearnedSkill() == 'A012' and GetUnitAbilityLevel(hero, 'A012') == 1 then
            set udg_Ninja_AuraOn[pId] = true
            if udg_Ninja_AuraFx[pId] == null then
                set udg_Ninja_AuraFx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", hero, "origin")
            endif
        endif
    endif
    set hero = null
    return false
endfunction"""

new_skill_func = """function Ninja_OnHeroSkill takes nothing returns boolean
    local unit hero = GetTriggerUnit()
    local integer pId = 0
    local group g = null
    local unit u = null
    local integer qLv = 0
    if GetUnitTypeId(hero) == 'H003' then
        set pId = GetPlayerId(GetOwningPlayer(hero))
        if not IsUnitInGroup(hero, udg_FakeHeroGroup) and not IsUnitIllusion(hero) then
            set udg_Ninja_TrueHero[pId] = hero
        endif
        if GetLearnedSkill() == 'A012' and GetUnitAbilityLevel(hero, 'A012') == 1 then
            set udg_Ninja_AuraOn[pId] = true
            if udg_Ninja_AuraFx[pId] == null then
                set udg_Ninja_AuraFx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", hero, "origin")
            endif
        endif
        if GetLearnedSkill() == 'A011' then
            set qLv = GetUnitAbilityLevel(hero, 'A011')
            if qLv > 0 and udg_Ninja_CloneGroup[pId] != null then
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
                        call SetUnitAbilityLevel(u, 'A015', qLv)
                    endif
                endloop
                call DestroyGroup(g)
                set g = null
            endif
        endif
    endif
    set hero = null
    return false
endfunction"""

assert old_skill_func in content, "old_skill_func not found in war3map.j"
content = content.replace(old_skill_func, new_skill_func, 1)

# 5. DM_CapTimerLoop: Add karma periodic drain loop
old_captimer = """function DM_CapTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local integer pId = 0
    local unit th = null
    local unit dmgSrc = null
    local integer aLv = 0
    local real pct = 0.0
    local real drain = 0.0
    local unit enumU = null"""

new_captimer = """function DM_CapTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local integer pId = 0
    local unit th = null
    local unit dmgSrc = null
    local integer aLv = 0
    local real pct = 0.0
    local real drain = 0.0
    local unit enumU = null
    local integer kLv = 0
    local player ko = null"""

assert old_captimer in content, "old_captimer not found in war3map.j"
content = content.replace(old_captimer, new_captimer, 1)

old_captimer_end = """        endif
        set pId = pId + 1
    endloop
endfunction"""

new_captimer_end = """        endif
        set pId = pId + 1
    endloop

    // 3. Process Karma Curse Drain (A013 Lv2 & Lv3)
    set i = 0
    loop
        exitwhen i >= udg_KarmaCount
        set u = udg_KarmaUnit[i]
        if u == null or IsUnitType(u, UNIT_TYPE_DEAD) or GetWidgetLife(u) <= 0.405 then
            call Ninja_RemoveKarmaIndex(i)
            set i = i - 1
        else
            set kLv = udg_KarmaLevel[i]
            if kLv >= 2 then
                if kLv == 2 then
                    set pct = 0.01
                else
                    set pct = 0.02
                endif
                set drain = GetUnitState(u, UNIT_STATE_MAX_LIFE) * pct
                if GetWidgetLife(u) > (drain + 1.0) then
                    call SetWidgetLife(u, GetWidgetLife(u) - drain)
                else
                    set ko = udg_KarmaOwner[i]
                    set dmgSrc = Ninja_GetTrueHero(ko)
                    if dmgSrc == null or IsUnitType(dmgSrc, UNIT_TYPE_DEAD) then
                        set dmgSrc = Ninja_PickLivingClone(GetPlayerId(ko))
                    endif
                    if dmgSrc == null then
                        set dmgSrc = u
                    endif
                    call UnitDamageTarget(dmgSrc, u, drain + 100.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_UNIVERSAL, WEAPON_TYPE_WHOKNOWS)
                    if i < udg_KarmaCount and udg_KarmaUnit[i] != u then
                        set i = i - 1
                    endif
                endif
            endif
        endif
        set u = null
        set i = i + 1
    endloop
endfunction"""

assert old_captimer_end in content, "old_captimer_end not found in war3map.j"
content = content.replace(old_captimer_end, new_captimer_end, 1)

# 6. DM_OnUnitDeath: Add hasLivingNinja, support u001 marking karma, and reincarnate True Hero if no ninja is alive
old_death_locals = """function DM_OnUnitDeath takes nothing returns boolean
    local unit dead = GetTriggerUnit()
    local unit killer = GetKillingUnit()
    local player deadOwner = GetOwningPlayer(dead)
    local integer deadPId = GetPlayerId(deadOwner)
    local integer deadType = GetUnitTypeId(dead)
    local real deadX = GetUnitX(dead)
    local real deadY = GetUnitY(dead)
    local real deadFacing = GetUnitFacing(dead)
    local boolean isFakeHero = IsUnitInGroup(dead, udg_FakeHeroGroup)
    local boolean isIllusion = IsUnitIllusion(dead)
    local integer idx = -1
    local integer kIdx = -1
    local player ko = null
    local integer klv = 0
    local player kp = null
    local unit th = null
    local integer eLv = 0
    local unit c = null
    local real nx = 0.0
    local real ny = 0.0
    local real nhp = 0.0"""

new_death_locals = """function DM_OnUnitDeath takes nothing returns boolean
    local unit dead = GetTriggerUnit()
    local unit killer = GetKillingUnit()
    local player deadOwner = GetOwningPlayer(dead)
    local integer deadPId = GetPlayerId(deadOwner)
    local integer deadType = GetUnitTypeId(dead)
    local real deadX = GetUnitX(dead)
    local real deadY = GetUnitY(dead)
    local real deadFacing = GetUnitFacing(dead)
    local boolean isFakeHero = IsUnitInGroup(dead, udg_FakeHeroGroup)
    local boolean isIllusion = IsUnitIllusion(dead)
    local integer idx = -1
    local integer kIdx = -1
    local player ko = null
    local integer klv = 0
    local boolean hasLivingNinja = false
    local player kp = null
    local unit th = null
    local integer eLv = 0
    local unit c = null
    local real nx = 0.0
    local real ny = 0.0
    local real nhp = 0.0"""

assert old_death_locals in content, "old_death_locals not found in war3map.j"
content = content.replace(old_death_locals, new_death_locals, 1)

old_death_body = """    // 2. 他化自在 (A013) - 击杀魔音忍者者被烙印因果
    if (deadType == 'H003' or deadType == 'u002') and killer != null and IsUnitEnemy(killer, deadOwner) then
        set th = Ninja_GetTrueHero(deadOwner)
        set eLv = GetUnitAbilityLevel(dead, 'A013')
        if th != null and GetUnitAbilityLevel(th, 'A013') > eLv then
            set eLv = GetUnitAbilityLevel(th, 'A013')
        endif
        if eLv > 0 then
            call Ninja_MarkKarma(killer, deadOwner, eLv)
        endif
    endif

    // 3. 他化自在 (A013) - 因果单位死亡化为魔音忍者
    set kIdx = Ninja_FindKarmaIndex(dead)
    if kIdx >= 0 then
        set ko = udg_KarmaOwner[kIdx]
        set klv = udg_KarmaLevel[kIdx]
        call Ninja_RemoveKarmaIndex(kIdx)
        call Ninja_SpawnClone(ko, deadX, deadY, deadFacing)
        if klv >= 3 then
            call Ninja_SpawnClone(ko, deadX + 45.0, deadY + 45.0, deadFacing)
        endif
        set ko = null
    endif"""

new_death_body = """    // 2. 他化自在 (A013) - 击杀魔音忍者者被烙印因果
    if (deadType == 'H003' or deadType == 'u002' or deadType == 'u001') and killer != null and IsUnitEnemy(killer, deadOwner) then
        set th = Ninja_GetTrueHero(deadOwner)
        set eLv = GetUnitAbilityLevel(dead, 'A013')
        if th != null and GetUnitAbilityLevel(th, 'A013') > eLv then
            set eLv = GetUnitAbilityLevel(th, 'A013')
        endif
        if eLv > 0 then
            call Ninja_MarkKarma(killer, deadOwner, eLv)
        endif
    endif

    // 3. 他化自在 (A013) - 因果单位死亡化为魔音忍者
    set kIdx = Ninja_FindKarmaIndex(dead)
    if kIdx >= 0 then
        set ko = udg_KarmaOwner[kIdx]
        set klv = udg_KarmaLevel[kIdx]
        call Ninja_RemoveKarmaIndex(kIdx)

        set th = Ninja_GetTrueHero(ko)
        set hasLivingNinja = false
        if th != null and not IsUnitType(th, UNIT_TYPE_DEAD) and GetWidgetLife(th) > 0.405 then
            set hasLivingNinja = true
        elseif Ninja_PickLivingClone(GetPlayerId(ko)) != null then
            set hasLivingNinja = true
        endif

        if not hasLivingNinja and th != null then
            // 当前场上没有任何魔音忍者（本体和分身都没有）：直接从该怪物尸体处产生（复活）魔音忍者本尊！
            call ReviveHero(th, deadX, deadY, true)
            call SetUnitFacing(th, deadFacing)
            call SetWidgetLife(th, GetUnitState(th, UNIT_STATE_MAX_LIFE))
            call SetUnitState(th, UNIT_STATE_MANA, GetUnitState(th, UNIT_STATE_MAX_MANA))
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\NightElf\\\\Blink\\\\BlinkTarget.mdl", th, "origin"))
            if GetLocalPlayer() == ko then
                call SelectUnit(th, true)
            endif
        else
            // 场上仍有魔音忍者（本体或分身）：产生魔音忍者分身！
            call Ninja_SpawnClone(ko, deadX, deadY, deadFacing)
            if klv >= 3 then
                call Ninja_SpawnClone(ko, deadX + 45.0, deadY + 45.0, deadFacing)
            endif
        endif
        set ko = null
    endif"""

assert old_death_body in content, "old_death_body not found in war3map.j"
content = content.replace(old_death_body, new_death_body, 1)

# Cleanup fake hero / clone / ult
old_cleanup = """    // 6. Cleanup Fake Hero / Clone
    if isFakeHero or deadType == 'u002' then
        if udg_Ninja_CloneGroup[deadPId] != null then
            call GroupRemoveUnit(udg_Ninja_CloneGroup[deadPId], dead)
        endif
        call GroupRemoveUnit(udg_FakeHeroGroup, dead)
        call SetUnitOwner(dead, Player(PLAYER_NEUTRAL_PASSIVE), false)
        call SetUnitExploded(dead, true)
        call RemoveUnit(dead)
    endif"""

new_cleanup = """    // 6. Cleanup Fake Hero / Clone
    if isFakeHero or deadType == 'u002' or deadType == 'u001' then
        if udg_Ninja_CloneGroup[deadPId] != null then
            call GroupRemoveUnit(udg_Ninja_CloneGroup[deadPId], dead)
        endif
        call GroupRemoveUnit(udg_FakeHeroGroup, dead)
        if deadType == 'u002' then
            call SetUnitOwner(dead, Player(PLAYER_NEUTRAL_PASSIVE), false)
            call SetUnitExploded(dead, true)
            call RemoveUnit(dead)
        endif
    endif"""

assert old_cleanup in content, "old_cleanup not found in war3map.j"
content = content.replace(old_cleanup, new_cleanup, 1)

with open(JASS_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated payload/war3map.j with all v1.7 changes!")
