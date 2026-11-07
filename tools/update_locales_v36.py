# -*- coding: utf-8 -*-
import glob, os, re

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v3.5'
new_title_zhcn = '测试版v3.6'
old_title_zhtw = '測試版v3.5'
new_title_zhtw = '測試版v3.6'

old_desc_zhcn = '四英雄全能对战版 v3.5：【百鬼军魂】平衡调优（+4生命/+0.5攻击并在场即时成长）；精锐伥鬼过滤工人杂鱼并开启12槽位优胜劣汰；消除普通击杀刷屏与开大汇总军势！'
new_desc_zhcn = '四英雄全能对战版 v3.6：彻底校准万灵化身90种野怪专属特技，杜绝张冠李戴（修复鹰身人丢巨石等Bug）；二级变身菜单按钮动态显示真实技能名与属性加成！'

old_desc_zhtw = '四英雄全能對戰版 v3.5：【百鬼軍魂】平衡調優（+4生命/+0.5攻擊並在場即時成長）；精銳倀鬼過濾工人雜魚並開啟12槽位優勝劣汰；消除普通擊殺刷屏與開大彙總軍勢！'
new_desc_zhtw = '四英雄全能對戰版 v3.6：徹底校準萬靈化身90種野怪專屬特技，杜絕張冠李戴（修復鷹身人丟巨石等Bug）；二級變身菜單按鈕動態顯示真實技能名與屬性加成！'

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
        print(f"Updated {p} -> v3.6")

print(f"Total wts updated: {updated_count}")
