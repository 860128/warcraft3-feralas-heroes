# -*- coding: utf-8 -*-
import glob
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v6.7'
new_title_zhcn = '测试版v6.8'
old_title_zhtw = '測試版v6.7'
new_title_zhtw = '測試版v6.8'

new_desc_zhcn = '五英雄全能对战版 v6.8：修复实验小兵[W]暗影突袭Cast=0每帧爆跳致死Bug，现为0直接伤害的纯14重Debuff诅咒！基地旁免费生成[u00B]（-buffunit可再召唤），[Q]全光环+全Buff（不含魔免）。'
new_desc_zhtw = '五英雄全能對戰版 v6.8：修復實驗小兵[W]暗影突襲Cast=0每幀爆跳致死Bug，現為0直接傷害的純14重Debuff詛咒！基地旁免費生成[u00B]（-buffunit可再召喚），[Q]全光環+全Buff（不含魔免）。'

updated_count = 0
multiline_errors = []

for p in sorted(files):
    with open(p, 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    raw_text = data[3:].decode('utf-8', errors='ignore') if has_bom else data.decode('utf-8', errors='ignore')
    is_crlf = '\r\n' in raw_text
    norm_text = raw_text.replace('\r\n', '\n')

    changed = False
    if old_title_zhcn in norm_text:
        norm_text = norm_text.replace(old_title_zhcn, new_title_zhcn)
        changed = True
    if old_title_zhtw in norm_text:
        norm_text = norm_text.replace(old_title_zhtw, new_title_zhtw)
        changed = True

    target_desc = new_desc_zhtw if 'zhTW' in p else new_desc_zhcn
    m3 = re.search(r'(STRING\s+3\s*\n\{\n)(.*?)(\n\})', norm_text, re.DOTALL)
    if m3 and m3.group(2) != target_desc:
        norm_text = norm_text[:m3.start(2)] + target_desc + norm_text[m3.end(2):]
        changed = True

    if changed:
        out_text = norm_text.replace('\n', '\r\n') if is_crlf else norm_text
        out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
        with open(p, 'wb') as f:
            f.write(out_bytes)
        updated_count += 1
        print(f"Updated {p}")

    for m in re.finditer(r'STRING\s+(\d+)\s*\n\{\n(.*?)\n\}', norm_text, re.DOTALL):
        sid = m.group(1)
        body = m.group(2)
        if '\n' in body:
            multiline_errors.append((p, sid))

assert updated_count >= 12, f"Expected >= 12 files updated, got {updated_count}"
assert not multiline_errors, f"Multiline STRING entries found: {multiline_errors}"
print(f"Total updated: {updated_count}/{len(files)}, multiline STRING errors: 0")
