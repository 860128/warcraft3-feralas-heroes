with open('verify_mod/war3map.j', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i in range(2750, min(len(lines), 2770)):
    print(f"{i}: {lines[i]}", end='')
