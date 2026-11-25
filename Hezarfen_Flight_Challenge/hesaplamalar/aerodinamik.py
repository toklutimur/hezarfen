"""Hezarfen Flight Challenge - tekrar uretilebilir aerodinamik ve yapisal hesap.

Calistirma:  python hesaplamalar/aerodinamik.py
Girdi:       hesaplamalar/parametreler.json
Cikti:       hesaplamalar/sonuclar.csv, hesaplamalar/duyarlilik.csv,
             hesaplamalar/ozet.json (SVG/Blender/rapor icin turetilmis degerler)

Model (yari-statik, dengeli duz suzulme):
    L = 1/2 rho V^2 S CL            D = 1/2 rho V^2 S CD
    CD = CD0 + CL^2 / (pi e AR)     (parabolik polar)
    (L/D)max = 1/2 sqrt(pi e AR / CD0),  CL* = sqrt(CD0 pi e AR)
    V = sqrt(2 W / (rho S CL)),     batis = V / (L/D)   (kucuk aci)
    menzil(sakin hava) = dh * (L/D)
Gecerlilik: sikistirilamaz akis, yapisik akis (CL < CLmax), sabit hiz, kucuk
suzulme acisi yaklasimi yerine tam aci (atan) kullanilir; turbulans, kalkis
gecisi, esneklik ve kumas sizdirmasi modellenmez.
"""
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = json.loads((HERE / "parametreler.json").read_text(encoding="utf-8"))
G = P["sabitler"]["g"]["deger"]
RHO = P["sabitler"]["rho"]["deger"]
MAT = P["malzemeler"]
GEO = P["cografya"]


# ---------- cografya ----------
def haversine(a, b):
    R = 6371008.8
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dp, dl = p2 - p1, math.radians(b["lon"] - a["lon"])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def bearing(a, b):
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dl = math.radians(b["lon"] - a["lon"])
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(y, x)) % 360


def rotalar():
    k = GEO["galata_kulesi"]
    zemin = GEO["kule_zemin_kotu_m"]["deger"]
    tepe = zemin + GEO["kule_mimari_yukseklik_m"]["deger"]
    kat = zemin + GEO["kule_en_ust_kat_m"]["deger"]
    d_dog = haversine(k, GEO["dogancilar_parki"])
    d_isk = haversine(k, GEO["uskudar_iskelesi"])
    dog = GEO["dogancilar_kotu_m"]["deger"]
    kiyi = GEO["kiyi_kotu_m"]["deger"]
    iddia = GEO["ikincil_kaynak_iddiasi"]
    return {
        "yon_dogancilar_derece": bearing(k, GEO["dogancilar_parki"]),
        "senaryolar": [
            {"ad": "N: kulah ucu -> Dogancilar (nominal)", "h0": tepe, "h1": dog, "mesafe": d_dog},
            {"ad": "K: en ust kat -> Dogancilar (kotumser)", "h0": kat, "h1": dog, "mesafe": d_dog},
            {"ad": "S: kulah ucu -> Uskudar kiyisi", "h0": tepe, "h1": kiyi, "mesafe": d_isk},
            {"ad": "I: ikincil kaynak iddiasi (en iyimser)", "h0": iddia["kule_tepe_deniz_seviyesi_m"], "h1": dog, "mesafe": d_dog},
        ],
    }


# ---------- geometri ve kutle ----------
def kanat_geometri(t):
    st = t["kanat"]["istasyonlar"]
    yari = 0.0
    mac_int = 0.0
    xac_int = 0.0
    for a, b in zip(st, st[1:]):
        dy = b["y"] - a["y"]
        c0, c1 = a["veter"], b["veter"]
        yari += 0.5 * (c0 + c1) * dy
        mac_int += dy * (c0 * c0 + c0 * c1 + c1 * c1) / 3.0
        # ceyrek-veter noktasinin alan agirlikli ortalamasi (yaklasik)
        q0, q1 = a["x_hucum"] + 0.25 * c0, b["x_hucum"] + 0.25 * c1
        xac_int += dy * 0.5 * (c0 * q0 + c1 * q1)
    S = 2 * yari
    b_ = 2 * t["kanat"]["yari_aciklik_m"]
    return {"S": S, "b": b_, "AR": b_ * b_ / S, "MAC": 2 * mac_int / S, "x_ac": 2 * xac_int / S}


