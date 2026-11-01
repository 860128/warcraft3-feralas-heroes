import subprocess

for f in ['ability.ini', 'unit.ini']:
    print(f"=== {f} ===")
    with open(f"factory_tpl/table/{f}", "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        print("Line count:", len(lines))
