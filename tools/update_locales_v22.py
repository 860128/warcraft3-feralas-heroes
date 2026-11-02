import glob, os

locales_dir = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload'
files = glob.glob(os.path.join(locales_dir, '**', 'war3map.wts'), recursive=True)

old_desc_zhcn = '幻梦大师与魔音忍者测试图 v2.1：彻底解决电脑AI兵力拉扯折返跑问题，移除警戒绳索羁绊并锁定进攻目标，军队坚决打野与全图推进。'
new_desc_zhcn = '幻梦大师与魔音忍者测试图 v2.2：竭心光环与因果流失非致死保底1血优化，彻底杜绝被动意外毙命，必须英雄亲自最后一击。'

old_desc_zhtw = '幻夢大師與魔音忍者測試圖 v2.1：徹底解決電腦AI兵力拉扯折返跑問題，移除警戒繩索羈絆並鎖定進攻目標，軍隊堅決打野與全圖推進。'
new_desc_zhtw = '幻夢大師與魔音忍者測試圖 v2.2：竭心光環與因果流失非致死保底1血優化，徹底杜絕被動意外斃命，必須英雄親自最後一擊。'

for p in files:
    with open(p, 'rb') as f:
        data = f.read()

    # Detect BOM
    has_bom = data.startswith(b'\xef\xbb\xbf')
    if has_bom:
        raw_text = data[3:].decode('utf-8')
    else:
        raw_text = data.decode('utf-8')

    is_crlf = '\r\n' in raw_text
    norm_text = raw_text.replace('\r\n', '\n')

    # Replace title
    norm_text = norm_text.replace('测试版v2.1', '测试版v2.2')
    norm_text = norm_text.replace('測試版v2.1', '測試版v2.2')

    # Replace desc for zhTW vs others
    if 'zhTW' in p:
        norm_text = norm_text.replace(old_desc_zhtw, new_desc_zhtw)
    else:
        norm_text = norm_text.replace(old_desc_zhcn, new_desc_zhcn)

    if is_crlf:
        final_text = norm_text.replace('\n', '\r\n')
    else:
        final_text = norm_text

    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + final_text.encode('utf-8')
    with open(p, 'wb') as f:
        f.write(out_bytes)
    print(f'Updated {p}: {b"2.2" in out_bytes}')
