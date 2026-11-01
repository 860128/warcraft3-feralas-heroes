import os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

desc_hans = '幻梦大师与魔音忍者测试图 v1.8：全新测试模式选择框架，支持全部电脑或精细逐个指定电脑出幻梦大师/魔音忍者/原版英雄，具备完整的电脑AI英雄自动换发、技能自动加点与智能战术施法。'
desc_hant = '幻夢大師與魔音忍者測試圖 v1.8：全新測試模式選擇框架，支持全部電腦或精細逐個指定電腦出幻夢大師/魔音忍者/原版英雄，具備完整的電腦AI英雄自動換發、技能自動加點與智能戰術施法。'

def update_wts(src_path, dst_path, is_zhtw):
    with open(src_path, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig', errors='ignore')
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    title = '測試版v1.8' if is_zhtw else '测试版v1.8'
    desc = desc_hant if is_zhtw else desc_hans

    text = re.sub(r'STRING 1\s*\{\s*[^}]*\}', f'STRING 1\n{{\n{title}\n}}', text)
    text = re.sub(r'STRING 3\s*\{\s*[^}]*\}', f'STRING 3\n{{\n{desc}\n}}', text)

    out_bytes = text.replace('\n', '\r\n').encode('utf-8')
    if has_bom:
        out_bytes = b'\xef\xbb\xbf' + out_bytes

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'wb') as f:
        f.write(out_bytes)

update_wts(os.path.join(ROOT, 'raw', 'war3map.wts'), os.path.join(ROOT, 'payload', 'war3map.wts'), False)

for mod in glob.glob(os.path.join(ROOT, 'raw', '_Locales', '*.w3mod')):
    loc_name = os.path.basename(mod)
    src_wts = os.path.join(mod, 'war3map.wts')
    if os.path.exists(src_wts):
        dst_wts = os.path.join(ROOT, 'payload', '_Locales', loc_name, 'war3map.wts')
        update_wts(src_wts, dst_wts, 'zhTW' in loc_name)

print('Updated wts files to v1.8 successfully.')
