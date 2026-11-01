with open('tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/item.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for line in text.splitlines():
    if 'abilList' in line and any(k in line for k in ['Ashm', 'Agho', 'Aivs', 'AOwk', 'Apiv']):
        print(line)
