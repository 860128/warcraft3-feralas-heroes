# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.7 (Release v6.7)**"
    new_ver = "**当前版本：测试版v6.8 (Release v6.8)**"
    assert old_ver in text, "Missing old version header"
    text = text.replace(old_ver, new_ver, 1)

    old_sec = "### 9.7 实验单位【实验小兵 · 万象状态师】(`u00B`) 与全 Buff / 全 Debuff 测试系统 (`v6.7`)"
    new_sec = "### 9.7 实验单位【实验小兵 · 万象状态师】(`u00B`) 与全 Buff / 全 Debuff 测试系统 (`v6.8` 修复纯 0 伤害减益)"
    assert old_sec in text, "Missing Section 9.7 heading"
    text = text.replace(old_sec, new_sec, 1)

    old_debuff = "- **`[W]` 万厄全 Debuff 诅咒 (`A061`, `A075`~`A082`)**：\n  - 同时对目标附加 **14 重魔兽经典负面状态**：诱捕网、残废 (`-75%` 移速 `-50%` 攻速 `-50%` 攻击)、减速、诅咒 (`33%` Miss)、精灵之火 (`-4` 甲+反隐)、酸液炸弹 (`-5` 甲+每秒腐蚀)、恐怖嚎叫 (`-50%` 攻击)、醉酒云雾 (`65%` Miss + `50%` 减速)、沉默术（禁技能）、灵魂燃烧 (`-50%` 伤害+沉默灼烧)、暗影突袭、纠缠根须（定身+DoT）、寒冰霜冻与妖术（刻意省略吹风/沉睡/放逐，确保目标依然可被集火击杀检验强度）。"
    new_debuff = "- **`[W]` 万厄全 Debuff 诅咒 (`A061`, `A075`~`A082`, `v6.8` 零伤害纯减益修复)**：\n  - 同时对目标附加 **14 重魔兽经典负面状态**：诱捕网、残废 (`-75%` 移速 `-50%` 攻速 `-50%` 攻击)、减速、诅咒 (`33%` Miss)、精灵之火 (`-4` 甲+反隐)、酸液炸弹 (`-5` 甲)、恐怖嚎叫 (`-50%` 攻击)、醉酒云雾 (`65%` Miss + `50%` 减速)、沉默术（禁技能）、灵魂燃烧 (`-50%` 伤害+沉默)、暗影突袭 (`-50%` 减速)、纠缠根须（纯定身缴械）、寒冰霜冻（纯冰冻减速）与妖术（刻意省略吹风/沉睡/放逐，且所有直接/DoT 伤害归零并恢复 `AEsh` 的 `Cast = 3.0s`，杜绝每帧爆跳伤害误杀测试单位）。"
    assert old_debuff in text, "Missing Section 9.7 Debuff block"
    text = text.replace(old_debuff, new_debuff, 1)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.8!")


if __name__ == '__main__':
    update_readme()
