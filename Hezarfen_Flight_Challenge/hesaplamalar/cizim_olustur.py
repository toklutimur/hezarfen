"""parametreler.json + ozet.json -> teknik cizim (SVG). Ust, on ve yan gorunus.

Calistirma:  python hesaplamalar/cizim_olustur.py v1 tasarim_v1/kanat_cizimi.svg
(once aerodinamik.py calistirilmis olmali)
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
kod = sys.argv[1] if len(sys.argv) > 1 else "v1"
hedef = ROOT / (sys.argv[2] if len(sys.argv) > 2 else f"tasarim_{kod}/kanat_cizimi.svg")
P = json.loads((HERE / "parametreler.json").read_text(encoding="utf-8"))
O = json.loads((HERE / "ozet.json").read_text(encoding="utf-8"))
T, R = P["tasarimlar"][kod], O["tasarimlar"][kod]
K, KU, ISK, PK = T["kanat"], T["kuyruk"], T["iskelet"], T["pilot_konumu"]
ST = K["istasyonlar"]
YARI = K["yari_aciklik_m"]
DIH = math.radians(K["dihedral_derece"])
S = 90.0 if YARI <= 3.6 else 70.0  # px / m
ET = {"kiris": "ana kirişler (dişbudak)", "nervur": "nervürler (söğüt)", "kaplama": "kumaş kaplama (mumlu keten)",
      "gergi": "gergi halatları (kendir)", **T.get("etiketler", {})}
YATAY = PK.get("yatay", False)
W, H = 1600, 1120
out = []


def add(s):
    out.append(s)


def line(x1, y1, x2, y2, cls="g"):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}"/>')


def poly(pts, cls="kanat"):
    add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" class="{cls}"/>')


def pline(pts, cls="g"):
    add(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" class="{cls}"/>')


def text(x, y, s, cls="t", anchor="start", rot=None):
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{r}>{s}</text>')


def olcu_yatay(x1, x2, y, etiket, ust=True):
    line(x1, y, x2, y, "olcu")
    for x in (x1, x2):
        line(x, y - 6, x, y + 6, "olcu")
    text((x1 + x2) / 2, y - 7 if ust else y + 17, etiket, "to", "middle")


def olcu_dikey(x, y1, y2, etiket):
    line(x, y1, x, y2, "olcu")
    for y in (y1, y2):
        line(x - 6, y, x + 6, y, "olcu")
    text(x - 8, (y1 + y2) / 2, etiket, "to", "middle", -90)


def isaret(x, y, ad, renk):
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="none" stroke="{renk}" stroke-width="2"/>')
    line(x - 10, y, x + 10, y, "ince")
    line(x, y - 10, x, y + 10, "ince")
    text(x + 11, y - 9, ad, "tk")


def interp(y, key):
    y = abs(y)
    for a, b in zip(ST, ST[1:]):
        if a["y"] <= y <= b["y"]:
            f = (y - a["y"]) / (b["y"] - a["y"])
            return a[key] + f * (b[key] - a[key])
    return ST[-1][key]


geo, den, per, kut = R["geo"], R["denge"], R["perf"], R["kutle"]

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add("""<style>
 .bg{fill:#fbf7ee}.kanat{fill:#e9dcc0;stroke:#3a2f22;stroke-width:1.6}.kuyruk{fill:#e3d3b2;stroke:#3a2f22;stroke-width:1.4}
 .kiris{stroke:#7a4a1e;stroke-width:4;fill:none;stroke-linecap:round}.nervur{stroke:#a9743a;stroke-width:1.5;fill:none}
 .gergi{stroke:#555;stroke-width:1;stroke-dasharray:6 4;fill:none}.g{stroke:#3a2f22;stroke-width:1.5;fill:none}
 .ince{stroke:#3a2f22;stroke-width:1}.olcu{stroke:#1d4e89;stroke-width:1}.pilot{fill:#c9c2b8;stroke:#3a2f22;stroke-width:1.4}
 .eksen{stroke:#999;stroke-width:1;stroke-dasharray:14 4 2 4}
 text{font-family:Arial,Helvetica,sans-serif;fill:#22201c}.t{font-size:13px}.to{font-size:13px;fill:#1d4e89}
 .tk{font-size:12px;font-weight:bold}.b{font-size:17px;font-weight:bold}.h{font-size:24px;font-weight:bold}.k{font-size:11.5px;fill:#555}
 .kutu{fill:#fff;stroke:#3a2f22;stroke-width:1}
</style>""")
add(f'<rect class="bg" width="{W}" height="{H}"/>')
text(40, 44, f"Hezarfen Ahmed Çelebi – kanat rekonstrüksiyonu {kod.upper()} (mühendislik varsayımı)", "h")
text(40, 66, T.get("alt_baslik", "Tarihsel kaynaklarda kanat ölçüsü veya çizimi YOKTUR. Bu geometri 'kartal kanatları' ifadesinden ve belgelenmiş ilk planörlerden türetilmiş bir varsayımdır. Ölçüler metre."), "k")

# ---------------- UST GORUNUS ----------------
cx, cy = 520.0, 130.0   # govde ekseni / kok hucum kenari


def U(x, y):            # govde ekseni: x geri (ekranda asagi), y aciklik (ekranda saga)
    return cx + y * S, cy + x * S


text(40, 104, "ÜST GÖRÜNÜŞ", "b")
for isa in (1, -1):
    le = [U(s["x_hucum"], isa * s["y"]) for s in ST]
    te = [U(s["x_hucum"] + s["veter"], isa * s["y"]) for s in reversed(ST)]
    poly(le + te, "kanat")
    n = ISK["nervur_adet_yarim_kanat"]
    for i in range(n):
        y = isa * YARI * (i + 0.5) / n
        x0, c = interp(y, "x_hucum"), interp(y, "veter")
        line(*U(x0, y), *U(x0 + c, y), "nervur")
    for oran in ISK["kiris_x_veter_orani"]:
        pts = [U(s["x_hucum"] + oran * s["veter"], isa * s["y"]) for s in ST if s["veter"] * (1 - oran) > 0.05]
        pline(pts, "kiris")
# kuyruk kirisi ve kuyruk
kb = ISK["kuyruk_kirisi"]
x_kb0 = KU["x_hucum_m"] + KU["veter_m"] - kb["uzunluk_m"]
line(*U(x_kb0, 0), *U(KU["x_hucum_m"] + KU["veter_m"], 0), "kiris")
kx, kc, kb2 = KU["x_hucum_m"], KU["veter_m"], KU["aciklik_m"] / 2
poly([U(kx, 0), U(kx + kc, -kb2), U(kx + kc * 0.85, 0), U(kx + kc, kb2)], "kuyruk")
# pilot boslugu
px, py = U(PK["x_m"], 0)
add(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{0.27 * S:.1f}" ry="{0.20 * S:.1f}" class="pilot"/>')
text(px, py + 4, "pilot", "k", "middle")
line(cx, cy - 30, cx, cy + (kx + kc) * S + 25, "eksen")
isaret(*U(den["x_cg"], 0), "AM", "#b00020")
isaret(*U(den["x_np"], 0.42), "NN", "#0b6e4f")
olcu_yatay(cx - YARI * S, cx + YARI * S, cy - 28, f"kanat açıklığı b = {geo['b']:.2f}")
olcu_dikey(cx - YARI * S - 30, cy, cy + ST[0]["veter"] * S, f"kök veteri {ST[0]['veter']:.2f}")
olcu_dikey(cx + YARI * S + 46, cy, cy + (kx + kc) * S, f"boy {kx + kc:.2f}")
olcu_yatay(cx - kb2 * S, cx + kb2 * S, cy + (kx + kc) * S + 22, f"kuyruk {KU['aciklik_m']:.2f}", False)
yt = cy + (max(s["x_hucum"] + s["veter"] for s in ST) + 0.35) * S
text(cx + 1.2 * S, yt + 0.2 * S, ET["kaplama"], "k")
text(cx - 3.3 * S, yt, f"{ET['kiris']} ×2 / yarım kanat", "k")
text(cx - 3.3 * S, yt + 0.2 * S, f"{ET['nervur']} ×{ISK['nervur_adet_yarim_kanat']} / yarım kanat", "k")

# ---------------- BILGI KUTUSU ----------------
bx, by = 1000, 96
add(f'<rect class="kutu" x="{bx}" y="{by}" width="560" height="420"/>')
text(bx + 14, by + 26, "Türetilmiş değerler (aerodinamik.py çıktısı)", "b")
rows = [
    ("Kanat alanı S", f"{geo['S']:.2f} m²", "HESAP"),
    ("Açıklık oranı AR = b²/S", f"{geo['AR']:.2f}", "HESAP"),
    ("Ortalama aerodinamik veter", f"{geo['MAC']:.2f} m", "HESAP"),
    ("Kambur oranı", f"{K['kambur_orani']:.2f}", "VARSAYIM"),
    ("Dihedral", f"{K['dihedral_derece']:.0f}°", "VARSAYIM"),
    ("Yapı kütlesi", f"{kut['toplam']:.1f} kg", "VARSAYIM" if "yapi_kutlesi_kg" in T else "HESAP"),
    ("Pilot kütlesi", f"{R['m_pilot']:.0f} kg", "VARSAYIM"),
    ("Uçuş kütlesi", f"{R['m_toplam']:.1f} kg", "HESAP"),
    ("Kanat yüklemesi W/S", f"{per['WS']:.1f} N/m²", "HESAP"),
    ("CD0 / Oswald e / CLmax", f"{T['aero']['CD0']['deger']:g} /{T['aero']['oswald_e']['deger']:.2f} / {T['aero']['CLmax']['deger']:.1f}", "VARSAYIM"),
    ("Süzülme oranı L/D", f"{per['LD']:.2f}", "HESAP"),
    ("Süzülme hızı / stall hızı", f"{per['V']:.1f} / {per['V_stall']:.1f} m/s", "HESAP"),
    ("Batış hızı", f"{per['batis']:.2f} m/s", "HESAP"),
    ("Ağırlık merkezi x (AM)", f"{den['x_cg']:.2f} m", "HESAP"),
    ("Nötr nokta x (NN)", f"{den['x_np']:.2f} m", "HESAP"),
    ("Statik kararlılık payı", f"{den['statik_pay_MAC'] * 100:.0f} % MAC", "HESAP"),
]
for i, (a, b, c) in enumerate(rows):
    yy = by + 54 + i * 22
    text(bx + 14, yy, a)
    text(bx + 330, yy, b, "tk")
    text(bx + 470, yy, c, "k")
text(bx + 14, by + 408, "x: kök hücum kenarından geriye, z: kanat düzleminden yukarı.", "k")

# ---------------- ON GORUNUS ----------------
fx, fy = 400.0, 760.0
text(40, 580, "ÖN GÖRÜNÜŞ", "b")


def F(y, z):
    return fx + y * S, fy - z * S


uc_z = YARI * math.tan(DIH)
dr = ISK["direk"]
for isa in (1, -1):
    pline([F(0, 0), F(isa * YARI, uc_z)], "kiris")
    gy = isa * YARI * ISK["gergi_y_orani"]
    gz = abs(gy) * math.tan(DIH)
    line(*F(0, dr["yukseklik_ust_m"]), *F(gy, gz), "gergi")
    line(*F(0, -dr["yukseklik_alt_m"]), *F(gy, gz), "gergi")
line(*F(0, -dr["yukseklik_alt_m"]), *F(0, dr["yukseklik_ust_m"]), "kiris")
# pilot
if YATAY:
    hx, hy = F(0, PK["z_m"])
    add(f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{0.22 * S:.1f}" ry="{0.16 * S:.1f}" class="pilot"/>')
    add(f'<circle cx="{hx:.1f}" cy="{hy - 0.05 * S:.1f}" r="{0.11 * S:.1f}" class="pilot"/>')
else:
    hx, hy = F(0, PK["z_m"] + 0.75)
    add(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{0.11 * S:.1f}" class="pilot"/>')
    add(f'<rect x="{fx - 0.2 * S:.1f}" y="{fy - (PK["z_m"] + 0.62) * S:.1f}" width="{0.4 * S:.1f}" height="{0.62 * S:.1f}" rx="10" class="pilot"/>')
    add(f'<rect x="{fx - 0.15 * S:.1f}" y="{fy - PK["z_m"] * S:.1f}" width="{0.3 * S:.1f}" height="{0.85 * S:.1f}" rx="8" class="pilot"/>')
isaret(*F(0, den["z_cg"]), "AM", "#b00020")
olcu_yatay(fx - YARI * S, fx + YARI * S, fy - dr["yukseklik_ust_m"] * S - 34, f"b = {geo['b']:.2f}")
olcu_dikey(fx + YARI * S + 30, fy - uc_z * S, fy, f"{uc_z:.2f}")
text(fx + YARI * S * 0.55, fy - 0.75 * S, ET["gergi"], "k")
text(fx + 0.1 * S, fy - dr["yukseklik_ust_m"] * S + 16, "direk", "k")
text(fx - YARI * S, fy + 0.5 * S, f"dihedral {K['dihedral_derece']:.0f}°", "k")

# ---------------- YAN GORUNUS ----------------
sx, sy = 960.0, 760.0
text(900, 580, "YAN GÖRÜNÜŞ (kök kesiti)", "b")


def Y(x, z):
    return sx + x * S, sy - z * S


c0 = ST[0]["veter"]
kam = K["kambur_orani"]
profil = [Y(c0 * i / 30, 4 * kam * c0 * (i / 30) * (1 - i / 30)) for i in range(31)]
pline(profil, "kiris")
line(*Y(x_kb0, 0.02), *Y(kx + kc, KU["z_m"]), "kiris")
pline([Y(kx, KU["z_m"]), Y(kx + kc, KU["z_m"] + 0.03)], "g")
line(*Y(PK["x_m"] + 0.15, -dr["yukseklik_alt_m"]), *Y(PK["x_m"] + 0.15, dr["yukseklik_ust_m"]), "kiris")
line(*Y(PK["x_m"] + 0.15, dr["yukseklik_ust_m"]), *Y(kx + kc * 0.5, KU["z_m"]), "gergi")
ppx = PK["x_m"]
if YATAY:
    hx, hy = Y(ppx - 0.55, PK["z_m"] + 0.05)
    add(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{0.11 * S:.1f}" class="pilot"/>')
    add(f'<rect x="{sx + (ppx - 0.40) * S:.1f}" y="{sy - (PK["z_m"] + 0.14) * S:.1f}" width="{1.6 * S:.1f}" height="{0.28 * S:.1f}" rx="10" class="pilot"/>')
else:
    hx, hy = Y(ppx, PK["z_m"] + 0.75)
    add(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{0.11 * S:.1f}" class="pilot"/>')
    add(f'<rect x="{sx + (ppx - 0.13) * S:.1f}" y="{sy - (PK["z_m"] + 0.62) * S:.1f}" width="{0.26 * S:.1f}" height="{0.62 * S:.1f}" rx="10" class="pilot"/>')
    add(f'<rect x="{sx + (ppx - 0.10) * S:.1f}" y="{sy - PK["z_m"] * S:.1f}" width="{0.2 * S:.1f}" height="{0.85 * S:.1f}" rx="8" class="pilot"/>')
isaret(*Y(den["x_cg"], den["z_cg"]), "AM", "#b00020")
isaret(*Y(den["x_np"], 0.30), "NN", "#0b6e4f")
olcu_yatay(sx, sx + c0 * S, sy - dr["yukseklik_ust_m"] * S - 34, f"kök veteri {c0:.2f}")
olcu_yatay(sx, sx + (kx + kc) * S, sy + 1.62 * S, f"toplam boy {kx + kc:.2f}", False)
text(sx + 2.3 * S, sy + 0.25 * S, "kuyruk kirişi", "k")
text(sx + (kx + 0.1) * S, sy + 0.45 * S, f"yatay kuyruk {KU['alan_m2']:.2f} m²", "k")
text(sx - 0.55 * S, sy + 0.3 * S, "uçuş yönü ←", "k")
text(40, H - 24, "AM: ağırlık merkezi · NN: nötr nokta (kaba tahmin) · Kaynak: hesaplamalar/parametreler.json → aerodinamik.py → cizim_olustur.py · Ölçek ≈ " + f"{S:.0f} px/m", "k")
add("</svg>")
hedef.parent.mkdir(parents=True, exist_ok=True)
hedef.write_text("\n".join(out), encoding="utf-8")
print(f"yazildi: {hedef}  ({hedef.stat().st_size} bayt)")
