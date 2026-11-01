# -*- coding: utf-8 -*-
import os, glob, re

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
name_str = "测试版v1.6"
desc_str = "幻梦大师与魔音忍者测试图 v1.6：修复独断万古与他化自在技能图标，修复魔音忍者分身分流本体经验问题（全新非英雄分身机制，不抢经验、不占头像、不进祭坛）。"

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

# Update root payload wts
update_wts(os.path.join(ROOT, "raw", "war3map.wts"), os.path.join(ROOT, "payload", "war3map.wts"))

# Update all locale wts
for mod in glob.glob(os.path.join(ROOT, "raw", "_Locales", "*.w3mod")):
    loc_name = os.path.basename(mod)
    src_wts = os.path.join(mod, "war3map.wts")
    if os.path.exists(src_wts):
        dst_wts = os.path.join(ROOT, "payload", "_Locales", loc_name, "war3map.wts")
        update_wts(src_wts, dst_wts)

print("v1.6 wts files successfully written!")
