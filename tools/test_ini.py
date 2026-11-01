with open('tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if '[' in line:
            print("Sample section:", line)
            break
