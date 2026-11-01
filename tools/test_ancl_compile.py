import os
import subprocess

TABLE = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\factory_tpl\table"
w2l = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\w2l.exe"

# Test compiling A002 with DataC = 1
txt = '''[A002]
_parent = "ANcl"
Name = "幻梦奴役"
Hotkey = "W"
Researchhotkey = "W"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNPossession.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNPossession.blp"
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Buttonpos_1 = 1
Buttonpos_2 = 2
Researchbuttonpos_1 = 1
Researchbuttonpos_2 = 0
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 1, 2 = 1, 3 = 1}
DataC = {1 = 1, 2 = 1, 3 = 1}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 1, 2 = 1, 3 = 1}
DataF = {1 = "charm", 2 = "charm", 3 = "charm"}
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cool = {1 = 30.0, 2 = 25.0, 3 = 20.0}
Cost = {1 = 100, 2 = 125, 3 = 150}
targs = {1 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward", 2 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward", 3 = "air,ground,enemy,neutral,friend,invulnerable,vulnerable,organic,mechanical,hero,nonhero,structure,debris,ward"}
Tip = {1 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 1|r]", 2 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 2|r]", 3 = "幻梦奴役(|cffffcc00W|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "测试", 2 = "测试", 3 = "测试"}
Researchtip = "学习 幻梦奴役"
Researchubertip = "测试"
'''

with open(os.path.join(TABLE, "ability.ini"), "w", encoding="utf-8") as f:
    f.write(txt)

src = os.path.abspath(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\factory_tpl")
dst = os.path.abspath(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\test_ancl.w3x")
p = subprocess.run([w2l, "obj", src, dst], cwd=os.path.dirname(w2l), capture_output=True)
print("RC:", p.returncode)

# Now check lni back
dst_lni = os.path.abspath(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\test_ancl_lni")
p2 = subprocess.run([w2l, "lni", dst, dst_lni], cwd=os.path.dirname(w2l), capture_output=True)
print("RC2:", p2.returncode)
print(open(os.path.join(dst_lni, "table", "ability.ini"), "r", encoding="utf-8", errors="replace").read())
