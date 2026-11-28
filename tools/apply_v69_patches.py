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

    # 1. Extend custom hero pId bounds 7 -> 15 so Mirror slots 13, 14, 15 run full hero mechanics
    text = replace_once(
        text,
        r'''function Asn_GetMahoAvgAdapt takes integer pId returns real
    local integer i = 0
    local real total = 0.0
    if pId < 0 or pId > 7 then''',
        r'''function Asn_GetMahoAvgAdapt takes integer pId returns real
    local integer i = 0
    local real total = 0.0
    if pId < 0 or pId > 15 then''',
        '1a_Asn_GetMahoAvgAdapt_pId15'
    )

    text = replace_once(
        text,
        r'''    if pId < 0 or pId > 7 or cat < 0 or cat > 6 or rawAdd <= 0.0 then
        return
    endif''',
        r'''    if pId < 0 or pId > 15 or cat < 0 or cat > 6 or rawAdd <= 0.0 then
        return
    endif''',
        '1b_Maho_AddDefAdapt_pId15'
    )

    text = replace_once(
        text,
        r'''    set pId = 0
    loop
        exitwhen pId > 7
        set udg_Maho_LastSkillTime[pId] = RMaxBJ(0.0, udg_Maho_LastSkillTime[pId] - 1.0)''',
        r'''    set pId = 0
    loop
        exitwhen pId > 15
        set udg_Maho_LastSkillTime[pId] = RMaxBJ(0.0, udg_Maho_LastSkillTime[pId] - 1.0)''',
        '1c_Maho_TimerLoop_pId15'
    )

    text = replace_once(
        text,
        r'''    set pId = 0
    loop
        exitwhen pId > 7
        // Deferred Egg Enter (100% outside of DealDamage callback stack!)''',
        r'''    set pId = 0
    loop
        exitwhen pId > 15
        // Deferred Egg Enter (100% outside of DealDamage callback stack!)''',
        '1d_Maho_StealthLoop_pId15'
    )

    text = replace_once(
        text,
        r'''    if tgt != null then
        // Single-target spell: ONLY adapt if target IS Mahoraga!
        set pId = 0
        loop
            exitwhen pId > 7
            set maho = udg_Maho_Hero[pId]
            if maho != null and Maho_IsUnitAlive(maho) and not udg_Maho_InEgg[pId] and tgt == maho and IsUnitEnemy(caster, GetOwningPlayer(maho)) then
                set udg_Maho_LastSkillId[pId] = abil
                set udg_Maho_LastSkillTime[pId] = 2.5
                call Maho_AddSkillAdapt(pId, abil, 0.03)
                call Maho_UpdateUI(pId)
            endif
            set pId = pId + 1
        endloop
    else
        // Ground target or point-blank AOE spell
        set tx = GetSpellTargetX()
        set ty = GetSpellTargetY()
        if tx == 0.0 and ty == 0.0 then
            set tx = GetUnitX(caster)
            set ty = GetUnitY(caster)
        endif

        set pId = 0
        loop
            exitwhen pId > 7
            set maho = udg_Maho_Hero[pId]''',
        r'''    if tgt != null then
        // Single-target spell: ONLY adapt if target IS Mahoraga!
        set pId = 0
        loop
            exitwhen pId > 15
            set maho = udg_Maho_Hero[pId]
            if maho != null and Maho_IsUnitAlive(maho) and not udg_Maho_InEgg[pId] and tgt == maho and IsUnitEnemy(caster, GetOwningPlayer(maho)) then
                set udg_Maho_LastSkillId[pId] = abil
                set udg_Maho_LastSkillTime[pId] = 2.5
                call Maho_AddSkillAdapt(pId, abil, 0.03)
                call Maho_UpdateUI(pId)
            endif
            set pId = pId + 1
        endloop
    else
        // Ground target or point-blank AOE spell
        set tx = GetSpellTargetX()
        set ty = GetSpellTargetY()
        if tx == 0.0 and ty == 0.0 then
            set tx = GetUnitX(caster)
            set ty = GetUnitY(caster)
        endif

        set pId = 0
        loop
            exitwhen pId > 15
            set maho = udg_Maho_Hero[pId]''',
        '1e_Maho_OnAnySpellEffect_pId15'
    )

    text = replace_once(
        text,
        r'''    set p = 0
    loop
        exitwhen p > 7
        if udg_Ninja_CloneGroup[p] != null and IsUnitInGroup(u, udg_Ninja_CloneGroup[p]) then''',
        r'''    set p = 0
    loop
        exitwhen p > 15
        if udg_Ninja_CloneGroup[p] != null and IsUnitInGroup(u, udg_Ninja_CloneGroup[p]) then''',
        '1f_Ninja_IsAnyClone_pId15'
    )

    text = replace_once(
        text,
        r'''        if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
            if pick == null then
                set pick = u
            endif
            call GroupAddUnit(tempG, u)
        endif''',
        r'''        if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
            if pick == null then
                if not udg_SM_Active or (pId != 13 and (udg_SM_Victim == null or GetOwningPlayer(udg_SM_Victim) != Player(pId))) or (GetUnitX(u) >= -820.0 and GetUnitX(u) <= 820.0 and GetUnitY(u) >= 7220.0 and GetUnitY(u) <= 8120.0) then
                    set pick = u
                endif
            endif
            call GroupAddUnit(tempG, u)
        endif''',
        '1g_Ninja_PickLivingClone_arena_isolation'
    )

    text = replace_once(
        text,
        r'''    // 0. Process Strain Mirror Image Sync Timer
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_MirrorSyncTimer[pId] > 0.0 then''',
        r'''    // 0. Process Strain Mirror Image Sync Timer
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Strain_MirrorSyncTimer[pId] > 0.0 then''',
        '1h_DM_StealthLoop_StrainSync_pId15'
    )

    text = replace_once(
        text,
        r'''    // 5. Hero #3 Burrow Movement & Dust Loop
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_Burrowed[pId] then''',
        r'''    // 5. Hero #3 Burrow Movement & Dust Loop
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Strain_Burrowed[pId] then''',
        '1i_DM_StealthLoop_Burrow_pId15'
    )

    text = replace_once(
        text,
        r'''    // 6. Hero #3 Mimicry Actor Position Sync & True Sight Check Loop
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_MimicActive[pId] then''',
        r'''    // 6. Hero #3 Mimicry Actor Position Sync & True Sight Check Loop
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Strain_MimicActive[pId] then''',
        '1j_DM_StealthLoop_Mimic_pId15'
    )

    text = replace_once(
        text,
        r'''    // 2. Process Ninja Aura (A012) - 900.0 Radius around body and all living clones, deduplicated per cycle
    set pId = 0
    loop
        exitwhen pId > 7
        set th = udg_Ninja_TrueHero[pId]''',
        r'''    // 2. Process Ninja Aura (A012) - 900.0 Radius around body and all living clones, deduplicated per cycle
    set pId = 0
    loop
        exitwhen pId > 15
        set th = udg_Ninja_TrueHero[pId]''',
        '1k_DM_CapTimerLoop_NinjaAura_pId15'
    )

    text = replace_once(
        text,
        r'''    // 3.4. Hero #3 Stage >= 2 Regenerative Carapace (2.5% Max HP / sec)
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_EvoStage[pId] >= 2 then''',
        r'''    // 3.4. Hero #3 Stage >= 2 Regenerative Carapace (2.5% Max HP / sec)
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Strain_EvoStage[pId] >= 2 then''',
        '1l_DM_CapTimerLoop_StrainRegen_pId15'
    )

    text = replace_once(
        text,
        r'''    // 3.5. Process Hero #3 Digestion Timer Countdown
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_DigestTimer[pId] > 0.0 then''',
        r'''    // 3.5. Process Hero #3 Digestion Timer Countdown
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Strain_DigestTimer[pId] > 0.0 then''',
        '1m_DM_CapTimerLoop_StrainDigest_pId15'
    )

    text = replace_once(
        text,
        r'''    // 3.7. Stage 3 Strain W Ability Cooldown Clamp (Hard lock to 4.0s)
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_EvoStage[pId] >= 3 then''',
        r'''    // 3.7. Stage 3 Strain W Ability Cooldown Clamp (Hard lock to 4.0s)
    set pId = 0
    loop
        exitwhen pId > 15
        if udg_Strain_EvoStage[pId] >= 3 then''',
        '1n_DM_CapTimerLoop_StrainCD_pId15'
    )

    text = replace_once(
        text,
        r'''    // 3.8. Hero #3 Skin Verification & Illusion Synchronization
    set pId = 0
    loop
        exitwhen pId > 7
        set u = Strain_GetRealHero(pId)''',
        r'''    // 3.8. Hero #3 Skin Verification & Illusion Synchronization
    set pId = 0
    loop
        exitwhen pId > 15
        set u = Strain_GetRealHero(pId)''',
        '1o_DM_CapTimerLoop_StrainSkin_pId15'
    )

    text = replace_once(
        text,
        r'''    // Golden Egg [u004] destroyed by 4-Stage Mahoraga
    if deadType == 'u004' then
        set i = 0
        loop
            exitwhen i > 7''',
        r'''    // Golden Egg [u004] destroyed by 4-Stage Mahoraga
    if deadType == 'u004' then
        set i = 0
        loop
            exitwhen i > 15''',
        '1p_DM_OnUnitDeath_Egg_pId15'
    )

    # 2. Globals for Seal Mountain
    text = replace_once(
        text,
        r'''    integer udg_BExp_AuraCount = 0''',
        r'''    integer udg_BExp_AuraCount = 0

    // Seal Mountain [E: A083 / R: A084] System Globals (v6.9)
    boolean udg_SM_Active = false
    unit udg_SM_Caster = null
    player udg_SM_CasterOwner = null
    unit udg_SM_Victim = null
    player udg_SM_VictimOwner = null
    unit udg_SM_Mirror = null
    real udg_SM_ReturnX = 0.0
    real udg_SM_ReturnY = 0.0
    real udg_SM_DeadCheckTimer = 0.0
    rect udg_SM_ArenaRect = null
    fogmodifier array udg_SM_FogMod
    group udg_SM_ConqueredGroup = null
    integer udg_SM_NextAllySlot = 14
    real udg_SM_MirrorCD_Q = 0.0
    real udg_SM_MirrorCD_W = 0.0
    real udg_SM_MirrorCD_E = 0.0
    real udg_SM_MirrorCD_R = 0.0
    real udg_SM_MirrorMorphCD = 0.0
    integer array udg_SM_HeroAbilId
    string array udg_SM_HeroAbilOrd
    integer array udg_SM_HeroAbilMode
    integer udg_SM_HeroAbilCount = 0''',
        '2_SM_Globals'
    )

    # 3. Skip Player(13..15) / Seal Mountain arena occupants on Assassination Bounty Board
    text = replace_once(
        text,
        r'''        if not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) and ut != 'u000' and ut != 'u001' and ut != 'u002' and ut != 'u003' and ut != 'n003' and ut != 'n005' and not Asn_IsAssassinType(ut) then''',
        r'''        if not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) and ut != 'u000' and ut != 'u001' and ut != 'u002' and ut != 'u003' and ut != 'u00B' and ut != 'n003' and ut != 'n005' and not Asn_IsAssassinType(ut) and GetPlayerId(GetOwningPlayer(u)) != 13 and not (GetUnitX(u) >= -820.0 and GetUnitX(u) <= 820.0 and GetUnitY(u) >= 7220.0) then''',
        '3_Asn_RefreshBoard_filter_SM'
    )

    # 4. Update BuffExp_InitSystem welcome message
    text = replace_once(
        text,
        r'''call DisplayTimedTextToPlayer(p, 0, 0, 11.0, "|cff00ffcc【实验单位已就位】|r 基地旁已生成【实验小兵 · 万象状态师】：[Q] 万象全Buff(9光环+9Buff，不含魔免) / [W] 万厄全Debuff(14重负面)！输入 |-buffunit|r 可随时再召唤一只测试。")''',
        r'''call DisplayTimedTextToPlayer(p, 0, 0, 12.0, "|cff00ffcc【实验单位已就位】|r 基地旁已生成【实验小兵 · 万象状态师】：[Q] 全Buff(不含魔免) / [W] 全Debuff / [E] |cffcc66ff封印术·山(无视魔免)|r / [R] 解封·破山！输入 |-buffunit|r 可再召唤，|-mount|r 观战封印之山。")''',
        '4_BuffExp_banner'
    )

    # 5. Insert full Seal Mountain system right before DM_OnSpellEffect
    sm_funcs = r'''//***************************************************************************
//*
//*  Seal Mountain Arena & Full-AI Mirror System [E: A083 / R: A084] (v6.9)
//*
//***************************************************************************

function SM_IsUnitInArena takes unit u returns boolean
    local real x = 0.0
    local real y = 0.0
    if u == null then
        return false
    endif
    set x = GetUnitX(u)
    set y = GetUnitY(u)
    return x >= -820.0 and x <= 820.0 and y >= 7220.0 and y <= 8120.0
endfunction

function SM_RegisterHeroAbil takes integer abilId, string ord, integer mode returns nothing
    if udg_SM_HeroAbilCount < 160 then
        set udg_SM_HeroAbilId[udg_SM_HeroAbilCount] = abilId
        set udg_SM_HeroAbilOrd[udg_SM_HeroAbilCount] = ord
        set udg_SM_HeroAbilMode[udg_SM_HeroAbilCount] = mode
        set udg_SM_HeroAbilCount = udg_SM_HeroAbilCount + 1
    endif
endfunction

function SM_InitHeroAbilPool takes nothing returns nothing
    if udg_SM_HeroAbilCount > 0 then
        return
    endif
    // Human Heroes (Modes: 0=Passive, 1=Immediate, 2=TargetEnemy, 3=TargetSelf, 4=PointEnemy, 5=LowHPImmediate)
    call SM_RegisterHeroAbil('AHtb', "thunderbolt", 2)
    call SM_RegisterHeroAbil('AHtc', "thunderclap", 1)
    call SM_RegisterHeroAbil('AHbh', "", 0)
    call SM_RegisterHeroAbil('AHav', "avatar", 5)
    call SM_RegisterHeroAbil('AHhb', "holybolt", 3)
    call SM_RegisterHeroAbil('AHds', "divineshield", 5)
    call SM_RegisterHeroAbil('AHad', "", 0)
    call SM_RegisterHeroAbil('AHre', "resurrection", 1)
    call SM_RegisterHeroAbil('AHbz', "blizzard", 4)
    call SM_RegisterHeroAbil('AHwe', "waterelemental", 1)
    call SM_RegisterHeroAbil('AHab', "", 0)
    call SM_RegisterHeroAbil('AHfs', "flamestrike", 4)
    call SM_RegisterHeroAbil('AHbn', "banish", 2)
    call SM_RegisterHeroAbil('AHdr', "", 0)
    call SM_RegisterHeroAbil('AHpx', "summonphoenix", 1)

    // Orc Heroes
    call SM_RegisterHeroAbil('AOwk', "windwalk", 1)
    call SM_RegisterHeroAbil('AOmi', "mirrorimage", 1)
    call SM_RegisterHeroAbil('AOcr', "", 0)
    call SM_RegisterHeroAbil('AOww', "whirlwind", 1)
    call SM_RegisterHeroAbil('AOcl', "chainlightning", 2)
    call SM_RegisterHeroAbil('AOsf', "spiritwolf", 1)
    call SM_RegisterHeroAbil('AOeq', "earthquake", 4)
    call SM_RegisterHeroAbil('AOsh', "shockwave", 4)
    call SM_RegisterHeroAbil('AOws', "stomp", 1)
    call SM_RegisterHeroAbil('AOae', "", 0)
    call SM_RegisterHeroAbil('AOre', "", 0)
    call SM_RegisterHeroAbil('AOhw', "healingwave", 3)
    call SM_RegisterHeroAbil('AOhx', "hex", 2)
    call SM_RegisterHeroAbil('AOsw', "ward", 4)

    // Night Elf Heroes
    call SM_RegisterHeroAbil('AEmb', "manaburn", 2)
    call SM_RegisterHeroAbil('AEim', "immolation", 1)
    call SM_RegisterHeroAbil('AEev', "", 0)
    call SM_RegisterHeroAbil('AEme', "metamorphosis", 1)
    call SM_RegisterHeroAbil('AEer', "entanglingroots", 2)
    call SM_RegisterHeroAbil('AEfn', "forceofnature", 4)
    call SM_RegisterHeroAbil('AEah', "", 0)
    call SM_RegisterHeroAbil('AEtq', "tranquility", 5)
    call SM_RegisterHeroAbil('AHfa', "", 0)
    call SM_RegisterHeroAbil('AEar', "", 0)
    call SM_RegisterHeroAbil('AEsf', "starfall", 1)
    call SM_RegisterHeroAbil('AEfk', "fanofknives", 1)
    call SM_RegisterHeroAbil('AEbl', "", 0)
    call SM_RegisterHeroAbil('AEsh', "shadowstrike", 2)
    call SM_RegisterHeroAbil('AEsv', "spiritofvengeance", 1)

    // Undead Heroes
    call SM_RegisterHeroAbil('AUdc', "deathcoil", 2)
    call SM_RegisterHeroAbil('AUdp', "deathpact", 0)
    call SM_RegisterHeroAbil('AUau', "", 0)
    call SM_RegisterHeroAbil('AUan', "", 0)
    call SM_RegisterHeroAbil('AUcs', "carrionswarm", 4)
    call SM_RegisterHeroAbil('AUsl', "sleep", 2)
    call SM_RegisterHeroAbil('AUav', "", 0)
    call SM_RegisterHeroAbil('AUin', "inferno", 4)
    call SM_RegisterHeroAbil('AUfn', "frostnova", 2)
    call SM_RegisterHeroAbil('AUfa', "frostarmor", 3)
    call SM_RegisterHeroAbil('AUdr', "", 0)
    call SM_RegisterHeroAbil('AUdd', "deathanddecay", 4)
    call SM_RegisterHeroAbil('AUim', "impale", 4)
    call SM_RegisterHeroAbil('AUts', "", 0)
    call SM_RegisterHeroAbil('AUls', "Locustswarm", 1)

    // Neutral Heroes & Demon Bosses (incl. Archimonde)
    call SM_RegisterHeroAbil('ANfl', "forkedlightning", 2)
    call SM_RegisterHeroAbil('ANfa', "", 0)
    call SM_RegisterHeroAbil('ANms', "manashieldon", 5)
    call SM_RegisterHeroAbil('ANto', "tornado", 4)
    call SM_RegisterHeroAbil('ANsi', "silence", 4)
    call SM_RegisterHeroAbil('ANba', "", 0)
    call SM_RegisterHeroAbil('ANdr', "", 0)
    call SM_RegisterHeroAbil('ANbf', "breathoffire", 4)
    call SM_RegisterHeroAbil('ANdh', "drunkenhaze", 2)
    call SM_RegisterHeroAbil('ANdb', "", 0)
    call SM_RegisterHeroAbil('ANef', "elementalfury", 1)
    call SM_RegisterHeroAbil('ANsg', "summongrizzly", 1)
    call SM_RegisterHeroAbil('ANsq', "summonquillbeast", 1)
    call SM_RegisterHeroAbil('ANsw', "summonwareagle", 1)
    call SM_RegisterHeroAbil('ANst', "stampede", 4)
    call SM_RegisterHeroAbil('ANhs', "healingspray", 4)
    call SM_RegisterHeroAbil('ANcr', "chemicalrage", 1)
    call SM_RegisterHeroAbil('ANab', "acidbomb", 2)
    call SM_RegisterHeroAbil('ANsy', "summonfactory", 4)
    call SM_RegisterHeroAbil('ANcs', "clusterrockets", 4)
    call SM_RegisterHeroAbil('ANeg', "", 0)
    call SM_RegisterHeroAbil('ANrg', "robogoblin", 1)
    call SM_RegisterHeroAbil('ANso', "soulburn", 2)
    call SM_RegisterHeroAbil('ANlm', "slimemonster", 2)
    call SM_RegisterHeroAbil('ANia', "", 0)
    call SM_RegisterHeroAbil('ANvc', "volcano", 4)
    call SM_RegisterHeroAbil('ANrf', "rainoffire", 4)
    call SM_RegisterHeroAbil('ANht', "howlofterror", 1)
    call SM_RegisterHeroAbil('ANfd', "fingerofdeath", 2)
    call SM_RegisterHeroAbil('ANdp', "darkportal", 4)
    call SM_RegisterHeroAbil('ANrc', "rainofchaos", 4)

    // Creep & Neutral Spells (also evaluated by AI on non-hero/Boss mirrors)
    call SM_RegisterHeroAbil('ACbl', "bloodlust", 3)
    call SM_RegisterHeroAbil('ACif', "innerfire", 3)
    call SM_RegisterHeroAbil('ACro', "roar", 1)
    call SM_RegisterHeroAbil('ACsw', "slow", 2)
    call SM_RegisterHeroAbil('ACcr', "cripple", 2)
    call SM_RegisterHeroAbil('ACcs', "curse", 2)
    call SM_RegisterHeroAbil('ACen', "ensnare", 2)
    call SM_RegisterHeroAbil('ACtb', "thunderbolt", 2)
    call SM_RegisterHeroAbil('AChx', "hex", 2)
    call SM_RegisterHeroAbil('ACst', "stomp", 1)
    call SM_RegisterHeroAbil('ACtc', "thunderclap", 1)
    call SM_RegisterHeroAbil('ACsh', "shockwave", 4)
    call SM_RegisterHeroAbil('ACfl', "forkedlightning", 2)
    call SM_RegisterHeroAbil('ACfn', "frostnova", 2)
    call SM_RegisterHeroAbil('ACrj', "rejuvination", 3)
    call SM_RegisterHeroAbil('ACpu', "purge", 2)
    call SM_RegisterHeroAbil('ACls', "lightningshield", 3)
    call SM_RegisterHeroAbil('ACfa', "frostarmor", 3)
endfunction

function SM_ResetCustomHeroSlot takes integer pId returns nothing
    local integer k = 0
    if pId < 0 or pId > 15 then
        return
    endif

    // Mahoraga reset
    set udg_Maho_Hero[pId] = null
    if udg_Maho_WheelFx[pId] != null then
        call DestroyEffect(udg_Maho_WheelFx[pId])
        set udg_Maho_WheelFx[pId] = null
    endif
    if udg_Maho_WatchFx[pId] != null then
        call DestroyEffect(udg_Maho_WatchFx[pId])
        set udg_Maho_WatchFx[pId] = null
    endif
    set udg_Maho_WatchTarget[pId] = null
    if udg_Maho_EggUnit[pId] != null then
        call RemoveUnit(udg_Maho_EggUnit[pId])
        set udg_Maho_EggUnit[pId] = null
    endif
    set udg_Maho_InEgg[pId] = false
    set udg_Maho_PendingEggEnter[pId] = false
    set udg_Maho_EggTimer[pId] = 0.0
    set udg_Maho_EggCD[pId] = 0.0
    set udg_Maho_MoveSpeed[pId] = 190.0
    set udg_Maho_AntiAirUnlocked[pId] = false
    set udg_Maho_HasNeverMiss[pId] = false
    set udg_Maho_FlyProgress[pId] = 0
    set udg_Maho_IsWinged[pId] = false
    set udg_Maho_AirHits[pId] = 0
    set udg_Maho_AtkHits[pId] = 0
    set udg_Maho_WheelSpins[pId] = 0
    set udg_Maho_AntiMahoAdapt[pId] = 0.0
    set udg_Maho_SkillCount[pId] = 0
    set udg_Maho_LastSkillId[pId] = 0
    set udg_Maho_LastSkillTime[pId] = 0.0
    set udg_Maho_CCTimer[pId] = 0.0
    set udg_Maho_WheelSpinTimer[pId] = 0.0
    set udg_Maho_ReskinTimer[pId] = 0.0
    set k = 0
    loop
        exitwhen k > 7
        set udg_Maho_DefAdapt[pId * 8 + k] = 0.0
        set udg_Maho_AtkAdapt[pId * 8 + k] = 0.0
        set k = k + 1
    endloop
    set k = 0
    loop
        exitwhen k >= 12
        set udg_Maho_SkillId[pId * 12 + k] = 0
        set udg_Maho_SkillPct[pId * 12 + k] = 0.0
        set k = k + 1
    endloop

    // Wild Avatar reset
    set udg_Wild_Hero[pId] = null
    set udg_Wild_IsMorphed[pId] = false
    set udg_Wild_CurrentForm[pId] = 0
    set udg_Wild_CurrentFormType[pId] = 0
    set udg_Wild_CurrentFormLevel[pId] = 0
    set udg_Wild_CurrentSubIdx[pId] = 1
    set udg_Wild_CurrentAbil[pId] = 0
    set udg_Wild_SoulStacks[pId] = 0
    set udg_Wild_HeroSoulHP[pId] = 0
    set udg_Wild_HeroSoulDmg[pId] = 0
    set udg_Wild_ArmyBonusHP[pId] = 0
    set udg_Wild_ArmyBonusDmg[pId] = 0
    set udg_Wild_StoredManaRatio[pId] = 1.0
    set udg_Wild_MorphCD[pId] = 0.0
    set udg_Wild_WrathTimer[pId] = 0.0
    set udg_Wild_HeroThrallCount[pId] = 0
    set udg_Wild_CreepThrallCount[pId] = 0

    // Strain reset
    set udg_Strain_Hero[pId] = null
    set udg_Strain_Burrowed[pId] = false
    set udg_Strain_BurrowTimer[pId] = 0.0
    if udg_Strain_MimicActor[pId] != null then
        call RemoveUnit(udg_Strain_MimicActor[pId])
        set udg_Strain_MimicActor[pId] = null
    endif
    set udg_Strain_MimicActive[pId] = false
    set udg_Strain_AmbushReady[pId] = false
    set udg_Strain_DigestTimer[pId] = 0.0
    if udg_Strain_DigestFx[pId] != null then
        call DestroyEffect(udg_Strain_DigestFx[pId])
        set udg_Strain_DigestFx[pId] = null
    endif
    if udg_Strain_Stage3Fx[pId] != null then
        call DestroyEffect(udg_Strain_Stage3Fx[pId])
        set udg_Strain_Stage3Fx[pId] = null
    endif
    set udg_Strain_EvoStage[pId] = 0
    set udg_Strain_DevourCount[pId] = 0
    set udg_Strain_TotalBonusHP[pId] = 0
    set udg_Strain_TotalBonusAtk[pId] = 0
    set udg_Strain_TotalBonusMana[pId] = 0
    set udg_Strain_TotalBonusArmor[pId] = 0.0
    set udg_Strain_StolenHeroAbil[pId] = 0
    set udg_Strain_StolenAbil1[pId] = 0
    set udg_Strain_StolenAbil2[pId] = 0
    set udg_Strain_EvoTier1[pId] = 0
    set udg_Strain_EvoTier2[pId] = 0

    // Ninja reset
    set udg_Ninja_TrueHero[pId] = null
    set udg_Ninja_AuraOn[pId] = false
    if udg_Ninja_AuraFx[pId] != null then
        call DestroyEffect(udg_Ninja_AuraFx[pId])
        set udg_Ninja_AuraFx[pId] = null
    endif
    if udg_Ninja_CloneGroup[pId] != null then
        call GroupClear(udg_Ninja_CloneGroup[pId])
    else
        set udg_Ninja_CloneGroup[pId] = CreateGroup()
    endif
endfunction

function SM_CopyAbilLv takes unit src, unit dst, integer abilId returns nothing
    local integer lv = 0
    if src == null or dst == null or abilId == 0 then
        return
    endif
    set lv = GetUnitAbilityLevel(src, abilId)
    if lv > 0 then
        if GetUnitAbilityLevel(dst, abilId) == 0 then
            call UnitAddAbility(dst, abilId)
        endif
        call SetUnitAbilityLevel(dst, abilId, lv)
    endif
endfunction

function SM_CopyCustomHeroState takes integer fromPid, integer toPid, unit src, unit dst returns nothing
    local integer ut = 0
    local integer k = 0
    local integer srcIdx = 0
    local integer dstIdx = 0
    if dst == null or fromPid < 0 or fromPid > 15 or toPid < 0 or toPid > 15 then
        return
    endif
    set ut = GetUnitTypeId(dst)

    if ut == 'H006' then
        set udg_Maho_Hero[toPid] = dst
        set udg_Maho_MoveSpeed[toPid] = udg_Maho_MoveSpeed[fromPid]
        if udg_Maho_MoveSpeed[toPid] < 190.0 then
            set udg_Maho_MoveSpeed[toPid] = 190.0
        endif
        set udg_Maho_FlyProgress[toPid] = udg_Maho_FlyProgress[fromPid]
        set udg_Maho_IsWinged[toPid] = udg_Maho_IsWinged[fromPid]
        set udg_Maho_AntiAirUnlocked[toPid] = udg_Maho_AntiAirUnlocked[fromPid]
        set udg_Maho_HasNeverMiss[toPid] = udg_Maho_HasNeverMiss[fromPid]
        set udg_Maho_AntiMahoAdapt[toPid] = udg_Maho_AntiMahoAdapt[fromPid]
        set udg_Maho_EggCD[toPid] = udg_Maho_EggCD[fromPid]
        set udg_Maho_AtkHits[toPid] = udg_Maho_AtkHits[fromPid]
        set udg_Maho_WheelSpins[toPid] = udg_Maho_WheelSpins[fromPid]
        set udg_Maho_SkillCount[toPid] = udg_Maho_SkillCount[fromPid]
        set udg_Maho_InEgg[toPid] = false
        set udg_Maho_PendingEggEnter[toPid] = false
        set udg_Maho_EggTimer[toPid] = 0.0

        set k = 0
        loop
            exitwhen k > 7
            set udg_Maho_DefAdapt[toPid * 8 + k] = udg_Maho_DefAdapt[fromPid * 8 + k]
            set udg_Maho_AtkAdapt[toPid * 8 + k] = udg_Maho_AtkAdapt[fromPid * 8 + k]
            set k = k + 1
        endloop
        set k = 0
        loop
            exitwhen k >= 12
            set udg_Maho_SkillId[toPid * 12 + k] = udg_Maho_SkillId[fromPid * 12 + k]
            set udg_Maho_SkillPct[toPid * 12 + k] = udg_Maho_SkillPct[fromPid * 12 + k]
            set k = k + 1
        endloop

        if src != null and src != dst then
            call SM_CopyAbilLv(src, dst, 'A041')
            call SM_CopyAbilLv(src, dst, 'A042')
            call SM_CopyAbilLv(src, dst, 'A043')
            call SM_CopyAbilLv(src, dst, 'A044')
            call SM_CopyAbilLv(src, dst, 'A045')
            call SM_CopyAbilLv(src, dst, 'A046')
        endif
        call Maho_ApplyAppearance(dst, toPid)
        call Maho_ApplyWheelVisual(toPid)
        call Maho_UpdateUI(toPid)

    elseif ut == 'H005' then
        set udg_Wild_Hero[toPid] = dst
        set udg_Wild_SoulStacks[toPid] = udg_Wild_SoulStacks[fromPid]
        set udg_Wild_HeroSoulHP[toPid] = udg_Wild_HeroSoulHP[fromPid]
        set udg_Wild_HeroSoulDmg[toPid] = udg_Wild_HeroSoulDmg[fromPid]
        set udg_Wild_ArmyBonusHP[toPid] = udg_Wild_ArmyBonusHP[fromPid]
        set udg_Wild_ArmyBonusDmg[toPid] = udg_Wild_ArmyBonusDmg[fromPid]
        set udg_Wild_StoredManaRatio[toPid] = udg_Wild_StoredManaRatio[fromPid]
        set udg_Wild_HeroThrallCount[toPid] = udg_Wild_HeroThrallCount[fromPid]
        set udg_Wild_CreepThrallCount[toPid] = udg_Wild_CreepThrallCount[fromPid]

        set k = 0
        loop
            exitwhen k > 7
            set srcIdx = fromPid * 8 + k
            set dstIdx = toPid * 8 + k
            set udg_Wild_ThrallSkin[dstIdx] = udg_Wild_ThrallSkin[srcIdx]
            set udg_Wild_ThrallName[dstIdx] = udg_Wild_ThrallName[srcIdx]
            set udg_Wild_ThrallLevel[dstIdx] = udg_Wild_ThrallLevel[srcIdx]
            set udg_Wild_ThrallHP[dstIdx] = udg_Wild_ThrallHP[srcIdx]
            set udg_Wild_ThrallMana[dstIdx] = udg_Wild_ThrallMana[srcIdx]
            set udg_Wild_ThrallDmg[dstIdx] = udg_Wild_ThrallDmg[srcIdx]
            set udg_Wild_ThrallArmor[dstIdx] = udg_Wild_ThrallArmor[srcIdx]
            set udg_Wild_ThrallAbil1[dstIdx] = udg_Wild_ThrallAbil1[srcIdx]
            set udg_Wild_ThrallAbil2[dstIdx] = udg_Wild_ThrallAbil2[srcIdx]
            set udg_Wild_ThrallAbil3[dstIdx] = udg_Wild_ThrallAbil3[srcIdx]
            set udg_Wild_ThrallAbil4[dstIdx] = udg_Wild_ThrallAbil4[srcIdx]
            set udg_Wild_ThrallAbilLv1[dstIdx] = udg_Wild_ThrallAbilLv1[srcIdx]
            set udg_Wild_ThrallAbilLv2[dstIdx] = udg_Wild_ThrallAbilLv2[srcIdx]
            set udg_Wild_ThrallAbilLv3[dstIdx] = udg_Wild_ThrallAbilLv3[srcIdx]
            set udg_Wild_ThrallAbilLv4[dstIdx] = udg_Wild_ThrallAbilLv4[srcIdx]
            set udg_Wild_ThrallItem0[dstIdx] = udg_Wild_ThrallItem0[srcIdx]
            set udg_Wild_ThrallItem1[dstIdx] = udg_Wild_ThrallItem1[srcIdx]
            set udg_Wild_ThrallItem2[dstIdx] = udg_Wild_ThrallItem2[srcIdx]
            set udg_Wild_ThrallItem3[dstIdx] = udg_Wild_ThrallItem3[srcIdx]
            set udg_Wild_ThrallItem4[dstIdx] = udg_Wild_ThrallItem4[srcIdx]
            set udg_Wild_ThrallItem5[dstIdx] = udg_Wild_ThrallItem5[srcIdx]
            set k = k + 1
        endloop
        set k = 0
        loop
            exitwhen k >= 12
            set udg_Wild_CreepThrallType[toPid * 12 + k] = udg_Wild_CreepThrallType[fromPid * 12 + k]
            set udg_Wild_CreepThrallPower[toPid * 12 + k] = udg_Wild_CreepThrallPower[fromPid * 12 + k]
            set k = k + 1
        endloop

        if src != null and src != dst then
            call SM_CopyAbilLv(src, dst, 'A031')
            call SM_CopyAbilLv(src, dst, 'A032')
            call SM_CopyAbilLv(src, dst, 'A033')
            call SM_CopyAbilLv(src, dst, 'A034')
            call SM_CopyAbilLv(src, dst, 'A035')
            call SM_CopyAbilLv(src, dst, 'A036')
        endif

        set udg_Wild_IsMorphed[toPid] = udg_Wild_IsMorphed[fromPid]
        set udg_Wild_CurrentForm[toPid] = udg_Wild_CurrentForm[fromPid]
        set udg_Wild_CurrentFormType[toPid] = udg_Wild_CurrentFormType[fromPid]
        set udg_Wild_CurrentFormLevel[toPid] = udg_Wild_CurrentFormLevel[fromPid]
        set udg_Wild_CurrentSubIdx[toPid] = udg_Wild_CurrentSubIdx[fromPid]
        set udg_Wild_CurrentAbil[toPid] = udg_Wild_CurrentAbil[fromPid]
        if udg_Wild_IsMorphed[fromPid] and udg_Wild_CurrentForm[fromPid] >= 1 and udg_Wild_CurrentFormLevel[fromPid] >= 1 then
            set udg_Wild_MorphCD[toPid] = 0.0
            call Wild_DoMorph(dst, udg_Wild_CurrentForm[fromPid], udg_Wild_CurrentFormLevel[fromPid], IMaxBJ(1, udg_Wild_CurrentSubIdx[fromPid]))
            set udg_Wild_MorphCD[toPid] = 0.0
        endif
        call Wild_UpdateHeroSoulBonus(toPid)
        call Wild_UpdateSoulTooltip(toPid)

    elseif ut == 'H004' then
        set udg_Strain_Hero[toPid] = dst
        set udg_Strain_EvoStage[toPid] = udg_Strain_EvoStage[fromPid]
        set udg_Strain_DevourCount[toPid] = udg_Strain_DevourCount[fromPid]
        set udg_Strain_TotalBonusHP[toPid] = udg_Strain_TotalBonusHP[fromPid]
        set udg_Strain_TotalBonusAtk[toPid] = udg_Strain_TotalBonusAtk[fromPid]
        set udg_Strain_TotalBonusMana[toPid] = udg_Strain_TotalBonusMana[fromPid]
        set udg_Strain_TotalBonusArmor[toPid] = udg_Strain_TotalBonusArmor[fromPid]
        set udg_Strain_GeneCat[toPid] = udg_Strain_GeneCat[fromPid]
        set udg_Strain_EvoTier[toPid] = udg_Strain_EvoTier[fromPid]
        set udg_Strain_StolenHeroAbil[toPid] = udg_Strain_StolenHeroAbil[fromPid]
        set udg_Strain_StolenAbil1[toPid] = udg_Strain_StolenAbil1[fromPid]
        set udg_Strain_StolenAbil2[toPid] = udg_Strain_StolenAbil2[fromPid]
        set udg_Strain_EvoTier1[toPid] = udg_Strain_EvoTier1[fromPid]
        set udg_Strain_EvoTier2[toPid] = udg_Strain_EvoTier2[fromPid]
        set udg_Strain_MimicType[toPid] = udg_Strain_MimicType[fromPid]
        set udg_Strain_MimicOwner[toPid] = udg_Strain_MimicOwner[fromPid]

        if src != null and src != dst then
            call SM_CopyAbilLv(src, dst, 'A021')
            call SM_CopyAbilLv(src, dst, 'A022')
            call SM_CopyAbilLv(src, dst, 'A023')
            call SM_CopyAbilLv(src, dst, 'A024')
            call SM_CopyAbilLv(src, dst, 'A025')
            call SM_CopyAbilLv(src, dst, 'A026')
            call SM_CopyAbilLv(src, dst, udg_Strain_StolenAbil1[fromPid])
            call SM_CopyAbilLv(src, dst, udg_Strain_StolenAbil2[fromPid])
            call SM_CopyAbilLv(src, dst, udg_Strain_StolenHeroAbil[fromPid])
        endif
        call Strain_ApplyCurrentSkin(dst, toPid)
        call Strain_UpdateEvoUI(toPid)

    elseif ut == 'H003' then
        set udg_Ninja_TrueHero[toPid] = dst
        set udg_Ninja_AuraOn[toPid] = udg_Ninja_AuraOn[fromPid]
        if udg_Ninja_CloneGroup[toPid] == null then
            set udg_Ninja_CloneGroup[toPid] = CreateGroup()
        endif
        if src != null and src != dst then
            call SM_CopyAbilLv(src, dst, 'A011')
            call SM_CopyAbilLv(src, dst, 'A012')
            call SM_CopyAbilLv(src, dst, 'A013')
            call SM_CopyAbilLv(src, dst, 'A014')
            call SM_CopyAbilLv(src, dst, 'A015')
        endif
        if udg_Ninja_AuraOn[toPid] and udg_Ninja_AuraFx[toPid] == null then
            set udg_Ninja_AuraFx[toPid] = AddSpecialEffectTarget("Abilities\\Spells\\Other\\GeneralAuraTarget\\GeneralAuraTarget.mdl", dst, "origin")
        endif

    elseif ut == 'H002' then
        if src != null and src != dst then
            call SM_CopyAbilLv(src, dst, 'A001')
            call SM_CopyAbilLv(src, dst, 'A002')
            call SM_CopyAbilLv(src, dst, 'A003')
            call SM_CopyAbilLv(src, dst, 'A004')
        endif
        call DM_GetHeroIndex(dst)
    endif
endfunction

function SM_CreateMirror takes unit orig, real mx, real my returns unit
    local unit m = null
    local integer ut = 0
    local integer origPid = 0
    local integer i = 0
    local integer aid = 0
    local item it = null
    local item newIt = null
    local boolean isHero = false
    local real curHP = 0.0
    local real curMana = 0.0

    if orig == null then
        return null
    endif
    set orig = Asn_GetTargetTrueUnit(orig)
    set ut = GetUnitTypeId(orig)
    set origPid = GetPlayerId(GetOwningPlayer(orig))
    set isHero = IsUnitType(orig, UNIT_TYPE_HERO)

    call SM_ResetCustomHeroSlot(13)
    set m = CreateUnit(Player(13), ut, mx, my, 180.0)
    if m == null then
        return null
    endif
    call RemoveGuardPosition(m)

    if isHero then
        if GetHeroLevel(orig) > 1 then
            call SetHeroLevel(m, GetHeroLevel(orig), false)
        endif
        call UnitModifySkillPoints(m, -GetHeroSkillPoints(m))
        call SetHeroStr(m, IMaxBJ(1, GetHeroStr(orig, false)), true)
        call SetHeroAgi(m, IMaxBJ(1, GetHeroAgi(orig, false)), true)
        call SetHeroInt(m, IMaxBJ(1, GetHeroInt(orig, false)), true)

        set i = 0
        loop
            exitwhen i >= udg_SM_HeroAbilCount
            set aid = udg_SM_HeroAbilId[i]
            if GetUnitAbilityLevel(orig, aid) > 0 then
                call SM_CopyAbilLv(orig, m, aid)
            endif
            set i = i + 1
        endloop

        call SM_CopyCustomHeroState(origPid, 13, orig, m)

        set i = 0
        loop
            exitwhen i > 5
            set it = UnitItemInSlot(orig, i)
            if it != null then
                set newIt = UnitAddItemById(m, GetItemTypeId(it))
                if newIt != null then
                    call SetItemDroppable(newIt, false)
                    call SetItemPawnable(newIt, false)
                    call SetItemCharges(newIt, GetItemCharges(it))
                endif
            endif
            set i = i + 1
        endloop
    endif

    // Final exact live combat stats sync (matches all buffed / evolved / item-enhanced values!)
    call BlzSetUnitMaxHP(m, IMaxBJ(1, BlzGetUnitMaxHP(orig)))
    call BlzSetUnitMaxMana(m, IMaxBJ(0, BlzGetUnitMaxMana(orig)))
    call BlzSetUnitBaseDamage(m, BlzGetUnitBaseDamage(orig, 0), 0)
    call BlzSetUnitBaseDamage(m, BlzGetUnitBaseDamage(orig, 1), 1)
    call BlzSetUnitArmor(m, BlzGetUnitArmor(orig))
    if BlzGetUnitAttackCooldown(orig, 0) > 0.05 then
        call BlzSetUnitAttackCooldown(m, BlzGetUnitAttackCooldown(orig, 0), 0)
    endif
    if GetUnitMoveSpeed(orig) > 1.0 then
        call SetUnitMoveSpeed(m, GetUnitMoveSpeed(orig))
    endif
    if ut != 'H006' and ut != 'H005' and ut != 'H004' then
        if BlzGetUnitSkin(orig) != 0 and BlzGetUnitSkin(orig) != ut then
            call BlzSetUnitSkin(m, BlzGetUnitSkin(orig))
        endif
        call SetUnitVertexColor(m, 165, 225, 255, 230)
    elseif ut == 'H003' or ut == 'H002' then
        call SetUnitVertexColor(m, 165, 225, 255, 230)
    endif

    set curHP = RMinBJ(I2R(BlzGetUnitMaxHP(m)), RMaxBJ(1.0, GetWidgetLife(orig)))
    call SetWidgetLife(m, curHP)
    if BlzGetUnitMaxMana(m) > 0 then
        set curMana = RMinBJ(I2R(BlzGetUnitMaxMana(m)), GetUnitState(orig, UNIT_STATE_MANA))
        call SetUnitState(m, UNIT_STATE_MANA, curMana)
    endif

    set it = null
    set newIt = null
    return m
endfunction

function SM_IsContestantAlive takes unit u returns boolean
    local integer pId = 0
    local integer ut = 0
    if u == null then
        return false
    endif
    if not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
        return true
    endif
    set ut = GetUnitTypeId(u)
    set pId = GetPlayerId(GetOwningPlayer(u))
    if ut == 'H006' and pId >= 0 and pId <= 15 then
        if (udg_Maho_InEgg[pId] or udg_Maho_PendingEggEnter[pId]) and udg_Maho_EggUnit[pId] != null and not IsUnitType(udg_Maho_EggUnit[pId], UNIT_TYPE_DEAD) and GetWidgetLife(udg_Maho_EggUnit[pId]) > 0.405 then
            return true
        endif
    elseif ut == 'H003' and pId >= 0 and pId <= 15 then
        if Ninja_PickLivingClone(pId) != null then
            return true
        endif
    endif
    return false
endfunction

function SM_GetCombatHandle takes unit u returns unit
    local integer pId = 0
    local integer ut = 0
    local unit cl = null
    if u == null then
        return null
    endif
    set ut = GetUnitTypeId(u)
    set pId = GetPlayerId(GetOwningPlayer(u))
    if ut == 'H006' and pId >= 0 and pId <= 15 and udg_Maho_InEgg[pId] and udg_Maho_EggUnit[pId] != null and not IsUnitType(udg_Maho_EggUnit[pId], UNIT_TYPE_DEAD) then
        return udg_Maho_EggUnit[pId]
    elseif ut == 'H003' and pId >= 0 and pId <= 15 and (IsUnitType(u, UNIT_TYPE_DEAD) or GetWidgetLife(u) <= 0.405) then
        set cl = Ninja_PickLivingClone(pId)
        if cl != null then
            return cl
        endif
    endif
    return u
endfunction

function SM_RunStandardHeroAI takes unit m, unit opp returns boolean
    local integer i = 0
    local integer aid = 0
    local integer mode = 0
    local string ord = ""
    local real hpPct = 1.0
    local real mana = 0.0

    if m == null or opp == null then
        return false
    endif
    set hpPct = GetWidgetLife(m) / RMaxBJ(1.0, GetUnitState(m, UNIT_STATE_MAX_LIFE))
    set mana = GetUnitState(m, UNIT_STATE_MANA)

    set i = 0
    loop
        exitwhen i >= udg_SM_HeroAbilCount
        set aid = udg_SM_HeroAbilId[i]
        set mode = udg_SM_HeroAbilMode[i]
        set ord = udg_SM_HeroAbilOrd[i]
        if mode != 0 and ord != "" and GetUnitAbilityLevel(m, aid) > 0 then
            if BlzGetUnitAbilityCooldownRemaining(m, aid) <= 0.15 and mana >= 35.0 then
                if mode == 5 then
                    if hpPct < 0.65 and IssueImmediateOrder(m, ord) then
                        return true
                    endif
                elseif mode == 3 then
                    if (aid != 'AHhb' and aid != 'AOhw' and aid != 'ACrj') or hpPct < 0.72 then
                        if IssueTargetOrder(m, ord, m) then
                            return true
                        endif
                    endif
                elseif mode == 2 then
                    if IssueTargetOrder(m, ord, opp) then
                        return true
                    endif
                elseif mode == 4 then
                    if IssuePointOrder(m, ord, GetUnitX(opp), GetUnitY(opp)) then
                        return true
                    endif
                elseif mode == 1 then
                    if IssueImmediateOrder(m, ord) then
                        return true
                    endif
                endif
            endif
        endif
        set i = i + 1
    endloop
    return false
endfunction

function SM_RunMirrorAI takes nothing returns nothing
    local unit m = SM_GetCombatHandle(udg_SM_Mirror)
    local unit opp = SM_GetCombatHandle(udg_SM_Victim)
    local integer ut = 0
    local integer heroLv = 1
    local real dx = 0.0
    local real dy = 0.0
    local real dist = 0.0
    local group g = null
    local unit enumU = null
    local integer curOrd = 0
    local boolean didCast = false
    local integer sa = 0

    if m == null or opp == null then
        set m = null
        set opp = null
        return
    endif

    if udg_SM_MirrorCD_Q > 0.0 then
        set udg_SM_MirrorCD_Q = udg_SM_MirrorCD_Q - 1.0
    endif
    if udg_SM_MirrorCD_W > 0.0 then
        set udg_SM_MirrorCD_W = udg_SM_MirrorCD_W - 1.0
    endif
    if udg_SM_MirrorCD_E > 0.0 then
        set udg_SM_MirrorCD_E = udg_SM_MirrorCD_E - 1.0
    endif
    if udg_SM_MirrorCD_R > 0.0 then
        set udg_SM_MirrorCD_R = udg_SM_MirrorCD_R - 1.0
    endif
    if udg_SM_MirrorMorphCD > 0.0 then
        set udg_SM_MirrorMorphCD = udg_SM_MirrorMorphCD - 1.0
    endif

    if GetUnitTypeId(m) != 'u004' and not IsUnitPaused(m) then
        set ut = GetUnitTypeId(m)
        set dx = GetUnitX(opp) - GetUnitX(m)
        set dy = GetUnitY(opp) - GetUnitY(m)
        set dist = SquareRoot(dx * dx + dy * dy)

        if ut == 'H006' then
            // Mahoraga Mirror AI: E heal/cleanse + Q Watch + aggressive strike
            if udg_SM_MirrorCD_E <= 0.0 and (GetWidgetLife(m) < GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.55 or udg_Maho_CCTimer[13] > 0.05) and GetUnitState(m, UNIT_STATE_MANA) >= 50.0 then
                if IssueImmediateOrder(m, "resurrection") then
                    set udg_SM_MirrorCD_E = 14.0
                endif
            endif
            if udg_SM_MirrorCD_Q <= 0.0 and GetUnitAbilityLevel(m, 'A041') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 35.0 then
                if IssueTargetOrder(m, "cripple", opp) then
                    set udg_SM_MirrorCD_Q = 10.0
                endif
            endif
            call IssueTargetOrder(m, "attack", opp)

        elseif ut == 'H005' then
            // Wild Avatar Mirror AI: Wrath summon + dynamic Overlord Morph + form skills
            set heroLv = GetHeroLevel(m)
            if udg_SM_MirrorCD_R <= 0.0 and GetUnitAbilityLevel(m, 'A035') > 0 then
                if BlzGetUnitMaxMana(m) > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 150.0 then
                    call SetUnitState(m, UNIT_STATE_MANA, GetUnitState(m, UNIT_STATE_MANA) - 150.0)
                    call Wild_CastWrath(m)
                    set udg_SM_MirrorCD_R = 90.0
                elseif BlzGetUnitMaxMana(m) == 0 and udg_Wild_StoredManaRatio[13] >= 0.35 then
                    set udg_Wild_StoredManaRatio[13] = udg_Wild_StoredManaRatio[13] - 0.35
                    call Wild_CastWrath(m)
                    set udg_SM_MirrorCD_R = 90.0
                endif
            endif
            if udg_SM_MirrorMorphCD <= 0.0 and udg_Wild_MorphCD[13] <= 0.0 then
                if heroLv >= 10 then
                    if GetWidgetLife(m) < GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.55 then
                        call Wild_DoMorph(m, 2, 10, 1)
                    elseif dist <= 320.0 then
                        call Wild_DoMorph(m, 1, 10, 2)
                    else
                        call Wild_DoMorph(m, 3, 10, 1)
                    endif
                else
                    if GetWidgetLife(m) < GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.45 then
                        call Wild_DoMorph(m, 3, IMaxBJ(1, heroLv), 1)
                    elseif dist <= 350.0 then
                        call Wild_DoMorph(m, 1, IMaxBJ(1, heroLv), 2)
                    else
                        call Wild_DoMorph(m, 2, IMaxBJ(1, heroLv), 1)
                    endif
                endif
                set udg_SM_MirrorMorphCD = 12.0
            endif
            if udg_SM_MirrorCD_W <= 0.0 then
                if AI_CastWildFormSkill(m, opp) then
                    set udg_SM_MirrorCD_W = 6.0
                endif
            endif
            call IssueTargetOrder(m, "attack", opp)

        elseif ut == 'H004' then
            // Primordial Strain Mirror AI: Burrow engage/escape, Devour finish, Stolen skills
            if udg_Strain_Burrowed[13] then
                if dist <= 220.0 and GetWidgetLife(m) > GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.50 then
                    call IssueImmediateOrder(m, "windwalk")
                endif
            else
                if udg_SM_MirrorCD_Q <= 0.0 and GetUnitAbilityLevel(m, 'A021') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 50.0 and GetWidgetLife(m) < GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.40 then
                    if IssueImmediateOrder(m, "windwalk") then
                        set udg_SM_MirrorCD_Q = 12.0
                    endif
                endif
                if udg_SM_MirrorCD_W <= 0.0 and GetUnitAbilityLevel(m, 'A022') > 0 and udg_Strain_DigestTimer[13] <= 0.0 and GetUnitState(m, UNIT_STATE_MANA) >= 75.0 then
                    if GetWidgetLife(opp) <= GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.10 or GetWidgetLife(opp) <= GetUnitState(opp, UNIT_STATE_MAX_LIFE) * 0.28 then
                        if IssueTargetOrder(m, "devour", opp) then
                            set udg_SM_MirrorCD_W = 10.0
                        endif
                    endif
                endif
                if udg_SM_MirrorCD_R <= 0.0 then
                    set didCast = false
                    set sa = udg_Strain_StolenAbil1[13]
                    if sa != 0 and GetUnitAbilityLevel(m, sa) > 0 then
                        set didCast = AI_CastStolenSkill(m, sa, opp)
                    endif
                    if not didCast then
                        set sa = udg_Strain_StolenAbil2[13]
                        if sa != 0 and GetUnitAbilityLevel(m, sa) > 0 then
                            set didCast = AI_CastStolenSkill(m, sa, opp)
                        endif
                    endif
                    if didCast then
                        set udg_SM_MirrorCD_R = 6.0
                    endif
                endif
            endif
            call IssueTargetOrder(m, "attack", opp)

        elseif ut == 'H003' then
            // Magic Sound Ninja Mirror AI: Heartstopper toggle, Q clones, E Karma, R Avatar Clone
            if GetUnitAbilityLevel(m, 'A012') > 0 and not udg_Ninja_AuraOn[13] then
                set udg_Ninja_AuraOn[13] = true
                if udg_Ninja_AuraFx[13] == null then
                    set udg_Ninja_AuraFx[13] = AddSpecialEffectTarget("Abilities\\Spells\\Other\\GeneralAuraTarget\\GeneralAuraTarget.mdl", m, "origin")
                endif
            endif
            if udg_SM_MirrorCD_Q <= 0.0 and GetUnitAbilityLevel(m, 'A011') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 60.0 and dist <= 600.0 then
                if IssuePointOrder(m, "blizzard", GetUnitX(opp), GetUnitY(opp)) then
                    set udg_SM_MirrorCD_Q = 8.0
                endif
            endif
            if udg_SM_MirrorCD_E <= 0.0 and GetUnitAbilityLevel(m, 'A013') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 50.0 then
                if IssueTargetOrder(m, "shadowstrike", opp) then
                    set udg_SM_MirrorCD_E = 10.0
                endif
            endif
            if udg_SM_MirrorCD_R <= 0.0 and GetUnitAbilityLevel(m, 'A014') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 100.0 then
                if IssueImmediateOrder(m, "summongrizzly") then
                    set udg_SM_MirrorCD_R = 60.0
                endif
            endif
            call IssueTargetOrder(m, "attack", opp)

        elseif ut == 'H002' then
            // Dream Master Mirror AI: E illusions, Q stealth, attack
            if udg_SM_MirrorCD_E <= 0.0 and GetUnitAbilityLevel(m, 'A003') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 80.0 then
                if IssuePointOrder(m, "cloudoffog", GetUnitX(opp), GetUnitY(opp)) then
                    set udg_SM_MirrorCD_E = 14.0
                endif
            endif
            if udg_SM_MirrorCD_Q <= 0.0 and GetUnitAbilityLevel(m, 'A001') > 0 and GetUnitState(m, UNIT_STATE_MANA) >= 50.0 and GetWidgetLife(m) < GetUnitState(m, UNIT_STATE_MAX_LIFE) * 0.65 then
                if IssueImmediateOrder(m, "mirrorimage") then
                    set udg_SM_MirrorCD_Q = 15.0
                endif
            endif
            call IssueTargetOrder(m, "attack", opp)

        else
            // Standard Heroes, Bosses, Magic Creeps & Normal Soldiers
            if SM_RunStandardHeroAI(m, opp) then
                // spell cast queued
            endif
            set curOrd = GetUnitCurrentOrder(m)
            if curOrd == 0 or curOrd == 851972 or curOrd == 851973 or GetRandomInt(1, 3) == 1 then
                call IssueTargetOrder(m, "attack", opp)
            endif
        endif
    endif

    // Drive all Mirror allies (clones/thralls/beasts/summons) & AI-controlled Victim allies in arena
    set g = CreateGroup()
    call GroupEnumUnitsInRect(g, udg_SM_ArenaRect, null)
    loop
        set enumU = FirstOfGroup(g)
        exitwhen enumU == null
        call GroupRemoveUnit(g, enumU)
        if not IsUnitType(enumU, UNIT_TYPE_DEAD) and GetWidgetLife(enumU) > 0.405 and GetUnitTypeId(enumU) != 'u000' and GetUnitTypeId(enumU) != 'u004' then
            if GetOwningPlayer(enumU) == Player(13) and enumU != m then
                call IssueTargetOrder(enumU, "attack", opp)
            elseif GetOwningPlayer(enumU) == udg_SM_VictimOwner and (GetPlayerController(udg_SM_VictimOwner) != MAP_CONTROL_USER or enumU != udg_SM_Victim) then
                set curOrd = GetUnitCurrentOrder(enumU)
                if curOrd == 0 or curOrd == 851972 or curOrd == 851973 then
                    call IssueTargetOrder(enumU, "attack", m)
                endif
            endif
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set enumU = null
    set m = null
    set opp = null
endfunction

function SM_CleanArenaUnits takes player onlyOwner, unit keepUnit returns nothing
    local group g = null
    local unit u = null
    if udg_SM_ArenaRect == null then
        return
    endif
    set g = CreateGroup()
    call GroupEnumUnitsInRect(g, udg_SM_ArenaRect, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        if u != keepUnit and (onlyOwner == null or GetOwningPlayer(u) == onlyOwner) then
            if GetUnitTypeId(u) != 'u000' then
                call RemoveUnit(u)
            endif
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set u = null
endfunction

function SM_PlayerHasSameCustomHero takes player p, integer ut returns boolean
    local group g = null
    local unit u = null
    local boolean hasIt = false
    if p == null or (ut != 'H003' and ut != 'H004' and ut != 'H005' and ut != 'H006') then
        return false
    endif
    set g = CreateGroup()
    call GroupEnumUnitsOfPlayer(g, p, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null or hasIt
        call GroupRemoveUnit(g, u)
        if u != udg_SM_Mirror and GetUnitTypeId(u) == ut and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
            set hasIt = true
        endif
    endloop
    call DestroyGroup(g)
    set g = null
    set u = null
    return hasIt
endfunction

function SM_ApplyAllySlotAlliance takes player allyP, player masterP returns nothing
    local integer i = 0
    if allyP == null or masterP == null then
        return
    endif
    call SetPlayerAlliance(allyP, masterP, ALLIANCE_PASSIVE, true)
    call SetPlayerAlliance(allyP, masterP, ALLIANCE_SHARED_VISION, true)
    call SetPlayerAlliance(allyP, masterP, ALLIANCE_SHARED_CONTROL, true)
    call SetPlayerAlliance(allyP, masterP, ALLIANCE_SHARED_ADVANCED_CONTROL, true)
    call SetPlayerAlliance(masterP, allyP, ALLIANCE_PASSIVE, true)
    call SetPlayerAlliance(masterP, allyP, ALLIANCE_SHARED_VISION, true)
    call SetPlayerAlliance(masterP, allyP, ALLIANCE_SHARED_CONTROL, true)

    set i = 0
    loop
        exitwhen i > 15
        if Player(i) != allyP and Player(i) != masterP then
            if IsPlayerAlly(Player(i), masterP) then
                call SetPlayerAlliance(allyP, Player(i), ALLIANCE_PASSIVE, true)
                call SetPlayerAlliance(Player(i), allyP, ALLIANCE_PASSIVE, true)
                call SetPlayerAlliance(allyP, Player(i), ALLIANCE_SHARED_VISION, true)
            else
                call SetPlayerAlliance(allyP, Player(i), ALLIANCE_PASSIVE, false)
                call SetPlayerAlliance(Player(i), allyP, ALLIANCE_PASSIVE, false)
            endif
        endif
        set i = i + 1
    endloop
    call SetPlayerAlliance(allyP, Player(PLAYER_NEUTRAL_AGGRESSIVE), ALLIANCE_PASSIVE, false)
    call SetPlayerAlliance(Player(PLAYER_NEUTRAL_AGGRESSIVE), allyP, ALLIANCE_PASSIVE, false)
endfunction

function SM_CloseAndRelease takes integer outcome returns nothing
    local unit v = udg_SM_Victim
    local unit m = udg_SM_Mirror
    local unit rel = null
    local integer vPid = 0
    local integer i = 0
    local integer ut = 0
    local integer dstPid = 0
    local player dstPlayer = null

    if not udg_SM_Active then
        return
    endif
    set udg_SM_Active = false

    // Release outcome: 0=manual R close, 1=original won, 2=mirror won
    if outcome == 2 and m != null then
        if udg_Maho_InEgg[13] then
            call Maho_OnEggComplete(13)
        endif
        call SM_CleanArenaUnits(udg_SM_VictimOwner, null)
        call SM_CleanArenaUnits(Player(13), m)

        set dstPlayer = udg_SM_CasterOwner
        if dstPlayer == null then
            set dstPlayer = Player(0)
        endif
        set dstPid = GetPlayerId(dstPlayer)
        set ut = GetUnitTypeId(m)

        if SM_PlayerHasSameCustomHero(dstPlayer, ut) then
            set dstPid = udg_SM_NextAllySlot
            set dstPlayer = Player(dstPid)
            if udg_SM_NextAllySlot == 14 then
                set udg_SM_NextAllySlot = 15
            else
                set udg_SM_NextAllySlot = 14
            endif
            call SM_ResetCustomHeroSlot(dstPid)
            call SM_ApplyAllySlotAlliance(dstPlayer, udg_SM_CasterOwner)
        endif

        call SetUnitOwner(m, dstPlayer, true)
        call SetUnitVertexColor(m, 255, 255, 255, 255)
        if ut == 'H002' or ut == 'H003' or ut == 'H004' or ut == 'H005' or ut == 'H006' then
            call SM_CopyCustomHeroState(13, dstPid, m, m)
        endif
        call SM_ResetCustomHeroSlot(13)

        call SetUnitPosition(m, udg_SM_ReturnX, udg_SM_ReturnY)
        call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\MassTeleport\\MassTeleportTarget.mdl", GetUnitX(m), GetUnitY(m)))
        call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Demon\\DarkPortal\\DarkPortalTarget.mdl", GetUnitX(m), GetUnitY(m)))
        if udg_SM_ConqueredGroup != null then
            call GroupAddUnit(udg_SM_ConqueredGroup, m)
        endif
        if GetLocalPlayer() == udg_SM_CasterOwner then
            call PanCameraToTimed(GetUnitX(m), GetUnitY(m), 0.35)
            call SelectUnit(m, true)
            call PingMinimapEx(GetUnitX(m), GetUnitY(m), 5.0, 120, 220, 255, false)
        endif
        call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 9.0, "|cffcc66ff【镜像夺舍 · 破山而出！】|r 封印之山内的镜像彻底击杀了本尊【|cffffcc00" + GetUnitName(m) + "|r】，现已携全套属性与技能破封而出，永久归属于你麾下！")
    else
        call SM_ResetCustomHeroSlot(13)
        call SM_CleanArenaUnits(Player(13), null)
        if v != null then
            set rel = SM_GetCombatHandle(v)
            call SM_CleanArenaUnits(udg_SM_VictimOwner, rel)
            set vPid = GetPlayerId(GetOwningPlayer(v))
            if vPid >= 0 and vPid <= 15 and udg_Maho_InEgg[vPid] and udg_Maho_EggUnit[vPid] != null then
                call SetUnitPosition(v, udg_SM_ReturnX, udg_SM_ReturnY)
                call SetUnitPosition(udg_Maho_EggUnit[vPid], udg_SM_ReturnX, udg_SM_ReturnY)
            elseif rel != null and not IsUnitType(rel, UNIT_TYPE_DEAD) then
                call SetUnitPosition(rel, udg_SM_ReturnX, udg_SM_ReturnY)
            endif
            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\MassTeleport\\MassTeleportTarget.mdl", udg_SM_ReturnX, udg_SM_ReturnY))
            if GetLocalPlayer() == udg_SM_VictimOwner then
                call PanCameraToTimed(udg_SM_ReturnX, udg_SM_ReturnY, 0.35)
                call SelectUnit(rel, true)
            endif
            if outcome == 1 then
                call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 7.0, "|cff00ff80【破封而出！】|r |cffffcc00" + GetUnitName(v) + "|r 亲手斩灭了自己的完美镜像，成功脱出封印之山重返战场！")
            else
                call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 6.0, "|cffffcc00【解封 · 破山】|r 实验小兵主动关闭了封印之山，镜像化影消散，|cffffffff" + GetUnitName(v) + "|r 已安全放归原位！")
            endif
        endif
    endif

    set i = 0
    loop
        exitwhen i > 7
        if udg_SM_FogMod[i] != null then
            call FogModifierStop(udg_SM_FogMod[i])
            call DestroyFogModifier(udg_SM_FogMod[i])
            set udg_SM_FogMod[i] = null
        endif
        call SetPlayerAlliance(Player(13), Player(i), ALLIANCE_PASSIVE, true)
        call SetPlayerAlliance(Player(i), Player(13), ALLIANCE_PASSIVE, true)
        set i = i + 1
    endloop
    call SetPlayerAlliance(Player(13), Player(PLAYER_NEUTRAL_AGGRESSIVE), ALLIANCE_PASSIVE, true)
    call SetPlayerAlliance(Player(PLAYER_NEUTRAL_AGGRESSIVE), Player(13), ALLIANCE_PASSIVE, true)

    set udg_SM_Caster = null
    set udg_SM_CasterOwner = null
    set udg_SM_Victim = null
    set udg_SM_VictimOwner = null
    set udg_SM_Mirror = null
    set v = null
    set m = null
    set rel = null
    set dstPlayer = null
endfunction

function SM_ClampSingleUnit takes unit u returns nothing
    local real x = 0.0
    local real y = 0.0
    local boolean clamped = false
    if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
        return
    endif
    set x = GetUnitX(u)
    set y = GetUnitY(u)
    if x < -672.0 then
        set x = -672.0
        set clamped = true
    elseif x > 672.0 then
        set x = 672.0
        set clamped = true
    endif
    if y < 7360.0 then
        set y = 7360.0
        set clamped = true
    elseif y > 8000.0 then
        set y = 8000.0
        set clamped = true
    endif
    if clamped then
        call SetUnitX(u, x)
        call SetUnitY(u, y)
    endif
endfunction

function SM_ClampLoop takes nothing returns nothing
    local integer vPid = 0
    local group g = null
    local unit u = null
    if not udg_SM_Active then
        return
    endif
    call SM_ClampSingleUnit(udg_SM_Victim)
    call SM_ClampSingleUnit(udg_SM_Mirror)
    if udg_SM_Victim != null then
        set vPid = GetPlayerId(GetOwningPlayer(udg_SM_Victim))
        if vPid >= 0 and vPid <= 15 and udg_Maho_InEgg[vPid] and udg_Maho_EggUnit[vPid] != null then
            call SM_ClampSingleUnit(udg_Maho_EggUnit[vPid])
        endif
    endif
    if udg_Maho_InEgg[13] and udg_Maho_EggUnit[13] != null then
        call SM_ClampSingleUnit(udg_Maho_EggUnit[13])
    endif
    if udg_SM_ArenaRect != null then
        set g = CreateGroup()
        call GroupEnumUnitsInRect(g, udg_SM_ArenaRect, null)
        loop
            set u = FirstOfGroup(g)
            exitwhen u == null
            call GroupRemoveUnit(g, u)
            call SM_ClampSingleUnit(u)
        endloop
        call DestroyGroup(g)
        set g = null
        set u = null
    endif
endfunction

function SM_DuelTickLoop takes nothing returns nothing
    local boolean vAlive = false
    local boolean mAlive = false
    if not udg_SM_Active then
        return
    endif
    set vAlive = SM_IsContestantAlive(udg_SM_Victim)
    set mAlive = SM_IsContestantAlive(udg_SM_Mirror)

    if not mAlive then
        call SM_CloseAndRelease(1)
        return
    endif

    if not vAlive then
        set udg_SM_DeadCheckTimer = udg_SM_DeadCheckTimer + 1.0
        if (GetUnitAbilityLevel(udg_SM_Victim, 'AOre') > 0 or UnitHasItemOfTypeBJ(udg_SM_Victim, 'rnsp')) and udg_SM_DeadCheckTimer < 6.0 then
            return
        endif
        if udg_SM_DeadCheckTimer >= 2.0 then
            call SM_CloseAndRelease(2)
            return
        endif
    else
        set udg_SM_DeadCheckTimer = 0.0
        call SM_RunMirrorAI()
    endif
endfunction

function SM_CastSealMountain takes unit caster, unit tgt returns nothing
    local integer ut = 0
    local player casterP = null
    local player victimP = null
    local integer i = 0
    local integer vPid = 0
    local unit combatV = null

    if caster == null or tgt == null then
        return
    endif
    set casterP = GetOwningPlayer(caster)
    if udg_SM_Active then
        call DisplayTimedTextToPlayer(casterP, 0, 0, 5.0, "|cffff6600[封印术 · 山]|r 封印之山内正在决斗中！请等待分出胜负，或点击实验小兵 |[R] 解封·破山|r 提前关闭（|-mount|r 观战）。")
        set casterP = null
        return
    endif

    set tgt = Asn_GetTargetTrueUnit(tgt)
    set ut = GetUnitTypeId(tgt)
    if IsUnitType(tgt, UNIT_TYPE_DEAD) or GetWidgetLife(tgt) <= 0.405 or IsUnitType(tgt, UNIT_TYPE_STRUCTURE) or BlzIsUnitInvulnerable(tgt) or ut == 'n003' or ut == 'n005' or ut == 'u000' or ut == 'u00B' then
        call DisplayTimedTextToPlayer(casterP, 0, 0, 4.0, "|cffff6600[封印术 · 山]|r 该目标（建筑/无敌单位/自身小兵）无法被封入封印之山！")
        set casterP = null
        return
    endif

    set victimP = GetOwningPlayer(tgt)
    set udg_SM_Caster = caster
    set udg_SM_CasterOwner = casterP
    set udg_SM_Victim = tgt
    set udg_SM_VictimOwner = victimP
    set udg_SM_ReturnX = GetUnitX(tgt)
    set udg_SM_ReturnY = GetUnitY(tgt)
    set udg_SM_DeadCheckTimer = 0.0
    set udg_SM_MirrorCD_Q = 0.0
    set udg_SM_MirrorCD_W = 0.0
    set udg_SM_MirrorCD_E = 0.0
    set udg_SM_MirrorCD_R = 0.0
    set udg_SM_MirrorMorphCD = 0.0

    // Set Player(13) hostile strictly to victimP, passive to everyone else, shared vision to human caster owner
    set i = 0
    loop
        exitwhen i > 7
        if Player(i) == victimP then
            call SetPlayerAlliance(Player(13), Player(i), ALLIANCE_PASSIVE, false)
            call SetPlayerAlliance(Player(i), Player(13), ALLIANCE_PASSIVE, false)
        else
            call SetPlayerAlliance(Player(13), Player(i), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(i), Player(13), ALLIANCE_PASSIVE, true)
        endif
        call SetPlayerAlliance(Player(13), Player(i), ALLIANCE_SHARED_CONTROL, false)
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER then
            call SetPlayerAlliance(Player(13), Player(i), ALLIANCE_SHARED_VISION, true)
            if udg_SM_FogMod[i] != null then
                call FogModifierStop(udg_SM_FogMod[i])
                call DestroyFogModifier(udg_SM_FogMod[i])
            endif
            set udg_SM_FogMod[i] = CreateFogModifierRect(Player(i), FOG_OF_WAR_VISIBLE, udg_SM_ArenaRect, true, false)
            call FogModifierStart(udg_SM_FogMod[i])
        endif
        set i = i + 1
    endloop
    if victimP == Player(PLAYER_NEUTRAL_AGGRESSIVE) then
        call SetPlayerAlliance(Player(13), Player(PLAYER_NEUTRAL_AGGRESSIVE), ALLIANCE_PASSIVE, false)
        call SetPlayerAlliance(Player(PLAYER_NEUTRAL_AGGRESSIVE), Player(13), ALLIANCE_PASSIVE, false)
    else
        call SetPlayerAlliance(Player(13), Player(PLAYER_NEUTRAL_AGGRESSIVE), ALLIANCE_PASSIVE, true)
        call SetPlayerAlliance(Player(PLAYER_NEUTRAL_AGGRESSIVE), Player(13), ALLIANCE_PASSIVE, true)
    endif

    call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Undead\\DarkRitual\\DarkRitualTarget.mdl", udg_SM_ReturnX, udg_SM_ReturnY))

    set vPid = GetPlayerId(victimP)
    set combatV = SM_GetCombatHandle(tgt)
    if vPid >= 0 and vPid <= 15 and udg_Maho_InEgg[vPid] and udg_Maho_EggUnit[vPid] != null then
        call SetUnitPosition(tgt, -320.0, 7680.0)
        call SetUnitPosition(udg_Maho_EggUnit[vPid], -320.0, 7680.0)
        call SetUnitFacing(tgt, 0.0)
    else
        call SetUnitPosition(tgt, -320.0, 7680.0)
        call SetUnitFacing(tgt, 0.0)
    endif
    call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Undead\\DarkRitual\\DarkRitualTarget.mdl", -320.0, 7680.0))

    set udg_SM_Mirror = SM_CreateMirror(tgt, 320.0, 7680.0)
    set udg_SM_Active = true

    if udg_SM_Mirror != null and combatV != null then
        call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Demon\\DarkPortal\\DarkPortalTarget.mdl", 320.0, 7680.0))
        call IssueTargetOrder(udg_SM_Mirror, "attack", combatV)
        if GetPlayerController(victimP) != MAP_CONTROL_USER then
            call IssueTargetOrder(combatV, "attack", udg_SM_Mirror)
        endif
    endif

    call PingMinimapEx(0.0, 7680.0, 6.0, 200, 100, 255, true)
    if GetLocalPlayer() == victimP or GetLocalPlayer() == casterP then
        call PanCameraToTimed(0.0, 7680.0, 0.35)
    endif

    call DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 9.0, "|cffcc66ff【封印术 · 山！】|r 【|cffffcc00" + GetUnitName(tgt) + "|r】已被无视魔免封入孤立的封印之山，与全属性、全技能、全AI镜像展开生死决斗！（输入 |-mount|r 观战，按 |[R]|r 可随时破山解封）")

    set casterP = null
    set victimP = null
    set combatV = null
endfunction

function SM_RemoveTreeEnum takes nothing returns nothing
    call RemoveDestructable(GetEnumDestructable())
endfunction

function SM_InitSystem takes nothing returns nothing
    local rect clearR = null
    local integer i = 0
    local real ang = 0.0
    local real ex = 0.0
    local real ey = 0.0

    call SM_InitHeroAbilPool()
    set udg_SM_ArenaRect = Rect(-768.0, 7296.0, 768.0, 8064.0)
    set udg_SM_ConqueredGroup = CreateGroup()

    set clearR = Rect(-864.0, 7200.0, 864.0, 8160.0)
    call EnumDestructablesInRect(clearR, null, function SM_RemoveTreeEnum)
    call RemoveRect(clearR)
    set clearR = null

    set i = 0
    loop
        exitwhen i >= 12
        set ang = I2R(i) * 0.5236
        set ex = 710.0 * Cos(ang)
        set ey = 7680.0 + 330.0 * Sin(ang)
        call AddSpecialEffect("Abilities\\Spells\\Human\\ManaFlare\\ManaFlareBase.mdl", ex, ey)
        set i = i + 1
    endloop

    call SetPlayerColor(Player(13), PLAYER_COLOR_AQUA)
    call SetPlayerColor(Player(14), PLAYER_COLOR_LIGHT_BLUE)
    call SetPlayerColor(Player(15), PLAYER_COLOR_SNOW)

    call TimerStart(CreateTimer(), 0.10, true, function SM_ClampLoop)
    call TimerStart(CreateTimer(), 1.00, true, function SM_DuelTickLoop)
endfunction

function SM_OnStartTimer takes nothing returns nothing
    local timer t = GetExpiredTimer()
    call PauseTimer(t)
    call DestroyTimer(t)
    set t = null
    call SM_InitSystem()
endfunction

function DM_OnSpellEffect takes nothing returns boolean'''

    text = replace_once(
        text,
        r'''function DM_OnSpellEffect takes nothing returns boolean''',
        sm_funcs,
        '5_SM_functions'
    )

    # 6. Hook A083 and A084 in DM_OnSpellEffect
    text = replace_once(
        text,
        r'''    if abil == 'A060' then
        call BuffExp_ApplyAllBuffs(caster, GetSpellTargetUnit())
        set caster = null
        return false
    elseif abil == 'A061' then
        call BuffExp_ApplyAllDebuffs(caster, GetSpellTargetUnit())
        set caster = null
        return false
    endif''',
        r'''    if abil == 'A060' then
        call BuffExp_ApplyAllBuffs(caster, GetSpellTargetUnit())
        set caster = null
        return false
    elseif abil == 'A061' then
        call BuffExp_ApplyAllDebuffs(caster, GetSpellTargetUnit())
        set caster = null
        return false
    elseif abil == 'A083' then
        call SM_CastSealMountain(caster, GetSpellTargetUnit())
        set caster = null
        return false
    elseif abil == 'A084' then
        if udg_SM_Active then
            call SM_CloseAndRelease(0)
        else
            call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 4.0, "|cffaaaaaa[解封 · 破山]|r 当前封印之山内没有被封印的单位。")
        endif
        set caster = null
        return false
    endif''',
        '6_DM_OnSpellEffect_SM_hooks'
    )

    # 7. Add -mount / -mountain camera command & update -buffunit notice
    text = replace_once(
        text,
        r'''            call DisplayTimedTextToPlayer(p, 0, 0, 7.0, "|cff00ffcc【实验单位已召唤】|r 已为你部署一只新的【实验小兵 · 万象状态师】：[Q] 万象全Buff（不含魔免） / [W] 万厄全Debuff！")
            set u = null
        endif
    elseif s == "-archimonde" then''',
        r'''            call DisplayTimedTextToPlayer(p, 0, 0, 7.0, "|cff00ffcc【实验单位已召唤】|r 已为你部署一只新的【实验小兵 · 万象状态师】：[Q] 全Buff / [W] 全Debuff / [E] 封印术·山 / [R] 解封·破山！")
            set u = null
        endif
    elseif s == "-mount" or s == "-mountain" then
        if GetLocalPlayer() == p then
            call PanCameraToTimed(0.0, 7680.0, 0.30)
            call PingMinimapEx(0.0, 7680.0, 5.0, 200, 100, 255, false)
        endif
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cffcc66ff【封印之山】|r 镜头已切至孤立决斗场地（地图正北山巅结界 (0, 7680)）！")
    elseif s == "-archimonde" then''',
        '7_TM_OnChatCommand_mount'
    )

    # 8. Start SM_OnStartTimer in DM_InitTriggers
    text = replace_once(
        text,
        r'''    call TimerStart(CreateTimer(), 1.80, false, function BuffExp_OnStartTimer)''',
        r'''    call TimerStart(CreateTimer(), 1.80, false, function BuffExp_OnStartTimer)
    call TimerStart(CreateTimer(), 1.95, false, function SM_OnStartTimer)''',
        '8_DM_InitTriggers_SM_timer'
    )

    # 9. Expand SetCameraBounds top edge 7168.0 -> 8192.0 so camera can pan into Seal Mountain
    text = replace_once(
        text,
        r'''    call SetCameraBounds( -9472.0 + GetCameraMargin(CAMERA_MARGIN_LEFT), -7680.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM), 9472.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT), 7168.0 - GetCameraMargin(CAMERA_MARGIN_TOP), -9472.0 + GetCameraMargin(CAMERA_MARGIN_LEFT), 7168.0 - GetCameraMargin(CAMERA_MARGIN_TOP), 9472.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT), -7680.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM) )''',
        r'''    call SetCameraBounds( -9472.0 + GetCameraMargin(CAMERA_MARGIN_LEFT), -7680.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM), 9472.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT), 8192.0 - GetCameraMargin(CAMERA_MARGIN_TOP), -9472.0 + GetCameraMargin(CAMERA_MARGIN_LEFT), 8192.0 - GetCameraMargin(CAMERA_MARGIN_TOP), 9472.0 - GetCameraMargin(CAMERA_MARGIN_RIGHT), -7680.0 + GetCameraMargin(CAMERA_MARGIN_BOTTOM) )''',
        '9_SetCameraBounds_north_expand'
    )

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open(TARGET_PATH, 'wb') as f:
        f.write(out_bytes)
    print("Successfully applied v6.9 Seal Mountain patches to payload/war3map.j!")


if __name__ == '__main__':
    main()
