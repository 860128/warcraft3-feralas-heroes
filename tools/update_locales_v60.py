# -*- coding: utf-8 -*-
import glob
import os

files = glob.glob('payload/**/war3map.wts', recursive=True)

old_title_zhcn = '测试版v5.9'
new_title_zhcn = '测试版v6.0'
old_title_zhtw = '測試版v5.9'
new_title_zhtw = '測試版v6.0'

old_desc_zhcn = '五英雄全能对战版 v5.9：万象皆虚全维克隆同步重构！完美继承魔虚罗/异种之源/万灵化身进化变身模型、实时攻击力与射程！'
new_desc_zhcn = '五英雄全能对战版 v6.0：魔虚罗内战四阶破法升维隐藏彩蛋（瓦解适应/拳拳到肉/斩魂真伤/弑神碎蛋）！纯白底纹五色神轮与火人体型精准适配！'

old_desc_zhtw = '五英雄全能對戰版 v5.9：萬象皆虛全維克隆同步重構！完美繼承魔虛羅/異種之源/萬靈化身進化變身模型、實時攻擊力與射程！'
new_desc_zhtw = '五英雄全能對戰版 v6.0：魔虛羅內戰四階破法升維隱藏彩蛋（瓦解適應/拳拳到肉/斬魂真傷/弑神碎蛋）！純白底紋五色神輪與火人體型精準適配！'

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
