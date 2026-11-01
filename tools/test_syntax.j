globals
    unit array udg_CapUnit
    player array udg_CapOrigOwner
    real array udg_CapDuration
    unit array udg_CapCaster
    boolean array udg_CapIsHero
    boolean array udg_CapAghBuff
    integer udg_CapCount = 0
    group udg_EnumGroup = null
    group udg_CloneHeroGroup = null
    group udg_AghCloneGroup = null
    group udg_MirrorGroup = null
    unit array udg_DM_Hero
    boolean array udg_DM_Backstab
    integer udg_DM_HeroCount = 0
endglobals
//===========================================================================
// 幻梦大师 (Dream Master) - 全套技能系统 JASS 核心实现
//===========================================================================

// 全局变量声明应注入到 globals ... endglobals 之间：
//
//     unit array udg_CapUnit
//     player array udg_CapOrigOwner
//     real array udg_CapDuration
//     unit array udg_CapCaster
//     boolean array udg_CapIsHero
//     boolean array udg_CapAghBuff
//     integer udg_CapCount = 0
//     group udg_EnumGroup = null
//     group udg_CloneHeroGroup = null
//     group udg_AghCloneGroup = null
//     group udg_MirrorGroup = null
//     unit array udg_DM_Hero
//     boolean array udg_DM_Backstab
//     integer udg_DM_HeroCount = 0

