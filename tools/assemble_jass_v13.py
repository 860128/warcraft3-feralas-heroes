import os, subprocess

with open("raw/war3map.j", "r", encoding="utf-8", errors="ignore") as f:
    orig_jass = f.read()

globals_extra = """
    // Dream Master globals
    unit array udg_CapUnit
    player array udg_CapOrigOwner
    real array udg_CapDuration
    integer udg_CapCount = 0

    unit array udg_DM_StealthUnit
    real array udg_DM_StealthTimer
    integer udg_DM_StealthCount = 0

    unit array udg_DM_Hero
    boolean array udg_DM_InStealth
    boolean array udg_DM_Backstab
    real array udg_DM_StealthDuration
    integer udg_DM_HeroCount = 0

    group udg_EnumGroup = null
"""

funcs_extra = """
//===========================================================================
// Dream Master (幻梦大师) v1.3 Core System
//===========================================================================

function DM_GetHeroIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_DM_HeroCount
        if udg_DM_Hero[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    if udg_DM_HeroCount < 32 then
        set udg_DM_Hero[udg_DM_HeroCount] = u
        set udg_DM_InStealth[udg_DM_HeroCount] = false
        set udg_DM_Backstab[udg_DM_HeroCount] = false
        set udg_DM_StealthDuration[udg_DM_HeroCount] = 0.0
        set udg_DM_HeroCount = udg_DM_HeroCount + 1
        return udg_DM_HeroCount - 1
    endif
    return -1
endfunction

function DM_FindCapIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_CapCount
        if udg_CapUnit[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    return -1
endfunction

function DM_RemoveCapIndex takes integer idx returns nothing
    if idx >= 0 and idx < udg_CapCount then
        set udg_CapUnit[idx] = udg_CapUnit[udg_CapCount - 1]
        set udg_CapOrigOwner[idx] = udg_CapOrigOwner[udg_CapCount - 1]
        set udg_CapDuration[idx] = udg_CapDuration[udg_CapCount - 1]
        set udg_CapUnit[udg_CapCount - 1] = null
        set udg_CapOrigOwner[udg_CapCount - 1] = null
        set udg_CapCount = udg_CapCount - 1
    endif
endfunction

function DM_BreakInvisibility takes unit hero, unit victim returns nothing
    local integer hIdx = DM_GetHeroIndex(hero)
    local integer lv = 1
    local boolean hasAgh = false
    local real dmg = 60.0

    if hIdx < 0 or not udg_DM_InStealth[hIdx] then
        return
    endif

    set udg_DM_InStealth[hIdx] = false
    call UnitRemoveBuffBJ('Binv', hero)
    call SetUnitVertexColor(hero, 255, 255, 255, 255)
    call SetUnitMoveSpeed(hero, 320.0)

    if victim != null and udg_DM_Backstab[hIdx] then
        set udg_DM_Backstab[hIdx] = false
        set lv = GetUnitAbilityLevel(hero, 'A001')
        set hasAgh = GetUnitAbilityLevel(hero, 'A004') > 0
        if lv == 2 then
            set dmg = 100.0
        elseif lv >= 3 then
            set dmg = 150.0
        endif
        if hasAgh then
            set dmg = dmg + 100.0
        endif

        call UnitDamageTarget(hero, victim, dmg, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_NORMAL, WEAPON_TYPE_WHOKNOWS)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\WindWalk\\\\WindWalkTarget.mdl", victim, "chest"))
    endif
endfunction

function DM_StealthLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    local player p = null
    local unit dummy = null
    local integer hIdx = -1
    local boolean hasAgh = false
    local integer lv = 1
    local real dur = 30.0

    // 1. Process pending stealth queue
    set i = 0
    loop
        exitwhen i >= udg_DM_StealthCount
        set udg_DM_StealthTimer[i] = udg_DM_StealthTimer[i] - 0.05
        if udg_DM_StealthTimer[i] <= 0.0 then
            set u = udg_DM_StealthUnit[i]
            set udg_DM_StealthUnit[i] = udg_DM_StealthUnit[udg_DM_StealthCount - 1]
            set udg_DM_StealthTimer[i] = udg_DM_StealthTimer[udg_DM_StealthCount - 1]
            set udg_DM_StealthUnit[udg_DM_StealthCount - 1] = null
            set udg_DM_StealthCount = udg_DM_StealthCount - 1
            set i = i - 1

            if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) then
                set p = GetOwningPlayer(u)
                set dummy = CreateUnit(p, 'u000', GetUnitX(u), GetUnitY(u), 0.0)
                call UnitAddAbility(dummy, 'A00V')
                call IssueTargetOrder(dummy, "invisibility", u)
                call UnitApplyTimedLife(dummy, 'BTLF', 1.0)
                set dummy = null
                set p = null

                call SetUnitVertexColor(u, 130, 150, 255, 120)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\WindWalk\\\\WindWalkTarget.mdl", u, "origin"))

                set hIdx = DM_GetHeroIndex(u)
                set hasAgh = GetUnitAbilityLevel(u, 'A004') > 0
                set lv = GetUnitAbilityLevel(u, 'A001')
                set dur = 30.0 + I2R(lv) * 5.0

                if hasAgh then
                    call SetUnitMoveSpeed(u, 522.0)
                else
                    call SetUnitMoveSpeed(u, 400.0)
                endif

                if hIdx >= 0 then
                    set udg_DM_InStealth[hIdx] = true
                    set udg_DM_Backstab[hIdx] = true
                    set udg_DM_StealthDuration[hIdx] = dur
                endif
            endif
            set u = null
        endif
        set i = i + 1
    endloop

    // 2. Check active stealth duration
    set i = 0
    loop
        exitwhen i >= udg_DM_HeroCount
        if udg_DM_InStealth[i] then
            set udg_DM_StealthDuration[i] = udg_DM_StealthDuration[i] - 0.05
            if udg_DM_StealthDuration[i] <= 0.0 or IsUnitType(udg_DM_Hero[i], UNIT_TYPE_DEAD) then
                call DM_BreakInvisibility(udg_DM_Hero[i], null)
            endif
        endif
        set i = i + 1
    endloop
endfunction

function DM_CapTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    loop
        exitwhen i >= udg_CapCount
        set udg_CapDuration[i] = udg_CapDuration[i] - 1.0
        set u = udg_CapUnit[i]
        if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
            if u != null and udg_CapOrigOwner[i] != null then
                call SetUnitOwner(u, udg_CapOrigOwner[i], true)
            endif
            call DM_RemoveCapIndex(i)
            set i = i - 1
        elseif udg_CapDuration[i] <= 0.0 then
            call SetUnitOwner(u, udg_CapOrigOwner[i], true)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", u, "origin"))
            call DM_RemoveCapIndex(i)
            set i = i - 1
        endif
        set u = null
        set i = i + 1
    endloop
endfunction

function DM_CloneOneUnit takes unit caster, unit orig, real tx, real ty returns nothing
    local player p = GetOwningPlayer(caster)
    local integer uId = GetUnitTypeId(orig)
    local unit clone = null
    local unit dummy = null
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0

    if IsUnitType(orig, UNIT_TYPE_HERO) then
        // Hero target: create engine-native Hero Phantom via Wand of Illusion (852274)
        // Ensures: NO left-bar hero icon, NEVER revivable at Altar, NEVER splits Hero XP!
        set dummy = CreateUnit(p, 'u000', GetUnitX(orig), GetUnitY(orig), 0.0)
        if hasAgh then
            call UnitAddAbility(dummy, 'A00J')
        else
            call UnitAddAbility(dummy, 'A00I')
        endif
        call IssueTargetOrderById(dummy, 852274, orig)
        call UnitApplyTimedLife(dummy, 'BTLF', 2.0)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", orig, "origin"))
        set dummy = null
    else
        // Non-hero target (includes Peasants, Peons, Wisps, Acolytes, Creeps, Spellcasters):
        // Clone with full active skills, 15-minute duration, blue illusion tint
        set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
        call UnitAddType(clone, UNIT_TYPE_SUMMONED)
        call UnitApplyTimedLife(clone, 'BTLF', 900.0)
        call SetUnitVertexColor(clone, 100, 150, 255, 180)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
        set clone = null
    endif

    set p = null
endfunction

function DM_CastMassIllusion takes unit caster, real targetX, real targetY returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A003')
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    local real radius = 250.0
    local unit enumU = null
    local real ox = 0.0
    local real oy = 0.0
    local real spawnX = 0.0
    local real spawnY = 0.0

    if lv == 2 then
        set radius = 350.0
    elseif lv >= 3 then
        set radius = 450.0
    endif
    if hasAgh then
        set radius = radius + 100.0
    endif

    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\MassTeleport\\\\MassTeleportTarget.mdl", targetX, targetY))

    call GroupClear(udg_EnumGroup)
    call GroupEnumUnitsInRange(udg_EnumGroup, targetX, targetY, radius, null)

    loop
        set enumU = FirstOfGroup(udg_EnumGroup)
        exitwhen enumU == null
        call GroupRemoveUnit(udg_EnumGroup, enumU)

        // Copy ALL living non-structure units (including peasants, wisps, peons, acolytes, creeps, heroes)
        if not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
            set ox = GetUnitX(enumU)
            set oy = GetUnitY(enumU)
            set spawnX = ox + 40.0
            set spawnY = oy + 40.0
            call DM_CloneOneUnit(caster, enumU, spawnX, spawnY)
        endif
    endloop
endfunction

function DM_CastPossession takes unit caster, unit target returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A002')
    local player casterPlayer = GetOwningPlayer(caster)
    local player origPlayer = GetOwningPlayer(target)
    local real dur = 30.0
    local integer idx = 0
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0

    if target == null or origPlayer == casterPlayer then
        return
    endif

    if lv == 2 then
        set dur = 120.0
    elseif lv >= 3 then
        if hasAgh then
            set dur = 999999.0
        else
            set dur = 600.0
        endif
    endif

    set idx = DM_FindCapIndex(target)
    if idx >= 0 then
        set udg_CapDuration[idx] = dur
    else
        if udg_CapCount < 128 then
            set udg_CapUnit[udg_CapCount] = target
            set udg_CapOrigOwner[udg_CapCount] = origPlayer
            set udg_CapDuration[udg_CapCount] = dur
            set udg_CapCount = udg_CapCount + 1
        endif
    endif

    call SetUnitOwner(target, casterPlayer, true)
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Possession\\\\PossessionTarget.mdl", target, "chest"))

    set casterPlayer = null
    set origPlayer = null
endfunction

function DM_OnCastMirror takes unit caster returns nothing
    if udg_DM_StealthCount < 32 then
        set udg_DM_StealthUnit[udg_DM_StealthCount] = caster
        set udg_DM_StealthTimer[udg_DM_StealthCount] = 0.40
        set udg_DM_StealthCount = udg_DM_StealthCount + 1
    endif
endfunction

function DM_OnSpellEffect takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer abil = GetSpellAbilityId()

    if abil == 'A001' then
        call DM_OnCastMirror(caster)
    elseif abil == 'A002' then
        call DM_CastPossession(caster, GetSpellTargetUnit())
    elseif abil == 'A003' then
        call DM_CastMassIllusion(caster, GetSpellTargetX(), GetSpellTargetY())
    endif

    set caster = null
    return false
endfunction

function DM_OnSpellCast takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer hIdx = DM_GetHeroIndex(caster)
    if hIdx >= 0 and udg_DM_InStealth[hIdx] then
        if GetSpellAbilityId() != 'A001' then
            call DM_BreakInvisibility(caster, null)
        endif
    endif
    set caster = null
    return false
endfunction

function DM_OnDamaged takes nothing returns boolean
    local unit src = GetEventDamageSource()
    local unit tgt = GetTriggerUnit()
    local integer hIdx = -1
    if src != null and tgt != null and GetEventDamage() > 0.0 then
        set hIdx = DM_GetHeroIndex(src)
        if hIdx >= 0 and udg_DM_InStealth[hIdx] then
            call DM_BreakInvisibility(src, tgt)
        endif
    endif
    set src = null
    set tgt = null
    return false
endfunction

function DM_OnUnitDeath takes nothing returns boolean
    local unit dead = GetTriggerUnit()
    local integer idx = DM_FindCapIndex(dead)
    if idx >= 0 then
        call SetUnitOwner(dead, udg_CapOrigOwner[idx], true)
        call DM_RemoveCapIndex(idx)
    endif
    set dead = null
    return false
endfunction

function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()

    set udg_EnumGroup = CreateGroup()

    call TriggerRegisterAnyUnitEventBJ(tEffect, EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddCondition(tEffect, Condition(function DM_OnSpellEffect))

    call TriggerRegisterAnyUnitEventBJ(tCast, EVENT_PLAYER_UNIT_SPELL_CAST)
    call TriggerAddCondition(tCast, Condition(function DM_OnSpellCast))

    call TriggerRegisterAnyUnitEventBJ(tDeath, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddCondition(tDeath, Condition(function DM_OnUnitDeath))

    call TriggerRegisterAnyUnitEventBJ(tDamage, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tmrCap = null
    set tmrStealth = null
endfunction

function CreateTestHero takes nothing returns nothing
    local location loc = GetStartLocationLoc(GetPlayerStartLocation(Player(0)))
    local real x = GetLocationX(loc) + 150.0
    local real y = GetLocationY(loc) - 150.0
    local unit hero = CreateUnit(Player(0), 'H002', x, y, 270.0)
    call SetHeroLevel(hero, 10, true)
    call RemoveLocation(loc)
    set loc = null
    set hero = null
endfunction
"""

endglobals_idx = orig_jass.find("endglobals")
jass_mod = orig_jass[:endglobals_idx] + globals_extra + orig_jass[endglobals_idx:]

main_idx = jass_mod.find("function main takes nothing returns nothing")
jass_mod = jass_mod[:main_idx] + funcs_extra + "\n" + jass_mod[main_idx:]

main_start = jass_mod.find("function main takes nothing returns nothing")
main_body_idx = jass_mod.find("\n", main_start) + 1
main_calls = """    call DM_InitTriggers()
    call CreateTestHero()
"""
jass_mod = jass_mod[:main_body_idx] + main_calls + jass_mod[main_body_idx:]

with open("payload/war3map.j", "w", encoding="utf-8") as f:
    f.write(jass_mod)

print("payload/war3map.j written. Length:", len(jass_mod))
