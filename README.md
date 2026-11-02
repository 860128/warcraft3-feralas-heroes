# 菲拉斯之战·自定义英雄与AI扩展重构项目 (Feralas Hero Mod)
**当前版本：测试版v2.2 (Release v2.2)**  
**地图底板：`(8)feralas.w3x` (暴雪官方菲拉斯之羽 8人对战地图)**  
**编译输出：`rebuild_feralas.w3x`**  
**游戏部署路径：`C:\Users\wyh\Documents\Warcraft III\Maps\Download\(8)feralas.w3x`**

---

## 目录
1. [项目总览与工程目录结构](#1-项目总览与工程目录结构)
2. [自动化构建与重构流水线](#2-自动化构建与重构流水线)
3. [完整对象注册表 (Object ID Registry)](#3-完整对象注册表-object-id-registry)
4. [英雄 1：幻梦大师 (`H002`) 机制与 JASS 架构](#4-英雄-1幻梦大师-h002-机制与-jass-架构)
5. [英雄 2：魔音忍者 (`H003`) 机制与 JASS 架构](#5-英雄-2魔音忍者-h003-机制与-jass-架构)
6. [测试模式与 AI 战略统帅体系 (AI Architecture)](#6-测试模式与-ai-战略统帅体系-ai-architecture)
7. [魔兽争霸III引擎避坑指南与开发铁律 (Golden Rules)](#7-魔兽争霸iii引擎避坑指南与开发铁律-golden-rules)
8. [二次开发指南：如何接入新英雄 (`H004`)](#8-二次开发指南如何接入新英雄-h004)

---

## 1. 项目总览与工程目录结构

本项目基于魔兽争霸III经典 8 人常规对战地图 `(8)feralas.w3x`，在保持四族经典对战建筑、兵种、科技树平衡的基础上，重构注入了全新的自定义高机制英雄、全套配套技能与克隆体系、智能双层测试模式（Test Mode Dialog）以及自主行动的战略级电脑 AI（Strategic Army Commander）。

### 核心目录与文件职责

```
feralas_hero/
│
├── feralas_orig.w3x                   # 官方纯净底板地图包 (Clean Base Map)
├── rebuild_feralas.w3x                 # 构建流水线输出的最终地图包
├── do_rebuild.ps1                      # 一键自动化重建与打包脚本 (PowerShell)
├── README.md                           # 本架构与二次开发技术文档
│
├── payload/                            # 注入地图 MPQ 内部的核心载荷
│   ├── war3map.j                       # 核心 JASS 业务逻辑代码 (4700+ 行)
│   ├── war3map.w3a                     # 二进制技能对象数据 (Ability Data)
│   ├── war3map.w3u                     # 二进制单位对象数据 (Unit Data)
│   ├── war3map.wts                     # 地图主字符串表 (String Table)
│   └── _Locales/                       # 多语言本地化目录 (zhCN, zhTW, deDE, frFR 等)
│       ├── zhCN.w3mod/war3map.wts
│       ├── zhTW.w3mod/war3map.wts
│       └── ...
│
├── factory_tpl/                        # w3x2lni 对象定义模板
│   └── table/
│       ├── unit.ini                    # INI 格式单位定义 (H002, H003, u000~u002, 祭坛等)
│       └── ability.ini                 # INI 格式技能定义 (A001~A004, A011~A017 等)
│
└── tools/                              # 工程工具链
    ├── JassHelper/
    │   └── pjass.exe                   # JASS 语法检查编译器 (支持 1.32+ 新 API 校验)
    ├── w3x2lni/
    │   ├── w2l.exe                     # 魔兽对象 LNI <-> 二进制转化工具
    │   └── data/                       # 包含 zhCN-1.32.8 脚本规范库
    ├── StormLib.dll                    # 32位 MPQ 底层读写库
    ├── StormLibSharp.dll               # 32位 MPQ C# / .NET 绑定封装
    ├── mpq_write.ps1                   # MPQ 文件写入与更新核心注入脚本
    ├── build_v13_objs.py               # 编译 INI 对象并同步提取至 payload
    ├── patch_v22_aura_nonlethal.py     # v2.2 竭心光环与因果流失非致死保底热修脚本
    └── update_locales_v22.py           # v2.2 多语言字符串一键同步脚本
```

---

## 2. 自动化构建与重构流水线

当对代码 (`war3map.j`) 或对象 (`build_v13_objs.py` / `*.ini`) 做出更改后，必须按以下标准流水线执行构建与部署：

### 步骤 1：JASS 语法编译检查 (Syntax Check)
魔兽争霸 III 引擎对 JASS 语法极其敏感，任何语法错误都会导致进入游戏提示“无法读取地图”。我们使用内置的 `pjass.exe` 结合 Patch 1.32.8 现代 API 库进行静默编译验证：
```powershell
Set-Location "C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
& tools\JassHelper\pjass.exe tools\w3x2lni\data\zhCN-1.32.8\mpq\Scripts\Common.j tools\w3x2lni\data\zhCN-1.32.8\mpq\Scripts\Blizzard.j payload\war3map.j
```
*必须看到输出 `Parse successful: ... payload\war3map.j` 且 `0 errors`。*

### 步骤 2：对象数据编译 (Object Compilation)
若修改了技能数值、说明文本或单位属性，运行：
```powershell
python tools/build_v13_objs.py
```
该脚本会将 `factory_tpl/table` 的 INI 文件通过 `w2l.exe` 编译并自动提取最新的 `war3map.w3a` 和 `war3map.w3u` 到 `payload/` 目录。

### 步骤 3：一键 MPQ 打包构建 (`do_rebuild.ps1`)
运行一键打包脚本：
```powershell
powershell -ExecutionPolicy Bypass -File do_rebuild.ps1
```
> **注意**：由于 `StormLibSharp.dll` 是 32 位二进制文件，`do_rebuild.ps1` 内部已固定调用 `C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`，切勿在外部强制以 64 位环境反射调用 `StormLibSharp`。

### 步骤 4：部署至魔兽争霸游戏目录
```powershell
Copy-Item rebuild_feralas.w3x "C:\Users\wyh\Documents\Warcraft III\Maps\Download\(8)feralas.w3x" -Force
```

---

## 3. 完整对象注册表 (Object ID Registry)

### 3.1 自定义单位 (Units)

| 单位 ID | 父类 (Parent) | 类别 / 种族 | 名称 | 核心定位与机制用途 |
| :--- | :--- | :--- | :--- | :--- |
| **`H002`** | `Obla` (剑圣) | 敏捷型自定义英雄 | **幻梦大师** | 英雄本尊 1。操纵镜像、控制目标、大范围克隆敌军、幻术升华。 |
| **`H003`** | `Ewar` (守望者) | 敏捷型自定义英雄 | **魔音忍者** | 英雄本尊 2。闪避击杀同化、全图竭心光环、因果印记夺舍、独断神尊。 |
| **`u000`** | `ewsp` (小精灵) | 辅助/无敌蝗虫 | **Dummy Caster** | 马甲施法者。无模型、无碰撞、无敌、0转身与0施法硬直，用于释放辅助技能。 |
| **`u001`** | `nbal` (恐惧魔王/巴纳扎尔) | 召唤生物/混沌守卫 | **独断万古·魔音神尊** | 大招 `A014` 召唤物。3000HP、混沌攻击、全魔法免疫(`Amim`)、分裂攻击、自带3级闪避(`A015`)与暴击(`A017`)，能触发同化分身并可作为替死移魂目标。 |
| **`u002`** | `ogru` (兽人步兵) | 伪英雄分身 | **魔音忍者 (伪英雄分身)** | **关键底层设计**：继承守望者模型与音效、挂载背包(`AInv`)与闪避(`A015`)，但**底层为普通非英雄单位**！彻底杜绝魔兽引擎平分吞噬真英雄打怪经验的缺陷。 |
| **`halt`** | `halt` (人族祭坛) | 建筑物 | 国王祭坛 (扩展) | 在默认可造英雄列表中挂载 `H002` 与 `H003`。 |
| **`oalt`** | `oalt` (兽族祭坛) | 建筑物 | 风暴祭坛 (扩展) | 在默认可造英雄列表中挂载 `H002` 与 `H003`。 |
| **`uaod`** | `uaod` (不死祭坛) | 建筑物 | 黑暗祭坛 (扩展) | 在默认可造英雄列表中挂载 `H002` 与 `H003`。 |
| **`eate`** | `eate` (暗夜祭坛) | 建筑物 | 长者祭坛 (扩展) | 在默认可造英雄列表中挂载 `H002` 与 `H003`。 |

### 3.2 自定义技能 (Abilities)

| 技能 ID | 父类 | 快捷键 | 施法命令 (Order) | 归属 / 名称 | 机制简述 |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`A001`** | `AOmi` | Q | `mirrorimage` (852274) | 幻梦大师：**镜像与潜行** | 召唤 1/2/3 具镜像并赋予延时隐匿潜行辅助。 |
| **`A002`** | `ANcl` | W | `charm` (852580) | 幻梦大师：**幻梦奴役** | 强制夺取任意目标操控权（小兵/野怪/敌方英雄/敌方建筑均可），持续数十秒。 |
| **`A003`** | `ANcl` | E | `blizzard` (852187) | 幻梦大师：**万象皆虚** | 区域指向法术，对范围内敌方全体生成真实全伤害幻象，支持无限链式克隆。 |
| **`A004`** | `Aamk` | R | *(被动)* | 幻梦大师：**幻界主宰** | 大招。全属性+10，并全面提升 Q/W/E 技能机制与强度（Q享522移速与背刺）。 |
| **`A00V`** | `Aivs` | - | - | 幻梦大师：**隐匿潜行辅助** | Q技能使用的隐身辅助底板。 |
| **`A00I`** | `AIil` | - | - | 幻梦大师：**万象幻影辅助** | E技能普通幻象权杖马甲辅助。 |
| **`A00J`** | `AIil` | - | - | 幻梦大师：**万象幻影神杖辅助** | E技能强化幻象神杖马甲辅助（大招升华）。 |
| **`A011`** | `AEev` | Q | *(被动)* | 魔音忍者：**魔音同化** | 获得 15%/25%/35% 闪避；击杀非建筑单位生成 `u002` 伪英雄分身；本尊受死时不死移魂。 |
| **`A012`** | `ANcl` | W | `roar` (852164) | 魔音忍者：**竭心光环** | 全图范围开关光环。每秒削减敌方非建筑 1%/2%/3% 最大生命。**v2.2 保底 1 HP 不致死**。 |
| **`A013`** | `AOcr` | E | *(被动)* | 魔音忍者：**他化自在** | 暴击提升；击杀魔音忍者者被种下因果印记；凶手死后化为新分身，若全灭则直接满血夺舍复活本尊。 |
| **`A014`** | `ANcl` | R | `summongrizzly` (852594) | 魔音忍者：**独断万古** | 召唤 3000 血混沌全魔免魔音神尊 `u001`，持续 120 秒。 |
| **`A015`** | `ACev` | - | - | 魔音分身闪避辅助 | 挂载于 `u002` 伪英雄分身上的闪避技能，等级与本尊 Q 同步。 |
| **`A016`** | `ACev` | - | - | 神尊闪避辅助 | 挂载于 `u001` 独断神尊上的闪避技能。 |
| **`A017`** | `AOcr` | - | - | 神尊暴击辅助 | 挂载于 `u001` 独断神尊上的致命一击。 |

---

## 4. 英雄 1：幻梦大师 (`H002`) 机制与 JASS 架构

### 4.1 镜像与潜行 (`A001` + `A00V` + `DM_StealthLoop`)
- **双重保命与刺客机制**：施法时基于 `AOmi` 生成分身混淆视听，同时通过底层马甲向施法者施加 `A00V` 隐身。
- **高频潜行监测 (`DM_StealthLoop`)**：由 0.05 秒高频计时器驱动。若施法者已学习大招 `A004`，潜行状态下强制将其移速提升至引擎极限 **522.0** (`SetUnitMoveSpeed`)。
- **破隐一击背刺 (`DM_BreakInvisibility`)**：通过 `EVENT_PLAYER_UNIT_DAMAGED` 监测，若英雄处于潜行中发起普攻，会瞬间破隐并附加背刺暴击伤害与特殊音效。

### 4.2 幻梦奴役 (`A002` + `DM_CastPossession` + `DM_CapTimerLoop`)
- **超维度强控**：能接管普通野怪、高级兵种甚至敌方英雄与建筑。
- **防止侵入玩家祭坛的死亡回退机制 (`DM_OnUnitDeath`)**：
  - 在魔兽争霸原生引擎中，若敌方英雄被控制期间死亡，极易判定为控制方的阵亡英雄，进而错误出现在控制方的英雄祭坛中！
  - **核心解法**：在 `DM_OnUnitDeath` 中优先检索 `DM_FindCapIndex(dead)`，在任何复活事件响应前**立刻**调用 `SetUnitOwner(dead, origOwner, true)` 将归属权返还原主并清除索引。

### 4.3 万象皆虚 (`A003` + `DM_CastMassIllusion` + `DM_CloneOneUnit`)
- **无限链式克隆支持**：不仅克隆野生单位，当对场上的真英雄、克隆体或幻象施法时，仍能正确派生出具有完全攻击力/防御属性的真实战力单位。
- **防抢经验与防占头像的伪英雄垃圾回收架构 (`udg_FakeHeroGroup`)**：
  - 传统 `CreateIllusion` 或英雄克隆体阵亡时，会触发暴雪引擎的 `EVENT_PLAYER_HERO_REVIVABLE`，导致玩家左侧面板出现幽灵头像、祭坛可复活无主单位，且打怪平分经验。
  - **三重安全拦截**：
    1. 克隆出的单位打上 `udg_FakeHeroGroup` 标记。
    2. 阵亡瞬间在 `DM_OnUnitDeath` 将其所有权切换为 `Player(PLAYER_NEUTRAL_PASSIVE)` 并调用 `SetUnitExploded(dead, true)` 彻底注销单位残骸。
    3. 在 `DM_OnHeroRevivable` 触发器中，若检索到单位位于 `udg_FakeHeroGroup`，立即阻断并将其注销，绝不进入祭坛复活队列！

### 4.4 幻界主宰 (`A004`)
- 敏捷、力量、智力三维常驻增加 10 点。
- 全面升华 Q（极速522+极高背刺）、W（持续时间延长+可控建筑）、E（使用神杖强化级辅助 `A00J` 提升幻象输出比并降低承伤比）。

---

## 5. 英雄 2：魔音忍者 (`H003`) 机制与 JASS 架构

### 5.1 魔音同化 (`A011` + `u002` + 装备复制)
- **非英雄底层伪英雄分身 (`u002`)**：
  - 魔兽争霸 III 引擎中，只要单位底层为 Hero（如 `Ewar`），即便调用 API `SuspendHeroXP(u, true)`，该单位依然会占据经验计算分母，严重拖垮周围友方英雄练级速度。
  - **创新解决方案**：`u002` 底层基于兽人步兵 `ogru`，仅外观与语音伪装为守望者。当击杀非建筑单位生成 `u002` 时：
    - 动态同步当前本尊的 `A015` 闪避等级。
    - 遍历本尊 6 格物品栏，通过 `UnitAddItemById` 为分身逐一克隆相同的神装！
- **无相真身不死移魂双重保险 (Soul Migration Dual-Safety Architecture)**：
  - **第一道防线：伤害致死前拦截 (`DM_OnDamaged`)**：
    - 注册现代原生事件 `EVENT_PLAYER_UNIT_DAMAGED`。
    - 当本尊 `H003` 受到致命伤害（`dmg >= curHP`）时，拦截伤害并恢复本尊血量。
    - 瞬时寻找全图任意存活的 `u002` 分身或 `u001` 神尊，将本尊瞬间转移至其坐标（`SetUnitPosition`），将替身湮灭，实现“杀而不死、移魂转生”。
  - **第二道防线：阵亡瞬时复活兜底 (`DM_OnUnitDeath`)**：
    - 若遭受不可抗拒的触发秒杀（例如超过单帧判定阈值），在 `DM_OnUnitDeath` 中判定场上是否存有活着的魔音分身。
    - 若有，立即在分身位置调用 `ReviveHeroLoc`，移魂转生，唯有杀尽全图所有本尊与分身，魔音忍者才真正死亡！

### 5.2 竭心光环 (`A012` - v2.2 非致死保底机制)
- **全局开关光环**：基于 `ANcl` (Order `roar`)，学习后默认开启，点击图标可随时自由启闭。
- **全图削减**：开启时每秒对全图所有敌方非建筑单位扣除最大生命值的 1% (Lv1) / 2% (Lv2) / 3% (Lv3)。
- **v2.2 保底 1 HP 不致死设计 (`DM_CapTimerLoop`)**：
  ```jass
  set drain = GetUnitState(enumU, UNIT_STATE_MAX_LIFE) * pct
  set curHP = GetWidgetLife(enumU)
  if curHP > 1.5 then
      if curHP - drain > 1.0 then
          call SetWidgetLife(enumU, curHP - drain)
      else
          call SetWidgetLife(enumU, 1.0)
      endif
  endif
  ```
  - **设计初衷**：光环纯粹作为削血与压血线手段，最低血量严格锁定在 1.0 点，**绝不直接杀死单位**。所有敌军击杀必须由英雄或友军单位亲自造成最后一击（补刀），彻底避免全图野怪和敌军莫名暴毙导致无击杀者判定的问题。

### 5.3 他化自在 (`A013` 因果烙印与夺舍复生)
- **因果烙印**：任何击杀魔音忍者（或其分身）的凶手，都会被永久种下【他化自在】诅咒。凶手头顶绑定紫色诅咒特效 (`udg_KarmaFx`) 并被调为暗紫色。
- **因果流失保底**：Lv2/Lv3 印记每秒削减凶手 1%/2% 最大生命值，同样受 v2.2 保护锁定最低 1.0 HP 不致死。
- **终极夺舍**：当凶手被消灭时：
  - 若魔音忍者场上仍有活动单位，凶手尸体化为 1~2 个新的魔音分身。
  - **逆转绝境**：若此时魔音忍者本尊及所有分身均已阵亡，凶手死亡将**直接在其尸体坐标满血夺舍复活魔音忍者本尊**！

### 5.4 独断万古 (`A014` + `u001`)
- 召唤拥有 3000 生命、混沌攻击、全魔法免疫、自带分裂攻击的魔音神尊 `u001`。
- 神尊具备英雄级威慑力，可触发同化分身，并作为最高优先级的移魂替死容器。

---

## 6. 测试模式与 AI 战略统帅体系 (AI Architecture)

### 6.1 智能双层对话框系统 (Two-Tier Dialog UI)
为方便单人调试与全图 AI 混战，地图内置了开局对话框系统：
- **第一层主菜单 (`TM_ShowMainDialog`)**：
  - `[1] 单挑快速测试`：玩家 1 vs 电脑 2（单挑对决）。
  - `[2] 全图满员大乱斗`：所有 8 个玩家槽位全部激活，电脑互相征伐。
  - `[3] 标准对战模式`：保留原生常规对战体验。
  - `[9] 自定义每家英雄`：进入第二层子菜单。
  - `[0] 关闭菜单`。
- **第二层子菜单 (`TM_ShowSlotDialog`)**：支持逐一为各个电脑玩家指派【幻梦大师】、【魔音忍者】或【常规对战英雄】。
- **聊天快捷指令**：游戏中随时输入 `-test` 呼出主菜单；`-m0` 切回标准模式；`-m1` 全局英雄乱斗；`-m2` 自定义配置。

### 6.2 电脑 AI 自适应无缝替换与祭坛复活
- **训练事件监听 (`EVENT_PLAYER_UNIT_TRAIN_FINISH`)**：当电脑玩家在祭坛训练出常规英雄的瞬间，`AI_SpawnCustomHeroForPlayer` 会安全移除该英雄并无缝替换为预设的自定义英雄，保留其等级与物品体系。
- **祭坛自动复活 (`AI_HandleAltarRevival`)**：电脑自定义英雄阵亡后，AI 会自动寻找本方祭坛执行复活，无需人工干预。

### 6.3 突破近战 AI 技能锁死的强制加点引擎 (`AI_ForceLearnSkill`)
- **引擎痛点**：暴雪默认的近战 AI 脚本 (`common.ai`) 仅能识别原版四族英雄的技能树。遇到 `H002` 与 `H003` 这类自定义英雄时，AI 会锁死技能点，导致 10 级英雄 0 技能。
- **强力破局方案**：
  - 监听 `EVENT_PLAYER_HERO_LEVEL` 事件与周期性 AI 巡检。
  - 查询 `GetHeroSkillPoints(h)`。
  - 按照预设的优先级（如优先学满同化 `A011`、光环 `A012`，6级秒学大招 `A014`），调用底层 API：
    ```jass
    call UnitAddAbility(h, abilId)
    call SetUnitAbilityLevel(h, abilId, targetLv)
    call UnitModifySkillPoints(h, -1)
    ```
  - 完美绕过 `SelectHeroSkill` 原生白名单限制，让 AI 英雄战斗力完全拉满！

### 6.4 战术施法大脑 (`AI_TacticalLoop`)
高频检索敌军密集度、生命值与施法距离：
- 幻梦大师 AI 会在陷入包围或血量偏低时自动释放 Q 分身隐身、智能选取敌方高战力兵种释放 W 奴役、在敌群扎堆处释放 E 万象皆虚。
- 魔音忍者 AI 会在遭遇战斗时开启 W 竭心光环、残血或敌方英雄聚团时召唤 R 独断神尊。

### 6.5 战略大军统帅系统 (`AI_StrategicCommander`)
- **彻底消除 AI 兵力“基地发呆”与“拉扯折返跑 (Rubber-banding)”**：
  - **病灶分析**：暴雪原版地图中，由基地兵营生产的单位都带有默认的“警戒区域驻留锚点 (Guard Position)”。当第三方脚本命令单位进攻时，原版 `common.ai` 内部的警戒绳索 (Leash) 会强制下达回防指令，导致 AI 大军在野外反复抽搐折返。
  - **核心解法**：
    1. 在向 AI 单位派发进攻任务前，全面调用 `RemoveGuardPosition(u)` 以及 `RemoveAllGuardPositions(pId)`，彻底切断暴雪原生的警戒绳索羁绊！
    2. 引入 `udg_AI_LockedTarget[pId]` 目标锁定机制：为 AI 锁定一个战略进攻点（野外矿点/野怪营地/敌方分基地/敌方主基地），在目标未清除前不随意重定向。
    3. AI 军队会坚决执行“集结 -> 抱团清野 (Creep) -> 压制敌军分矿 -> 决战推平主基地”的完整战略行动！

---

## 7. 魔兽争霸III引擎避坑指南与开发铁律 (Golden Rules)

在对本项目做二次开发时，必须牢记以下由血泪实战验证的底层铁律：

### 铁律 1：`war3map.wts` 严禁出现未转义的多行字符串 (Single-Line Rule)
- 魔兽争霸 III 现代版本（重制版 / 1.32+）的字符串表解析器在处理多语言 `.wts` 文件时，若在单个 `STRING` 项内使用了物理多行（回车换行），会导致游戏主界面的 WebUI 直接假死或卡在加载进度条 100%！
- **必须保证**：所有 `war3map.wts` 中的标题与介绍字段，均放在同一行内，换行必须用 `|n` 表示，不得直接敲物理回车。

### 铁律 2：MPQ 注入必须使用 32 位 PowerShell
- 项目附带的 `tools/StormLibSharp.dll` 与 `tools/StormLib.dll` 是 32 位（x86）的原生动态链接库。
- 如果在 64 位 PowerShell 环境中执行注入，会引发 `BadImageFormatException: 试图加载格式不正确的程序`。
- **必须使用**：`C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`（在 `do_rebuild.ps1` 中已内置该路径）。

### 铁律 3：克隆体与分身严禁继承自 Hero 对象父类
- 若想制作一个“具备英雄外形与战斗力”的替身或召唤物，其 `_parent` **绝对不能**是 `Obla`、`Ewar`、`Hpal` 等英雄对象！
- 即使设置了 `hero = 0`，魔兽底层判定该对象仍属于英雄分类，打怪击杀时会平分吞噬真英雄的经验池，且阵亡时会误触祭坛机制。
- **正确做法**：像 `u002` 一样，继承普通步兵 `ogru`，通过修改模型文件、挂载 `AInv` 背包与技能，伪装成英雄。

### 铁律 4：`DialogAddButton` 严禁在 `0.00` 秒地图初始化时生成
- 重制版引擎中，如果在 `main` 或 `InitCustomTriggers`（即地图时间 0.00 秒）直接生成 Dialog 按钮，对话框的点击碰撞盒 (Hitbox) 会出现不可逆的偏移或点击无响应 Bug。
- **正确做法**：必须通过单次计时器延迟至少 `1.00` 秒（参考 `TM_OnStartTimer`），待游戏引擎视口与 UI 渲染稳定后，再动态添加按钮并展示。

---

## 8. 二次开发指南：如何接入新英雄 (`H004`)

若需要为地图添加第 3 位全新的自定义英雄（例如 `H004`），请遵循以下标准流程：

### 步骤 1：在 `factory_tpl/table/unit.ini` 中定义英雄
在文件末尾追加新英雄配置，并在四大种族祭坛的 `heroAbilList` 或产出列表中加上 `H004`：
```ini
[H004]
_parent = "Hamg"
Name = "新英雄名称"
Propernames = "名字1,名字2"
Tip = "召唤 新英雄(|cffffcc00X|r)"
Ubertip = "新英雄详细介绍..."
Revivetip = "复活 新英雄(|cffffcc00X|r)"
Awakentip = "唤醒 新英雄(|cffffcc00X|r)"
Hotkey = "X"
Art = "ReplaceableTextures\\CommandButtons\\BTNHeroArchMage.blp"
file = "units\\human\\HeroArchMage\\HeroArchMage"
primary = "INT"
STR = 19
AGI = 15
INT = 24
heroAbilList = "A021,A022,A023,A024"
```

### 步骤 2：在 `factory_tpl/table/ability.ini` 中定义技能
分配新的技能 ID（如 `A021` ~ `A024`）：
```ini
[A021]
_parent = "ANcl"
Name = "新英雄一技能"
Order = "thunderbolt"
Hotkey = "Q"
...
```

### 步骤 3：更新对象编译脚本并执行编译
在 `tools/build_v13_objs.py` 中将 `H004` 和 `A021`~`A024` 加入校验列表，运行：
```powershell
python tools/build_v13_objs.py
```
确保 `payload/war3map.w3a` 和 `payload/war3map.w3u` 编译生成完毕。

### 步骤 4：在 `payload/war3map.j` 中接入核心逻辑
1. **技能响应**：在 `DM_OnSpellCast` 或 `DM_OnSpellEffect` 中添加 `GetSpellAbilityId() == 'A021'` 的分支处理。
2. **AI 技能强制加点**：在 `AI_ForceLearnSkill` 函数中添加针对 `H004` 的技能升级优先级与等级判断（普通技能 `curLv * 2 + 1`，终极技能 6 级）。
3. **AI 战术施法**：在 `AI_TacticalLoop` 中加入 `H004` 的施法逻辑。
4. **测试模式菜单集成**：
   - 在 `TM_ShowSlotDialog` 中为槽位选择增加 `H004` 按钮。
   - 在 `TM_OnSlotDialogClick` 中增加 `H004` 的分支生成与替换。

### 步骤 5：验证与发布
1. 运行 `pjass.exe` 验证 JASS 语法为 0 错误。
2. 运行 `do_rebuild.ps1` 重新打包地图。
3. 拷贝 `rebuild_feralas.w3x` 到游戏目录实机测试。

---
**项目技术支持与维护者：Antigravity Agentic Engineer**  
*遵循本规范可实现百分之百平滑二次开发与无缝迭代！*
