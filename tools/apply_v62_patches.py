# -*- coding: utf-8 -*-
import sys

def apply_patches():
    with open('payload/war3map.j', 'rb') as f:
        content = f.read().decode('utf-8')

    is_crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    patches = []

    # 1. Add Refuge safe coordinates globals
    target_1 = """    // Human Player Invulnerable Refuge System (测试酒馆·无敌避难所)
    unit array udg_RefugeBuilding
    integer udg_RefugeDeadCount = 0
    unit array udg_RefugeDeadUnit
    real array udg_RefugeDeadTime"""

    replacement_1 = """    // Human Player Invulnerable Refuge System (测试酒馆·无敌避难所)
    unit array udg_RefugeBuilding
    integer udg_RefugeDeadCount = 0
    unit array udg_RefugeDeadUnit
    real array udg_RefugeDeadTime
    real udg_Refuge_SafeX = 0.0
    real udg_Refuge_SafeY = 0.0"""
    patches.append(("Refuge safe coordinates globals", target_1, replacement_1))

    # 2. Add safety detection helpers and rewrite Refuge_InitForPlayer
    target_2 = """//***************************************************************************
//*
//*  Human Player Invulnerable Refuge System (测试酒馆·无敌避难所)
//*
//***************************************************************************

function Refuge_InitForPlayer takes player p returns nothing
    local integer pId = GetPlayerId(p)
    local real startX = GetStartLocationX(GetPlayerStartLocation(p))
    local real startY = GetStartLocationY(GetPlayerStartLocation(p))
    local real minX = GetRectMinX(bj_mapInitialPlayableArea) + 600.0
    local real maxX = GetRectMaxX(bj_mapInitialPlayableArea) - 600.0
    local real minY = GetRectMinY(bj_mapInitialPlayableArea) + 600.0
    local real maxY = GetRectMaxY(bj_mapInitialPlayableArea) - 600.0
    local real bestX = minX
    local real bestY = minY
    local real minD = 9999999999.0
    local real dx = 0.0
    local real dy = 0.0
    local real d = 0.0
    local real searchR = 0.0
    local real searchAngle = 0.0
    local real testX = minX
    local real testY = minY
    local boolean found = false
    local unit u = null

    // Check corner 0 (Bottom-Left)
    set dx = startX - minX
    set dy = startY - minY
    set d = dx * dx + dy * dy
    if d < minD then
        set minD = d
        set bestX = minX
        set bestY = minY
    endif

    // Check corner 1 (Top-Left)
    set dx = startX - minX
    set dy = startY - maxY
    set d = dx * dx + dy * dy
    if d < minD then
        set minD = d
        set bestX = minX
        set bestY = maxY
    endif

    // Check corner 2 (Bottom-Right)
    set dx = startX - maxX
    set dy = startY - minY
    set d = dx * dx + dy * dy
    if d < minD then
        set minD = d
        set bestX = maxX
        set bestY = minY
    endif

    // Check corner 3 (Top-Right)
    set dx = startX - maxX
    set dy = startY - maxY
    set d = dx * dx + dy * dy
    if d < minD then
        set minD = d
        set bestX = maxX
        set bestY = maxY
    endif

    // Spiral search around closest corner for buildable & walkable point
    set testX = bestX
    set testY = bestY
    set searchR = 0.0
    set searchAngle = 0.0
    loop
        exitwhen searchR > 1500.0 or found
        set testX = bestX + searchR * Cos(searchAngle)
        set testY = bestY + searchR * Sin(searchAngle)
        if testX >= minX - 300.0 and testX <= maxX + 300.0 and testY >= minY - 300.0 and testY <= maxY + 300.0 then
            if not IsTerrainPathable(testX, testY, PATHING_TYPE_BUILDABILITY) and not IsTerrainPathable(testX, testY, PATHING_TYPE_WALKABILITY) then
                set found = true
            endif
        endif
        if not found then
            set searchAngle = searchAngle + 0.5
            set searchR = searchR + 5.093
        endif
    endloop

    if not found then
        set testX = startX + 800.0
        set testY = startY + 800.0
    endif

    set u = CreateUnit(p, 'n003', testX, testY, 270.0)
    call SetUnitInvulnerable(u, true)
    set udg_RefugeBuilding[pId] = u

    if GetLocalPlayer() == p then
        call PingMinimapEx(testX, testY, 8.0, 0, 255, 0, true)
    endif
    call DisplayTimedTextToPlayer(p, 0, 0, 10.0, "|cff00ff00[测试避难所]|r 已在地图角落生成无敌避难所：主基地被摧毁也不会判负，阵亡英雄可在此复活。输入 |-refuge|r 可迁至英雄身旁。")

    set u = null
    set p = null
endfunction"""

    replacement_2 = """//***************************************************************************
//*
//*  Human Player Invulnerable Refuge System (测试酒馆·无敌避难所)
//*
//***************************************************************************

function Refuge_IsSafeTerrainPoint takes real x, real y, integer targetCliff, boolean requireBuild returns boolean
    if x < GetRectMinX(bj_mapInitialPlayableArea) + 256.0 or x > GetRectMaxX(bj_mapInitialPlayableArea) - 256.0 or y < GetRectMinY(bj_mapInitialPlayableArea) + 256.0 or y > GetRectMaxY(bj_mapInitialPlayableArea) - 256.0 then
        return false
    endif
    if GetTerrainCliffLevel(x, y) != targetCliff then
        return false
    endif
    if IsTerrainPathable(x, y, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if requireBuild and IsTerrainPathable(x, y, PATHING_TYPE_BUILDABILITY) then
        return false
    endif

    // Check surrounding 8 directions at radius 224.0
    if GetTerrainCliffLevel(x + 224.0, y) != targetCliff or IsTerrainPathable(x + 224.0, y, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x - 224.0, y) != targetCliff or IsTerrainPathable(x - 224.0, y, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x, y + 224.0) != targetCliff or IsTerrainPathable(x, y + 224.0, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x, y - 224.0) != targetCliff or IsTerrainPathable(x, y - 224.0, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x + 160.0, y + 160.0) != targetCliff or IsTerrainPathable(x + 160.0, y + 160.0, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x + 160.0, y - 160.0) != targetCliff or IsTerrainPathable(x + 160.0, y - 160.0, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x - 160.0, y + 160.0) != targetCliff or IsTerrainPathable(x - 160.0, y + 160.0, PATHING_TYPE_WALKABILITY) then
        return false
    endif
    if GetTerrainCliffLevel(x - 160.0, y - 160.0) != targetCliff or IsTerrainPathable(x - 160.0, y - 160.0, PATHING_TYPE_WALKABILITY) then
        return false
    endif

    return true
endfunction

function Refuge_CalcSafeReviveXY takes real cx, real cy, real startX, real startY returns nothing
    local integer baseCliff = GetTerrainCliffLevel(startX, startY)
    local real r = 160.0
    local real angle = 0.0
    local real rx = 0.0
    local real ry = 0.0
    local boolean found = false

    loop
        exitwhen r > 520.0 or found
        set rx = cx + r * Cos(angle)
        set ry = cy + r * Sin(angle)
        if GetTerrainCliffLevel(rx, ry) == baseCliff and not IsTerrainPathable(rx, ry, PATHING_TYPE_WALKABILITY) then
            if GetTerrainCliffLevel(rx + 96.0, ry) == baseCliff and not IsTerrainPathable(rx + 96.0, ry, PATHING_TYPE_WALKABILITY) then
                if GetTerrainCliffLevel(rx - 96.0, ry) == baseCliff and not IsTerrainPathable(rx - 96.0, ry, PATHING_TYPE_WALKABILITY) then
                    if GetTerrainCliffLevel(rx, ry + 96.0) == baseCliff and not IsTerrainPathable(rx, ry + 96.0, PATHING_TYPE_WALKABILITY) then
                        if GetTerrainCliffLevel(rx, ry - 96.0) == baseCliff and not IsTerrainPathable(rx, ry - 96.0, PATHING_TYPE_WALKABILITY) then
                            set found = true
                        endif
                    endif
                endif
            endif
        endif
        if not found then
            set angle = angle + 0.5
            set r = r + 8.0
        endif
    endloop

    if found then
        set udg_Refuge_SafeX = rx
        set udg_Refuge_SafeY = ry
    else
        set udg_Refuge_SafeX = startX
        set udg_Refuge_SafeY = startY
    endif
endfunction

function Refuge_InitForPlayer takes player p returns nothing
    local integer pId = GetPlayerId(p)
    local real startX = GetStartLocationX(GetPlayerStartLocation(p))
    local real startY = GetStartLocationY(GetPlayerStartLocation(p))
    local integer baseCliff = GetTerrainCliffLevel(startX, startY)
    local real outAngle = Atan2(startY, startX)
    local real searchR = 0.0
    local real angle = 0.0
    local real testX = startX
    local real testY = startY
    local integer k = 0
    local boolean found = false
    local unit u = null

    // Pass 1: Same cliff level connected plateau behind/beside base
    set searchR = 550.0
    loop
        exitwhen searchR > 1600.0 or found
        set k = 0
        loop
            exitwhen k >= 16 or found
            set angle = outAngle + I2R(k) * 0.3927
            set testX = startX + searchR * Cos(angle)
            set testY = startY + searchR * Sin(angle)
            if Refuge_IsSafeTerrainPoint(testX, testY, baseCliff, true) then
                if GetTerrainCliffLevel(startX + (testX - startX) * 0.25, startY + (testY - startY) * 0.25) == baseCliff and GetTerrainCliffLevel(startX + (testX - startX) * 0.50, startY + (testY - startY) * 0.50) == baseCliff and GetTerrainCliffLevel(startX + (testX - startX) * 0.75, startY + (testY - startY) * 0.75) == baseCliff then
                    set found = true
                endif
            endif
            set k = k + 1
        endloop
        if not found then
            set searchR = searchR + 128.0
        endif
    endloop

    // Pass 2: Relaxed search on same cliff level
    if not found then
        set searchR = 400.0
        loop
            exitwhen searchR > 1800.0 or found
            set k = 0
            loop
                exitwhen k >= 16 or found
                set angle = outAngle + I2R(k) * 0.3927
                set testX = startX + searchR * Cos(angle)
                set testY = startY + searchR * Sin(angle)
                if Refuge_IsSafeTerrainPoint(testX, testY, baseCliff, true) then
                    set found = true
                endif
                set k = k + 1
            endloop
            if not found then
                set searchR = searchR + 128.0
            endif
        endloop
    endif

    // Final fallback
    if not found then
        set testX = startX
        set testY = startY
    endif

    set u = CreateUnit(p, 'n003', testX, testY, 270.0)
    call SetUnitInvulnerable(u, true)
    set udg_RefugeBuilding[pId] = u

    if GetLocalPlayer() == p then
        call PingMinimapEx(testX, testY, 8.0, 0, 255, 0, true)
    endif
    call DisplayTimedTextToPlayer(p, 0, 0, 10.0, "|cff00ff00[测试避难所]|r 已在基地安全平地生成无敌避难所：主基地被摧毁也不会判负，阵亡英雄可在此复活。输入 |-refuge|r 可迁至英雄身旁，输入 |-unstuck|r 可紧急脱离卡点。")

    set u = null
    set p = null
endfunction"""
    patches.append(("Safety helpers & Refuge_InitForPlayer rewrite", target_2, replacement_2))

    # 3. Fix Refuge_Relocate (-refuge)
    target_3 = """    if heroU != null then
        set tx = GetUnitX(heroU)
        set ty = GetUnitY(heroU)
    else
        set tx = GetStartLocationX(GetPlayerStartLocation(p))
        set ty = GetStartLocationY(GetPlayerStartLocation(p))
    endif

    // 2. Spiral search nearby buildable & walkable point
    set px = tx
    set py = ty
    loop
        exitwhen searchR > 800.0 or found
        set px = tx + searchR * Cos(searchAngle)
        set py = ty + searchR * Sin(searchAngle)
        if not IsTerrainPathable(px, py, PATHING_TYPE_BUILDABILITY) and not IsTerrainPathable(px, py, PATHING_TYPE_WALKABILITY) then
            set found = true
        else
            set searchAngle = searchAngle + 0.6
            set searchR = searchR + 8.0
        endif
    endloop

    if not found then
        set px = tx + 200.0
        set py = ty + 200.0
    endif"""

    replacement_3 = """    if heroU != null then
        set tx = GetUnitX(heroU)
        set ty = GetUnitY(heroU)
    else
        set tx = GetStartLocationX(GetPlayerStartLocation(p))
        set ty = GetStartLocationY(GetPlayerStartLocation(p))
    endif
    set targetCliff = GetTerrainCliffLevel(tx, ty)

    // 2. Spiral search nearby buildable & walkable point on same cliff level
    set px = tx
    set py = ty
    loop
        exitwhen searchR > 900.0 or found
        set px = tx + searchR * Cos(searchAngle)
        set py = ty + searchR * Sin(searchAngle)
        if Refuge_IsSafeTerrainPoint(px, py, targetCliff, true) then
            set found = true
        else
            set searchAngle = searchAngle + 0.6
            set searchR = searchR + 8.0
        endif
    endloop

    if not found then
        set px = tx
        set py = ty
    endif"""
    patches.append(("Refuge_Relocate safe cliff search", target_3, replacement_3))

    # 3b. Add local integer targetCliff = 0 in Refuge_Relocate
    target_3b = """function Refuge_Relocate takes player p returns nothing
    local integer pId = GetPlayerId(p)
    local unit heroU = null
    local group g = null
    local unit u = null
    local real tx = 0.0
    local real ty = 0.0
    local real searchR = 250.0"""

    replacement_3b = """function Refuge_Relocate takes player p returns nothing
    local integer pId = GetPlayerId(p)
    local unit heroU = null
    local group g = null
    local unit u = null
    local real tx = 0.0
    local real ty = 0.0
    local integer targetCliff = 0
    local real searchR = 250.0"""
    patches.append(("Refuge_Relocate targetCliff local", target_3b, replacement_3b))

    # 4. Fix Refuge_ProcessRevives
    target_4 = """                set pId = GetPlayerId(GetOwningPlayer(u))
                set ref = udg_RefugeBuilding[pId]
                if ref != null and not IsUnitType(ref, UNIT_TYPE_DEAD) and GetWidgetLife(ref) > 0.405 then
                    call ReviveHero(u, GetUnitX(ref), GetUnitY(ref) - 150.0, true)
                    call Strain_ApplyCrippledClampOnRevive(u)
                    if GetUnitTypeId(u) == 'H005' then
                        call Wild_ClearMorphAbil(u, pId)
                        call Wild_RevertToAvatar(u)
                    elseif GetUnitTypeId(u) == 'H004' then
                        call Strain_ApplyCurrentSkin(u, pId)
                        call Strain_UpdateEvoUI(pId)
                    elseif GetUnitTypeId(u) == 'H006' then
                        call Maho_ApplyAppearance(u, pId)
                        call Maho_UpdateUI(pId)
                    endif
                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", GetUnitX(ref), GetUnitY(ref) - 150.0))
                    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 6.0, "|cff00ff00[避难所复活]|r 你的英雄已在无敌避难所免费自动复活！")"""

    replacement_4 = """                set pId = GetPlayerId(GetOwningPlayer(u))
                set ref = udg_RefugeBuilding[pId]
                if ref != null and not IsUnitType(ref, UNIT_TYPE_DEAD) and GetWidgetLife(ref) > 0.405 then
                    call Refuge_CalcSafeReviveXY(GetUnitX(ref), GetUnitY(ref), GetStartLocationX(GetPlayerStartLocation(Player(pId))), GetStartLocationY(GetPlayerStartLocation(Player(pId))))
                    call ReviveHero(u, udg_Refuge_SafeX, udg_Refuge_SafeY, true)
                    call Strain_ApplyCrippledClampOnRevive(u)
                    if GetUnitTypeId(u) == 'H005' then
                        call Wild_ClearMorphAbil(u, pId)
                        call Wild_RevertToAvatar(u)
                    elseif GetUnitTypeId(u) == 'H004' then
                        call Strain_ApplyCurrentSkin(u, pId)
                        call Strain_UpdateEvoUI(pId)
                    elseif GetUnitTypeId(u) == 'H006' then
                        call Maho_ApplyAppearance(u, pId)
                        call Maho_UpdateUI(pId)
                    endif
                    call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Human\\\\Resurrect\\\\ResurrectTarget.mdl", udg_Refuge_SafeX, udg_Refuge_SafeY))
                    call DisplayTimedTextToPlayer(Player(pId), 0, 0, 6.0, "|cff00ff00[避难所复活]|r 你的英雄已在无敌避难所免费自动复活！")"""
    patches.append(("Refuge_ProcessRevives safe revive position", target_4, replacement_4))

    # 5. Wild_OnHeroReviveFinish protect manual tavern/altar revive
    target_5 = """function Wild_OnHeroReviveFinish takes nothing returns boolean
    local unit rev = GetRevivingUnit()
    local integer pId = 0
    if rev == null then
        set rev = GetTriggerUnit()
    endif
    if rev != null then
        call Strain_ApplyCrippledClampOnRevive(rev)
    endif"""

    replacement_5 = """function Wild_OnHeroReviveFinish takes nothing returns boolean
    local unit rev = GetRevivingUnit()
    local integer pId = 0
    local player revOwner = null
    local real startX = 0.0
    local real startY = 0.0
    local integer baseCliff = 0
    local real rx = 0.0
    local real ry = 0.0

    if rev == null then
        set rev = GetTriggerUnit()
    endif
    if rev != null then
        call Strain_ApplyCrippledClampOnRevive(rev)
        set revOwner = GetOwningPlayer(rev)
        if GetPlayerController(revOwner) == MAP_CONTROL_USER then
            set pId = GetPlayerId(revOwner)
            set startX = GetStartLocationX(GetPlayerStartLocation(revOwner))
            set startY = GetStartLocationY(GetPlayerStartLocation(revOwner))
            set baseCliff = GetTerrainCliffLevel(startX, startY)
            set rx = GetUnitX(rev)
            set ry = GetUnitY(rev)
            if IsTerrainPathable(rx, ry, PATHING_TYPE_WALKABILITY) or (GetTerrainCliffLevel(rx, ry) != baseCliff and (udg_RefugeBuilding[pId] == null or GetTerrainCliffLevel(rx, ry) != GetTerrainCliffLevel(GetUnitX(udg_RefugeBuilding[pId]), GetUnitY(udg_RefugeBuilding[pId])))) then
                if udg_RefugeBuilding[pId] != null and not IsUnitType(udg_RefugeBuilding[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_RefugeBuilding[pId]) > 0.405 then
                    call Refuge_CalcSafeReviveXY(GetUnitX(udg_RefugeBuilding[pId]), GetUnitY(udg_RefugeBuilding[pId]), startX, startY)
                else
                    call Refuge_CalcSafeReviveXY(startX, startY, startX, startY)
                endif
                call SetUnitPosition(rev, udg_Refuge_SafeX, udg_Refuge_SafeY)
            endif
        endif
        set revOwner = null
    endif"""
    patches.append(("Wild_OnHeroReviveFinish manual revive protection", target_5, replacement_5))

    # 6. TM_OnChatCommand add -unstuck
    target_6 = """function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    local integer pId = 0
    local unit u = null"""

    replacement_6 = """function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    local integer pId = 0
    local unit u = null
    local group g = null
    local real startX = 0.0
    local real startY = 0.0"""
    patches.append(("TM_OnChatCommand locals", target_6, replacement_6))

    target_7 = """    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    elseif s == "-anti" then"""

    replacement_7 = """    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    elseif s == "-unstuck" then
        set g = CreateGroup()
        set startX = GetStartLocationX(GetPlayerStartLocation(p))
        set startY = GetStartLocationY(GetPlayerStartLocation(p))
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set u = FirstOfGroup(g)
            exitwhen u == null
            call GroupRemoveUnit(g, u)
            if IsUnitType(u, UNIT_TYPE_HERO) and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
                call SetUnitPosition(u, startX, startY)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\MassTeleport\\\\MassTeleportTarget.mdl", u, "origin"))
            endif
        endloop
        call DestroyGroup(g)
        set g = null
        if GetLocalPlayer() == p then
            call PingMinimapEx(startX, startY, 5.0, 0, 255, 0, true)
        endif
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[脱离卡点]|r 已将你的英雄安全传送回出生点平地！")
    elseif s == "-anti" then"""
    patches.append(("TM_OnChatCommand -unstuck command", target_7, replacement_7))

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
    print("All patches successfully applied to payload/war3map.j for v6.2!")

if __name__ == '__main__':
    apply_patches()
