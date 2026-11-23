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
    old_ver = "**当前版本：测试版v6.0 (Release v6.0)**"
    new_ver = "**当前版本：测试版v6.1 (Release v6.1)**"
    assert old_ver in text
    text = text.replace(old_ver, new_ver)

    # 2. Update directory
    old_toc = "8. [英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v6.0 四阶破法升维彩蛋、五色纯白神轮与凤凰金卵斩碎机制)](#8-英雄-5异界神将魔虚罗-h006-机制与-jass-架构-v60-四阶破法升维彩蛋五色纯白神轮与凤凰金卵斩碎机制)"
    new_toc = "8. [英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v6.1 根治2血站桩活死人、秘籍豁免通道与双步换肤外观守护)](#8-英雄-5异界神将魔虚罗-h006-机制与-jass-架构-v61-根治2血站桩活死人秘籍豁免通道与双步换肤外观守护)"
    assert old_toc in text
    text = text.replace(old_toc, new_toc)

    # 3. Add Section 8.10 before Section 9
    sec_810 = """### 8.10 根治 2 血站桩无敌活死人 Bug、秘籍豁免通道与翼化双步换肤外观守护 (v6.1 关键热更)
1. **彻底根治“魔虚罗 1~2 血站桩不战斗、无敌打不动”活死人 Bug**：
   - **底层元凶定位**：魔虚罗受到致死伤害触发金卵涅槃时，底层会将本体暂停（`PauseUnit(h, true)`）并挂上引擎级无敌（`SetUnitInvulnerable(h, true)`）。在极少数金卵异常提前清除、死锁或 `udg_Ninja_DeathLock` 递归锁拦截时，本体未能正常执行复活解除回调，导致魔虚罗永久保留在“暂停 + 引擎级无敌 + 1~2 血”状态，成为既不战斗也无法被杀死的“活死人”；
   - **双重无条件解冻与看门狗自愈体系**：
     - **`Maho_OnEggComplete(pId)` 无条件重置**：无论英雄句柄是否为 null，无条件先将 `udg_Maho_InEgg`、`udg_Maho_PendingEggEnter`、`udg_Maho_EggTimer` 彻底清空并清理金卵，句柄存在时必定解冻、解除无敌、恢复不透明度并满血；
     - **`Maho_CapTimerLoop` 每秒看门狗巡检**：只要魔虚罗存活且不在蛋中（`not udg_Maho_InEgg and not udg_Maho_PendingEggEnter`），一旦检测到 `IsUnitPaused(h)` 或 `BlzIsUnitInvulnerable(h)`，下一秒立即强制解冻、解除无敌并恢复金色显形！若金卵超时（`EggTimer <= 0`）或金卵实体丢失/已阵亡，瞬间强行触发破茧完成！
     - **`Maho_ApplyDeathPenalty(pId)` 兜底解冻**：任何途径真正阵亡时，必先解除 `SetUnitInvulnerable` 与 `PauseUnit`，杜绝任何复活后残留无敌状态。
2. **`whosyourdaddy` 秘籍无敌清场与绝对致死豁免通道**：
   - 原版魔兽秘籍 `whosyourdaddy` 本质是将普攻输出放大 100 倍（单次达数万~数十万），依然会走 `DM_OnDamaged` 伤害回调栈；
   - 当魔虚罗将某项抗性叠至 100% 绝对免疫时，`whosyourdaddy` 的巨额伤害也会被 `effResist >= 0.9999` 强制归零；
   - **秘籍穿透豁免通道**：在 `DM_OnDamaged` 中判定，只要原始伤害 `dmg >= 50000.0`（常规对局绝无可能单发达到 5 万，实锤为玩家输入了测试秘籍），**立即穿透 100% 适应免疫与凤凰金卵保护，且直接越过金卵涅槃触发判定**，实现 100% 真实一击秒杀，确保开发者与玩家使用秘籍清场测试畅通无阻！
3. **二段翼化魔虚罗战斗中突变回小火人根治（双步换肤 + 解控外观守护）**：
   - **底层引擎陷阱**：在魔兽争霸3重制版 2.0.3 引擎中，单位受到敌方【妖术 (`'Bhex'`)】、【变形术 (`'Bply'`)】或特殊变形状态后，当魔虚罗自动驱散负面控制（`UnitRemoveBuffs`）时，引擎 C++ 底层会自动从 `unit.ini` 重新载入 `H006` 的默认外观（即初始熔岩魔像 `LavaSpawn`），导致二阶段 `'nbal'` 皮肤与飞行高度瞬间被冲掉；
   - **双步强制换肤刷新**：在 `Maho_ApplyAppearance` 的翼化分支中，先重置为 `H006` 再重置为 `nbal`，强刷引擎渲染缓存：
     ```jass
     call BlzSetUnitSkin(h, 'H006')
     call BlzSetUnitSkin(h, 'nbal')
     ```
   - **`udg_Maho_ReskinTimer` (0.15s) 驱散外观重载守护**：在 `Maho_StealthLoop` 自动驱散与 E 技能【法轮强转】驱散后，若魔虚罗处于翼化状态，立即启动 0.15 秒延迟换肤定时器，待妖术/变形状态完全结束的下一刻瞬间重新刷新圣金带翼末日神将与 240 飞行高度！
   - **每秒守护巡检**：`Maho_CapTimerLoop` 每秒检测若为翼化状态却 `BlzGetUnitSkin(h) != 'nbal'` 或飞行高度 < 100，1 秒内无感自动重置外观，永不退化！

---

"""

    target_sec9 = "\n## 9. 测试模式、沙盒指令与 AI 战略统帅体系"
    assert target_sec9 in text
    text = text.replace(target_sec9, "\n" + sec_810 + "## 9. 测试模式、沙盒指令与 AI 战略统帅体系")

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')

    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.1!")

if __name__ == '__main__':
    update_readme()
