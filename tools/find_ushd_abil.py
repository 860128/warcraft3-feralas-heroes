with open('tools/w3x2lni/template/Melee/unit.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

i = text.find('[ushd]')
j = text.find('[', i+1)
block = text[i:j]
for line in block.splitlines():
    if 'abil' in line.lower():
        print(line)
