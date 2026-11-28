# -*- coding: utf-8 -*-
"""
v6.5 补丁：
1. 修复魔音忍者 (H003) 杀手提前消失 Bug：只要本尊活着或场上仍有任意存活分身/神尊，绝不结单，追杀清光所有分身与本尊为止；
   并完整还原魔音忍者对杀手的分身替死机制（消耗分身救命 + 清零当次致命伤害 + 防止忍者杀石像白嫖新分身）。
2. 调弱第 1 波试探先锋（2~3名低门槛配置），改为【每波实时扫描目标最新进化/军团属性再叠加几何级爆涨倍率】的无限反进化强袭系统，
   压制第 2、3、4...N 波持续成长后的魔虚罗/虫皇/万灵化身/阿克蒙德等一切强敌！
"""

JASS_PATH = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j"


def apply():
    with open(JASS_PATH, "r", encoding="utf-8") as f:
        txt = f.read().replace("\r\n", "\n")

    patches = []

    # 1. Asn_IsUnitAliveOrEgg & Asn_GetCombatUnitForTarget：覆盖 H003 场上残留分身
    t1 = """function Asn_IsUnitAliveOrEgg takes unit t returns boolean
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
endfunction"""

    r1 = """function Asn_IsUnitAliveOrEgg takes unit t returns boolean
    local integer pId = 0
    local integer ut = 0
    if t == null then
        return false
    endif
    if not IsUnitType(t, UNIT_TYPE_DEAD) and GetWidgetLife(t) > 0.405 then
        return true
    endif
    set ut = GetUnitTypeId(t)
    set pId = GetPlayerId(GetOwningPlayer(t))
    if ut == 'H006' then
        if pId >= 0 and pId <= 7 and udg_Maho_InEgg[pId] and udg_Maho_EggUnit[pId] != null and not IsUnitType(udg_Maho_EggUnit[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_Maho_EggUnit[pId]) > 0.405 then
            return true
        endif
    elseif ut == 'H003' then
        if pId >= 0 and pId <= 7 and Ninja_PickLivingClone(pId) != null then
            return true
        endif
    endif
    return false
endfunction

function Asn_GetCombatUnitForTarget takes unit t returns unit
    local integer pId = 0
    local integer ut = 0
    local unit cl = null
    if t == null then
        return null
    endif
    set ut = GetUnitTypeId(t)
    set pId = GetPlayerId(GetOwningPlayer(t))
    if ut == 'H006' then
        if pId >= 0 and pId <= 7 and udg_Maho_InEgg[pId] and udg_Maho_EggUnit[pId] != null and not IsUnitType(udg_Maho_EggUnit[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_Maho_EggUnit[pId]) > 0.405 then
            return udg_Maho_EggUnit[pId]
        endif
    elseif ut == 'H003' then
        if (IsUnitType(t, UNIT_TYPE_DEAD) or GetWidgetLife(t) <= 0.405) and pId >= 0 and pId <= 7 then
            set cl = Ninja_PickLivingClone(pId)
            if cl != null then
                return cl
            endif
        endif
    endif
    return t
endfunction"""
    patches.append(("Support Ninja clones in Asn_IsUnitAliveOrEgg & GetCombatUnitForTarget", t1, r1))

    # 2. Asn_StyleAndBuffKiller & Asn_SpawnWave：调弱第1波 + 每波实时重扫目标进化状态 + 几何级大幅暴涨
    t2 = r"""function Asn_StyleAndBuffKiller takes unit k, integer c, integer kType, integer wave returns nothing
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
endfunction"""

    r2 = r"""function Asn_StyleAndBuffKiller takes unit k, integer c, integer kType, integer wave returns nothing
    local real w = I2R(wave - 1)
    local real hpMul = RMinBJ(120.0, 1.0 + 0.90 * w + 0.40 * w * w + 0.12 * w * w * w)
    local real dmgMul = RMinBJ(120.0, 1.0 + 0.85 * w + 0.38 * w * w + 0.12 * w * w * w)
    local real hpR = RMinBJ(1800000.0, I2R(udg_Asn_ConBaseHP[c]) * hpMul)
    local real dmgR = RMinBJ(450000.0, I2R(udg_Asn_ConBaseDmg[c]) * dmgMul)
    local integer hp = R2I(hpR)
    local integer dmg = R2I(dmgR)
    local real arm = udg_Asn_ConBaseArmor[c] * (1.0 + 0.45 * w) + 7.0 * w
    local real sc = RMinBJ(1.75, 0.95 + 0.12 * w)

    if hp < 750 then
        set hp = 750
    endif
    if dmg < 42 then
        set dmg = 42
    endif

    call BlzSetUnitMaxHP(k, hp)
    call SetWidgetLife(k, I2R(hp))
    call BlzSetUnitBaseDamage(k, dmg, 0)
    call BlzSetUnitBaseDamage(k, dmg, 1)
    call BlzSetUnitArmor(k, arm)
    call SetUnitMoveSpeed(k, RMinBJ(522.0, 395.0 + 30.0 * w))
    call BlzSetUnitAttackCooldown(k, RMaxBJ(0.30, 1.15 - 0.15 * w), 0)
    call SetUnitScale(k, sc, sc, sc)
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
    local integer count = 2 + (wave - 1) * 2
    local integer i = 0
    local real ang = 0.0
    local real px = 0.0
    local real py = 0.0
    local unit k = null
    local unit firstK = null
    local unit combatTgt = Asn_GetCombatUnitForTarget(tgt)
    local integer tPid = 0
    local integer tUt = 0
    local real curHP = 0.0
    local integer curAtk = 0
    local real curArm = 0.0
    local integer heroStat = 0
    local real liveScale = 1.0
    local integer tc = 0
    local integer liveBaseHP = 0
    local integer liveBaseDmg = 0
    local real liveBaseArmor = 0.0
    local integer truePctShow = 0

    // 每一波全部重新扫描目标【当前最新进化属性与战力】，叠加后续指数级波次压制！
    if tgt != null then
        set tUt = GetUnitTypeId(tgt)
        set tPid = GetPlayerId(GetOwningPlayer(tgt))
        set curHP = RMaxBJ(800.0, GetUnitState(tgt, UNIT_STATE_MAX_LIFE))
        set curAtk = IMaxBJ(40, BlzGetUnitBaseDamage(tgt, 0))
        if IsUnitType(tgt, UNIT_TYPE_HERO) then
            set heroStat = IMaxBJ(GetHeroStr(tgt, true), IMaxBJ(GetHeroAgi(tgt, true), GetHeroInt(tgt, true)))
            set curAtk = curAtk + heroStat
        endif
        set curArm = RMaxBJ(0.0, BlzGetUnitArmor(tgt))

        set liveScale = 1.0
        if tUt == 'H006' and tPid >= 0 and tPid <= 7 then
            set liveScale = 1.0 + Asn_GetMahoAvgAdapt(tPid) * 1.25 + udg_Maho_AntiMahoAdapt[tPid] * 0.25
            if udg_Maho_IsWinged[tPid] then
                set liveScale = liveScale + 0.65
                if wave == 1 then
                    set count = 3
                endif
            endif
        elseif tUt == 'H004' and tPid >= 0 and tPid <= 7 then
            set liveScale = 1.0 + I2R(udg_Strain_EvoStage[tPid]) * 0.35 + I2R(udg_Strain_DevourCount[tPid]) * 0.025
        elseif tUt == 'H005' and tPid >= 0 and tPid <= 7 then
            if udg_Wild_ArmyGroup != null then
                set tc = CountUnitsInGroup(udg_Wild_ArmyGroup)
            endif
            set liveScale = 1.0 + I2R(udg_Wild_SoulStacks[tPid]) * 0.012 + I2R(IMinBJ(tc, 20)) * 0.08
        elseif tUt == 'H003' and tPid >= 0 and tPid <= 7 then
            if udg_Ninja_CloneGroup[tPid] != null then
                set tc = CountUnitsInGroup(udg_Ninja_CloneGroup[tPid])
            endif
            set liveScale = 1.0 + I2R(tc) * 0.20
        elseif tUt == 'Uwar' or tUt == 'Nklj' or tUt == 'Nman' or tUt == 'Nmag' then
            set liveScale = 1.25
            if wave == 1 then
                set count = 3
            endif
        else
            set liveScale = 1.0 + I2R(IMaxBJ(1, GetUnitLevel(tgt))) * 0.05
        endif

        set liveBaseHP = IMaxBJ(800, R2I(RMinBJ(600000.0, curHP * 0.45 * liveScale)) + 250)
        set liveBaseDmg = IMaxBJ(45, R2I(RMinBJ(120000.0, (curHP * 0.015 + I2R(curAtk) * 0.65) * liveScale)) + 25)
        set liveBaseArmor = RMaxBJ(4.0, curArm * 0.30 + 3.0)

        if wave == 1 then
            set udg_Asn_ConBaseHP[c] = liveBaseHP
            set udg_Asn_ConBaseDmg[c] = liveBaseDmg
            set udg_Asn_ConBaseArmor[c] = liveBaseArmor
        else
            set udg_Asn_ConBaseHP[c] = IMaxBJ(udg_Asn_ConBaseHP[c], liveBaseHP)
            set udg_Asn_ConBaseDmg[c] = IMaxBJ(udg_Asn_ConBaseDmg[c], liveBaseDmg)
            set udg_Asn_ConBaseArmor[c] = RMaxBJ(udg_Asn_ConBaseArmor[c], liveBaseArmor)
        endif
    endif

    if count > 12 then
        set count = 12
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
                if firstK == null then
                    set firstK = k
                endif
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

    if tgt != null then
        set truePctShow = IMinBJ(35, R2I(2.5 + 4.5 * I2R(wave - 1)))
        if firstK != null then
            if wave == 1 then
                call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffff3366【幽影暗杀出动】|r 第 |cffffcc001|r 波试探先锋 " + Asn_GetKillerSquadName(kType) + "（" + I2S(count) + "名，单兵 " + I2S(BlzGetUnitMaxHP(firstK)) + "血/" + I2S(BlzGetUnitBaseDamage(firstK, 0)) + "攻/" + I2S(truePctShow) + "%真伤）出击，追杀【" + Asn_GetUnitDisplayLabel(tgt) + "】！")
            else
                call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 7.0, "|cffff2244【幽影暗杀 · 第 " + I2S(wave) + " 波反进化强袭！】|r 已重扫目标最新战力并大幅升维！派出 " + I2S(count) + " 名" + Asn_GetKillerSquadName(kType) + "（单兵 |cffffdd44" + I2S(BlzGetUnitMaxHP(firstK)) + "血 / " + I2S(BlzGetUnitBaseDamage(firstK, 0)) + "攻 / " + I2S(truePctShow) + "%真伤|r），锁定【" + Asn_GetUnitDisplayLabel(tgt) + "】！")
            endif
        endif
        if GetLocalPlayer() == udg_Asn_ConBuyer[c] then
            call PingMinimapEx(sx, sy, 4.0, 255, 50, 100, false)
        endif
    endif
    set firstK = null
    set k = null
    set combatTgt = null
    set tgt = null
endfunction"""
    patches.append(("Dynamic real-time scaling + geometric wave escalation", t2, r2))

    # 3. Asn_OnDamagedHook：真伤从 2.5% 起步每波 +4.5%（金卵 15% + 8%*(wave-1)），顺路清障倍伤每波递增
    t3 = """            if GetUnitTypeId(src) == 'u005' then
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
            endif"""

    r3 = """            if GetUnitTypeId(src) == 'u005' then
                // 反魔虚罗：绝对真伤（W1 2.5% -> W2 7% -> W3 11.5%... 上限 35%；金卵 W1 15% + 8%/波）
                if tgtType == 'u004' then
                    set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.55, 0.15 + 0.08 * I2R(wave - 1))
                else
                    set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.35, 0.025 + 0.045 * I2R(wave - 1))
                endif
            elseif GetUnitTypeId(src) == 'u006' then
                // 反魔音忍者：强行熄灭竭心光环 + 逐波递增真伤
                if tgtType == 'H003' and pId >= 0 and pId <= 7 then
                    if udg_Ninja_AuraOn[pId] then
                        set udg_Ninja_AuraOn[pId] = false
                        if udg_Ninja_AuraFx[pId] != null then
                            call DestroyEffect(udg_Ninja_AuraFx[pId])
                            set udg_Ninja_AuraFx[pId] = null
                        endif
                    endif
                endif
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.35, 0.025 + 0.045 * I2R(wave - 1))
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
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.35, 0.025 + 0.045 * I2R(wave - 1))
            elseif GetUnitTypeId(src) == 'u008' then
                // 反万灵化身：破灵无视魔免斩首真伤
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.35, 0.025 + 0.045 * I2R(wave - 1))
            elseif GetUnitTypeId(src) == 'u009' then
                // 反幻梦大师：破妄破隐 + 真伤
                if tgtType == 'H002' then
                    call DM_BreakInvisibility(tgt, src)
                endif
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.35, 0.025 + 0.045 * I2R(wave - 1))
            else
                // 圣光混乱裁决者 (u00A)：对阿克蒙德等恶魔Boss与常规英雄逐波倍增灌伤
                set trueDmg = I2R(BlzGetUnitMaxHP(tgt)) * RMinBJ(0.35, 0.025 + 0.045 * I2R(wave - 1))
            endif"""
    patches.append(("Scale true damage per wave starting low at W1", t3, r3))

    t4 = """            elseif IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitIllusion(tgt) then
                set bonusMult = 3.0
            else
                set bonusMult = 2.5
            endif"""
    r4 = """            elseif IsUnitType(tgt, UNIT_TYPE_SUMMONED) or IsUnitIllusion(tgt) then
                set bonusMult = 1.8 + 0.6 * I2R(wave - 1)
            else
                set bonusMult = 1.4 + 0.5 * I2R(wave - 1)
            endif"""
    patches.append(("Scale blocker bonus multiplier per wave", t4, r4))

    # 4. Asn_Loop：即使契约主目标在杀手本波全灭前刚换成场上分身或恢复，顺便也防止“魔音忍者还剩分身”时的错报
    t5 = """                if aliveK == 0 then
                    if udg_Asn_ConRespawnCD[c] <= 0.0 then
                        set udg_Asn_ConRespawnCD[c] = 3.0
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffff6600【暗杀升级警报！】|r 第 " + I2S(udg_Asn_ConWave[c]) + " 波杀手已被拦下！幽影公会正在集结更庞大的第 " + I2S(udg_Asn_ConWave[c] + 1) + " 波强化杀手小队（3秒后抵达）...")
                    else"""
    r5 = """                if aliveK == 0 then
                    if udg_Asn_ConRespawnCD[c] <= 0.0 then
                        set udg_Asn_ConRespawnCD[c] = 3.0
                        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 4.0, "|cffff6600【暗杀升级警报！】|r 第 " + I2S(udg_Asn_ConWave[c]) + " 波杀手已被拦下！幽影公会正在重扫目标最新进化状态，集结第 " + I2S(udg_Asn_ConWave[c] + 1) + " 波狂暴反制小队（3秒后抵达）...")
                    else"""
    patches.append(("Update escalation alert message", t5, r5))

    # 5. DM_OnDamaged：当杀手攻击 H003 魔音忍者时，允许穿透至下面的 Ninja Pre-lethal clone swap！
    t6 = """        // Assassin Interception Hook (Target Counter-TrueDmg & Blocker Destruction)
        if Asn_IsAssassin(src) or Asn_IsAssassin(tgt) then
            set dmg = Asn_OnDamagedHook(src, tgt, dmg)
            if Asn_IsAssassin(src) then
                call BlzSetEventDamage(dmg)
                set src = null
                set tgt = null
                return false
            endif
        endif"""
    r6 = """        // Assassin Interception Hook (Target Counter-TrueDmg & Blocker Destruction)
        if Asn_IsAssassin(src) or Asn_IsAssassin(tgt) then
            set dmg = Asn_OnDamagedHook(src, tgt, dmg)
            if Asn_IsAssassin(src) then
                call BlzSetEventDamage(dmg)
                if GetUnitTypeId(tgt) != 'H003' then
                    set src = null
                    set tgt = null
                    return false
                endif
            endif
        endif"""
    patches.append(("Allow assassin damage on H003 to reach Ninja pre-lethal swap", t6, r6))

    # 6. DM_OnDamaged Ninja Pre-lethal swap: 允许杀手触发替死 + 使用 RMaxBJ(dmg, GetEventDamage()) + 替死清零当次伤害
    t7 = """        // Ninja (A011) - Pre-lethal swap (sealed against Assassins)
        if GetUnitTypeId(tgt) == 'H003' and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and not IsUnitIllusion(tgt) and not Asn_IsAssassin(src) then
            set pId = GetPlayerId(GetOwningPlayer(tgt))
            set udg_Ninja_TrueHero[pId] = tgt
            if GetEventDamage() >= (GetWidgetLife(tgt) - 1.0) then
                set c = Ninja_PickLivingClone(pId)
                if c != null then"""
    r7 = """        // Ninja (A011) - Pre-lethal swap (clones keep Ninja alive until all clones are purged)
        if GetUnitTypeId(tgt) == 'H003' and not IsUnitInGroup(tgt, udg_FakeHeroGroup) and not IsUnitIllusion(tgt) then
            set pId = GetPlayerId(GetOwningPlayer(tgt))
            set udg_Ninja_TrueHero[pId] = tgt
            if RMaxBJ(dmg, GetEventDamage()) >= (GetWidgetLife(tgt) - 1.0) then
                set c = Ninja_PickLivingClone(pId)
                if c != null then
                    call BlzSetEventDamage(0.0)"""
    patches.append(("Fix Ninja pre-lethal swap against assassins & zero fatal hit", t7, r7))

    # 7. DM_OnUnitDeath: 击杀杀手不给忍者白刷分身，同时还原死后分身替死复活
    t8 = """    // 4. Ninja Clone on Kill (A011): Clones CANNOT be cloned; victims must not be any clone!
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and not isAnyClone and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'H003' and not isFakeHero and not isIllusion and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u002' or GetUnitTypeId(killer) == 'u001') then"""
    r8 = """    // 4. Ninja Clone on Kill (A011): Clones CANNOT be cloned; assassins do not spawn free clones!
    if killer != null and not IsUnitType(dead, UNIT_TYPE_STRUCTURE) and not isAnyClone and not Asn_IsAssassin(dead) and deadType != 'u000' and deadType != 'u001' and deadType != 'u002' and deadType != 'H003' and not isFakeHero and not isIllusion and (GetUnitTypeId(killer) == 'H003' or GetUnitTypeId(killer) == 'u002' or GetUnitTypeId(killer) == 'u001') then"""
    patches.append(("Prevent Ninja gaining free clones by killing assassins", t8, r8))

    t9 = """    // 5. Ninja Clone Swap Fallback (sealed when slain by Assassin!)
    if deadType == 'H003' and not isFakeHero and not isIllusion and not isAnyClone and not Asn_IsAssassin(killer) then"""
    r9 = """    // 5. Ninja Clone Swap Fallback (revive via living clone until all clones are purged)
    if deadType == 'H003' and not isFakeHero and not isIllusion and not isAnyClone then"""
    patches.append(("Restore Ninja clone fallback revival against assassins", t9, r9))

    for name, tgt, rep in patches:
        cnt = txt.count(tgt)
        if cnt != 1:
            raise RuntimeError(f"Patch '{name}' expected count 1, got {cnt}")
        txt = txt.replace(tgt, rep, 1)
        print(f"[ok] {name}")

    with open(JASS_PATH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(txt)
    print(f"[DONE] v6.5 war3map.j updated ({len(txt.splitlines())} lines)")


if __name__ == "__main__":
    apply()
