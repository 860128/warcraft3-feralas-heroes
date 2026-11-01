with open('tools/w3x2lni/template/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for c in ['Apiv', 'Agho', 'Aivs']:
    i = text.find('[' + c + ']')
    j = text.find('[', i+1)
    print("=== " + c + " ===")
    print(text[i:j])
