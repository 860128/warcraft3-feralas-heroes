with open('tools/w3x2lni/data/zhCN-1.32.8/mpq/Units/UnitMetaData.slk', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for k in ['Revive', 'Revivetip', 'Reviveat']:
    idx = text.find('K"' + k + '"')
    print("=== " + k + " ===")
    print(text[idx-50:idx+250])
