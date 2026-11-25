"""Blender icinde calisir: parametreler.json + ozet.json -> 3B model.

Kullanim (Blender Python):
    KOD = "v1"; exec(open(r".../hesaplamalar/model_olustur.py", encoding="utf-8").read())
Eksenler: X = geriye (kok hucum kenarindan), Y = aciklik, Z = yukari. Birim: metre.
"""
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(globals().get("PROJE_KOK") or (Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd()))  # exec() icinde: PROJE_KOK ver ya da Hezarfen_Flight_Challenge'da calistir
import sys
KOD = globals().get("KOD", "v1")
if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 1:      # blender -b --python model_olustur.py -- v2a
    KOD = sys.argv[sys.argv.index("--") + 1]
P = json.loads((ROOT / "hesaplamalar" / "parametreler.json").read_text(encoding="utf-8"))
O = json.loads((ROOT / "hesaplamalar" / "ozet.json").read_text(encoding="utf-8"))
T, R = P["tasarimlar"][KOD], O["tasarimlar"][KOD]
K, KU, ISK, PK = T["kanat"], T["kuyruk"], T["iskelet"], T["pilot_konumu"]
ST, YARI = K["istasyonlar"], K["yari_aciklik_m"]
TAN_D = math.tan(math.radians(K["dihedral_derece"]))
KAM = K["kambur_orani"]

# ---- sahneyi temizle (varsayilan sahne) ----
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
col = bpy.data.collections.new(f"Hezarfen_{KOD}")
bpy.context.scene.collection.children.link(col)


def mat(ad, renk, rough=0.7, emis=0.0):
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Roughness"].default_value = rough
    if emis:
        for k in ("Emission Color", "Emission"):
            if k in b.inputs:
                b.inputs[k].default_value = (*renk, 1)
                break
        if "Emission Strength" in b.inputs:
            b.inputs["Emission Strength"].default_value = emis
    return m


if T.get("teknoloji") == "modern":
    M_BEZ = mat("sentetik_yelken_bezi", (0.85, 0.87, 0.90), 0.5)
    M_DIS = mat("aluminyum_boru", (0.55, 0.57, 0.60), 0.3)
    M_SOG = mat("profil_citasi", (0.45, 0.47, 0.50), 0.4)
    M_IP = mat("celik_tel", (0.15, 0.15, 0.16), 0.4)
else:
    M_BEZ = mat("mumlu_keten", (0.80, 0.70, 0.50), 0.85)
    M_DIS = mat("disbudak", (0.42, 0.25, 0.11), 0.6)
    M_SOG = mat("sogut", (0.62, 0.45, 0.24), 0.6)
    M_IP = mat("kendir_ip", (0.30, 0.27, 0.22), 0.9)
M_PIL = mat("pilot_temsili", (0.55, 0.57, 0.60), 0.8)
M_AM = mat("AM_isareti", (0.9, 0.02, 0.05), 0.4, 3.0)
M_NN = mat("NN_isareti", (0.02, 0.6, 0.3), 0.4, 3.0)
M_ZEM = mat("zemin", (0.33, 0.35, 0.36), 0.95)


def link(ob, m=None):
    col.objects.link(ob)
    if m:
        ob.data.materials.append(m)
    return ob


def z_kanat(xi, c, y):
    """Kambur (parabolik yay) + dihedral."""
    return 4 * KAM * c * xi * (1 - xi) + abs(y) * TAN_D


def interp(y, key):
    y = abs(y)
    for a, b in zip(ST, ST[1:]):
        if a["y"] <= y <= b["y"]:
            f = (y - a["y"]) / (b["y"] - a["y"])
            return a[key] + f * (b[key] - a[key])
    return ST[-1][key]


def kanat_noktasi(xi, y):
    c = interp(y, "veter")
    return Vector((interp(y, "x_hucum") + xi * c, y, z_kanat(xi, c, y)))


def egri(ad, noktalar, yaricaplar, m):
    cu = bpy.data.curves.new(ad, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 1.0
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(noktalar) - 1)
    for p, co, r in zip(sp.points, noktalar, yaricaplar):
        p.co = (*co, 1.0)
        p.radius = r
    return link(bpy.data.objects.new(ad, cu), m)


