for fn in ['tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Melee/ability.ini', 'tools/w3x2lni/data/zhCN-1.32.8/prebuilt/Custom/ability.ini', 'tools/w3x2lni/template/Melee/ability.ini']:
    try:
        with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for c in ['AOwk', 'Apiv', 'Ashm', 'Agho', 'Aivs']:
            idx = content.find('[' + c + ']')
            if idx != -1:
                print(fn, c, content[idx:idx+250])
    except Exception as e:
        print(fn, e)
