# -*- coding: utf-8 -*-
import glob
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v6.5'
new_title_zhcn = '测试版v6.6'
old_title_zhtw = '測試版v6.5'
new_title_zhtw = '測試版v6.6'

old_desc_zhcn = '五英雄全能对战版 v6.5：暗杀波次随目标实时进化重扫+几何级反超狂暴升级！并彻底修复魔音忍者分身替死与杀手提前消失Bug！'
new_desc_zhcn = '五英雄全能对战版 v6.6：新增测试期限定自我暗杀极限挑战！玩家可在暗杀介绍所免费点击自身头像或输入 -killme 测试真人耐力波数（-stopkill 终止，后期正式版移除）。'

old_desc_zhtw = '五英雄全能對戰版 v6.5：暗殺波次隨目標實時進化重掃+幾何級反超狂暴升級！並徹底修復魔音忍者分身替死與殺手提前消失Bug！'
new_desc_zhtw = '五英雄全能對戰版 v6.6：新增測試期限定自我暗殺極限挑戰！玩家可在暗殺介紹所免費點擊自身頭像或輸入 -killme 測試真人耐力波數（-stopkill 終止，後期正式版移除）。'

updated_count = 0
multiline_errors = []

has_v66_count = 0
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

    if 'zhTW' in p:
        if old_desc_zhtw in norm_text:
            norm_text = norm_text.replace(old_desc_zhtw, new_desc_zhtw)
            changed = True
        elif old_desc_zhcn in norm_text:
            norm_text = norm_text.replace(old_desc_zhcn, new_desc_zhtw)
            changed = True
    else:
        if old_desc_zhcn in norm_text:
            norm_text = norm_text.replace(old_desc_zhcn, new_desc_zhcn)
            changed = True
        elif old_desc_zhtw in norm_text:
            norm_text = norm_text.replace(old_desc_zhtw, new_desc_zhcn)
            changed = True

    if changed:
        out_text = norm_text.replace('\n', '\r\n') if is_crlf else norm_text
        out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
        with open(p, 'wb') as f:
            f.write(out_bytes)
        updated_count += 1
        print(f"Updated {p}")

    if new_title_zhcn in norm_text or new_title_zhtw in norm_text:
        has_v66_count += 1

    # Single-line verification across all STRING blocks
    for m in re.finditer(r'STRING\s+(\d+)\s*\n\{\n(.*?)\n\}', norm_text, re.DOTALL):
        sid = m.group(1)
        body = m.group(2)
        if '\n' in body:
            multiline_errors.append((p, sid))

assert has_v66_count >= 12, f"Expected >= 12 files at v6.6, got {has_v66_count}"
assert not multiline_errors, f"Multiline STRING entries found: {multiline_errors}"
print(f"Verified {has_v66_count}/{len(files)} locale files at v6.6, freshly updated: {updated_count}, multiline STRING errors: 0")
