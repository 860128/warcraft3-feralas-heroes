with open('tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/item.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("Length:", len(text))
print("First 500 chars:\n", text[:500])
