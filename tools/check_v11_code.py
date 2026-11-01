with open('verify_mod/war3map.j', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'DM_CastMirrorImage' in line or 'A001' in line:
        for k in range(max(0, i-5), min(len(lines), i+30)):
            print(lines[k], end='')
        break
