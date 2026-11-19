# -*- coding: utf-8 -*-
import sys
import os
import re

jass_path = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j"

with open(jass_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add global variable udg_Strain_MirrorSyncTimer
old_global = "    effect array udg_Strain_Stage3Fx"
new_global = """    effect array udg_Strain_Stage3Fx
    real array udg_Strain_MirrorSyncTimer"""

if old_global in text:
    text = text.replace(old_global, new_global, 1)
    print("1. Added udg_Strain_MirrorSyncTimer global.")
else:
    print("Error: old_global not found")
    sys.exit(1)

# 2. Add Strain_GetRealHero before Strain_ApplyCurrentSkin, and update Strain_ApplyCurrentSkin
old_skin_fn_start = "function Strain_ApplyCurrentSkin takes unit u, integer pId returns nothing"
old_skin_fn_end = "endfunction\n\nfunction Strain_UpdateEvoUI"

idx_skin_start = text.find(old_skin_fn_start)
idx_skin_end = text.find(old_skin_fn_end)

if idx_skin_start == -1 or idx_skin_end == -1:
    print(f"Error: skin function indices: {idx_skin_start}, {idx_skin_end}")
    sys.exit(1)

new_helper_and_skin = """function Strain_GetRealHero takes integer pId returns unit
    local group g = null
    local unit enumU = null
    local unit candidate = null

    if pId < 0 or pId > 15 then
        return null
    endif

    set candidate = udg_Strain_Hero[pId]
    if candidate != null and not IsUnitIllusion(candidate) and not IsUnitInGroup(candidate, udg_FakeHeroGroup) and GetUnitTypeId(candidate) == 'H004' then
        return candidate
    endif

    // Strictly scan Player(pId)'s units for the genuine, non-illusion H004
    set g = CreateGroup()
    call GroupEnumUnitsOfPlayer(g, Player(pId), null)
    loop
        set enumU = FirstOfGroup(g)
        exitwhen enumU == null
        call GroupRemoveUnit(g, enumU)
        if GetUnitTypeId(enumU) == 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
            set udg_Strain_Hero[pId] = enumU
            call DestroyGroup(g)
            return enumU
        endif
    endloop
    call DestroyGroup(g)

    return null
endfunction

function Strain_ApplyCurrentSkin takes unit u, integer pId returns nothing
    local integer stage = 0
    local integer targetSkin = 'zzrg'
    local real scale = 1.15
    if u == null then
        return
    endif
    set stage = udg_Strain_EvoStage[pId]
    if stage == 0 then
        set targetSkin = 'zzrg'
        set scale = 1.15
    elseif stage == 1 then
        set targetSkin = 'nano'
        set scale = 1.30
    elseif stage == 2 then
        set targetSkin = 'zhyd'
        set scale = 1.40
    elseif stage >= 3 then
        set targetSkin = 'Ucrl'
        set scale = 1.65
    endif

    // 2-step skin swap to flush Warcraft 3 1.32 internal C++ skin cache (fixes AOmi Mirror Image skin lock)
    call BlzSetUnitSkin(u, 'H004')
    call BlzSetUnitSkin(u, targetSkin)
    call SetUnitScale(u, scale, scale, scale)

    if stage == 0 then
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 0, 128.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 1, 128.0)
        call SetUnitAcquireRange(u, 500.0)
        call SetUnitVertexColor(u, 255, 255, 255, 255)
    elseif stage == 1 then
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 0, 128.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 1, 128.0)
        call SetUnitAcquireRange(u, 500.0)
        call SetUnitVertexColor(u, 255, 255, 255, 255)
    elseif stage == 2 then
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 0, 500.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 1, 500.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_PROJECTILE_SPEED, 0, 1200.0)
        call BlzSetUnitWeaponStringField(u, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0, "Abilities\\\\Weapons\\\\ChimaeraAcidMissile\\\\ChimaeraAcidMissile.mdl")
        call SetUnitAcquireRange(u, 650.0)
        call SetUnitVertexColor(u, 255, 255, 255, 255)
    elseif stage >= 3 then
        call SetUnitVertexColor(u, 235, 200, 255, 255)
        call BlzSetUnitAbilityCooldown(u, 'A022', 0, 4.0)
        call BlzSetUnitAbilityCooldown(u, 'A022', 1, 4.0)
        call BlzSetUnitAbilityCooldown(u, 'A022', 2, 4.0)
        if not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
            if udg_Strain_Stage3Fx[pId] != null then
                call DestroyEffect(udg_Strain_Stage3Fx[pId])
                set udg_Strain_Stage3Fx[pId] = null
            endif
            set udg_Strain_Stage3Fx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\GeneralAuraTarget\\\\GeneralAuraTarget.mdl", u, "origin")
        endif
    endif
endfunction

function Strain_SyncAllHeroAndIllusions takes integer pId returns nothing
    local unit realHero = null
    local group g = null
    local unit enumU = null

    if pId < 0 or pId > 15 then
        return
    endif

    set realHero = Strain_GetRealHero(pId)
    if realHero != null and not IsUnitType(realHero, UNIT_TYPE_DEAD) and GetWidgetLife(realHero) > 0.405 then
        if not udg_Strain_Burrowed[pId] and not udg_Strain_MimicActive[pId] then
            call Strain_ApplyCurrentSkin(realHero, pId)
        endif
    endif

    // Sync all illusions of H004 for this player
    set g = CreateGroup()
    call GroupEnumUnitsOfPlayer(g, Player(pId), null)
    loop
        set enumU = FirstOfGroup(g)
        exitwhen enumU == null
        call GroupRemoveUnit(g, enumU)
        if GetUnitTypeId(enumU) == 'H004' and (IsUnitIllusion(enumU) or IsUnitInGroup(enumU, udg_FakeHeroGroup)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 then
            call GroupAddUnit(udg_FakeHeroGroup, enumU)
            call Strain_ApplyCurrentSkin(enumU, pId)
        endif
    endloop
    call DestroyGroup(g)
endfunction

function Strain_OnUnitSummon takes nothing returns boolean
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

text = text[:idx_skin_start] + new_helper_and_skin + "\n\n" + text[idx_skin_end+11:]
print("2. Added Strain_GetRealHero, Strain_ApplyCurrentSkin, Strain_SyncAllHeroAndIllusions, Strain_OnUnitSummon.")

# 3. Update Strain_CheckEvolution to always force real hero and sync illusions
old_evo_fn_start = "function Strain_CheckEvolution takes unit u, integer pId returns nothing"
old_evo_fn_end = "endfunction\n\nfunction Strain_InitHero"

idx_evo_start = text.find(old_evo_fn_start)
idx_evo_end = text.find(old_evo_fn_end)

if idx_evo_start == -1 or idx_evo_end == -1:
    print(f"Error: evo function indices: {idx_evo_start}, {idx_evo_end}")
    sys.exit(1)

new_evo_fn = """function Strain_CheckEvolution takes unit u, integer pId returns nothing
    local integer devours = 0
    local integer curStage = 0
    local unit realHero = null

    if pId < 0 or pId > 15 then
        return
    endif

    set realHero = Strain_GetRealHero(pId)
    if realHero == null or IsUnitType(realHero, UNIT_TYPE_DEAD) then
        return
    endif
    set u = realHero

    set devours = udg_Strain_DevourCount[pId]
    set curStage = udg_Strain_EvoStage[pId]

    // Stage 1 threshold: 8 devours
    if devours >= 8 and curStage < 1 then
        set udg_Strain_EvoStage[pId] = 1
        set curStage = 1

        call Strain_ApplyCurrentSkin(u, pId)
        call SetUnitMoveSpeed(u, GetUnitMoveSpeed(u) + 45.0)
        call BlzSetUnitAttackCooldown(u, BlzGetUnitAttackCooldown(u, 0) * 0.80, 0)
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + 300)
        call SetWidgetLife(u, GetWidgetLife(u) + 300.0)
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + 25, 0)
        call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + 4.0)
        set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + 300
        set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + 25
        set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + 4.0

        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Devour\\\\DevourEffectArt.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5.0, "|cff9900ff【一阶基因蜕壳·紫晶重装巨蝎】|r 异种之源突破幼体束缚完成蜕壳！永久获得 +45移速 / +20%攻速 / +300生命 / +25攻击 / +4护甲！")
    endif

    // Stage 2 threshold: 18 devours
    if devours >= 18 and curStage < 2 then
        set udg_Strain_EvoStage[pId] = 2
        set curStage = 2

        call Strain_ApplyCurrentSkin(u, pId)
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + 600)
        call SetWidgetLife(u, GetWidgetLife(u) + 600.0)
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + 45, 0)
        call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + 6.0)
        set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + 600
        set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + 45
        set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + 6.0

        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Devour\\\\DevourEffectArt.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5.0, "|cff33ff33【二阶基因蜕壳·星际虫族刺蛇】|r 进化为星际刺蛇！获得500码远程强酸骨刺喷射、每秒2.5%最大生命值再生甲壳、+600生命 / +45攻击 / +6护甲！")
    endif

    // Stage 3 threshold: 30 devours
    if devours >= 30 and curStage < 3 then
        set udg_Strain_EvoStage[pId] = 3
        set curStage = 3

        call UnitAddAbility(u, 'ACmi')
        call Strain_ApplyCurrentSkin(u, pId)
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + 1200)
        call SetWidgetLife(u, GetWidgetLife(u) + 1200.0)
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + 80, 0)
        call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + 10.0)
        set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + 1200
        set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + 80
        set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + 10.0

        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Objects\\\\Spawnmodels\\\\Human\\\\HumanLargeDeathExplode\\\\HumanLargeDeathExplode.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 6.0, "|cffff0000【终极基因蜕壳·始祖利维坦虫皇】|r 登顶为至高无上的深渊始祖虫皇！获得永久魔免、25%深渊吸血、W技能4秒CD且1秒秒速消化、+1200生命 / +80攻击 / +10护甲！")
    endif

    call Strain_SyncAllHeroAndIllusions(pId)
    call Strain_UpdateEvoUI(pId)
