with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'\[([A-Za-z0-9]{4})\].*?Art\s*=\s*"([^"]+)"', text)
for c, art in matches:
    if 'potionofinvis' in art.lower() or 'invis' in art.lower():
        print(c, art)
