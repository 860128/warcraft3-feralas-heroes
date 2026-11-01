# -*- coding: utf-8 -*-
import os, sys

RAW_J = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\raw\war3map.j"
PAYLOAD_DIR = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload"
os.makedirs(PAYLOAD_DIR, exist_ok=True)
OUT_J = os.path.join(PAYLOAD_DIR, "war3map.j")

GLOBALS = '''    // [Dream Master globals]
    unit array udg_CapUnit
    player array udg_CapOrigOwner
    real array udg_CapDuration
    unit array udg_CapCaster
    boolean array udg_CapIsHero
    boolean array udg_CapAghBuff
    integer udg_CapCount = 0
    group udg_EnumGroup = null
    group udg_CloneHeroGroup = null
    group udg_AghCloneGroup = null
    group udg_MirrorGroup = null
    unit array udg_DM_Hero
    boolean array udg_DM_Backstab
    integer udg_DM_HeroCount = 0
'''

FUNCTIONS = '''//===========================================================================
// Dream Master System Implementation
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
        set udg_DM_Backstab[udg_DM_HeroCount] = false
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
        set udg_CapCaster[idx] = udg_CapCaster[udg_CapCount - 1]
        set udg_CapIsHero[idx] = udg_CapIsHero[udg_CapCount - 1]
        set udg_CapAghBuff[idx] = udg_CapAghBuff[udg_CapCount - 1]
        set udg_CapUnit[udg_CapCount - 1] = null
        set udg_CapOrigOwner[udg_CapCount - 1] = null
        set udg_CapCaster[udg_CapCount - 1] = null
        set udg_CapCount = udg_CapCount - 1
    endif
endfunction

function DM_RestoreControl takes integer idx returns nothing
    local unit u = udg_CapUnit[idx]
    local player p = udg_CapOrigOwner[idx]
    if u != null and p != null then
        call SetUnitOwner(u, p, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DispelMagic\\\\DispelMagicTarget.mdl", u, "origin"))
    endif
    call DM_RemoveCapIndex(idx)
    set u = null
    set p = null
endfunction

function DM_CastMirrorImage takes unit caster returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A001')
    local integer hIdx = DM_GetHeroIndex(caster)
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    call UnitAddAbility(caster, 'A00W')
    call SetUnitAbilityLevel(caster, 'A00W', lv)
    call IssueImmediateOrder(caster, "windwalk")
    
    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\WindWalk\\\\WindWalkTarget.mdl", GetUnitX(caster), GetUnitY(caster)))
    
    if hasAgh and hIdx >= 0 then
        call SetUnitMoveSpeed(caster, 522.0)
        set udg_DM_Backstab[hIdx] = true
    endif
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
        set dur = 600.0
    endif
    
    set idx = DM_FindCapIndex(target)
    if idx >= 0 then
        set udg_CapDuration[idx] = dur
        set udg_CapCaster[idx] = caster
        set udg_CapAghBuff[idx] = hasAgh
        return
    endif
    
    if udg_CapCount < 128 then
        set udg_CapUnit[udg_CapCount] = target
        set udg_CapOrigOwner[udg_CapCount] = origPlayer
        set udg_CapDuration[udg_CapCount] = dur
        set udg_CapCaster[udg_CapCount] = caster
        set udg_CapIsHero[udg_CapCount] = IsUnitType(target, UNIT_TYPE_HERO)
        set udg_CapAghBuff[udg_CapCount] = hasAgh
        set udg_CapCount = udg_CapCount + 1
        
        call SetUnitOwner(target, casterPlayer, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Possession\\\\PossessionTarget.mdl", target, "overhead"))
        
        if hasAgh and not IsUnitType(target, UNIT_TYPE_STRUCTURE) then
            call SetUnitMoveSpeed(target, GetUnitMoveSpeed(target) * 1.40)
        endif
    endif
endfunction

function DM_CastMassIllusion takes unit caster, real cx, real cy returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A003')
    local player p = GetOwningPlayer(caster)
    local real radius = 250.0
    local unit t = null
    local unit clone = null
    local integer utid = 0
    local integer oldFood = 0
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    if lv == 2 then
        set radius = 350.0
    elseif lv >= 3 then
        set radius = 450.0
    endif
    
    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Other\\\\Silence\\\\SilenceAreaBirth.mdl", cx, cy))
    
    call GroupEnumUnitsInRange(udg_EnumGroup, cx, cy, radius, null)
    loop
        set t = FirstOfGroup(udg_EnumGroup)
        exitwhen t == null
        call GroupRemoveUnit(udg_EnumGroup, t)
        
        if GetUnitState(t, UNIT_STATE_LIFE) > 0.405 and not IsUnitType(t, UNIT_TYPE_STRUCTURE) and not IsUnitType(t, UNIT_TYPE_DEAD) then
            set utid = GetUnitTypeId(t)
            
            set oldFood = GetPlayerState(p, PLAYER_STATE_RESOURCE_FOOD_USED)
            set clone = CreateUnit(p, utid, GetUnitX(t), GetUnitY(t), GetUnitFacing(t))
            call SetPlayerState(p, PLAYER_STATE_RESOURCE_FOOD_USED, oldFood)
            
            if clone != null then
                call UnitApplyTimedLife(clone, 'BTLF', 900.0)
                call UnitAddType(clone, UNIT_TYPE_SUMMONED)
                
                call SetUnitVertexColor(clone, 90, 130, 255, 175)
                call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", GetUnitX(clone), GetUnitY(clone)))
                
                if IsUnitType(t, UNIT_TYPE_HERO) then
                    call SetHeroLevel(clone, GetHeroLevel(t), false)
                    call GroupAddUnit(udg_CloneHeroGroup, clone)
                endif
                
                if hasAgh then
                    call GroupAddUnit(udg_AghCloneGroup, clone)
                endif
            endif
            
            if hasAgh and IsUnitEnemy(t, p) then
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Sleep\\\\SleepTarget.mdl", t, "overhead"))
            endif
        endif
    endloop
    
    set t = null
    set clone = null
endfunction

function DM_OnSpellEffect takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer abil = GetSpellAbilityId()
    
    if abil == 'A001' then
        call DM_CastMirrorImage(caster)
    elseif abil == 'A002' then
        call DM_CastPossession(caster, GetSpellTargetUnit())
    elseif abil == 'A003' then
        call DM_CastMassIllusion(caster, GetSpellTargetX(), GetSpellTargetY())
    endif
    
    set caster = null
    return false
endfunction

function DM_OnDamaged takes nothing returns boolean
    local unit victim = GetTriggerUnit()
    local unit attacker = GetEventDamageSource()
    local real dmg = GetEventDamage()
    local integer idx = 0
    local integer hIdx = 0
    
    set idx = DM_FindCapIndex(victim)
    if idx >= 0 then
        if dmg >= GetWidgetLife(victim) then
            call DM_RestoreControl(idx)
        endif
    endif
    
    set hIdx = DM_GetHeroIndex(attacker)
    if hIdx >= 0 and udg_DM_Backstab[hIdx] then
        set udg_DM_Backstab[hIdx] = false
        call UnitDamageTarget(attacker, victim, 200.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_MAGIC, WEAPON_TYPE_WHOKNOWS)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\ShadowHunter\\\\ShadowHunterMissile.mdl", victim, "chest"))
    endif
    
    if IsUnitInGroup(attacker, udg_AghCloneGroup) and dmg > 0.0 then
        set hIdx = 0
        loop
            exitwhen hIdx >= udg_DM_HeroCount
            if GetOwningPlayer(udg_DM_Hero[hIdx]) == GetOwningPlayer(attacker) and GetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE) > 0.405 then
                call SetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE, GetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE) + dmg * 0.25)
            endif
            set hIdx = hIdx + 1
        endloop
    endif
    
    set victim = null
    set attacker = null
    return false
endfunction

function DM_OnDeath takes nothing returns boolean
    local unit dying = GetDyingUnit()
    local unit killer = GetKillingUnit()
    local integer idx = 0
    
    set idx = DM_FindCapIndex(dying)
    if idx >= 0 then
        call DM_RestoreControl(idx)
    endif
    
    if IsUnitInGroup(dying, udg_CloneHeroGroup) then
        call GroupRemoveUnit(udg_CloneHeroGroup, dying)
        call RemoveUnit(dying)
    endif
    
    if killer != null then
        set idx = DM_FindCapIndex(killer)
        if idx >= 0 and udg_CapAghBuff[idx] then
            set udg_CapDuration[idx] = udg_CapDuration[idx] + 15.0
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Bloodlust\\\\BloodlustTarget.mdl", killer, "origin"))
        endif
    endif
    
    set dying = null
    set killer = null
    return false
endfunction

function DM_PeriodicLoop takes nothing returns nothing
    local integer i = udg_CapCount - 1
    local unit u = null
    local real maxHP = 0.0
    
    loop
        exitwhen i < 0
        set u = udg_CapUnit[i]
        
        if u == null or GetUnitState(u, UNIT_STATE_LIFE) <= 0.405 then
            call DM_RestoreControl(i)
        else
            set udg_CapDuration[i] = udg_CapDuration[i] - 1.0
            
            if udg_CapAghBuff[i] and not IsUnitType(u, UNIT_TYPE_STRUCTURE) then
                set maxHP = GetUnitState(u, UNIT_STATE_MAX_LIFE)
                call SetUnitState(u, UNIT_STATE_LIFE, GetUnitState(u, UNIT_STATE_LIFE) + maxHP * 0.03)
            endif
            
            if udg_CapDuration[i] <= 0.0 then
                call DM_RestoreControl(i)
            endif
        endif
        
        set i = i - 1
    endloop
    set u = null
endfunction

function Init_DreamMasterSystem takes nothing returns nothing
    local trigger tSpell = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local timer tTimer = CreateTimer()
    local integer i = 0
    
    set udg_EnumGroup = CreateGroup()
    set udg_CloneHeroGroup = CreateGroup()
    set udg_AghCloneGroup = CreateGroup()
    set udg_MirrorGroup = CreateGroup()
    
    loop
        exitwhen i >= 16
        call TriggerRegisterPlayerUnitEvent(tSpell, Player(i), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
        call TriggerRegisterPlayerUnitEvent(tDamage, Player(i), EVENT_PLAYER_UNIT_DAMAGED, null)
        call TriggerRegisterPlayerUnitEvent(tDeath, Player(i), EVENT_PLAYER_UNIT_DEATH, null)
        set i = i + 1
    endloop
    
    call TriggerRegisterPlayerUnitEvent(tSpell, Player(24), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
    call TriggerRegisterPlayerUnitEvent(tDamage, Player(24), EVENT_PLAYER_UNIT_DAMAGED, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(24), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tSpell, Player(25), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
    call TriggerRegisterPlayerUnitEvent(tDamage, Player(25), EVENT_PLAYER_UNIT_DAMAGED, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(25), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(26), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(27), EVENT_PLAYER_UNIT_DEATH, null)
    
    call TriggerAddCondition(tSpell, Condition(function DM_OnSpellEffect))
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))
    call TriggerAddCondition(tDeath, Condition(function DM_OnDeath))
    
    call TimerStart(tTimer, 1.00, true, function DM_PeriodicLoop)
endfunction

'''

# Read raw script
with open(RAW_J, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

# 1. Insert globals
pos_endglobals = text.find("endglobals")
if pos_endglobals == -1:
    raise ValueError("endglobals not found")
text = text[:pos_endglobals] + GLOBALS + text[pos_endglobals:]

# 2. Insert functions before function main
pos_main = text.find("function main takes nothing returns nothing")
if pos_main == -1:
    raise ValueError("function main not found")
text = text[:pos_main] + FUNCTIONS + text[pos_main:]

# 3. Add call Init_DreamMasterSystem() inside main
pos_main = text.find("function main takes nothing returns nothing")
pos_endmain = text.find("endfunction", pos_main)
if pos_endmain == -1:
    raise ValueError("endfunction for main not found")

init_call = "    call Init_DreamMasterSystem()\n"
text = text[:pos_endmain] + init_call + text[pos_endmain:]

# Write to payload
with open(OUT_J, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(text)

print(f"[ok] payload/war3map.j written: {len(text)} bytes, {len(text.splitlines())} lines")
