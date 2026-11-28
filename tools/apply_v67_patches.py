# -*- coding: utf-8 -*-
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

    # 1. Globals after udg_Asn_AllowSelfTest
    text = replace_once(
        text,
        r'''    boolean udg_Asn_AllowSelfTest = true''',
        r'''    boolean udg_Asn_AllowSelfTest = true

    // Experimental All-Buff / All-Debuff Soldier [u00B] Globals (v6.7)
    unit array udg_BExp_AuraUnit
    real array udg_BExp_AuraTimer
    integer udg_BExp_AuraCount = 0''',
        '1_bexp_globals'
    )

    # 2. BuffExp_* functions directly before DM_OnSpellEffect
    bexp_funcs = r'''//***************************************************************************
//*
//*  Experimental All-Buff / All-Debuff Soldier System (v6.7)
//*
//***************************************************************************

function BuffExp_CastTarget takes player owner, unit tgt, integer abilId, string orderStr returns nothing
    local unit d = null
    if tgt == null or IsUnitType(tgt, UNIT_TYPE_DEAD) or GetWidgetLife(tgt) <= 0.405 then
        return
    endif
    set d = CreateUnit(owner, 'u000', GetUnitX(tgt), GetUnitY(tgt), 0.0)
    if d != null then
        call UnitAddAbility(d, abilId)
        call IssueTargetOrder(d, orderStr, tgt)
        call UnitApplyTimedLife(d, 'BTLF', 1.5)
        set d = null
    endif
endfunction

function BuffExp_CastPoint takes player owner, real x, real y, integer abilId, string orderStr returns nothing
    local unit d = CreateUnit(owner, 'u000', x, y, 0.0)
    if d != null then
        call UnitAddAbility(d, abilId)
        call IssuePointOrder(d, orderStr, x, y)
        call UnitApplyTimedLife(d, 'BTLF', 1.5)
        set d = null
    endif
endfunction

function BuffExp_CastImmediate takes player owner, real x, real y, integer abilId, string orderStr returns nothing
    local unit d = CreateUnit(owner, 'u000', x, y, 0.0)
    if d != null then
        call UnitAddAbility(d, abilId)
        call IssueImmediateOrder(d, orderStr)
        call UnitApplyTimedLife(d, 'BTLF', 1.5)
        set d = null
    endif
endfunction

function BuffExp_GrantAuraBook takes unit tgt, real dur returns nothing
    local integer i = 0
    local boolean found = false
    if tgt == null or IsUnitType(tgt, UNIT_TYPE_DEAD) or GetWidgetLife(tgt) <= 0.405 then
        return
    endif
    call SetPlayerAbilityAvailable(GetOwningPlayer(tgt), 'A062', false)
    if GetUnitAbilityLevel(tgt, 'A062') == 0 then
        call UnitAddAbility(tgt, 'A062')
        call UnitMakeAbilityPermanent(tgt, true, 'A062')
    endif
    set i = 0
    loop
        exitwhen i >= udg_BExp_AuraCount or found
        if udg_BExp_AuraUnit[i] == tgt then
            set udg_BExp_AuraTimer[i] = dur
            set found = true
        endif
        set i = i + 1
    endloop
    if not found and udg_BExp_AuraCount < 64 then
        set udg_BExp_AuraUnit[udg_BExp_AuraCount] = tgt
        set udg_BExp_AuraTimer[udg_BExp_AuraCount] = dur
        set udg_BExp_AuraCount = udg_BExp_AuraCount + 1
    endif
endfunction

function BuffExp_AuraTimerLoop takes nothing returns nothing
    local integer i = 0
    local unit u = null
    loop
        exitwhen i >= udg_BExp_AuraCount
        set u = udg_BExp_AuraUnit[i]
        set udg_BExp_AuraTimer[i] = udg_BExp_AuraTimer[i] - 1.0
        if u == null or IsUnitType(u, UNIT_TYPE_DEAD) or GetWidgetLife(u) <= 0.405 or udg_BExp_AuraTimer[i] <= 0.0 then
            if u != null and GetUnitAbilityLevel(u, 'A062') > 0 then
                call UnitRemoveAbility(u, 'A062')
            endif
            set udg_BExp_AuraCount = udg_BExp_AuraCount - 1
            set udg_BExp_AuraUnit[i] = udg_BExp_AuraUnit[udg_BExp_AuraCount]
            set udg_BExp_AuraTimer[i] = udg_BExp_AuraTimer[udg_BExp_AuraCount]
            set udg_BExp_AuraUnit[udg_BExp_AuraCount] = null
            set i = i - 1
        endif
        set i = i + 1
    endloop
    set u = null
endfunction

function BuffExp_ApplyAllBuffs takes unit caster, unit tgt returns nothing
    local player owner = null
    local real tx = 0.0
    local real ty = 0.0
    if tgt == null or IsUnitType(tgt, UNIT_TYPE_DEAD) or GetWidgetLife(tgt) <= 0.405 then
        return
    endif
    call BuffExp_GrantAuraBook(tgt, 45.0)
    set owner = GetOwningPlayer(tgt)
    set tx = GetUnitX(tgt)
    set ty = GetUnitY(tgt)

    // 施加 9 大经典主动强化 Buff（严格不含魔免，且隐藏光环不外泄周围）
    call BuffExp_CastTarget(owner, tgt, 'A06C', "bloodlust")
    call BuffExp_CastTarget(owner, tgt, 'A06D', "innerfire")
    call BuffExp_CastTarget(owner, tgt, 'A06E', "unholyfrenzy")
    call BuffExp_CastTarget(owner, tgt, 'A06F', "frostarmor")
    call BuffExp_CastImmediate(owner, tx, ty, 'A070', "roar")
    call BuffExp_CastTarget(owner, tgt, 'A071', "rejuvination")
    call BuffExp_CastTarget(owner, tgt, 'A072', "lightningshield")
    call BuffExp_CastTarget(owner, tgt, 'A073', "spiritlink")
    call BuffExp_CastTarget(owner, tgt, 'A074', "invisibility")

    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\Resurrect\\ResurrectTarget.mdl", tgt, "origin"))
    if caster != null then
        call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 7.0, "|cff00ff80【万象全 Buff 加持！】|r |cffffcc00" + GetUnitName(tgt) + "|r 已获得 9 大满级光环 + 9 大主动强化（持续 45 秒，不含魔免）！")
    endif
    set owner = null
endfunction

function BuffExp_ApplyAllDebuffs takes unit caster, unit tgt returns nothing
    local player dummyOwner = Player(PLAYER_NEUTRAL_AGGRESSIVE)
    local real tx = 0.0
    local real ty = 0.0
    if tgt == null or IsUnitType(tgt, UNIT_TYPE_DEAD) or GetWidgetLife(tgt) <= 0.405 then
        return
    endif
    if caster != null and IsUnitEnemy(tgt, GetOwningPlayer(caster)) then
        set dummyOwner = GetOwningPlayer(caster)
    endif
    set tx = GetUnitX(tgt)
    set ty = GetUnitY(tgt)

    // 先诱捕将空军拉落地面，再叠加其余 Debuff，最后妖术（省略吹风/沉睡/放逐确保可被攻击测试）
    call BuffExp_CastTarget(dummyOwner, tgt, 'A081', "ensnare")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A075', "cripple")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A076', "slow")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A077', "curse")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A078', "faeriefire")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A079', "acidbomb")
    call BuffExp_CastImmediate(dummyOwner, tx, ty, 'A07A', "howlofterror")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A07B', "drunkenhaze")
    call BuffExp_CastPoint(dummyOwner, tx, ty, 'A07C', "silence")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A07D', "soulburn")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A07E', "shadowstrike")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A07F', "entanglingroots")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A080', "frostnova")
    call BuffExp_CastTarget(dummyOwner, tgt, 'A082', "hex")

    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\Cripple\\CrippleTarget.mdl", tgt, "origin"))
    if caster != null then
        call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 7.0, "|cffff3366【万厄全 Debuff 诅咒！】|r |cffffcc00" + GetUnitName(tgt) + "|r 同时遭受 14 重负面减益侵蚀！")
    endif
    set dummyOwner = null
endfunction

function BuffExp_SpawnForPlayer takes player p, real baseX, real baseY returns unit
    local integer baseCliff = GetTerrainCliffLevel(baseX, baseY)
    local real searchR = 260.0
    local integer k = 0
    local real angle = 0.0
    local real px = baseX
    local real py = baseY
    local boolean found = false
    local unit u = null

    loop
        exitwhen searchR > 540.0 or found
        set k = 0
        loop
            exitwhen k >= 16 or found
            set angle = I2R(k) * 0.3927
            set px = baseX + searchR * Cos(angle)
            set py = baseY + searchR * Sin(angle)
            if Refuge_IsSafeTerrainPoint(px, py, baseCliff, false) then
                set found = true
            endif
            set k = k + 1
        endloop
        if not found then
            set searchR = searchR + 70.0
        endif
    endloop
    if not found then
        set px = baseX + 240.0
        set py = baseY - 240.0
    endif

    set u = CreateUnit(p, 'u00B', px, py, 270.0)
    if u != null then
        call SetUnitVertexColor(u, 255, 240, 195, 255)
        call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\MassTeleport\\MassTeleportTarget.mdl", GetUnitX(u), GetUnitY(u)))
    endif
    return u
endfunction

function BuffExp_InitSystem takes nothing returns nothing
    local integer i = 0
    local player p = null
    local real sx = 0.0
    local real sy = 0.0
    local unit u = null

    loop
        exitwhen i >= bj_MAX_PLAYER_SLOTS
        call SetPlayerAbilityAvailable(Player(i), 'A062', false)
        set i = i + 1
    endloop

    set i = 0
    loop
        exitwhen i > 7
        set p = Player(i)
        if GetPlayerSlotState(p) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(p) == MAP_CONTROL_USER then
            set sx = GetStartLocationX(GetPlayerStartLocation(p))
            set sy = GetStartLocationY(GetPlayerStartLocation(p))
            set u = BuffExp_SpawnForPlayer(p, sx, sy)
            if u != null then
                if GetLocalPlayer() == p then
                    call PingMinimapEx(GetUnitX(u), GetUnitY(u), 5.0, 0, 220, 255, false)
                endif
                call DisplayTimedTextToPlayer(p, 0, 0, 11.0, "|cff00ffcc【实验单位已就位】|r 基地旁已生成【实验小兵 · 万象状态师】：[Q] 万象全Buff(9光环+9Buff，不含魔免) / [W] 万厄全Debuff(14重负面)！输入 |-buffunit|r 可随时再召唤一只测试。")
                set u = null
            endif
        endif
        set i = i + 1
    endloop

    call TimerStart(CreateTimer(), 1.0, true, function BuffExp_AuraTimerLoop)
    set p = null
endfunction

function BuffExp_OnStartTimer takes nothing returns nothing
    local timer t = GetExpiredTimer()
    call PauseTimer(t)
    call DestroyTimer(t)
    set t = null
    call BuffExp_InitSystem()
endfunction

function DM_OnSpellEffect takes nothing returns boolean'''

    text = replace_once(
        text,
        r'''function DM_OnSpellEffect takes nothing returns boolean''',
        bexp_funcs,
        '2_bexp_functions'
    )

    # 3. Hook A060 / A061 in DM_OnSpellEffect
    text = replace_once(
        text,
        r'''    if abil >= 'A050' and abil <= 'A05A' then
        if GetUnitTypeId(caster) == 'n005' then
            call Asn_OnCastAbility(caster, abil)
        endif
        set caster = null
        return false
    endif''',
        r'''    if abil >= 'A050' and abil <= 'A05A' then
        if GetUnitTypeId(caster) == 'n005' then
            call Asn_OnCastAbility(caster, abil)
        endif
        set caster = null
        return false
    endif

    if abil == 'A060' then
        call BuffExp_ApplyAllBuffs(caster, GetSpellTargetUnit())
        set caster = null
        return false
    elseif abil == 'A061' then
        call BuffExp_ApplyAllDebuffs(caster, GetSpellTargetUnit())
        set caster = null
        return false
    endif''',
        '3_dm_on_spell_effect_hook'
    )

    # 4. Add -buffunit chat command right after -stopkill in TM_OnChatCommand
    text = replace_once(
        text,
        r'''        else
            call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cffaaaaaa[自测提示]|r 当前没有针对你自己的活跃暗杀测试。")
        endif
    elseif s == "-archimonde" then''',
        r'''        else
            call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cffaaaaaa[自测提示]|r 当前没有针对你自己的活跃暗杀测试。")
        endif
    elseif s == "-buffunit" then
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
        set u = BuffExp_SpawnForPlayer(p, startX, startY)
        if u != null then
            if GetLocalPlayer() == p then
                call SelectUnit(u, true)
                call PingMinimapEx(GetUnitX(u), GetUnitY(u), 4.0, 0, 255, 180, false)
            endif
            call DisplayTimedTextToPlayer(p, 0, 0, 7.0, "|cff00ffcc【实验单位已召唤】|r 已为你部署一只新的【实验小兵 · 万象状态师】：[Q] 万象全Buff（不含魔免） / [W] 万厄全Debuff！")
            set u = null
        endif
    elseif s == "-archimonde" then''',
        '4_chat_buffunit'
    )

    # 5. Start BuffExp_OnStartTimer in DM_InitTriggers
    text = replace_once(
        text,
        r'''    call TimerStart(CreateTimer(), 1.65, false, function Asn_OnStartTimer)''',
        r'''    call TimerStart(CreateTimer(), 1.65, false, function Asn_OnStartTimer)
    call TimerStart(CreateTimer(), 1.80, false, function BuffExp_OnStartTimer)''',
        '5_init_timer'
    )

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open(TARGET_PATH, 'wb') as f:
        f.write(out_bytes)
    print("Successfully applied v6.7 BuffExp patches to payload/war3map.j!")


if __name__ == '__main__':
    main()
