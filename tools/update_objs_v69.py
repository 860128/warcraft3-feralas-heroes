# -*- coding: utf-8 -*-
"""
v6.9 对象数据补丁：
- 更新实验小兵 [u00B] 技能列表追加 [A083] 封印术·山 (E, 无视魔免) 与 [A084] 解封·破山 (R)
- 保留 H002..u00A 与 A001..A082 全部现有自定义对象
- 调用 w2l.exe obj 编译并提取至 payload/war3map.w3u 与 payload/war3map.w3a
"""
import os
import subprocess

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
TPL_DIR = os.path.join(ROOT, "factory_tpl")
UNIT_INI = os.path.join(TPL_DIR, "table", "unit.ini")
ABIL_INI = os.path.join(TPL_DIR, "table", "ability.ini")
W2L_EXE = os.path.join(ROOT, "tools", "w3x2lni", "w2l.exe")
STORM_DLL = os.path.join(ROOT, "tools", "StormLibSharp.dll")
PAYLOAD_DIR = os.path.join(ROOT, "payload")

NEW_U00B = r'''[u00B]
_parent = "hfoo"
Name = "实验小兵 · 万象状态师"
Ubertip = "【实验测试单位】普通步兵模型：|n- |cff00ff80[Q] 万象全Buff加持|r：9 大满级光环 + 9 大主动增益（45秒，不含魔免）；|n- |cffff3366[W] 万厄全Debuff诅咒|r：14 重纯净零伤害负面减益；|n- |cffcc66ff[E] 封印术 · 山（无视魔免）|r：封入孤立封印之山与全属性/全技能/全AI镜像死斗，镜像胜出归己方；|n- |cffffcc00[R] 解封 · 破山|r：主动关闭封印之山并释放被封印目标（镜像消失）。"
Art = "ReplaceableTextures\\CommandButtons\\BTNFootman.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNFootman.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNFootman.blp"
file = "units\\human\\Footman\\Footman"
"file:hd" = "units\\human\\Footman\\Footman"
"file:sd" = "units\\human\\Footman\\Footman"
unitSound = "Footman"
modelScale = 1.05
HP = 650
regenHP = 2.0
def = 4.0
spd = 320
manaN = 500
mana0 = 500
regenMana = 5.0
dmgplus1 = 16
cool1 = 1.35
foodCost = 0
goldcost = 0
lumbercost = 0
level = 3
abilList = "A060,A061,A083,A084"
'''

NEW_ABILS = r'''
[A083]
_parent = "ANcl"
Name = "封印术 · 山"
Hotkey = "E"
Buttonpos_1 = 2
Buttonpos_2 = 2
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Art = "ReplaceableTextures\\CommandButtons\\BTNMountainGiant.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNMountainGiant.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNMountainGiant.blp"
CasterArt = ""
"CasterArt:hd" = ""
"CasterArt:sd" = ""
EffectArt = ""
"EffectArt:hd" = ""
"EffectArt:sd" = ""
TargetArt = ""
"TargetArt:hd" = ""
"TargetArt:sd" = ""
DataA = {1 = 0.0}
DataB = {1 = 1}
DataC = {1 = 13}
DataD = {1 = 0.0}
DataE = {1 = 0}
DataF = {1 = "banish"}
Order = "banish"
Rng = {1 = 900.0}
Cost = {1 = 0}
Cool = {1 = 3.0}
Cast = {1 = 0.0}
targs = {1 = "air,ground,enemy,friend,self,neutral,organic,mechanical"}
Tip = "|cffcc66ff封印术 · 山|r(|cffffcc00E|r) |cffffcc00[无视魔免]|r"
Ubertip = "【无视魔免】将选定非建筑单位封入孤立的【封印之山】结界，在山巅与一个完全相同的全属性、全技能、全AI镜像展开死斗！|n- 只有最终存活的一方才能破封而出；|n- 若本尊获胜，本尊重返战场；|n- 若镜像获胜，该镜像将携全套能力破山而出并归属于你（可操控作战）；|n- 无攻击力单位（如小精灵）将在山内永世对峙直至你按 [R] 解封；|n- 输入 -mount 可随时切镜头观战。"

[A084]
_parent = "ANcl"
Name = "解封 · 破山"
Hotkey = "R"
Buttonpos_1 = 3
Buttonpos_2 = 2
levels = 1
hero = 0
item = 0
checkdep = 0
Requires = ""
Art = "ReplaceableTextures\\CommandButtons\\BTNEarthquake.blp"
"Art:hd" = "ReplaceableTextures\\CommandButtons\\BTNEarthquake.blp"
"Art:sd" = "ReplaceableTextures\\CommandButtons\\BTNEarthquake.blp"
CasterArt = ""
"CasterArt:hd" = ""
"CasterArt:sd" = ""
EffectArt = ""
"EffectArt:hd" = ""
"EffectArt:sd" = ""
TargetArt = ""
"TargetArt:hd" = ""
"TargetArt:sd" = ""
DataA = {1 = 0.0}
DataB = {1 = 0}
DataC = {1 = 1}
DataD = {1 = 0.0}
DataE = {1 = 0}
DataF = {1 = "tranquility"}
Order = "tranquility"
Cost = {1 = 0}
Cool = {1 = 1.0}
Cast = {1 = 0.0}
Tip = "|cffffcc00解封 · 破山|r(|cffffcc00R|r)"
Ubertip = "主动关闭【封印之山】：立刻摧毁山内镜像，并将仍存活的被封印单位安全释放回原位置。"
'''


