with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for c in ['AIvi', 'AIpv', 'AIsi', 'AIil', 'Aivs']:
    i = text.find('[' + c + ']')
    if i != -1:
        j = text.find('[', i+1)
        print("=== " + c + " ===")
        print(text[i:j])
