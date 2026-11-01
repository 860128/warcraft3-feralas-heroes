import os
t = open(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\data\zhCN-1.24.4\prebuilt\Custom\ability.ini", "r", encoding="utf-8", errors="replace").read()
idx = t.find("[ANcl]")
print(t[idx:idx+1000])
