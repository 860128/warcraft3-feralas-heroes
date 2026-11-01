with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for code in ['AHad', 'AEev', 'Aamk']:
    i = text.find('[' + code + ']')
    j = text.find('[', i+1)
    print("=== " + code + " ===")
    print(text[i:j])
