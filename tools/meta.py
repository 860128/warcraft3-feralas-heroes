import re, sys
sys.stdout.reconfigure(encoding='utf-8')
D = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\data\zhCN-1.32.8\mpq\Units"

def load(fn):
    t = open(D + "\\" + fn, 'rb').read().decode('utf-8', 'replace')
    rows = {}
    y = None
    for line in t.split('\n'):
        line = line.strip()
        if not line.startswith('C;'):
            continue
        parts = line.split(';')
        x = None
        val = None
        for p in parts[1:]:
            if p.startswith('X'): x = int(p[1:])
            elif p.startswith('Y'): y = int(p[1:])
            elif p.startswith('K'): val = p[1:].strip('"')
        rows.setdefault(y, {})[x] = val
    hdr = rows[1]
    inv = {v: k for k, v in hdr.items()}
    out = []
    for yy, r in rows.items():
        if yy == 1: continue
        out.append({k: r.get(c) for k, c in inv.items()})
    return out

want = set(sys.argv[2].split(','))
for o in load(sys.argv[1]):
    if o.get('ID') in want or (o.get('useSpecific') or '') and any(w in (o.get('useSpecific') or '') for w in want):
        print(o.get('ID'), o.get('field'), o.get('data'), o.get('index'), o.get('type'), o.get('useSpecific'), o.get('displayName'))
