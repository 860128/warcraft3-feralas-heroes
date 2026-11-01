import re
ini_path = 'tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/ability.ini'
with open(ini_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

sections = text.split('[')
for s in sections:
    if not s.strip(): continue
    code = s[:4]
    name_m = re.search(r'Name\s*=\s*"([^"]+)"', s)
    name = name_m.group(1) if name_m else ''
    if any(k in name for k in ['隐形', '潜行', '幽灵', '疾风步', '影遁', '隐身', '永久']):
        print(f'{code}: {name}')
