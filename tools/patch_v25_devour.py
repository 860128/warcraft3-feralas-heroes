import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JASS_PATH = os.path.join(ROOT, "payload", "war3map.j")
BUILD_OBJS_PATH = os.path.join(ROOT, "tools", "build_v13_objs.py")

# -------------------------------------------------------------
# 1. Update tools/build_v13_objs.py
# -------------------------------------------------------------
print("Updating tools/build_v13_objs.py...")
with open(BUILD_OBJS_PATH, "r", encoding="utf-8") as f:
    objs_content = f.read()

# Replace A022 in ini_ability
old_a022_pattern = re.compile(r'\[A022\][\s\S]*?(?=\[A023\])')
new_a022 = """[A022]
_parent = "ANcl"
Name = "捕食吞噬"
Hotkey = "W"
Researchhotkey = "W"
Buttonpos_1 = 1
Buttonpos_2 = 2
Researchbuttonpos_1 = 1
Researchbuttonpos_2 = 0
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Cost = {1 = 75, 2 = 75, 3 = 75}
Cool = {1 = 12.0, 2 = 10.0, 3 = 8.0}
Rng = {1 = 250.0, 2 = 275.0, 3 = 300.0}
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDevour.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNDevour.blp"
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "devour", 2 = "devour", 3 = "devour"}
Order = "devour"
targs = "air,ground,enemy,neutral,organic"
Researchtip = "学习 捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 %d|r]"
Researchubertip = "撕裂并吞噬生命值低于35%的非魔免单位（敌方英雄需低于28%），直接将其致死斩杀！|n吞噬后进入消化期，消化完成后恢复25%生命与法力，并根据猎物类型获得永久属性进化：|n- |cff00ff80近战小兵|r：永久增加最大生命值|n- |cffff6600远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff魔法单位(有魔法)|r：永久增加最大法力值|n- |cffffcc00敌方英雄(顶端掠食)|r：永久夺取 4 点敏捷属性，并从其 4 个技能中任选 1 个掠夺！"
Tip = {
1 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 1|r]",
2 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 2|r]",
3 = "捕食吞噬(|cffffcc00W|r) - [|cffffcc00等级 3|r]",
}
Ubertip = {
1 = "撕裂并吞噬射程250码内生命值低于35%的非魔免单位（敌方英雄需低于28%），直接斩杀！|n吞噬后进入6.5秒消化期，消化完成后恢复25%生命/法力，解锁受害者的【拟态伪装】，并根据猎物类型获得永久属性进化：|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值（基础+30，每级+10）|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值（基础+25，每级+5）|n- |cffffcc00吞噬敌方英雄|r：永久夺取 4 点主属性，并4选1掠夺其英雄技能！",
2 = "撕裂并吞噬射程275码内生命值低于35%的非魔免单位（敌方英雄需低于28%），直接斩杀！|n吞噬后进入5.0秒消化期，消化完成后恢复25%生命/法力，解锁受害者的【拟态伪装】，并根据猎物类型获得永久属性进化：|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值（基础+30，每级+10）|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值（基础+25，每级+5）|n- |cffffcc00吞噬敌方英雄|r：永久夺取 4 点主属性，并4选1掠夺其英雄技能！",
3 = "撕裂并吞噬射程300码内生命值低于35%的非魔免单位（敌方英雄需低于28%），直接斩杀！|n吞噬后进入3.5秒消化期，消化完成后恢复25%生命/法力，解锁受害者的【拟态伪装】，并根据猎物类型获得永久属性进化：|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值（基础+30，每级+10）|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值（基础+25，每级+5）|n- |cffffcc00吞噬敌方英雄|r：永久夺取 4 点主属性，并4选1掠夺其英雄技能！",
}

"""

objs_content, count_a022 = old_a022_pattern.subn(lambda m: new_a022, objs_content)
print(f"Replaced A022 count: {count_a022}")

