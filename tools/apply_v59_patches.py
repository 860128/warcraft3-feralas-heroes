# -*- coding: utf-8 -*-
import sys

def apply_patches():
    with open('payload/war3map.j', 'rb') as f:
        content = f.read().decode('utf-8')

    is_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    patches = []

    # 1. Globals: add udg_DM_CloneOrigList and udg_DM_CloneOrigIndex
    target_1 = """    button udg_TM_BtnMode5All = null
endglobals"""
    replacement_1 = """    button udg_TM_BtnMode5All = null
    unit array udg_DM_CloneOrigList
    integer udg_DM_CloneOrigIndex = 0
endglobals"""
    patches.append(("Globals", target_1, replacement_1))

    # 2. Remove Strain_OnUnitSummon from line ~4539
    target_2 = """function Strain_OnUnitSummon takes nothing returns boolean
    local unit summoned = GetSummonedUnit()
    local integer pId = 0
    local unit realHero = null

    if summoned != null and GetUnitTypeId(summoned) == 'H004' then
        set pId = GetPlayerId(GetOwningPlayer(summoned))
        call GroupAddUnit(udg_FakeHeroGroup, summoned)
        call Strain_ApplyCurrentSkin(summoned, pId)
        set realHero = Strain_GetRealHero(pId)
        if realHero != null and not udg_Strain_Burrowed[pId] and not udg_Strain_MimicActive[pId] then
            call Strain_ApplyCurrentSkin(realHero, pId)
        endif
    endif
    set summoned = null
    return false
endfunction"""
    replacement_2 = """// Strain_OnUnitSummon moved below line 9560 to integrate with DM_SyncClonedUnit"""
    patches.append(("Remove old Strain_OnUnitSummon", target_2, replacement_2))

    # 3. Add DM_FindMatchingOrig, DM_SyncClonedUnit, and new Strain_OnUnitSummon right before DM_CloneOneUnit
    target_3 = """function DM_CloneOneUnit takes unit caster, unit orig, real tx, real ty returns nothing"""
    replacement_3 = """function DM_FindMatchingOrig takes unit summoned returns unit
    local integer uId = GetUnitTypeId(summoned)
    local integer i = 0
    local integer bestIdx = -1
    local unit candidate = null
    local real minDist = 999999.0
    local real d = 0.0
    local unit best = null
    local real sx = GetUnitX(summoned)
    local real sy = GetUnitY(summoned)

    set i = 0
    loop
        exitwhen i >= 32
        set candidate = udg_DM_CloneOrigList[i]
        if candidate != null and GetUnitTypeId(candidate) == uId then
            set d = SquareRoot((GetUnitX(candidate) - sx) * (GetUnitX(candidate) - sx) + (GetUnitY(candidate) - sy) * (GetUnitY(candidate) - sy))
            if d < minDist then
                set minDist = d
                set best = candidate
                set bestIdx = i
            endif
        endif
        set i = i + 1
    endloop

    if bestIdx >= 0 then
        set udg_DM_CloneOrigList[bestIdx] = null
    endif

    return best
endfunction

function DM_SyncClonedUnit takes unit clone, unit orig returns nothing
    local integer origTypeId = 0
    local integer origSkin = 0
    local integer origPid = 0
    local integer evoStage = 0
    local real effScale = 1.0
    local real origRange = 0.0
    local string origMissile = ""

    if clone == null or orig == null then
        return
    endif

    set origTypeId = GetUnitTypeId(orig)
    set origPid = GetPlayerId(GetOwningPlayer(orig))

    // 1. Synchronize Appearance, Skin, Model, Scale, Flight
    if origTypeId == 'H006' then
        if origPid >= 0 and origPid <= 15 and udg_Maho_IsWinged[origPid] then
            call BlzSetUnitSkin(clone, 'nbal')
            call SetUnitScale(clone, 1.25, 1.25, 1.25)
            call UnitAddAbility(clone, 'Amrf')
            call UnitRemoveAbility(clone, 'Amrf')
            call SetUnitFlyHeight(clone, 240.0, 400.0)
            call SetUnitPathing(clone, false)
            call UnitAddAbility(clone, 'A045')
            call SetUnitAcquireRange(clone, 650.0)
        else
            call BlzSetUnitSkin(clone, 'H006')
            call SetUnitScale(clone, 1.25, 1.25, 1.25)
            call UnitAddAbility(clone, 'Amrf')
            call UnitRemoveAbility(clone, 'Amrf')
            call SetUnitFlyHeight(clone, 0.0, 400.0)
            call SetUnitPathing(clone, true)
            if origPid >= 0 and origPid <= 15 and udg_Maho_AntiAirUnlocked[origPid] then
                call UnitAddAbility(clone, 'A045')
                call SetUnitAcquireRange(clone, 650.0)
            endif
        endif
    elseif origTypeId == 'H004' then
        set evoStage = 0
        if origPid >= 0 and origPid <= 15 then
            set evoStage = udg_Strain_EvoStage[origPid]
        endif
        if evoStage == 0 then
            set origSkin = 'zzrg'
            set effScale = 1.15
        elseif evoStage == 1 then
            set origSkin = 'nano'
            set effScale = 1.30
        elseif evoStage == 2 then
            set origSkin = 'zhyd'
            set effScale = 1.40
        else
            set origSkin = 'Ucrl'
            set effScale = 1.65
        endif
        call BlzSetUnitSkin(clone, 'H004')
        call BlzSetUnitSkin(clone, origSkin)
        call SetUnitScale(clone, effScale, effScale, effScale)
        if evoStage == 2 then
            call BlzSetUnitWeaponRealField(clone, UNIT_WEAPON_RF_ATTACK_RANGE, 0, 500.0)
            call BlzSetUnitWeaponRealField(clone, UNIT_WEAPON_RF_ATTACK_RANGE, 1, 500.0)
            call BlzSetUnitWeaponRealField(clone, UNIT_WEAPON_RF_ATTACK_PROJECTILE_SPEED, 0, 1200.0)
            call BlzSetUnitWeaponStringField(clone, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0, "Abilities\\\\Weapons\\\\ChimaeraAcidMissile\\\\ChimaeraAcidMissile.mdl")
            call SetUnitAcquireRange(clone, 650.0)
        endif
    elseif origTypeId == 'H005' then
        if origPid >= 0 and origPid <= 15 and udg_Wild_IsMorphed[origPid] then
            set origSkin = udg_Wild_CurrentForm[origPid]
            if origSkin != 0 then
                call BlzSetUnitSkin(clone, origSkin)
                set effScale = Wild_GetCreepEffectiveScale(origSkin, GetHeroLevel(orig), 1.0)
                call SetUnitScale(clone, effScale, effScale, effScale)
                call Wild_ApplyFlight(clone, origSkin)
            endif
        else
            call BlzSetUnitSkin(clone, 'H005')
            call SetUnitScale(clone, 1.0, 1.0, 1.0)
            call Wild_ApplyFlight(clone, 'H005')
        endif
    else
        set origSkin = BlzGetUnitSkin(orig)
        if origSkin != 0 and origSkin != GetUnitTypeId(clone) then
            call BlzSetUnitSkin(clone, origSkin)
        endif
    endif

    // Mark as fake hero / illusion tracking
    call GroupAddUnit(udg_FakeHeroGroup, clone)

    // Preserve Illusion translucent bluish tint
    call SetUnitVertexColor(clone, 110, 165, 255, 195)

    // 2. Synchronize Max HP & Current HP
    call BlzSetUnitMaxHP(clone, BlzGetUnitMaxHP(orig))
    call SetWidgetLife(clone, GetWidgetLife(orig))

    // 3. Synchronize Max Mana & Current Mana
    if BlzGetUnitMaxMana(orig) > 0 then
        call BlzSetUnitMaxMana(clone, BlzGetUnitMaxMana(orig))
        call SetUnitState(clone, UNIT_STATE_MANA, GetUnitState(orig, UNIT_STATE_MANA))
    endif

    // 4. Synchronize Base Damage (Weapons 0 and 1)
    call BlzSetUnitBaseDamage(clone, BlzGetUnitBaseDamage(orig, 0), 0)
    call BlzSetUnitBaseDamage(clone, BlzGetUnitBaseDamage(orig, 1), 1)

    // 5. Synchronize Armor, Attack Cooldown, Move Speed
    call BlzSetUnitArmor(clone, BlzGetUnitArmor(orig))
    call BlzSetUnitAttackCooldown(clone, BlzGetUnitAttackCooldown(orig, 0), 0)
    call SetUnitMoveSpeed(clone, GetUnitMoveSpeed(orig))

    // 6. Synchronize Attack Range & Projectile Art
    set origRange = BlzGetUnitWeaponRealField(orig, UNIT_WEAPON_RF_ATTACK_RANGE, 0)
    if origRange >= 300.0 then
        call SetUnitAcquireRange(clone, origRange + 150.0)
        call BlzSetUnitWeaponRealField(clone, UNIT_WEAPON_RF_ATTACK_RANGE, 0, origRange)
        call BlzSetUnitWeaponRealField(clone, UNIT_WEAPON_RF_ATTACK_RANGE, 1, origRange)
        set origMissile = BlzGetUnitWeaponStringField(orig, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0)
        if origMissile != null and origMissile != "" then
            call BlzSetUnitWeaponStringField(clone, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0, origMissile)
        elseif origTypeId == 'H005' and origPid >= 0 and origPid <= 15 and udg_Wild_IsMorphed[origPid] and origSkin != 0 then
            call BlzSetUnitWeaponStringField(clone, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0, Wild_GetCreepMissileArt(origSkin))
        endif
    endif
endfunction

function Strain_OnUnitSummon takes nothing returns boolean
    local unit summoned = GetSummonedUnit()
    local integer pId = 0
    local unit realHero = null
    local unit orig = null

    if summoned != null then
        if IsUnitIllusion(summoned) then
            set orig = DM_FindMatchingOrig(summoned)
            if orig != null then
                call DM_SyncClonedUnit(summoned, orig)
            endif
        endif

        // Strain (H004) own Mirror Image (AOmi) handling (only when not created by Dream Master)
        if GetUnitTypeId(summoned) == 'H004' and orig == null then
            set pId = GetPlayerId(GetOwningPlayer(summoned))
            call GroupAddUnit(udg_FakeHeroGroup, summoned)
            call Strain_ApplyCurrentSkin(summoned, pId)
            set realHero = Strain_GetRealHero(pId)
            if realHero != null and not udg_Strain_Burrowed[pId] and not udg_Strain_MimicActive[pId] then
                call Strain_ApplyCurrentSkin(realHero, pId)
            endif
        endif
    endif

    set summoned = null
    set orig = null
    set realHero = null
    return false
endfunction

function DM_CloneOneUnit takes unit caster, unit orig, real tx, real ty returns nothing"""
    patches.append(("Add DM_SyncClonedUnit and new Strain_OnUnitSummon", target_3, replacement_3))

    # 4. In DM_CloneOneUnit: Record orig before native Wand of Illusion order, and call DM_SyncClonedUnit in fallback branches
    target_4 = """        // Hero target (Real Hero OR Fake Hero/Hero Illusion):
        // First try to create an engine-native Hero Illusion via Wand of Illusion (852274)
        set dummy = CreateUnit(p, 'u000', GetUnitX(orig), GetUnitY(orig), 0.0)
        if hasAgh then
            call UnitAddAbility(dummy, 'A00J')
        else
            call UnitAddAbility(dummy, 'A00I')
        endif
        set success = IssueTargetOrderById(dummy, 852274, orig)
        call UnitApplyTimedLife(dummy, 'BTLF', 2.0)
        set dummy = null

        if not success then
            // If the native Wand of Illusion rejected targeting an existing illusion,
            // create clone with full active skills, matching level & items,
            // but completely stripped of hero properties (no altar revival, no XP gain, no hero icon):
            set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
            call RemoveGuardPosition(clone)
            call UnitRemoveType(clone, UNIT_TYPE_HERO)
            call UnitAddType(clone, UNIT_TYPE_SUMMONED)
            call SuspendHeroXP(clone, true)
            call SetHeroLevel(clone, GetHeroLevel(orig), false)
            set itemSlot = 0
            loop
                exitwhen itemSlot >= 6
                set itm = UnitItemInSlot(orig, itemSlot)
                if itm != null then
                    call UnitAddItemById(clone, GetItemTypeId(itm))
                endif
                set itemSlot = itemSlot + 1
            endloop
            set itm = null
            call GroupAddUnit(udg_FakeHeroGroup, clone)
            call UnitApplyTimedLife(clone, 'BTLF', 900.0)
            call SetUnitVertexColor(clone, 100, 150, 255, 180)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
            if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
                call IssuePointOrder(clone, "attack", GetUnitX(orig), GetUnitY(orig))
            endif
            set clone = null
        else
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", orig, "origin"))
        endif
    else
        // Non-hero target (includes Peasants, Peons, Wisps, Acolytes, Creeps, Spellcasters):
        // Clone with full active skills, 15-minute duration, blue illusion tint
        set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
        call RemoveGuardPosition(clone)
        call UnitAddType(clone, UNIT_TYPE_SUMMONED)
        call UnitApplyTimedLife(clone, 'BTLF', 900.0)
        call SetUnitVertexColor(clone, 100, 150, 255, 180)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            call IssuePointOrder(clone, "attack", GetUnitX(orig), GetUnitY(orig))
        endif
        set clone = null
    endif"""

    replacement_4 = """        // Hero target (Real Hero OR Fake Hero/Hero Illusion):
        // First try to create an engine-native Hero Illusion via Wand of Illusion (852274)
        set udg_DM_CloneOrigList[udg_DM_CloneOrigIndex] = orig
        set dummy = CreateUnit(p, 'u000', GetUnitX(orig), GetUnitY(orig), 0.0)
        if hasAgh then
            call UnitAddAbility(dummy, 'A00J')
        else
            call UnitAddAbility(dummy, 'A00I')
        endif
        set success = IssueTargetOrderById(dummy, 852274, orig)
        call UnitApplyTimedLife(dummy, 'BTLF', 2.0)
        set dummy = null

        if success then
            set udg_DM_CloneOrigIndex = udg_DM_CloneOrigIndex + 1
            if udg_DM_CloneOrigIndex >= 32 then
                set udg_DM_CloneOrigIndex = 0
            endif
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", orig, "origin"))
        else
            set udg_DM_CloneOrigList[udg_DM_CloneOrigIndex] = null
            // If the native Wand of Illusion rejected targeting an existing illusion,
            // create clone with full active skills, matching level & items,
            // but completely stripped of hero properties (no altar revival, no XP gain, no hero icon):
            set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
            call RemoveGuardPosition(clone)
            call UnitRemoveType(clone, UNIT_TYPE_HERO)
            call UnitAddType(clone, UNIT_TYPE_SUMMONED)
            call SuspendHeroXP(clone, true)
            call SetHeroLevel(clone, GetHeroLevel(orig), false)
            set itemSlot = 0
            loop
                exitwhen itemSlot >= 6
                set itm = UnitItemInSlot(orig, itemSlot)
                if itm != null then
                    call UnitAddItemById(clone, GetItemTypeId(itm))
                endif
                set itemSlot = itemSlot + 1
            endloop
            set itm = null
            call GroupAddUnit(udg_FakeHeroGroup, clone)
            call UnitApplyTimedLife(clone, 'BTLF', 900.0)
            call SetUnitVertexColor(clone, 100, 150, 255, 180)
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
            if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
                call IssuePointOrder(clone, "attack", GetUnitX(orig), GetUnitY(orig))
            endif
            call DM_SyncClonedUnit(clone, orig)
            set clone = null
        endif
    else
        // Non-hero target (includes Peasants, Peons, Wisps, Acolytes, Creeps, Spellcasters):
        // Clone with full active skills, 15-minute duration, blue illusion tint
        set clone = CreateUnit(p, uId, tx, ty, GetUnitFacing(orig))
        call RemoveGuardPosition(clone)
        call UnitAddType(clone, UNIT_TYPE_SUMMONED)
        call UnitApplyTimedLife(clone, 'BTLF', 900.0)
        call SetUnitVertexColor(clone, 100, 150, 255, 180)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageCaster.mdl", clone, "origin"))
        if GetPlayerController(p) == MAP_CONTROL_COMPUTER then
            call IssuePointOrder(clone, "attack", GetUnitX(orig), GetUnitY(orig))
        endif
        call DM_SyncClonedUnit(clone, orig)
        set clone = null
    endif"""
    patches.append(("DM_CloneOneUnit interception", target_4, replacement_4))

    # 5. DM_OnDamaged protection against illusion handle pollution
    target_5 = """            set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
            call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
            set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
            if udg_Maho_AtkHits[pId] >= 4 then
                set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
                call Maho_AddBaseDamage(src, 1)
            endif
            if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                call Maho_AddAntiMahoAdapt(pId, 0.02)
                call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
            endif
            call Maho_UpdateUI(pId)
        endif

        // Hero #5: Mahoraga Defensive Damage Adaptation & Nirvana Egg
        if GetUnitTypeId(tgt) == 'H006' and dmg > 0.5 then"""

    replacement_5 = """            if not IsUnitIllusion(src) and not IsUnitInGroup(src, udg_FakeHeroGroup) then
                set udg_Maho_AtkAdapt[pId * 8 + defType] = udg_Maho_AtkAdapt[pId * 8 + defType] + 0.015
                call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
                set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] + 1
                if udg_Maho_AtkHits[pId] >= 4 then
                    set udg_Maho_AtkHits[pId] = udg_Maho_AtkHits[pId] - 4
                    call Maho_AddBaseDamage(src, 1)
                endif
                if GetUnitTypeId(tgt) == 'H006' and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                    call Maho_AddAntiMahoAdapt(pId, 0.02)
                    call Maho_TriggerWheelSpin(pId, 0.55, 1.5)
                endif
                call Maho_UpdateUI(pId)
            endif
        endif

        // Hero #5: Mahoraga Defensive Damage Adaptation & Nirvana Egg
        if GetUnitTypeId(tgt) == 'H006' and not IsUnitIllusion(tgt) and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and dmg > 0.5 then"""
    patches.append(("DM_OnDamaged illusion protection", target_5, replacement_5))

    for name, tgt, rep in patches:
        count = content.count(tgt)
        if count != 1:
            print(f"ERROR: Patch '{name}' matched {count} times (expected 1)!")
            sys.exit(1)
        content = content.replace(tgt, rep)
        print(f"Applied patch: {name}")

    if is_crlf:
        content = content.replace('\n', '\r\n')

    with open('payload/war3map.j', 'wb') as f:
        f.write(content.encode('utf-8'))
    print("All patches successfully applied to payload/war3map.j for v5.9!")

if __name__ == '__main__':
    apply_patches()
