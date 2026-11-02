import glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
locales_dir = os.path.join(ROOT, 'payload')
files = glob.glob(os.path.join(locales_dir, '**', 'war3map.wts'), recursive=True)

old_title_zhcn = '测试版v2.4'
new_title_zhcn = '测试版v2.5'
old_title_zhtw = '測試版v2.4'
new_title_zhtw = '測試版v2.5'

old_desc_zhcn = '三英雄测试图 v2.4：异种之源Q渊潜掠影真隐身（真视可见、禁误普攻）与E拟态伪装间谍欺骗机制修复（同阵营小地图绿点/绿血条/受害者名讳/仇恨免疫/破伪装暴击）。'
new_desc_zhcn = '三英雄测试图 v2.5：异种之源W捕食吞噬小兵机制重构（近战小兵永久加最大生命，无蓝远程小兵永久加基础攻击，魔法单位永久加最大法力），R异种进化控制台实时显示累计属性与管理英雄技能。'

old_desc_zhtw = '三英雄測試圖 v2.4：異種之源Q淵潛掠影真隱身（真視可見、禁誤普攻）與E擬態偽裝間諜欺騙機制修復（同陣營小地圖綠點/綠血條/受害者名諱/仇恨免疫/破偽裝暴擊）。'
new_desc_zhtw = '三英雄測試圖 v2.5：異種之源W捕食吞噬小兵機制重構（近戰小兵永久加最大生命，無藍遠程小兵永久加基礎攻擊，魔法單位永久加最大法力），R異種進化控制台即時顯示累計屬性與管理英雄技能。'

for p in files:
    with open(p, 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    if has_bom:
        raw_text = data[3:].decode('utf-8')
    else:
        raw_text = data.decode('utf-8')

    is_crlf = '\r\n' in raw_text
    norm_text = raw_text.replace('\r\n', '\n')

    norm_text = norm_text.replace(old_title_zhcn, new_title_zhcn)
    norm_text = norm_text.replace(old_title_zhtw, new_title_zhtw)

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
    print(f'Updated {p}: {b"2.5" in out_bytes}')