def frustum_hacim(L, d0, d1):
    return math.pi * L * (d0 * d0 + d0 * d1 + d1 * d1) / 12.0


def kutle_butcesi(t, geo):
    if "yapi_kutlesi_kg" in t:                      # kutle dogrudan verilmis (modern karsilastirma)
        return {"toplam": t["yapi_kutlesi_kg"]["deger"]}
    isk = t["iskelet"]
    yari = t["kanat"]["yari_aciklik_m"]
    rho_k = MAT[isk["kiris_malzeme"]]["yogunluk"]
    kiris = 2 * isk["ana_kiris_adet"] * frustum_hacim(yari, isk["kiris_cap_kok_m"], isk["kiris_cap_uc_m"]) * rho_k
    st = t["kanat"]["istasyonlar"]
    ort_veter = geo["S"] / geo["b"]
    n_nervur = 2 * isk["nervur_adet_yarim_kanat"]
    nervur = n_nervur * ort_veter * math.pi * isk["nervur_cap_m"] ** 2 / 4 * MAT[isk["nervur_malzeme"]]["yogunluk"]
    kb = isk["kuyruk_kirisi"]
    kuyruk_kiris = kb["uzunluk_m"] * math.pi * kb["cap_m"] ** 2 / 4 * MAT[kb["malzeme"]]["yogunluk"]
    dr = isk["direk"]
    direk = (dr["yukseklik_ust_m"] + dr["yukseklik_alt_m"]) * math.pi * dr["cap_m"] ** 2 / 4 * MAT[dr["malzeme"]]["yogunluk"]
    kaplama = (geo["S"] + t["kuyruk"]["alan_m2"]) * MAT["keten_bez"]["alan_yogunlugu"]
    bag = isk["baglanti_ve_kosum_kg"]["deger"]
    kalem = {"ana_kirisler": kiris, "nervurler": nervur, "kuyruk_kirisi": kuyruk_kiris,
             "direk": direk, "kaplama": kaplama, "baglanti_kosum": bag}
    kalem["toplam"] = sum(kalem.values())
    return kalem


# ---------- aerodinamik ----------
def performans(S, AR, m_top, CD0, e, CLmax, rho=RHO):
    W = m_top * G
    k = 1.0 / (math.pi * e * AR)
    LD = 0.5 * math.sqrt(1.0 / (k * CD0))
    CL_opt = math.sqrt(CD0 / k)
    sinirli = CL_opt > 0.9 * CLmax          # en iyi suzulme stall'a cok yakinsa
    CL = min(CL_opt, 0.9 * CLmax)           # %10 CL payi (yaklasik %5 hiz payi)
    CD = CD0 + k * CL * CL
    LD_kul = CL / CD
    gamma = math.atan(1.0 / LD_kul)
    V = math.sqrt(2 * W * math.cos(gamma) / (rho * S * CL))
    Vs = math.sqrt(2 * W / (rho * S * CLmax))
    q = 0.5 * rho * V * V
    return {"W": W, "WS": W / S, "LD_max": LD, "CL_opt": CL_opt, "CL": CL, "CD": CD,
            "LD": LD_kul, "gamma_deg": math.degrees(gamma), "V": V, "V_stall": Vs,
            "batis": V * math.sin(gamma), "V_yatay": V * math.cos(gamma),
            "L": q * S * CL, "D": q * S * CD, "stall_sinirli": sinirli}


