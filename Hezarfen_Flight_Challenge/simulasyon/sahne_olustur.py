"""Blender suzulme sahnesi: ucus_verileri.csv -> keyframe + HUD. Basitlestirilmis model; CFD DEGILDIR.

Calistirma:
  blender -b --python simulasyon/sahne_olustur.py -- <kod> <fps> <onizleme|nihai>
Sahne gercek olceklidir (1 birim = 1 m): X = rota boyunca yatay mesafe, Z = deniz seviyesinden irtifa.
Arazi ve kule SEMATIKTIR; yalnizca kalkis irtifasi, deniz seviyesi, hedef mesafesi ve hedef kotu veridir.
"""
import csv
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
arg = sys.argv[sys.argv.index("--") + 1:]
KOD, FPS, MOD = arg[0], int(arg[1]), arg[2]
O = json.loads((ROOT / "hesaplamalar" / "ozet.json").read_text(encoding="utf-8"))
SEN = O["rota"]["senaryolar"][0]
PERF = O["tasarimlar"][KOD]["perf"]
with open(ROOT / "simulasyon" / "ucus_verileri.csv", encoding="utf-8") as f:
    VERI = [r for r in csv.DictReader(f) if r["tasarim"] == KOD and float(r["lodos_ms"]) == 0.0]
for r in VERI:
    for k in ("t_s", "yatay_m", "kalan_m", "irtifa_m", "irtifa_kaybi_m", "hava_hizi_ms", "yer_hizi_ms", "suzulme_orani_yer"):
        r[k] = float(r[k])

for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
s = bpy.context.scene
s.render.fps = FPS


def mat(ad, renk, rough=0.8, emis=0.0):
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Roughness"].default_value = rough
    if emis:
        b.inputs["Emission Color"].default_value = (*renk, 1)
        b.inputs["Emission Strength"].default_value = emis
    return m


def mesh(ad, verts, faces, m):
    me = bpy.data.meshes.new(ad)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(ad, me)
    s.collection.objects.link(ob)
    me.materials.append(m)
    return ob


def kama(ad, x0, x1, x2, h, m, yy=600):
    """x0..x1 arasi duz (h), x1..x2 arasi denize inen yamac (ya da tersi)."""
    v = [(x0, -yy, 0), (x0, yy, 0), (x0, -yy, h), (x0, yy, h), (x1, -yy, h), (x1, yy, h), (x2, -yy, 0), (x2, yy, 0)]
    return mesh(ad, v, [(0, 1, 3, 2), (2, 3, 5, 4), (4, 5, 7, 6), (0, 2, 4, 6), (1, 7, 5, 3)], m)


M_SU = mat("deniz", (0.10, 0.28, 0.45), 0.25)
M_KARA = mat("kara_sematik", (0.45, 0.47, 0.38))
M_TAS = mat("kule_sematik", (0.62, 0.58, 0.50))
M_HEDEF = mat("hedef", (0.0, 0.7, 0.3), 0.5, 4.0)
M_IZ = mat("yorunge", (0.9, 0.1, 0.1), 0.5, 3.0)
M_GEREK = mat("gereken_yol", (0.0, 0.7, 0.3), 0.5, 2.0)
M_HUD = mat("hud", (1, 1, 1), 0.5, 2.5)

mesh("deniz", [(-2000, -6000, 0), (6000, -6000, 0), (6000, 6000, 0), (-2000, 6000, 0)], [(0, 1, 2, 3)], M_SU)
kama("galata_sematik", -600, 40, 350, 35.0, M_KARA)   # kiyi konumu OLCULMEDI, sematik
kama("uskudar_sematik", 4600, SEN["mesafe"], 2900, SEN["h1"], M_KARA)
# kule: silindir + kulah (sematik; yaricap varsayim)
import bmesh
for ad, z0, z1, r0, r1 in (("kule_govde", 35.0, 35.0 + 0.82 * (SEN["h0"] - 35.0), 8.0, 8.0),
                           ("kule_kulah", 35.0 + 0.82 * (SEN["h0"] - 35.0), SEN["h0"], 8.5, 0.05)):
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=r0, radius2=r1, depth=z1 - z0)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(ad, me)
    s.collection.objects.link(ob)
    me.materials.append(M_TAS)
    ob.location = (-9.0, 0, (z0 + z1) / 2)          # kule kalkis noktasinin hemen arkasinda


