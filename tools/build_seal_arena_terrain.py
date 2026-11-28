# -*- coding: utf-8 -*-
"""
Carves an isolated high-mountain arena (Seal Mountain) in the unused North-Center
margin of feralas_orig.w3x without altering any main battlefield tiles:
- Interior arena: tx in 74..85 (X=[-768, 768]), ty in 121..126 (Y=[7296, 8064])
- Center: (0.0, 7680.0)
- Writes modified payload/war3map.w3e and payload/war3map.wpm cleanly.
"""
import os
import struct
import subprocess

ROOT = r"C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
ORIG_MPQ = os.path.join(ROOT, "feralas_orig.w3x")
STORM_DLL = os.path.join(ROOT, "tools", "StormLibSharp.dll")
PAYLOAD_DIR = os.path.join(ROOT, "payload")
SCRATCH_W3E = os.path.join(ROOT, "tools", "_tmp_orig.w3e")
SCRATCH_WPM = os.path.join(ROOT, "tools", "_tmp_orig.wpm")


def extract_orig_terrain():
    ps = rf'''
$ErrorActionPreference = 'Stop'
$asm = [Reflection.Assembly]::LoadFrom('{STORM_DLL}')
$mpq = New-Object StormLibSharp.MpqArchive('{ORIG_MPQ}', [System.IO.FileAccess]::Read)
$mpq.ExtractFile('war3map.w3e', '{SCRATCH_W3E}')
$mpq.ExtractFile('war3map.wpm', '{SCRATCH_WPM}')
$mpq.Dispose()
'''
    res = subprocess.run(
        [r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe", "-NoProfile", "-Command", ps],
        capture_output=True, text=True, timeout=20,
    )
    if res.returncode != 0:
        raise RuntimeError(f"Extract w3e/wpm failed: {res.stderr}")


def carve_w3e(raw: bytes) -> bytes:
    buf = bytearray(raw)
    off = 13
    ng = struct.unpack_from('<I', buf, off)[0]
    off += 4 + ng * 4
    nc = struct.unpack_from('<I', buf, off)[0]
    off += 4 + nc * 4
    w, h, ox, oy = struct.unpack_from('<IIff', buf, off)
    off += 16
    assert w == 161 and h == 129, f"Unexpected W3E grid {w}x{h}"

    for vy in range(121, 128):
        for vx in range(74, 87):
            p = off + (vy * w + vx) * 7
            is_border = (vx in (74, 86)) or (vy in (121, 127))
            gh = 10800
            wl = 0x2200  # clear boundary bit 0x4000, normal dry height
            fl = 1 if is_border else 3  # 1=Ldro perimeter, 3=Lrok stone interior
            det = 0
            lv = (1 << 4) | 5  # cliff type 1 (CLgr), cliff level 5
            struct.pack_into('<HHBBB', buf, p, gh, wl, fl, det, lv)

    assert len(buf) == len(raw)
    return bytes(buf)


def carve_wpm(raw: bytes) -> bytes:
    buf = bytearray(raw)
    magic, ver, pw, ph = struct.unpack_from('<4sIII', buf, 0)
    assert magic == b'MP3W' and pw == 640 and ph == 512 and len(buf) == 16 + pw * ph

    # Enclosing unwalkable+unflyable ring: tx in 73..86, ty in 120..127
    # Interior walkable+flyable: tx in 74..85, ty in 121..126
    for ty in range(120, 128):
        for tx in range(73, 87):
            inside = (74 <= tx <= 85) and (121 <= ty <= 126)
            val = 0x00 if inside else 0x06
            for sy in range(4):
                row_base = 16 + (ty * 4 + sy) * pw + (tx * 4)
                for sx in range(4):
                    buf[row_base + sx] = val

    assert len(buf) == 327696
    return bytes(buf)


def main():
    extract_orig_terrain()
    with open(SCRATCH_W3E, 'rb') as f:
        orig_w3e = f.read()
    with open(SCRATCH_WPM, 'rb') as f:
        orig_wpm = f.read()

    new_w3e = carve_w3e(orig_w3e)
    new_wpm = carve_wpm(orig_wpm)

    out_w3e = os.path.join(PAYLOAD_DIR, 'war3map.w3e')
    out_wpm = os.path.join(PAYLOAD_DIR, 'war3map.wpm')
    with open(out_w3e, 'wb') as f:
        f.write(new_w3e)
    with open(out_wpm, 'wb') as f:
        f.write(new_wpm)

    for p in (SCRATCH_W3E, SCRATCH_WPM):
        if os.path.exists(p):
            os.remove(p)

    print(f"[ok] Carved Seal Mountain Arena: w3e={len(new_w3e)} B, wpm={len(new_wpm)} B")


if __name__ == '__main__':
    main()