# Replace A024 in ini_ability
old_a024_pattern = re.compile(r'\[A024\][\s\S]*?(?=\[A025\])')
new_a024 = """[A024]
_parent = "ANcl"
Name = "异种进化：基因掠夺"
Hotkey = "R"
Researchhotkey = "R"
Buttonpos_1 = 3
Buttonpos_2 = 2
Researchbuttonpos_1 = 3
Researchbuttonpos_2 = 0
levels = 1
hero = 1
reqLevel = 1
Cost = 0
Cool = 1.0
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNLocustSwarm.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNLocustSwarm.blp"
DataA = 0.0
DataB = 0
DataC = 1
DataD = 0.0
DataE = 0
DataF = "ancestralspirit"
Order = "ancestralspirit"
Researchtip = "学习 异种进化：基因掠夺(|cffffcc00R|r)"
Researchubertip = "点击呼出【异种进化与基因控制台】，实时查看吞噬小兵累计进化的生命、攻击、法力属性，以及管理掠夺的敌方英雄技能！|n- |cff00ff80吞噬近战小兵|r：永久增加最大生命值|n- |cffff6600吞噬远程小兵(无魔法)|r：永久增加 1~2 点基础攻击力|n- |cff33ccff吞噬魔法单位(有魔法)|r：永久增加最大法力值|n- |cffffcc00吞噬敌方英雄(Apex Harvest)|r：永久夺取 4 点敏捷属性，并4选1掠夺其英雄技能；重复吞噬敌方英雄可叠加【基因超载】层数强化技能，释放技能时触发酸液爆发与法力返还！"
Tip = "异种进化：基因掠夺(|cffffcc00R|r)"
Ubertip = "点击打开【异种进化控制台】：查看当前吞噬累计增加的生命值、基础攻击力与最大法力值，以及保留或遗忘已掠夺的敌方英雄技能。|n- |cff00ff80近战小兵|r：永久提升最大生命值|n- |cffff6600远程小兵(无魔法)|r：永久提升 1~2 点基础攻击力|n- |cff33ccff魔法单位(有魔法)|r：永久提升最大法力值|n- |cffffcc00敌方英雄|r：永久夺取 4 点敏捷属性 + 4选1掠夺技能 + 基因超载强化！"

"""

objs_content, count_a024 = old_a024_pattern.subn(lambda m: new_a024, objs_content)
print(f"Replaced A024 count: {count_a024}")

# Replace H004 Ubertip in ini_unit
old_h004_ubertip_pattern = re.compile(r'Ubertip = "来自远古地底的终极捕食者与欺诈潜伏者。擅长极速潜地突袭[\s\S]*?(?=Revivetip)')
new_h004_ubertip = """Ubertip = "来自远古地底的终极捕食者与欺诈潜伏者。擅长极速潜地突袭、斩杀吞噬残血猎物并获得永久生命/攻击/法力进化、拟态伪装成受害者混入敌阵，并通过基因掠夺夺取敌方英雄的核心技能！|n|n|cffffcc00技能：|r|n- 渊潜掠影 (Q)|n- 捕食吞噬 (W)|n- 拟态伪装 (E)|n- 异种进化：基因掠夺 (R)"\n"""
objs_content, count_h004 = old_h004_ubertip_pattern.subn(lambda m: new_h004_ubertip, objs_content)
print(f"Replaced H004 count: {count_h004}")

with open(BUILD_OBJS_PATH, "w", encoding="utf-8") as f:
    f.write(objs_content)
print("Updated tools/build_v13_objs.py successfully.")

# -------------------------------------------------------------
# 2. Update payload/war3map.j
# -------------------------------------------------------------
print("\nUpdating payload/war3map.j...")
with open(JASS_PATH, "r", encoding="utf-8") as f:
    jass = f.read()

# 2.1 Add globals
globals_anchor = "    effect array udg_Strain_DigestFx\n"
new_globals = """    effect array udg_Strain_DigestFx
    integer array udg_Strain_DigestFeedType // 1 = Melee (HP), 2 = Ranged No-Mana (Atk), 3 = Mana Unit (Mana)
    integer array udg_Strain_DigestVictimLv
    integer array udg_Strain_TotalBonusHP
    integer array udg_Strain_TotalBonusAtk
    integer array udg_Strain_TotalBonusMana
"""
assert globals_anchor in jass, "globals_anchor not found!"
jass = jass.replace(globals_anchor, new_globals, 1)
print("Added globals successfully.")

