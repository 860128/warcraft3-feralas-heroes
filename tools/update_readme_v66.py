# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.5 (Release v6.5)**"
    new_ver = "**当前版本：测试版v6.6 (Release v6.6)**"
    assert old_ver in text, "Missing old version header"
    text = text.replace(old_ver, new_ver, 1)

    old_sec96 = "### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.5 反进化波次重塑与忍者分身全清修复)"
    new_sec96 = "### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.6 新增测试限定自我暗杀挑战)"
    assert old_sec96 in text, "Missing old section 9.6 heading"
    text = text.replace(old_sec96, new_sec96, 1)

    old_shortcut = "- **沙盒测试捷径**：新增 **`-kill` / `-assassin`** 一键定位选中最近介绍所；新增 **`-archimonde`** 在身边召唤 10 级中立敌对阿克蒙德用于当场下单实测。"
    new_shortcut = """- **沙盒测试捷径**：新增 **`-kill` / `-assassin`** 一键定位选中最近介绍所；新增 **`-archimonde`** 在身边召唤 10 级中立敌对阿克蒙德用于当场下单实测。
- **自我暗杀极限耐力挑战（测试期限定，`v6.6`）**：
  - 由单个总开关 `udg_Asn_AllowSelfTest = true` 控制（**后期正式版将一键关闭/移除，仅用于测试期测算真人玩家抵抗波次极限**）。
  - 人类玩家选中暗杀介绍所 (`n005`) 时，榜单首位将显示自己的存活英雄头像（标注 `【自测挑战·对自己下单】` 与实时评估身价），点击即可 **0 黄金免费对自己下单**，也可随时在聊天框输入 **`-killme`**（或 `-selfkill`）一键开启自测，或输入 **`-stopkill`** 手动中止并恢复中立和平。
  - **自测敌对与碎障联动**：仅针对当前自我暗杀开启 `Player(26)` 与测试玩家的敌对状态（不影响并存的其他敌对悬赏契约），玩家自身操控的护卫部队、召唤物、分身/伥鬼与防御塔攻击杀手时均会被标记为阻碍者顺路摧毁；全歼当前波次时会广播【自测波次突破】，主角彻底阵亡后自动结算 **共成功抵挡 X 波，最终倒在第 Y 波强袭之下** 并恢复 `Player(26)` 中立和平。"""
    assert old_shortcut in text, "Missing old sandbox shortcut block"
    text = text.replace(old_shortcut, new_shortcut, 1)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.6!")


if __name__ == '__main__':
    update_readme()
