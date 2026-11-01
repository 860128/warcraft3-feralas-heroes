t = open(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\data\zhCN-1.32.8\mpq\UI\UnitEditorData.txt", "r", encoding="utf-8", errors="replace").read()
idx = t.find("[orderString]")
if idx != -1:
    print(t[idx:idx+400])
else:
    print("no orderString section")
    # search where order is used
    import re
    print(re.findall(r'\[.*?order.*?\]', t, re.I))