# 2.2 Update Strain_Unburrow move speed reset
old_unburrow_speed = """    if udg_Strain_GeneCat[pId] == 1 and udg_Strain_EvoTier[pId] >= 2 then
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 65.0)
    elseif udg_Strain_GeneCat[pId] == 3 and udg_Strain_EvoTier[pId] >= 2 then
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u) + 60.0)
    else
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))
    endif"""
new_unburrow_speed = """    call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))"""
assert old_unburrow_speed in jass, "old_unburrow_speed not found!"
jass = jass.replace(old_unburrow_speed, new_unburrow_speed, 1)
print("Updated Strain_Unburrow successfully.")

# 2.3 Update Strain_ClearCurrentGene
clear_gene_pattern = re.compile(r'function Strain_ClearCurrentGene takes unit u, integer pId returns nothing[\s\S]*?endfunction')
new_clear_gene = r"""function Strain_ClearCurrentGene takes unit u, integer pId returns nothing
    if u != null then
        call UnitRemoveAbility(u, 'A025')
        call UnitRemoveAbility(u, 'A026')
        if udg_Strain_StolenHeroAbil[pId] != 0 then
            call UnitRemoveAbility(u, udg_Strain_StolenHeroAbil[pId])
        endif
        call SetUnitMoveSpeed(u, GetUnitDefaultMoveSpeed(u))
        call SetUnitScale(u, 1.25, 1.25, 1.25)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\DispelMagic\\DispelMagicTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 3.0, "|cffffcc00[异种进化]|r 已遗忘当前掠夺的英雄技能！")
    endif
    set udg_Strain_GeneCat[pId] = 0
    set udg_Strain_EvoTier[pId] = 0
    set udg_Strain_StolenHeroAbil[pId] = 0
endfunction"""

jass, count_cg = clear_gene_pattern.subn(lambda m: new_clear_gene, jass, count=1)
assert count_cg == 1, f"clear_gene_pattern matched {count_cg} times!"
print("Updated Strain_ClearCurrentGene successfully.")

# 2.4 Update Strain_ShowGeneDialog
gene_dialog_pattern = re.compile(r'function Strain_ShowGeneDialog takes player p, integer pId returns nothing[\s\S]*?endfunction')
new_gene_dialog = r"""function Strain_ShowGeneDialog takes player p, integer pId returns nothing
    local string msg = "【异种之源 - 进化控制台】"
    if p == null then
        return
    endif
    set msg = msg + "\n累计进化：+" + I2S(udg_Strain_TotalBonusHP[pId]) + "生命 / +" + I2S(udg_Strain_TotalBonusAtk[pId]) + "攻击 / +" + I2S(udg_Strain_TotalBonusMana[pId]) + "法力"
    if udg_Strain_StolenHeroAbil[pId] != 0 then
        set msg = msg + "\n当前掠夺英雄技能：" + GetObjectName(udg_Strain_StolenHeroAbil[pId]) + " (强化 " + I2S(udg_Strain_EvoTier[pId]) + " 阶)"
    else
        set msg = msg + "\n当前掠夺英雄技能：无（吞噬敌方英雄可掠夺技能）"
    endif
    call DialogDisplay(p, udg_Strain_GeneDialog, false)
    call DialogClear(udg_Strain_GeneDialog)
    call DialogSetMessage(udg_Strain_GeneDialog, msg)
    set udg_Strain_BtnKeep = DialogAddButton(udg_Strain_GeneDialog, "[1] 保留当前技能与属性 (确认)", 49)
    set udg_Strain_BtnDiscard = DialogAddButton(udg_Strain_GeneDialog, "[2] 遗忘掠夺的英雄技能 (腾出技能槽)", 50)
    call DialogDisplay(p, udg_Strain_GeneDialog, true)
endfunction"""

