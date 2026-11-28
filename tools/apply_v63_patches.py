# -*- coding: utf-8 -*-
"""
v6.3 JASS 补丁：暗杀介绍所（n005）完整系统 + 六大机制硬克制钩子 + 顺路毁障 AI + 无限增援直到必死
"""
import sys

JASS_PATH = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j"

GLOBALS_ADD = """    // Assassination Agency System (暗杀介绍所 · 幽影杀手公会 v6.3)
    unit array udg_Asn_Shop
    integer udg_Asn_ShopCount = 0
    player udg_Asn_LastBuyer = null
    integer array udg_Asn_SlotAbil
    unit array udg_Asn_BoardUnit
    integer array udg_Asn_BoardPrice
    integer array udg_Asn_BoardKillerType
    unit array udg_Asn_SlotLastUnit
    boolean array udg_Asn_SlotHidden
    string array udg_Asn_SlotLastIcon
    // Active contracts (max 8)
    boolean array udg_Asn_ConActive
    unit array udg_Asn_ConTarget
    player array udg_Asn_ConBuyer
    player array udg_Asn_ConVictimOwner
    integer array udg_Asn_ConKillerType
    integer array udg_Asn_ConWave
    real array udg_Asn_ConRespawnCD
    real array udg_Asn_ConDeadTimer
    real array udg_Asn_ConSpawnX
    real array udg_Asn_ConSpawnY
    unit array udg_Asn_ConBlocker
    integer array udg_Asn_ConBaseHP
    integer array udg_Asn_ConBaseDmg
    real array udg_Asn_ConBaseArmor
    // Individual killers (max 96)
    unit array udg_Asn_KillerUnit
    integer array udg_Asn_KillerCon
    real array udg_Asn_KillerLastX
    real array udg_Asn_KillerLastY
    integer array udg_Asn_KillerStuck
    integer udg_Asn_KillerCount = 0
"""

# 放在 Refuge_InitForPlayer 之后（确保 Refuge_IsSafeTerrainPoint 已声明！）与 DM_CastPossession 之前
# 注意：需要引用 Maho_GetAvgDefAdapt, Strain_Unburrow, Strain_BreakMimicry, DM_BreakInvisibility, Ninja_PickLivingClone 等，
# 检查这些函数在文件中的行号，若放在 DM_OnUnitAttacked 之前还是之后：
# DM_OnSpellEffect 在 line 10100, DM_OnDamaged 在 line 10545, DM_OnUnitDeath 在 line 11037。
# 把核心 Asn_* 函数插入到 function DM_OnSpellEffect 之前（大约 line 10099），这样全图所有英雄与避难所辅助函数都已声明在上方！
ASN_EARLY_HELPERS = r'''
function Asn_IsAssassinType takes integer ut returns boolean
    return ut == 'u005' or ut == 'u006' or ut == 'u007' or ut == 'u008' or ut == 'u009' or ut == 'u00A'
endfunction

function Asn_IsAssassin takes unit u returns boolean
    if u == null then
        return false
    endif
    return GetOwningPlayer(u) == Player(26) and Asn_IsAssassinType(GetUnitTypeId(u))
endfunction

function Asn_GetMahoAvgAdapt takes integer pId returns real
    local integer i = 0
    local real total = 0.0
    if pId < 0 or pId > 7 then
        return 0.0
    endif
    loop
        exitwhen i > 7
        set total = total + udg_Maho_DefAdapt[pId * 8 + i]
        set i = i + 1
    endloop
    return total / 8.0
endfunction
'''

