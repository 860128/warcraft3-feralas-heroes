with open('hero_obj_v3_raw/war3map.w3a', 'rb') as f:
    text = f.read()

print("A00W in w3a:", b'A00W' in text)
