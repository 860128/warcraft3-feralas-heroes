import os, glob, re

name_str = "测试版v1.3"
desc_str = "幻梦大师测试图 v1.3：移除技能漂浮文字；支持复制农民与小精灵等全部单位；英雄幻影不占左侧头像、阵亡不进祭坛、绝不抢夺本体经验；修复三技能图标。"

def update_wts(src_path, dst_path):
    with open(src_path, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig', errors='ignore')
    # Normalize to \n first
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    text = re.sub(r'STRING 1\s*\{\s*[^}]*\}', f'STRING 1\n{{\n{name_str}\n}}', text)
    text = re.sub(r'STRING 3\s*\{\s*[^}]*\}', f'STRING 3\n{{\n{desc_str}\n}}', text)

    # Convert back to \r\n exactly once
    out_bytes = text.replace('\n', '\r\n').encode('utf-8')
    if has_bom:
        out_bytes = b'\xef\xbb\xbf' + out_bytes

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'wb') as f:
        f.write(out_bytes)

update_wts("raw/war3map.wts", "payload/war3map.wts")

for mod in glob.glob("raw/_Locales/*.w3mod"):
    loc_name = os.path.basename(mod)
    src_wts = os.path.join(mod, "war3map.wts")
    if os.path.exists(src_wts):
        dst_wts = os.path.join("payload", "_Locales", loc_name, "war3map.wts")
        update_wts(src_wts, dst_wts)

print("Clean single-line wts written.")
