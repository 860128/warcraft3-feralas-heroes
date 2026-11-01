with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'\[([A-Za-z0-9]{4})\].*?BuffID\s*=\s*"([^"]+)"', text)
for c, b in matches:
    if 'inv' in b.lower():
        print(c, b)
