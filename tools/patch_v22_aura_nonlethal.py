import os

jass_path = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j'

with open(jass_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Verify CRLF
crlf = '\r\n' in text
newline = '\r\n' if crlf else '\n'

old_section = """    // 2. Process Ninja Aura (A012)
    set pId = 0
    loop
        exitwhen pId > 7
        set th = udg_Ninja_TrueHero[pId]
        if th != null and udg_Ninja_AuraOn[pId] then
            set dmgSrc = null
            if not IsUnitType(th, UNIT_TYPE_DEAD) then
                set dmgSrc = th
            else
                set dmgSrc = Ninja_PickLivingClone(pId)
            endif
            if dmgSrc != null then
                set aLv = GetUnitAbilityLevel(th, 'A012')
                if aLv > 0 then
                    set pct = 0.01 * I2R(aLv)
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRect(udg_EnumGroup, bj_mapInitialPlayableArea, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, Player(pId)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
                            set drain = GetUnitState(enumU, UNIT_STATE_MAX_LIFE) * pct
                            if GetWidgetLife(enumU) > (drain + 1.0) then
                                call SetWidgetLife(enumU, GetWidgetLife(enumU) - drain)
                            else
                                call UnitDamageTarget(dmgSrc, enumU, drain + 100.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_UNIVERSAL, WEAPON_TYPE_WHOKNOWS)
                            endif
                        endif
                    endloop
                endif
            endif
        endif
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
    endloop"""

new_section = """    // 2. Process Ninja Aura (A012)
    set pId = 0
    loop
        exitwhen pId > 7
        set th = udg_Ninja_TrueHero[pId]
        if th != null and udg_Ninja_AuraOn[pId] then
            set dmgSrc = null
            if not IsUnitType(th, UNIT_TYPE_DEAD) then
                set dmgSrc = th
            else
                set dmgSrc = Ninja_PickLivingClone(pId)
            endif
            if dmgSrc != null then
                set aLv = GetUnitAbilityLevel(th, 'A012')
                if aLv > 0 then
                    set pct = 0.01 * I2R(aLv)
                    call GroupClear(udg_EnumGroup)
                    call GroupEnumUnitsInRect(udg_EnumGroup, bj_mapInitialPlayableArea, null)
                    loop
                        set enumU = FirstOfGroup(udg_EnumGroup)
                        exitwhen enumU == null
                        call GroupRemoveUnit(udg_EnumGroup, enumU)
                        if IsUnitEnemy(enumU, Player(pId)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then
                            set drain = GetUnitState(enumU, UNIT_STATE_MAX_LIFE) * pct
                            set curHP = GetWidgetLife(enumU)
                            if curHP > 1.5 then
                                if curHP - drain > 1.0 then
                                    call SetWidgetLife(enumU, curHP - drain)
                                else
                                    call SetWidgetLife(enumU, 1.0)
                                endif
                            endif
                        endif
                    endloop
                endif
            endif
        endif
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
                set curHP = GetWidgetLife(u)
                if curHP > 1.5 then
                    if curHP - drain > 1.0 then
                        call SetWidgetLife(u, curHP - drain)
                    else
                        call SetWidgetLife(u, 1.0)
                    endif
                endif
            endif
        endif
        set u = null
        set i = i + 1
    endloop"""

# Also ensure curHP is declared in DM_CapTimerLoop
old_decl = """    local real drain = 0.0
    local unit enumU = null"""

new_decl = """    local real drain = 0.0
    local real curHP = 0.0
    local unit enumU = null"""

norm_text = text.replace('\r\n', '\n')
norm_old_decl = old_decl.replace('\r\n', '\n')
norm_new_decl = new_decl.replace('\r\n', '\n')
norm_old_sec = old_section.replace('\r\n', '\n')
norm_new_sec = new_section.replace('\r\n', '\n')

assert norm_old_decl in norm_text, "Declaration target not found!"
assert norm_old_sec in norm_text, "Section target not found!"

norm_text = norm_text.replace(norm_old_decl, norm_new_decl, 1)
norm_text = norm_text.replace(norm_old_sec, norm_new_sec, 1)

if crlf:
    out_text = norm_text.replace('\n', '\r\n')
else:
    out_text = norm_text

with open(jass_path, 'w', encoding='utf-8') as f:
    f.write(out_text)

print("Successfully patched DM_CapTimerLoop in war3map.j!")
