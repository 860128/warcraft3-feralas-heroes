# -*- coding: utf-8 -*-
import sys
import os

def main():
    jass_path = 'payload/war3map.j'
    with open(jass_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original content length: {len(content)}")

    # 1. Globals declaration: Add udg_Strain_TotalBonusArmor, udg_Strain_DevourCount, udg_Strain_EvoStage, udg_Strain_Stage3Fx
    target_globals = '''    integer array udg_Strain_TotalBonusMana'''
    repl_globals = '''    integer array udg_Strain_TotalBonusMana
    real array udg_Strain_TotalBonusArmor
    integer array udg_Strain_DevourCount
    integer array udg_Strain_EvoStage
    effect array udg_Strain_Stage3Fx'''
    assert target_globals in content, "target_globals not found"
    content = content.replace(target_globals, repl_globals, 1)
    print("1. Globals declared.")

    # 2. Add Strain_ApplyCurrentSkin, Strain_UpdateEvoUI, Strain_CheckEvolution right before Strain_InitHero
    target_inithero = '''function Strain_InitHero takes unit h returns nothing
    if h == null then
        return
    endif
    if GetUnitAbilityLevel(h, 'A024') == 0 then
        call UnitAddAbility(h, 'A024')
    endif
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Burrow\\\\BurrowTarget.mdl", h, "origin"))
endfunction'''

    repl_inithero = '''function Strain_ApplyCurrentSkin takes unit u, integer pId returns nothing
    local integer stage = 0
    if u == null then
        return
    endif
    set stage = udg_Strain_EvoStage[pId]
    if stage == 0 then
        call BlzSetUnitSkin(u, 'zzrg')
        call SetUnitScale(u, 1.15, 1.15, 1.15)
    elseif stage == 1 then
        call BlzSetUnitSkin(u, 'nano')
        call SetUnitScale(u, 1.30, 1.30, 1.30)
    elseif stage == 2 then
        call BlzSetUnitSkin(u, 'zhyd')
        call SetUnitScale(u, 1.40, 1.40, 1.40)
    elseif stage >= 3 then
        call BlzSetUnitSkin(u, 'Ucrl')
        call SetUnitScale(u, 1.65, 1.65, 1.65)
    endif
endfunction

function Strain_UpdateEvoUI takes integer pId returns nothing
    local integer devours = 0
    local integer stage = 0
    local string stageTitle = ""
    local string nextReq = ""
    local string titleR = ""
    local string tipR = ""
    local string titleW = ""
    local string tipW = ""
    local integer curBonusHP = 0
    local integer curBonusAtk = 0
    local integer curBonusMana = 0
    local real curBonusArmor = 0.0

    if pId < 0 or pId > 15 then
        return
    endif

    set devours = udg_Strain_DevourCount[pId]
    set stage = udg_Strain_EvoStage[pId]
    set curBonusHP = udg_Strain_TotalBonusHP[pId]
    set curBonusAtk = udg_Strain_TotalBonusAtk[pId]
    set curBonusMana = udg_Strain_TotalBonusMana[pId]
    set curBonusArmor = udg_Strain_TotalBonusArmor[pId]

    if stage == 0 then
        set stageTitle = "【幼体·星际跳虫】(近战128)"
        set nextReq = "还需 " + I2S(8 - devours) + " 次吞噬进阶【紫晶巨蝎】"
    elseif stage == 1 then
        set stageTitle = "【一阶·紫晶重装巨蝎】(+45移速/+20%攻速)"
        set nextReq = "还需 " + I2S(18 - devours) + " 次吞噬进阶【星际刺蛇】"
    elseif stage == 2 then
        set stageTitle = "【二阶·星际虫族刺蛇】(500远程强酸骨刺/2.5%每秒回血)"
        set nextReq = "还需 " + I2S(30 - devours) + " 次吞噬进阶【始祖利维坦虫皇】"
    else
        set stageTitle = "【终极·始祖利维坦虫皇】(永久魔免/25%吸血/4秒深渊饕餮)"
        set nextReq = "已达最高始祖形态！"
    endif

    set titleR = "异种蜕壳进化 (R) [形态:" + I2S(stage) + "阶 | 吞噬:" + I2S(devours) + "次]"
    set tipR = "查看异种之源当前的蜕壳进化阶级与掠夺基因。|n|n|cff00ff00【星际虫族蜕壳状态】|r|n- 当前阶级：|cffffcc00" + stageTitle + "|r|n- 累计吞噬：|cffff00ff" + I2S(devours) + " 次|r|n- 蜕壳进度：|cff00ccff" + nextReq + "|r|n|n|cff00ff00【全维基因累计增幅】|r|n- 累计生命：|cffffcc00+" + I2S(curBonusHP) + "|r|n- 累计攻击：|cffff6600+" + I2S(curBonusAtk) + "|r|n- 累计法力：|cff33ccff+" + I2S(curBonusMana) + "|r|n- 累计护甲：|cffaaaaaa+" + R2SW(curBonusArmor, 1, 1) + "|r"

    if stage >= 3 then
        set titleW = "深渊饕餮 (W)"
        set tipW = "【终极始祖饕餮】：撕裂吞噬任意敌方单位，冷却极速缩短为 4.0 秒，消化时间缩短为 1.0 秒！|n吞噬英雄时抽 10 点属性并掠夺 10% 血蓝与攻击，吞噬普通单位全维吸收血/攻/护甲！"
    endif

    if GetLocalPlayer() == Player(pId) then
        call BlzSetAbilityTooltip('A024', titleR, 0)
        call BlzSetAbilityExtendedTooltip('A024', tipR, 0)
        if stage >= 3 then
            call BlzSetAbilityTooltip('A022', titleW, 0)
            call BlzSetAbilityTooltip('A022', titleW, 1)
            call BlzSetAbilityTooltip('A022', titleW, 2)
            call BlzSetAbilityExtendedTooltip('A022', tipW, 0)
            call BlzSetAbilityExtendedTooltip('A022', tipW, 1)
            call BlzSetAbilityExtendedTooltip('A022', tipW, 2)
        endif
    endif
endfunction

function Strain_CheckEvolution takes unit u, integer pId returns nothing
    local integer devours = udg_Strain_DevourCount[pId]
    local integer curStage = udg_Strain_EvoStage[pId]

    if u == null or IsUnitType(u, UNIT_TYPE_DEAD) then
        return
    endif

    // Stage 1 threshold: 8 devours
    if devours >= 8 and curStage < 1 then
        set udg_Strain_EvoStage[pId] = 1
        set curStage = 1

        call BlzSetUnitSkin(u, 'nano')
        call SetUnitScale(u, 1.30, 1.30, 1.30)
        call SetUnitMoveSpeed(u, GetUnitMoveSpeed(u) + 45.0)
        call BlzSetUnitAttackCooldown(u, BlzGetUnitAttackCooldown(u, 0) * 0.80, 0)
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + 300)
        call SetWidgetLife(u, GetWidgetLife(u) + 300.0)
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + 25, 0)
        call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + 4.0)
        set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + 300
        set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + 25
        set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + 4.0

        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Devour\\\\DevourEffectArt.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5.0, "|cff9900ff【一阶基因蜕壳·紫晶重装巨蝎】|r 异种之源突破幼体束缚完成蜕壳！永久获得 +45移速 / +20%攻速 / +300生命 / +25攻击 / +4护甲！")
    endif

    // Stage 2 threshold: 18 devours
    if devours >= 18 and curStage < 2 then
        set udg_Strain_EvoStage[pId] = 2
        set curStage = 2

        call BlzSetUnitSkin(u, 'zhyd')
        call SetUnitScale(u, 1.40, 1.40, 1.40)
        call SetUnitAcquireRange(u, 650.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 0, 500.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_RANGE, 1, 500.0)
        call BlzSetUnitWeaponRealField(u, UNIT_WEAPON_RF_ATTACK_PROJECTILE_SPEED, 0, 1200.0)
        call BlzSetUnitWeaponStringField(u, UNIT_WEAPON_SF_ATTACK_PROJECTILE_ART, 0, "Abilities\\\\Weapons\\\\ChimaeraAcidMissile\\\\ChimaeraAcidMissile.mdl")
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + 600)
        call SetWidgetLife(u, GetWidgetLife(u) + 600.0)
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + 45, 0)
        call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + 6.0)
        set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + 600
        set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + 45
        set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + 6.0

        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Orc\\\\Devour\\\\DevourEffectArt.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5.0, "|cff33ff33【二阶基因蜕壳·星际虫族刺蛇】|r 进化为星际刺蛇！获得500码远程强酸骨刺喷射、每秒2.5%最大生命值再生甲壳、+600生命 / +45攻击 / +6护甲！")
    endif

    // Stage 3 threshold: 30 devours
    if devours >= 30 and curStage < 3 then
        set udg_Strain_EvoStage[pId] = 3
        set curStage = 3

        call BlzSetUnitSkin(u, 'Ucrl')
        call SetUnitScale(u, 1.65, 1.65, 1.65)
        call UnitAddAbility(u, 'ACmi')
        call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + 1200)
        call SetWidgetLife(u, GetWidgetLife(u) + 1200.0)
        call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + 80, 0)
        call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + 10.0)
        set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + 1200
        set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + 80
        set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + 10.0

        if udg_Strain_Stage3Fx[pId] != null then
            call DestroyEffect(udg_Strain_Stage3Fx[pId])
        endif
        set udg_Strain_Stage3Fx[pId] = AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\DarkSummoning\\\\DarkSummonTarget.mdl", u, "chest")

        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Human\\\\Thunderclap\\\\ThunderClapCaster.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Objects\\\\Spawnmodels\\\\Human\\\\HumanLargeDeathExplode\\\\HumanLargeDeathExplode.mdl", u, "origin"))
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 6.0, "|cffff0000【终极基因蜕壳·始祖利维坦虫皇】|r 登顶为至高无上的深渊始祖虫皇！获得永久魔免、25%深渊吸血、W技能4秒CD且1秒秒速消化、+1200生命 / +80攻击 / +10护甲！")
    endif

    call Strain_UpdateEvoUI(pId)
endfunction

function Strain_InitHero takes unit h returns nothing
    local integer pId = 0
    if h == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(h))
    set udg_Strain_Hero[pId] = h
    if GetUnitAbilityLevel(h, 'A024') == 0 then
        call UnitAddAbility(h, 'A024')
    endif
    call Strain_ApplyCurrentSkin(h, pId)
    call Strain_UpdateEvoUI(pId)
    call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\Burrow\\\\BurrowTarget.mdl", h, "origin"))
endfunction'''

    assert target_inithero in content, "target_inithero not found"
    content = content.replace(target_inithero, repl_inithero, 1)
    print("2. Evolution helpers & Strain_InitHero updated.")

    # 3. Update Strain_BreakMimicry to call Strain_ApplyCurrentSkin
    target_break_mimic = '''        call SetUnitColor(u, GetPlayerColor(GetOwningPlayer(u)))
        call SetPlayerAllianceStateBJ(Player(PLAYER_NEUTRAL_AGGRESSIVE), GetOwningPlayer(u), bj_ALLIANCE_UNALLIED)
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageDeathCaster.mdl", GetUnitX(u), GetUnitY(u)))'''
    repl_break_mimic = '''        call SetUnitColor(u, GetPlayerColor(GetOwningPlayer(u)))
        call SetPlayerAllianceStateBJ(Player(PLAYER_NEUTRAL_AGGRESSIVE), GetOwningPlayer(u), bj_ALLIANCE_UNALLIED)
        call Strain_ApplyCurrentSkin(u, pId)
        call DestroyEffect(AddSpecialEffect("Abilities\\\\Spells\\\\Orc\\\\MirrorImage\\\\MirrorImageDeathCaster.mdl", GetUnitX(u), GetUnitY(u)))'''
    assert target_break_mimic in content, "target_break_mimic not found"
    content = content.replace(target_break_mimic, repl_break_mimic, 1)
    print("3. Strain_BreakMimicry updated.")

    # 4. Update Strain_ClearCurrentGene: scale & speed
    target_clear_gene = '''        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))
        call SetUnitScale(u, 1.25, 1.25, 1.25)'''
    repl_clear_gene = '''        if udg_Strain_EvoStage[pId] >= 1 then
            call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 45.0)
        else
            call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))
        endif
        call Strain_ApplyCurrentSkin(u, pId)'''
    assert target_clear_gene in content, "target_clear_gene not found"
    content = content.replace(target_clear_gene, repl_clear_gene, 1)
    print("4. Strain_ClearCurrentGene updated.")

    # 5. Update Strain_DrainEnemyHero with 4+wLv*2, 10% HP/Atk drain, and +3 devours
    target_drain_hero = '''function Strain_DrainEnemyHero takes unit caster, unit victim returns nothing
    local integer pId = 0
    local integer k = 1
    local integer vAgi = 0
    local integer vStr = 0
    local integer vInt = 0
    local integer curMaxHP = 0
    local integer curMaxMana = 0
    local integer drainHP = 0
    local integer drainMana = 0
    local integer gainAgi = 0
    local integer gainStr = 0
    local integer gainInt = 0
    local integer totalDrainHP = 0
    local integer totalDrainMana = 0
    local boolean drainedSomething = false
    local string gainMsg = ""
    local integer idx = 0
    local integer cIdx = -1

    if caster == null or victim == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(caster))

    // 1. Cascading drain 4 points: Agi -> Str -> Int -> Max HP/Mana down to 1
    // Mirror Gain: whatever is drained from enemy is permanently added to H004
    loop
        exitwhen k > 4'''

    repl_drain_hero = '''function Strain_DrainEnemyHero takes unit caster, unit victim returns nothing
    local integer pId = 0
    local integer k = 1
    local integer maxK = 6
    local integer wLv = 1
    local integer vAgi = 0
    local integer vStr = 0
    local integer vInt = 0
    local integer curMaxHP = 0
    local integer curMaxMana = 0
    local integer drainHP = 0
    local integer drainMana = 0
    local integer gainAgi = 0
    local integer gainStr = 0
    local integer gainInt = 0
    local integer totalDrainHP = 0
    local integer totalDrainMana = 0
    local integer heroMaxHP = 0
    local integer heroBaseAtk = 0
    local integer heroDrainHP = 0
    local integer heroDrainAtk = 0
    local boolean drainedSomething = false
    local string gainMsg = ""
    local integer idx = 0
    local integer cIdx = -1

    if caster == null or victim == null then
        return
    endif
    set pId = GetPlayerId(GetOwningPlayer(caster))
    set wLv = IMaxBJ(1, GetUnitAbilityLevel(caster, 'A022'))
    set maxK = 4 + wLv * 2

    // 1. Cascading drain (4 + wLv*2) points: Agi -> Str -> Int -> Max HP/Mana down to 1
    // Mirror Gain: whatever is drained from enemy is permanently added to H004
    loop
        exitwhen k > maxK'''

    assert target_drain_hero in content, "target_drain_hero not found"
    content = content.replace(target_drain_hero, repl_drain_hero, 1)

    target_drain_hero_end = '''    // 2. Track crippled hero so revive at Altar enforces Max HP / Mana clamp'''
    repl_drain_hero_end = '''    // 1.5. Direct 10% Max HP & 10% Base Attack Plunder
    set heroMaxHP = BlzGetUnitMaxHP(victim)
    set heroBaseAtk = BlzGetUnitBaseDamage(victim, 0)
    set heroDrainHP = R2I(I2R(heroMaxHP) * 0.10)
    set heroDrainAtk = R2I(I2R(heroBaseAtk) * 0.10)
    if heroDrainHP < 1 then
        set heroDrainHP = 1
    endif
    if heroDrainAtk < 1 then
        set heroDrainAtk = 1
    endif

    if heroMaxHP > heroDrainHP then
        call BlzSetUnitMaxHP(victim, heroMaxHP - heroDrainHP)
    else
        call BlzSetUnitMaxHP(victim, 1)
    endif
    if heroBaseAtk > heroDrainAtk then
        call BlzSetUnitBaseDamage(victim, heroBaseAtk - heroDrainAtk, 0)
    else
        call BlzSetUnitBaseDamage(victim, 1, 0)
    endif

    call BlzSetUnitMaxHP(caster, BlzGetUnitMaxHP(caster) + heroDrainHP)
    call BlzSetUnitBaseDamage(caster, BlzGetUnitBaseDamage(caster, 0) + heroDrainAtk, 0)
    set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + heroDrainHP
    set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + heroDrainAtk
    set totalDrainHP = totalDrainHP + heroDrainHP

    // Devour Count +3 for devouring an enemy hero
    set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 3
    call Strain_CheckEvolution(caster, pId)

    // 2. Track crippled hero so revive at Altar enforces Max HP / Mana clamp'''

    assert target_drain_hero_end in content, "target_drain_hero_end not found"
    content = content.replace(target_drain_hero_end, repl_drain_hero_end, 1)

    target_drain_msg = '''    if totalDrainMana > 0 then
        set gainMsg = gainMsg + " 法力+" + I2S(totalDrainMana)
    endif

    call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 5.0, "|cff00ff00[顶端掠食-镜像获得]|r 成功蚕食敌方英雄，永久夺取：" + gainMsg + "！")'''
    repl_drain_msg = '''    if totalDrainMana > 0 then
        set gainMsg = gainMsg + " 法力+" + I2S(totalDrainMana)
    endif
    if heroDrainAtk > 0 then
        set gainMsg = gainMsg + " 攻击+" + I2S(heroDrainAtk)
    endif

    call DisplayTimedTextToPlayer(GetOwningPlayer(caster), 0, 0, 5.0, "|cff00ff00[顶端掠食-镜像翻倍获得]|r 成功蚕食敌方英雄，永久夺取：" + gainMsg + "！(蜕壳进度+3，累计: " + I2S(udg_Strain_DevourCount[pId]) + "次)")'''
    assert target_drain_msg in content, "target_drain_msg not found"
    content = content.replace(target_drain_msg, repl_drain_msg, 1)
    print("5. Strain_DrainEnemyHero updated.")

    # 6. Update Strain_ShowGeneDialog to display evolution stage & thresholds
    target_dialog_msg = '''function Strain_ShowGeneDialog takes player p, integer pId returns nothing
    local string msg = "【异种之源 - 基因控制台】"
    if p == null then
        return
    endif
    set msg = msg + "\\n累计进化：+" + I2S(udg_Strain_TotalBonusHP[pId]) + "生命 / +" + I2S(udg_Strain_TotalBonusAtk[pId]) + "攻击 / +" + I2S(udg_Strain_TotalBonusMana[pId]) + "法力"'''

    repl_dialog_msg = '''function Strain_ShowGeneDialog takes player p, integer pId returns nothing
    local string msg = "【异种之源 - 基因控制台】"
    local integer devours = 0
    local integer stage = 0
    local string stageTitle = ""
    local string nextReq = ""

    if p == null then
        return
    endif
    set devours = udg_Strain_DevourCount[pId]
    set stage = udg_Strain_EvoStage[pId]

    if stage == 0 then
        set stageTitle = "幼体·星际跳虫 (近战128)"
        set nextReq = "还需 " + I2S(8 - devours) + " 次吞噬蜕壳为【紫晶重装巨蝎】"
    elseif stage == 1 then
        set stageTitle = "一阶·紫晶重装巨蝎 (+45移速/+20%攻速)"
        set nextReq = "还需 " + I2S(18 - devours) + " 次吞噬蜕壳为【星际虫族刺蛇】"
    elseif stage == 2 then
        set stageTitle = "二阶·星际虫族刺蛇 (500远程强酸骨刺/2.5%每秒回血)"
        set nextReq = "还需 " + I2S(30 - devours) + " 次吞噬蜕壳为【始祖利维坦虫皇】"
    else
        set stageTitle = "终极·始祖利维坦虫皇 (永久魔免/25%吸血/4秒深渊饕餮)"
        set nextReq = "已达始祖终极形态！"
    endif

    set msg = msg + "\\n【星际蜕壳】：" + stageTitle + " (累计吞噬: " + I2S(devours) + " 次)"
    set msg = msg + "\\n【进化进度】：" + nextReq
    set msg = msg + "\\n【全维增幅】：+" + I2S(udg_Strain_TotalBonusHP[pId]) + "生命 / +" + I2S(udg_Strain_TotalBonusAtk[pId]) + "攻击 / +" + I2S(udg_Strain_TotalBonusMana[pId]) + "法力 / +" + R2SW(udg_Strain_TotalBonusArmor[pId], 1, 1) + "护甲"'''

    assert target_dialog_msg in content, "target_dialog_msg not found"
    content = content.replace(target_dialog_msg, repl_dialog_msg, 1)
    print("6. Strain_ShowGeneDialog updated.")

    # 7. Update Strain_OnDigestComplete for non-hero: full-dimensional absorption + +1 devour count
    target_digest_nonhero = '''        if udg_Strain_DigestFeedType[pId] == 1 then
            // Case C: Melee Unit without Mana -> Permanent Max HP bonus
            set bonusHP = R2I(I2R(30 + 10 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + bonusHP)
            call SetWidgetLife(u, GetWidgetLife(u) + I2R(bonusHP))
            set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + bonusHP
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff00ff80[吞噬进化-近战猎物]|r 永久增加 " + I2S(bonusHP) + " 点最大生命值！（" + multStr + "收益，累计+" + I2S(udg_Strain_TotalBonusHP[pId]) + "生命）")
        elseif udg_Strain_DigestFeedType[pId] == 2 then
            // Case B: Ranged Unit without Mana -> Permanent Base Attack bonus (+1~2)
            if udg_Strain_DigestVictimLv[pId] <= 1 then
                set bonusAtk = R2I(1.0 * mult + 0.5)
            else
                set bonusAtk = R2I(2.0 * mult + 0.5)
            endif
            if bonusAtk < 1 then
                set bonusAtk = 1
            endif
            call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + bonusAtk, 0)
            set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + bonusAtk
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cffff6600[吞噬进化-远程猎物]|r 永久增加 " + I2S(bonusAtk) + " 点基础攻击力！（" + multStr + "收益，累计+" + I2S(udg_Strain_TotalBonusAtk[pId]) + "攻击）")
        else
            // Case A: Magical Unit -> Permanent Max Mana bonus
            set bonusMana = R2I(I2R(25 + 5 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            call BlzSetUnitMaxMana(u, BlzGetUnitMaxMana(u) + bonusMana)
            call SetUnitState(u, UNIT_STATE_MANA, GetUnitState(u, UNIT_STATE_MANA) + I2R(bonusMana))
            set udg_Strain_TotalBonusMana[pId] = udg_Strain_TotalBonusMana[pId] + bonusMana
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff33ccff[吞噬进化-魔法猎物]|r 永久增加 " + I2S(bonusMana) + " 点最大法力值！（" + multStr + "收益，累计+" + I2S(udg_Strain_TotalBonusMana[pId]) + "法力）")
        endif
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))'''

    repl_digest_nonhero = '''        if udg_Strain_DigestFeedType[pId] == 1 then
            // Case C: Melee Unit -> bonusHP = (45 + 22*vLv)*mult, bonusAtk = (2 + vLv)*mult, bonusArmor = 0.30*vLv*mult
            set bonusHP = R2I(I2R(45 + 22 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            set bonusAtk = R2I(I2R(2 + udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            set bonusArmor = 0.30 * I2R(udg_Strain_DigestVictimLv[pId]) * mult
            if bonusAtk < 1 then
                set bonusAtk = 1
            endif

            call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + bonusHP)
            call SetWidgetLife(u, GetWidgetLife(u) + I2R(bonusHP))
            call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + bonusAtk, 0)
            call BlzSetUnitArmor(u, BlzGetUnitArmor(u) + bonusArmor)
            set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + bonusHP
            set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + bonusAtk
            set udg_Strain_TotalBonusArmor[pId] = udg_Strain_TotalBonusArmor[pId] + bonusArmor
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff00ff80[全维基因吸收-近战猎物]|r 永久增加 +" + I2S(bonusHP) + "生命 / +" + I2S(bonusAtk) + "攻击 / +" + R2SW(bonusArmor, 1, 1) + "护甲！（" + multStr + "收益）")
        elseif udg_Strain_DigestFeedType[pId] == 2 then
            // Case B: Ranged Unit -> bonusHP = (25 + 12*vLv)*mult, bonusAtk = (4 + 3*vLv)*mult
            set bonusHP = R2I(I2R(25 + 12 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            set bonusAtk = R2I(I2R(4 + 3 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            if bonusAtk < 1 then
                set bonusAtk = 1
            endif

            call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + bonusHP)
            call SetWidgetLife(u, GetWidgetLife(u) + I2R(bonusHP))
            call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + bonusAtk, 0)
            set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + bonusHP
            set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + bonusAtk
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cffff6600[全维基因吸收-远程猎物]|r 永久增加 +" + I2S(bonusAtk) + "基础攻击 / +" + I2S(bonusHP) + "最大生命！（" + multStr + "收益）")
        else
            // Case A: Magical Unit -> bonusHP = (30 + 14*vLv)*mult, bonusMana = (35 + 15*vLv)*mult, bonusAtk = (3 + 2*vLv)*mult
            set bonusHP = R2I(I2R(30 + 14 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            set bonusMana = R2I(I2R(35 + 15 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            set bonusAtk = R2I(I2R(3 + 2 * udg_Strain_DigestVictimLv[pId]) * mult + 0.5)
            if bonusAtk < 1 then
                set bonusAtk = 1
            endif

            call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + bonusHP)
            call SetWidgetLife(u, GetWidgetLife(u) + I2R(bonusHP))
            call BlzSetUnitMaxMana(u, BlzGetUnitMaxMana(u) + bonusMana)
            call SetUnitState(u, UNIT_STATE_MANA, GetUnitState(u, UNIT_STATE_MANA) + I2R(bonusMana))
            call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + bonusAtk, 0)
            set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + bonusHP
            set udg_Strain_TotalBonusMana[pId] = udg_Strain_TotalBonusMana[pId] + bonusMana
            set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + bonusAtk
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff33ccff[全维基因吸收-魔法猎物]|r 永久增加 +" + I2S(bonusMana) + "法力 / +" + I2S(bonusHP) + "生命 / +" + I2S(bonusAtk) + "攻击！（" + multStr + "收益）")
        endif
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Items\\\\AIam\\\\AIamTarget.mdl", u, "origin"))

        // Devour count +1
        set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 1
        call Strain_CheckEvolution(u, pId)'''

    target_digest_vars = '''function Strain_OnDigestComplete takes unit u, integer pId returns nothing
    local integer tgtType = 0
    local integer bonusHP = 0
    local integer bonusAtk = 0
    local integer bonusMana = 0'''

    repl_digest_vars = '''function Strain_OnDigestComplete takes unit u, integer pId returns nothing
    local integer tgtType = 0
    local integer bonusHP = 0
    local integer bonusAtk = 0
    local integer bonusMana = 0
    local real bonusArmor = 0.0'''

    assert target_digest_vars in content, "target_digest_vars not found"
    content = content.replace(target_digest_vars, repl_digest_vars, 1)

    assert target_digest_nonhero in content, "target_digest_nonhero not found"
    content = content.replace(target_digest_nonhero, repl_digest_nonhero, 1)
    print("7. Strain_OnDigestComplete updated.")

    # 8. Update DM_CapTimerLoop: Regenerative Carapace for Stage >= 2
    target_cap_loop = '''    // 3.5. Process Hero #3 Digestion Timer Countdown'''
    repl_cap_loop = '''    // 3.4. Hero #3 Stage >= 2 Regenerative Carapace (2.5% Max HP / sec)
    set pId = 0
    loop
        exitwhen pId > 7
        if udg_Strain_EvoStage[pId] >= 2 then
            set u = udg_Strain_Hero[pId]
            if u == null then
                set u = udg_AI_CustomHero[pId]
            endif
            if u != null and not IsUnitType(u, UNIT_TYPE_DEAD) and GetWidgetLife(u) > 0.405 then
                call SetWidgetLife(u, GetWidgetLife(u) + 0.025 * I2R(BlzGetUnitMaxHP(u)))
            endif
            set u = null
        endif
        set pId = pId + 1
    endloop

    // 3.5. Process Hero #3 Digestion Timer Countdown'''
    assert target_cap_loop in content, "target_cap_loop not found"
    content = content.replace(target_cap_loop, repl_cap_loop, 1)
    print("8. DM_CapTimerLoop updated with Regenerative Carapace.")

    # 9. Update DM_OnSpellEffect for A022: Stage 3 Cooldown (4.0s) & Digest Time (1.0s)
    target_a022_cast = '''            set udg_Strain_DigestTimer[pId] = 8.0 - 1.5 * I2R(GetUnitAbilityLevel(caster, 'A022'))'''
    repl_a022_cast = '''            if udg_Strain_EvoStage[pId] >= 3 then
                set udg_Strain_DigestTimer[pId] = 1.0
                call BlzStartUnitAbilityCooldown(caster, 'A022', 4.0)
            else
                set udg_Strain_DigestTimer[pId] = 8.0 - 1.5 * I2R(GetUnitAbilityLevel(caster, 'A022'))
            endif'''
    assert target_a022_cast in content, "target_a022_cast not found"
    content = content.replace(target_a022_cast, repl_a022_cast, 1)
    print("9. A022 cast updated with Stage 3 4.0s CD & 1.0s digestion.")

    # 10. Update DM_OnUnitAttacked: H004 missile visual effect for Stage >= 2
    target_on_attacked = '''        if attTypeId == 'H004' then
            set pId = GetPlayerId(GetOwningPlayer(attacker))
            if udg_Strain_MimicActive[pId] then
                set udg_Strain_AmbushReady[pId] = true
                call Strain_BreakMimicry(attacker, pId)
            endif
        elseif attTypeId == 'H005' and target != null then'''
    repl_on_attacked = '''        if attTypeId == 'H004' then
            set pId = GetPlayerId(GetOwningPlayer(attacker))
            if udg_Strain_MimicActive[pId] then
                set udg_Strain_AmbushReady[pId] = true
                call Strain_BreakMimicry(attacker, pId)
            endif
            if udg_Strain_EvoStage[pId] >= 2 and target != null then
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Weapons\\\\ChimaeraAcidMissile\\\\ChimaeraAcidMissile.mdl", target, "chest"))
            endif
        elseif attTypeId == 'H005' and target != null then'''
    assert target_on_attacked in content, "target_on_attacked not found"
    content = content.replace(target_on_attacked, repl_on_attacked, 1)
    print("10. DM_OnUnitAttacked updated with Stage 2 acid missile art.")

    # 11. Update DM_OnDamaged: Stage 3 Abyss Lifesteal (25%)
    target_on_damaged = '''            // Gene On-Attack Effects
            set tier = udg_Strain_EvoTier[pId]'''
    repl_on_damaged = '''            // Stage 3: Abyss Lifesteal (heal 25% of damage dealt)
            if udg_Strain_EvoStage[pId] >= 3 then
                call SetWidgetLife(src, GetWidgetLife(src) + dmg * 0.25)
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\\\Spells\\\\Undead\\\\VampiricAura\\\\VampiricAuraTarget.mdl", src, "origin"))
            endif

            // Gene On-Attack Effects
            set tier = udg_Strain_EvoTier[pId]'''
    assert target_on_damaged in content, "target_on_damaged not found"
    content = content.replace(target_on_damaged, repl_on_damaged, 1)
    print("11. DM_OnDamaged updated with Stage 3 Abyss Lifesteal.")

    # 12. Update Wild_OnHeroReviveFinish & Refuge_ProcessRevives for H004 skin/scale/UI restore
    target_revive_finish = '''    if rev != null and GetUnitTypeId(rev) == 'H005' then
        set pId = GetPlayerId(GetOwningPlayer(rev))
        call Wild_ClearMorphAbil(rev, pId)
        call Wild_RevertToAvatar(rev)
    endif'''
    repl_revive_finish = '''    if rev != null and GetUnitTypeId(rev) == 'H005' then
        set pId = GetPlayerId(GetOwningPlayer(rev))
        call Wild_ClearMorphAbil(rev, pId)
        call Wild_RevertToAvatar(rev)
    elseif rev != null and GetUnitTypeId(rev) == 'H004' then
        set pId = GetPlayerId(GetOwningPlayer(rev))
        call Strain_ApplyCurrentSkin(rev, pId)
        call Strain_UpdateEvoUI(pId)
    endif'''
    assert target_revive_finish in content, "target_revive_finish not found"
    content = content.replace(target_revive_finish, repl_revive_finish, 1)

    target_refuge_revive = '''                    if GetUnitTypeId(u) == 'H005' then
                        call Wild_ClearMorphAbil(u, pId)
                        call Wild_RevertToAvatar(u)
                    endif'''
    repl_refuge_revive = '''                    if GetUnitTypeId(u) == 'H005' then
                        call Wild_ClearMorphAbil(u, pId)
                        call Wild_RevertToAvatar(u)
                    elseif GetUnitTypeId(u) == 'H004' then
                        call Strain_ApplyCurrentSkin(u, pId)
                        call Strain_UpdateEvoUI(pId)
                    endif'''
    assert target_refuge_revive in content, "target_refuge_revive not found"
    content = content.replace(target_refuge_revive, repl_refuge_revive) # replace all occurrences (there are 2 in refuge)
    print("12. Hero revive handlers updated.")

    # 13. Update TM_SpawnSandboxTargets: grant +4 devours on -spawn
    target_spawn_cmd = '''    if udg_Strain_Hero[pId] != null then
        call UnitResetCooldown(udg_Strain_Hero[pId])
    endif'''
    repl_spawn_cmd = '''    if udg_Strain_Hero[pId] != null then
        call UnitResetCooldown(udg_Strain_Hero[pId])
        set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 4
        call Strain_CheckEvolution(udg_Strain_Hero[pId], pId)
        call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cff00ff00[沙盒测试]|r 异种之源获得 +4 吞噬进度！累计: " + I2S(udg_Strain_DevourCount[pId]) + " 次")
    endif'''
    assert target_spawn_cmd in content, "target_spawn_cmd not found"
    content = content.replace(target_spawn_cmd, repl_spawn_cmd, 1)

    # 14. Add -evo chat command and declare pId in TM_OnChatCommand
    target_chat_head = '''function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif'''
    repl_chat_head = '''function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    local integer pId = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif
    if p != null then
        set pId = GetPlayerId(p)
    endif'''
    assert target_chat_head in content, "target_chat_head not found"
    content = content.replace(target_chat_head, repl_chat_head, 1)

    target_chat_cmds = '''    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    endif'''
    repl_chat_cmds = '''    elseif s == "-refuge" then
        call Refuge_Relocate(p)
    elseif s == "-evo" then
        if udg_Strain_Hero[pId] != null then
            set udg_Strain_DevourCount[pId] = udg_Strain_DevourCount[pId] + 8
            call Strain_CheckEvolution(udg_Strain_Hero[pId], pId)
            call DisplayTimedTextToPlayer(p, 0, 0, 4.0, "|cff00ff00[极速进化测试]|r 异种之源获得 +8 吞噬进度！累计: " + I2S(udg_Strain_DevourCount[pId]) + " 次")
        else
            call DisplayTimedTextToPlayer(p, 0, 0, 3.0, "|cffffcc00[极速进化测试]|r 未检测到异种之源英雄！")
        endif
    endif'''
    assert target_chat_cmds in content, "target_chat_cmds not found"
    content = content.replace(target_chat_cmds, repl_chat_cmds, 1)
    print("13 & 14. -spawn and -evo testing commands updated.")

    with open(jass_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"All v3.9 JASS modifications applied successfully! New length: {len(content)}")

if __name__ == '__main__':
    main()
