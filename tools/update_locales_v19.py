import glob, os

locales_dir = r'C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload'
files = glob.glob(os.path.join(locales_dir, '**', 'war3map.wts'), recursive=True)

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
    norm_text = norm_text.replace('测试版v1.8', '测试版v1.9')
    norm_text = norm_text.replace('測試版v1.8', '測試版v1.9')

    # Replace desc for zhTW
    if 'zhTW' in p:
        norm_text = norm_text.replace(
            '幻夢大師與魔音忍者測試圖 v1.8：全新測試模式選擇框架，支持全部電腦或精細逐個指定電腦出幻夢大師/魔音忍者/原版英雄，具備完整的電腦AI英雄自動換發、技能自動加點與智能戰術施法。',
            '幻夢大師與魔音忍者測試圖 v1.9：修復魔音神尊35%閃避率與電腦魔音忍者智能自動加點/擊殺分身機制，具備完整的電腦AI英雄自動換發、技能自動加點與智能戰術施法。'
        )
    else:
        norm_text = norm_text.replace(
            '幻梦大师与魔音忍者测试图 v1.8：全新测试模式选择框架，支持全部电脑或精细逐个指定电脑出幻梦大师/魔音忍者/原版英雄，具备完整的电脑AI英雄自动换发、技能自动加点与智能战术施法。',
            '幻梦大师与魔音忍者测试图 v1.9：修复魔音神尊35%闪避率与电脑魔音忍者智能自动加点/击杀分身机制，具备完整的电脑AI英雄自动换发、技能自动加点与智能战术施法。'
        )

    if is_crlf:
        final_text = norm_text.replace('\n', '\r\n')
    else:
        final_text = norm_text

    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + final_text.encode('utf-8')
    with open(p, 'wb') as f:
        f.write(out_bytes)
    print(f'Updated {p}: {b"1.9" in out_bytes}')
