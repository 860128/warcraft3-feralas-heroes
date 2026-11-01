with open('tools/w3x2lni/data/zhCN-1.32.8/mpq/Units/itemabilityfunc.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()
i = text.find('[AIil]')
print(text[i:i+300])
