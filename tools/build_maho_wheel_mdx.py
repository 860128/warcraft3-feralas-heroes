"""
tools/build_maho_wheel_mdx.py
Generates the custom 3D artifact model: Eight-Grip Sword Cross Wheel (MahoWheel.mdx)
Format: Blizzard MDX (v800) format for Warcraft III.
Includes:
- Torus outer ring: R=46.0, r=5.0 (28 seg x 8 cs)
- 8 Spokes: cylindrical bars along 0..315 deg extending to R=66.0, radius 3.4
- 8 Pommel Spheres: at spoke tips (R=67.0), radius 6.8 (10 lon x 6 lat)
- Central Hub: cylinder/disc (R=12.0, H=9.0)
- Z position: centered around Z=+18.0
- Continuous 360-degree rotation animation ("Stand", 4000ms loop, 5 KGRT keyframes)
- Texture: Textures\\white.blp (Pure golden yellow)
- Double-sided material (shadingFlags = 16)
- Built-in binary self-verification validating all chunks, offsets, and quaternion norms.
"""

import os
import sys
import math
import struct

def generate_maho_wheel_mdx(output_path="payload/war3mapImported/MahoWheel.mdx"):
    vertices = []
    normals = []
    uvs = []
    triangles = []

    def add_vertex(pos, norm, uv):
        idx = len(vertices)
        vertices.append(pos)
        normals.append(norm)
        uvs.append(uv)
        return idx

    def add_triangle(i0, i1, i2):
        triangles.append((i0, i1, i2))

    # Center Z offset
    Z_center = 18.0

    # ---------------------------------------------------------
    # 1. Torus Outer Ring: R=46.0, r=5.0 (28 segments x 8 cs)
    # ---------------------------------------------------------
    R_torus = 46.0
    r_torus = 5.0
    N_torus_seg = 28
    N_torus_cs = 8
    torus_grid = []

    for i in range(N_torus_seg):
        row = []
        theta = 2.0 * math.pi * i / N_torus_seg
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        for j in range(N_torus_cs):
            phi = 2.0 * math.pi * j / N_torus_cs
            cos_p = math.cos(phi)
            sin_p = math.sin(phi)
            x = (R_torus + r_torus * cos_p) * cos_t
            y = (R_torus + r_torus * cos_p) * sin_t
            z = Z_center + r_torus * sin_p
            nx = cos_p * cos_t
            ny = cos_p * sin_t
            nz = sin_p
            u = i / N_torus_seg
            v = j / N_torus_cs
            idx = add_vertex((x, y, z), (nx, ny, nz), (u, v))
            row.append(idx)
        torus_grid.append(row)

    for i in range(N_torus_seg):
        i_next = (i + 1) % N_torus_seg
        for j in range(N_torus_cs):
            j_next = (j + 1) % N_torus_cs
            v00 = torus_grid[i][j]
            v10 = torus_grid[i_next][j]
            v01 = torus_grid[i][j_next]
            v11 = torus_grid[i_next][j_next]
            add_triangle(v00, v10, v11)
            add_triangle(v00, v11, v01)

    # ---------------------------------------------------------
    # 2. 8 Spokes: R_in=10.0, R_out=66.0, radius=3.4, 8 cs
    # ---------------------------------------------------------
    r_spoke = 3.4
    R_in = 10.0
    R_out = 66.0
    N_spoke_cs = 8

    for k in range(8):
        alpha = k * (math.pi / 4.0)
        cos_a = math.cos(alpha)
        sin_a = math.sin(alpha)
        ux, uy, uz = -sin_a, cos_a, 0.0
        wx, wy, wz = 0.0, 0.0, 1.0
        spoke_in_idx = []
        spoke_out_idx = []
        for m in range(N_spoke_cs):
            beta = 2.0 * math.pi * m / N_spoke_cs
            cos_b = math.cos(beta)
            sin_b = math.sin(beta)
            nx = cos_b * ux + sin_b * wx
            ny = cos_b * uy + sin_b * wy
            nz = cos_b * uz + sin_b * wz
            ox = r_spoke * nx
            oy = r_spoke * ny
            oz = r_spoke * nz
            pin = (R_in * cos_a + ox, R_in * sin_a + oy, Z_center + oz)
            pout = (R_out * cos_a + ox, R_out * sin_a + oy, Z_center + oz)
            idx_in = add_vertex(pin, (nx, ny, nz), (0.0, m / N_spoke_cs))
            idx_out = add_vertex(pout, (nx, ny, nz), (1.0, m / N_spoke_cs))
            spoke_in_idx.append(idx_in)
            spoke_out_idx.append(idx_out)
        for m in range(N_spoke_cs):
            m_next = (m + 1) % N_spoke_cs
            v0 = spoke_in_idx[m]
            v1 = spoke_out_idx[m]
            v2 = spoke_in_idx[m_next]
            v3 = spoke_out_idx[m_next]
            add_triangle(v0, v1, v3)
            add_triangle(v0, v3, v2)

    # ---------------------------------------------------------
    # 3. 8 Pommel Spheres: tips at R=67.0, radius=6.8, 10 lon x 6 lat
    # ---------------------------------------------------------
    r_pommel = 6.8
    R_pommel = 67.0
    N_lon = 10
    N_lat = 6

    for k in range(8):
        alpha = k * (math.pi / 4.0)
        cx = R_pommel * math.cos(alpha)
        cy = R_pommel * math.sin(alpha)
        cz = Z_center
        top_idx = add_vertex((cx, cy, cz + r_pommel), (0.0, 0.0, 1.0), (0.5, 1.0))
        bot_idx = add_vertex((cx, cy, cz - r_pommel), (0.0, 0.0, -1.0), (0.5, 0.0))
        lat_rows = []
        for b in range(1, N_lat):
            phi = -math.pi / 2.0 + math.pi * b / N_lat
            cos_p = math.cos(phi)
            sin_p = math.sin(phi)
            row = []
            for l in range(N_lon):
                lam = 2.0 * math.pi * l / N_lon
                nx = cos_p * math.cos(lam)
                ny = cos_p * math.sin(lam)
                nz = sin_p
                px = cx + r_pommel * nx
                py = cy + r_pommel * ny
                pz = cz + r_pommel * nz
                idx = add_vertex((px, py, pz), (nx, ny, nz), (l / N_lon, b / N_lat))
                row.append(idx)
            lat_rows.append(row)
        # Top cap
        for l in range(N_lon):
            l_next = (l + 1) % N_lon
            add_triangle(top_idx, lat_rows[-1][l_next], lat_rows[-1][l])
        # Middle quads
        for b in range(len(lat_rows) - 1):
            for l in range(N_lon):
                l_next = (l + 1) % N_lon
                v00 = lat_rows[b][l]
                v10 = lat_rows[b][l_next]
                v01 = lat_rows[b+1][l]
                v11 = lat_rows[b+1][l_next]
                add_triangle(v00, v10, v11)
                add_triangle(v00, v11, v01)
        # Bottom cap
        for l in range(N_lon):
            l_next = (l + 1) % N_lon
            add_triangle(bot_idx, lat_rows[0][l], lat_rows[0][l_next])

    # ---------------------------------------------------------
    # 4. Central Hub: R=12.0, H=9.0, 16 segments
    # ---------------------------------------------------------
    R_hub = 12.0
    H_hub = 9.0
    N_hub = 16
    z_top = Z_center + H_hub / 2.0
    z_bot = Z_center - H_hub / 2.0
    hub_top_center = add_vertex((0.0, 0.0, z_top), (0.0, 0.0, 1.0), (0.5, 0.5))
    hub_bot_center = add_vertex((0.0, 0.0, z_bot), (0.0, 0.0, -1.0), (0.5, 0.5))
    top_ring = []
    bot_ring = []
    side_top = []
    side_bot = []

    for s in range(N_hub):
        psi = 2.0 * math.pi * s / N_hub
        cos_s = math.cos(psi)
        sin_s = math.sin(psi)
        px = R_hub * cos_s
        py = R_hub * sin_s
        top_ring.append(add_vertex((px, py, z_top), (0.0, 0.0, 1.0), (0.5 + 0.5 * cos_s, 0.5 + 0.5 * sin_s)))
        bot_ring.append(add_vertex((px, py, z_bot), (0.0, 0.0, -1.0), (0.5 + 0.5 * cos_s, 0.5 + 0.5 * sin_s)))
        side_top.append(add_vertex((px, py, z_top), (cos_s, sin_s, 0.0), (s / N_hub, 1.0)))
        side_bot.append(add_vertex((px, py, z_bot), (cos_s, sin_s, 0.0), (s / N_hub, 0.0)))

    for s in range(N_hub):
        s_next = (s + 1) % N_hub
        # Top cap
        add_triangle(hub_top_center, top_ring[s_next], top_ring[s])
        # Bottom cap
        add_triangle(hub_bot_center, bot_ring[s], bot_ring[s_next])
        # Side wall
        v0 = side_bot[s]
        v1 = side_top[s]
        v2 = side_bot[s_next]
        v3 = side_top[s_next]
        add_triangle(v0, v1, v3)
        add_triangle(v0, v3, v2)

    # ---------------------------------------------------------
    # MDX Binary Assembly
    # ---------------------------------------------------------
    buf = bytearray()
    buf += b'MDLX'

    # VERS (800)
    buf += b'VERS'
    buf += struct.pack('<II', 4, 800)

    # MODL
    modl_data = bytearray()
    modl_data += b'MahoWheel'.ljust(80, b'\x00')
    modl_data += b''.ljust(260, b'\x00')
    modl_data += struct.pack('<fffffffI', 80.0, -80.0, -80.0, 0.0, 80.0, 80.0, 40.0, 150)
    buf += b'MODL'
    buf += struct.pack('<I', len(modl_data))
    buf += modl_data

    # SEQS ("Stand", 4000ms loop)
    seqs_data = bytearray()
    seqs_data += b'Stand'.ljust(80, b'\x00')
    seqs_data += struct.pack('<II', 0, 4000)
    seqs_data += struct.pack('<f', 0.0) # moveSpeed
    seqs_data += struct.pack('<I', 0)   # flags (0 = looping)
    seqs_data += struct.pack('<f', 0.0) # rarity
    seqs_data += struct.pack('<I', 0)   # syncPoint
    seqs_data += struct.pack('<fffffff', 80.0, -80.0, -80.0, 0.0, 80.0, 80.0, 40.0)
    buf += b'SEQS'
    buf += struct.pack('<I', len(seqs_data))
    buf += seqs_data

    # MTLS (Double-sided material, shadingFlags = 16)
    mtls_data = bytearray()
    mat_data = bytearray()
    lay_data = bytearray()
    lay_data += struct.pack('<IIIIII', 28, 0, 16, 0, 0xFFFFFFFF, 0) # size=28, filter=0, shading=16, tex=0, anim=-1, coord=0
    lay_data += struct.pack('<f', 1.0) # alpha
    mat_data += struct.pack('<III', 4 + 4 + 4 + 8 + len(lay_data), 0, 0)
    mat_data += b'LAYS'
    mat_data += struct.pack('<I', 1)
    mat_data += lay_data
    mtls_data += mat_data
    buf += b'MTLS'
    buf += struct.pack('<I', len(mtls_data))
    buf += mtls_data

    # TEXS (TeamColor04.blp - pure golden yellow)
    texs_data = bytearray()
    texs_data += struct.pack('<I', 0) # replaceableId
    texs_data += b'Textures\\white.blp'.ljust(260, b'\x00')
    texs_data += struct.pack('<I', 0) # flags
    buf += b'TEXS'
    buf += struct.pack('<I', len(texs_data))
    buf += texs_data

    # GEOS (Geoset with full VRTX, NRMS, PTYP, PCNT, PVTX, GNDX, MTGC, MATS, UVAS)
    geos_data = bytearray()
    geoset = bytearray()
    # VRTX
    geoset += b'VRTX'
    geoset += struct.pack('<I', len(vertices))
    for v in vertices:
        geoset += struct.pack('<fff', v[0], v[1], v[2])
    # NRMS
    geoset += b'NRMS'
    geoset += struct.pack('<I', len(normals))
    for n in normals:
        geoset += struct.pack('<fff', n[0], n[1], n[2])
    # PTYP (4 = Triangles)
    geoset += b'PTYP'
    geoset += struct.pack('<II', 1, 4)
    # PCNT (Total index count)
    geoset += b'PCNT'
    geoset += struct.pack('<II', 1, len(triangles) * 3)
    # PVTX (Index array uint16)
    geoset += b'PVTX'
    geoset += struct.pack('<I', len(triangles) * 3)
    for tri in triangles:
        geoset += struct.pack('<HHH', tri[0], tri[1], tri[2])
    # GNDX (Vertex group array, all 0)
    geoset += b'GNDX'
    geoset += struct.pack('<I', len(vertices))
    geoset += b'\x00' * len(vertices)
    # MTGC (1 group)
    geoset += b'MTGC'
    geoset += struct.pack('<II', 1, 1)
    # MATS (Matrix index pointing to Bone 0)
    geoset += b'MATS'
    geoset += struct.pack('<II', 1, 0)
    # Material ID 0, Selection Group 0, Selection Flags 0
    geoset += struct.pack('<III', 0, 0, 0)
    # Bounds Extents
    geoset += struct.pack('<fffffff', 80.0, -80.0, -80.0, 0.0, 80.0, 80.0, 40.0)
    geoset += struct.pack('<I', 0) # extentsCount
    # UVAS / UVBS
    geoset += b'UVAS'
    geoset += struct.pack('<I', 1)
    geoset += b'UVBS'
    geoset += struct.pack('<I', len(uvs))
    for uv in uvs:
        geoset += struct.pack('<ff', uv[0], uv[1])

    total_geoset_len = 4 + len(geoset)
    geos_data += struct.pack('<I', total_geoset_len)
    geos_data += geoset
    buf += b'GEOS'
    buf += struct.pack('<I', len(geos_data))
    buf += geos_data

    # GEOA (Geoset Animation: static alpha=1.0, tint color=(1.0, 1.0, 1.0))
    geoa_entry = bytearray()
    geoa_entry += struct.pack('<IfI', 28, 1.0, 0)
    geoa_entry += struct.pack('<fff', 1.0, 1.0, 1.0)
    geoa_entry += struct.pack('<I', 0)
    buf += b'GEOA'
    buf += struct.pack('<I', len(geoa_entry))
    buf += geoa_entry

    # BONE (Bone 0 with continuous 360-degree KGRT rotation track)
    node_data = bytearray()
    node_data += b'Bone_Wheel'.ljust(80, b'\x00')
    node_data += struct.pack('<III', 0, 0xFFFFFFFF, 256)

    kgrt = bytearray()
    kgrt += b'KGRT'
    kgrt += struct.pack('<III', 5, 1, 0xFFFFFFFF) # 5 keys, Linear interpolation, globalSeqId = -1

    # 5 Keyframes for continuous 360-degree rotation around Z axis:
    # t=0:    (0, 0, 0, 1)
    # t=1000: (0, 0, 0.70710678, 0.70710678)
    # t=2000: (0, 0, 1, 0)
    # t=3000: (0, 0, 0.70710678, -0.70710678)
    # t=4000: (0, 0, 0, -1)
    keys = [
        (0, 0.0, 0.0, 0.0, 1.0),
        (1000, 0.0, 0.0, 0.70710678, 0.70710678),
        (2000, 0.0, 0.0, 1.0, 0.0),
        (3000, 0.0, 0.0, 0.70710678, -0.70710678),
        (4000, 0.0, 0.0, 0.0, -1.0)
    ]
    for k in keys:
        kgrt += struct.pack('<iffff', k[0], k[1], k[2], k[3], k[4])

    node_inc_size = 4 + len(node_data) + len(kgrt)
    bone_entry = bytearray()
    bone_entry += struct.pack('<I', node_inc_size)
    bone_entry += node_data
    bone_entry += kgrt
    bone_entry += struct.pack('<II', 0xFFFFFFFF, 0xFFFFFFFF) # geosetId, geosetAnimationId

    buf += b'BONE'
    buf += struct.pack('<I', len(bone_entry))
    buf += bone_entry

    # PIVT (Pivot point at center of rotation: 0.0, 0.0, 18.0)
    pivt_data = bytearray()
    pivt_data += struct.pack('<fff', 0.0, 0.0, Z_center)
    buf += b'PIVT'
    buf += struct.pack('<I', len(pivt_data))
    buf += pivt_data

    # ---------------------------------------------------------
    # Built-in Binary Self-Verification
    # ---------------------------------------------------------
    assert buf[:4] == b'MDLX', "Magic check failed: expected MDLX"
    pos = 4
    found_chunks = []
    while pos < len(buf):
        tag = buf[pos:pos+4].decode('latin1', errors='replace')
        size = struct.unpack('<I', buf[pos+4:pos+8])[0]
        cdata = buf[pos+8:pos+8+size]
        found_chunks.append((tag, size))
        pos += 8 + size
    assert pos == len(buf), f"File boundary mismatch: pos={pos}, total={len(buf)}"

    # Validate quaternion norms
    for k in keys:
        norm_sq = k[1]**2 + k[2]**2 + k[3]**2 + k[4]**2
        assert abs(norm_sq - 1.0) < 1e-5, f"Quaternion norm error: {k}"

    # Validate triangle indices
    for tri in triangles:
        for idx in tri:
            assert 0 <= idx < len(vertices), f"Index out of bounds: {idx} >= {len(vertices)}"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(buf)

    print(f"[SUCCESS] MahoWheel.mdx generated successfully!")
    print(f"  Output path: {output_path}")
    print(f"  Total file size: {len(buf)} bytes")
    print(f"  Total vertices: {len(vertices)}, Total triangles: {len(triangles)}")
    print(f"  Chunks verified: {[c[0] for c in found_chunks]}")
    return True

if __name__ == '__main__':
    generate_maho_wheel_mdx()