def strip_old_section(text: str, start_marker: str) -> str:
    idx = text.find(f"\n[{start_marker}]")
    if idx < 0:
        if text.startswith(f"[{start_marker}]"):
            idx = 0
        else:
            return text
    return text[:idx].rstrip() + "\n"


def main():
    with open(UNIT_INI, "r", encoding="utf-8") as f:
        u_txt = f.read().replace("\r\n", "\n")
    assert "[u00A]" in u_txt and "[n005]" in u_txt and "[u00B]" in u_txt, "Missing expected base units in unit.ini!"
    u_txt = strip_old_section(u_txt, "u00B")
    u_txt = u_txt.rstrip() + "\n\n" + NEW_U00B.strip() + "\n"
    with open(UNIT_INI, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(u_txt)

    with open(ABIL_INI, "r", encoding="utf-8") as f:
        a_txt = f.read().replace("\r\n", "\n")
    assert "[A05A]" in a_txt and "[A060]" in a_txt and "[A082]" in a_txt, "Missing expected base abilities in ability.ini!"
    a_txt = strip_old_section(a_txt, "A083")
    a_txt = a_txt.rstrip() + "\n\n" + NEW_ABILS.strip() + "\n"
    with open(ABIL_INI, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(a_txt)

    tmp_w3x = os.path.join(ROOT, "tmp_v69_objs.w3x")
    if os.path.exists(tmp_w3x):
        os.remove(tmp_w3x)
    res = subprocess.run(
        [W2L_EXE, "obj", TPL_DIR, tmp_w3x],
        cwd=os.path.dirname(W2L_EXE),
        input=b"y\ny\n",
        capture_output=True,
        timeout=30,
    )
    if res.returncode != 0 or not os.path.exists(tmp_w3x):
        raise RuntimeError(
            f"w2l obj failed rc={res.returncode}: "
            f"{res.stdout.decode('utf-8','replace')} | {res.stderr.decode('utf-8','replace')}"
        )

    w3u_out = os.path.join(PAYLOAD_DIR, "war3map.w3u")
    w3a_out = os.path.join(PAYLOAD_DIR, "war3map.w3a")
    ps = rf'''
$ErrorActionPreference = 'Stop'
$asm = [Reflection.Assembly]::LoadFrom('{STORM_DLL}')
$mpq = New-Object StormLibSharp.MpqArchive('{tmp_w3x}', [System.IO.FileAccess]::Read)
$mpq.ExtractFile('war3map.w3u', '{w3u_out}')
$mpq.ExtractFile('war3map.w3a', '{w3a_out}')
$mpq.Dispose()
'''
    ps_res = subprocess.run(
        [r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe", "-NoProfile", "-Command", ps],
        capture_output=True, text=True, timeout=20,
    )
    if ps_res.returncode != 0:
        raise RuntimeError(f"Extract failed: {ps_res.stderr}")
    if os.path.exists(tmp_w3x):
        os.remove(tmp_w3x)

    w3u_sz = os.path.getsize(w3u_out)
    w3a_sz = os.path.getsize(w3a_out)
    assert w3u_sz >= 14249, f"Expected w3u >= 14249 B, got {w3u_sz}"
    assert w3a_sz > 76930, f"Expected w3a > 76930 B, got {w3a_sz}"
    print(f"[ok] Compiled & extracted v6.9 objs: w3u={w3u_sz} B, w3a={w3a_sz} B")


if __name__ == "__main__":
    main()
