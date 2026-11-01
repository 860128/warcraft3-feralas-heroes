with open('raw/war3map.j', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'CreateUnitsForPlayer0' in line or 'Player(0)' in line:
        print(f"Line {i}: {line.strip()[:80]}")
