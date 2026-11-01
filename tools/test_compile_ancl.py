import subprocess, os

test_dir = "test_a003_ancl"
os.makedirs(f"{test_dir}/table", exist_ok=True)
with open(f"{test_dir}/table/ability.ini", "w", encoding="utf-8") as f:
    f.write('''[A003]
_parent = "ANcl"
Name = "万象皆虚"
Tip = "万象皆虚(|cffffcc00E|r) - [等级 1]","万象皆虚(|cffffcc00E|r) - [等级 2]","万象皆虚(|cffffcc00E|r) - [等级 3]"
Ubertip = "制造目标区域所有单位幻象","制造目标区域所有单位幻象","制造目标区域所有单位幻象"
Hotkey = "E"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNDisruption.blp"
Buttonpos_1 = 2
Buttonpos_2 = 2
levels = 3
reqLevel = 1
levelSkip = 2
hero = 1
Cost = {120, 140, 160}
Cool = {50.0, 45.0, 40.0}
Rng = {700.0, 700.0, 700.0}
Area = {250.0, 350.0, 450.0}
DataA = {0.0, 0.0, 0.0}
DataB = {2, 2, 2}
DataC = {3, 3, 3}
DataD = {0.0, 0.0, 0.0}
DataE = {1, 1, 1}
DataF = "blizzard,blizzard,blizzard"
Order = "blizzard"
targs = "ground,air"
''')

with open(f"{test_dir}/table/unit.ini", "w", encoding="utf-8") as f:
    f.write('''[H002]
_parent = "Obla"
Name = "幻梦大师"
heroAbilList = "A003"
''')

# Compile with w2l
res = subprocess.run(["tools/w3x2lni/w2l.exe", "obj", test_dir, "test_ancl_out.w3x"], capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
