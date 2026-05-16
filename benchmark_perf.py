# SPDX-License-Identifier: AGPL-3.0-or-later
"""
BoltPDF performance benchmark harness.

Measures the two things the "lightweight" promise depends on:

  1. Cold-open latency   — time from PdfDocument(path) to the first
                            page being rendered (what the user feels).
  2. Peak RSS memory     — high-water mark while rendering a windowed
                            burst of pages, the way the app does.

It deliberately mirrors pdf_reader.py's render path (pypdfium2,
draw_annots=False, the adaptive ~1.5 Mpx scale) so the numbers track
the real app. Run it BEFORE and AFTER each Phase 1 feature on the same
files; fail the change if cold-open or peak memory regresses.

Usage:
    python benchmark_perf.py <big.pdf> [more.pdf ...] [--window 21] [--json]

Tip: test with one 500+ page vector PDF and one large scanned PDF —
those are the two worst cases for a reader.
"""

import argparse
import gc
import json
import os
import sys
import time

try:
    import pypdfium2 as pdfium
except ImportError:
    sys.exit("pypdfium2 not installed — run: pip install -r requirements.txt")

_TARGET_PIXELS = 1_500_000  # must match DocumentTab._TARGET_PIXELS


def _choose_scale(pt_w: float, pt_h: float) -> float:
    raw = (_TARGET_PIXELS / max(pt_w * pt_h, 1)) ** 0.5
    return max(0.5, min(round(raw, 2), 3.0))


def _peak_rss_mb() -> float | None:
    """Best-effort current RSS in MiB (psutil if present, else Windows
    ctypes, else None)."""
    try:
        import psutil  # type: ignore
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        pass
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            class _PMC(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            c = _PMC()
            c.cb = ctypes.sizeof(_PMC)
            h = ctypes.windll.kernel32.GetCurrentProcess()
            if ctypes.windll.psapi.GetProcessMemoryInfo(
                    h, ctypes.byref(c), c.cb):
                return c.PeakWorkingSetSize / (1024 * 1024)
        except Exception:
            pass
    return None


def benchmark(path: str, window: int) -> dict:
    n_pages = 0
    result = {"file": os.path.basename(path)}

    gc.collect()
    rss_before = _peak_rss_mb()

    # --- Cold open: open + size sampling, exactly like load_pdf ----------
    t0 = time.perf_counter()
    doc = pdfium.PdfDocument(path)
    n_pages = len(doc)
    sample_idx = sorted(set(
        [0, n_pages // 4, n_pages // 2, 3 * n_pages // 4, n_pages - 1]))
    sample_idx = [i for i in sample_idx if 0 <= i < n_pages]
    sizes = []
    for i in sample_idx:
        pg = doc[i]
        sizes.append((pg.get_width(), pg.get_height()))
        pg.close()
    pt_w, pt_h = sizes[0]
    scale = _choose_scale(pt_w, pt_h)

    # First visible page rendered = what the user actually waits for.
    pg = doc[0]
    pg.render(scale=scale, draw_annots=False).to_pil()
    pg.close()
    cold_open = time.perf_counter() - t0

    # --- Windowed burst: render a focus window like the app does --------
    t1 = time.perf_counter()
    lo = max(0, n_pages // 2 - window // 2)
    hi = min(n_pages - 1, lo + window - 1)
    for i in range(lo, hi + 1):
        pg = doc[i]
        pg.render(scale=scale, draw_annots=False).to_pil()
        pg.close()
    burst = time.perf_counter() - t1
    rendered = hi - lo + 1
    doc.close()

    rss_after = _peak_rss_mb()
    result.update({
        "pages": n_pages,
        "scale": scale,
        "cold_open_s": round(cold_open, 3),
        "window_pages": rendered,
        "window_render_s": round(burst, 3),
        "per_page_ms": round(burst / max(rendered, 1) * 1000, 1),
        "peak_rss_mb": (round(rss_after, 1)
                        if rss_after is not None else None),
        "rss_delta_mb": (round(rss_after - rss_before, 1)
                         if rss_after is not None
                         and rss_before is not None else None),
    })
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="BoltPDF perf benchmark")
    ap.add_argument("pdfs", nargs="+", help="PDF file(s) to benchmark")
    ap.add_argument("--window", type=int, default=21,
                    help="focus-window size (default 21 = ±10, matches "
                         "PageRenderer._RENDER_WINDOW)")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON")
    args = ap.parse_args()

    results = []
    for p in args.pdfs:
        if not os.path.isfile(p):
            print(f"SKIP (not found): {p}", file=sys.stderr)
            continue
        results.append(benchmark(p, args.window))

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    for r in results:
        print(f"\n{r['file']}  ({r['pages']} pp, scale {r['scale']})")
        print(f"  cold open .......... {r['cold_open_s']:.3f} s   "
              "(open + sample + first page)")
        print(f"  window render ...... {r['window_render_s']:.3f} s "
              f"for {r['window_pages']} pp  "
              f"({r['per_page_ms']:.1f} ms/page)")
        if r["peak_rss_mb"] is not None:
            extra = (f"  (+{r['rss_delta_mb']} MB)"
                     if r["rss_delta_mb"] is not None else "")
            print(f"  peak RSS ........... {r['peak_rss_mb']} MB{extra}")
        else:
            print("  peak RSS ........... (install psutil for memory "
                  "numbers)")
    print("\nRun identically before/after each change; treat a >10% "
          "cold-open or peak-RSS rise as a regression.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