def ucus(perf, h0, h1, mesafe, ruzgar, ruzgar_yonu_nereden, rota_yonu):
    """Sabit ruzgarda dengeli suzulme. Ruzgar bilesenleri rota eksenine gore."""
    dh = h0 - h1
    esis = (ruzgar_yonu_nereden + 180.0) % 360.0          # ruzgarin gittigi yon
    aci = math.radians(esis - rota_yonu)
    arka, yan = ruzgar * math.cos(aci), ruzgar * math.sin(aci)
    Vh = perf["V_yatay"]
    if abs(yan) >= Vh:
        yer_hizi, rota_tutulur = arka, False             # yengec acisi yetmez, suruklenir
    else:
        yer_hizi, rota_tutulur = math.sqrt(Vh * Vh - yan * yan) + arka, True
    t = dh / perf["batis"] if dh > 0 else 0.0
    menzil = max(yer_hizi, 0.0) * t
    # hedefe varmak icin gereken ortalama yukselen hava (surekli, tum rota boyunca)
    if yer_hizi > 0:
        t_gerek = mesafe / yer_hizi
        yukselen_gerek = perf["batis"] - dh / t_gerek
    else:
        t_gerek, yukselen_gerek = float("inf"), float("inf")
    return {"dh": dh, "gereken_LD": mesafe / dh if dh > 0 else float("inf"),
            "arka_ruzgar": arka, "yan_ruzgar": yan, "yer_hizi": yer_hizi,
            "rota_tutulur": rota_tutulur, "sure": t, "menzil": menzil,
            "oran": menzil / mesafe, "ulasir": menzil >= mesafe,
            "t_gerek": t_gerek, "gereken_yukselen_hava": max(yukselen_gerek, 0.0)}


# ---------- yapi ----------
def yapi(t, geo, m_top):
    isk = t["iskelet"]
    n = t["yuk_faktoru_tasarim"]["deger"]
    W = m_top * G
    yari = t["kanat"]["yari_aciklik_m"]
    mor = MAT[isk["kiris_malzeme"]]["MOR_MPa"] * 1e6
    Z = math.pi * isk["kiris_cap_kok_m"] ** 3 / 32.0 * isk["ana_kiris_adet"]
    # duzgun yayili yuk varsayimi: yarim kanat yuku W/2, bileske yari/2'de
    M_ankastre = (W / 2) * (yari / 2)
    # gergili: gergi noktasinin disinda kalan konsol parca
    f = isk["gergi_y_orani"]
    L_dis = yari * (1 - f)
    M_gergili = (W / 2) * (1 - f) * (L_dis / 2)
    d_gergi = isk["kiris_cap_kok_m"] + (isk["kiris_cap_uc_m"] - isk["kiris_cap_kok_m"]) * f
    Z_gergi = math.pi * d_gergi ** 3 / 32.0 * isk["ana_kiris_adet"]
    s_a, s_g = M_ankastre / Z, M_gergili / Z_gergi
    return {"n": n, "M_ankastre": M_ankastre, "sigma_ankastre_1g": s_a,
            "GK_ankastre_1g": mor / s_a, "GK_ankastre_n": mor / (n * s_a),
            "M_gergili": M_gergili, "sigma_gergili_1g": s_g,
            "GK_gergili_1g": mor / s_g, "GK_gergili_n": mor / (n * s_g)}


def denge(t, geo, kutle, m_pilot):
    pk = t["pilot_konumu"]
    x_yapi = geo["x_ac"] + 0.20 * geo["MAC"]      # VARSAYIM: yapi agirlik merkezi ~%45 MAC
    m_y = kutle["toplam"]
    x_cg = (m_pilot * pk["x_m"] + m_y * x_yapi) / (m_pilot + m_y)
    z_cg = (m_pilot * pk["z_m"]) / (m_pilot + m_y)
    ku = t["kuyruk"]
    l_t = ku["x_hucum_m"] + 0.25 * ku["veter_m"] - geo["x_ac"]
    eta = 0.5                                      # VARSAYIM: (a_t/a_w)(1-de/da) ~ 0.5
    x_np = geo["x_ac"] + eta * (ku["alan_m2"] / geo["S"]) * l_t
    return {"x_cg": x_cg, "z_cg": z_cg, "x_np": x_np, "x_ac": geo["x_ac"],
            "statik_pay_MAC": (x_np - x_cg) / geo["MAC"], "kuyruk_kolu": l_t}


# ---------- ana akis ----------
def tasarim_hesapla(kod, t):
    geo = kanat_geometri(t)
    kutle = kutle_butcesi(t, geo)
    m_p = P["pilot"]["kutle_kg"]["deger"]
    m_top = m_p + kutle["toplam"]
    a = t["aero"]
    perf = performans(geo["S"], geo["AR"], m_top, a["CD0"]["deger"], a["oswald_e"]["deger"], a["CLmax"]["deger"])
    return {"kod": kod, "geo": geo, "kutle": kutle, "m_pilot": m_p, "m_toplam": m_top,
            "perf": perf, "yapi": yapi(t, geo, m_top) if t.get("yapi_hesabi", True) else None,
            "denge": denge(t, geo, kutle, m_p)}


