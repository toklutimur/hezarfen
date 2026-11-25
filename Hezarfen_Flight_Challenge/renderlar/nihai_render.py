"""Nihai gorseller: 3 aci Cycles + 360 derece turntable (EEVEE).

Calistirma:  blender -b <model.blend> --python renderlar/nihai_render.py -- v1
Model dosyasi DEGISTIRILMEZ (kaydedilmez).
"""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
KOD = sys.argv[sys.argv.index("--") + 1]
P = json.loads((ROOT / "hesaplamalar" / "parametreler.json").read_text(encoding="utf-8"))
YARI = P["tasarimlar"][KOD]["kanat"]["yari_aciklik_m"]
k = YARI / 3.5
s = bpy.context.scene
cam = s.camera
hedef = Vector((1.25, 0.0, -0.15)) * k


def bak(konum):
    cam.location = konum
    cam.rotation_euler = (hedef - cam.location).to_track_quat("-Z", "Y").to_euler()


s.render.image_settings.file_format = "PNG"
s.render.resolution_x, s.render.resolution_y, s.render.resolution_percentage = 1920, 1080, 100

# ---------- Cycles: 3 aci ----------
try:
    s.render.engine = "CYCLES"
except TypeError as e:
    print("motor hatasi:", e)
s.cycles.samples = 96
s.cycles.use_denoising = True
try:
    pr = bpy.context.preferences.addons["cycles"].preferences
    for tip in ("OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            pr.compute_device_type = tip
            pr.get_devices()
            if any(d.type == tip for d in pr.devices):
                for d in pr.devices:
                    d.use = True
                s.cycles.device = "GPU"
                print("GPU:", tip)
                break
        except Exception:
            continue
except Exception as e:
    print("GPU ayarlanamadi, CPU:", e)

ACILAR = {
    "1_alt_on_ceyrek": Vector((-4.6, -5.6, -1.25)) * k,
    "2_ust_arka_ceyrek": Vector((7.6, -6.2, 4.6)) * k,
    "3_yan": Vector((1.3, -9.5, 0.3)) * k,
}
for ad, konum in ACILAR.items():
    bak(konum)
    s.render.filepath = str(ROOT / "renderlar" / "nihai" / f"{KOD}_{ad}.png")
    bpy.ops.render.render(write_still=True)
    print("render:", s.render.filepath)

# ---------- turntable: EEVEE, 72 kare ----------
s.render.engine = "BLENDER_EEVEE"
s.render.resolution_x, s.render.resolution_y = 1280, 720
N = 72
R, Z = 9.0 * k, 2.2 * k
for i in range(N):
    a = 2 * math.pi * i / N
    bak(Vector((hedef.x + R * math.cos(a), R * math.sin(a), Z)))
    s.render.filepath = str(ROOT / "renderlar" / "animasyon" / f"{KOD}_turntable" / f"{i:04d}.png")
    bpy.ops.render.render(write_still=True)
print("turntable tamam:", KOD)
