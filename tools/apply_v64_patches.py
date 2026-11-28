# -*- coding: utf-8 -*-
"""
v6.4 紧急热修与全图通缉广播补丁：
1. 新增 udg_Asn_WorldRect = GetWorldBounds()，无死角扫描全图敌对高价值单位。
2. 彻底废除会导致引用计数叠加卡死隐藏的 BlzUnitHideAbility，改用 UnitRemoveAbility + UnitAddAbility 零故障刷新敌方头像与悬赏槽。
3. 新增 Asn_GetPlayerFactionName，下单时向全图广播【某势力 · 某某英雄】已被下单买命通缉。
4. 优化望远镜按钮 (A05A)：点击时不仅刷新榜单，还会直接打印所有当前上榜敌方目标与报价清单。
"""

JASS_PATH = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j"


def apply():
    with open(JASS_PATH, "r", encoding="utf-8") as f:
        txt = f.read().replace("\r\n", "\n")

    patches = []

    # 1. 添加 udg_Asn_WorldRect 全局变量
    t1 = """    integer udg_Asn_KillerCount = 0"""
    r1 = """    integer udg_Asn_KillerCount = 0
    rect udg_Asn_WorldRect = null"""
    patches.append(("Add udg_Asn_WorldRect global", t1, r1))

    # 2. 在 Asn_GetDefaultHumanBuyer 后新增 Asn_GetPlayerFactionName 并重写 Asn_SetShopAbilVisible 为 UnitRemove/AddAbility
    t2 = """function Asn_SetShopAbilVisible takes integer slotIdx, boolean visible returns nothing
    local integer abilId = udg_Asn_SlotAbil[slotIdx]
    local integer s = 0
    loop
        exitwhen s >= udg_Asn_ShopCount
        if udg_Asn_Shop[s] != null then
            call BlzUnitHideAbility(udg_Asn_Shop[s], abilId, not visible)
        endif
        set s = s + 1
    endloop
    set udg_Asn_SlotHidden[slotIdx] = not visible
endfunction"""

    r2 = """function Asn_GetPlayerFactionName takes player p returns string
    local integer pid = 0
    if p == null then
        return "未知势力"
    endif
    set pid = GetPlayerId(p)
    if pid == 0 then
        return "|cffff3333红方(" + GetPlayerName(p) + ")|r"
    elseif pid == 1 then
        return "|cff3399ff蓝方(" + GetPlayerName(p) + ")|r"
    elseif pid == 2 then
        return "|cff00e6c8青方(" + GetPlayerName(p) + ")|r"
    elseif pid == 3 then
        return "|cff9944ff紫方(" + GetPlayerName(p) + ")|r"
    elseif pid == 4 then
        return "|cffffff33黄方(" + GetPlayerName(p) + ")|r"
    elseif pid == 5 then
        return "|cffff8822橙方(" + GetPlayerName(p) + ")|r"
    elseif pid == 6 then
        return "|cff33dd33绿方(" + GetPlayerName(p) + ")|r"
    elseif pid == 7 then
        return "|cffff77cc粉方(" + GetPlayerName(p) + ")|r"
    elseif pid == PLAYER_NEUTRAL_AGGRESSIVE or pid == 24 then
        return "|cffff5522中立敌对势力|r"
    endif
    return "|cffcccccc" + GetPlayerName(p) + "|r"
endfunction

function Asn_SetShopAbilVisible takes integer slotIdx, boolean visible returns nothing
    local integer abilId = udg_Asn_SlotAbil[slotIdx]
    local integer s = 0
    loop
        exitwhen s >= udg_Asn_ShopCount
        if udg_Asn_Shop[s] != null then
            call UnitRemoveAbility(udg_Asn_Shop[s], abilId)
            if visible then
                call UnitAddAbility(udg_Asn_Shop[s], abilId)
                call UnitMakeAbilityPermanent(udg_Asn_Shop[s], true, abilId)
            endif
        endif
        set s = s + 1
    endloop
    set udg_Asn_SlotHidden[slotIdx] = not visible
endfunction"""
    patches.append(("Add Asn_GetPlayerFactionName & rewrite Asn_SetShopAbilVisible", t2, r2))

    # 3. 更新 Asn_RefreshBoard 使用 udg_Asn_WorldRect 并消除二次隐藏问题
    t3 = """    // 扫描全图敌对高价值目标（英雄 + 沙盒Boss + 涅槃金卵对应的魔虚罗）
    call GroupEnumUnitsInRect(g, bj_mapInitialPlayableArea, null)"""
    r3 = """    // 扫描全图敌对高价值目标（英雄 + 沙盒Boss + 涅槃金卵对应的魔虚罗）
    if udg_Asn_WorldRect == null then
        set udg_Asn_WorldRect = GetWorldBounds()
    endif
    call GroupEnumUnitsInRect(g, udg_Asn_WorldRect, null)"""
    patches.append(("Use udg_Asn_WorldRect in Asn_RefreshBoard", t3, r3))

    t4 = """            if udg_Asn_SlotHidden[s] or udg_Asn_SlotLastUnit[s] != u or udg_Asn_SlotLastIcon[s] != iconPath then
                call BlzSetAbilityIcon(abilId, iconPath)
                set udg_Asn_SlotLastIcon[s] = iconPath
                set udg_Asn_SlotLastUnit[s] = u
                call Asn_SetShopAbilVisible(s, false)
                call Asn_SetShopAbilVisible(s, true)
            endif
            call BlzSetAbilityTooltip(abilId, tipStr, 0)
            call BlzSetAbilityExtendedTooltip(abilId, extStr, 0)"""
    r4 = """            call BlzSetAbilityTooltip(abilId, tipStr, 0)
            call BlzSetAbilityExtendedTooltip(abilId, extStr, 0)
            if udg_Asn_SlotHidden[s] or udg_Asn_SlotLastUnit[s] != u or udg_Asn_SlotLastIcon[s] != iconPath then
                call BlzSetAbilityIcon(abilId, iconPath)
                set udg_Asn_SlotLastIcon[s] = iconPath
                set udg_Asn_SlotLastUnit[s] = u
                call Asn_SetShopAbilVisible(s, true)
            endif"""
    patches.append(("Fix slot visibility refresh without double-hide bug", t4, r4))

    # 4. 望远镜按钮列出全部当前可下单敌方英雄与报价 + 下单全图广播某势力某某英雄被通缉
    t5 = """    if abilId == 'A05A' then
        call Asn_RefreshBoard()
        call DisplayTimedTextToPlayer(buyer, 0, 0, 8.0, "|cffffcc00【暗杀介绍所 · 实时情报】|r 悬赏榜头像与报价已同步刷新！输入 |-kill|r 可快捷定位介绍所。")
        set i = 0
        loop
            exitwhen i >= 8
            if udg_Asn_ConActive[i] and udg_Asn_ConTarget[i] != null then
                call DisplayTimedTextToPlayer(buyer, 0, 0, 8.0, "  • 进行中契约 #" + I2S(i + 1) + "：追杀 |cffff3366" + Asn_GetUnitDisplayLabel(udg_Asn_ConTarget[i]) + "|r（当前第 " + I2S(udg_Asn_ConWave[i]) + " 波）")
            endif
            set i = i + 1
        endloop
        set buyer = null
        return true
    endif"""

    r5 = """    if abilId == 'A05A' then
        call Asn_RefreshBoard()
        call DisplayTimedTextToPlayer(buyer, 0, 0, 10.0, "|cffffcc00【暗杀介绍所 · 实时悬赏榜单】|r 敌方头像与报价已刷新：")
        set i = 0
        set aliveK = 0
        loop
            exitwhen i >= 10
            if udg_Asn_BoardUnit[i] != null then
                set aliveK = aliveK + 1
                call DisplayTimedTextToPlayer(buyer, 0, 0, 10.0, "  [" + I2S(i + 1) + "] " + Asn_GetPlayerFactionName(GetOwningPlayer(udg_Asn_BoardUnit[i])) + " · |cffffffff" + Asn_GetUnitDisplayLabel(udg_Asn_BoardUnit[i]) + "|r — 报价 |cffffdd44" + I2S(udg_Asn_BoardPrice[i]) + " 黄金|r")
            endif
            set i = i + 1
        endloop
        if aliveK == 0 then
            call DisplayTimedTextToPlayer(buyer, 0, 0, 8.0, "  |cffaaaaaa（当前全图尚未发现存活的敌方英雄或Boss，请稍待电脑出英雄或输入 -archimonde 测试）|r")
        endif
        set i = 0
        loop
            exitwhen i >= 8
            if udg_Asn_ConActive[i] and udg_Asn_ConTarget[i] != null then
                call DisplayTimedTextToPlayer(buyer, 0, 0, 10.0, "  • 进行中契约 #" + I2S(i + 1) + "：" + Asn_GetPlayerFactionName(udg_Asn_ConVictimOwner[i]) + " 【" + Asn_GetUnitDisplayLabel(udg_Asn_ConTarget[i]) + "】（第 " + I2S(udg_Asn_ConWave[i]) + " 波）")
            endif
            set i = i + 1
        endloop
        set buyer = null
        return true
    endif"""
    patches.append(("Enhance A05A board report with faction and quotes", t5, r5))

    t6 = """    call DisplayTimedTextToPlayer(buyer, 0, 0, 6.0, "|cff00ff80[契约成立]|r 已支付 |cffffdd44" + I2S(quote) + "|r 黄金！幽影公会绝不受任何人操纵，杀手小队不死不休！")
    call Asn_SpawnWave(freeC)"""

    r6 = """    call DisplayTimedTextToPlayer(buyer, 0, 0, 6.0, "|cff00ff80[契约成立]|r 已支付 |cffffdd44" + I2S(quote) + "|r 黄金！幽影公会绝不受任何人操纵，杀手小队不死不休！")
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING then
            call DisplayTimedTextToPlayer(Player(i), 0, 0, 8.0, "|cffff2244【全图通缉 · 暗杀契约生效！】|r " + Asn_GetPlayerFactionName(GetOwningPlayer(tgt)) + " 的 |cffffcc00【" + Asn_GetUnitDisplayLabel(tgt) + "】|r 已经被下单买命（悬赏 |cffffdd44" + I2S(quote) + " 黄金|r）！幽影公会已派出 " + Asn_GetKillerSquadName(udg_Asn_ConKillerType[freeC]) + "，不死不休！")
        endif
        set i = i + 1
    endloop
    call PingMinimapEx(GetUnitX(tgt), GetUnitY(tgt), 5.0, 255, 40, 40, true)
    call Asn_SpawnWave(freeC)"""
    patches.append(("Add global assassination broadcast to all players", t6, r6))

    # 5. Asn_InitSystem 中初始化 udg_Asn_WorldRect 并在创建 n005 后立刻显式移除初始空槽再刷新
    t7 = """    set s1 = Asn_SpawnAgencyAt(-5760.0, -128.0)
    set s2 = Asn_SpawnAgencyAt(5120.0, -192.0)
    if s1 != null then
        call PingMinimapEx(GetUnitX(s1), GetUnitY(s1), 6.0, 255, 40, 120, false)
    endif
    if s2 != null then
        call PingMinimapEx(GetUnitX(s2), GetUnitY(s2), 6.0, 255, 40, 120, false)
    endif
    set s1 = null
    set s2 = null

    call Asn_RefreshBoard()"""

    r7 = """    set udg_Asn_WorldRect = GetWorldBounds()
    set s1 = Asn_SpawnAgencyAt(-5760.0, -128.0)
    set s2 = Asn_SpawnAgencyAt(5120.0, -192.0)
    if s1 != null then
        call PingMinimapEx(GetUnitX(s1), GetUnitY(s1), 6.0, 255, 40, 120, false)
    endif
    if s2 != null then
        call PingMinimapEx(GetUnitX(s2), GetUnitY(s2), 6.0, 255, 40, 120, false)
    endif
    set s1 = null
    set s2 = null

    set i = 0
    loop
        exitwhen i >= 10
        call Asn_SetShopAbilVisible(i, false)
        set i = i + 1
    endloop
    call Asn_RefreshBoard()"""
    patches.append(("Init world rect and clean empty slots in Asn_InitSystem", t7, r7))

    for name, tgt, rep in patches:
        cnt = txt.count(tgt)
        if cnt != 1:
            raise RuntimeError(f"Patch '{name}' expected count 1, got {cnt}")
        txt = txt.replace(tgt, rep, 1)
        print(f"[ok] {name}")

    with open(JASS_PATH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(txt)
    print(f"[DONE] v6.4 war3map.j updated ({len(txt.splitlines())} lines)")


if __name__ == "__main__":
    apply()
