import glob
for p in glob.glob('tools/w3x2lni/**/*', recursive=True):
    if p.endswith(('.slk', '.ini', '.lua', '.txt')):
        try:
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()
            if '852274' in c or 'AIil' in c:
                print(p)
        except Exception:
            pass
