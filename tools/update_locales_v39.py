# -*- coding: utf-8 -*-
import glob
import os
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v3.8'
new_title_zhcn = '测试版v3.9'
old_title_zhtw = '測試版v3.8'
new_title_zhtw = '測試版v3.9'

old_desc_zhcn = '四英雄全能对战版 v3.8：万灵大军推进AI彻底修复！解除警戒站位锁死，全图动态锁定存活敌方玩家与野怪，出招即刻全军冲锋，告别空地发呆！'
new_desc_zhcn = '四英雄全能对战版 v3.9：异种之源星际虫族四阶蜕壳进化！跳虫->巨蝎->刺蛇->始祖虫皇；全维基因吸收+英雄蚕食翻倍；魔免吸血4秒深渊饕餮！'

old_desc_zhtw = '四英雄全能對戰版 v3.8：萬靈大軍推進AI徹底修復！解除警戒站位鎖死，全圖動態鎖定存活敵方玩家與野怪，出招即刻全軍衝鋒，告別空地發呆！'
new_desc_zhtw = '四英雄全能對戰版 v3.9：異種之源星際蟲族四階蛻殼進化！跳蟲->巨蠍->刺蛇->始祖蟲皇；全維基因吸收+英雄蠶食翻倍；魔免吸血4秒深淵饕餮！'

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
    else:
        if old_desc_zhcn in norm_text:
            norm_text = norm_text.replace(old_desc_zhcn, new_desc_zhcn)
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
        print(f"Updated {p} -> v3.9")

print(f"Total wts updated: {updated_count}")
