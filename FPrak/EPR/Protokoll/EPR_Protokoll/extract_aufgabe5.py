#!/usr/bin/env python3
"""
Extract the dispersion curves from every HDSDR screenshot in Aufgabe5/
and store them as CSV:   x = frequency [kHz] , y = time [s from top of waterfall].

Per-image calibration (read off the screenshots):
  * frequency ruler: leftmost label value [kHz] and tick step [kHz]
  * time axis: wall-clock of the first and last timestamp label -> elapsed s
Pixel anchors (ruler label centres, timestamp row centres) are detected
automatically; the physical values above pin the linear axes.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A5 = os.path.join(ROOT, "Aufgabe5")
OUT = os.path.join(os.path.dirname(__file__), "figures", "csv_aufgabe5")
os.makedirs(OUT, exist_ok=True)

# name -> (file, first_label_kHz, tick_step_kHz, elapsed_seconds_first_to_last)
CFG = {
    "DPPH_1ug":        ("DPPH_1mg_Sequence.png",       792800, 100, 105),
    "DPPH_10ug":       ("DPPH_Sequence_10mg.png",      792200, 100, 101),
    "UM_pure":         ("pure_ultramarine.png",        792900, 100, 144),
    "UM_pure_best":    ("pure_ultramarine_best.png",   793200,  20, 238),
    "UM_pure_zoomed":  ("pure_ultramarine_zoomed.png", 793150,  50, 239),
    "UM_1_10":         ("ultramarine_1_10.png",        794260,  20, 117),
    "UM_1_100":        ("ultramarine_1_100.png",       796600,  10, 122),
    "UM_1_1000":       ("ulramarine_1_1000.png",       794517,   3, 197),
}

# The undiluted-UM screenshots captured the sweep several times. Keep one clean
# cycle by restricting to a time window [s] (only for these redundant views).
TIME_WINDOW = {
    "UM_pure":        (19, 51),
    "UM_pure_best":   (-5, 47),
    "UM_pure_zoomed": (120, 161),
}


def ruler_fit(a, f0, step):
    """kHz = m*x_px + c from the white numerals under the waterfall."""
    H, W, _ = a.shape
    band = a[543:556, 150:W - 90]
    wht = (band[:, :, 0] > 200) & (band[:, :, 1] > 200) & (band[:, :, 2] > 200)
    cols = np.where(wht.sum(axis=0) > 0)[0]
    runs = []
    cur = [cols[0]]
    for x in cols[1:]:
        if x - cur[-1] <= 6:
            cur.append(x)
        else:
            runs.append((cur[0], cur[-1])); cur = [x]
    runs.append((cur[0], cur[-1]))
    centers = []
    grp = [runs[0]]
    for s, e in runs[1:]:
        if s - grp[-1][1] <= 20:     # intra-number gap ~11, inter-number ~38
            grp.append((s, e))
        else:
            centers.append((grp[0][0] + grp[-1][1]) / 2); grp = [(s, e)]
    centers.append((grp[0][0] + grp[-1][1]) / 2)
    centers = np.array(centers) + 150
    freqs = f0 + step * np.arange(len(centers))
    m, c = np.polyfit(centers, freqs, 1)
    return m, c


def time_fit(a, elapsed_s):
    """seconds_from_top = m*y_px + c from the first/last timestamp rows."""
    white = (a[:, :, 0] > 200) & (a[:, :, 1] > 200) & (a[:, :, 2] > 200)
    left = white[:, 2:88].sum(axis=1)
    rows = np.where(left > 5)[0]
    rows = rows[(rows >= 34) & (rows <= 525)]
    g = []
    cur = [rows[0]]
    for r in rows[1:]:
        if r - cur[-1] <= 4:
            cur.append(r)
        else:
            g.append(int(np.mean(cur))); cur = [r]
    g.append(int(np.mean(cur)))
    y0, y1 = g[0], g[-1]
    m = elapsed_s / (y1 - y0)        # s per pixel
    c = -m * y0
    return m, c


def extract_branch(a):
    """Strongest dispersion branch: (y_px, x_px).

    For every time row we take the position of the BRIGHTEST trace pixel (the
    strongest signal), so faint repeated sweeps sitting next to the main one are
    ignored. Rows whose peak is too dim to be a real trace are dropped. If two
    disjoint branches remain (e.g. the waterfall wrapped), the one carrying the
    higher total brightness is kept.
    """
    H, W, _ = a.shape
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    score = (r + g) - b                 # trace = warm colours, background = blue
    y0, y1, x0, x1 = 34, 527, 150, W - 90
    sub = score[y0:y1, x0:x1]
    peak = sub.max(axis=1)
    # Adaptive per-row threshold: a row carries a trace if its peak stands clearly
    # above that row's own background. This keeps the FAINT dispersion wings (the
    # long low-field tail) that a single global threshold would drop.
    cy, cx, cw = [], [], []
    for i in range(sub.shape[0]):
        row = sub[i]
        base = np.median(row)
        pk = row.max()
        if pk < base + 45 or pk < 55:   # no real trace in this row
            continue
        xmax = int(np.argmax(row))
        lo, hi = max(0, xmax - 6), min(len(row), xmax + 7)
        seg = np.clip(row[lo:hi] - base, 0, None)
        cx.append((np.arange(lo, hi) * seg).sum() / seg.sum() + x0)
        cy.append(i + y0)
        cw.append(pk)
    cy = np.array(cy, float); cx = np.array(cx, float); cw = np.array(cw, float)
    # split into y-continuous branches; small gaps (<=18 px) still count as the
    # same sweep so the tail stays attached to the main S-curve.
    segs = []
    cur = [0]
    for i in range(1, len(cy)):
        if cy[i] - cy[i - 1] <= 18:
            cur.append(i)
        else:
            segs.append(cur); cur = [i]
    segs.append(cur)

    # score each branch: the most complete single sweep spans the whole
    # dispersion (large frequency extent) with many points and high brightness.
    def branch_score(s):
        s = np.array(s)
        fx = cx[s]
        extent = fx.max() - fx.min()
        return len(s) * (1 + extent / 20.0) * (cw[s].mean() / 255.0)

    keep = np.array(max(segs, key=branch_score))
    ky, kx, kw = cy[keep], cx[keep], cw[keep]
    order = np.argsort(ky)
    ky, kx, kw = ky[order], kx[order], kw[order]

    # If the waterfall captured the sweep several times, the trace runs through
    # the same S-curve repeatedly. Cut it into cycles at the points where the
    # frequency jumps sharply back (end of one sweep -> start of the next) and
    # keep the single most complete cycle (widest frequency span).
    dx = np.diff(kx)
    dy = np.diff(ky)
    # a cycle boundary = a large BACKWARD frequency jump over a small time step
    # (sweep resets); the smooth tail (large dx spread over many rows) is NOT cut.
    jump = max(np.median(np.abs(dx)) * 8, 40)
    cuts = [0] + [i + 1 for i in range(len(dx))
                  if dx[i] < -jump and dy[i] <= 6] + [len(kx)]
    cycles = [(cuts[j], cuts[j + 1]) for j in range(len(cuts) - 1)
              if cuts[j + 1] - cuts[j] >= 20]
    if len(cycles) > 1:
        s, e = max(cycles, key=lambda c: kx[c[0]:c[1]].max() - kx[c[0]:c[1]].min())
        ky, kx = ky[s:e], kx[s:e]

    # NOTE: no frequency-based outlier filter here -- the dispersion curve
    # legitimately spans a wide frequency range (including the long flat wing at
    # low field), so filtering "far from the median frequency" would clip it.
    # Isolated strays are already suppressed by the one-point-per-time-row
    # extraction and the time-continuity segmentation above.
    return ky, kx


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 4, figsize=(19, 9))
    axes = axes.ravel()
    for ax, (name, (fn, f0, step, el)) in zip(axes, CFG.items()):
        a = np.asarray(Image.open(os.path.join(A5, fn)).convert("RGB")).astype(int)
        m_f, c_f = ruler_fit(a, f0, step)
        m_t, c_t = time_fit(a, el)
        yy, xx = extract_branch(a)
        freq_kHz = m_f * xx + c_f
        time_s = m_t * yy + c_t
        if name in TIME_WINDOW:
            lo, hi = TIME_WINDOW[name]
            m = (time_s >= lo) & (time_s <= hi)
            freq_kHz, time_s = freq_kHz[m], time_s[m]
        out = np.column_stack([freq_kHz, time_s])
        np.savetxt(os.path.join(OUT, f"{name}.csv"), out, delimiter=",",
                   header="frequency_kHz,time_s", comments="")
        ax.scatter(freq_kHz / 1000, time_s, s=6, color="#1f3b73")
        ax.invert_yaxis()
        ax.set_title(f"{name} (n={len(xx)})", fontsize=9)
        ax.set_xlabel("frequency / MHz"); ax.set_ylabel("time / s")
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("/tmp/aufgabe5_curves.png", dpi=100)
    print("CSVs ->", OUT)
    print("overview -> /tmp/aufgabe5_curves.png")


if __name__ == "__main__":
    main()
