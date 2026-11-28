# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.6 (Release v6.6)**"
    new_ver = "**当前版本：测试版v6.7 (Release v6.7)**"
    assert old_ver in text, "Missing old version header"
    text = text.replace(old_ver, new_ver, 1)

    anchor = "\n---\n\n## 10. 魔兽争霸III引擎避坑指南与开发铁律"
    sec_97 = """
### 9.7 实验单位【实验小兵 · 万象状态师】(`u00B`) 与全 Buff / 全 Debuff 测试系统 (`v6.7`)
- **单位定位与获取**：普通步兵模型非英雄实验单位（`u00B`），零人口消耗。开局 `1.80s` 在每位人类玩家基地旁免费自动生成 1 只，也可随时输入 **`-buffunit`** 在英雄/基地旁再召唤测试，专用于评估“全正面叠加 / 全负面叠加”的实战强度上限。
- **`[Q]` 万象全 Buff 加持 (`A060`，不含魔免)**：
  - **9 大满级自身光环 (`A062` 禁用隐藏法术书承载 `A063`~`A06B`，持续 45 秒)**：专注光环 (`+4.5` 甲)、辉煌光环 (`+2.25` 回蓝)、耐久光环 (`+30%` 移速 `+15%` 攻速)、邪恶光环 (`+30%` 移速 `+2.0` 回血)、吸血光环 (`+45%` 近战吸血)、荆棘光环 (`30%` 反伤)、强击光环 (`+30%` 远程攻击)、命令光环 (`+20%` 近战攻击)、科多战鼓 (`+10%` 攻击)——光环范围严格设 `50` 且 `targs = "self"`，绝不外泄给周边单位。
  - **9 大经典主动增益 Buff (`A06C`~`A074`)**：嗜血术 (`+40%` 攻速 `+25%` 移速)、心灵之火 (`+10%` 攻击 `+5` 护甲 `+1.5` 回血)、邪恶狂热 (`+75%` 攻速，`-2 HP/s`)、霜冻护甲 (`+7` 甲并冰冻近战攻击者)、咆哮 (`+25%` 攻击)、返老还童 (`12s` 回复 `400` 血)、闪电护盾 (`20 DPS`)、灵魂链 (`50%` 伤害分摊)、隐身术（置于末尾释放，刻意不包含任何魔免或无敌类 Buff）。
- **`[W]` 万厄全 Debuff 诅咒 (`A061`, `A075`~`A082`)**：
  - 同时对目标附加 **14 重魔兽经典负面状态**：诱捕网、残废 (`-75%` 移速 `-50%` 攻速 `-50%` 攻击)、减速、诅咒 (`33%` Miss)、精灵之火 (`-4` 甲+反隐)、酸液炸弹 (`-5` 甲+每秒腐蚀)、恐怖嚎叫 (`-50%` 攻击)、醉酒云雾 (`65%` Miss + `50%` 减速)、沉默术（禁技能）、灵魂燃烧 (`-50%` 伤害+沉默灼烧)、暗影突袭、纠缠根须（定身+DoT）、寒冰霜冻与妖术（刻意省略吹风/沉睡/放逐，确保目标依然可被集火击杀检验强度）。
"""
    assert anchor in text, "Missing anchor before Section 10"
    text = text.replace(anchor, "\n" + sec_97.strip() + "\n" + anchor, 1)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.7!")


if __name__ == '__main__':
    update_readme()
