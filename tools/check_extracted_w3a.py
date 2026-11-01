with open('hero_obj_v3_extract/war3map.w3a', 'rb') as f:
    text = f.read()

for code in [b'A001', b'A002', b'A003', b'A004', b'A00V']:
    print(code.decode('ascii'), code in text)