jass, count_gd = gene_dialog_pattern.subn(lambda m: new_gene_dialog, jass, count=1)
assert count_gd == 1, f"gene_dialog_pattern matched {count_gd} times!"
print("Updated Strain_ShowGeneDialog successfully.")

# 2.5 Update Strain_OnDigestComplete
digest_complete_pattern = re.compile(r'function Strain_OnDigestComplete takes unit u, integer pId returns nothing[\s\S]*?endfunction')
new_digest_complete = r"""function Strain_OnDigestComplete takes unit u, integer pId returns nothing
    local integer tgtType = 0
    local integer bonusHP = 0
    local integer bonusAtk = 0
    local integer bonusMana = 0
    if u == null then
        return
    endif
    set tgtType = udg_Strain_DigestType[pId]

    if udg_Strain_DigestIsHero[pId] then
        // Apex Harvest: Hero Devoured!
        call SetHeroAgi(u, GetHeroAgi(u, false) + 4, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Items\\AIam\\AIamTarget.mdl", u, "origin"))
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff00ff00[顶端掠食]|r 成功吞噬敌方英雄，永久夺取 +4 点敏捷！")

        if tgtType == 'H002' then
            set udg_Strain_CandidateAbil0[pId] = 'A001'
            set udg_Strain_CandidateAbil1[pId] = 'A002'
            set udg_Strain_CandidateAbil2[pId] = 'A003'
            set udg_Strain_CandidateAbil3[pId] = 'A004'
        elseif tgtType == 'H003' then
            set udg_Strain_CandidateAbil0[pId] = 'A011'
            set udg_Strain_CandidateAbil1[pId] = 'A012'
            set udg_Strain_CandidateAbil2[pId] = 'A013'
            set udg_Strain_CandidateAbil3[pId] = 'A014'
        elseif tgtType == 'Hamg' then
            set udg_Strain_CandidateAbil0[pId] = 'AHbz'
            set udg_Strain_CandidateAbil1[pId] = 'AHwe'
            set udg_Strain_CandidateAbil2[pId] = 'AHab'
            set udg_Strain_CandidateAbil3[pId] = 'AHmt'
        elseif tgtType == 'Hmkg' then
            set udg_Strain_CandidateAbil0[pId] = 'AHtb'
            set udg_Strain_CandidateAbil1[pId] = 'AHtc'
            set udg_Strain_CandidateAbil2[pId] = 'AHbh'
            set udg_Strain_CandidateAbil3[pId] = 'AHav'
        elseif tgtType == 'Hpal' then
            set udg_Strain_CandidateAbil0[pId] = 'AHhb'
            set udg_Strain_CandidateAbil1[pId] = 'AHds'
            set udg_Strain_CandidateAbil2[pId] = 'AHad'
            set udg_Strain_CandidateAbil3[pId] = 'AHre'
        elseif tgtType == 'Hblm' then
            set udg_Strain_CandidateAbil0[pId] = 'AHfs'
            set udg_Strain_CandidateAbil1[pId] = 'AHbn'
            set udg_Strain_CandidateAbil2[pId] = 'AHdr'
            set udg_Strain_CandidateAbil3[pId] = 'AHpx'
        elseif tgtType == 'Obla' then
            set udg_Strain_CandidateAbil0[pId] = 'AOwk'
            set udg_Strain_CandidateAbil1[pId] = 'AOmi'
            set udg_Strain_CandidateAbil2[pId] = 'AOcr'
            set udg_Strain_CandidateAbil3[pId] = 'AOww'
        elseif tgtType == 'Ofar' then
            set udg_Strain_CandidateAbil0[pId] = 'AOcl'
            set udg_Strain_CandidateAbil1[pId] = 'AOfs'
            set udg_Strain_CandidateAbil2[pId] = 'AOsf'
            set udg_Strain_CandidateAbil3[pId] = 'AOeq'
        elseif tgtType == 'Otch' then
            set udg_Strain_CandidateAbil0[pId] = 'AOsh'
            set udg_Strain_CandidateAbil1[pId] = 'AOws'
            set udg_Strain_CandidateAbil2[pId] = 'AOae'
            set udg_Strain_CandidateAbil3[pId] = 'AOre'
        elseif tgtType == 'Oshd' then
            set udg_Strain_CandidateAbil0[pId] = 'AOhw'
            set udg_Strain_CandidateAbil1[pId] = 'AOhx'
            set udg_Strain_CandidateAbil2[pId] = 'AOsw'
            set udg_Strain_CandidateAbil3[pId] = 'AOvd'
        elseif tgtType == 'Edem' then
            set udg_Strain_CandidateAbil0[pId] = 'AEmb'
            set udg_Strain_CandidateAbil1[pId] = 'AEim'
            set udg_Strain_CandidateAbil2[pId] = 'AEev'
            set udg_Strain_CandidateAbil3[pId] = 'AEme'
        elseif tgtType == 'Ekee' then
            set udg_Strain_CandidateAbil0[pId] = 'AEer'
            set udg_Strain_CandidateAbil1[pId] = 'AEfn'
            set udg_Strain_CandidateAbil2[pId] = 'AEah'
            set udg_Strain_CandidateAbil3[pId] = 'AEtq'
        elseif tgtType == 'Emoo' then
            set udg_Strain_CandidateAbil0[pId] = 'AHfa'
            set udg_Strain_CandidateAbil1[pId] = 'AEst'
            set udg_Strain_CandidateAbil2[pId] = 'AEar'
            set udg_Strain_CandidateAbil3[pId] = 'AEsf'
        elseif tgtType == 'Ewar' then
            set udg_Strain_CandidateAbil0[pId] = 'AEfk'
            set udg_Strain_CandidateAbil1[pId] = 'AEbl'
            set udg_Strain_CandidateAbil2[pId] = 'AEsh'
            set udg_Strain_CandidateAbil3[pId] = 'AEsv'
        elseif tgtType == 'Udea' then
            set udg_Strain_CandidateAbil0[pId] = 'AUdc'
            set udg_Strain_CandidateAbil1[pId] = 'AUdp'
            set udg_Strain_CandidateAbil2[pId] = 'AUau'
            set udg_Strain_CandidateAbil3[pId] = 'AUan'
        elseif tgtType == 'Ulic' then
            set udg_Strain_CandidateAbil0[pId] = 'AUfn'
            set udg_Strain_CandidateAbil1[pId] = 'AUfu'
            set udg_Strain_CandidateAbil2[pId] = 'AUdr'
            set udg_Strain_CandidateAbil3[pId] = 'AUdd'
        elseif tgtType == 'Udre' then
            set udg_Strain_CandidateAbil0[pId] = 'AUcs'
            set udg_Strain_CandidateAbil1[pId] = 'AUsl'
            set udg_Strain_CandidateAbil2[pId] = 'AUva'
            set udg_Strain_CandidateAbil3[pId] = 'AUin'
        else
            set udg_Strain_CandidateAbil0[pId] = 'AUim'
            set udg_Strain_CandidateAbil1[pId] = 'AUts'
            set udg_Strain_CandidateAbil2[pId] = 'AUcb'
            set udg_Strain_CandidateAbil3[pId] = 'AUls'
        endif

        if GetPlayerController(GetOwningPlayer(u)) == MAP_CONTROL_USER then
            call Strain_ShowHeroSkillDialog(GetOwningPlayer(u), pId)
        else
            call Strain_ApplyStolenHeroSkill(u, pId, udg_Strain_CandidateAbil0[pId])
        endif
    else
        // Non-Hero unit: Creep, Lane unit, Summon Devoured!
        if udg_Strain_DigestFeedType[pId] == 1 then
            // Case C: Melee Unit without Mana -> Permanent Max HP bonus
            set bonusHP = 30 + 10 * udg_Strain_DigestVictimLv[pId]
            call BlzSetUnitMaxHP(u, BlzGetUnitMaxHP(u) + bonusHP)
            call SetWidgetLife(u, GetWidgetLife(u) + I2R(bonusHP))
            set udg_Strain_TotalBonusHP[pId] = udg_Strain_TotalBonusHP[pId] + bonusHP
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff00ff80[吞噬进化-近战猎物]|r 永久增加 " + I2S(bonusHP) + " 点最大生命值！（累计+" + I2S(udg_Strain_TotalBonusHP[pId]) + "生命）")
        elseif udg_Strain_DigestFeedType[pId] == 2 then
            // Case B: Ranged Unit without Mana -> Permanent Base Attack bonus (+1~2)
            if udg_Strain_DigestVictimLv[pId] <= 1 then
                set bonusAtk = 1
            else
                set bonusAtk = 2
            endif
            call BlzSetUnitBaseDamage(u, BlzGetUnitBaseDamage(u, 0) + bonusAtk, 0)
            set udg_Strain_TotalBonusAtk[pId] = udg_Strain_TotalBonusAtk[pId] + bonusAtk
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cffff6600[吞噬进化-远程猎物]|r 永久增加 " + I2S(bonusAtk) + " 点基础攻击力！（累计+" + I2S(udg_Strain_TotalBonusAtk[pId]) + "攻击）")
        else
            // Case A: Magical Unit -> Permanent Max Mana bonus
            set bonusMana = 25 + 5 * udg_Strain_DigestVictimLv[pId]
            call BlzSetUnitMaxMana(u, BlzGetUnitMaxMana(u) + bonusMana)
            call SetUnitState(u, UNIT_STATE_MANA, GetUnitState(u, UNIT_STATE_MANA) + I2R(bonusMana))
            set udg_Strain_TotalBonusMana[pId] = udg_Strain_TotalBonusMana[pId] + bonusMana
            call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 4.0, "|cff33ccff[吞噬进化-魔法猎物]|r 永久增加 " + I2S(bonusMana) + " 点最大法力值！（累计+" + I2S(udg_Strain_TotalBonusMana[pId]) + "法力）")
        endif
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Items\\AIam\\AIamTarget.mdl", u, "origin"))
    endif
endfunction"""

