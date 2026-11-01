t = open(r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\tools\w3x2lni\data\zhCN-1.32.8\mpq\Scripts\Common.j", "r", encoding="utf-8", errors="replace").read()
import re
print("IsUnitIllusion:", re.findall(r"native\s+IsUnitIllusion.*", t))
print("IsUnitType:", re.findall(r"constant\s+unittype\s+UNIT_TYPE_ILLUSION.*", t))
