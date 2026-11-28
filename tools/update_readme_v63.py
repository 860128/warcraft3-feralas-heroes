# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.2 (Release v6.2)**"
    new_ver = "**当前版本：测试版v6.3 (Release v6.3)**"
    assert old_ver in text
    text = text.replace(old_ver, new_ver)

    old_anchor = """---

## 10. 魔兽争霸III引擎避坑指南与开发铁律 (Golden Rules)"""

    new_sec96 = """### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.3 重磅新增)
- **建筑机制与动态悬赏面板 (`n005`, `A050`~`A05A`)**：
  - 在东西两座中立酒馆旁各开放一座无敌【暗杀介绍所】，属于中立势力 `Player(25)`，仅对人类玩家共享操作界面用于下单买杀（AI 电脑不会使用）。
  - 介绍所实时扫描场上所有敌方英雄与强力 Boss（含 `-spawn`、`-archimonde` 与处于金卵 `u004` 状态的魔虚罗），动态把 `A050`~`A059` 图标替换成目标**真实头像**（含 `H004` 四阶形态与 `H006` 翼化动态头像），按实时等级、血量、攻击、护甲与成长层数精准计算黄金报价（`400` 起步，高发育魔虚罗可达上万金）。
- **独立中立执行者 (`Player(26)`)**：
  - 下单后从介绍所派出对应克制类型的中立杀手小队（雇主**完全无法操控**杀手），拥有视野共享便于观战；
  - 途中若有敌方部队、防御塔或任意第三方单位阻拦或攻击杀手，杀手将**顺路转火以 2.5 倍碎障伤害将其毁灭**后再继续追猎；
  - 若当前波次杀手被全歼而目标仍存活（或靠重生复生站起），公会将在 3 秒后派出人数 `+2`（上限 12）、属性大幅增幅的下一波小队，直到目标彻底死亡为止。
- **六大专属机制硬克制杀手单位 (`u005`~`u00A`)**：
  - `u005` **破法弑神者（克制魔虚罗）**：混乱远程高攻、100% 穿透适应度与护甲、不触发法轮任何成长与变蛋，可直接击破并当场斩碎涅槃金卵 `u004`。
  - `u006` **禁魔镇魂石像（克制魔音忍者）**：永久魔免免疫竭心光环、因果必中破闪避、真视、对分身/神尊/召唤物 10 倍伤害、击中本体强关光环并封印业火复仇与替身替死。
  - `u007` **净世焚虫机甲（克制异种之源）**：魔免免疫 `A022` 吞噬并反噬 10% 血量、震破潜地与伪装、压制三阶吸血并附加净世真伤。
  - `u008` **猎灵破法裁决者（克制万灵化身）**：550 码对空压制、对伥鬼与召唤物 8 倍秒清、无视魔免斩首真伤，绝不被收编为伥鬼。
  - `u009` **破妄真瞳猎手（克制幻梦大师）**：免疫幻梦奴役、对幻象镜像 10 倍伤害、真视破潜行并高额真伤直取本体。
  - `u00A` **圣光混乱裁决者（克制阿克蒙德等恶魔领主与常规英雄）**：混乱圣光高额纯粹灌伤，迅速击穿阿克蒙德等高血高甲 Boss。
- **沙盒测试捷径**：新增 **`-kill` / `-assassin`** 一键定位选中最近介绍所；新增 **`-archimonde`** 在身边召唤 10 级中立敌对阿克蒙德用于当场下单实测。

---

## 10. 魔兽争霸III引擎避坑指南与开发铁律 (Golden Rules)"""

    assert old_anchor in text
    text = text.replace(old_anchor, new_sec96)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.3!")

if __name__ == '__main__':
    update_readme()
