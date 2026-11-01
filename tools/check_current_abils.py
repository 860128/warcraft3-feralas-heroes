with open('factory_tpl/table/ability.ini', 'r', encoding='utf-8') as f:
    text = f.read()

for c in ['A001', 'A002', 'A003', 'A004', 'A00I', 'A00J']:
    i = text.find('[' + c + ']')
    j = text.find('[', i+1) if i != -1 else -1
    print(text[i:j] if j != -1 else text[i:])
