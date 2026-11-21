# -*- coding: utf-8 -*-
import os

with open('README.md', 'rb') as f:
    raw = f.read()

# Strip any leading BOMs
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]

text = raw.decode('utf-8')

# 1. Update version header
text = text.replace('**当前版本：测试版v5.5 (Release v5.5)**', '**当前版本：测试版v5.6 (Release v5.6)**')

# 2. Update TOC
text = text.replace(
    '8. [英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.2 四段式防御登神曲线与绝对免疫)](#8-英雄-5异界神将魔虚罗-h006-机制与-jass-架构-v52-四段式防御登神曲线与绝对免疫)',
    '8. [英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.6 颜值细节大升级与自制3D连续旋转八握剑法轮)](#8-英雄-5异界神将魔虚罗-h006-机制与-jass-架构-v56-颜值细节大升级与自制3d连续旋转八握剑法轮)'
)

# 3. Update Section 8 title
text = text.replace(
    '## 8. 英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.2 四段式防御登神曲线与绝对免疫)',
    '## 8. 英雄 5：异界神将·魔虚罗 (`H006`) 机制与 JASS 架构 (v5.6 颜值细节大升级与自制3D连续旋转八握剑法轮)'
)

# 4. Update Section 8.1
old_81 = """### 8.1 英雄档案与开局特性
- **模型与视觉呈现**：采用暴雪原版经典地狱火模型 (`units\\demon\\Infernal\\Infernal`)，开局与复活时通过 `SetUnitVertexColor(u, 255, 215, 60, 255)` 涂装为耀眼的圣金色，并在头顶挂载金色旋转光轮特效 `DevotionAura.mdl`（保存在 `udg_Maho_WheelFx[pId]` 中）。"""

new_81 = """### 8.1 英雄档案与开局特性
- **英雄本名与职业称号严格校正 (v5.6)**：
  - 职业称号：`Name = "异界神将"`（祭坛招募、酒馆与英雄属性面板职业类别显示）；
  - 英雄本名：`Propernames = "魔虚罗"`，`nameCount = 1`（**英雄本名严格指定为“魔虚罗”，彻底剔除武器名“八握剑”与“异界神将”别名带来的随机抽取混乱**）；
  - 提示信息：`Tip = "召唤 异界神将 - 魔虚罗(|cffffcc00M|r)"`、`Revivetip = "复活 异界神将 - 魔虚罗(|cffffcc00M|r)"`、`Awakentip = "唤醒 异界神将 - 魔虚罗(|cffffcc00M|r)"`。
- **外观模型与视觉呈现 (v5.6 暴雪原版炽焰熔岩魔像 + 圣金色涂装)**：
  - 采用暴雪原版经典赤红熔岩烈焰魔像模型 (`Units\\Creeps\\LavaSpawn\\LavaSpawn`)，开局与复活时通过 `SetUnitVertexColor(u, 255, 215, 60, 255)` 涂装为耀眼的圣金色，呈现“赤金烈焰神将”的恢弘质感；
  - 缩放设定为 `modelScale = 1.25`（威武高大），配套头像图标 `BTNLavaSpawn.blp` 与专属音效 `LavaSpawn`；
  - 头顶悬浮自制高精度连续 360° 自转的 3D 八握剑金色法轮 (`war3mapImported\\MahoWheel.mdx`)；
  - 达成 20 秒满速奔袭后，依然翼化升维蜕变为暴雪原版带翼末日神将 (`'nbal'`) 240 高空真飞行。"""

text = text.replace(old_81, new_81)

# 5. Add Section 8.6 after 8.5
sec_86 = """

### 8.6 颜值细节大升级与自制 3D 连续旋转八握剑法轮 (v5.6 重磅更新)
1. **英雄身份与本名校正**：
   - 彻底修复了暴雪引擎在 Altar 招募英雄时因 `Propernames` 列表中含有 `"八握剑"` 而随机将武器名作为英雄名字显示的 Bug。
   - 明确将 `Name` 设定为职业称号 **`"异界神将"`**，`Propernames` 严格锁死为 **`"魔虚罗"`**（`nameCount = 1`），保证召唤与复活时 100% 呈现霸气本名【魔虚罗】。
2. **赤金烈焰神将视觉重塑**：
   - 将原版略显死板的绿火地狱火模型替换为暴雪原版拥有完整奔跑、攻击、施法与熔岩爆燃动画的 **【红色炽焰熔岩魔像 (`Units\\Creeps\\LavaSpawn\\LavaSpawn`)】**；
   - 结合 JASS 层注入的 `SetUnitVertexColor(u, 255, 215, 60, 255)` 圣金色调色渲染，与暗红翻滚的岩浆内核相互辉映，展现极具压迫感的神将威仪；
   - 体积缩放提升至 **1.25 倍**，步伐沉稳强横。
3. **程序化算法自制 3D 八握剑法轮 (`war3mapImported\\MahoWheel.mdx`)**：
   - 编写独立算法构建脚本 `tools/build_maho_wheel_mdx.py`，严格遵循暴雪 MDX v800 二进制规格程序化生成专属高精 3D 轮盘模型：
     - **几何拓扑**：外环圆环（$R=46.0, r=5.0$，28 环段 $\\times$ 8 截面）、八方剑柄圆柱辐条（$R=10.0 \\sim 66.0, r=3.4$）、八向剑首金球（$R=67.0, r=6.8$，10 经线 $\\times$ 6 纬环）与中央金盘轴心（$R=12.0, H=9.0$），共计 834 顶点、1440 纯三角面；
     - **材质与光照**：采用魔兽争霸3原生内置的纯金队伍色贴图 `ReplaceableTextures\\TeamColor\\TeamColor04.blp`，启用双面漫反射渲染（`shadingFlags = 16`），全方位受光无黑面无背部穿帮；
     - **360° 无缝自转动画**：内置循环序列 `"Stand"`（4000ms 周期），配置 Bone 0 线性四元数关键帧旋转轨迹（`KGRT` 5 关键帧精确跨越四个象限 $0^\\circ \\to 90^\\circ \\to 180^\\circ \\to 270^\\circ \\to 360^\\circ$），实现恒定顺滑的因果之轮自转；
     - **内建二进制校验器**：打包脚本自检包含 `VERS(800)`、`MODL`、`SEQS`、`MTLS`、`TEXS`、`GEOS`、`GEOA`、`BONE`、`PIVT` 在内的全套标准区块，并严格校验四元数模长（$|\\mathbf{q}| = 1.0$）与面索引边界；
     - **流水线自动装配**：`do_rebuild.ps1` 自动递归扫描 `payload/war3mapImported/` 并将 37KB 极速加载的 `MahoWheel.mdx` 注入地图 MPQ；JASS `Maho_ApplyAppearance` 中精准挂载至 `"overhead"`，打造原汁原味的命运动态法轮。"""

# Insert before Section 9
idx_sec9 = text.find('## 9. 测试模式、沙盒指令与 AI 战略统帅体系')
assert idx_sec9 != -1, "Could not find Section 9 in README.md"
text = text[:idx_sec9] + sec_86.strip() + "\n\n---\n\n" + text[idx_sec9:]

# Format as CRLF and prepend UTF-8 BOM
out_text = text.replace('\r\n', '\n').replace('\n', '\r\n')
out_bytes = b'\xef\xbb\xbf' + out_text.encode('utf-8')

with open('README.md', 'wb') as f:
    f.write(out_bytes)

print("Successfully updated README.md with v5.6 documentation, BOM and CRLF preserved.")
