import os

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
JASS_PATH = os.path.join(ROOT, "payload", "war3map.j")

with open(JASS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update globals: add button udg_TM_SlotBack = null
old_glob = """    dialog udg_TM_SlotDialog = null
    button array udg_TM_SlotBtn
    button udg_TM_SlotConfirm = null"""

new_glob = """    dialog udg_TM_SlotDialog = null
    button array udg_TM_SlotBtn
    button udg_TM_SlotConfirm = null
    button udg_TM_SlotBack = null"""

assert old_glob in content, "old_glob not found"
content = content.replace(old_glob, new_glob, 1)

# 2. Update TM Dialog functions
old_funcs = """function TM_ShowSlotDialog takes player p returns nothing
    local integer i = 0
    local string lbl = ""
    set udg_TM_PromptPlayer = p
    call DialogClear(udg_TM_SlotDialog)
    call DialogSetMessage(udg_TM_SlotDialog, "点击切换各电脑英雄（确认后生效）")
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] == 1 then
                set lbl = "电脑 " + I2S(i + 1) + "：【幻梦大师】 (点击切换)"
            elseif udg_AI_HeroMode[i] == 2 then
                set lbl = "电脑 " + I2S(i + 1) + "：【魔音忍者】 (点击切换)"
            else
                set lbl = "电脑 " + I2S(i + 1) + "：原版默认英雄 (点击切换)"
            endif
            set udg_TM_SlotBtn[i] = DialogAddButton(udg_TM_SlotDialog, lbl, 0)
        else
            set udg_TM_SlotBtn[i] = null
        endif
        set i = i + 1
    endloop
    set udg_TM_SlotConfirm = DialogAddButton(udg_TM_SlotDialog, "【确认配置并开始】", 0)
    call DialogDisplay(p, udg_TM_SlotDialog, true)
endfunction

function TM_ShowMainDialog takes player p returns nothing
    set udg_TM_PromptPlayer = p
    call DialogDisplay(p, udg_TM_MainDialog, true)
endfunction

function TM_OnMainDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if b == udg_TM_BtnNormal then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 0
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 已选择正常模式：所有电脑使用原版默认英雄。")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode1All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 已选择测试模式一：全部电脑出【幻梦大师】！")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode2All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 2
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 已选择测试模式二：全部电脑出【魔音忍者】！")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnCustom then
        call TM_ShowSlotDialog(p)
    endif

    set b = null
    set p = null
endfunction

function TM_OnSlotDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if b == udg_TM_SlotConfirm then
        call DisplayTimedTextToPlayer(p, 0, 0, 5.0, "|cff00ff00[测试模式]|r 电脑英雄精细配置已确认并生效！")
        call TM_ApplyAIConfig()
    else
        set i = 0
        loop
            exitwhen i > 7
            if b == udg_TM_SlotBtn[i] then
                if udg_AI_HeroMode[i] == 0 then
                    set udg_AI_HeroMode[i] = 1
                elseif udg_AI_HeroMode[i] == 1 then
                    set udg_AI_HeroMode[i] = 2
                else
                    set udg_AI_HeroMode[i] = 0
                endif
                call TM_ShowSlotDialog(p)
                set b = null
                set p = null
                return
            endif
            set i = i + 1
        endloop
    endif

    set b = null
    set p = null
endfunction

function TM_GetFirstHumanPlayer takes nothing returns player
    local integer i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER then
            return Player(i)
        endif
        set i = i + 1
    endloop
    return null
endfunction

function TM_OnStartTimer takes nothing returns nothing
    local player p = TM_GetFirstHumanPlayer()
    if p != null then
        call TM_ShowMainDialog(p)
    endif
    set p = null
    call DestroyTimer(GetExpiredTimer())
endfunction"""

new_funcs = """function TM_ShowMainDialog takes player p returns nothing
    if p == null then
        return
    endif
    set udg_TM_PromptPlayer = p
    call DialogDisplay(p, udg_TM_MainDialog, false)
    call DialogClear(udg_TM_MainDialog)
    call DialogSetMessage(udg_TM_MainDialog, "【测试模式选择】(鼠标点击或按数字键1-4)")
    set udg_TM_BtnNormal = DialogAddButton(udg_TM_MainDialog, "[1] 正常模式：电脑使用原版随机英雄", 49)
    set udg_TM_BtnMode1All = DialogAddButton(udg_TM_MainDialog, "[2] 测试模式一：全部电脑出【幻梦大师】", 50)
    set udg_TM_BtnMode2All = DialogAddButton(udg_TM_MainDialog, "[3] 测试模式二：全部电脑出【魔音忍者】", 51)
    set udg_TM_BtnCustom = DialogAddButton(udg_TM_MainDialog, "[4] 精细配置：逐个指定各家电脑英雄...", 52)
    call DialogDisplay(p, udg_TM_MainDialog, true)
endfunction

function TM_ShowSlotDialog takes player p returns nothing
    local integer i = 0
    local string lbl = ""
    if p == null then
        return
    endif
    set udg_TM_PromptPlayer = p
    call DialogDisplay(p, udg_TM_SlotDialog, false)
    call DialogClear(udg_TM_SlotDialog)
    call DialogSetMessage(udg_TM_SlotDialog, "【精细配置】点击切换各电脑英雄 (确认后生效)")
    set i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
            if udg_AI_HeroMode[i] == 1 then
                set lbl = "电脑 " + I2S(i + 1) + "：【幻梦大师】 (点击切换)"
            elseif udg_AI_HeroMode[i] == 2 then
                set lbl = "电脑 " + I2S(i + 1) + "：【魔音忍者】 (点击切换)"
            else
                set lbl = "电脑 " + I2S(i + 1) + "：原版默认英雄 (点击切换)"
            endif
            set udg_TM_SlotBtn[i] = DialogAddButton(udg_TM_SlotDialog, lbl, 0)
        else
            set udg_TM_SlotBtn[i] = null
        endif
        set i = i + 1
    endloop
    set udg_TM_SlotConfirm = DialogAddButton(udg_TM_SlotDialog, "[9] 【确认配置并开始】", 57)
    set udg_TM_SlotBack = DialogAddButton(udg_TM_SlotDialog, "[0] 返回上一级菜单", 48)
    call DialogDisplay(p, udg_TM_SlotDialog, true)
endfunction

function TM_OnMainDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    call DialogDisplay(p, udg_TM_MainDialog, false)

    if b == udg_TM_BtnNormal then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 0
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置正常模式：电脑使用原版英雄 (可随时输入 -test 重新选择)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode1All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式一：全部电脑出【幻梦大师】！(可随时输入 -test 重新选择)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnMode2All then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 2
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式二：全部电脑出【魔音忍者】！(可随时输入 -test 重新选择)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_BtnCustom then
        call TM_ShowSlotDialog(p)
    endif

    set b = null
    set p = null
endfunction

function TM_OnSlotDialogClicked takes nothing returns nothing
    local button b = GetClickedButton()
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if b == udg_TM_SlotConfirm then
        call DialogDisplay(p, udg_TM_SlotDialog, false)
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 电脑英雄精细配置已生效！(可随时输入 -test 重新配置)")
        call TM_ApplyAIConfig()
    elseif b == udg_TM_SlotBack then
        call DialogDisplay(p, udg_TM_SlotDialog, false)
        call TM_ShowMainDialog(p)
    else
        set i = 0
        loop
            exitwhen i > 7
            if b == udg_TM_SlotBtn[i] then
                if udg_AI_HeroMode[i] == 0 then
                    set udg_AI_HeroMode[i] = 1
                elseif udg_AI_HeroMode[i] == 1 then
                    set udg_AI_HeroMode[i] = 2
                else
                    set udg_AI_HeroMode[i] = 0
                endif
                call TM_ShowSlotDialog(p)
                set b = null
                set p = null
                return
            endif
            set i = i + 1
        endloop
    endif

    set b = null
    set p = null
endfunction

function TM_OnChatCommand takes nothing returns nothing
    local string s = StringCase(GetEventPlayerChatString(), false)
    local player p = GetTriggerPlayer()
    local integer i = 0
    if p == null then
        set p = udg_TM_PromptPlayer
    endif

    if s == "-test" or s == "-mode" then
        call TM_ShowMainDialog(p)
    elseif s == "-m0" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 0
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置正常模式：所有电脑使用原版默认英雄。")
        call TM_ApplyAIConfig()
    elseif s == "-m1" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 1
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式一：全部电脑出【幻梦大师】！")
        call TM_ApplyAIConfig()
    elseif s == "-m2" then
        set i = 0
        loop
            exitwhen i > 7
            if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_COMPUTER then
                set udg_AI_HeroMode[i] = 2
            endif
            set i = i + 1
        endloop
        call DisplayTimedTextToPlayer(p, 0, 0, 6.0, "|cff00ff00[测试模式]|r 已设置测试模式二：全部电脑出【魔音忍者】！")
        call TM_ApplyAIConfig()
    endif

    set p = null
endfunction

function TM_GetFirstHumanPlayer takes nothing returns player
    local integer i = 0
    loop
        exitwhen i > 7
        if GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER then
            return Player(i)
        endif
        set i = i + 1
    endloop
    return null
endfunction

function TM_OnStartTimer takes nothing returns nothing
    local timer t = GetExpiredTimer()
    local player p = TM_GetFirstHumanPlayer()
    call PauseTimer(t)
    call DestroyTimer(t)
    set t = null
    if p != null then
        call TM_ShowMainDialog(p)
    endif
    set p = null
endfunction"""

assert old_funcs in content, "old_funcs not found"
content = content.replace(old_funcs, new_funcs, 1)

# 3. Update DM_InitTriggers
old_init = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tSkill = CreateTrigger()
    local trigger tTrain = CreateTrigger()
    local trigger tMainDialog = CreateTrigger()
    local trigger tSlotDialog = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()
    local timer tmrStart = CreateTimer()
    local integer i = 0

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()

    set i = 0
    loop
        exitwhen i > 15
        set udg_Ninja_CloneGroup[i] = CreateGroup()
        set udg_Ninja_AuraOn[i] = false
        set udg_Ninja_AuraFx[i] = null
        set udg_Ninja_TrueHero[i] = null

        // Initialize AI variables
        set udg_AI_HeroMode[i] = 0
        set udg_AI_CustomHero[i] = null
        set udg_AI_HeroSpawned[i] = false
        set udg_AI_CastCD_Q[i] = 0.0
        set udg_AI_CastCD_W[i] = 0.0
        set udg_AI_CastCD_E[i] = 0.0
        set udg_AI_CastCD_R[i] = 0.0
        set udg_AI_DeadTimer[i] = 0.0
        set udg_AI_AltarTimer[i] = 0.0
        set udg_AI_WaitTimer[i] = 0.0
        set udg_TM_SlotBtn[i] = null
        set i = i + 1
    endloop

    // Initialize Test Mode Dialogs
    set udg_TM_MainDialog = DialogCreate()
    call DialogSetMessage(udg_TM_MainDialog, "【测试模式选择】(可扩展AI测试框架)")
    set udg_TM_BtnNormal = DialogAddButton(udg_TM_MainDialog, "正常模式：电脑使用原版随机英雄", 0)
    set udg_TM_BtnMode1All = DialogAddButton(udg_TM_MainDialog, "测试模式一：全部电脑出【幻梦大师】", 0)
    set udg_TM_BtnMode2All = DialogAddButton(udg_TM_MainDialog, "测试模式二：全部电脑出【魔音忍者】", 0)
    set udg_TM_BtnCustom = DialogAddButton(udg_TM_MainDialog, "精细配置：逐个指定各家电脑出什么英雄...", 0)

    set udg_TM_SlotDialog = DialogCreate()

    call TriggerRegisterDialogEvent(tMainDialog, udg_TM_MainDialog)
    call TriggerAddAction(tMainDialog, function TM_OnMainDialogClicked)

    call TriggerRegisterDialogEvent(tSlotDialog, udg_TM_SlotDialog)
    call TriggerAddAction(tSlotDialog, function TM_OnSlotDialogClicked)

    call TriggerRegisterAnyUnitEventBJ(tEffect, EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddCondition(tEffect, Condition(function DM_OnSpellEffect))

    call TriggerRegisterAnyUnitEventBJ(tCast, EVENT_PLAYER_UNIT_SPELL_CAST)
    call TriggerAddCondition(tCast, Condition(function DM_OnSpellCast))

    call TriggerRegisterAnyUnitEventBJ(tDeath, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddCondition(tDeath, Condition(function DM_OnUnitDeath))

    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))

    call TriggerRegisterAnyUnitEventBJ(tDamage, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))

    call TriggerRegisterAnyUnitEventBJ(tSkill, EVENT_PLAYER_HERO_SKILL)
    call TriggerAddCondition(tSkill, Condition(function Ninja_OnHeroSkill))

    call TriggerRegisterAnyUnitEventBJ(tTrain, EVENT_PLAYER_UNIT_TRAIN_FINISH)
    call TriggerAddCondition(tTrain, Condition(function AI_OnUnitTrainFinish))

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)
    call TimerStart(tmrStart, 0.50, false, function TM_OnStartTimer)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tSkill = null
    set tTrain = null
    set tMainDialog = null
    set tSlotDialog = null
    set tmrCap = null
    set tmrStealth = null
    set tmrStart = null
