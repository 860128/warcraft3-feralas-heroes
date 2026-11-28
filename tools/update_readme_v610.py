# -*- coding: utf-8 -*-


def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.9 (Release v6.9)**"
    new_ver = "**当前版本：测试版v6.10 (Release v6.10)**"
    assert old_ver in text, "Missing old version header"
    text = text.replace(old_ver, new_ver, 1)

    anchor = "\n---\n\n## 10. 魔兽争霸III引擎避坑指南与开发铁律"
    sec_99 = """
### 9.9 【封印术 · 山】镜像满血满蓝生成与夺舍胜出全盛恢复 (`v6.10`)
- **入山满状态克隆 (`SM_CreateMirror`)**：不再继承本尊入山前的残血/低蓝状态，即使将残血或 1 血单位投入【封印之山】，生成的敌对镜像也始终以 **100% 满生命值、100% 满魔法值**（含 `H005` 万灵满蓄能百分比）全盛应战。
- **镜像夺舍全盛出山 (`SM_CloseAndRelease`)**：解决此前镜像险胜本尊后带着 1~2 滴残血破封出山的问题——镜像击杀本尊胜出并在完成状态移交与碰撞友军槽切换后，立即强制解除暂停/无敌、净化全部负面状态 (`UnitRemoveBuffs`)、重置所有技能冷却 (`UnitResetCooldown`)、并将生命与魔法恢复至 **100% 满值**（兼容 `H005` 变身、`H006` 法轮适应/待入蛋安全复位及 `H003`/`H004`），伴随圣光复苏特效回归战场。
"""
    assert anchor in text, "Missing anchor before Section 10"
    text = text.replace(anchor, "\n" + sec_99.strip() + "\n" + anchor, 1)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.10!")


if __name__ == '__main__':
    update_readme()
