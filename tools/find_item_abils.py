with open('tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/item.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'\[([a-z0-9]{4})\].*?abillist\s*=\s*"([^"]+)"', text)
for item_id, abil in matches:
    if abil in ['Aivs', 'Apiv', 'Ashm', 'Agho', 'AIil', 'AIsi', 'AIvi']:
        print(item_id, abil)