function DM_GetHeroIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_DM_HeroCount
        if udg_DM_Hero[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    if udg_DM_HeroCount < 32 then
        set udg_DM_Hero[udg_DM_HeroCount] = u
        set udg_DM_Backstab[udg_DM_HeroCount] = false
        set udg_DM_HeroCount = udg_DM_HeroCount + 1
        return udg_DM_HeroCount - 1
    endif
    return -1
endfunction

function DM_FindCapIndex takes unit u returns integer
    local integer i = 0
    loop
        exitwhen i >= udg_CapCount
        if udg_CapUnit[i] == u then
            return i
        endif
        set i = i + 1
    endloop
    return -1
endfunction

function DM_RemoveCapIndex takes integer idx returns nothing
    if idx >= 0 and idx < udg_CapCount then
        set udg_CapUnit[idx] = udg_CapUnit[udg_CapCount - 1]
        set udg_CapOrigOwner[idx] = udg_CapOrigOwner[udg_CapCount - 1]
        set udg_CapDuration[idx] = udg_CapDuration[udg_CapCount - 1]
        set udg_CapCaster[idx] = udg_CapCaster[udg_CapCount - 1]
        set udg_CapIsHero[idx] = udg_CapIsHero[udg_CapCount - 1]
        set udg_CapAghBuff[idx] = udg_CapAghBuff[udg_CapCount - 1]
        set udg_CapUnit[udg_CapCount - 1] = null
        set udg_CapOrigOwner[udg_CapCount - 1] = null
        set udg_CapCaster[udg_CapCount - 1] = null
        set udg_CapCount = udg_CapCount - 1
    endif
endfunction

function DM_RestoreControl takes integer idx returns nothing
    local unit u = udg_CapUnit[idx]
    local player p = udg_CapOrigOwner[idx]
    if u != null and p != null then
        call SetUnitOwner(u, p, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\DispelMagic\\DispelMagicTarget.mdl", u, "origin"))
    endif
    call DM_RemoveCapIndex(idx)
    set u = null
    set p = null
endfunction

// 一技能：镜像触发隐身与质变
function DM_CastMirrorImage takes unit caster returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A001')
    local integer hIdx = DM_GetHeroIndex(caster)
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    // 添加并施放隐形/疾步风
    call UnitAddAbility(caster, 'A00W')
    call SetUnitAbilityLevel(caster, 'A00W', lv)
    call IssueImmediateOrder(caster, "windwalk")
    
    // 视觉特效与音效反馈
    call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Orc\\WindWalk\\WindWalkTarget.mdl", GetUnitX(caster), GetUnitY(caster)))
    
    // 神杖被动质变：穿相、极限移速522、破隐致命一击准备
    if hasAgh and hIdx >= 0 then
        call SetUnitMoveSpeed(caster, 522.0)
        set udg_DM_Backstab[hIdx] = true
    endif
endfunction

// 二技能：幻梦奴役
function DM_CastPossession takes unit caster, unit target returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A002')
    local player casterPlayer = GetOwningPlayer(caster)
    local player origPlayer = GetOwningPlayer(target)
    local real dur = 30.0
    local integer idx = 0
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    if target == null or origPlayer == casterPlayer then
        return
    endif
    
    if lv == 2 then
        set dur = 120.0
    elseif lv >= 3 then
        set dur = 600.0
    endif
    
    // 若已经被奴役，则刷新时间
    set idx = DM_FindCapIndex(target)
    if idx >= 0 then
        set udg_CapDuration[idx] = dur
        set udg_CapCaster[idx] = caster
        set udg_CapAghBuff[idx] = hasAgh
        return
    endif
    
    // 新增奴役记录
    if udg_CapCount < 128 then
        set udg_CapUnit[udg_CapCount] = target
        set udg_CapOrigOwner[udg_CapCount] = origPlayer
        set udg_CapDuration[udg_CapCount] = dur
        set udg_CapCaster[udg_CapCount] = caster
        set udg_CapIsHero[udg_CapCount] = IsUnitType(target, UNIT_TYPE_HERO)
        set udg_CapAghBuff[udg_CapCount] = hasAgh
        set udg_CapCount = udg_CapCount + 1
        
        // 改变控制权
        call SetUnitOwner(target, casterPlayer, true)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\Possession\\PossessionTarget.mdl", target, "overhead"))
        
        // 神杖质变：狂暴增益（移速+40%）
        if hasAgh and not IsUnitType(target, UNIT_TYPE_STRUCTURE) then
            call SetUnitMoveSpeed(target, GetUnitMoveSpeed(target) * 1.40)
        endif
    endif
endfunction

// 三技能：万象皆虚（召唤指定范围内所有单位的真实幻象）
function DM_CastMassIllusion takes unit caster, real cx, real cy returns nothing
    local integer lv = GetUnitAbilityLevel(caster, 'A003')
    local player p = GetOwningPlayer(caster)
    local real radius = 250.0
    local unit t = null
    local unit clone = null
    local integer utid = 0
    local integer oldFood = 0
    local boolean hasAgh = GetUnitAbilityLevel(caster, 'A004') > 0
    
    if lv == 2 then
        set radius = 350.0
    elseif lv >= 3 then
        set radius = 450.0
    endif
    
    // 特效
    call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Other\\Silence\\SilenceAreaBirth.mdl", cx, cy))
    
    call GroupEnumUnitsInRange(udg_EnumGroup, cx, cy, radius, null)
    loop
        set t = FirstOfGroup(udg_EnumGroup)
        exitwhen t == null
        call GroupRemoveUnit(udg_EnumGroup, t)
        
        if GetUnitState(t, UNIT_STATE_LIFE) > 0.405 and not IsUnitType(t, UNIT_TYPE_STRUCTURE) and not IsUnitType(t, UNIT_TYPE_DEAD) then
            set utid = GetUnitTypeId(t)
            
            // 复制前记录人口，复制后重置人口消耗（确保幻象单位绝不卡玩家人口）
            set oldFood = GetPlayerState(p, PLAYER_STATE_RESOURCE_FOOD_USED)
            set clone = CreateUnit(p, utid, GetUnitX(t), GetUnitY(t), GetUnitFacing(t))
            call SetPlayerState(p, PLAYER_STATE_RESOURCE_FOOD_USED, oldFood)
            
            if clone != null then
                // 15 分钟持续时间 (900.0 秒)
                call UnitApplyTimedLife(clone, 'BTLF', 900.0)
                call UnitAddType(clone, UNIT_TYPE_SUMMONED)
                
                // 幻象半透明蓝紫幽光外观
                call SetUnitVertexColor(clone, 90, 130, 255, 175)
                call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Orc\\MirrorImage\\MirrorImageCaster.mdl", GetUnitX(clone), GetUnitY(clone)))
                
                // 若复制的是英雄，赋予相同等级并加入追踪防祭坛复活
                if IsUnitType(t, UNIT_TYPE_HERO) then
                    call SetHeroLevel(clone, GetHeroLevel(t), false)
                    call GroupAddUnit(udg_CloneHeroGroup, clone)
                endif
                
                // 神杖质变：加入反哺组
                if hasAgh then
                    call GroupAddUnit(udg_AghCloneGroup, clone)
                endif
            endif
            
            // 神杖质变：敌方目标陷入 3 秒梦魇昏睡
            if hasAgh and IsUnitEnemy(t, p) then
                call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\Sleep\\SleepTarget.mdl", t, "overhead"))
            endif
        endif
    endloop
    
    set t = null
    set clone = null
endfunction

// 施法事件分发
function DM_OnSpellEffect takes nothing returns boolean
    local unit caster = GetTriggerUnit()
    local integer abil = GetSpellAbilityId()
    
    if abil == 'A001' then
        call DM_CastMirrorImage(caster)
    elseif abil == 'A002' then
        call DM_CastPossession(caster, GetSpellTargetUnit())
    elseif abil == 'A003' then
        call DM_CastMassIllusion(caster, GetSpellTargetX(), GetSpellTargetY())
    endif
    
    set caster = null
    return false
endfunction

// 攻击与伤害事件：破隐一击、神杖反哺、英雄濒死提前返还原主
function DM_OnDamaged takes nothing returns boolean
    local unit victim = GetTriggerUnit()
    local unit attacker = GetEventDamageSource()
    local real dmg = GetEventDamage()
    local integer idx = 0
    local integer hIdx = 0
    
    // 1. 奴役目标濒死保护：伤害致死前瞬间归还给原主，绝不在己方祭坛复活！
    set idx = DM_FindCapIndex(victim)
    if idx >= 0 then
        if dmg >= GetWidgetLife(victim) then
            call DM_RestoreControl(idx)
        endif
    endif
    
    // 2. 破隐一击（神杖质变）：解除隐身的一击造成 200 点额外暗影伤害
    set hIdx = DM_GetHeroIndex(attacker)
    if hIdx >= 0 and udg_DM_Backstab[hIdx] then
        set udg_DM_Backstab[hIdx] = false
        call UnitDamageTarget(attacker, victim, 200.0, true, false, ATTACK_TYPE_HERO, DAMAGE_TYPE_MAGIC, WEAPON_TYPE_WHOKNOWS)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\ShadowHunter\\ShadowHunterMissile.mdl", victim, "chest"))
    endif
    
    // 3. 神杖反哺：幻象造成的伤害 25% 转化为生命值反哺幻梦大师
    if IsUnitInGroup(attacker, udg_AghCloneGroup) and dmg > 0.0 then
        // 给幻梦大师回血
        set hIdx = 0
        loop
            exitwhen hIdx >= udg_DM_HeroCount
            if GetOwningPlayer(udg_DM_Hero[hIdx]) == GetOwningPlayer(attacker) and GetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE) > 0.405 then
                call SetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE, GetUnitState(udg_DM_Hero[hIdx], UNIT_STATE_LIFE) + dmg * 0.25)
            endif
            set hIdx = hIdx + 1
        endloop
    endif
    
    set victim = null
    set attacker = null
    return false
