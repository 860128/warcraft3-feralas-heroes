import glob, os

locales_dir = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload'
files = glob.glob(os.path.join(locales_dir, '**', 'war3map.wts'), recursive=True)

old_desc_zhcn = '幻梦大师与魔音忍者测试图 v1.9：修复魔音神尊35%闪避率与电脑魔音忍者智能自动加点/击杀分身机制，具备完整的电脑AI英雄自动换发、技能自动加点与智能战术施法。'
new_desc_zhcn = '幻梦大师与魔音忍者测试图 v2.0：新增电脑AI战略大军统帅系统，解决AI兵力在基地发呆问题，英雄与军队智能打野、集结推进与全图进攻。'

old_desc_zhtw = '幻夢大師與魔音忍者測試圖 v1.9：修復魔音神尊35%閃避率與電腦魔音忍者智能自動加點/擊殺分身機制，具備完整的電腦AI英雄自動換發、技能自動加點與智能戰術施法。'
new_desc_zhtw = '幻夢大師與魔音忍者測試圖 v2.0：新增電腦AI戰略大軍統帥系統，解決AI兵力在基地發呆問題，英雄與軍隊智能打野、集結推進與全圖進攻。'

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
    norm_text = norm_text.replace('测试版v1.9', '测试版v2.0')
    norm_text = norm_text.replace('測試版v1.9', '測試版v2.0')

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
    print(f'Updated {p}: {b"2.0" in out_bytes}')
