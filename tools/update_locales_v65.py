# -*- coding: utf-8 -*-
import glob

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v6.4'
new_title_zhcn = '测试版v6.5'
old_title_zhtw = '測試版v6.4'
new_title_zhtw = '測試版v6.5'

old_desc_zhcn = '五英雄全能对战版 v6.4：彻底修复暗杀介绍所悬赏头像槽隐形Bug！动态重挂载实时显示全部敌方头像报价，下单立即全图通缉广播！'
new_desc_zhcn = '五英雄全能对战版 v6.5：暗杀波次随目标实时进化重扫+几何级反超狂暴升级！并彻底修复魔音忍者分身替死与杀手提前消失Bug！'

old_desc_zhtw = '五英雄全能對戰版 v6.4：徹底修復暗殺介紹所懸賞頭像槽隱形Bug！動態重掛載實時顯示全部敵方頭像報價，下單立即全圖通緝廣播！'
new_desc_zhtw = '五英雄全能對戰版 v6.5：暗殺波次隨目標實時進化重掃+幾何級反超狂暴升級！並徹底修復魔音忍者分身替死與殺手提前消失Bug！'

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