def duyarlilik(t, taban, h0, h1):
    """Tek-degiskenli tarama: her parametre dusuk/yuksek, digerleri nominal."""
    geo, a = taban["geo"], t["aero"]
    nom = dict(S=geo["S"], AR=geo["AR"], m=taban["m_toplam"], CD0=a["CD0"]["deger"],
               e=a["oswald_e"]["deger"], CLmax=a["CLmax"]["deger"], rho=RHO, dh=h0 - h1)

    def menzil(**kw):
        p = {**nom, **kw}
        return p["dh"] * performans(p["S"], p["AR"], p["m"], p["CD0"], p["e"], p["CLmax"], p["rho"])["LD"]

    m_yapi = taban["kutle"]["toplam"]
    pk = P["pilot"]["kutle_kg"]
    zemin = GEO["kule_zemin_kotu_m"]
    ust = GEO["kule_mimari_yukseklik_m"]["deger"]
    dog = GEO["dogancilar_kotu_m"]
    taramalar = [
        ("CD0 (parazit surukleme)", "CD0", a["CD0"]["dusuk"], a["CD0"]["yuksek"]),
        ("Oswald e", "e", a["oswald_e"]["dusuk"], a["oswald_e"]["yuksek"]),
        ("CLmax", "CLmax", a["CLmax"]["dusuk"], a["CLmax"]["yuksek"]),
        ("pilot kutlesi", "m", pk["dusuk"] + m_yapi, pk["yuksek"] + m_yapi),
        ("yapi kutlesi (-%30/+%50)", "m", nom["m"] - 0.3 * m_yapi, nom["m"] + 0.5 * m_yapi),
        ("hava yogunlugu", "rho", P["sabitler"]["rho"]["dusuk"], P["sabitler"]["rho"]["yuksek"]),
        ("kalkis kotu (zemin 35-54 m)", "dh", zemin["dusuk"] + ust - h1, zemin["yuksek"] + ust - h1),
        ("inis kotu (44-54 m)", "dh", h0 - dog["yuksek"], h0 - dog["dusuk"]),
        ("kalkis noktasi (ust kat / kulah ucu)", "dh", zemin["deger"] + GEO["kule_en_ust_kat_m"]["deger"] - h1, h0 - h1),
    ]
    out = []
    r0 = menzil()
    for ad, key, lo, hi in taramalar:
        rl, rh = menzil(**{key: lo}), menzil(**{key: hi})
        out.append({"parametre": ad, "dusuk": lo, "yuksek": hi, "menzil_dusuk_m": rl,
                    "menzil_yuksek_m": rh, "salinim_m": abs(rh - rl), "nominal_menzil_m": r0})
    out.sort(key=lambda r: -r["salinim_m"])
    return out


