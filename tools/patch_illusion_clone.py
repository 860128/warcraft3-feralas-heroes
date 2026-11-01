with open("payload/war3map.j", "r", encoding="utf-8") as f:
    text = f.read()

old_clone = """function DM_CloneOneUnit takes unit caster, unit orig, real tx, real ty returns nothing
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
endfunction"""

new_clone = """function DM_CloneOneUnit takes unit caster, unit orig, real tx, real ty returns nothing
    local player p = GetOwningPlayer(caster)
    local integer uId = GetUnitTypeId(orig)
    local unit clone = null
    local unit dummy = null
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0

    // Check if the target is an illusion (either native illusion or has illusion buff)
    if IsUnitIllusionBJ(orig) or GetUnitAbilityLevel(orig, 'BIil') > 0 or GetUnitAbilityLevel(orig, 'BOmi') > 0 then
        // Clones cannot be cloned again!
        set p = null
        return
    endif

    if IsUnitType(orig, UNIT_TYPE_HERO) then
        // True Hero target: create engine-native Hero Phantom via Wand of Illusion (852274)
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
endfunction"""

assert old_clone in text, "old_clone not found!"
text = text.replace(old_clone, new_clone)

with open("payload/war3map.j", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated payload/war3map.j successfully.")
