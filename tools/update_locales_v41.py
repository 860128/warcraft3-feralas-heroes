# -*- coding: utf-8 -*-
import glob
import os
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v4.0'
new_title_zhcn = '测试版v4.1'
old_title_zhtw = '測試版v4.0'
new_title_zhtw = '測試版v4.1'

old_desc_zhcn = '四英雄全能对战【v4.0：异种之源W/R技能说明校准、3阶虫皇W双重锁死4秒CD、移除刺眼绿光柱与暗紫金甲】'
new_desc_zhcn = '四英雄全能对战【v4.1：彻底根除偷取镜像AOmi分身污染与模型卡死Bug，本体与分身100%同步星际进化】'

old_desc_zhtw = '四英雄全能對戰【v4.0：異種之源W/R技能說明校準、3階蟲皇W雙重鎖死4秒CD、移除刺眼綠光柱與暗紫金甲】'
new_desc_zhtw = '四英雄全能對戰【v4.1：徹底根除偷取鏡像AOmi分身污染與模型卡死Bug，本體與分身100%同步星際進化】'

updated_count = 0
for p in files:
    with open(p, 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    if has_bom:
        raw_text = data[3:].decode('utf-8', errors='ignore')
    else:
        raw_text = data.decode('utf-8', errors='ignore')

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
        if is_crlf:
            final_text = norm_text.replace('\n', '\r\n')
        else:
            final_text = norm_text

        out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + final_text.encode('utf-8')
        with open(p, 'wb') as f:
            f.write(out_bytes)
        updated_count += 1
        print(f"Updated {p} -> v4.1")

print(f"Total wts updated: {updated_count}")
