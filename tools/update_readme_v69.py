# -*- coding: utf-8 -*-

def update_readme():
    with open('README.md', 'rb') as f:
        data = f.read()

    has_bom = data.startswith(b'\xef\xbb\xbf')
    text = data[3:].decode('utf-8') if has_bom else data.decode('utf-8')
    is_crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    old_ver = "**当前版本：测试版v6.8 (Release v6.8)**"
    new_ver = "**当前版本：测试版v6.9 (Release v6.9)**"
    assert old_ver in text, "Missing old version header"
    text = text.replace(old_ver, new_ver, 1)

    anchor = "\n---\n\n## 10. 魔兽争霸III引擎避坑指南与开发铁律"
    sec_98 = """
### 9.8 实验技能【封印术 · 山】(`A083`, `[E]`, 无视魔免) 与镜像AI死斗结界 (`v6.9`)
- **正北高崖孤立小地图 (`war3map.w3e` / `war3map.wpm` + `SM_ClampLoop`)**：
  - 在菲拉斯原地图正北未利用的边界山体中单独雕琢出一块孤立高崖石台竞技场（`X = [-768, 768]`, `Y = [7296, 8064]`，中心 `(0, 7680)`，一圈不可通行/不可飞越结界悬崖 + `0.10s` 高频坐标钳位），并扩展相机北界至 `Y = 8192`，输入 **`-mount`**（或 `-mountain`）可随时切镜头观战。
- **`[E]` 封印术 · 山 (`A083`，`DataC = 13` 无视魔免/虚无)**：
  - 将任意非建筑目标投入【封印之山】，并在对面生成一尊隶属 `Player(13)` 的**全属性、全物品、全技能、全状态镜像**：
    - 完整拷贝白字属性、实时血蓝/攻防/移速/攻速、6 格物品、所有标准英雄/Boss 技能与五大自定义英雄深度进度（魔虚罗四维适应度/3D法轮/翼化状态、万灵 90 态变身与全套伥鬼名单、虫皇进化阶位与偷取技能、忍者光环与分身替死结界隔离、幻梦大师技能）；
    - **独立全套 AI 镜像引擎 (`SM_RunMirrorAI`)**：魔虚罗镜像会自动转轮适应并吃 E 清状态、万灵镜像会择机开 D 召兽群与伥鬼并动态切换三态/龙神、虫皇/忍者/幻梦镜像执行对应连招，传统英雄与带技能野怪自动施放约 90 个官方主动技能，普通步兵/小兵自动平 A，无攻击单位（如小精灵）将在山内永世对峙。
  - **生死归属结算 (`SM_CloseAndRelease`)**：只有最终存活一方能破山而出——若本尊获胜，本尊重返原位；若镜像获胜，该镜像连同全套战力破山而出**永久归属于施法玩家**（若与己方已有自定义英雄撞槽，则自动使用共享控制友军槽位 `Player(14)`/`Player(15)` 独立运行四维数据，互不串槽冲突）。
- **`[R]` 解封 · 破山 (`A084`)**：随时点击关闭封印之山，立刻销毁镜像并将仍存活的被封印目标安全送回原位。
"""
    assert anchor in text, "Missing anchor before Section 10"
    text = text.replace(anchor, "\n" + sec_98.strip() + "\n" + anchor, 1)

    out_text = text.replace('\n', '\r\n') if is_crlf else text
    out_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + out_text.encode('utf-8')
    with open('README.md', 'wb') as f:
        f.write(out_bytes)
    print("README.md successfully updated for v6.9!")


if __name__ == '__main__':
    update_readme()
