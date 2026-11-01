with open('tools/w3x2lni/template/Melee/unit.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'\[ushd\].*?abilList\s*=\s*"([^"]+)"', text)
print("Shade abilList:", matches)
