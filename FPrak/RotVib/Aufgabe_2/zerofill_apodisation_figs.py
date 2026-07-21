import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "/Users/fynnlucca/Documents/Grundpraktikum-1/FPrak/RotVib/Aufgabe_2/"
FIGDIR = "/Users/fynnlucca/Documents/Grundpraktikum-1/FPrak/RotVib/Protokoll/figures/"

def lese_asc(pfad):
    x, y = [], []
    with open(pfad, "r", encoding="latin-1") as f:
        daten = False
        for zeile in f:
            z = zeile.strip()
            if z == "#DATA":
                daten = True; continue
            if daten and z:
                t = z.split()
                if len(t) == 2:
                    try:
                        x.append(float(t[0])); y.append(float(t[1]))
                    except ValueError:
                        pass
    x, y = np.array(x), np.array(y)
    idx = np.argsort(x)
    return x[idx], y[idx]

ds = 6.36e-5  # cm, Schrittweite aus CO2-Kalibrierung (Protokoll Aufgabe 1.2)

# ================= Zerofilling (±1000-Messung) ============================
x, y = lese_asc(BASE + "Interferogramm_2_1000.asc")
y = y - y.mean()
n = len(y)

lo, hi = 1580, 1620
fig, ax = plt.subplots(figsize=(9, 5))
norm = None
for fac, stil in [(1, dict(color="C0", marker="o", ms=5, lw=1.2, zorder=5)),
                  (2, dict(color="C1", marker=".", ms=4, lw=0.9)),
                  (4, dict(color="C2", marker=".", ms=4, lw=0.9)),
                  (8, dict(color="C3", marker=".", ms=4, lw=0.9))]:
    ypad = np.concatenate([y, np.zeros(n * (fac - 1))])
    Y = np.abs(np.fft.rfft(ypad))
    wn = np.fft.rfftfreq(len(ypad), d=ds)
    m = (wn >= lo) & (wn <= hi)
    if norm is None:  # gemeinsame Normierung fuer alle Kurven
        norm = Y[m].max()
    ax.plot(wn[m], Y[m] / norm, label=f"Zerofill $\\times${fac}", **stil)
ax.set_xlabel("Wellenzahl (cm$^{-1}$)")
ax.set_ylabel("norm. Amplitude")
ax.set_title("Einfluss des Zerofilling ($\\pm$1000-Messung)")
ax.legend(loc="lower left")
ax.grid(True, linewidth=0.3, alpha=0.5)
fig.savefig(FIGDIR + "a2_zerofill.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# Kontrolle: Werte an Originalbins identisch?
Y1 = np.abs(np.fft.rfft(y))
Y8 = np.abs(np.fft.rfft(np.concatenate([y, np.zeros(7 * n)])))
print("Zerofill-Check (x8 an Originalbins vs x1), max. rel. Abw.:",
      np.max(np.abs(Y8[::8][:len(Y1)] - Y1) / Y1.max()))

# ================= Apodisation (±8000-Messung) ============================
x8, y8 = lese_asc(BASE + "Interferogramm_2_8000.asc")
y8 = y8 - y8.mean()
n8 = len(y8)
ZF = 4  # Zerofilling x4 fuer glatte Kurven, wie im bisherigen Protokoll

fenster = [
    ("Rechteck", np.ones(n8), "C0"),
    ("Dreieck", 1 - np.abs(np.arange(n8) - (n8 - 1) / 2) / ((n8 - 1) / 2), "C1"),
    ("Blackman", np.blackman(n8), "C2"),
]

lo, hi = 1776, 1793  # isolierte Wasserdampflinie bei 1784,5 cm^-1
fig, ax = plt.subplots(figsize=(9, 5))
for name, w, c in fenster:
    ypad = np.concatenate([y8 * w, np.zeros((ZF - 1) * n8)])
    Y = np.abs(np.fft.rfft(ypad))
    wn = np.fft.rfftfreq(len(ypad), d=ds)
    # Normierung auf Fenstergewinn (Summe der Fensterfunktion): gleiche
    # Kontinuumshoehe, Intensitaetsverlust der Linie bleibt sichtbar
    kont = (wn > 1770) & (wn < 1800)
    Yn = Y / np.median(Y[kont & (np.abs(wn - 1784.5) > 5)])
    m = (wn >= lo) & (wn <= hi)
    ax.plot(wn[m], Yn[m], color=c, lw=1.1, label=name)
ax.set_xlabel("Wellenzahl (cm$^{-1}$)")
ax.set_ylabel("Amplitude (auf Kontinuum normiert)")
ax.set_title("Einfluss der Apodisation ($\\pm$8000, Wasserdampflinie bei 1784,5 cm$^{-1}$)")
ax.legend(loc="lower left")
ax.grid(True, linewidth=0.3, alpha=0.5)
fig.savefig(FIGDIR + "a2_apodisation.png", dpi=130, bbox_inches="tight")
plt.close(fig)
print("Figuren geschrieben.")
