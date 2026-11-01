import os, subprocess

TABLE = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\factory_tpl\table"
w2l = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\w2l.exe"

txt = '''[A003]
_parent = "ANcl"
Name = "万象皆虚"
Hotkey = "E"
Researchhotkey = "E"
Art = "ReplaceableTextures\\\\CommandButtons\\\\BTNWand.blp"
ResearchArt = "ReplaceableTextures\\\\CommandButtons\\\\BTNWand.blp"
levels = 3
hero = 1
reqLevel = 1
levelSkip = 2
Buttonpos_1 = 2
Buttonpos_2 = 2
Researchbuttonpos_1 = 2
Researchbuttonpos_2 = 0
DataA = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataB = {1 = 2, 2 = 2, 3 = 2}
DataC = {1 = 3, 2 = 3, 3 = 3}
DataD = {1 = 0.0, 2 = 0.0, 3 = 0.0}
DataE = {1 = 0, 2 = 0, 3 = 0}
DataF = {1 = "blizzard", 2 = "blizzard", 3 = "blizzard"}
Order = "blizzard"
Area = {1 = 250.0, 2 = 350.0, 3 = 450.0}
Rng = {1 = 700.0, 2 = 750.0, 3 = 800.0}
Cool = {1 = 35.0, 2 = 30.0, 25.0}
Cost = {1 = 120, 2 = 140, 3 = 160}
checkdep = 0
TargetArt = "Abilities\\\\Spells\\\\Other\\\\Silence\\\\SilenceAreaBirth.mdl"
EffectArt = "Abilities\\\\Spells\\\\Other\\\\Silence\\\\SilenceAreaBirth.mdl"
Tip = {1 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 1|r]", 2 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 2|r]", 3 = "万象皆虚(|cffffcc00E|r) - [|cffffcc00等级 3|r]"}
Ubertip = {1 = "测试", 2 = "测试", 3 = "测试"}
Researchtip = "学习 万象皆虚"
Researchubertip = "测试"
'''

with open(os.path.join(TABLE, "ability.ini"), "w", encoding="utf-8") as f:
    f.write(txt)

src = os.path.abspath(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\factory_tpl")
dst = os.path.abspath(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\test_a003.w3x")
p = subprocess.run([w2l, "obj", src, dst], cwd=os.path.dirname(w2l), capture_output=True)
print("RC:", p.returncode)

dst_lni = os.path.abspath(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\test_a003_lni")
p2 = subprocess.run([w2l, "lni", dst, dst_lni], cwd=os.path.dirname(w2l), capture_output=True)
print("RC2:", p2.returncode)
print(open(os.path.join(dst_lni, "table", "ability.ini"), "r", encoding="utf-8", errors="replace").read())