ASN_SYSTEM_CODE = r'''
//***************************************************************************
//*
//*  Assassination Agency System (暗杀介绍所 · 幽影杀手公会 v6.3)
//*
//***************************************************************************

function Asn_FindKillerContract takes unit k returns integer
    local integer i = 0
    if k == null then
        return -1
    endif
    loop
        exitwhen i >= udg_Asn_KillerCount
        if udg_Asn_KillerUnit[i] == k then
            return udg_Asn_KillerCon[i]
        endif
        set i = i + 1
    endloop
    return -1
endfunction

function Asn_FindContractByTarget takes unit tgt returns integer
    local integer c = 0
    if tgt == null then
        return -1
    endif
    loop
        exitwhen c >= 8
        if udg_Asn_ConActive[c] and udg_Asn_ConTarget[c] == tgt then
            return c
        endif
        set c = c + 1
    endloop
    return -1
endfunction

function Asn_GetTargetTrueUnit takes unit cand returns unit
    local integer i = 0
    if cand == null then
        return null
    endif
    if GetUnitTypeId(cand) == 'u004' then
        set i = 0
        loop
            exitwhen i > 7
            if udg_Maho_InEgg[i] and udg_Maho_EggUnit[i] == cand and udg_Maho_Hero[i] != null then
                return udg_Maho_Hero[i]
            endif
            set i = i + 1
        endloop
    endif
    return cand
endfunction

function Asn_IsUnitAliveOrEgg takes unit t returns boolean
    local integer pId = 0
    if t == null then
        return false
    endif
    if not IsUnitType(t, UNIT_TYPE_DEAD) and GetWidgetLife(t) > 0.405 then
        return true
    endif
    if GetUnitTypeId(t) == 'H006' then
        set pId = GetPlayerId(GetOwningPlayer(t))
        if pId >= 0 and pId <= 7 and udg_Maho_InEgg[pId] and udg_Maho_EggUnit[pId] != null and not IsUnitType(udg_Maho_EggUnit[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_Maho_EggUnit[pId]) > 0.405 then
            return true
        endif
    endif
    return false
endfunction

function Asn_GetCombatUnitForTarget takes unit t returns unit
    local integer pId = 0
    if t == null then
        return null
    endif
    if GetUnitTypeId(t) == 'H006' then
        set pId = GetPlayerId(GetOwningPlayer(t))
        if pId >= 0 and pId <= 7 and udg_Maho_InEgg[pId] and udg_Maho_EggUnit[pId] != null and not IsUnitType(udg_Maho_EggUnit[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_Maho_EggUnit[pId]) > 0.405 then
            return udg_Maho_EggUnit[pId]
        endif
    endif
    return t
endfunction

function Asn_IsAssassinForContractTarget takes unit src, unit tgt returns boolean
    local integer c = Asn_FindKillerContract(src)
    local integer pId = 0
    if c < 0 or tgt == null then
        return false
    endif
    if udg_Asn_ConTarget[c] == tgt then
        return true
    endif
    if GetUnitTypeId(tgt) == 'u004' and udg_Asn_ConTarget[c] != null and GetUnitTypeId(udg_Asn_ConTarget[c]) == 'H006' then
        set pId = GetPlayerId(GetOwningPlayer(udg_Asn_ConTarget[c]))
        if pId >= 0 and pId <= 7 and udg_Maho_EggUnit[pId] == tgt then
            return true
        endif
    endif
    return false
endfunction

function Asn_GetUnitIconPath takes unit u returns string
    local integer ut = 0
    local integer pId = 0
    if u == null then
        return "ReplaceableTextures\\CommandButtons\\BTNSelectHeroOn.blp"
    endif
    set ut = GetUnitTypeId(u)
    set pId = GetPlayerId(GetOwningPlayer(u))

    // 5大自定义英雄（含动态进化/升空头像）
    if ut == 'H002' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroBlademaster.blp"
    elseif ut == 'H003' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroWarden.blp"
    elseif ut == 'H004' then
        if pId >= 0 and pId <= 7 then
            if udg_Strain_EvoStage[pId] >= 3 then
                return "ReplaceableTextures\\CommandButtons\\BTNHeroCryptLord.blp"
            elseif udg_Strain_EvoStage[pId] == 2 then
                return "ReplaceableTextures\\CommandButtons\\BTNHydralisk.blp"
            elseif udg_Strain_EvoStage[pId] == 1 then
                return "ReplaceableTextures\\CommandButtons\\BTNArachnathidpurple.blp"
            endif
        endif
        return "ReplaceableTextures\\CommandButtons\\BTNZergling.blp"
    elseif ut == 'H005' then
        return "ReplaceableTextures\\CommandButtons\\BTNFurion.blp"
    elseif ut == 'H006' then
        if pId >= 0 and pId <= 7 and udg_Maho_IsWinged[pId] then
            return "ReplaceableTextures\\CommandButtons\\BTNDoomGuard.blp"
        endif
        return "ReplaceableTextures\\CommandButtons\\BTNLavaSpawn.blp"
    elseif ut == 'u004' then
        return "ReplaceableTextures\\CommandButtons\\BTNPhoenixEgg.blp"
    // 燃烧军团与战役Boss
    elseif ut == 'Uwar' then
        return "ReplaceableTextures\\CommandButtons\\BTNArchimonde.blp"
    elseif ut == 'Nklj' or ut == 'Nkjx' then
        return "ReplaceableTextures\\CommandButtons\\BTNKiljaedin.blp"
    elseif ut == 'Nman' then
        return "ReplaceableTextures\\CommandButtons\\BTNMannoroth.blp"
    elseif ut == 'Nmag' or ut == 'Npld' then
        return "ReplaceableTextures\\CommandButtons\\BTNPitLord.blp"
    elseif ut == 'Eevi' then
        return "ReplaceableTextures\\CommandButtons\\BTNEvilIllidan.blp"
    elseif ut == 'Hart' then
        return "ReplaceableTextures\\CommandButtons\\BTNArthas.blp"
    elseif ut == 'Hjai' then
        return "ReplaceableTextures\\CommandButtons\\BTNJaina.blp"
    elseif ut == 'Hkal' then
        return "ReplaceableTextures\\CommandButtons\\BTNBloodMage2.blp"
    elseif ut == 'Othr' then
        return "ReplaceableTextures\\CommandButtons\\BTNThrall.blp"
    elseif ut == 'Orex' then
        return "ReplaceableTextures\\CommandButtons\\BTNRexxar.blp"
    elseif ut == 'Orkn' then
        return "ReplaceableTextures\\CommandButtons\\BTNShadowHunter.blp"
    elseif ut == 'Hvsh' then
        return "ReplaceableTextures\\CommandButtons\\BTNNagaSeaWitch.blp"
    // 24原版英雄 & 酒馆英雄
    elseif ut == 'Hamg' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroArchMage.blp"
    elseif ut == 'Hpal' or ut == 'Huth' or ut == 'Hapm' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroPaladin.blp"
    elseif ut == 'Hmkg' or ut == 'Hmbr' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroMountainKing.blp"
    elseif ut == 'Hblm' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroBloodElfPrince.blp"
    elseif ut == 'Obla' or ut == 'Nbbc' or ut == 'Ogrh' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroBlademaster.blp"
    elseif ut == 'Ofar' or ut == 'Odrt' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroFarseer.blp"
    elseif ut == 'Otch' or ut == 'Ocb2' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroTaurenChieftain.blp"
    elseif ut == 'Oshd' then
        return "ReplaceableTextures\\CommandButtons\\BTNShadowHunter.blp"
    elseif ut == 'Edem' or ut == 'Eill' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroDemonHunter.blp"
    elseif ut == 'Ekee' or ut == 'Efur' or ut == 'Ecen' then
        return "ReplaceableTextures\\CommandButtons\\BTNKeeperOfTheGrove.blp"
    elseif ut == 'Emoo' then
        return "ReplaceableTextures\\CommandButtons\\BTNPriestessOfTheMoon.blp"
    elseif ut == 'Ewar' or ut == 'Ewrd' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroWarden.blp"
    elseif ut == 'Udea' or ut == 'Uear' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroDeathKnight.blp"
    elseif ut == 'Udre' or ut == 'Ubal' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroDreadLord.blp"
    elseif ut == 'Ulic' or ut == 'Uktl' then
        return "ReplaceableTextures\\CommandButtons\\BTNLichVersion2.blp"
    elseif ut == 'Ucrl' or ut == 'Uanb' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroCryptLord.blp"
    elseif ut == 'Nngs' then
        return "ReplaceableTextures\\CommandButtons\\BTNNagaSeaWitch.blp"
    elseif ut == 'Nbrn' or ut == 'Usyl' then
        return "ReplaceableTextures\\CommandButtons\\BTNBansheeRanger.blp"
    elseif ut == 'Npbm' or ut == 'Nsjs' then
        return "ReplaceableTextures\\CommandButtons\\BTNPandarenBrewmaster.blp"
    elseif ut == 'Nbst' then
        return "ReplaceableTextures\\CommandButtons\\BTNBeastMaster.blp"
    elseif ut == 'Nalc' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroAlchemist.blp"
    elseif ut == 'Ntin' or ut == 'Nrob' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroTinker.blp"
    elseif ut == 'Nfir' then
        return "ReplaceableTextures\\CommandButtons\\BTNHeroAvatarOfFlame.blp"
    elseif ut == 'Naka' then
        return "ReplaceableTextures\\CommandButtons\\BTNDranaiAkama.blp"
    endif
    return "ReplaceableTextures\\CommandButtons\\BTNSelectHeroOn.blp"
endfunction

function Asn_GetCounterTypeForTarget takes unit t returns integer
    local integer ut = GetUnitTypeId(t)
    if ut == 'H006' then
        return 'u005'
    elseif ut == 'H003' then
        return 'u006'
    elseif ut == 'H004' then
        return 'u007'
    elseif ut == 'H005' then
        return 'u008'
    elseif ut == 'H002' then
        return 'u009'
    endif
    return 'u00A'
endfunction

function Asn_GetKillerSquadName takes integer kType returns string
    if kType == 'u005' then
        return "|cffff3366破法弑神者小队|r"
    elseif kType == 'u006' then
        return "|cff66ccff禁魔镇魂石像小队|r"
    elseif kType == 'u007' then
        return "|cffffaa22净世焚虫机甲小队|r"
    elseif kType == 'u008' then
        return "|cffcc66ff猎灵破法裁决者小队|r"
    elseif kType == 'u009' then
        return "|cff33ffff破妄真瞳猎手小队|r"
    endif
    return "|cffffdd44圣光混乱裁决者小队|r"
endfunction

function Asn_GetCounterDesc takes unit t returns string
    local integer ut = GetUnitTypeId(t)
    if ut == 'H006' then
        return "混乱远程+无视法轮适应与护甲+纯粹真伤，击中绝不涨抗性且直接破除/泯灭涅槃金卵"
    elseif ut == 'H003' then
        return "永久魔免免疫竭心光环+因果必中破闪避+真视+10倍清分身，击杀封印业火复仇"
    elseif ut == 'H004' then
        return "魔免机体免疫捕食吞噬并灼烧反噬+震破潜地伪装+压制三阶吸血+净世烈焰真伤"
    elseif ut == 'H005' then
        return "550码对空破法+8倍清场伥鬼军团+无视巨龙魔免破灵真伤，绝不被收编为伥鬼"
    elseif ut == 'H002' then
        return "免疫幻梦奴役+10倍伤害瞬清幻象+真视破除潜行+高额破妄真伤直取本尊"
    endif
    return "高强度圣光混乱灌伤小队，精准倾泻无视护甲与魔免的纯粹圣光裁决重击，3倍速清护卫"
endfunction

function Asn_GetUnitDisplayLabel takes unit t returns string
    local integer ut = GetUnitTypeId(t)
    local integer lv = IMaxBJ(1, GetUnitLevel(t))
    local integer pId = GetPlayerId(GetOwningPlayer(t))
    local string nm = GetUnitName(t)
    if ut == 'H006' then
        if pId >= 0 and pId <= 7 and udg_Maho_InEgg[pId] then
            return "魔虚罗(金卵涅槃中)"
        elseif pId >= 0 and pId <= 7 and udg_Maho_IsWinged[pId] then
            return "圣翼·魔虚罗 Lv." + I2S(lv)
        endif
        return "魔虚罗 Lv." + I2S(lv)
    elseif ut == 'H004' and pId >= 0 and pId <= 7 and udg_Strain_EvoStage[pId] >= 3 then
        return "四阶虫皇·利维坦 Lv." + I2S(lv)
    elseif ut == 'Uwar' then
        return "毁灭魔王·阿克蒙德 Lv." + I2S(lv)
    endif
    return nm + " Lv." + I2S(lv)
endfunction

function Asn_CalcQuote takes unit t returns integer
    local integer ut = GetUnitTypeId(t)
    local integer pId = GetPlayerId(GetOwningPlayer(t))
    local integer lv = IMaxBJ(1, GetUnitLevel(t))
    local real maxHp = GetUnitState(t, UNIT_STATE_MAX_LIFE)
    local integer dmg = BlzGetUnitBaseDamage(t, 0)
    local real arm = RMaxBJ(0.0, BlzGetUnitArmor(t))
    local real score = 350.0
    local real avgAdapt = 0.0
    local integer tc = 0

    if maxHp < 400.0 then
        set maxHp = 400.0
    endif
    set score = 320.0 + I2R(lv) * 145.0 + maxHp * 0.22 + I2R(dmg) * 4.5 + arm * 38.0

    if ut == 'H006' and pId >= 0 and pId <= 7 then
        set avgAdapt = Asn_GetMahoAvgAdapt(pId)
        set score = score + avgAdapt * 3200.0
        if udg_Maho_IsWinged[pId] then
            set score = score + 1400.0
        endif
        if udg_Maho_AntiMahoAdapt[pId] > 0.01 then
            set score = score + udg_Maho_AntiMahoAdapt[pId] * 450.0
        endif
        set score = score * 1.15
    elseif ut == 'H004' and pId >= 0 and pId <= 7 then
        set score = score + I2R(udg_Strain_EvoStage[pId]) * 650.0 + I2R(udg_Strain_DevourCount[pId]) * 55.0
    elseif ut == 'H005' and pId >= 0 and pId <= 7 then
        if udg_Wild_ArmyGroup != null then
            set tc = CountUnitsInGroup(udg_Wild_ArmyGroup)
        endif
        set score = score + I2R(udg_Wild_SoulStacks[pId]) * 18.0 + I2R(IMinBJ(tc, 20)) * 120.0
    elseif ut == 'H003' and pId >= 0 and pId <= 7 then
        if udg_Ninja_CloneGroup[pId] != null then
            set score = score + I2R(CountUnitsInGroup(udg_Ninja_CloneGroup[pId])) * 220.0
        endif
        if lv >= 6 then
            set score = score + 450.0
        endif
    elseif ut == 'H002' then
        if GetUnitAbilityLevel(t, 'A004') > 0 then
            set score = score + 650.0
        endif
    elseif ut == 'Uwar' or ut == 'Nklj' or ut == 'Nman' or ut == 'Nmag' then
        set score = score + 1200.0
    endif

    // 向上取整至 50 黄金，最低保底 400
    set tc = ((R2I(score) + 49) / 50) * 50
    if tc < 400 then
        set tc = 400
    endif
    return tc
endfunction

function Asn_GetDefaultHumanBuyer takes nothing returns player
    local integer i = 0
    if udg_Asn_LastBuyer != null and GetPlayerController(udg_Asn_LastBuyer) == MAP_CONTROL_USER and GetPlayerSlotState(udg_Asn_LastBuyer) == PLAYER_SLOT_STATE_PLAYING then
        return udg_Asn_LastBuyer
    endif
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER then
            return Player(i)
        endif
        set i = i + 1
    endloop
    return Player(0)
endfunction

function Asn_SetShopAbilVisible takes integer slotIdx, boolean visible returns nothing
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
endfunction

function Asn_RefreshBoard takes nothing returns nothing
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
    call GroupEnumUnitsInRect(g, bj_mapInitialPlayableArea, null)
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
            endif

            if udg_Asn_SlotHidden[s] or udg_Asn_SlotLastUnit[s] != u or udg_Asn_SlotLastIcon[s] != iconPath then
                call BlzSetAbilityIcon(abilId, iconPath)
                set udg_Asn_SlotLastIcon[s] = iconPath
                set udg_Asn_SlotLastUnit[s] = u
                call Asn_SetShopAbilVisible(s, false)
                call Asn_SetShopAbilVisible(s, true)
            endif
            call BlzSetAbilityTooltip(abilId, tipStr, 0)
            call BlzSetAbilityExtendedTooltip(abilId, extStr, 0)
        else
            set udg_Asn_BoardUnit[s] = null
            set udg_Asn_BoardPrice[s] = 0
            set udg_Asn_SlotLastUnit[s] = null
            if not udg_Asn_SlotHidden[s] then
                call Asn_SetShopAbilVisible(s, false)
            endif
        endif
        set s = s + 1
    endloop
    set u = null
    set buyer = null
endfunction

function Asn_ApplyAllianceForBuyerAndVictim takes player buyer, player victim returns nothing
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
endfunction

function Asn_StyleAndBuffKiller takes unit k, integer c, integer kType, integer wave returns nothing
    local real scaleMul = 1.0 + 0.65 * I2R(wave - 1)
    local real dmgMul = 1.0 + 0.75 * I2R(wave - 1)
    local integer hp = R2I(I2R(udg_Asn_ConBaseHP[c]) * scaleMul)
    local integer dmg = R2I(I2R(udg_Asn_ConBaseDmg[c]) * dmgMul)
    local real arm = udg_Asn_ConBaseArmor[c] + 6.0 * I2R(wave - 1)

    if hp < 2500 then
        set hp = 2500
    endif
    if dmg < 120 then
        set dmg = 120
    endif

    call BlzSetUnitMaxHP(k, hp)
    call SetWidgetLife(k, I2R(hp))
    call BlzSetUnitBaseDamage(k, dmg, 0)
    call BlzSetUnitBaseDamage(k, dmg, 1)
    call BlzSetUnitArmor(k, arm)
    call SetUnitMoveSpeed(k, RMinBJ(522.0, 445.0 + 18.0 * I2R(wave - 1)))
    call BlzSetUnitAttackCooldown(k, RMaxBJ(0.32, 0.82 - 0.08 * I2R(wave - 1)), 0)
    call SetUnitAcquireRange(k, 1400.0)
    call RemoveGuardPosition(k)

    // 专属幻彩染身便于玩家直观辨识各克制小队
    if kType == 'u005' then
        call SetUnitVertexColor(k, 255, 65, 95, 255)
    elseif kType == 'u006' then
        call SetUnitVertexColor(k, 140, 210, 255, 255)
    elseif kType == 'u007' then
        call SetUnitVertexColor(k, 255, 185, 70, 255)
    elseif kType == 'u008' then
        call SetUnitVertexColor(k, 220, 120, 255, 255)
    elseif kType == 'u009' then
        call SetUnitVertexColor(k, 90, 245, 255, 255)
    else
        call SetUnitVertexColor(k, 255, 235, 115, 255)
    endif
endfunction

function Asn_SpawnWave takes integer c returns nothing
    local unit tgt = udg_Asn_ConTarget[c]
    local integer kType = udg_Asn_ConKillerType[c]
    local integer wave = udg_Asn_ConWave[c]
    local real sx = udg_Asn_ConSpawnX[c]
    local real sy = udg_Asn_ConSpawnY[c]
    local integer count = 4 + (wave - 1) * 2
    local integer i = 0
    local real ang = 0.0
    local real px = 0.0
    local real py = 0.0
    local unit k = null
    local unit combatTgt = Asn_GetCombatUnitForTarget(tgt)

    if count > 12 then
        set count = 12
    endif

    // 按目标实时强度动态校准第 1 波基线面板，确保同等级灌死（高强度目标起手即更高配小队）
    if wave == 1 and tgt != null then
        set udg_Asn_ConBaseHP[c] = IMaxBJ(2800, R2I(GetUnitState(tgt, UNIT_STATE_MAX_LIFE) * 1.15) + 1200)
        set udg_Asn_ConBaseDmg[c] = IMaxBJ(140, R2I(GetUnitState(tgt, UNIT_STATE_MAX_LIFE) * 0.045) + BlzGetUnitBaseDamage(tgt, 0) + 95)
        set udg_Asn_ConBaseArmor[c] = RMaxBJ(12.0, BlzGetUnitArmor(tgt) * 0.55 + 10.0)
        if GetUnitTypeId(tgt) == 'H006' and Asn_GetMahoAvgAdapt(GetPlayerId(GetOwningPlayer(tgt))) >= 0.45 then
            set count = 5
            set udg_Asn_ConBaseHP[c] = udg_Asn_ConBaseHP[c] + 2200
            set udg_Asn_ConBaseDmg[c] = udg_Asn_ConBaseDmg[c] + 150
        endif
    endif

    call Asn_ApplyAllianceForBuyerAndVictim(udg_Asn_ConBuyer[c], udg_Asn_ConVictimOwner[c])

    set i = 0
    loop
        exitwhen i >= count
        if udg_Asn_KillerCount < 96 then
            set ang = I2R(i) * (6.28318 / I2R(count))
            set px = sx + 170.0 * Cos(ang)
            set py = sy + 170.0 * Sin(ang)
            set k = CreateUnit(Player(26), kType, px, py, 270.0)
            if k != null then
                call Asn_StyleAndBuffKiller(k, c, kType, wave)
                set udg_Asn_KillerUnit[udg_Asn_KillerCount] = k
                set udg_Asn_KillerCon[udg_Asn_KillerCount] = c
                set udg_Asn_KillerLastX[udg_Asn_KillerCount] = px
                set udg_Asn_KillerLastY[udg_Asn_KillerCount] = py
                set udg_Asn_KillerStuck[udg_Asn_KillerCount] = 0
                set udg_Asn_KillerCount = udg_Asn_KillerCount + 1

                call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Undead\\DarkRitual\\DarkRitualTarget.mdl", px, py))
                if combatTgt != null then
                    call IssueTargetOrder(k, "attack", combatTgt)
                endif
            endif
        endif
        set i = i + 1
    endloop
    set k = null
    set combatTgt = null

    if tgt != null then
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff3366【幽影暗杀出动】|r 第 |cffffcc00" + I2S(wave) + "|r 波 " + Asn_GetKillerSquadName(kType) + "（" + I2S(count) + "名）已受雇出征，猎杀目标：【" + Asn_GetUnitDisplayLabel(tgt) + "】！")
        if GetLocalPlayer() == udg_Asn_ConBuyer[c] then
            call PingMinimapEx(sx, sy, 4.0, 255, 50, 100, false)
        endif
    endif
    set tgt = null
endfunction

function Asn_ClearContractUnits takes integer c returns nothing
    local integer i = 0
    local unit k = null
    loop
        exitwhen i >= udg_Asn_KillerCount
        if udg_Asn_KillerCon[i] == c then
            set k = udg_Asn_KillerUnit[i]
            if k != null then
                call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\NightElf\\Blink\\BlinkCaster.mdl", GetUnitX(k), GetUnitY(k)))
                call RemoveUnit(k)
            endif
            set udg_Asn_KillerCount = udg_Asn_KillerCount - 1
            set udg_Asn_KillerUnit[i] = udg_Asn_KillerUnit[udg_Asn_KillerCount]
            set udg_Asn_KillerCon[i] = udg_Asn_KillerCon[udg_Asn_KillerCount]
            set udg_Asn_KillerLastX[i] = udg_Asn_KillerLastX[udg_Asn_KillerCount]
            set udg_Asn_KillerLastY[i] = udg_Asn_KillerLastY[udg_Asn_KillerCount]
            set udg_Asn_KillerStuck[i] = udg_Asn_KillerStuck[udg_Asn_KillerCount]
            set udg_Asn_KillerUnit[udg_Asn_KillerCount] = null
            set i = i - 1
        endif
        set i = i + 1
    endloop
    set k = null
endfunction

function Asn_OnDamagedHook takes unit src, unit tgt, real dmg returns real
    local integer c = -1
    local integer srcCon = -1
    local integer wave = 1
    local integer tgtType = 0
    local integer pId = 0
    local real trueDmg = 0.0
    local real bonusMult = 1.0
    local real curArmor = 0.0
    local real armorRed = 0.0
    local real curLife = 0.0

    if src == null or tgt == null or dmg <= 0.5 then
        return dmg
    endif

    // 1. 若杀手小队遭到任何单位袭击，立即将其锁定为阻碍目标并全面转敌对，顺路毁灭！
    if Asn_IsAssassin(tgt) then
        set c = Asn_FindKillerContract(tgt)
        if c >= 0 and src != udg_Asn_ConTarget[c] then
            if udg_Asn_ConBuyer[c] == null or not IsUnitAlly(src, udg_Asn_ConBuyer[c]) then
                set udg_Asn_ConBlocker[c] = src
                call SetPlayerAlliance(Player(26), GetOwningPlayer(src), ALLIANCE_PASSIVE, false)
                call SetPlayerAlliance(GetOwningPlayer(src), Player(26), ALLIANCE_PASSIVE, false)
            endif
        endif
        return dmg
    endif

    // 2. 杀手出击：实施针对性克制真伤与顺路碎障倍伤！
    set srcCon = Asn_FindKillerContract(src)
    if srcCon >= 0 then
        set wave = IMaxBJ(1, udg_Asn_ConWave[srcCon])
        set tgtType = GetUnitTypeId(tgt)
        set pId = GetPlayerId(GetOwningPlayer(tgt))

        // 判断是否是正在追杀的主目标（或正在变金卵中的魔虚罗）
        if Asn_IsAssassinForContractTarget(src, tgt) then
            // 先忽略目标护甲还原混乱实伤
            set curArmor = BlzGetUnitArmor(tgt)
            if curArmor > 0.0 then
                set armorRed = (curArmor * 0.06) / (1.0 + curArmor * 0.06)
                if armorRed < 0.95 then
                    set dmg = dmg / (1.0 - armorRed)
                endif
            endif

            if GetUnitTypeId(src) == 'u005' then
                // 反魔虚罗：绝对真伤，无视适应与金卵无敌
                if tgtType == 'u004' then
                    set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * 0.35
                else
                    set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.24, 0.08 + 0.025 * I2R(wave))
                endif
            elseif GetUnitTypeId(src) == 'u006' then
                // 反魔音忍者：强行熄灭竭心光环 + 真伤
                if tgtType == 'H003' and pId >= 0 and pId <= 7 then
                    if udg_Ninja_AuraOn[pId] then
                        set udg_Ninja_AuraOn[pId] = false
                        if udg_Ninja_AuraFx[pId] != null then
                            call DestroyEffect(udg_Ninja_AuraFx[pId])
                            set udg_Ninja_AuraFx[pId] = null
                        endif
                    endif
                endif
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.22, 0.07 + 0.02 * I2R(wave))
            elseif GetUnitTypeId(src) == 'u007' then
                // 反异种虫皇：震破潜地/伪装 + 净化焚烧真伤
                if tgtType == 'H004' and pId >= 0 and pId <= 7 then
                    if udg_Strain_Burrowed[pId] then
                        call Strain_Unburrow(tgt, pId)
                    endif
                    if udg_Strain_MimicActive[pId] then
                        call Strain_BreakMimicry(tgt, pId)
                    endif
                endif
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.22, 0.07 + 0.02 * I2R(wave))
            elseif GetUnitTypeId(src) == 'u008' then
                // 反万灵化身：破灵无视魔免斩首真伤
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.22, 0.07 + 0.02 * I2R(wave))
            elseif GetUnitTypeId(src) == 'u009' then
                // 反幻梦大师：破妄破隐 + 真伤
                if tgtType == 'H002' then
                    call DM_BreakInvisibility(tgt, src)
                endif
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.24, 0.08 + 0.02 * I2R(wave))
            else
                // 圣光混乱裁决者 (u00A)：对阿克蒙德等恶魔Boss与常规英雄灌伤
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.22, 0.065 + 0.02 * I2R(wave))
            endif

            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\CriticalStrike\\CriticalStrikeTarget.mdl", tgt, "origin"))
            set curLife = GetWidgetLife(tgt)
            if dmg + trueDmg >= curLife - 0.5 then
                // 直接让本击以纯粹致命伤害归因于杀手完成击杀！
                return curLife + 9999.0
            elseif trueDmg > 0.0 then
                call SetWidgetLife(tgt, curLife - trueDmg)
            endif
            return dmg
        else
            // 路上遇到的召唤物、幻象、魔音分身、伥鬼与普通阻碍单位：高倍清障销毁！
            if GetUnitTypeId(src) == 'u006' and (IsUnitIllusion(tgt) or IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitInGroup(tgt, udg_FakeHeroGroup) or tgtType == 'u001' or tgtType == 'u002') then
                set bonusMult = 10.0
            elseif GetUnitTypeId(src) == 'u009' and (IsUnitIllusion(tgt) or IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitInGroup(tgt, udg_FakeHeroGroup)) then
                set bonusMult = 10.0
            elseif GetUnitTypeId(src) == 'u008' and (IsUnitIllusion(tgt) or IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitInGroup(tgt, udg_Wild_ArmyGroup) or tgtType == 'u003') then
                set bonusMult = 8.0
            elseif IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitIllusion(tgt) then
                set bonusMult = 3.0
            else
                set bonusMult = 2.5
            endif
            return dmg * bonusMult
        endif
    endif

    return dmg
endfunction

function Asn_OnSelectUnit takes nothing returns boolean
    local unit u = GetTriggerUnit()
    local player p = GetTriggerPlayer()
    if u != null and GetUnitTypeId(u) == 'n005' and GetPlayerController(p) == MAP_CONTROL_USER then
        set udg_Asn_LastBuyer = p
        call Asn_RefreshBoard()
    endif
    set u = null
    set p = null
    return false
endfunction

function Asn_OnCastAbility takes unit shop, integer abilId returns boolean
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
    call Asn_SpawnWave(freeC)
    call Asn_RefreshBoard()

    set buyer = null
    set tgt = null
    return true
endfunction

function Asn_Loop takes nothing returns nothing
    local integer c = 0
    local integer i = 0
    local unit k = null
    local unit tgt = null
    local unit combatTgt = null
    local unit blocker = null
    local unit orderTgt = null
    local integer aliveK = 0
    local real kx = 0.0
    local real ky = 0.0
    local real tx = 0.0
    local real ty = 0.0
    local real dx = 0.0
    local real dy = 0.0
    local real dist = 0.0
    local real stepAng = 0.0
    local real bx = 0.0
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
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffff6600【暗杀升级警报！】|r 第 " + I2S(udg_Asn_ConWave[c]) + " 波杀手已被拦下！幽影公会正在集结更庞大的第 " + I2S(udg_Asn_ConWave[c] + 1) + " 波强化杀手小队（3秒后抵达）...")
                    else
                        set udg_Asn_ConRespawnCD[c] = udg_Asn_ConRespawnCD[c] - 1.0
                        if udg_Asn_ConRespawnCD[c] <= 0.0 then
                            set udg_Asn_ConWave[c] = udg_Asn_ConWave[c] + 1
                            call Asn_SpawnWave(c)
                        endif
                    endif
                endif
            endif
        endif
        set c = c + 1
    endloop

    // 2. 驱动每一个在编杀手的狩猎、顺路清障与防卡死暗影步 AI
    set i = 0
    loop
        exitwhen i >= udg_Asn_KillerCount
        set k = udg_Asn_KillerUnit[i]
        set c = udg_Asn_KillerCon[i]
        if k != null and not IsUnitType(k, UNIT_TYPE_DEAD) and GetWidgetLife(k) > 0.405 and c >= 0 and udg_Asn_ConActive[c] then
            set tgt = udg_Asn_ConTarget[c]
            set combatTgt = Asn_GetCombatUnitForTarget(tgt)
            set blocker = udg_Asn_ConBlocker[c]
            if blocker != null and (IsUnitType(blocker, UNIT_TYPE_DEAD) or GetWidgetLife(blocker) <= 0.405) then
                set udg_Asn_ConBlocker[c] = null
                set blocker = null
            endif

            set kx = GetUnitX(k)
            set ky = GetUnitY(k)
            set orderTgt = combatTgt
            if blocker != null and combatTgt != null then
                // 若主目标距离较远而阻碍者就在 750 码内，顺手碾碎阻碍者！
                set dx = GetUnitX(combatTgt) - kx
                set dy = GetUnitY(combatTgt) - ky
                if dx * dx + dy * dy > 360000.0 then
                    set dx = GetUnitX(blocker) - kx
                    set dy = GetUnitY(blocker) - ky
                    if dx * dx + dy * dy <= 562500.0 then
                        set orderTgt = blocker
                    endif
                endif
            elseif blocker != null then
                set orderTgt = blocker
            endif

            if orderTgt != null and not IsUnitType(orderTgt, UNIT_TYPE_DEAD) and GetWidgetLife(orderTgt) > 0.405 then
                set tx = GetUnitX(orderTgt)
                set ty = GetUnitY(orderTgt)
                set dx = tx - kx
                set dy = ty - ky
                set dist = SquareRoot(dx * dx + dy * dy)

                // 卡地形自救闪烁
                if (kx - udg_Asn_KillerLastX[i]) * (kx - udg_Asn_KillerLastX[i]) + (ky - udg_Asn_KillerLastY[i]) * (ky - udg_Asn_KillerLastY[i]) < 6400.0 and dist > 750.0 and GetUnitCurrentOrder(k) != 851983 then
                    set udg_Asn_KillerStuck[i] = udg_Asn_KillerStuck[i] + 1
                    if udg_Asn_KillerStuck[i] >= 5 then
                        set udg_Asn_KillerStuck[i] = 0
                        set stepAng = Atan2(dy, dx)
                        set bx = kx + 600.0 * Cos(stepAng)
                        set by = ky + 600.0 * Sin(stepAng)
                        if not IsTerrainPathable(bx, by, PATHING_TYPE_WALKABILITY) then
                            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\NightElf\\Blink\\BlinkCaster.mdl", kx, ky))
                            call SetUnitPosition(k, bx, by)
                            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\NightElf\\Blink\\BlinkTarget.mdl", bx, by))
                        endif
                    endif
                else
                    set udg_Asn_KillerStuck[i] = 0
                endif
                set udg_Asn_KillerLastX[i] = kx
                set udg_Asn_KillerLastY[i] = ky

                // 使用 attack-move 确保即使沿途遇到普通敌军也能顺路攻击砍翻
                if dist <= 680.0 and not IsUnitInvisible(orderTgt, Player(26)) then
                    call IssueTargetOrder(k, "attack", orderTgt)
                else
                    call IssuePointOrder(k, "attack", tx, ty)
                endif
            endif
        endif
        set i = i + 1
    endloop

    // 每 2 秒顺带同步刷新一次报价与敌方英雄头像面板
    call Asn_RefreshBoard()

    set k = null
    set tgt = null
    set combatTgt = null
    set blocker = null
    set orderTgt = null
endfunction

function Asn_SpawnAgencyAt takes real nearX, real nearY returns unit
    local integer baseCliff = GetTerrainCliffLevel(nearX, nearY)
    local real searchR = 320.0
    local real searchAngle = 0.0
    local real px = nearX
    local real py = nearY
    local boolean found = false
    local unit shop = null
    local texttag tt = null

    loop
        exitwhen searchR > 1600.0 or found
        set px = nearX + searchR * Cos(searchAngle)
        set py = nearY + searchR * Sin(searchAngle)
        if Refuge_IsSafeTerrainPoint(px, py, baseCliff, true) then
            // 同时避开酒馆自身中心 280 码内以免重合
            if (px - nearX) * (px - nearX) + (py - nearY) * (py - nearY) >= 90000.0 then
                set found = true
            endif
        endif
        if not found then
            set searchAngle = searchAngle + 0.5
            set searchR = searchR + 10.0
        endif
    endloop
    if not found then
        set px = nearX
        set py = nearY - 420.0
    endif

    set shop = CreateUnit(Player(25), 'n005', px, py, 270.0)
    if shop != null then
        call SetUnitInvulnerable(shop, true)
        call SetUnitVertexColor(shop, 185, 130, 225, 255)
        set udg_Asn_Shop[udg_Asn_ShopCount] = shop
        set udg_Asn_ShopCount = udg_Asn_ShopCount + 1

        set tt = CreateTextTag()
        call SetTextTagText(tt, "|cffff3366【暗杀介绍所】|r|n|cffffcc00点击雇佣针对性必杀杀手|r", 0.024)
        call SetTextTagPos(tt, px - 200.0, py - 80.0, 210.0)
        call SetTextTagColor(tt, 255, 255, 255, 255)
        call SetTextTagPermanent(tt, true)
        call SetTextTagVisibility(tt, true)
        set tt = null
    endif
    return shop
endfunction

function Asn_InitSystem takes nothing returns nothing
    local integer i = 0
    local trigger tSel = CreateTrigger()
    local unit s1 = null
    local unit s2 = null

    set udg_Asn_SlotAbil[0] = 'A050'
    set udg_Asn_SlotAbil[1] = 'A051'
    set udg_Asn_SlotAbil[2] = 'A052'
    set udg_Asn_SlotAbil[3] = 'A053'
    set udg_Asn_SlotAbil[4] = 'A054'
    set udg_Asn_SlotAbil[5] = 'A055'
    set udg_Asn_SlotAbil[6] = 'A056'
    set udg_Asn_SlotAbil[7] = 'A057'
    set udg_Asn_SlotAbil[8] = 'A058'
    set udg_Asn_SlotAbil[9] = 'A059'

    set i = 0
    loop
        exitwhen i >= 10
        set udg_Asn_SlotHidden[i] = false
        set udg_Asn_SlotLastUnit[i] = null
        set udg_Asn_SlotLastIcon[i] = ""
        set i = i + 1
    endloop

    // 允许人类玩家选中并操作中立建筑 n005 (Player 25) 购买暗杀契约，AI绝不共享控制
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER then
            call SetPlayerAlliance(Player(25), Player(i), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(25), Player(i), ALLIANCE_SHARED_VISION, true)
            call SetPlayerAlliance(Player(25), Player(i), ALLIANCE_SHARED_CONTROL, true)
            call SetPlayerAlliance(Player(i), Player(25), ALLIANCE_PASSIVE, true)

            call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_SHARED_VISION, true)
            call SetPlayerAlliance(Player(26), Player(i), ALLIANCE_SHARED_CONTROL, false)
            call SetPlayerAlliance(Player(i), Player(26), ALLIANCE_PASSIVE, true)

            call TriggerRegisterPlayerSelectionEventBJ(tSel, Player(i), true)
        else
            call SetPlayerAlliance(Player(25), Player(i), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(i), Player(25), ALLIANCE_PASSIVE, true)
        endif
        set i = i + 1
    endloop
    call TriggerAddCondition(tSel, Condition(function Asn_OnSelectUnit))
    set tSel = null

    // 在东西两座中立酒馆旁各自建设一座暗杀介绍所
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

    call Asn_RefreshBoard()
    call TimerStart(CreateTimer(), 1.25, true, function Asn_Loop)
    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 10.0, "|cffff3366【暗杀介绍所已开业】|r 东西中立酒馆旁已开放【暗杀介绍所】：可凭敌方头像按实时战力报价雇佣针对性必杀杀手！输入 |-kill|r 一键直达！")
endfunction

function Asn_OnStartTimer takes nothing returns nothing
    local timer t = GetExpiredTimer()
    call PauseTimer(t)
    call DestroyTimer(t)
    set t = null
    call Asn_InitSystem()
endfunction
'''


