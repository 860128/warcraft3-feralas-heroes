# -*- coding: utf-8 -*-
import glob
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v6.9'
new_title_zhcn = '测试版v6.10'
old_title_zhtw = '測試版v6.9'
new_title_zhtw = '測試版v6.10'

new_desc_zhcn = '五英雄全能对战版 v6.10：实验小兵[E]封印术·山镜像入山与夺舍破封出山均保持满血满蓝全盛状态并净化负面状态、重置冷却！含[Q]全buff、[W]全debuff与[R]解封·破山，-mount 随时观战！'
new_desc_zhtw = '五英雄全能對戰版 v6.10：實驗小兵[E]封印術·山鏡像入山與奪舍破封出山均保持滿血滿藍全盛狀態並淨化負面狀態、重置冷卻！含[Q]全buff、[W]全debuff與[R]解封·破山，-mount 隨時觀戰！'

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
