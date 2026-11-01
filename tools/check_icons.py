import re
with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

arts = sorted(set(re.findall(r'Art\s*=\s*"([^"]+)"', text)))
for a in arts:
    if any(k in a.lower() for k in ['mirror', 'illus', 'wand', 'charm', 'possess', 'dark', 'scepter', 'silence', 'invis', 'spirit', ' ethereal', 'banish', 'blink', 'mana', 'orb']):
        print(a)
