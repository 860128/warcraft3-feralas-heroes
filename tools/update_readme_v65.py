# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.4 (Release v6.4)**"
    new_ver = "**当前版本：测试版v6.5 (Release v6.5)**"
    assert old_ver in text
    text = text.replace(old_ver, new_ver)

    old_sec96 = """### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.4 热修完备)"""
    new_sec96 = """### 9.6 中立机构【暗杀介绍所 · 幽影杀手公会】(`n005`) 与绝对机制克制系统 (v6.5 反进化波次重塑与忍者分身全清修复)"""
    assert old_sec96 in text
    text = text.replace(old_sec96, new_sec96)

    old_line = """  - 若当前波次杀手被全歼而目标仍存活（或靠重生复生站起），公会将在 3 秒后自动集结人数 `+2`（上限 12）、属性大幅增幅的下一波小队，直到目标彻底死亡为止。"""
    new_line = """  - **第1波试探先锋 + 反进化几何级暴涨曲线 (`v6.5`)**：第1波调弱为 `2~3` 名低门槛先锋，一旦遭目标或护卫歼灭，**每一波刷新前均实时重扫目标当时最新血量、主攻、护甲及成长层数**（如魔虚罗新增的适应度/翼化、虫皇新增的吞噬等），再叠加几何级波次狂暴倍率（第2波 `2.42x`、第3波 `5.36x`、第4波 `10.54x`、第5波 `18.68x`，人数 `+2` 上限 12，纯真伤由 `2.5%` 每波暴涨 `+4.5%` 至最高 `35% MaxHP`），越打越压倒性碾压！
  - **魔音忍者分身全清与替死修复 (`v6.5`)**：还原魔音忍者面对杀手时的分身替死逃生机制，同时修复“仅击杀本体一次杀手就消失”的 Bug——只要场上仍有任意存活分身 `u002`/`u001`，杀手小队绝不收队，自动追剿清光所有分身与本尊才宣告暗杀成功。"""
    if old_line not in text:
        # fallback match exact wording in README
        old_line = """  - 若当前波次杀手被全歼而目标仍存活（或靠重生复生站起），公会将在 3 秒后派出人数 `+2`（上限 12）、属性大幅增幅的下一波小队，直到目标彻底死亡为止。"""
    assert old_line in text
    text = text.replace(old_line, new_line)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.5!")

if __name__ == '__main__':
    update_readme()
