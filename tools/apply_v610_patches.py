# -*- coding: utf-8 -*-
import os

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
J_PATH = os.path.join(ROOT, "payload", "war3map.j")


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"[{label}] expected 1 match, got {count}")
    return text.replace(old, new, 1)


def main() -> None:
    with open(J_PATH, "rb") as f:
        raw = f.read()

    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8").replace("\r\n", "\n")

    # 1. SM_CreateMirror: always spawn Mirror at 100% full HP & Mana
    old_create = """    set curHP = RMinBJ(I2R(BlzGetUnitMaxHP(m)), RMaxBJ(1.0, GetWidgetLife(orig)))
    call SetWidgetLife(m, curHP)
    if BlzGetUnitMaxMana(m) > 0 then
        set curMana = RMinBJ(I2R(BlzGetUnitMaxMana(m)), GetUnitState(orig, UNIT_STATE_MANA))
        call SetUnitState(m, UNIT_STATE_MANA, curMana)
    endif"""

    new_create = """    if ut == 'H005' then
        set udg_Wild_StoredManaRatio[13] = 1.0
    endif
    set curHP = GetUnitState(m, UNIT_STATE_MAX_LIFE)
    call SetWidgetLife(m, curHP)
    set curMana = GetUnitState(m, UNIT_STATE_MAX_MANA)
    if curMana > 0.0 then
        call SetUnitState(m, UNIT_STATE_MANA, curMana)
    endif"""

    text = replace_exact(text, old_create, new_create, "SM_CreateMirror full HP/Mana")

    # 2. SM_CloseAndRelease (outcome == 2): handle egg/dead safety + restore 100% HP/Mana/cleanse/CD reset
    old_egg = """    if outcome == 2 and m != null then
        if udg_Maho_InEgg[13] then
            call Maho_OnEggComplete(13)
        endif"""

    new_egg = """    if outcome == 2 and m != null then
        if udg_Maho_InEgg[13] then
            call Maho_OnEggComplete(13)
        elseif udg_Maho_PendingEggEnter[13] then
            set udg_Maho_PendingEggEnter[13] = false
            call ShowUnit(m, true)
            call PauseUnit(m, false)
            call SetUnitInvulnerable(m, false)
        endif
        if IsUnitType(m, UNIT_TYPE_DEAD) and IsUnitType(m, UNIT_TYPE_HERO) then
            call ReviveHero(m, udg_SM_ReturnX, udg_SM_ReturnY, false)
        endif"""

    text = replace_exact(text, old_egg, new_egg, "SM_CloseAndRelease egg/revive safety")

    old_exit = """        call SM_ResetCustomHeroSlot(13)

        call SetUnitPosition(m, udg_SM_ReturnX, udg_SM_ReturnY)
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\MassTeleport\\\\MassTeleportTarget.mdl", GetUnitX(m), GetUnitY(m)))
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Demon\\\\DarkPortal\\\\DarkPortalTarget.mdl", GetUnitX(m), GetUnitY(m)))
        if udg_SM_ConqueredGroup != null then
            call GroupAddUnit(udg_SM_ConqueredGroup, m)
        endif
        if GetLocalPlayer() == udg_SM_CasterOwner then
            call PanCameraToTimed(GetUnitX(m), GetUnitY(m), 0.35)
            call SelectUnit(m, true)
            call PingMinimapEx(GetUnitX(m), GetUnitY(m), 5.0, 120, 220, 255, false)
        endif
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 9.0, "|cffcc66ff【镜像夺舍 · 破山而出！】|r 封印之山内的镜像彻底击杀了本尊【|cffffcc00" + GetUnitName(m) + "|r】，现已携全套属性与技能破封而出，永久归属于你麾下！")"""

    new_exit = """        call SM_ResetCustomHeroSlot(13)

        call PauseUnit(m, false)
        call SetUnitInvulnerable(m, false)
        call UnitRemoveBuffs(m, false, true)
        call UnitResetCooldown(m)
        if ut == 'H005' then
            set udg_Wild_StoredManaRatio[dstPid] = 1.0
            set udg_Wild_MorphCD[dstPid] = 0.0
        elseif ut == 'H006' then
            set udg_Maho_EggCD[dstPid] = 0.0
            set udg_Maho_CCTimer[dstPid] = 0.0
        endif
        call SetWidgetLife(m, GetUnitState(m, UNIT_STATE_MAX_LIFE))
        if GetUnitState(m, UNIT_STATE_MAX_MANA) > 0.0 then
            call SetUnitState(m, UNIT_STATE_MANA, GetUnitState(m, UNIT_STATE_MAX_MANA))
        endif

        call SetUnitPosition(m, udg_SM_ReturnX, udg_SM_ReturnY)
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\MassTeleport\\\\MassTeleportTarget.mdl", GetUnitX(m), GetUnitY(m)))
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Demon\\\\DarkPortal\\\\DarkPortalTarget.mdl", GetUnitX(m), GetUnitY(m)))
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", GetUnitX(m), GetUnitY(m)))
        if udg_SM_ConqueredGroup != null then
            call GroupAddUnit(udg_SM_ConqueredGroup, m)
        endif
        if GetLocalPlayer() == udg_SM_CasterOwner then
            call PanCameraToTimed(GetUnitX(m), GetUnitY(m), 0.35)
            call SelectUnit(m, true)
            call PingMinimapEx(GetUnitX(m), GetUnitY(m), 5.0, 120, 220, 255, false)
        endif
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 9.0, "|cffcc66ff【镜像夺舍 · 破山而出！】|r 封印之山内的镜像彻底击杀了本尊【|cffffcc00" + GetUnitName(m) + "|r】，现已满血满蓝携全套属性与技能破封而出，永久归属于你麾下！")"""

    text = replace_exact(text, old_exit, new_exit, "SM_CloseAndRelease exit full state")

    out = text.replace("\n", "\r\n") if has_crlf else text
    with open(J_PATH, "wb") as f:
        f.write(out.encode("utf-8"))

    print("Successfully applied v6.10 patches to payload/war3map.j")


if __name__ == "__main__":
    main()
