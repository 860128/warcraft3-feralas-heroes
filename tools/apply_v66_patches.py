# -*- coding: utf-8 -*-
import os

TARGET_PATH = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    cnt = text.count(old)
    assert cnt == 1, f"[{label}] Expected 1 occurrence, found {cnt}"
    return text.replace(old, new, 1)


def main():
    with open(TARGET_PATH, 'rb') as f:
        raw = f.read()

    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw[3:].decode('utf-8') if has_bom else raw.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    # 1. Global toggle udg_Asn_AllowSelfTest
    text = replace_once(
        text,
        r'''    integer udg_Asn_KillerCount = 0
    rect udg_Asn_WorldRect = null''',
        r'''    integer udg_Asn_KillerCount = 0
    rect udg_Asn_WorldRect = null
    boolean udg_Asn_AllowSelfTest = true''',
        '1_global_toggle'
    )

    # 2. Asn_RefreshBoard: locals, filter, sort, tooltips
    old_refresh = r'''function Asn_RefreshBoard takes nothing returns nothing
    local player buyer = Asn_GetDefaultHumanBuyer()
    local unit array cands
    local integer array candQuotes
    local integer candCount = 0
    local group g = CreateGroup()
    local unit u = null
    local unit trueT = null
    local integer s = 0
    local integer j = 0
    local boolean dup = false
    local integer tmpQ = 0
    local unit tmpU = null
    local integer abilId = 0
    local integer conIdx = -1
    local string iconPath = ""
    local string tipStr = ""
    local string extStr = ""
    local string label = ""
    local integer kType = 0
    local integer ut = 0

    // 扫描全图敌对高价值目标（英雄 + 沙盒Boss + 涅槃金卵对应的魔虚罗）
    if udg_Asn_WorldRect == null then
        set udg_Asn_WorldRect = GetWorldBounds()
    endif
    call GroupEnumUnitsInRect(g, udg_Asn_WorldRect, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        set ut = GetUnitTypeId(u)
        if not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) and ut != 'u000' and ut != 'u001' and ut != 'u002' and ut != 'u003' and ut != 'n003' and ut != 'n005' and not Asn_IsAssassinType(ut) then
            if IsUnitEnemy(u, buyer) and (IsUnitType(u, UNIT_TYPE_HERO) or ut == 'Uwar' or ut == 'Nklj' or ut == 'Nman' or ut == 'Nmag' or ut == 'u004') then
                set trueT = Asn_GetTargetTrueUnit(u)
                if trueT != null then
                    set dup = false
                    set j = 0
                    loop
                        exitwhen j >= candCount or dup
                        if cands[j] == trueT then
                            set dup = true
                        endif
                        set j = j + 1
                    endloop
                    if not dup and candCount < 24 then
                        set cands[candCount] = trueT
                        set candQuotes[candCount] = Asn_CalcQuote(trueT)
                        set candCount = candCount + 1
                    endif
                endif
            endif
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set u = null
    set trueT = null

    // 按身价降序排列（最强/最贵目标靠前）
    set s = 0
    loop
        exitwhen s >= candCount - 1
        set j = s + 1
        loop
            exitwhen j >= candCount
            if candQuotes[j] > candQuotes[s] then
                set tmpQ = candQuotes[s]
                set candQuotes[s] = candQuotes[j]
                set candQuotes[j] = tmpQ
                set tmpU = cands[s]
                set cands[s] = cands[j]
                set cands[j] = tmpU
            endif
            set j = j + 1
        endloop
        set s = s + 1
    endloop
    set tmpU = null

    // 刷新 10 个暗杀悬赏槽位
    set s = 0
    loop
        exitwhen s >= 10
        set abilId = udg_Asn_SlotAbil[s]
        if s < candCount then
            set u = cands[s]
            set udg_Asn_BoardUnit[s] = u
            set udg_Asn_BoardPrice[s] = candQuotes[s]
            set kType = Asn_GetCounterTypeForTarget(u)
            set udg_Asn_BoardKillerType[s] = kType
            set conIdx = Asn_FindContractByTarget(u)
            set label = Asn_GetUnitDisplayLabel(u)
            set iconPath = Asn_GetUnitIconPath(u)

            if conIdx >= 0 then
                set tipStr = "|cffff3366[追杀中·第" + I2S(udg_Asn_ConWave[conIdx]) + "波]|r " + label + " (已签约)"
                set extStr = "|cffff3366【幽影公会 · 契约执行中】|r|n" + "当前目标：" + label + " (" + GetPlayerName(GetOwningPlayer(u)) + ")|n" + "实时战力：生命 " + I2S(R2I(GetUnitState(u, UNIT_STATE_MAX_LIFE))) + " | 基础攻击 " + I2S(BlzGetUnitBaseDamage(u, 0)) + " | 护甲 " + I2S(R2I(BlzGetUnitArmor(u))) + "|n" + "出动部队：" + Asn_GetKillerSquadName(kType) + "（第 " + I2S(udg_Asn_ConWave[conIdx]) + " 波）|n" + "|cff00ff80承诺：杀手不受任何控制且会自动清除路上阻碍者；若被消灭，3秒后自动派出更强波次直至目标必死！|r"
            else
                set tipStr = "|cffffcc00[暗杀悬赏]|r " + label + " — |cffffdd44" + I2S(candQuotes[s]) + " 黄金|r"
                set extStr = "目标身份：" + label + " (" + GetPlayerName(GetOwningPlayer(u)) + ")|n" + "目标属性：生命 " + I2S(R2I(GetUnitState(u, UNIT_STATE_MAX_LIFE))) + " | 攻击 " + I2S(BlzGetUnitBaseDamage(u, 0)) + " | 护甲 " + I2S(R2I(BlzGetUnitArmor(u))) + "|n" + "特派杀手：" + Asn_GetKillerSquadName(kType) + "|n" + "克制手段：" + Asn_GetCounterDesc(u) + "|n|n|cffffcc00雇佣报价：" + I2S(candQuotes[s]) + " 黄金|r（一次性买断！绝不受雇主控制，顺路摧毁一切阻拦者，若阵亡则无限增援更强波次直到目标彻底死亡！）"
            endif'''

    new_refresh = r'''function Asn_RefreshBoard takes nothing returns nothing
    local player buyer = Asn_GetDefaultHumanBuyer()
    local unit array cands
    local integer array candQuotes
    local integer candCount = 0
    local group g = CreateGroup()
    local unit u = null
    local unit trueT = null
    local integer s = 0
    local integer j = 0
    local boolean dup = false
    local integer tmpQ = 0
    local unit tmpU = null
    local integer abilId = 0
    local integer conIdx = -1
    local string iconPath = ""
    local string tipStr = ""
    local string extStr = ""
    local string label = ""
    local integer kType = 0
    local integer ut = 0
    local boolean sIsSelf = false
    local boolean jIsSelf = false
    local boolean isSelf = false

    // 扫描全图敌对高价值目标（测试模式开启 udg_Asn_AllowSelfTest 时同步纳入自身英雄用于极限耐力自测）
    if udg_Asn_WorldRect == null then
        set udg_Asn_WorldRect = GetWorldBounds()
    endif
    call GroupEnumUnitsInRect(g, udg_Asn_WorldRect, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        set ut = GetUnitTypeId(u)
        if not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) and ut != 'u000' and ut != 'u001' and ut != 'u002' and ut != 'u003' and ut != 'n003' and ut != 'n005' and not Asn_IsAssassinType(ut) then
            if (IsUnitEnemy(u, buyer) or (udg_Asn_AllowSelfTest and GetOwningPlayer(u) == buyer)) and (IsUnitType(u, UNIT_TYPE_HERO) or ut == 'Uwar' or ut == 'Nklj' or ut == 'Nman' or ut == 'Nmag' or ut == 'u004') then
                set trueT = Asn_GetTargetTrueUnit(u)
                if trueT != null then
                    set dup = false
                    set j = 0
                    loop
                        exitwhen j >= candCount or dup
                        if cands[j] == trueT then
                            set dup = true
                        endif
                        set j = j + 1
                    endloop
                    if not dup and candCount < 24 then
                        set cands[candCount] = trueT
                        set candQuotes[candCount] = Asn_CalcQuote(trueT)
                        set candCount = candCount + 1
                    endif
                endif
            endif
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set u = null
    set trueT = null

    // 测试模式下将自身英雄优先置于靠前槽位，其余按身价降序排列
    set s = 0
    loop
        exitwhen s >= candCount - 1
        set j = s + 1
        loop
            exitwhen j >= candCount
            set sIsSelf = (udg_Asn_AllowSelfTest and GetOwningPlayer(cands[s]) == buyer)
            set jIsSelf = (udg_Asn_AllowSelfTest and GetOwningPlayer(cands[j]) == buyer)
            if (jIsSelf and not sIsSelf) or (jIsSelf == sIsSelf and candQuotes[j] > candQuotes[s]) then
                set tmpQ = candQuotes[s]
                set candQuotes[s] = candQuotes[j]
                set candQuotes[j] = tmpQ
                set tmpU = cands[s]
                set cands[s] = cands[j]
                set cands[j] = tmpU
            endif
            set j = j + 1
        endloop
        set s = s + 1
    endloop
    set tmpU = null

    // 刷新 10 个暗杀悬赏槽位
    set s = 0
    loop
        exitwhen s >= 10
        set abilId = udg_Asn_SlotAbil[s]
        if s < candCount then
            set u = cands[s]
            set udg_Asn_BoardUnit[s] = u
            set udg_Asn_BoardPrice[s] = candQuotes[s]
            set kType = Asn_GetCounterTypeForTarget(u)
            set udg_Asn_BoardKillerType[s] = kType
            set conIdx = Asn_FindContractByTarget(u)
            set label = Asn_GetUnitDisplayLabel(u)
            set iconPath = Asn_GetUnitIconPath(u)
            set isSelf = (GetOwningPlayer(u) == buyer)

            if conIdx >= 0 then
                if isSelf then
                    set tipStr = "|cff00ffcc[自测进行中·第" + I2S(udg_Asn_ConWave[conIdx]) + "波]|r " + label + " (已撑过" + I2S(udg_Asn_ConWave[conIdx] - 1) + "波)"
                    set extStr = "|cff00ffcc【测试模式 · 自我暗杀极限挑战进行中】|r|n" + "当前受试英雄：" + label + " (" + GetPlayerName(GetOwningPlayer(u)) + ")|n" + "实时战力：生命 " + I2S(R2I(GetUnitState(u, UNIT_STATE_MAX_LIFE))) + " | 基础攻击 " + I2S(BlzGetUnitBaseDamage(u, 0)) + " | 护甲 " + I2S(R2I(BlzGetUnitArmor(u))) + "|n" + "当前波次：第 " + I2S(udg_Asn_ConWave[conIdx]) + " 波（已成功抵挡 " + I2S(udg_Asn_ConWave[conIdx] - 1) + " 波）|n" + "出动部队：" + Asn_GetKillerSquadName(kType) + "|n|cff00ff80提示：倒下后将结算最终抵挡波数；输入 -stopkill 可中途终止自测。|r"
                else
                    set tipStr = "|cffff3366[追杀中·第" + I2S(udg_Asn_ConWave[conIdx]) + "波]|r " + label + " (已签约)"
                    set extStr = "|cffff3366【幽影公会 · 契约执行中】|r|n" + "当前目标：" + label + " (" + GetPlayerName(GetOwningPlayer(u)) + ")|n" + "实时战力：生命 " + I2S(R2I(GetUnitState(u, UNIT_STATE_MAX_LIFE))) + " | 基础攻击 " + I2S(BlzGetUnitBaseDamage(u, 0)) + " | 护甲 " + I2S(R2I(BlzGetUnitArmor(u))) + "|n" + "出动部队：" + Asn_GetKillerSquadName(kType) + "（第 " + I2S(udg_Asn_ConWave[conIdx]) + " 波）|n" + "|cff00ff80承诺：杀手不受任何控制且会自动清除路上阻碍者；若被消灭，3秒后自动派出更强波次直至目标必死！|r"
                endif
            else
                if isSelf then
                    set tipStr = "|cff00ffcc[自测挑战·对自己下单]|r " + label + " — |cff00ff80免费(身价" + I2S(candQuotes[s]) + "金)|r"
                    set extStr = "|cff00ffcc【测试模式限定 · 自我暗杀极限挑战】|r|n" + "受试目标：" + label + " (" + GetPlayerName(GetOwningPlayer(u)) + ")|n" + "目标属性：生命 " + I2S(R2I(GetUnitState(u, UNIT_STATE_MAX_LIFE))) + " | 攻击 " + I2S(BlzGetUnitBaseDamage(u, 0)) + " | 护甲 " + I2S(R2I(BlzGetUnitArmor(u))) + "|n" + "特派杀手：" + Asn_GetKillerSquadName(kType) + "|n" + "克制手段：" + Asn_GetCounterDesc(u) + "|n|n|cffffcc00实时评估身价：" + I2S(candQuotes[s]) + " 黄金|r（|cff00ff80测试模式对自己下单完全免费！|r点击立即派出不死不休的针对性杀手波次，测测真人玩家能撑几波！后期正式版将移除此测试项，也可直接输入 -killme 快捷开战）"
                else
                    set tipStr = "|cffffcc00[暗杀悬赏]|r " + label + " — |cffffdd44" + I2S(candQuotes[s]) + " 黄金|r"
                    set extStr = "目标身份：" + label + " (" + GetPlayerName(GetOwningPlayer(u)) + ")|n" + "目标属性：生命 " + I2S(R2I(GetUnitState(u, UNIT_STATE_MAX_LIFE))) + " | 攻击 " + I2S(BlzGetUnitBaseDamage(u, 0)) + " | 护甲 " + I2S(R2I(BlzGetUnitArmor(u))) + "|n" + "特派杀手：" + Asn_GetKillerSquadName(kType) + "|n" + "克制手段：" + Asn_GetCounterDesc(u) + "|n|n|cffffcc00雇佣报价：" + I2S(candQuotes[s]) + " 黄金|r（一次性买断！绝不受雇主控制，顺路摧毁一切阻拦者，若阵亡则无限增援更强波次直到目标彻底死亡！）"
                endif
            endif'''
    text = replace_once(text, old_refresh, new_refresh, '2_Asn_RefreshBoard')

    # 3. Asn_HasActiveContractOnPlayer + Asn_ApplyAllianceForBuyerAndVictim
    old_alliance = r'''function Asn_ApplyAllianceForBuyerAndVictim takes player buyer, player victim returns nothing
    local integer i = 0
    // 确保杀手(Player 26)绝对不能被任何玩家操控，对雇主及其盟友保持友好视野，仅对目标方与阻碍者开战
    call SetPlayerAlliance(Player(26), buyer, ALLIANCE_PASSIVE, true)
    call SetPlayerAlliance(Player(26), buyer, ALLIANCE_SHARED_VISION, true)
    call SetPlayerAlliance(Player(26), buyer, ALLIANCE_SHARED_CONTROL, false)
    call SetPlayerAlliance(buyer, Player(26), ALLIANCE_PASSIVE, true)

    set i = 0
    loop
        exitwhen i > 7
        if IsPlayerAlly(Player(i), buyer) then
            call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(i), Player(26), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_SHARED_CONTROL, false)
        endif
        set i = i + 1
    endloop

    if victim != null then
        call SetPlayerAlliance(Player(26), victim, ALLIANCE_PASSIVE, false)
        call SetPlayerAlliance(victim, Player(26), ALLIANCE_PASSIVE, false)
        set i = 0
        loop
            exitwhen i > 7
            if IsPlayerAlly(Player(i), victim) and not IsPlayerAlly(Player(i), buyer) then
                call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_PASSIVE, false)
                call SetPlayerAlliance(Player(i), Player(26), ALLIANCE_PASSIVE, false)
            endif
            set i = i + 1
        endloop
    endif
endfunction'''

    new_alliance = r'''function Asn_HasActiveContractOnPlayer takes player p returns boolean
    local integer c = 0
    if p == null then
        return false
    endif
    loop
        exitwhen c >= 8
        if udg_Asn_ConActive[c] and udg_Asn_ConVictimOwner[c] == p then
            return true
        endif
        set c = c + 1
    endloop
    return false
endfunction

function Asn_ApplyAllianceForBuyerAndVictim takes player buyer, player victim returns nothing
    local integer i = 0
    // 确保杀手(Player 26)绝对不能被任何玩家操控；若雇主自身正处于自测被通缉状态，绝不误切回和平
    call SetPlayerAlliance(Player(26), buyer, ALLIANCE_SHARED_VISION, true)
    call SetPlayerAlliance(Player(26), buyer, ALLIANCE_SHARED_CONTROL, false)
    if victim != buyer and not Asn_HasActiveContractOnPlayer(buyer) then
        call SetPlayerAlliance(Player(26), buyer, ALLIANCE_PASSIVE, true)
        call SetPlayerAlliance(buyer, Player(26), ALLIANCE_PASSIVE, true)
    endif

    set i = 0
    loop
        exitwhen i > 7
        if IsPlayerAlly(Player(i), buyer) then
            call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_SHARED_CONTROL, false)
            if Player(i) != victim and not Asn_HasActiveContractOnPlayer(Player(i)) then
                call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_PASSIVE, true)
                call SetPlayerAlliance(Player(i), Player(26), ALLIANCE_PASSIVE, true)
            endif
        endif
        set i = i + 1
    endloop

    if victim != null then
        call SetPlayerAlliance(Player(26), victim, ALLIANCE_PASSIVE, false)
        call SetPlayerAlliance(victim, Player(26), ALLIANCE_PASSIVE, false)
        set i = 0
        loop
            exitwhen i > 7
            if IsPlayerAlly(Player(i), victim) and not IsPlayerAlly(Player(i), buyer) then
                call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_PASSIVE, false)
                call SetPlayerAlliance(Player(i), Player(26), ALLIANCE_PASSIVE, false)
            endif
            set i = i + 1
        endloop
    endif
endfunction'''
    text = replace_once(text, old_alliance, new_alliance, '3_Asn_ApplyAllianceForBuyerAndVictim')

    # 4. Asn_OnDamagedHook blocker targeting fix
    old_blocker = r'''    // 1. 若杀手小队遭到任何单位袭击，立即将其锁定为阻碍目标并全面转敌对，顺路毁灭！
    if Asn_IsAssassin(tgt) then
        set c = Asn_FindKillerContract(tgt)
        if c >= 0 and src != udg_Asn_ConTarget[c] then
            if udg_Asn_ConBuyer[c] == null or not IsUnitAlly(src, udg_Asn_ConBuyer[c]) then
                set udg_Asn_ConBlocker[c] = src'''

    new_blocker = r'''    // 1. 若杀手小队遭到任何单位袭击，立即将其锁定为阻碍目标并全面转敌对，顺路毁灭！（自测模式下玩家自身部队/防御塔攻击杀手同样视为阻碍者）
    if Asn_IsAssassin(tgt) then
        set c = Asn_FindKillerContract(tgt)
        if c >= 0 and src != udg_Asn_ConTarget[c] then
            if udg_Asn_ConBuyer[c] == null or udg_Asn_ConVictimOwner[c] == udg_Asn_ConBuyer[c] or not IsUnitAlly(src, udg_Asn_ConBuyer[c]) then
                set udg_Asn_ConBlocker[c] = src'''
    text = replace_once(text, old_blocker, new_blocker, '4_Asn_OnDamagedHook_blocker')

    # 5. Asn_StartContract + Asn_OnCastAbility
    old_cast = r'''function Asn_OnCastAbility takes unit shop, integer abilId returns boolean
    local integer i = 0
    local integer slotIdx = -1
    local player buyer = Asn_GetDefaultHumanBuyer()
    local unit tgt = null
    local integer quote = 0
    local integer gold = 0
    local integer freeC = -1
    local integer existingC = -1
    local integer aliveK = 0

    if abilId == 'A05A' then
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
    endif

    loop
        exitwhen i >= 10 or slotIdx >= 0
        if udg_Asn_SlotAbil[i] == abilId then
            set slotIdx = i
        endif
        set i = i + 1
    endloop
    if slotIdx < 0 then
        set buyer = null
        return false
    endif

    set tgt = udg_Asn_BoardUnit[slotIdx]
    if tgt == null or not Asn_IsUnitAliveOrEgg(tgt) then
        call DisplayTimedTextToPlayer(buyer, 0, 0, 4.0, "|cffff6600[暗杀介绍所]|r 该悬赏目标已倒下或暂不可用，正在重新扫描榜单...")
        call Asn_RefreshBoard()
        set buyer = null
        set tgt = null
        return true
    endif

    set existingC = Asn_FindContractByTarget(tgt)
    if existingC >= 0 then
        set aliveK = 0
        set i = 0
        loop
            exitwhen i >= udg_Asn_KillerCount
            if udg_Asn_KillerCon[i] == existingC and udg_Asn_KillerUnit[i] != null and not IsUnitType(udg_Asn_KillerUnit[i], UNIT_TYPE_DEAD) then
                set aliveK = aliveK + 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(buyer, 0, 0, 5.0, "|cffffcc00[契约执行中]|r 公会已在全力追杀 |cffff3366" + Asn_GetUnitDisplayLabel(tgt) + "|r（第 " + I2S(udg_Asn_ConWave[existingC]) + " 波，存活杀手 " + I2S(aliveK) + " 名），无需重复付费！")
        set buyer = null
        set tgt = null
        return true
    endif

    // 以最新报价核价
    set quote = Asn_CalcQuote(tgt)
    set gold = GetPlayerState(buyer, PLAYER_STATE_RESOURCE_GOLD)
    if gold < quote then
        call DisplayTimedTextToPlayer(buyer, 0, 0, 5.0, "|cffff3333[资金不足]|r 聘请 " + Asn_GetKillerSquadName(Asn_GetCounterTypeForTarget(tgt)) + " 需要 |cffffdd44" + I2S(quote) + "|r 黄金，你还缺少 " + I2S(quote - gold) + " 黄金！")
        set buyer = null
        set tgt = null
        return true
    endif

    set freeC = -1
    set i = 0
    loop
        exitwhen i >= 8 or freeC >= 0
        if not udg_Asn_ConActive[i] then
            set freeC = i
        endif
        set i = i + 1
    endloop
    if freeC < 0 then
        call DisplayTimedTextToPlayer(buyer, 0, 0, 5.0, "|cffff3333[暗杀介绍所]|r 当前并发追杀契约已达上限（8单），请等待已有暗杀完成后再下单！")
        set buyer = null
        set tgt = null
        return true
    endif

    // 扣费并立约
    call SetPlayerState(buyer, PLAYER_STATE_RESOURCE_GOLD, gold - quote)
    set udg_Asn_ConActive[freeC] = true
    set udg_Asn_ConTarget[freeC] = tgt
    set udg_Asn_ConBuyer[freeC] = buyer
    set udg_Asn_ConVictimOwner[freeC] = GetOwningPlayer(tgt)
    set udg_Asn_ConKillerType[freeC] = Asn_GetCounterTypeForTarget(tgt)
    set udg_Asn_ConWave[freeC] = 1
    set udg_Asn_ConRespawnCD[freeC] = 0.0
    set udg_Asn_ConDeadTimer[freeC] = 0.0
    set udg_Asn_ConBlocker[freeC] = null
    set udg_Asn_ConSpawnX[freeC] = GetUnitX(shop)
    set udg_Asn_ConSpawnY[freeC] = GetUnitY(shop) - 220.0

    call DisplayTimedTextToPlayer(buyer, 0, 0, 6.0, "|cff00ff80[契约成立]|r 已支付 |cffffdd44" + I2S(quote) + "|r 黄金！幽影公会绝不受任何人操纵，杀手小队不死不休！")
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING then
            call DisplayTimedTextToPlayer(Player(i), 0, 0, 8.0, "|cffff2244【全图通缉 · 暗杀契约生效！】|r " + Asn_GetPlayerFactionName(GetOwningPlayer(tgt)) + " 的 |cffffcc00【" + Asn_GetUnitDisplayLabel(tgt) + "】|r 已经被下单买命（悬赏 |cffffdd44" + I2S(quote) + " 黄金|r）！幽影公会已派出 " + Asn_GetKillerSquadName(udg_Asn_ConKillerType[freeC]) + "，不死不休！")
        endif
        set i = i + 1
    endloop
    call PingMinimapEx(GetUnitX(tgt), GetUnitY(tgt), 5.0, 255, 40, 40, true)
    call Asn_SpawnWave(freeC)
    call Asn_RefreshBoard()

    set buyer = null
    set tgt = null
    return true
endfunction'''

    new_cast = r'''function Asn_StartContract takes player buyer, unit shop, unit tgt returns boolean
    local integer i = 0
    local integer quote = 0
    local integer gold = 0
    local integer freeC = -1
    local integer existingC = -1
    local integer aliveK = 0
    local boolean isSelf = false

    if buyer == null or shop == null or tgt == null or not Asn_IsUnitAliveOrEgg(tgt) then
        if buyer != null then
            call DisplayTimedTextToPlayer(buyer, 0, 0, 4.0, "|cffff6600[暗杀介绍所]|r 该悬赏目标已倒下或暂不可用，正在重新扫描榜单...")
        endif
        call Asn_RefreshBoard()
        return true
    endif

    set isSelf = (GetOwningPlayer(tgt) == buyer)
    if isSelf and not udg_Asn_AllowSelfTest then
        call DisplayTimedTextToPlayer(buyer, 0, 0, 4.0, "|cffff6600[暗杀介绍所]|r 当前正式模式已关闭对自己下单功能。")
        return true
    endif

    set existingC = Asn_FindContractByTarget(tgt)
    if existingC >= 0 then
        set aliveK = 0
        set i = 0
        loop
            exitwhen i >= udg_Asn_KillerCount
            if udg_Asn_KillerCon[i] == existingC and udg_Asn_KillerUnit[i] != null and not IsUnitType(udg_Asn_KillerUnit[i], UNIT_TYPE_DEAD) then
                set aliveK = aliveK + 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(buyer, 0, 0, 5.0, "|cffffcc00[契约执行中]|r 公会已在全力追杀 |cffff3366" + Asn_GetUnitDisplayLabel(tgt) + "|r（第 " + I2S(udg_Asn_ConWave[existingC]) + " 波，存活杀手 " + I2S(aliveK) + " 名），无需重复下单！")
        return true
    endif

    // 以最新报价核价（测试模式对自己下单完全免费，仍展示实时评估身价）
    set quote = Asn_CalcQuote(tgt)
    if not isSelf then
        set gold = GetPlayerState(buyer, PLAYER_STATE_RESOURCE_GOLD)
        if gold < quote then
            call DisplayTimedTextToPlayer(buyer, 0, 0, 5.0, "|cffff3333[资金不足]|r 聘请 " + Asn_GetKillerSquadName(Asn_GetCounterTypeForTarget(tgt)) + " 需要 |cffffdd44" + I2S(quote) + "|r 黄金，你还缺少 " + I2S(quote - gold) + " 黄金！")
            return true
        endif
    endif

    set freeC = -1
    set i = 0
    loop
        exitwhen i >= 8 or freeC >= 0
        if not udg_Asn_ConActive[i] then
            set freeC = i
        endif
        set i = i + 1
    endloop
    if freeC < 0 then
        call DisplayTimedTextToPlayer(buyer, 0, 0, 5.0, "|cffff3333[暗杀介绍所]|r 当前并发追杀契约已达上限（8单），请等待已有暗杀完成后再下单！")
        return true
    endif

    // 扣费（自测免费）并立约
    if not isSelf then
        call SetPlayerState(buyer, PLAYER_STATE_RESOURCE_GOLD, gold - quote)
    endif
    set udg_Asn_ConActive[freeC] = true
    set udg_Asn_ConTarget[freeC] = tgt
    set udg_Asn_ConBuyer[freeC] = buyer
    set udg_Asn_ConVictimOwner[freeC] = GetOwningPlayer(tgt)
    set udg_Asn_ConKillerType[freeC] = Asn_GetCounterTypeForTarget(tgt)
    set udg_Asn_ConWave[freeC] = 1
    set udg_Asn_ConRespawnCD[freeC] = 0.0
    set udg_Asn_ConDeadTimer[freeC] = 0.0
    set udg_Asn_ConBlocker[freeC] = null
    set udg_Asn_ConSpawnX[freeC] = GetUnitX(shop)
    set udg_Asn_ConSpawnY[freeC] = GetUnitY(shop) - 220.0

    if isSelf then
        call DisplayTimedTextToPlayer(buyer, 0, 0, 7.0, "|cff00ffcc[自测挑战成立]|r 测试模式对自己下单免费（实时身价评估 |cffffdd44" + I2S(quote) + "|r 黄金）！幽影公会绝不受你控制，请全力抵挡逐波反进化强袭！（输入 |-stopkill|r 可中途结束）")
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING then
                call DisplayTimedTextToPlayer(Player(i), 0, 0, 8.0, "|cff00ffcc【测试模式 · 自我暗杀极限挑战！】|r " + Asn_GetPlayerFactionName(GetOwningPlayer(tgt)) + " 对自己的 |cffffcc00【" + Asn_GetUnitDisplayLabel(tgt) + "】|r 下达了不死不休暗杀令（评估身价 |cffffdd44" + I2S(quote) + " 黄金|r）！幽影公会已派出 " + Asn_GetKillerSquadName(udg_Asn_ConKillerType[freeC]) + "，看看能挡多少波！")
            endif
            set i = i + 1
        endloop
    else
        call DisplayTimedTextToPlayer(buyer, 0, 0, 6.0, "|cff00ff80[契约成立]|r 已支付 |cffffdd44" + I2S(quote) + "|r 黄金！幽影公会绝不受任何人操纵，杀手小队不死不休！")
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING then
                call DisplayTimedTextToPlayer(Player(i), 0, 0, 8.0, "|cffff2244【全图通缉 · 暗杀契约生效！】|r " + Asn_GetPlayerFactionName(GetOwningPlayer(tgt)) + " 的 |cffffcc00【" + Asn_GetUnitDisplayLabel(tgt) + "】|r 已经被下单买命（悬赏 |cffffdd44" + I2S(quote) + " 黄金|r）！幽影公会已派出 " + Asn_GetKillerSquadName(udg_Asn_ConKillerType[freeC]) + "，不死不休！")
            endif
            set i = i + 1
        endloop
    endif

    call PingMinimapEx(GetUnitX(tgt), GetUnitY(tgt), 5.0, 255, 40, 40, true)
    call Asn_SpawnWave(freeC)
    call Asn_RefreshBoard()
    return true
endfunction

function Asn_OnCastAbility takes unit shop, integer abilId returns boolean
    local integer i = 0
    local integer slotIdx = -1
    local player buyer = Asn_GetDefaultHumanBuyer()
    local integer aliveK = 0

    if abilId == 'A05A' then
        call Asn_RefreshBoard()
        call DisplayTimedTextToPlayer(buyer, 0, 0, 10.0, "|cffffcc00【暗杀介绍所 · 实时悬赏榜单】|r 头像与报价已刷新：")
        set i = 0
        set aliveK = 0
        loop
            exitwhen i >= 10
            if udg_Asn_BoardUnit[i] != null then
                set aliveK = aliveK + 1
                if udg_Asn_AllowSelfTest and GetOwningPlayer(udg_Asn_BoardUnit[i]) == buyer then
                    call DisplayTimedTextToPlayer(buyer, 0, 0, 10.0, "  [" + I2S(i + 1) + "] |cff00ffcc[自测挑战]|r " + Asn_GetPlayerFactionName(GetOwningPlayer(udg_Asn_BoardUnit[i])) + " · |cffffffff" + Asn_GetUnitDisplayLabel(udg_Asn_BoardUnit[i]) + "|r — |cff00ff80自测免费（评估身价 " + I2S(udg_Asn_BoardPrice[i]) + " 黄金）|r")
                else
                    call DisplayTimedTextToPlayer(buyer, 0, 0, 10.0, "  [" + I2S(i + 1) + "] " + Asn_GetPlayerFactionName(GetOwningPlayer(udg_Asn_BoardUnit[i])) + " · |cffffffff" + Asn_GetUnitDisplayLabel(udg_Asn_BoardUnit[i]) + "|r — 报价 |cffffdd44" + I2S(udg_Asn_BoardPrice[i]) + " 黄金|r")
                endif
            endif
            set i = i + 1
        endloop
        if aliveK == 0 then
            call DisplayTimedTextToPlayer(buyer, 0, 0, 8.0, "  |cffaaaaaa（当前全图尚未发现存活英雄或Boss，请稍待电脑出英雄或输入 -archimonde 测试）|r")
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
    endif

    loop
        exitwhen i >= 10 or slotIdx >= 0
        if udg_Asn_SlotAbil[i] == abilId then
            set slotIdx = i
        endif
        set i = i + 1
    endloop
    if slotIdx < 0 then
        set buyer = null
        return false
    endif

    call Asn_StartContract(buyer, shop, udg_Asn_BoardUnit[slotIdx])
    set buyer = null
    return true
endfunction'''
    text = replace_once(text, old_cast, new_cast, '5_Asn_StartContract_and_OnCastAbility')

    # 6. Asn_Loop self-contract settlement, wave clear banner, and peaceful alliance restoration
    old_loop_head = r'''    local real bx = 0.0
    local real by = 0.0

    // 1. 推进全部活跃暗杀契约与波次监控
    set c = 0
    loop
        exitwhen c >= 8
        if udg_Asn_ConActive[c] then
            set tgt = udg_Asn_ConTarget[c]
            if tgt == null or not Asn_IsUnitAliveOrEgg(tgt) then
                // 连续 3 秒确认目标未复生/彻底死透后再收回杀手并结单
                set udg_Asn_ConDeadTimer[c] = udg_Asn_ConDeadTimer[c] + 1.0
                    if (GetUnitAbilityLevel(tgt, 'AOre') > 0 or UnitHasItemOfTypeBJ(tgt, 'rnsp')) and udg_Asn_ConDeadTimer[c] < 6.0 then
                        // 原生重生复生读取中，蹲守等待复生后补刀
                    elseif udg_Asn_ConDeadTimer[c] >= 2.0 then
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cff00ff80【暗杀任务圆满完成！】|r 契约目标 |cffffcc00" + Asn_GetUnitDisplayLabel(tgt) + "|r 已被彻底诛杀，幽影杀手全员化影归隐！")
                        call Asn_ClearContractUnits(c)
                        set udg_Asn_ConActive[c] = false
                        set udg_Asn_ConTarget[c] = null
                        set udg_Asn_ConBlocker[c] = null
                        call Asn_RefreshBoard()
                    endif
            else
                // 若目标曾短暂倒地又爬起（如重生十字章/AOre），归零确认计时，立刻继续扑杀！
                set udg_Asn_ConDeadTimer[c] = 0.0

                // 验证当前波次存活杀手数量
                set aliveK = 0
                set i = 0
                loop
                    exitwhen i >= udg_Asn_KillerCount
                    if udg_Asn_KillerCon[i] == c then
                        set k = udg_Asn_KillerUnit[i]
                        if k != null and not IsUnitType(k, UNIT_TYPE_DEAD) and GetWidgetLife(k) > 0.405 then
                            set aliveK = aliveK + 1
                        else
                            set udg_Asn_KillerCount = udg_Asn_KillerCount - 1
                            set udg_Asn_KillerUnit[i] = udg_Asn_KillerUnit[udg_Asn_KillerCount]
                            set udg_Asn_KillerCon[i] = udg_Asn_KillerCon[udg_Asn_KillerCount]
                            set udg_Asn_KillerLastX[i] = udg_Asn_KillerLastX[udg_Asn_KillerCount]
                            set udg_Asn_KillerLastY[i] = udg_Asn_KillerLastY[udg_Asn_KillerCount]
                            set udg_Asn_KillerStuck[i] = udg_Asn_KillerStuck[udg_Asn_KillerCount]
                            set udg_Asn_KillerUnit[udg_Asn_KillerCount] = null
                            set i = i - 1
                        endif
                    endif
                    set i = i + 1
                endloop

                if aliveK == 0 then
                    if udg_Asn_ConRespawnCD[c] <= 0.0 then
                        set udg_Asn_ConRespawnCD[c] = 3.0
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffff6600【暗杀升级警报！】|r 第 " + I2S(udg_Asn_ConWave[c]) + " 波杀手已被拦下！幽影公会正在重扫目标最新进化状态，集结第 " + I2S(udg_Asn_ConWave[c] + 1) + " 波狂暴反制小队（3秒后抵达）...")
                    else'''

    new_loop_head = r'''    local real bx = 0.0
    local real by = 0.0
    local boolean wasSelf = false
    local player victimP = null
    local integer endWave = 1
    local string tgtLabel = ""

    // 1. 推进全部活跃暗杀契约与波次监控
    set c = 0
    loop
        exitwhen c >= 8
        if udg_Asn_ConActive[c] then
            set tgt = udg_Asn_ConTarget[c]
            if tgt == null or not Asn_IsUnitAliveOrEgg(tgt) then
                // 连续确认目标未复生/彻底死透后再收回杀手并结单
                set udg_Asn_ConDeadTimer[c] = udg_Asn_ConDeadTimer[c] + 1.0
                    if (GetUnitAbilityLevel(tgt, 'AOre') > 0 or UnitHasItemOfTypeBJ(tgt, 'rnsp')) and udg_Asn_ConDeadTimer[c] < 6.0 then
                        // 原生重生复生读取中，蹲守等待复生后补刀
                    elseif udg_Asn_ConDeadTimer[c] >= 2.0 then
                        set wasSelf = (udg_Asn_ConBuyer[c] == udg_Asn_ConVictimOwner[c])
                        set victimP = udg_Asn_ConVictimOwner[c]
                        set endWave = udg_Asn_ConWave[c]
                        set tgtLabel = Asn_GetUnitDisplayLabel(tgt)
                        if wasSelf then
                            call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 10.0, "|cffffcc00【自我暗杀极限挑战结算！】|r " + Asn_GetPlayerFactionName(victimP) + " 的 |cffffffff【" + tgtLabel + "】|r 共成功抵挡了 |cff00ff80" + I2S(endWave - 1) + "|r 波幽影杀手，最终倒在第 |cffff3366" + I2S(endWave) + "|r 波反进化强袭之下！（随时可再点暗杀介绍所或输入 |-killme|r 再次挑战）")
                        else
                            call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cff00ff80【暗杀任务圆满完成！】|r 契约目标 |cffffcc00" + tgtLabel + "|r 已被彻底诛杀，幽影杀手全员化影归隐！")
                        endif
                        call Asn_ClearContractUnits(c)
                        set udg_Asn_ConActive[c] = false
                        set udg_Asn_ConTarget[c] = null
                        set udg_Asn_ConBlocker[c] = null
                        set udg_Asn_ConBuyer[c] = null
                        set udg_Asn_ConVictimOwner[c] = null
                        if wasSelf and victimP != null and not Asn_HasActiveContractOnPlayer(victimP) then
                            call SetPlayerAlliance(Player(26), victimP, ALLIANCE_PASSIVE, true)
                            call SetPlayerAlliance(victimP, Player(26), ALLIANCE_PASSIVE, true)
                            call SetPlayerAlliance(Player(26), victimP, ALLIANCE_SHARED_VISION, true)
                            call SetPlayerAlliance(Player(26), victimP, ALLIANCE_SHARED_CONTROL, false)
                        endif
                        call Asn_RefreshBoard()
                    endif
            else
                // 若目标曾短暂倒地又爬起（如重生十字章/AOre），归零确认计时，立刻继续扑杀！
                set udg_Asn_ConDeadTimer[c] = 0.0

                // 验证当前波次存活杀手数量
                set aliveK = 0
                set i = 0
                loop
                    exitwhen i >= udg_Asn_KillerCount
                    if udg_Asn_KillerCon[i] == c then
                        set k = udg_Asn_KillerUnit[i]
                        if k != null and not IsUnitType(k, UNIT_TYPE_DEAD) and GetWidgetLife(k) > 0.405 then
                            set aliveK = aliveK + 1
                        else
                            set udg_Asn_KillerCount = udg_Asn_KillerCount - 1
                            set udg_Asn_KillerUnit[i] = udg_Asn_KillerUnit[udg_Asn_KillerCount]
                            set udg_Asn_KillerCon[i] = udg_Asn_KillerCon[udg_Asn_KillerCount]
                            set udg_Asn_KillerLastX[i] = udg_Asn_KillerLastX[udg_Asn_KillerCount]
                            set udg_Asn_KillerLastY[i] = udg_Asn_KillerLastY[udg_Asn_KillerCount]
                            set udg_Asn_KillerStuck[i] = udg_Asn_KillerStuck[udg_Asn_KillerCount]
                            set udg_Asn_KillerUnit[udg_Asn_KillerCount] = null
                            set i = i - 1
                        endif
                    endif
                    set i = i + 1
                endloop

                if aliveK == 0 then
                    if udg_Asn_ConRespawnCD[c] <= 0.0 then
                        set udg_Asn_ConRespawnCD[c] = 3.0
                        if udg_Asn_ConBuyer[c] == udg_Asn_ConVictimOwner[c] then
                            call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 5.0, "|cff00ffcc【自测波次突破！】|r 漂亮！你已成功全歼第 |cffffdd44" + I2S(udg_Asn_ConWave[c]) + "|r 波幽影杀手！公会正在重扫你的最新属性，3秒后派出第 |cffff3366" + I2S(udg_Asn_ConWave[c] + 1) + "|r 波狂暴反进化强袭小队...")
                        else
                            call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffff6600【暗杀升级警报！】|r 第 " + I2S(udg_Asn_ConWave[c]) + " 波杀手已被拦下！幽影公会正在重扫目标最新进化状态，集结第 " + I2S(udg_Asn_ConWave[c] + 1) + " 波狂暴反制小队（3秒后抵达）...")
                        endif
                    else'''
    text = replace_once(text, old_loop_head, new_loop_head, '6a_Asn_Loop_body')

    old_loop_end = r'''    set blocker = null
    set orderTgt = null
endfunction

function Asn_SpawnAgencyAt'''

    new_loop_end = r'''    set blocker = null
    set orderTgt = null
    set victimP = null
endfunction

function Asn_SpawnAgencyAt'''
    text = replace_once(text, old_loop_end, new_loop_end, '6b_Asn_Loop_end')

    # 7. Asn_InitSystem welcome banner
    old_banner = r'''    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 10.0, "|cffff3366【暗杀介绍所已开业】|r 东西中立酒馆旁已开放【暗杀介绍所】：可凭敌方头像按实时战力报价雇佣针对性必杀杀手！输入 |-kill|r 一键直达！")'''
    new_banner = r'''    if udg_Asn_AllowSelfTest then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 12.0, "|cffff3366【暗杀介绍所已开业】|r 东西酒馆旁已开放：可下单暗杀敌方英雄，|cff00ffcc[测试模式限定]|r 也可点击自身头像或输入 |-killme|r 对自己免费下单测耐力波数（|-stopkill|r 停止，|-kill|r 直达）！")
    else
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 10.0, "|cffff3366【暗杀介绍所已开业】|r 东西中立酒馆旁已开放【暗杀介绍所】：可凭敌方头像按实时战力报价雇佣针对性必杀杀手！输入 |-kill|r 一键直达！")
    endif'''
    text = replace_once(text, old_banner, new_banner, '7_Asn_InitSystem_banner')

    # 8. TM_OnChatCommand locals & -killme / -selfkill / -stopkill
    old_chat_locals = r'''function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    local integer pId = 0
    local unit u = null
    local group g = null
    local real startX = 0.0
    local real startY = 0.0'''

    new_chat_locals = r'''function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    local integer pId = 0
    local unit u = null
    local group g = null
    local real startX = 0.0
    local real startY = 0.0
    local unit selfHero = null
    local unit nearShop = null
    local integer stopped = 0
    local integer bestScore = 0
    local integer curScore = 0
    local integer utSelf = 0'''
    text = replace_once(text, old_chat_locals, new_chat_locals, '8a_TM_OnChatCommand_locals')

    old_chat_kill = r'''            call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cffff3366【暗杀介绍所】|r 已为你定位并选中最近的暗杀介绍所，可点击右下命令栏内敌方目标头像下单暗杀！")
            set u = null
        endif
    elseif s == "-archimonde" then'''

    new_chat_kill = r'''            call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cffff3366【暗杀介绍所】|r 已为你定位并选中最近的暗杀介绍所，可点击右下命令栏内目标头像下单暗杀（测试模式含自身挑战）！")
            set u = null
        endif
    elseif s == "-killme" or s == "-selfkill" then
        if not udg_Asn_AllowSelfTest then
            call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cffff6600[暗杀介绍所]|r 当前正式模式已关闭自我暗杀测试功能！")
        else
            set selfHero = null
            set bestScore = -1
            set g = CreateGroup()
            call GroupEnumUnitsOfPlayer(g, p, null)
            loop
                set u = FirstOfGroup(g)
                exitwhen u == null
                call GroupRemoveUnit(g, u)
                set utSelf = GetUnitTypeId(u)
                if not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) and not Asn_IsAssassinType(utSelf) then
                    if IsUnitType(u, UNIT_TYPE_HERO) or utSelf == 'u004' then
                        set u = Asn_GetTargetTrueUnit(u)
                        if u != null then
                            set utSelf = GetUnitTypeId(u)
                            set curScore = IMaxBJ(1, GetUnitLevel(u))
                            if utSelf == 'H002' or utSelf == 'H003' or utSelf == 'H004' or utSelf == 'H005' or utSelf == 'H006' then
                                set curScore = curScore + 1000
                            endif
                            if curScore > bestScore then
                                set bestScore = curScore
                                set selfHero = u
                            endif
                        endif
                    endif
                endif
            endloop
            call DestroyGroup(g)
            set g = null

            set nearShop = udg_Asn_Shop[0]
            if selfHero != null and udg_Asn_Shop[1] != null then
                if nearShop == null then
                    set nearShop = udg_Asn_Shop[1]
                elseif (GetUnitX(udg_Asn_Shop[1]) - GetUnitX(selfHero)) * (GetUnitX(udg_Asn_Shop[1]) - GetUnitX(selfHero)) + (GetUnitY(udg_Asn_Shop[1]) - GetUnitY(selfHero)) * (GetUnitY(udg_Asn_Shop[1]) - GetUnitY(selfHero)) < (GetUnitX(nearShop) - GetUnitX(selfHero)) * (GetUnitX(nearShop) - GetUnitX(selfHero)) + (GetUnitY(nearShop) - GetUnitY(selfHero)) * (GetUnitY(nearShop) - GetUnitY(selfHero)) then
                    set nearShop = udg_Asn_Shop[1]
                endif
            endif

            if selfHero == null then
                call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cffff6600[自测挑战]|r 未检测到你当前存活的英雄！请先在祭坛/酒馆召唤或复活一名英雄后再输入 |-killme|r！")
            elseif nearShop == null then
                call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cffff6600[自测挑战]|r 暗杀介绍所尚未初始化完毕，请 1 秒后再试！")
            else
                set udg_Asn_LastBuyer = p
                call Asn_StartContract(p, nearShop, selfHero)
            endif
        endif
    elseif s == "-stopkill" then
        set stopped = 0
        set bestScore = 0
        set i = 0
        loop
            exitwhen i >= 8
            if udg_Asn_ConActive[i] and udg_Asn_ConBuyer[i] == p and udg_Asn_ConVictimOwner[i] == p then
                if udg_Asn_ConWave[i] - 1 > bestScore then
                    set bestScore = udg_Asn_ConWave[i] - 1
                endif
                call Asn_ClearContractUnits(i)
                set udg_Asn_ConActive[i] = false
                set udg_Asn_ConTarget[i] = null
                set udg_Asn_ConBlocker[i] = null
                set udg_Asn_ConBuyer[i] = null
                set udg_Asn_ConVictimOwner[i] = null
                set stopped = stopped + 1
            endif
            set i = i + 1
        endloop
        if stopped > 0 then
            if p != null and not Asn_HasActiveContractOnPlayer(p) then
                call SetPlayerAlliance(Player(26), p, ALLIANCE_PASSIVE, true)
                call SetPlayerAlliance(p, Player(26), ALLIANCE_PASSIVE, true)
                call SetPlayerAlliance(Player(26), p, ALLIANCE_SHARED_VISION, true)
                call SetPlayerAlliance(Player(26), p, ALLIANCE_SHARED_CONTROL, false)
            endif
            call Asn_RefreshBoard()
            call DisplayTimedTextToPlayer(p, 0, 0, 7.0, "|cff00ffcc【自我暗杀测试已手动终止】|r 已撤回杀手小队并恢复中立和平（本次已撑过 |cff00ff80" + I2S(bestScore) + "|r 波）。")
        else
            call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cffaaaaaa[自测提示]|r 当前没有针对你自己的活跃暗杀测试。")
        endif
    elseif s == "-archimonde" then'''
    text = replace_once(text, old_chat_kill, new_chat_kill, '8b_TM_OnChatCommand_handlers')

    old_chat_end = r'''    set u = null
    set p = null
endfunction

function TM_GetFirstHumanPlayer'''

    new_chat_end = r'''    set u = null
    set selfHero = null
    set nearShop = null
    set p = null
endfunction

function TM_GetFirstHumanPlayer'''
    text = replace_once(text, old_chat_end, new_chat_end, '8c_TM_OnChatCommand_end')

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open(TARGET_PATH, 'wb') as f:
        f.write(out_bytes)
    print("Successfully applied v6.6 patches to payload/war3map.j!")


if __name__ == '__main__':
    main()