def cizgi(ad, a, b, r, m):
    cu = bpy.data.curves.new(ad, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    sp = cu.splines.new("POLY")
    sp.points.add(1)
    sp.points[0].co = (*a, 1)
    sp.points[1].co = (*b, 1)
    ob = bpy.data.objects.new(ad, cu)
    s.collection.objects.link(ob)
    cu.materials.append(m)
    return ob


son = VERI[-1]
cizgi("yorunge", (0, 0, SEN["h0"]), (son["yatay_m"], 0, 0), 0.03, M_IZ)
cizgi("gereken_yol", (0, 0, SEN["h0"]), (SEN["mesafe"], 0, SEN["h1"]), 0.25, M_GEREK)
cizgi("hedef_diregi", (SEN["mesafe"], 0, SEN["h1"]), (SEN["mesafe"], 0, SEN["h1"] + 60), 1.5, M_HEDEF)

# ---- planor: model.blend'den eklenir ----
blend = ROOT / ("tasarim_v1" if KOD == "v1" else f"tasarim_v2/{KOD}") / "model.blend"
with bpy.data.libraries.load(str(blend)) as (src, dst):
    dst.objects = [n for n in src.objects if not n.startswith(("zemin", "gunes", "kamera", "etiket"))]
planor = bpy.data.objects.new("planor", None)
s.collection.objects.link(planor)
for ob in dst.objects:
    if ob is not None:
        s.collection.objects.link(ob)
        ob.parent = planor
gamma = math.radians(PERF["gamma_deg"])
planor.rotation_euler = (0, -gamma, math.pi)        # model burnu -X; ucus +X; burun asagi gamma

# ---- kamera: planoru izleyen bos nesneye bagli ----
iz = bpy.data.objects.new("izleyici", None)
s.collection.objects.link(iz)
cam = bpy.data.cameras.new("kamera")
cam.lens = 35
cam.clip_end = 20000
co = bpy.data.objects.new("kamera", cam)
s.collection.objects.link(co)
co.parent = iz
kk = O["tasarimlar"][KOD]["geo"]["b"] / 7.0      # kadraj aciklikla olceklenir
co.location = (-10 * kk, -17 * kk, 4.5 * kk)
co.rotation_euler = (Vector((-5.5 * kk, 0, 2.2 * kk)) - Vector(co.location)).to_track_quat("-Z", "Y").to_euler()
s.camera = co

for r in VERI:
    fr = 1 + r["t_s"] * FPS
    for ob in (planor, iz):
        ob.location = (r["yatay_m"], 0, r["irtifa_m"])
        ob.keyframe_insert("location", frame=fr)
s.frame_start, s.frame_end = 1, int(round(1 + son["t_s"] * FPS))


def dogrusal(ob):
    """Tum keyframe'leri dogrusal ara degerlemeye cevirir (surume dayanikli)."""
    ad = ob.animation_data
    act = ad.action if ad else None
    if not act:
        return
    egriler = []
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        egriler = list(act.fcurves)
    else:
        for lay in getattr(act, "layers", []):
            for strip in lay.strips:
                for cb in strip.channelbags:
                    egriler += list(cb.fcurves)
    for fc in egriler:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


dogrusal(planor)
dogrusal(iz)

# ---- isik / gok ----
sun = bpy.data.lights.new("gunes", "SUN")
sun.energy = 3.5
so = bpy.data.objects.new("gunes", sun)
s.collection.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(-35))
w = s.world or bpy.data.worlds.new("World")
s.world = w
w.use_nodes = True
bg = next((n for n in w.node_tree.nodes if n.type == "BACKGROUND"), None)
if bg:
    bg.inputs[0].default_value = (0.45, 0.62, 0.85, 1)
    bg.inputs[1].default_value = 0.6
try:
    s.view_settings.view_transform = "Standard"
except TypeError as e:
    print("view_transform:", e)

# ---- HUD: kameraya bagli metin ----
SATIR = 11
hud = []
panel = mesh("hud_panel", [(-0.52, 0.30, -1.003), (0.12, 0.30, -1.003), (0.12, -0.005, -1.003), (-0.52, -0.005, -1.003)],
             [(0, 1, 2, 3)], mat("hud_panel", (0.02, 0.03, 0.05), 1.0))
panel.parent = co
for i in range(SATIR):
    cu = bpy.data.curves.new(f"hud{i}", "FONT")
    cu.size = 0.019
    cu.body = "-"
    ob = bpy.data.objects.new(f"hud{i}", cu)
    s.collection.objects.link(ob)
    cu.materials.append(M_HUD)
    ob.parent = co
    ob.location = (-0.495, 0.262 - i * 0.025, -1.0)
    hud.append(cu)


