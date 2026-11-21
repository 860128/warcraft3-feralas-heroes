# -*- coding: utf-8 -*-
import glob
import os
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v5.5'
new_title_zhcn = '测试版v5.6'
old_title_zhtw = '測試版v5.5'
new_title_zhtw = '測試版v5.6'

old_desc_zhcn = '五英雄全能对战版 v5.5：魔虚罗涅槃金卵真凶闪退修复！独立金卵实体单位[u004]+脱离伤害栈延迟变蛋，特效路径彻底矫正！'
new_desc_zhcn = '五英雄全能对战版 v5.6：魔虚罗本名与职业称号校准，暴雪原版炽焰熔岩魔像金焰神将，自制3D连续旋转八握剑法轮[MahoWheel.mdx]！'

old_desc_zhtw = '五英雄全能對戰版 v5.5：魔虛羅涅槃金卵真兇閃退修復！獨立金卵實體單位[u004]+脫離傷害棧延遲變蛋，特效路徑徹底矯正！'
new_desc_zhtw = '五英雄全能對戰版 v5.6：魔虛羅本名與職業稱號校準，暴雪原版熾焰熔岩魔像金焰神將，自製3D連續旋轉八握劍法輪[MahoWheel.mdx]！'

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
        out_text = norm_text.replace('\n', '\r\n') if is_crlf else norm_text
        out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
        with open(p, 'wb') as f:
            f.write(out_bytes)
        updated_count += 1
        print(f"Updated {p}")

print(f"Total updated: {updated_count}")
