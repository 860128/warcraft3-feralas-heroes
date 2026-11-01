with open('tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/item.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
items = re.findall(r'\[([A-Za-z0-9]{4})\].*?Name\s*=\s*"([^"]+)"', text)
for code, name in items:
    if '风衣' in name or '隐形' in name or '隐身' in name:
        print(code, name)
