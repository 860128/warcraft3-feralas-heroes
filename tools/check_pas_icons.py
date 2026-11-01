import re
with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

arts = sorted(set(re.findall(r'Art\s*=\s*"([^"]+)"', text)))
for a in arts:
    if 'pasbtn' in a.lower():
        print(a)
