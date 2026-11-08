# -*- coding: utf-8 -*-
import glob
import os
import re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v3.6'
new_title_zhcn = '测试版v3.7'
old_title_zhtw = '測試版v3.6'
new_title_zhtw = '測試版v3.7'

old_desc_zhcn = '四英雄全能对战版 v3.6：彻底校准万灵化身90种野怪专属特技，杜绝张冠李戴（修复鹰身人丢巨石等Bug）；二级变身菜单按钮动态显示真实技能名与属性加成！'
new_desc_zhcn = '四英雄全能对战版 v3.7：万灵化身10点技能完美加满（大招1点随等级进阶）；百鬼军魂常驻50%共鸣（大招翻倍100%）；状态栏Buff与D/R动态实时追踪；10级野怪霸主赋予魔免/献祭/巨龙吞噬等复合绝技！'

old_desc_zhtw = '四英雄全能對戰版 v3.6：徹底校準萬靈化身90種野怪專屬特技，杜絕張冠李戴（修復鷹身人丟巨石等Bug）；二級變身菜單按鈕動態顯示真實技能名與屬性加成！'
new_desc_zhtw = '四英雄全能對戰版 v3.7：萬靈化身10點技能完美加滿（大招1點隨等級進階）；百鬼軍魂常駐50%共鳴（大招翻倍100%）；狀態欄Buff與D/R動態即時追蹤；10級野怪霸主賦予魔免/獻祭/巨龍吞噬等複合絕技！'

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
        print(f"Updated {p} -> v3.7")

print(f"Total wts updated: {updated_count}")