def apply():
    with open(JASS_PATH, "r", encoding="utf-8") as f:
        txt = f.read().replace("\r\n", "\n")

    patches = []

    # 1. 添加全局变量
    t1 = """    real udg_Refuge_SafeX = 0.0
    real udg_Refuge_SafeY = 0.0"""
    r1 = t1 + "\n" + GLOBALS_ADD
    patches.append(("Add Asn globals", t1, r1))

    # 1.5. Early declaration of Asn_IsAssassinType / Asn_IsAssassin before DM_CapTimerLoop & Ninja_AuraTick
    t1b = """function Maho_IsUnitAlive takes unit u returns boolean"""
    r1b = ASN_EARLY_HELPERS + "\n" + t1b
    patches.append(("Insert early Asn helpers", t1b, r1b))

    # 2. 魔音光环豁免中立杀手
    t2 = """                        if IsUnitEnemy(enumU, Player(pId)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' then"""
    r2 = """                        if IsUnitEnemy(enumU, Player(pId)) and not IsUnitType(enumU, UNIT_TYPE_DEAD) and not IsUnitType(enumU, UNIT_TYPE_STRUCTURE) and GetUnitTypeId(enumU) != 'u000' and not Asn_IsAssassin(enumU) then"""
    patches.append(("Ninja aura exclude assassins", t2, r2))

    # 3. 幻梦奴役 A002 免疫杀手
    t3 = """    if target == null or origPlayer == casterPlayer then
        return
    endif"""
    r3 = """    if target == null or origPlayer == casterPlayer or Asn_IsAssassin(target) then
        if Asn_IsAssassin(target) then
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", target, "origin"))
            call DisplayTimedTextToPlayer(casterPlayer, 0, 0, 4.0, "|cffff3366[暗杀免疫]|r 幽影公会杀手意志绝对独立，免疫一切心智奴役！")
        endif
        return
    endif"""
    patches.append(("DM_CastPossession exclude assassins", t3, r3))

    # 4. 在 DM_OnSpellEffect 之前插入全套 Asn 系统实现，并接管 A050~A05A
    t4 = """function DM_OnSpellEffect takes nothing returns boolean"""
    r4 = ASN_SYSTEM_CODE + "\n" + t4
    patches.append(("Insert Asn system before DM_OnSpellEffect", t4, r4))

    t5 = """    if abil == 'A001' then"""
    r5 = """    if abil >= 'A050' and abil <= 'A05A' then
        if GetUnitTypeId(caster) == 'n005' then
            call Asn_OnCastAbility(caster, abil)
        endif
        set caster = null
        return false
    endif

    if abil == 'A001' then"""
    patches.append(("Hook A050..A05A in DM_OnSpellEffect", t5, r5))

    # 5. 异种之源 A022 捕食吞噬遇到杀手免疫+反噬灼烧
    t6 = """        if ult != null then
            if GetUnitTypeId(ult) == 'H006' then"""
    r6 = """        if ult != null then
            if Asn_IsAssassin(ult) then
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\DivineShield\\\\DivineShieldTarget.mdl", ult, "origin"))
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Other\\\\Doom\\\\DoomDeath.mdl", caster, "origin"))
                call SetWidgetLife(caster, RMaxBJ(1.0, GetWidgetLife(caster) - GetUnitState(caster, UNIT_STATE_MAX_LIFE) * 0.10))
                call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 4.0, "|cffff3366[反制免疫]|r 杀手魔免机体无法被吞噬，异种遭受反噬灼烧损失 10% 生命！")
                set ult = null
            elseif GetUnitTypeId(ult) == 'H006' then"""
    patches.append(("A022 devour exclude and punish assassins", t6, r6))

    # 6. DM_OnDamaged: u004 金卵放行反魔虚罗杀手 + 杀手通用克制钩子 + 魔虚罗不对杀手涨抗性/护甲/不变蛋 + 魔音忍者不对杀手分身替死
    t7 = r"""        // Nirvana Golden Egg [u004] Special Damage Filtering
        if GetUnitTypeId(tgt) == 'u004' then
            if dmg >= 50000.0 then
                // Whosyourdaddy cheat bypass
                call BlzSetEventDamage(dmg)
            else
                set srcPid = GetPlayerId(GetOwningPlayer(src))
                if GetUnitTypeId(src) == 'H006' and udg_Maho_AntiMahoAdapt[srcPid] >= 3.9999 and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                    set dmg = dmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.05
                    call BlzSetEventDamage(dmg)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\CriticalStrike\\CriticalStrikeTarget.mdl", tgt, "origin"))
                else
                    call BlzSetEventDamage(0.0)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\DivineShield\\DivineShieldTarget.mdl", tgt, "origin"))
                    set src = null
                    set tgt = null
                    return false
                endif
            endif
        endif"""
    r7 = r"""        // Nirvana Golden Egg [u004] Special Damage Filtering (incl. Assassin executioner u005)
        if GetUnitTypeId(tgt) == 'u004' then
            if dmg >= 50000.0 then
                // Whosyourdaddy cheat bypass
                call BlzSetEventDamage(dmg)
            elseif Asn_IsAssassinForContractTarget(src, tgt) or GetUnitTypeId(src) == 'u005' then
                set dmg = Asn_OnDamagedHook(src, tgt, dmg)
                call BlzSetEventDamage(dmg)
                set src = null
                set tgt = null
                return false
            else
                set srcPid = GetPlayerId(GetOwningPlayer(src))
                if GetUnitTypeId(src) == 'H006' and udg_Maho_AntiMahoAdapt[srcPid] >= 3.9999 and IsUnitEnemy(tgt, GetOwningPlayer(src)) then
                    set dmg = dmg + I2R(BlzGetUnitMaxHP(tgt)) * 0.05
                    call BlzSetEventDamage(dmg)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\CriticalStrike\\CriticalStrikeTarget.mdl", tgt, "origin"))
                else
                    call BlzSetEventDamage(0.0)
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\DivineShield\\DivineShieldTarget.mdl", tgt, "origin"))
                    set src = null
                    set tgt = null
                    return false
                endif
            endif
        endif

        // Assassin Interception Hook (Target Counter-TrueDmg & Blocker Destruction)
        if Asn_IsAssassin(src) or Asn_IsAssassin(tgt) then
            set dmg = Asn_OnDamagedHook(src, tgt, dmg)
            if Asn_IsAssassin(src) then
                call BlzSetEventDamage(dmg)
                set src = null
                set tgt = null
                return false
            endif
        endif"""
    patches.append(("DM_OnDamaged golden egg + assassin hook", t7, r7))

    # 7. Ninja pre-lethal clone swap: blocked if killed by assassin
    t8 = """        // Ninja (A011) - Pre-lethal swap
        if GetUnitTypeId(tgt) == 'H003' and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and not IsUnitIllusion(tgt) then"""
    r8 = """        // Ninja (A011) - Pre-lethal swap (sealed against Assassins)
        if GetUnitTypeId(tgt) == 'H003' and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and not IsUnitIllusion(tgt) and not Asn_IsAssassin(src) then"""
    patches.append(("Seal Ninja pre-lethal swap vs assassins", t8, r8))

    # 8. DM_OnUnitDeath: u004 egg shattered wording, Wild Thrall skip assassins, Ninja Karma/Clone/Swap skip assassins
    t9 = """                    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff0033【因果斩断 · 金卵破碎！】|r 涅槃金卵被四阶弑神魔虚罗当场斩碎，涅槃彻底失败！")"""
    r9 = """                    if killer != null and Asn_IsAssassin(killer) then
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff3366【暗杀处决 · 涅槃金卵泯灭！】|r 幽影公会破法弑神者当场劈碎金卵，魔虚罗真灵被彻底抹杀！")
                    else
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff0033【因果斩断 · 金卵破碎！】|r 涅槃金卵被四阶弑神魔虚罗当场斩碎，涅槃彻底失败！")
                    endif"""
    patches.append(("Golden egg death msg for assassin", t9, r9))

    t10 = """        if killerOwner != null and IsUnitEnemy(dead, killerOwner) and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and not isIllusion and not isFakeHero and not isAnyClone and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'u003' then"""
    r10 = """        if killerOwner != null and IsUnitEnemy(dead, killerOwner) and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and not isIllusion and not isFakeHero and not isAnyClone and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'u003' and not Asn_IsAssassin(dead) then"""
    patches.append(("Wild Thrall enslavement skip assassins", t10, r10))

    t11 = """    // 2. Ninja Karma Mark (ONLY TRUE HERO H003 marks killer; clones NEVER mark killer!)
    if deadType == 'H003' and not isFakeHero and not isIllusion and not isAnyClone and killer != null and IsUnitEnemy(killer, deadOwner) then"""
    r11 = """    // 2. Ninja Karma Mark (ONLY TRUE HERO H003 marks killer; sealed when slain by Assassin!)
    if deadType == 'H003' and not isFakeHero and not isIllusion and not isAnyClone and killer != null and IsUnitEnemy(killer, deadOwner) and not Asn_IsAssassin(killer) then"""
    patches.append(("Seal Ninja Karma mark vs assassins", t11, r11))

    t12 = """    // 5. Ninja Clone Swap Fallback (True Hero death swap into living clone)
    if deadType == 'H003' and not isFakeHero and not isIllusion and not isAnyClone then"""
    r12 = """    // 5. Ninja Clone Swap Fallback (sealed when slain by Assassin!)
    if deadType == 'H003' and not isFakeHero and not isIllusion and not isAnyClone and not Asn_IsAssassin(killer) then"""
    patches.append(("Seal Ninja clone fallback vs assassins", t12, r12))

    # 9. Chat commands: -kill / -assassin / -archimonde
    t13 = """    elseif s == "-refuge" then
        call Refuge_Relocate(p)"""
    r13 = """    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    elseif s == "-kill" or s == "-assassin" then
        set udg_Asn_LastBuyer = p
        call Asn_RefreshBoard()
        if udg_Asn_Shop[0] != null then
            set u = udg_Asn_Shop[0]
            if udg_Asn_Shop[1] != null then
                set startX = GetStartLocationX(GetPlayerStartLocation(p))
                set startY = GetStartLocationY(GetPlayerStartLocation(p))
                if (GetUnitX(udg_Asn_Shop[1]) - startX) * (GetUnitX(udg_Asn_Shop[1]) - startX) + (GetUnitY(udg_Asn_Shop[1]) - startY) * (GetUnitY(udg_Asn_Shop[1]) - startY) < (GetUnitX(udg_Asn_Shop[0]) - startX) * (GetUnitX(udg_Asn_Shop[0]) - startX) + (GetUnitY(udg_Asn_Shop[0]) - startY) * (GetUnitY(udg_Asn_Shop[0]) - startY) then
                    set u = udg_Asn_Shop[1]
                endif
            endif
            if GetLocalPlayer() == p then
                call PanCameraToTimed(GetUnitX(u), GetUnitY(u), 0.25)
                call SelectUnit(u, true)
                call PingMinimapEx(GetUnitX(u), GetUnitY(u), 4.0, 255, 50, 120, false)
            endif
            call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cffff3366【暗杀介绍所】|r 已为你定位并选中最近的暗杀介绍所，可点击右下命令栏内敌方目标头像下单暗杀！")
            set u = null
        endif
    elseif s == "-archimonde" then
        set startX = GetStartLocationX(GetPlayerStartLocation(p))
        set startY = GetStartLocationY(GetPlayerStartLocation(p))
        set g = CreateGroup()
        call GroupEnumUnitsOfPlayer(g, p, null)
        loop
            set u = FirstOfGroup(g)
            exitwhen u == null
            call GroupRemoveUnit(g, u)
            if IsUnitType(u, UNIT_TYPE_HERO) and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
                set startX = GetUnitX(u)
                set startY = GetUnitY(u)
            endif
        endloop
        call DestroyGroup(g)
        set g = null
        set u = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'Uwar', startX + 350.0, startY - 350.0, 180.0)
        if u != null then
            call SetHeroLevel(u, 10, false)
            call BlzSetUnitMaxHP(u, 5200)
            call SetWidgetLife(u, 5200.0)
            call BlzSetUnitBaseDamage(u, 220, 0)
            call BlzSetUnitArmor(u, 20.0)
            call Asn_RefreshBoard()
            call DisplayTimedTextToPlayer(p, 0, 0, 7.0, "|cffff3366[沙盒Boss]|r 已召唤 10 级恶魔领主【阿克蒙德】（5200HP/220攻/20甲），可去暗杀介绍所聘请圣骑士小队体验灌伤处决！")
            set u = null
        endif"""
    patches.append(("Chat commands -kill / -archimonde", t13, r13))

    # 10. Init Asn_OnStartTimer inside DM_InitTriggers (after InitBlizzard)
    t14 = """    call TimerStart(tmrRefuge, 1.50, false, function Refuge_OnStartTimer)"""
    r14 = t14 + "\n    call TimerStart(CreateTimer(), 1.65, false, function Asn_OnStartTimer)"
    patches.append(("Init Asn_OnStartTimer in DM_InitTriggers", t14, r14))

    for name, tgt, rep in patches:
        cnt = txt.count(tgt)
        if cnt != 1:
            raise RuntimeError(f"Patch '{name}' expected count 1, got {cnt}")
        txt = txt.replace(tgt, rep, 1)
        print(f"[ok] {name}")

    with open(JASS_PATH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(txt)
    print(f"[DONE] Patched war3map.j cleanly ({len(txt.splitlines())} lines)")


if __name__ == "__main__":
    apply()
