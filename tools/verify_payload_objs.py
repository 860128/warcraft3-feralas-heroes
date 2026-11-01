import os

payload_dir = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload"

with open(os.path.join(payload_dir, 'war3map.w3a'), 'rb') as f:
    text = f.read()

print("=== Ability Verification (war3map.w3a) ===")
for c in [b'A001', b'A002', b'A003', b'A004', b'A00V', b'A011', b'A012', b'A013', b'A014']:
    print(c.decode('ascii'), c in text)

with open(os.path.join(payload_dir, 'war3map.w3u'), 'rb') as f:
    text = f.read()

print("\n=== Unit Verification (war3map.w3u) ===")
for c in [b'H002', b'H003', b'u000', b'u001', b'halt', b'oalt', b'uaod', b'eate']:
    print(c.decode('ascii'), c in text)
