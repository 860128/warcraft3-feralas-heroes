with open('tools/w3x2lni/template/Melee/item.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'\[([A-Za-z0-9]{4})\].*?abilList\s*=\s*"([^"]+)"', text)
for u, abils in matches:
    if 'Apiv' in abils:
        print(f'Item {u} has Apiv')