endfunction"""

text = text[:idx_evo_start] + new_evo_fn + "\n\n" + text[idx_evo_end+11:]
print("3. Updated Strain_CheckEvolution.")

# 4. Update Strain_InitHero to guard against illusions
old_init_hero = """function Strain_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif"""

new_init_hero = """function Strain_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null or IsUnitIllusion(h) or IsUnitInGroup(h, udg_FakeHeroGroup) then
        return
    endif"""

if old_init_hero in text:
    text = text.replace(old_init_hero, new_init_hero, 1)
    print("4. Guarded Strain_InitHero against illusions.")
else:
    print("Warning: old_init_hero not found")
    sys.exit(1)

# 5. In dialog click handlers, use Strain_GetRealHero
# 5a. Strain_OnGeneChoiceClick
old_gene_click = """    set pId = GetPlayerId(p)
    set u = udg_Strain_Hero[pId]
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif
    if u == null then
        set g = CreateGroup()
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set enumU = FirstOfGroup(g)
            exitwhen enumU == null
            call GroupRemoveUnit(g, enumU)
            if GetUnitTypeId(enumU) == 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                set u = enumU
                set udg_Strain_Hero[pId] = enumU
                exitwhen true
            endif
        endloop
        call DestroyGroup(g)
        set g = null
    endif"""

new_gene_click = """    set pId = GetPlayerId(p)
    set u = Strain_GetRealHero(pId)
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif"""

if old_gene_click in text:
    text = text.replace(old_gene_click, new_gene_click, 1)
    print("5a. Replaced hero lookup in Strain_OnGeneChoiceClick.")
else:
    print("Warning: old_gene_click not found")
    sys.exit(1)

# 5b. Strain_OnSkillDialogClick
old_skill_click = """    set pId = GetPlayerId(p)
    set u = udg_Strain_Hero[pId]
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif
    if u == null then
        set g = CreateGroup()
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set enumU = FirstOfGroup(g)
            exitwhen enumU == null
            call GroupRemoveUnit(g, enumU)
            if GetUnitTypeId(enumU) == 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                set u = enumU
                set udg_Strain_Hero[pId] = enumU
                exitwhen true
            endif
        endloop
        call DestroyGroup(g)
        set g = null
    endif"""

new_skill_click = """    set pId = GetPlayerId(p)
    set u = Strain_GetRealHero(pId)
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif"""

if old_skill_click in text:
    text = text.replace(old_skill_click, new_skill_click, 1)
    print("5b. Replaced hero lookup in Strain_OnSkillDialogClick.")
else:
    print("Warning: old_skill_click not found")
    sys.exit(1)

# 5c. Strain_OnConsoleDialogClick
old_console_click = """    set pId = GetPlayerId(p)
    set u = udg_Strain_Hero[pId]
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif
    if u == null then
        set g = CreateGroup()
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set enumU = FirstOfGroup(g)
            exitwhen enumU == null
            call GroupRemoveUnit(g, enumU)
            if GetUnitTypeId(enumU) == 'H004' and not IsUnitIllusion(enumU) and not IsUnitInGroup(enumU, udg_FakeHeroGroup) then
                set u = enumU
                set udg_Strain_Hero[pId] = enumU
                exitwhen true
            endif
        endloop
        call DestroyGroup(g)
        set g = null
    endif"""

new_console_click = """    set pId = GetPlayerId(p)
    set u = Strain_GetRealHero(pId)
    if u == null then
        set u = udg_AI_CustomHero[pId]
    endif"""

if old_console_click in text:
    text = text.replace(old_console_click, new_console_click, 1)
    print("5c. Replaced hero lookup in Strain_OnConsoleDialogClick.")
else:
    print("Warning: old_console_click not found")
    sys.exit(1)

# 7. Update DM_CapTimerLoop:
# 7a. Regenerative Carapace (use Strain_GetRealHero)
old_rc = """        if udg_Strain_EvoStage[pId] >= 2 then
            set u = udg_Strain_Hero[pId]
            if u == null then
                set u = udg_AI_CustomHero[pId]
            endif"""

new_rc = """        if udg_Strain_EvoStage[pId] >= 2 then
            set u = Strain_GetRealHero(pId)
            if u == null then
                set u = udg_AI_CustomHero[pId]
            endif"""

if old_rc in text:
    text = text.replace(old_rc, new_rc, 1)
    print("7a. Regenerative Carapace uses Strain_GetRealHero.")

# 7b. Digestion completion (use Strain_GetRealHero)
old_digest = """                set u = udg_Strain_Hero[pId]
                if u == null then
                    set u = udg_AI_CustomHero[pId]
                endif"""

new_digest = """                set u = Strain_GetRealHero(pId)
                if u == null then
                    set u = udg_AI_CustomHero[pId]
                endif"""

if old_digest in text:
    text = text.replace(old_digest, new_digest, 1)
    print("7b. Digestion completion uses Strain_GetRealHero.")

# 7c. Stage 3 Cooldown clamp (use Strain_GetRealHero)
old_clamp = """        if udg_Strain_EvoStage[pId] >= 3 then
            set u = udg_Strain_Hero[pId]
            if u == null then
                set u = udg_AI_CustomHero[pId]
            endif"""

new_clamp = """        if udg_Strain_EvoStage[pId] >= 3 then
            set u = Strain_GetRealHero(pId)
            if u == null then
                set u = udg_AI_CustomHero[pId]
            endif"""

if old_clamp in text:
    text = text.replace(old_clamp, new_clamp, 1)
    print("7c. Cooldown clamp uses Strain_GetRealHero.")

# 7d. Add 1s loop skin verification in DM_CapTimerLoop
old_clamp_end = """            if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) then
                if BlzGetUnitAbilityCooldownRemaining(u, 'A022') > 4.0 then
                    call BlzStartUnitAbilityCooldown(u, 'A022', 3.5)
                endif
            endif
            set u = null
        endif
        set pId = pId + 1
    endloop"""

new_clamp_end = """            if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) then
                if BlzGetUnitAbilityCooldownRemaining(u, 'A022') > 4.0 then
                    call BlzStartUnitAbilityCooldown(u, 'A022', 3.5)
                endif
            endif
            set u = null
        endif
        set pId = pId + 1
    endloop

    // 3.8. Hero #3 Skin Verification & Illusion Synchronization
    set pId = 0
    loop
        exitwhen pId > 7
        set u = Strain_GetRealHero(pId)
        if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
            if not udg_Strain_Burrowed[pId] and not udg_Strain_MimicActive[pId] then
                if BlzGetUnitSkin(u) == 'H004' and udg_Strain_EvoStage[pId] > 0 then
                    call Strain_ApplyCurrentSkin(u, pId)
                endif
            endif
        endif
        set u = null
        set pId = pId + 1
    endloop"""

if old_clamp_end in text:
    text = text.replace(old_clamp_end, new_clamp_end, 1)
    print("7d. Added skin verification to DM_CapTimerLoop.")
else:
    print("Warning: old_clamp_end not found")
    sys.exit(1)

# 8. Update DM_StealthLoop to handle udg_Strain_MirrorSyncTimer
stealth_hook_target = "    // 1. Process pending stealth queue\n    set i = 0"
new_stealth_timer_code = """    // 0. Process Strain Mirror Image Sync Timer
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_MirrorSyncTimer[pId] > 0.0 then
            set udg_Strain_MirrorSyncTimer[pId] = udg_Strain_MirrorSyncTimer[pId] - 0.05
            if udg_Strain_MirrorSyncTimer[pId] <= 0.0 then
                call Strain_SyncAllHeroAndIllusions(pId)
            endif
        endif
        set pId = pId + 1
    endloop

    // 1. Process pending stealth queue
    set i = 0"""

if stealth_hook_target in text:
    text = text.replace(stealth_hook_target, new_stealth_timer_code, 1)
    print("8. Added Mirror Image timer countdown to DM_StealthLoop.")
else:
    print("Warning: stealth_hook_target not found")
    sys.exit(1)

# 9. Update DM_OnSpellEffect:
# 9a. For A021, A022, A023, A024: only set udg_Strain_Hero[pId] if not illusion
text = text.replace(
    "    elseif abil == 'A021' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        set udg_Strain_Hero[pId] = caster",
    "    elseif abil == 'A021' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        if not IsUnitIllusion(caster) and not IsUnitInGroup(caster, udg_FakeHeroGroup) then\n            set udg_Strain_Hero[pId] = caster\n        endif"
)
text = text.replace(
    "    elseif abil == 'A022' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        set ult = GetSpellTargetUnit()\n        set udg_Strain_Hero[pId] = caster",
    "    elseif abil == 'A022' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        set ult = GetSpellTargetUnit()\n        if not IsUnitIllusion(caster) and not IsUnitInGroup(caster, udg_FakeHeroGroup) then\n            set udg_Strain_Hero[pId] = caster\n        endif"
)
text = text.replace(
    "    elseif abil == 'A023' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        set udg_Strain_Hero[pId] = caster",
    "    elseif abil == 'A023' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        if not IsUnitIllusion(caster) and not IsUnitInGroup(caster, udg_FakeHeroGroup) then\n            set udg_Strain_Hero[pId] = caster\n        endif"
)
text = text.replace(
    "    elseif abil == 'A024' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        set udg_Strain_Hero[pId] = caster",
    "    elseif abil == 'A024' then\n        set pId = GetPlayerId(GetOwningPlayer(caster))\n        if not IsUnitIllusion(caster) and not IsUnitInGroup(caster, udg_FakeHeroGroup) then\n            set udg_Strain_Hero[pId] = caster\n        endif"
)
print("9a. Guarded A021/A022/A023/A024 udg_Strain_Hero assignment against illusions.")

# 9b. Add AOmi hook in DM_OnSpellEffect
aomi_hook_target = "    elseif abil == 'A024' then"
aomi_hook_code = """    elseif abil == 'AOmi' then
        set pId = GetPlayerId(GetOwningPlayer(caster))
        if GetUnitTypeId(caster) == 'H004' then
            if not IsUnitIllusion(caster) and not IsUnitInGroup(caster, udg_FakeHeroGroup) then
                set udg_Strain_Hero[pId] = caster
            endif
            set udg_Strain_MirrorSyncTimer[pId] = 0.60
        endif
    elseif abil == 'A024' then"""

if aomi_hook_target in text:
    text = text.replace(aomi_hook_target, aomi_hook_code, 1)
    print("9b. Added AOmi hook to DM_OnSpellEffect.")
else:
    print("Warning: aomi_hook_target not found")
    sys.exit(1)

# 10. Update DM_OnDamaged at line 8404: guard udg_Strain_Hero[pId] = src
dmg_hero_target = """        // Hero #3: The Primordial Strain (H004) Damage Interactions
        if GetUnitTypeId(src) == 'H004' then
            set pId = GetPlayerId(GetOwningPlayer(src))
            set udg_Strain_Hero[pId] = src"""

dmg_hero_new = """        // Hero #3: The Primordial Strain (H004) Damage Interactions
        if GetUnitTypeId(src) == 'H004' then
            set pId = GetPlayerId(GetOwningPlayer(src))
            if not IsUnitIllusion(src) and not IsUnitInGroup(src, udg_FakeHeroGroup) then
                set udg_Strain_Hero[pId] = src
            endif"""

if dmg_hero_target in text:
    text = text.replace(dmg_hero_target, dmg_hero_new, 1)
    print("10. Guarded DM_OnDamaged udg_Strain_Hero assignment against illusions.")
else:
    print("Warning: dmg_hero_target not found")
    sys.exit(1)

# 11. Update TM_SpawnSandboxTargets (-spawn) & TM_OnChatCommand (-evo)
spawn_target = """    if udg_Strain_Hero[pId] != null then
        call UnitResetCooldown(udg_Strain_Hero[pId])
        set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 4
        call Strain_CheckEvolution(udg_Strain_Hero[pId], pId)
        call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cff00ff00[沙盒测试]|r 异种之源获得 +4 吞噬进度！累计: " + I2S(udg_Strain_DevourCount[pId]) + " 次")
    endif"""

spawn_new = """    set u = Strain_GetRealHero(pId)
    if u != null then
        call UnitResetCooldown(u)
        set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 4
        call Strain_CheckEvolution(u, pId)
        call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cff00ff00[沙盒测试]|r 异种之源获得 +4 吞噬进度！累计: " + I2S(udg_Strain_DevourCount[pId]) + " 次")
    endif"""

if spawn_target in text:
    text = text.replace(spawn_target, spawn_new, 1)
    print("11a. -spawn updated to use Strain_GetRealHero.")
else:
    print("Warning: spawn_target not found")
    sys.exit(1)

# -evo block replacement
evo_pos = text.find('s == "-evo"')
if evo_pos != -1:
    evo_end = text.find('endif\n', evo_pos)
    if evo_end != -1:
        new_evo_sub = """s == "-evo" then
        set u = Strain_GetRealHero(pId)
        if u != null then
            set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 8
            call Strain_CheckEvolution(u, pId)
            call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cff00ff00[极速进化测试]|r 异种之源获得 +8 吞噬进度！累计: " + I2S(udg_Strain_DevourCount[pId]) + " 次")
        else
            call DisplayTimedTextToPlayer(p, 0, 0, 3.0, "|cffffcc00[极速进化测试]|r 未检测到异种之源英雄！")
        endif"""
        text = text[:evo_pos] + new_evo_sub + text[evo_end+5:]
        print("11b. -evo updated to use Strain_GetRealHero.")
    else:
        print("Warning: evo_end not found")
        sys.exit(1)
else:
    print("Warning: evo_pos not found")
    sys.exit(1)

# 12. Register tSummon in DM_InitTriggers
init_target = """    local trigger tWildDialog = CreateTrigger()"""
init_new = """    local trigger tWildDialog = CreateTrigger()
    local trigger tSummon = CreateTrigger()"""

if init_target in text:
    text = text.replace(init_target, init_new, 1)
    print("12a. Declared tSummon in DM_InitTriggers.")
else:
    print("Warning: init_target not found")
    sys.exit(1)

# Initialize timer in loop
init_loop_target = """        set udg_Strain_PendingNewAbil[i] = 0
        set udg_Strain_Hero[i] = null"""

init_loop_new = """        set udg_Strain_PendingNewAbil[i] = 0
        set udg_Strain_Hero[i] = null
        set udg_Strain_MirrorSyncTimer[i] = 0.0"""

if init_loop_target in text:
    text = text.replace(init_loop_target, init_loop_new, 1)
    print("12b. Initialized udg_Strain_MirrorSyncTimer in DM_InitTriggers.")
else:
    print("Warning: init_loop_target not found")
    sys.exit(1)

# Register event
reg_event_target = """    call TriggerRegisterAnyUnitEventBJ(tAttack, EVENT_PLAYER_UNIT_ATTACKED)
    call TriggerAddCondition(tAttack, Condition(function DM_OnUnitAttacked))"""

reg_event_new = """    call TriggerRegisterAnyUnitEventBJ(tSummon, EVENT_PLAYER_UNIT_SUMMON)
    call TriggerAddCondition(tSummon, Condition(function Strain_OnUnitSummon))

    call TriggerRegisterAnyUnitEventBJ(tAttack, EVENT_PLAYER_UNIT_ATTACKED)
    call TriggerAddCondition(tAttack, Condition(function DM_OnUnitAttacked))"""

if reg_event_target in text:
    text = text.replace(reg_event_target, reg_event_new, 1)
    print("12c. Registered EVENT_PLAYER_UNIT_SUMMON in DM_InitTriggers.")
else:
    print("Warning: reg_event_target not found")
    sys.exit(1)

# Null out tSummon
null_target = """    set tReplaceDialog = null"""
null_new = """    set tReplaceDialog = null
    set tSummon = null"""

if null_target in text:
    text = text.replace(null_target, null_new, 1)
    print("12d. Nulled tSummon.")
else:
    print("Warning: null_target not found")
    sys.exit(1)

with open(jass_path, "w", encoding="utf-8") as f:
    f.write(text)

print("apply_v41_patch.py finished successfully!")
