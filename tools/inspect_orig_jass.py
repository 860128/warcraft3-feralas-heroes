import os, subprocess

with open("raw/war3map.j", "r", encoding="utf-8", errors="ignore") as f:
    orig_jass = f.read()

# Let's inspect globals section in orig_jass
globals_idx = orig_jass.find("globals")
endglobals_idx = orig_jass.find("endglobals", globals_idx)
print("Globals found:", globals_idx != -1, endglobals_idx != -1)

# Let's inspect main function in orig_jass
main_idx = orig_jass.find("function main takes nothing returns nothing")
print("Main found:", main_idx != -1)
