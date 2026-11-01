with open('tools/w3x2lni/template/Melee/unit.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

i = text.find('[ewsp]')
j = text.find('[', i+1)
print(text[i:j])
