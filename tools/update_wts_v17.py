import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOAD = os.path.join(ROOT, "payload")

desc_hans = "幻梦大师与魔音忍者测试图 v1.7：修复魔音分身与魔音神尊闪避率异常，新增他化自在因果印记持续特效与百分比扣血，新增无忍者存活时本尊夺舍复活机制。"
desc_hant = "幻夢大師與魔音忍者測試圖 v1.7：修復魔音分身與魔音神尊閃避率異常，新增他化自在因果印記持續特效與百分比扣血，新增無忍者存活時本尊奪舍復活機制。"

for root, dirs, files in os.walk(PAYLOAD):
    for f in files:
        if f.endswith(".wts"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                text = fp.read()

            is_zhtw = "zhTW" in path
            title = "測試版v1.7" if is_zhtw else "测试版v1.7"
            desc = desc_hant if is_zhtw else desc_hans

            # Standardize replacement of STRING 1
            text = re.sub(r'STRING 1\s*\{[^}]*\}', f'STRING 1\n{{\n{title}\n}}', text)
            # Remove any stray line between STRING 1 and STRING 2
            text = re.sub(r'(\}\s*\n)[^\nS]*\n(?=\s*STRING 2)', r'\1\n', text)

            # Standardize replacement of STRING 3
            text = re.sub(r'STRING 3\s*\{[^}]*\}', f'STRING 3\n{{\n{desc}\n}}', text)
            # Remove any stray line between STRING 3 and STRING 4
            text = re.sub(r'(\}\s*\n)[^\nS]*\n(?=\s*STRING 4)', r'\1\n', text)

            with open(path, "w", encoding="utf-8") as fp:
                fp.write(text)
            print("Cleaned & Updated:", path)