jass, count_dc = digest_complete_pattern.subn(lambda m: new_digest_complete, jass, count=1)
assert count_dc == 1, f"digest_complete_pattern matched {count_dc} times!"
print("Updated Strain_OnDigestComplete successfully.")

# 2.6 Record unit type category in DM_OnSpellEffect (abil == 'A022')
old_spell_a022 = """            set udg_Strain_DigestType[pId] = GetUnitTypeId(ult)
            set udg_Strain_DigestOwner[pId] = GetOwningPlayer(ult)
            set udg_Strain_DigestIsHero[pId] = IsUnitType(ult, UNIT_TYPE_HERO) or IsHeroUnitId(GetUnitTypeId(ult))
            set udg_Strain_DigestTimer[pId] = 8.0 - 1.5 * I2R(GetUnitAbilityLevel(caster, 'A022'))"""

new_spell_a022 = """            set udg_Strain_DigestType[pId] = GetUnitTypeId(ult)
            set udg_Strain_DigestOwner[pId] = GetOwningPlayer(ult)
            set udg_Strain_DigestIsHero[pId] = IsUnitType(ult, UNIT_TYPE_HERO) or IsHeroUnitId(GetUnitTypeId(ult))
            set udg_Strain_DigestVictimLv[pId] = IMaxBJ(1, GetUnitLevel(ult))
            if not udg_Strain_DigestIsHero[pId] then
                if GetUnitState(ult, UNIT_STATE_MAX_MANA) > 0.5 then
                    set udg_Strain_DigestFeedType[pId] = 3
                elseif IsUnitType(ult, UNIT_TYPE_RANGED_ATTACKER) then
                    set udg_Strain_DigestFeedType[pId] = 2
                else
                    set udg_Strain_DigestFeedType[pId] = 1
                endif
            else
                set udg_Strain_DigestFeedType[pId] = 0
            endif
            set udg_Strain_DigestTimer[pId] = 8.0 - 1.5 * I2R(GetUnitAbilityLevel(caster, 'A022'))"""

