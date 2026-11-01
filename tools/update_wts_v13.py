import os, glob, re

name_str = "测试版 v1.3 (幻梦大师)"
desc_str = """【测试版 v1.3 更新日志】
新增全新敏捷型第五英雄：幻梦大师（四族祭坛均可招募）

【v1.3 重点修复】
1. 全面移除所有技能施放与攻击时的漂浮文字提示，画面清爽纯粹。
2. 修复三技能【万象皆虚】无法复制农民、小精灵、苦工、侍僧等工人单位的问题，现在范围内一切非建筑活体单位均可复制。
3. 重构三技能复制英雄的底层机制：改为生成100%全额攻防血量的真实英雄幻影（持续15分钟）——左侧屏幕不再出现多余英雄头像、阵亡后直接消散绝不进入祭坛复活列表、且绝不抢夺或分薄本体英雄的一分一毫经验！
4. 修复三技能【万象皆虚】与四技能【幻界主宰】图标显示为绿块的材质路径问题。"""

def update_wts(src_path, dst_path):
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    text = re.sub(r'STRING 1\s*\{\s*[^}]*\}', f'STRING 1\n{{\n{name_str}\n}}', text)
    text = re.sub(r'STRING 3\s*\{\s*[^}]*\}', f'STRING 3\n{{\n{desc_str}\n}}', text)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(text)

update_wts("raw/war3map.wts", "payload/war3map.wts")

for mod in glob.glob("raw/_Locales/*.w3mod"):
    loc_name = os.path.basename(mod)
    src_wts = os.path.join(mod, "war3map.wts")
    if os.path.exists(src_wts):
        dst_wts = os.path.join("payload", "_Locales", loc_name, "war3map.wts")
        update_wts(src_wts, dst_wts)
        print("Updated locale:", loc_name)

print("All wts updated to v1.3!")
