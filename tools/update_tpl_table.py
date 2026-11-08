# -*- coding: utf-8 -*-
import re

with open('tools/verify_tpl_table.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip().startswith('(2, 10, 1,'):
        new_lines.append('    (2, 10, 1, \'nbwm\', "极黑成年巨龙", 1950, 0, 92, 9.0, 1.25, 340.0, 600, 1.40, \'ACfn\', "冰霜新星"),\n')
    elif line.strip().startswith('(2, 10, 2,'):
        new_lines.append('    (2, 10, 2, \'nadw\', "碧蓝成年巨龙", 1700, 0, 115, 6.0, 0.90, 390.0, 600, 1.40, \'ACf2\', "霜冻吐息"),\n')
    elif line.strip().startswith('(2, 10, 3,'):
        new_lines.append('    (2, 10, 3, \'nbzw\', "青铜成年巨龙", 1800, 0, 100, 7.0, 1.15, 340.0, 600, 1.40, \'ACcs\', "狂暴冲击"),\n')
    elif line.strip().startswith('(3, 10, 1,'):
        new_lines.append('    (3, 10, 1, \'nerw\', "艾瑞达术士", 1800, 1000, 75, 8.0, 1.25, 330.0, 600, 1.40, \'AChx\', "妖术"),\n')
    elif line.strip().startswith('(3, 10, 2,'):
        new_lines.append('    (3, 10, 2, \'nrwm\', "猩红成年巨龙", 1600, 950, 98, 6.0, 1.10, 350.0, 600, 1.40, \'ACif\', "心灵之火"),\n')
    elif line.strip().startswith('(3, 10, 3,'):
        new_lines.append('    (3, 10, 3, \'nbzw\', "远古虚空巨龙", 1700, 1050, 85, 7.0, 1.20, 340.0, 600, 1.40, \'ACsh\', "闪电护盾"),\n')
    else:
        new_lines.append(line)

with open('tools/verify_tpl_table.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("verify_tpl_table.py Tier 10 successfully updated!")
