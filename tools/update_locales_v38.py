# -*- coding: utf-8 -*-
import glob
import os
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v3.7'
new_title_zhcn = '测试版v3.8'
old_title_zhtw = '測試版v3.7'
new_title_zhtw = '測試版v3.8'

old_desc_zhcn = '四英雄全能对战版 v3.7：万灵化身10点技能完美加满（大招1点随等级进阶）；百鬼军魂常驻50%共鸣（大招翻倍100%）；状态栏Buff与D/R动态实时追踪；10级野怪霸主赋予魔免/献祭/巨龙吞噬等复合绝技！'
new_desc_zhcn = '四英雄全能对战版 v3.8：万灵大军推进AI彻底修复！解除警戒站位锁死，全图动态锁定存活敌方玩家与野怪，出招即刻全军冲锋，告别空地发呆！'

old_desc_zhtw = '四英雄全能對戰版 v3.7：萬靈化身10點技能完美加滿（大招1點隨等級進階）；百鬼軍魂常駐50%共鳴（大招翻倍100%）；狀態欄Buff與D/R動態即時追蹤；10級野怪霸主賦予魔免/獻祭/巨龍吞噬等複合絕技！'
new_desc_zhtw = '四英雄全能對戰版 v3.8：萬靈大軍推進AI徹底修復！解除警戒站位鎖死，全圖動態鎖定存活敵方玩家與野怪，出招即刻全軍衝鋒，告別空地發呆！'

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
        print(f"Updated {p} -> v3.8")

print(f"Total wts updated: {updated_count}")