endfunction"""

new_init = """function DM_InitTriggers takes nothing returns nothing
    local trigger tEffect = CreateTrigger()
    local trigger tCast = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tRevive = CreateTrigger()
    local trigger tSkill = CreateTrigger()
    local trigger tTrain = CreateTrigger()
    local trigger tMainDialog = CreateTrigger()
    local trigger tSlotDialog = CreateTrigger()
    local trigger tChat = CreateTrigger()
    local timer tmrCap = CreateTimer()
    local timer tmrStealth = CreateTimer()
    local timer tmrStart = CreateTimer()
    local integer i = 0

    set udg_EnumGroup = CreateGroup()
    set udg_FakeHeroGroup = CreateGroup()

    set i = 0
    loop
        exitwhen i > 15
        set udg_Ninja_CloneGroup[i] = CreateGroup()
        set udg_Ninja_AuraOn[i] = false
        set udg_Ninja_AuraFx[i] = null
        set udg_Ninja_TrueHero[i] = null

        // Initialize AI variables
        set udg_AI_HeroMode[i] = 0
        set udg_AI_CustomHero[i] = null
        set udg_AI_HeroSpawned[i] = false
        set udg_AI_CastCD_Q[i] = 0.0
        set udg_AI_CastCD_W[i] = 0.0
        set udg_AI_CastCD_E[i] = 0.0
        set udg_AI_CastCD_R[i] = 0.0
        set udg_AI_DeadTimer[i] = 0.0
        set udg_AI_AltarTimer[i] = 0.0
        set udg_AI_WaitTimer[i] = 0.0
        set udg_TM_SlotBtn[i] = null
        set i = i + 1
    endloop

    // Initialize Test Mode Dialogs (Handles only - buttons added after game start to avoid click freeze)
    set udg_TM_MainDialog = DialogCreate()
    set udg_TM_SlotDialog = DialogCreate()

    call TriggerRegisterDialogEvent(tMainDialog, udg_TM_MainDialog)
    call TriggerAddAction(tMainDialog, function TM_OnMainDialogClicked)

    call TriggerRegisterDialogEvent(tSlotDialog, udg_TM_SlotDialog)
    call TriggerAddAction(tSlotDialog, function TM_OnSlotDialogClicked)

    set i = 0
    loop
        exitwhen i > 7
        call TriggerRegisterPlayerChatEvent(tChat, Player(i), "-", false)
        set i = i + 1
    endloop
    call TriggerAddAction(tChat, function TM_OnChatCommand)

    call TriggerRegisterAnyUnitEventBJ(tEffect, EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddCondition(tEffect, Condition(function DM_OnSpellEffect))

    call TriggerRegisterAnyUnitEventBJ(tCast, EVENT_PLAYER_UNIT_SPELL_CAST)
    call TriggerAddCondition(tCast, Condition(function DM_OnSpellCast))

    call TriggerRegisterAnyUnitEventBJ(tDeath, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddCondition(tDeath, Condition(function DM_OnUnitDeath))

    call TriggerRegisterAnyUnitEventBJ(tRevive, EVENT_PLAYER_HERO_REVIVABLE)
    call TriggerAddCondition(tRevive, Condition(function DM_OnHeroRevivable))

    call TriggerRegisterAnyUnitEventBJ(tDamage, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))

    call TriggerRegisterAnyUnitEventBJ(tSkill, EVENT_PLAYER_HERO_SKILL)
    call TriggerAddCondition(tSkill, Condition(function Ninja_OnHeroSkill))

    call TriggerRegisterAnyUnitEventBJ(tTrain, EVENT_PLAYER_UNIT_TRAIN_FINISH)
    call TriggerAddCondition(tTrain, Condition(function AI_OnUnitTrainFinish))

    call TimerStart(tmrCap, 1.0, true, function DM_CapTimerLoop)
    call TimerStart(tmrStealth, 0.05, true, function DM_StealthLoop)
    call TimerStart(tmrStart, 1.00, false, function TM_OnStartTimer)

    set tEffect = null
    set tCast = null
    set tDeath = null
    set tDamage = null
    set tRevive = null
    set tSkill = null
    set tTrain = null
    set tMainDialog = null
    set tSlotDialog = null
    set tChat = null
    set tmrCap = null
    set tmrStealth = null
    set tmrStart = null
endfunction"""

assert old_init in content, "old_init not found"
content = content.replace(old_init, new_init, 1)

with open(JASS_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully patched payload/war3map.j!")
