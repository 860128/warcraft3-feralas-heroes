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

    # 1. Update version on line 2
    old_v_line = "**当前版本：测试版v5.7 (Release v5.7)**"
    new_v_line = "**当前版本：测试版v5.8 (Release v5.8)**"
    assert old_v_line in text, "Could not find version line in README.md"
    text = text.replace(old_v_line, new_v_line, 1)

    # 2. Update TOC item 8
    old_toc = "8. [英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.7 3D因果法轮动态律、W退魔被动特攻、四大被动深度无效化与友方技能净化)](#8-英雄-5异界神将魔虚罗-h006-机制与-jass-架构-v57-3d因果法轮动态律w退魔被动特攻四大被动深度无效化与友方技能净化)"
    new_toc = "8. [英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.8 法轮微速强制锁停、破法穿透·反魔虚罗内战破局法则)](#8-英雄-5异界神将魔虚罗-h006-机制与-jass-架构-v58-法轮微速强制锁停破法穿透反魔虚罗内战破局法则)"
    assert old_toc in text, "Could not find TOC item 8 in README.md"
    text = text.replace(old_toc, new_toc, 1)

    # 3. Update Section 8 heading
    old_h8 = "## 8. 英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.7 3D因果法轮动态律、W退魔被动特攻、四大被动深度无效化与友方技能净化)"
    new_h8 = "## 8. 英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.8 法轮微速强制锁停、破法穿透·反魔虚罗内战破局法则)"
    assert old_h8 in text, "Could not find Section 8 heading in README.md"
    text = text.replace(old_h8, new_h8, 1)

    # 4. Insert Section 8.8 right after Section 8.7 (before Section 9)
    target_end_87 = """4. **修复“误适应友方/自施法辅助技能（例如回春术）” Bug**：
   - 编写 `Maho_IsNonHostileSpell` 函数，彻底过滤回春术、医疗、治疗波、圣光术、嗜血术、霜冻护甲、心火等所有纯增益/恢复技能；
   - 严格重构 `Maho_OnAnySpellEffect`：单体指向技能唯有以魔虚罗为目标时才记录适应，绝不再因敌人在周围自愈或奶队友而误把回春术塞入魔虚罗因果档案；
   - 清理 Q 主动解析中的非敌对技能，确保档案绝对纯净。

---"""

    section_88 = """4. **修复“误适应友方/自施法辅助技能（例如回春术）” Bug**：
   - 编写 `Maho_IsNonHostileSpell` 函数，彻底过滤回春术、医疗、治疗波、圣光术、嗜血术、霜冻护甲、心火等所有纯增益/恢复技能；
   - 严格重构 `Maho_OnAnySpellEffect`：单体指向技能唯有以魔虚罗为目标时才记录适应，绝不再因敌人在周围自愈或奶队友而误把回春术塞入魔虚罗因果档案；
   - 清理 Q 主动解析中的非敌对技能，确保档案绝对纯净。

---

### 8.8 法轮出生自转三重彻底根治与【破法穿透·反魔虚罗内战破局法则】 (v5.8 重磅更新)
1. **彻底根治魔虚罗刚出生未适应时法轮偷转 Bug（三重根治防御体系）**：
   - **收紧追击移速判定**：旧版本仅判断 `GetUnitCurrentOrder != 0`，导致英雄刚从祭坛出生走向集结点（周围空无一人）即误触发“追击适应”并带动法轮旋转。v5.8 引入 `Maho_HasEnemyNearby(player, x, y, 1600.0)` 严格判定，**唯有在移动且周围 1600 码内有活体敌人或已锁定 Q 目标时**，才算作“追击适应”，在空旷基地散步绝不触发适应、绝不转动法轮！
   - **`0.0001` 极微速冻结取代 `0.0`**：重制版 2.0.3 引擎底层在异步加载或特效重置时偶会将 `0.0` 视为异常值回退为 `1.0` 正常速播放。v5.8 将静止时间流速全线重构为 `0.0001`（视觉上绝对零转动，但严格大于 0，杜绝底层引擎自动回退机制）；
   - **`Maho_StealthLoop` (0.05秒) 持续强制锁死**：每 0.05 秒循环中，只要转动倒计时归零且法轮存在，持续执行 `BlzSetSpecialEffectTimeScale(udg_Maho_WheelFx[pId], 0.0001)`，确保模型异步加载完成后的下一帧瞬间锁死制动，彻底杜绝任何偷转！
2. **重磅破局机制：【破法穿透 · 反魔虚罗适应】（彻底杜绝内战 100% 免疫互刮死局）**：
   - **设计背景**：在多个魔虚罗同场竞技（如 `-m5` 8 魔虚罗大战）时，若双方防御适应均达到 100% 绝对免疫，将陷入永无休止的平局。
   - **反适应穿透度全局变量**：`real array udg_Maho_AntiMahoAdapt`（范围 `0.00` ~ `1.00` 即 0%~100%，代表魔虚罗对敌方同类防御适应法则的破法穿透深度）；
   - **增长途径**：
     - **互殴斩击增长**：每次普攻或 W 斩击敌方魔虚罗（即使对方处于 100% 免疫），攻击方永久累积 **`+2.0%`（`+0.02`）** 破法穿透度，并触发法轮清脆转动；首次达到 100% 时触发全图庄严播报：`【法轮终极反制 · 破法适应完成！】`；
     - **Q【法轮注视】持续解析**：Q 因果锁定敌方魔虚罗存活体时，每秒自动累积 **`+2.5%`（`+0.025`）** 破法穿透；
     - **E【法轮强转】爆发推进**：在锁定敌方魔虚罗时施放 E 强转，瞬间爆发推进 **`+6.0%`（`+0.06`）** 破法穿透；
     - **真死惩罚**：魔虚罗真正阵亡时，破法穿透度乘以 `0.70` 回退 30%；
   - **伤害穿透计算（`DM_OnDamaged`）**：
     - 在防御减免分支中，针对敌方魔虚罗攻击施加破法剥离：
       `effResist = effResist * (1.0 - udg_Maho_AntiMahoAdapt[srcMahoPid])`；
     - 对方即使拥有 100% 绝对免疫，我方反适应度从 0% 攀升至 100% 的过程中，我方对敌造成的伤害比例也将从 0% 平滑攀升至 100% 全额伤害！双方均可相互破法，实现极致精彩的因果博弈！
   - **UI 与 R 键档案全面集成**：当 `udg_Maho_AntiMahoAdapt > 0.0` 时，在 R 键技能面板与全图因果档案中实时打印：`[破法穿透·反魔虚罗适应] 穿透同类防御免疫: XX%`！

---"""

    assert target_end_87 in text, "Could not find end of Section 8.7 in README.md"
    text = text.replace(target_end_87, section_88, 1)

    out_text = text.replace('\n', '\r\n')
    out_bytes = b'\xef\xbb\xbf' + out_text.encode('utf-8')

    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("Successfully updated README.md with Section 8.8, single UTF-8 BOM, and CRLF!")

if __name__ == '__main__':
    update_readme()
