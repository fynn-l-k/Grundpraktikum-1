#!/usr/bin/env python3
"""
EPR protocol analysis.

Part A -- Magnet calibration (B0 vs coil current) from the video data.
Part B -- Dispersion curves + g-factor for the digitised samples.

Run from the EPR_Protokoll directory with the project venv:
    ../../.venv/bin/python3 analysis.py
(or any python with numpy + matplotlib)

CSV layout expected for the digitised dispersion curves (Part B):
    put them into  figures/csv/<name>.csv
    two columns, header optional:  x , frequency
where x is EITHER the magnetic field B0 in mT (preferred) OR, if you
digitised against the coil current, set X_IS_CURRENT = True below and the
script converts via the calibration. 'frequency' is the HDSDR output
frequency (any unit; only the position of the dispersion centre matters).
The resonance field is taken at the centre (zero-crossing / inflection) of
the S-shaped dispersion curve -- here estimated as the field of the steepest
slope. Adjust by hand in the printed table if needed.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CALFILE = os.path.join(ROOT, "Magnet_kalibration_vom_Video")
FIGDIR = os.path.join(HERE, "figures")
CSVDIR = os.path.join(FIGDIR, "csv")

# physical constants
H = 6.62607015e-34       # J s
MU_B = 9.2740100783e-24  # J/T

X_IS_CURRENT = False     # set True if your dispersion CSVs use current (A) on x


# ---------------------------------------------------------------- calibration
def load_calibration():
    raw = []
    with open(CALFILE) as f:
        next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw.append([float(x) for x in line.split(",")])
    raw = np.array(raw)
    V, I, B = raw[:, 0], raw[:, 1], raw[:, 2]
    # drop supply-settling rows (first 3) and current read-off errors (I<3.0)
    mask = np.ones(len(V), bool)
    mask[:3] = False
    mask[I < 3.0] = False
    p, cov = np.polyfit(I[mask], B[mask], 1, cov=True)
    perr = np.sqrt(np.diag(cov))
    fit = np.polyval(p, I[mask])
    r2 = 1 - np.sum((B[mask] - fit) ** 2) / np.sum((B[mask] - B[mask].mean()) ** 2)
    return dict(I=I, B=B, mask=mask, slope=p[0], intercept=p[1],
                slope_err=perr[0], intercept_err=perr[1], r2=r2)


def plot_calibration(cal):
    I, B, m = cal["I"], cal["B"], cal["mask"]
    a, b = cal["slope"], cal["intercept"]
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.scatter(I[m], B[m], s=18, color="#1f3b73", zorder=3,
               label="calibration data")
    ax.scatter(I[~m], B[~m], s=22, facecolors="none", edgecolors="#b00",
               zorder=3, label="excluded (settling / read-off errors)")
    xx = np.linspace(I[m].min() - 0.05, I[m].max() + 0.05, 100)
    ax.plot(xx, a * xx + b, "-", color="#c1272d", lw=1.6,
            label=fr"linear fit: $B={a:.1f}\,I{b:+.1f}$ mT")
    ax.set_xlabel("coil current $I$ / A")
    ax.set_ylabel("magnetic flux density $B_0$ / mT")
    ax.text(0.04, 0.92, fr"$R^2={cal['r2']:.4f}$", transform=ax.transAxes, va="top")
    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.95)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "calibration_fit.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------- dispersion
def load_csv(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip().replace(";", ",")
            if not line:
                continue
            parts = [p for p in line.split(",") if p != ""]
            try:
                rows.append([float(parts[0]), float(parts[1])])
            except (ValueError, IndexError):
                continue  # header line
    a = np.array(rows)
    return a[:, 0], a[:, 1]


def resonance_field(x, y):
    """Field of steepest slope of the dispersion curve (centre estimate)."""
    order = np.argsort(x)
    xs, ys = x[order], y[order]
    dy = np.gradient(ys, xs)
    return xs[np.argmax(np.abs(dy))]


def analyse_samples(cal):
    """Iterate over CSVs in figures/csv/, make plots, compute g-factors."""
    if not os.path.isdir(CSVDIR):
        print(f"[Part B] no CSV directory yet ({CSVDIR}). "
              "Add digitised curves there to enable the g-factor analysis.")
        return
    files = sorted(f for f in os.listdir(CSVDIR) if f.lower().endswith(".csv"))
    if not files:
        print(f"[Part B] {CSVDIR} is empty -- add <sample>.csv files.")
        return
    a, b = cal["slope"], cal["intercept"]
    print("\n--- Part B: dispersion curves & g-factor ---")
    print(f"{'sample':<22}{'B0/mT':>10}{'nu0/GHz':>10}{'g':>10}")
    for fn in files:
        name = os.path.splitext(fn)[0]
        x, y = load_csv(os.path.join(CSVDIR, fn))
        if X_IS_CURRENT:
            B = a * x + b           # convert current -> field (mT)
        else:
            B = x                   # already field in mT
        B0 = resonance_field(B, y)  # mT
        # NU0: the microwave frequency. For direct mixing nu0 = 10.6 GHz,
        #      for the calibrated LNB nu0 = 9.75 GHz. Edit per sample as needed.
        nu0 = 10.6e9
        g = H * nu0 / (MU_B * (B0 * 1e-3))
        print(f"{name:<22}{B0:>10.1f}{nu0/1e9:>10.3f}{g:>10.4f}")

        fig, ax = plt.subplots(figsize=(5.6, 4.0))
        ax.plot(B, y, ".", ms=4, color="#1f3b73")
        ax.axvline(B0, ls="--", color="#c1272d", lw=1.2,
                   label=fr"$B_0={B0:.1f}$ mT")
        ax.set_xlabel("external magnetic field $B_0$ / mT")
        ax.set_ylabel("output frequency $\\nu$ / a.u.")
        ax.legend(); ax.grid(alpha=0.25)
        fig.tight_layout()
        fig.savefig(os.path.join(FIGDIR, f"disp_{name}.pdf"))
        plt.close(fig)


if __name__ == "__main__":
    cal = load_calibration()
    print("--- Part A: magnet calibration B0 = a*I + b ---")
    print(f"a = {cal['slope']:.2f} +- {cal['slope_err']:.2f} mT/A")
    print(f"b = {cal['intercept']:.2f} +- {cal['intercept_err']:.2f} mT")
    print(f"R2 = {cal['r2']:.5f}")
    plot_calibration(cal)
    analyse_samples(cal)