assert old_spell_a022 in jass, "old_spell_a022 not found!"
jass = jass.replace(old_spell_a022, new_spell_a022, 1)
print("Updated DM_OnSpellEffect A022 handling successfully.")

# 2.7 Update TM_SpawnSandboxTargets to spawn the 4 test types
sandbox_pattern = re.compile(r'function TM_SpawnSandboxTargets takes player p returns nothing[\s\S]*?endfunction')
new_sandbox = r"""function TM_SpawnSandboxTargets takes player p returns nothing
    local group g = CreateGroup()
    local unit u = null
    local real hx = 0.0
    local real hy = 0.0
    local unit targetU = null

    if p == null then
        return
    endif

    call GroupEnumUnitsOfPlayer(g, p, null)
    loop
        set u = FirstOfGroup(g)
        exitwhen u == null
        call GroupRemoveUnit(g, u)
        if IsUnitType(u, UNIT_TYPE_HERO) and not IsUnitIllusion(u) and not IsUnitInGroup(u, udg_FakeHeroGroup) then
            set hx = GetUnitX(u)
            set hy = GetUnitY(u)
            set u = null
            exitwhen true
        endif
    endloop
    call DestroyGroup(g)
    set g = null

    if hx == 0.0 and hy == 0.0 then
        set hx = GetStartLocationX(GetPlayerStartLocation(p))
        set hy = GetStartLocationY(GetPlayerStartLocation(p))
    endif

    // 1. Footman (hfoo) - Melee, no mana -> +HP
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'hfoo', hx + 180.0, hy + 60.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 2. Archer (earc) - Ranged attacker, no mana -> +Attack
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'earc', hx + 180.0, hy + 180.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 3. Shaman (oshm) - Magical caster, has mana -> +Mana
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'oshm', hx + 180.0, hy - 60.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    // 4. Blademaster (Obla) - Hero devour -> +4 Agi & 4-skill steal
    set targetU = CreateUnit(Player(PLAYER_NEUTRAL_AGGRESSIVE), 'Obla', hx + 180.0, hy - 180.0, 180.0)
    call SetWidgetLife(targetU, GetUnitState(targetU, UNIT_STATE_MAX_LIFE) * 0.20)
    call PauseUnit(targetU, true)

    set targetU = null
    call DisplayTimedTextToPlayer(p, 0, 0, 8.0, "|cff00ff00[沙盒测试]|r 已生成4个20%残血测试靶子（步兵[近战+血]/弓手[远程+攻]/萨满[魔法+蓝]/剑圣[英雄]），可直接用W【捕食吞噬】测试进化！")
endfunction"""

