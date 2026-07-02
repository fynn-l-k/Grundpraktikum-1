#!/usr/bin/env python3
"""
Regenerate the dispersion "*_curve.png" figures for Aufgabe 5 and Aufgabe 6.

Input CSVs (col1 = downmixed frequency [Hz], col2 = calibrated field [mT]) live in
    ../../Aufgabe_5_Magnetfeld/*.csv
    ../../Aufgabe_6_Magnetfeld/*.csv

Plot convention (matches the DPPH figures in the old protocol):
  * x = magnetic field B0 [T], y = downmixed frequency [kHz]
  * red dashed vertical line  -> resonance field B0 (steepest point of the S-curve)
  * green dotted horizontal line -> resonance frequency nu = curve value AT B0
Because nu is read off the curve exactly at the steepest (inflection) point, the
green line always lands in the MIDDLE of the S-curve, never at the peak/trough.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
A5 = os.path.join(ROOT, "Aufgabe_5_Magnetfeld")
A6 = os.path.join(ROOT, "Aufgabe_6_Magnetfeld")
FIG = os.path.join(HERE, "figures")

# csv file -> (output png stem, plot title, B0_fixed [T], nu_off [kHz])
# B0_fixed pins the red resonance-field line; nu (green) is then read off the
# curve AT B0 so both lines meet on the trace, in the MIDDLE of the S-feature.
# nu_off is a small manual nudge of the green line (and, implicitly via B0, the
# red line) requested for two plots:
#   * UM unverdünnt: B0 nudged left to 0.356 -> green a bit higher on the flank
#   * DPPH 1 µg: green nudged a little lower
JOBS = [
    (os.path.join(A5, "DPPH_1ug.csv"),            "task4_dpph_1ug_curve",       "DPPH 1 µg",   0.372, -30.0),
    (os.path.join(A5, "DPPH_10ug.csv"),           "task4_dpph_10ug_curve",      "DPPH 10 µg",  0.345,   0.0),
    (os.path.join(A5, "pure_ultramarine.csv"),    "task5_um_pure_curve",        "UM unverdünnt", 0.357, 0.0),
    (os.path.join(A5, "ultramarine_1_10.csv"),    "task5_um_1_10_curve",        "UM 1:10",     0.370,   0.0),
    (os.path.join(A5, "ultramarine_1_100.csv"),   "task5_um_1_100_curve",       "UM 1:100",    0.370,   0.0),
    (os.path.join(A5, "ultramarine_1_1000.csv"),  "task5_um_1_1000_curve",      "UM 1:1000",   0.359,   0.0),
    (os.path.join(A6, "DPPH_10ug_calibrated.csv"),"task6_dpph_calibrated_curve","DPPH 10 µg, kalibrierter LNB", 0.374, 0.0),
]


def load(path):
    """Return (B_field_T, freq_kHz), rows sorted by field, NaNs dropped."""
    a = np.genfromtxt(path, delimiter=",")
    a = a[np.isfinite(a).all(axis=1)]
    freq_kHz = a[:, 0]            # col1 is already in kHz
    B_T = a[:, 1] / 1000.0        # col2 is field in mT -> T
    order = np.argsort(B_T)
    return B_T[order], freq_kHz[order]


def main_cluster(B, f):
    """Drop the isolated low-field strays: keep the longest run of points whose
    point-to-point spacing in B stays below an outlier-gap threshold."""
    dB = np.diff(B)
    gap = np.median(dB) * 6 if len(dB) else 0.0
    runs, cur = [], [0]
    for i in range(1, len(B)):
        if dB[i - 1] <= gap:
            cur.append(i)
        else:
            runs.append(cur); cur = [i]
    runs.append(cur)
    main = max(runs, key=len)
    return B[main], f[main]


def resonance(B, f, B0_fixed=None, nu_off=0.0):
    """Return (B0, nu).

    B0: the protocol value if given, else the steepest point of the S-curve.
    nu: the curve frequency AT B0, taken as the mean over a small B-window
        centred on B0. On a symmetric/near-vertical S-feature this is the
        baseline-crossing value, so the green line sits in the MIDDLE of the S.
    """
    Bc, fc = main_cluster(B, f)

    if B0_fixed is None:
        # steepest slope via a local linear fit over a small moving window
        k = max(3, len(Bc) // 12)
        best_i, best_slope = len(Bc) // 2, 0.0
        for i in range(len(Bc)):
            a, b = max(0, i - k), min(len(Bc), i + k + 1)
            if b - a < 2 or (Bc[b - 1] - Bc[a]) == 0:
                continue
            slope = np.polyfit(Bc[a:b], fc[a:b], 1)[0]
            if abs(slope) > abs(best_slope):
                best_slope, best_i = slope, i
        B0 = float(Bc[best_i])
    else:
        B0 = float(B0_fixed)

    # nu = frequency where the red B0 line crosses the dispersion trace, taken
    # as the vertical centre of the trace in a TIGHT field window around B0
    # (midpoint of its min and max there). On a near-vertical jump this is the
    # baseline-crossing level; on a gentle branch it is simply the curve value
    # at B0. Either way the green line meets the red line on the curve and sits
    # in the MIDDLE of the S-feature.
    # Use ALL points here (not just the main cluster): on a near-vertical jump
    # the two arms can fall into separate B-runs, and we need both to find the
    # true vertical centre of the feature.
    win = 0.002                                      # +/- window in Tesla
    sel = np.abs(B - B0) <= win
    while sel.sum() < 4 and win < 0.02:              # widen if too sparse
        win += 0.002
        sel = np.abs(B - B0) <= win
    fw = f[sel]
    nu = float(0.5 * (fw.min() + fw.max())) + nu_off
    return B0, nu


def main():
    for path, stem, title, B0_fixed, nu_off in JOBS:
        if not os.path.exists(path):
            print("skip (missing):", path)
            continue
        B, f = load(path)
        B0, nu = resonance(B, f, B0_fixed, nu_off)

        fig, ax = plt.subplots(figsize=(6.4, 4.8))
        ax.scatter(B, f, s=18, color="#1f3b73", zorder=3)
        ax.axvline(B0, color="red", ls="--", lw=1.8,
                   label=fr"$B_0$ = {B0:.3f} T")
        ax.axhline(nu, color="green", ls=":", lw=1.8,
                   label=fr"$\nu$ = {nu:.0f} kHz")
        ax.set_xlabel(r"äußeres Magnetfeld $B_0$ [T]")
        ax.set_ylabel("Frequenz [kHz]")
        ax.set_title(title)
        ax.legend(loc="best")
        ax.grid(alpha=0.25)
        fig.tight_layout()
        out = os.path.join(FIG, stem + ".png")
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"{stem}: B0={B0:.4f} T, nu={nu:.1f} kHz -> {out}")


if __name__ == "__main__":
    main()
