# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    if has_bom:
        text = data[3:].decode('utf-8')
    else:
        text = data.decode('utf-8')

    text = text.replace('\r\n', '\n')

    # 1. Update version on line 2
    old_v_line = "**当前版本：测试版v5.8 (Release v5.8)**"
    new_v_line = "**当前版本：测试版v5.9 (Release v5.9)**"
    assert old_v_line in text, "Could not find version line in README.md"
    text = text.replace(old_v_line, new_v_line, 1)

    # 2. Add section 4.3 update
    target_43 = """    3. 在 `DM_OnHeroRevivable` 触发器中，若检索到单位位于 `udg_FakeHeroGroup`，立即阻断并将其注销，绝不进入祭坛复活队列！"""
    
    addition_43 = """    3. 在 `DM_OnHeroRevivable` 触发器中，若检索到单位位于 `udg_FakeHeroGroup`，立即阻断并将其注销，绝不进入祭坛复活队列！
- **全维克隆同步重构 (`DM_SyncClonedUnit` + `EVENT_PLAYER_UNIT_SUMMON` 拦截) (v5.9 重大更新)**：
  - **根治进化/变身英雄复制失效**：原生幻象杖及底层 `CreateUnit` 仅从 `unit.ini` 读取模板，不继承英雄运行时通过 `BlzSetUnitSkin`、`SetUnitScale`、`SetUnitFlyHeight`、`BlzSetUnitBaseDamage`、`BlzSetUnitArmor`、`BlzSetUnitAttackCooldown` 等动态修改的战斗状态。
  - **`DM_SyncClonedUnit` 1:1 动态克隆引擎**：
    1. **魔虚罗 (`H006`)**：若目标已翼化升维，分身同步化身圣金带翼末日神将 (`'nbal'`)，拉升 240 飞行高度并赋予对空破空剑气；且完整同步魔虚罗通过挨打与注视叠加的数百点基础攻击力，使幻象具备强横的实战输出！
    2. **异种之源 (`H004`)**：严格同步当前 4 阶段蜕壳进化模型与体型缩放（0阶跳虫、1阶巨蝎、2阶刺蛇、3阶虫皇），2 阶刺蛇分身自动继承 500 码远程酸液弹道！
    3. **万灵化身 (`H005`)**：若目标处于化形形态，分身严格继承当前的 90 种野怪皮肤、体型缩放、飞行状态及远程投射物攻击！
    4. **全动态属性完美复刻**：实时同步目标最大生命/魔法、双武器基础攻击、护甲、攻速与移速，同时施加淡蓝半透明染色标明幻象身份。
  - **双路径拦截保障**：Path A 通过全局环形队列 `udg_DM_CloneOrigList` 在原生幻象生成事件中精准匹配原体并刷新；Path B 在兜底创建时无缝触发同步。"""

    assert target_43 in text, "Could not find target_43 in README.md"
    text = text.replace(target_43, addition_43, 1)

    out_text = text.replace('\n', '\r\n')
    out_bytes = b'\xef\xbb\xbf' + out_text.encode('utf-8')

    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("Successfully updated README.md for v5.9!")

if __name__ == '__main__':
    update_readme()
