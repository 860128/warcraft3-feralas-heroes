import os, hashlib

for fn in ['war3map.w3a', 'war3map.w3u', 'war3map.j', 'war3map.wts', '_Locales/zhCN.w3mod/war3map.wts']:
    p1 = os.path.join('verify_v12', fn)
    p2 = os.path.join('payload', fn)
    b1 = open(p1, 'rb').read()
    b2 = open(p2, 'rb').read()
    print(f"{fn}: v1.2={len(b1)} bytes, v1.3={len(b2)} bytes, same={b1==b2}")
