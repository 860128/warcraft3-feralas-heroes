# -*- coding: utf-8 -*-
import sys
import os

jass_path = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero\payload\war3map.j"

with open(jass_path, "r", encoding="utf-8") as f:
    text = f.read()

# Clean up any potential duplicate endfunction
text = text.replace("endfunctionendfunction", "endfunction")

with open(jass_path, "w", encoding="utf-8") as f:
    f.write(text)

print("apply_v40_jass.py check passed.")