endfunction

// 死亡事件：防祭坛复活、幻象英雄清理、奴役击杀延时
function DM_OnDeath takes nothing returns boolean
    local unit dying = GetDyingUnit()
    local unit killer = GetKillingUnit()
    local integer idx = 0
    
    // 1. 若被奴役单位死亡，确保所属权立即归还给原主
    set idx = DM_FindCapIndex(dying)
    if idx >= 0 then
        call DM_RestoreControl(idx)
    endif
    
    // 2. 若复制的英雄幻象死亡，立即彻底移除，永不进入祭坛复活列表！
    if IsUnitInGroup(dying, udg_CloneHeroGroup) then
        call GroupRemoveUnit(udg_CloneHeroGroup, dying)
        call RemoveUnit(dying)
    endif
    
    // 3. 奴役击杀延时（神杖质变）：每击杀一名敌人，控制时间延长 15 秒！
    if killer != null then
        set idx = DM_FindCapIndex(killer)
        if idx >= 0 and udg_CapAghBuff[idx] then
            set udg_CapDuration[idx] = udg_CapDuration[idx] + 15.0
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl", killer, "origin"))
        endif
    endif
    
    set dying = null
    set killer = null
    return false
endfunction

// 每秒周期心跳：奴役倒计时结算与生命恢复
function DM_PeriodicLoop takes nothing returns nothing
    local integer i = udg_CapCount - 1
    local unit u = null
    local real maxHP = 0.0
    
    loop
        exitwhen i < 0
        set u = udg_CapUnit[i]
        
        // 若单位已失效或死亡
        if u == null or GetUnitState(u, UNIT_STATE_LIFE) <= 0.405 then
            call DM_RestoreControl(i)
        else
            set udg_CapDuration[i] = udg_CapDuration[i] - 1.0
            
            // 神杖质变：每秒恢复 3% 最大生命
            if udg_CapAghBuff[i] and not IsUnitType(u, UNIT_TYPE_STRUCTURE) then
                set maxHP = GetUnitState(u, UNIT_STATE_MAX_LIFE)
                call SetUnitState(u, UNIT_STATE_LIFE, GetUnitState(u, UNIT_STATE_LIFE) + maxHP * 0.03)
            endif
            
            // 到期叛变归还
            if udg_CapDuration[i] <= 0.0 then
                call DM_RestoreControl(i)
            endif
        endif
        
        set i = i - 1
    endloop
    set u = null