def main():
    rota = rotalar()
    yon = rota["yon_dogancilar_derece"]
    lodos = GEO["lodos_yonu_derece"]["deger"]
    satirlar, ozet = [], {"rota": rota, "tasarimlar": {}}
    for kod, t in P["tasarimlar"].items():
        r = tasarim_hesapla(kod, t)
        ozet["tasarimlar"][kod] = r
        for sen in rota["senaryolar"]:
            for w in GEO["ruzgar_hizlari_ms"]["degerler"]:
                u = ucus(r["perf"], sen["h0"], sen["h1"], sen["mesafe"], w, lodos, yon)
                satirlar.append({
                    "tasarim": kod, "senaryo": sen["ad"], "lodos_ms": w,
                    "h0_m": round(sen["h0"], 2), "h1_m": round(sen["h1"], 2), "dh_m": round(u["dh"], 2),
                    "mesafe_m": round(sen["mesafe"], 1), "gereken_LD": round(u["gereken_LD"], 1),
                    "LD": round(r["perf"]["LD"], 2), "V_ms": round(r["perf"]["V"], 2),
                    "V_stall_ms": round(r["perf"]["V_stall"], 2), "batis_ms": round(r["perf"]["batis"], 2),
                    "arka_ruzgar_ms": round(u["arka_ruzgar"], 2), "yan_ruzgar_ms": round(u["yan_ruzgar"], 2),
                    "yer_hizi_ms": round(u["yer_hizi"], 2), "rota_tutulur": u["rota_tutulur"],
                    "sure_s": round(u["sure"], 1), "menzil_m": round(u["menzil"], 1),
                    "menzil_orani": round(u["oran"], 3), "hedefe_ulasir": u["ulasir"],
                    "gereken_yukselen_hava_ms": round(u["gereken_yukselen_hava"], 2),
                })
        n = rota["senaryolar"][0]
        d = duyarlilik(t, r, n["h0"], n["h1"])
        ozet["tasarimlar"][kod]["duyarlilik"] = d
        with open(HERE / f"duyarlilik_{kod}.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(d[0].keys()))
            wr.writeheader()
            for row in d:
                wr.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()})

    with open(HERE / "sonuclar.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(satirlar[0].keys()))
        wr.writeheader()
        wr.writerows(satirlar)
    (HERE / "ozet.json").write_text(json.dumps(ozet, indent=1, ensure_ascii=False), encoding="utf-8")

    # ---- konsol ozeti ----
    print(f"Rota yonu (Galata->Dogancilar): {yon:.1f} derece; lodos {lodos:.0f} dereceden eser")
    for sen in rota["senaryolar"]:
        print(f"  {sen['ad']}: mesafe {sen['mesafe']:.0f} m, dh {sen['h0'] - sen['h1']:.1f} m, gereken L/D {sen['mesafe'] / (sen['h0'] - sen['h1']):.1f}")
    for kod, r in ozet["tasarimlar"].items():
        g, p, k, y, dn = r["geo"], r["perf"], r["kutle"], r["yapi"], r["denge"]
        print(f"\n[{kod}] S={g['S']:.2f} m2  b={g['b']:.2f} m  AR={g['AR']:.2f}  MAC={g['MAC']:.2f} m")
        print("  kutle (kg): " + ", ".join(f"{a}={v:.2f}" for a, v in k.items()) + f" | pilot={r['m_pilot']:.0f} | ucus={r['m_toplam']:.1f}")
        print(f"  W={p['W']:.0f} N  W/S={p['WS']:.1f} N/m2  (L/D)max={p['LD_max']:.2f}  kullanilan L/D={p['LD']:.2f} (CL={p['CL']:.2f}, stall sinirli={p['stall_sinirli']})")
        print(f"  V={p['V']:.2f} m/s  Vstall={p['V_stall']:.2f} m/s  batis={p['batis']:.2f} m/s  aci={p['gamma_deg']:.1f} derece  L={p['L']:.0f} N  D={p['D']:.0f} N")
        if y is None:
            print("  yapi: hesaplanmadi (kutle dogrudan varsayildi)")
        else:
            print(f"  yapi: ankastre 1g sigma={y['sigma_ankastre_1g'] / 1e6:.1f} MPa GK={y['GK_ankastre_1g']:.2f} (n={y['n']:.0f}: {y['GK_ankastre_n']:.2f}) | gergili 1g sigma={y['sigma_gergili_1g'] / 1e6:.1f} MPa GK={y['GK_gergili_1g']:.2f} (n={y['n']:.0f}: {y['GK_gergili_n']:.2f})")
        print(f"  denge: x_cg={dn['x_cg']:.2f} m  x_np={dn['x_np']:.2f} m  statik pay={dn['statik_pay_MAC'] * 100:.0f}% MAC  z_cg={dn['z_cg']:.2f} m")
        for s in [s for s in satirlar if s["tasarim"] == kod]:
            print(f"  {s['senaryo'][:1]} lodos {s['lodos_ms']:>4.0f} m/s: menzil {s['menzil_m']:>7.0f} m / {s['mesafe_m']:.0f} m ({s['menzil_orani'] * 100:4.1f}%)  sure {s['sure_s']:.0f} s  gereken yukselen hava {s['gereken_yukselen_hava_ms']:.2f} m/s")
        print("  duyarlilik (nominal senaryo, sakin hava menzili):")
        for row in r["duyarlilik"]:
            print(f"    {row['parametre']:<38} {row['menzil_dusuk_m']:7.0f} .. {row['menzil_yuksek_m']:7.0f} m  (salinim {row['salinim_m']:.0f} m)")


if __name__ == "__main__":
    main()
