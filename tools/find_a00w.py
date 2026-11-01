with open('factory_tpl/table/ability.ini', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

i = text.find('[A00W]')
if i != -1:
    j = text.find('[', i+1)
    print(text[i:j])
else:
    print("A00W not found")
