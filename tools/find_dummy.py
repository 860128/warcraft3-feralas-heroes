with open('factory_tpl/table/unit.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for u in ['u000', 'e000', 'h000']:
    if '[' + u + ']' in text:
        print(f"Found {u} in unit.ini")
