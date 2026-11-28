# -*- coding: utf-8 -*-
import glob
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v6.8'
new_title_zhcn = '测试版v6.9'
old_title_zhtw = '測試版v6.8'
new_title_zhtw = '測試版v6.9'

new_desc_zhcn = '五英雄全能对战版 v6.9：实验小兵新增[E]封印术·山（无视魔免）与[R]解封·破山！将任意单位封入正北山巅孤立结界与全属性/全技能/全AI镜像死斗，镜像胜出归己方，-mount 随时观战！'
new_desc_zhtw = '五英雄全能對戰版 v6.9：實驗小兵新增[E]封印術·山（無視魔免）與[R]解封·破山！將任意單位封入正北山巔孤立結界與全屬性/全技能/全AI鏡像死鬥，鏡像勝出歸己方，-mount 隨時觀戰！'

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