# ---- kaplama ----
NX = 14
for isa, ad in ((1, "sag"), (-1, "sol")):
    ys = []
    for a, b in zip(ST, ST[1:]):
        ys += [a["y"] + (b["y"] - a["y"]) * i / 3 for i in range(3)]
    ys.append(ST[-1]["y"])
    verts, faces = [], []
    for y in ys:
        for i in range(NX + 1):
            verts.append(kanat_noktasi(i / NX, isa * y))
    for j in range(len(ys) - 1):
        for i in range(NX):
            a = j * (NX + 1) + i
            faces.append((a, a + 1, a + NX + 2, a + NX + 1))
    me = bpy.data.meshes.new(f"kaplama_{ad}")
    me.from_pydata(verts, [], faces)
    me.update()
    ob = link(bpy.data.objects.new(f"kaplama_{ad}", me), M_BEZ)
    for p in me.polygons:
        p.use_smooth = True
    sol = ob.modifiers.new("kalinlik", "SOLIDIFY")
    sol.thickness = 0.004

    # ---- ana kirisler (konik) ----
    for n, oran in enumerate(ISK["kiris_x_veter_orani"]):
        pts, rs = [], []
        for s in ST:
            if s["veter"] * (1 - oran) <= 0.05:
                continue
            p = kanat_noktasi(oran, isa * s["y"])
            p.z -= 0.03
            pts.append(p)
            f = s["y"] / YARI
            rs.append(0.5 * (ISK["kiris_cap_kok_m"] + f * (ISK["kiris_cap_uc_m"] - ISK["kiris_cap_kok_m"])))
        egri(f"kiris{n + 1}_{ad}", pts, rs, M_DIS)

    # ---- nervurler ----
    nn = ISK["nervur_adet_yarim_kanat"]
    for i in range(nn):
        y = isa * YARI * (i + 0.5) / nn
        pts = [kanat_noktasi(k / 10, y) - Vector((0, 0, 0.012)) for k in range(11)]
        egri(f"nervur{i + 1}_{ad}", pts, [ISK["nervur_cap_m"] / 2] * 11, M_SOG)

    # ---- gergi halatlari ----
    gy = isa * YARI * ISK["gergi_y_orani"]
    dr = ISK["direk"]
    xd = PK["x_m"] + 0.15
    for n, oran in enumerate(ISK["kiris_x_veter_orani"]):
        hedef = kanat_noktasi(oran, gy)
        egri(f"gergi_ust{n}_{ad}", [Vector((xd, 0, dr["yukseklik_ust_m"])), hedef], [0.004] * 2, M_IP)
        egri(f"gergi_alt{n}_{ad}", [Vector((xd, 0, -dr["yukseklik_alt_m"])), hedef], [0.004] * 2, M_IP)

# ---- direk, kuyruk kirisi, kuyruk ----
dr, kb = ISK["direk"], ISK["kuyruk_kirisi"]
xd = PK["x_m"] + 0.15
egri("direk", [Vector((xd, 0, -dr["yukseklik_alt_m"])), Vector((xd, 0, dr["yukseklik_ust_m"]))], [dr["cap_m"] / 2] * 2, M_DIS)
kx, kc, kb2 = KU["x_hucum_m"], KU["veter_m"], KU["aciklik_m"] / 2
x_son = kx + kc
egri("kuyruk_kirisi", [Vector((x_son - kb["uzunluk_m"], 0, 0.02)), Vector((x_son, 0, KU["z_m"]))], [kb["cap_m"] / 2] * 2, M_DIS)
egri("gergi_kuyruk", [Vector((xd, 0, dr["yukseklik_ust_m"])), Vector((kx + kc * 0.5, 0, KU["z_m"]))], [0.004] * 2, M_IP)
me = bpy.data.meshes.new("kuyruk")
z = KU["z_m"] + 0.02
me.from_pydata([(kx, 0, z), (x_son, -kb2, z), (kx + kc * 0.85, 0, z), (x_son, kb2, z)], [], [(0, 1, 2), (0, 2, 3)])
ob = link(bpy.data.objects.new("kuyruk", me), M_BEZ)
ob.modifiers.new("kalinlik", "SOLIDIFY").thickness = 0.004
for isa in (1, -1):
    egri(f"kuyruk_kenar{isa}", [Vector((kx, 0, z)), Vector((x_son, isa * kb2, z))], [0.008] * 2, M_SOG)

# ---- pilot (temsili kutle; anatomik model degil) ----
px, pz = PK["x_m"], PK["z_m"]


def kapsul(ad, a, b, r):
    return egri(ad, [Vector(a), Vector(b)], [r, r], M_PIL)


YATAY = PK.get("yatay", False)
if YATAY:
    kapsul("pilot_govde", (px - 0.30, 0, pz), (px + 0.32, 0, pz), 0.16)
    kapsul("pilot_bacak_sag", (px + 0.32, 0.09, pz), (px + 1.17, 0.09, pz), 0.075)
    kapsul("pilot_bacak_sol", (px + 0.32, -0.09, pz), (px + 1.17, -0.09, pz), 0.075)
    BAS, OMUZ_X, OMUZ_Z = (px - 0.52, 0, pz + 0.05), px - 0.25, pz