jass, count_sb = sandbox_pattern.subn(lambda m: new_sandbox, jass, count=1)
assert count_sb == 1, f"sandbox_pattern matched {count_sb} times!"
print("Updated TM_SpawnSandboxTargets successfully.")

# 2.8 Initialize new globals in init loop
old_init_loop = """        set udg_Strain_Burrowed[i] = false
        set udg_Strain_BurrowTimer[i] = 0.0
        set udg_Strain_DigestTimer[i] = 0.0"""

new_init_loop = """        set udg_Strain_Burrowed[i] = false
        set udg_Strain_BurrowTimer[i] = 0.0
        set udg_Strain_DigestTimer[i] = 0.0
        set udg_Strain_DigestFeedType[i] = 0
        set udg_Strain_DigestVictimLv[i] = 1
        set udg_Strain_TotalBonusHP[i] = 0
        set udg_Strain_TotalBonusAtk[i] = 0
        set udg_Strain_TotalBonusMana[i] = 0"""

assert old_init_loop in jass, "old_init_loop not found!"
jass = jass.replace(old_init_loop, new_init_loop, 1)
print("Updated variable initialization loop successfully.")

with open(JASS_PATH, "w", encoding="utf-8") as f:
    f.write(jass)
print("payload/war3map.j written successfully.")
