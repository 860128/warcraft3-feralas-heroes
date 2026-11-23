# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    if has_bom:
        text = data[3:].decode('utf-8')
    else:
        text = data.decode('utf-8')

    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    # 1. Update version title
    old_ver = "**当前版本：测试版v6.1 (Release v6.1)**"
    new_ver = "**当前版本：测试版v6.2 (Release v6.2)**"
    assert old_ver in text
    text = text.replace(old_ver, new_ver)

    # 2. Update Section 9.4
    old_sec94 = """### 9.4 人类玩家专属“无敌避难所”(`n003`)与 `-refuge` 迁移指令 (v3.0 新增)
- **痛点诉求**：在深度测试异种之源(`H004`)或其他英雄野外成长时，敌方电脑 AI 部队常趁虚拆除玩家出生点基地建筑，触发暴雪原生常规对战判负机制（`MeleeCheckForLosersAndVictors` -> `MeleeGetAllyStructureCount == 0`），导致英雄存活却被强制判定失败。
- **零破坏原生解决方案**：不修改暴雪原生胜负判定规则，而是在地图开局 1.5 秒自动为人类玩家在地图最靠近出生点的偏远角落（4个角落螺旋探测寻路）生成一座绝对无敌的建筑单位 **测试酒馆·无敌避难所 (`n003`)**。由于玩家恒拥有一座无敌建筑，引擎的存活建筑计数器恒大于0，从底层杜绝判负退出。
- **全英雄支持与15秒免费复活兜底**：
  - 酒馆拥有复活与全英雄训练列表，可随时用金币/木材购买复活或训练。
  - 若玩家无金币或基地瘫痪，自带 15 秒定时器自动复活保护：真英雄阵亡 15 秒后直接在避难所免费满血复活，克隆体/幻象/召唤物严格排除不触发。
- **AI 锁定规避**：所有战略部队进军与技能索敌逻辑（`AI_CommandArmyForPlayer`、`AI_TacticalLoop`、`AI_FindStrategicTarget`）全域排除无敌单位与 `n003`，电脑部队绝不会围攻或被避难所吸引卡死。
- **随时迁移指令 (`-refuge`)**：玩家在聊天框输入 `-refuge`，避难所会立刻螺旋寻路闪烁传送至玩家当前英雄身旁，方便就近补给与复活！"""

    new_sec94 = """### 9.4 人类玩家专属“无敌避难所”(`n003`)、`-refuge` 迁移与全维悬崖安全重构 (v6.2 重磅重构)
- **痛点诉求**：在深度测试异种之源(`H004`)或其他英雄野外成长时，敌方电脑 AI 部队常趁虚拆除玩家出生点基地建筑，触发暴雪原生常规对战判负机制（`MeleeCheckForLosersAndVictors` -> `MeleeGetAllyStructureCount == 0`），导致英雄存活却被强制判定失败。此外，旧版避难所盲目在地图四角选址，偶尔刷在下层悬崖边缘或凹坑，导致英雄复活后永久卡在悬崖下无法返回主战场。
- **零破坏原生解决方案**：不修改暴雪原生胜负判定规则，而是在地图开局 1.5 秒自动为人类玩家在基地附近连通平地生成一座绝对无敌的建筑单位 **测试酒馆·无敌避难所 (`n003`)**。由于玩家恒拥有一座无敌建筑，引擎的存活建筑计数器恒大于0，从底层杜绝判负退出。
- **同层连通平地选址算法 (`Refuge_IsSafeTerrainPoint` & `Refuge_InitForPlayer` v6.2)**：
  - **Pass 1（首选连通高地/平地）**：计算自地图中心向外扩散角度，以 `searchR` 从 550 到 1600 码（步长 128）按 16 个方向进行同心圆扫描。要求目标点与主基地悬崖高程严格一致（`baseCliff`）、周围 224 码内 8 个方位点全部满足同高程可通行且可建，并验证与基地连线上 $t=0.25, 0.50, 0.75$ 三个中间点高程均一致，确保避难所与主基地同处一片无断崖隔离的连通平地！
  - **Pass 2（放宽同层兜底）**：若连线上有特殊障碍，在 400~1800 码同层平地内搜索合格点；若仍未找到，直接稳妥落于主基地出生点。
- **全英雄支持与安全复活坐标算法 (`Refuge_CalcSafeReviveXY` v6.2)**：
  - 酒馆拥有复活与全英雄训练列表，可随时用金币/木材购买复活或训练。真英雄阵亡 15 秒后触发免费自动复活；
  - 彻底废除旧版硬编码 `-150` 偏移容易掉下悬崖的缺陷，采用螺旋算法在避难所周围 160~520 码内计算四向 96 码全通行的安全复活点 `(udg_Refuge_SafeX, udg_Refuge_SafeY)`，并激荡复活圣光！
- **AI 锁定规避**：所有战略部队进军与技能索敌逻辑全域排除无敌单位与 `n003`，电脑部队绝不会围攻或被避难所吸引卡死。
- **随时迁移指令 (`-refuge` v6.2)**：玩家在聊天框输入 `-refuge`，避难所会在英雄周围 250~900 码内寻找同层安全平地迁移，绝不再盲目位移导致坠崖！

### 9.5 紧急脱离卡点指令 (`-unstuck`) 与酒馆/祭坛复活纠偏 (v6.2 新增)
- **酒馆/祭坛手动复活防卡死拦截 (`Wild_OnHeroReviveFinish`)**：
  - 玩家在任意酒馆或祭坛手动购买复活英雄时，触发器实时校验复活坐标的通行度与悬崖高程。若检测到英雄被挤入不可通行障碍或处于孤立断崖下层，系统将自动调用安全坐标算法瞬间将英雄纠偏并传送至避难所或主基地平地，彻底根绝卡死隐患！
- **紧急脱离卡点指令 (`-unstuck`)**：
  - 玩家在游戏聊天框输入 **`-unstuck`**：
  - 系统立即枚举该玩家所有存活真英雄，瞬间将其安全传送回主基地出生点平地（`startX, startY`）；
  - 激荡群体传送光效（`MassTeleportTarget`），向玩家广播确认信息，并在小地图上闪烁高亮出生点坐标，随时拯救误入悬崖或地形死角的英雄！"""

    assert old_sec94 in text
    text = text.replace(old_sec94, new_sec94)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')

    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.2!")

if __name__ == '__main__':
    update_readme()