def ornekle(t):
    t = max(0.0, min(t, son["t_s"]))
    for a, b in zip(VERI, VERI[1:]):
        if a["t_s"] <= t <= b["t_s"]:
            f = (t - a["t_s"]) / (b["t_s"] - a["t_s"]) if b["t_s"] > a["t_s"] else 0.0
            return {k: a[k] + f * (b[k] - a[k]) for k in ("yatay_m", "kalan_m", "irtifa_m", "irtifa_kaybi_m", "hava_hizi_ms", "yer_hizi_ms", "suzulme_orani_yer")}
    return {k: son[k] for k in ("yatay_m", "kalan_m", "irtifa_m", "irtifa_kaybi_m", "hava_hizi_ms", "yer_hizi_ms", "suzulme_orani_yer")}


def hud_guncelle(scene, *_):
    t = (scene.frame_current - 1) / FPS
    d = ornekle(t)
    durum = "hedef kotunun ustunde" if d["irtifa_m"] >= SEN["h1"] else "HEDEF KOTUNUN ALTINDA - hedefe ulasamaz"
    if t >= son["t_s"] - 1e-6:
        durum = "DENIZ SEVIYESINE INDI - hedefe ulasamadi"
    yaz = [
        f"Tasarim {KOD} | Senaryo N: kule tepesi -> Dogancilar, sakin hava",
        f"Sure                  {t:7.1f} s",
        f"Yatay ilerleme        {d['yatay_m']:7.0f} m",
        f"Hedefe kalan          {d['kalan_m']:7.0f} m   (toplam {SEN['mesafe']:.0f} m)",
        f"Irtifa (deniz sev.)   {d['irtifa_m']:7.1f} m   (hedef kotu {SEN['h1']:.0f} m)",
        f"Irtifa kaybi          {d['irtifa_kaybi_m']:7.1f} m",
        f"Hava hizi             {d['hava_hizi_ms']:7.1f} m/s",
        f"Yer hizi              {d['yer_hizi_ms']:7.1f} m/s",
        f"Suzulme orani         {d['suzulme_orani_yer']:7.2f} : 1   (gereken {SEN['mesafe'] / (SEN['h0'] - SEN['h1']):.0f} : 1)",
        f"Durum: {durum}",
        "Basitlestirilmis nokta-kutle modeli - CFD degildir. Arazi ve kule sematiktir.",
    ]
    for cu, satir in zip(hud, yaz):
        cu.body = satir


bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(hud_guncelle)

# ---- dogrulama: animasyon konumu <-> CSV ----
sapma = 0.0
for r in VERI[:: max(1, len(VERI) // 25)] + [son]:
    fr = 1 + r["t_s"] * FPS
    s.frame_set(int(fr), subframe=fr - int(fr))
    p = planor.matrix_world.translation
    sapma = max(sapma, abs(p.x - r["yatay_m"]), abs(p.z - r["irtifa_m"]))
print(f"DOGRULAMA {KOD}: en buyuk keyframe-CSV sapmasi = {sapma:.4f} m ; kare {s.frame_start}-{s.frame_end} @ {FPS} fps")

bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "simulasyon" / f"sim_{KOD}.blend"))

# ---- render ----
s.render.image_settings.file_format = "PNG"
if MOD == "onizleme":
    s.render.resolution_x, s.render.resolution_y = 960, 540
    kareler = sorted({s.frame_start, (s.frame_start + s.frame_end) // 3, 2 * (s.frame_start + s.frame_end) // 3, s.frame_end})
    hedef = ROOT / "simulasyon" / "onizleme"
else:
    s.render.resolution_x, s.render.resolution_y = 1280, 720
    kareler = range(s.frame_start, s.frame_end + 1)
    hedef = ROOT / "renderlar" / "animasyon" / f"{KOD}_sim"
for fr in kareler:
    cikti = hedef / (f"{KOD}_sim_{fr:04d}.png" if MOD == "onizleme" else f"{fr:04d}.png")
    # nihai dizi uzun; bellek yetersizliğiyle kesilirse kaldığı yerden devam eder
    if MOD == "nihai" and cikti.exists() and cikti.stat().st_size > 0:
        continue
    s.frame_set(fr)
    hud_guncelle(s)
    s.render.filepath = str(cikti)
    bpy.ops.render.render(write_still=True)
print("render tamam:", KOD, MOD, len(list(kareler)))
