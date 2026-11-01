t = open(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\data\zhCN-1.24.4\prebuilt\Custom\ability.ini", "r", encoding="utf-8", errors="replace").read()
idx = t.find("[AOfs]")
print(t[idx:idx+600])
