# -*- coding: utf-8 -*-
import glob

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v6.2'
new_title_zhcn = '测试版v6.3'
old_title_zhtw = '測試版v6.2'
new_title_zhtw = '測試版v6.3'

old_desc_zhcn = '五英雄全能对战版 v6.2：避难所与复活全维地形悬崖安全重构！同层连通平地选址、复活悬崖卡死自愈与-unstuck脱离指令！'
new_desc_zhcn = '五英雄全能对战版 v6.3：新增中立【暗杀介绍所】！敌方实时头像与战力报价、绝不受控的绝对克制杀手小队（顺路毁障+无限强化增援必杀）！'

old_desc_zhtw = '五英雄全能對戰版 v6.2：避難所與復活全維地形懸崖安全重構！同層連通平地選址、復活懸崖卡死自癒與-unstuck脫離指令！'
new_desc_zhtw = '五英雄全能對戰版 v6.3：新增中立【暗殺介紹所】！敵方實時頭像與戰力報價、絕不受控的絕對剋制殺手小隊（順路毀障+無限強化增援必殺）！'

updated_count = 0
for p in files:
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

print(f"Total updated: {updated_count}")
