with open('tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/item.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'abillist\s*=\s*"([^"]+)"', text)
abils = set(matches)
for a in sorted(abils):
    if 'i' in a.lower():
        print(a)