else:
    kapsul("pilot_govde", (px, 0, pz), (px, 0, pz + 0.62), 0.16)
    kapsul("pilot_bacak_sag", (px, 0.09, pz - 0.85), (px, 0.09, pz), 0.075)
    kapsul("pilot_bacak_sol", (px, -0.09, pz - 0.85), (px, -0.09, pz), 0.075)
    BAS, OMUZ_X, OMUZ_Z = (px, 0, pz + 0.75), px, pz + 0.55
me = bpy.data.meshes.new("pilot_bas")
ob = link(bpy.data.objects.new("pilot_bas", me), M_PIL)
import bmesh
bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.11)
bm.to_mesh(me)
bm.free()
ob.location = BAS
for isa, ad in ((1, "sag"), (-1, "sol")):
    omuz = Vector((OMUZ_X, isa * 0.2, OMUZ_Z))
    tutus = kanat_noktasi(ISK["kiris_x_veter_orani"][0], isa * 0.75) - Vector((0, 0, 0.05))
    kapsul(f"pilot_kol_{ad}", omuz, tutus, 0.045)

# ---- teknik referanslar: agirlik merkezi (AM) ve notr nokta (NN) ----
den = R["denge"]
for ad, konum, m in (("AM_agirlik_merkezi", (den["x_cg"], 0, den["z_cg"]), M_AM), ("NN_notr_nokta", (den["x_np"], 0, 0.0), M_NN)):
    me = bpy.data.meshes.new(ad)
    ob = link(bpy.data.objects.new(ad, me), m)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=0.06)
    bm.to_mesh(me)
    bm.free()
    ob.location = konum
    ob.show_in_front = True
for ad, konum, yazi in (("etiket_AM", (den["x_cg"] - 0.1, -0.9, den["z_cg"] - 0.05), "AM"), ("etiket_NN", (den["x_np"] + 0.1, -0.9, 0.12), "NN")):
    cu = bpy.data.curves.new(ad, "FONT")
    cu.body = yazi
    cu.size = 0.22
    cu.extrude = 0.005
    ob = link(bpy.data.objects.new(ad, cu), M_AM if yazi == "AM" else M_NN)
    ob.location = konum
    ob.rotation_euler = (math.radians(90), 0, 0)

# ---- sunum: zemin, isik, kamera ----
ZEMIN_Z = min(pz - 0.85 - 0.075, -ISK["direk"]["yukseklik_alt_m"]) - 0.6   # model yerden 0.6 m yukarida asili gosterilir
me = bpy.data.meshes.new("zemin")
me.from_pydata([(-40, -40, ZEMIN_Z), (40, -40, ZEMIN_Z), (40, 40, ZEMIN_Z), (-40, 40, ZEMIN_Z)], [], [(0, 1, 2, 3)])
link(bpy.data.objects.new("zemin", me), M_ZEM)
sun = bpy.data.lights.new("gunes", "SUN")
sun.energy = 3.5
sun.angle = math.radians(8)
so = link(bpy.data.objects.new("gunes", sun))
so.rotation_euler = (math.radians(50), math.radians(10), math.radians(-40))
w = bpy.context.scene.world or bpy.data.worlds.new("World")
bpy.context.scene.world = w
w.use_nodes = True
bg = next((n for n in w.node_tree.nodes if n.type == "BACKGROUND"), None)
if bg:
    bg.inputs[0].default_value = (0.62, 0.74, 0.90, 1)
    bg.inputs[1].default_value = 0.9
cam = bpy.data.cameras.new("kamera")
cam.lens = 35
co = link(bpy.data.objects.new("kamera", cam))
co.location = Vector((-4.6, -5.6, -1.25)) * (YARI / 3.5)   # alttan-onden: iskelet kaplamanin altinda oldugu icin
hedef = Vector((1.25, 0.0, -0.15))
co.rotation_euler = (hedef - co.location).to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.camera = co

# ---- olcu dogrulama ----
dg = bpy.context.evaluated_depsgraph_get()
mn, mx = Vector((1e9,) * 3), Vector((-1e9,) * 3)
for ob in col.objects:
    if not ob.name.startswith(("kaplama", "kuyruk")):
        continue
    e = ob.evaluated_get(dg)
    for c in e.bound_box:
        v = e.matrix_world @ Vector(c)
        mn = Vector(map(min, mn, v))
        mx = Vector(map(max, mx, v))
print(f"MODEL {KOD}: aciklik(Y)={mx.y - mn.y:.3f} m (JSON {2 * YARI:.3f}) | boy(X)={mx.x - mn.x:.3f} m (JSON {x_son - min(s['x_hucum'] for s in ST):.3f}) | nesne={len(col.objects)}")

# ---- arka planda (blender -b) calisiyorsa dosyayi kaydet ----
if bpy.app.background:
    klasor = ROOT / ("tasarim_v1" if KOD == "v1" else f"tasarim_v2/{KOD}")
    klasor.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(klasor / "model.blend"))
    print("kaydedildi:", klasor / "model.blend")
