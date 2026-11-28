# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.3 (Release v6.3)**"
    new_ver = "**当前版本：测试版v6.4 (Release v6.4)**"
    assert old_ver in text
    text = text.replace(old_ver, new_ver)

    old_sec96 = """### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.3 重磅新增)"""
    new_sec96 = """### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.4 热修完备)"""
    assert old_sec96 in text
    text = text.replace(old_sec96, new_sec96)

    old_line = """- **沙盒测试捷径**：新增 **`-kill` / `-assassin`** 一键定位选中最近介绍所；新增 **`-archimonde`** 在身边召唤 10 级中立敌对阿克蒙德用于当场下单实测。"""
    new_line = """- **全图通缉广播与热修修复 (v6.4)**：
  - 彻底根治 `BlzUnitHideAbility` 引用计数叠加导致悬赏头像槽永久隐形的 Bug，改用 `UnitRemoveAbility` + `UnitAddAbility` 零故障动态重绘全部敌方头像与实时报价，全图视野改用 `udg_Asn_WorldRect = GetWorldBounds()` 无死角扫描；
  - 下单成功后立即向全图所有玩家（`0..7`）放送红字通缉公告：**`【全图通缉 · 暗杀契约生效！】某势力的【某英雄】已经被下单买命！`** 并在目标位置闪烁红色警示 Ping；
  - 点击望远镜 (`A05A`) 也会在屏幕列出全部当前可下单敌方势力、目标与实时报价。
- **沙盒测试捷径**：新增 **`-kill` / `-assassin`** 一键定位选中最近介绍所；新增 **`-archimonde`** 在身边召唤 10 级中立敌对阿克蒙德用于当场下单实测。"""
    assert old_line in text
    text = text.replace(old_line, new_line)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.4!")

if __name__ == '__main__':
    update_readme()
