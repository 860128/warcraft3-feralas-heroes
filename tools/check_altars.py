with open('tools/w3x2lni/template/Melee/unit.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for a in ['halt', 'oalt', 'uaod', 'eate']:
    i = text.find('[' + a + ']')
    j = text.find('[', i+1)
    block = text[i:j]
    for line in block.splitlines():
        if any(k in line.lower() for k in ['train', 'research', 'res', 'abil']):
            print(a, line)
