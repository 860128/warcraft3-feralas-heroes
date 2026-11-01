with open('verify_mod/war3map.j', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'H002' in line:
        print(f"Line {i}: {line.strip()}")