endfunction

// 系统初始化入口
function Init_DreamMasterSystem takes nothing returns nothing
    local trigger tSpell = CreateTrigger()
    local trigger tDamage = CreateTrigger()
    local trigger tDeath = CreateTrigger()
    local timer tTimer = CreateTimer()
    local integer i = 0
    
    set udg_EnumGroup = CreateGroup()
    set udg_CloneHeroGroup = CreateGroup()
    set udg_AghCloneGroup = CreateGroup()
    set udg_MirrorGroup = CreateGroup()
    
    // 注册所有玩家事件 (0..15 及中立怪 24..27)
    loop
        exitwhen i >= 16
        call TriggerRegisterPlayerUnitEvent(tSpell, Player(i), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
        call TriggerRegisterPlayerUnitEvent(tDamage, Player(i), EVENT_PLAYER_UNIT_DAMAGED, null)
        call TriggerRegisterPlayerUnitEvent(tDeath, Player(i), EVENT_PLAYER_UNIT_DEATH, null)
        set i = i + 1
    endloop
    
    // 注册中立敌对/野怪 (24 = Creeps, 25 = Passive)
    call TriggerRegisterPlayerUnitEvent(tSpell, Player(24), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
    call TriggerRegisterPlayerUnitEvent(tDamage, Player(24), EVENT_PLAYER_UNIT_DAMAGED, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(24), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tSpell, Player(25), EVENT_PLAYER_UNIT_SPELL_EFFECT, null)
    call TriggerRegisterPlayerUnitEvent(tDamage, Player(25), EVENT_PLAYER_UNIT_DAMAGED, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(25), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(26), EVENT_PLAYER_UNIT_DEATH, null)
    call TriggerRegisterPlayerUnitEvent(tDeath, Player(27), EVENT_PLAYER_UNIT_DEATH, null)
    
    call TriggerAddCondition(tSpell, Condition(function DM_OnSpellEffect))
    call TriggerAddCondition(tDamage, Condition(function DM_OnDamaged))
    call TriggerAddCondition(tDeath, Condition(function DM_OnDeath))
    
    // 启动每秒心跳
    call TimerStart(tTimer, 1.00, true, function DM_PeriodicLoop)
endfunction

function main takes nothing returns nothing
    call Init_DreamMasterSystem()
endfunction
function config takes nothing returns nothing
endfunction
