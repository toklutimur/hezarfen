"""Basitlestirilmis suzulme simulasyonu (nokta-kutle, dengeli suzulme). CFD DEGILDIR.

aerodinamik.py'nin urettigi ozet.json'daki performans degerlerini zaman serisine cevirir:
    simulasyon/ucus_verileri.csv   (Blender animasyonu ve HUD bu dosyayi okur)
    simulasyon/ucus_profili.svg    (irtifa-mesafe profili; gereken dogru ile karsilastirma)
Ucus, hedef kotunun altina indikten sonra deniz seviyesine kadar surdurulur (arac hedefe varamazsa suya iner).
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "hesaplamalar"))
import aerodinamik as A  # noqa: E402

O = json.loads((ROOT / "hesaplamalar" / "ozet.json").read_text(encoding="utf-8"))
ROTA = O["rota"]
YON = ROTA["yon_dogancilar_derece"]
LODOS = A.GEO["lodos_yonu_derece"]["deger"]
SEN = ROTA["senaryolar"][0]                     # N: nominal
DT = 0.5
RUZGARLAR = [0.0, 8.0]

satirlar, ozetler = [], []
for kod, r in O["tasarimlar"].items():
    p = r["perf"]
    for w in RUZGARLAR:
        u = A.ucus(p, SEN["h0"], SEN["h1"], SEN["mesafe"], w, LODOS, YON)
        vg, batis = u["yer_hizi"], p["batis"]
        t_son = SEN["h0"] / batis               # deniz seviyesine inis
        n = int(t_son / DT) + 1
        zamanlar = [i * DT for i in range(n)] + [t_son]
        for t in zamanlar:
            x, z = vg * t, SEN["h0"] - batis * t
            satirlar.append({
                "tasarim": kod, "senaryo": "N", "lodos_ms": w, "t_s": round(t, 3),
                "yatay_m": round(x, 2), "kalan_m": round(SEN["mesafe"] - x, 2),
                "irtifa_m": round(max(z, 0.0), 2), "irtifa_kaybi_m": round(SEN["h0"] - max(z, 0.0), 2),
                "hava_hizi_ms": round(p["V"], 2), "yer_hizi_ms": round(vg, 2),
                "suzulme_orani_yer": round(vg / batis, 2),
                "hedef_kotu_ustunde": z >= SEN["h1"],
            })
        ozetler.append({"kod": kod, "w": w, "vg": vg, "batis": batis, "t_son": t_son,
                        "x_hedef_kotu": vg * u["sure"], "x_deniz": vg * t_son})

with open(HERE / "ucus_verileri.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(satirlar[0].keys()))
    wr.writeheader()
    wr.writerows(satirlar)

# ---------------- profil cizimi ----------------
W, H, L, T_, R_, B = 1600, 760, 90, 90, 40, 90
XMAX, ZMAX = 3600.0, 110.0
sx, sz = (W - L - R_) / XMAX, (H - T_ - B) / ZMAX


def X(x):
    return L + x * sx


def Z(z):
    return H - B - z * sz


RENK = {"v1": "#b00020", "v2a": "#c77700", "v2b": "#1d4e89"}
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#22201c;font-size:13px}.h{font-size:22px;font-weight:bold}.k{font-size:11.5px;fill:#555}</style>',
     f'<rect width="{W}" height="{H}" fill="#fbf7ee"/>',
     '<text x="40" y="38" class="h">Galata Kulesi → Doğancılar: süzülme profili (nominal senaryo, sakin hava)</text>',
     '<text x="40" y="58" class="k">Basitleştirilmiş nokta-kütle modeli; CFD değildir. Düşey eksen yataya göre yaklaşık 5 kat abartılıdır. Arazi kesiti ve kıyı konumu şematiktir (yalnızca kule zemini, deniz ve iniş kotu veridir).</text>']
# deniz ve sematik arazi
s.append(f'<rect x="{X(0):.0f}" y="{Z(0):.0f}" width="{XMAX * sx:.0f}" height="14" fill="#9ec5e6"/>')
s.append(f'<polygon points="{X(0):.0f},{Z(0):.0f} {X(0):.0f},{Z(35):.0f} {X(40):.0f},{Z(35):.0f} {X(350):.0f},{Z(0):.0f}" fill="#cdbf9f"/>')
s.append(f'<polygon points="{X(2900):.0f},{Z(0):.0f} {X(3360):.0f},{Z(SEN["h1"]):.0f} {X(XMAX):.0f},{Z(SEN["h1"]):.0f} {X(XMAX):.0f},{Z(0):.0f}" fill="#cdbf9f"/>')
s.append(f'<rect x="{X(0) - 5:.0f}" y="{Z(SEN["h0"]):.0f}" width="10" height="{(SEN["h0"] - 35) * sz:.0f}" fill="#7d705c"/>')
s.append(f'<text x="{X(0) + 10:.0f}" y="{Z(SEN["h0"]) - 6:.0f}">kalkış {SEN["h0"]:.1f} m</text>')
s.append(f'<circle cx="{X(SEN["mesafe"]):.0f}" cy="{Z(SEN["h1"]):.0f}" r="6" fill="#0b6e4f"/>')
s.append(f'<text x="{X(SEN["mesafe"]) - 10:.0f}" y="{Z(SEN["h1"]) - 12:.0f}" text-anchor="end" dy="-14">hedef: Doğancılar {SEN["h1"]:.0f} m, {SEN["mesafe"]:.0f} m</text>')
# eksenler
for x in range(0, 3601, 500):
    s.append(f'<line x1="{X(x):.0f}" y1="{Z(0) + 14:.0f}" x2="{X(x):.0f}" y2="{Z(0) + 20:.0f}" stroke="#333"/><text x="{X(x):.0f}" y="{Z(0) + 36:.0f}" text-anchor="middle">{x}</text>')
for z in range(0, 101, 20):
    s.append(f'<line x1="{L - 6}" y1="{Z(z):.0f}" x2="{L}" y2="{Z(z):.0f}" stroke="#333"/><text x="{L - 10}" y="{Z(z) + 4:.0f}" text-anchor="end">{z}</text>')
s.append(f'<text x="{(L + W - R_) / 2:.0f}" y="{H - 24}" text-anchor="middle">rota boyunca yatay mesafe (m)</text>')
s.append(f'<text x="24" y="{(T_ + H - B) / 2:.0f}" text-anchor="middle" transform="rotate(-90 24 {(T_ + H - B) / 2:.0f})">deniz seviyesinden irtifa (m)</text>')
# gereken dogru
s.append(f'<line x1="{X(0):.0f}" y1="{Z(SEN["h0"]):.0f}" x2="{X(SEN["mesafe"]):.0f}" y2="{Z(SEN["h1"]):.0f}" stroke="#0b6e4f" stroke-width="2" stroke-dasharray="10 6"/>')
s.append(f'<text x="{X(1700):.0f}" y="{Z(76):.0f}" fill="#0b6e4f">gereken yol: süzülme oranı {SEN["mesafe"] / (SEN["h0"] - SEN["h1"]):.0f}:1</text>')
for i, o in enumerate([o for o in ozetler if o["w"] == 0.0]):
    c = RENK.get(o["kod"], "#333")
    s.append(f'<line x1="{X(0):.0f}" y1="{Z(SEN["h0"]):.0f}" x2="{X(o["x_deniz"]):.0f}" y2="{Z(0):.0f}" stroke="{c}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{X(o["x_deniz"]):.0f}" cy="{Z(0):.0f}" r="5" fill="{c}"/>')
    ld = O["tasarimlar"][o["kod"]]["perf"]["LD"]
    s.append(f'<text x="{X(1500):.0f}" y="{Z(34) + i * 22:.0f}" fill="{c}">{o["kod"]}: L/D {ld:.1f} → hedef kotunda {o["x_hedef_kotu"]:.0f} m, denize iniş {o["x_deniz"]:.0f} m ({o["t_son"]:.0f} s)</text>')
s.append("</svg>")
(HERE / "ucus_profili.svg").write_text("\n".join(s), encoding="utf-8")

print(f"{len(satirlar)} satir -> ucus_verileri.csv")
for o in ozetler:
    print(f"  {o['kod']} lodos {o['w']:.0f} m/s: yer hizi {o['vg']:.2f} m/s, batis {o['batis']:.2f} m/s, hedef kotunda {o['x_hedef_kotu']:.0f} m, denizde {o['x_deniz']:.0f} m, sure {o['t_son']:.0f} s")
