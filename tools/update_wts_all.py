import os, glob

name_str = "测试版 v1.2 (幻梦大师)"
desc_str = """【测试版 v1.2 更新日志】
新增全新敏捷型第五英雄：幻梦大师（四族祭坛均可招募）

1.【Q技能 - 镜像与潜行】
- 召唤强力镜像（满级100%攻防血量），本体在分身分裂完成后自动进入绝对隐匿状态（疾风步机制，半透明显示并获得移速加成），攻击或施法破隐，破隐一击附带高额背刺额外伤害。

2.【W技能 - 幻梦奴役】
- 可强行操控任何敌军、野怪或中立单位/建筑（持续30秒/2分钟/10分钟）。
- 阵亡保护机制：若受控的敌方英雄在控制期间阵亡，所有权将在死亡瞬间自动归还原始玩家，杜绝己方祭坛错误复活敌方英雄的恶性BUG。

3.【E技能 - 万象皆虚】
- 还原纯净的地面绿色AOE施法范围指示圈（基于Channel纯净点目标），彻底移除任何沉默负面效果！
- 复制范围内全部敌友单位的真实幻象，幻象拥有全套技能与物品，持续15分钟。
- 经验共享机制修复：移除幻象英雄的英雄经验判定，幻象消灭敌人提供经验，但绝不会分薄/瓜分本体英雄的任何经验！

4.【R技能 - 幻界主宰（神杖质变）】
- 学习后全面激活前三技能机制升华：
  · 镜像潜行：破隐一击提升至250点额外伤害并附带眩晕，潜行移速提升至极限522；
  · 幻梦奴役：三级直接晋级为永久掌控，技能冷却时间大幅缩短；
  · 万象皆虚：施法范围大幅扩增+100码，幻象攻击力与攻击速度全面飞跃！"""

def update_wts(src_path, dst_path):
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Replace STRING 1
    import re
    text = re.sub(r'STRING 1\s*\{\s*[^}]*\}', f'STRING 1\n{{\n{name_str}\n}}', text)
    # Replace STRING 3
    text = re.sub(r'STRING 3\s*\{\s*[^}]*\}', f'STRING 3\n{{\n{desc_str}\n}}', text)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(text)

# Update root war3map.wts
update_wts("raw/war3map.wts", "payload/war3map.wts")

# Update all locale wts
for mod in glob.glob("raw/_Locales/*.w3mod"):
    loc_name = os.path.basename(mod)
    src_wts = os.path.join(mod, "war3map.wts")
    if os.path.exists(src_wts):
        dst_wts = os.path.join("payload", "_Locales", loc_name, "war3map.wts")
        update_wts(src_wts, dst_wts)
        print("Updated locale:", loc_name)

print("All wts updated successfully!")
