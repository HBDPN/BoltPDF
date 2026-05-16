# BoltPDF

A fast, free, lightweight **PDF reader and editor for Windows** — multi-core
PDFium rendering, Windows built-in OCR (no extra installs), a tabbed
interface, and a full annotation/editing toolset. No sign-up, no ads, no
telemetry.

## Features

**Reading**
- Multi-core PDFium rendering; tabbed, drag-and-drop multi-document
- Windows built-in OCR with selectable text; full-text search
- Page-thumbnail sidebar; recent files; per-document bookmarks
- Reading modes: continuous scroll, single page, two-page spread
- Night / sepia / warm / dim reading tints
- Crash-safe: opens blank normally, offers to recover unsaved work
  after an unclean shutdown

**Editing (beta)**
- Add / move / edit text and images; redaction and whiteout
- Shapes (rectangle, circle, line, arrow) with dashed/dotted styles,
  fill opacity, both-end arrowheads and Shift-constrain; highlighter
- Stamps with a saved stamp library, date/time stamp and Bates /
  page numbering; sticky notes (clickable in the Notes panel, plus an
  Add Note button)
- Full multi-step undo / redo; a properties inspector for the
  selected object
- Multi-select with group / ungroup, align and distribute; snapping
  with alignment guides; copy / paste / duplicate (across pages)
- In-place text editing that matches the original font style
- Edits are saved as real, editable PDF annotations
- Export pages to images or Word; combine / rebuild PDFs

> The editing tools are in active beta — solid on most documents, but
> may need care on unusual layouts or embedded fonts.

## Licence

BoltPDF is **free software** released under the
**GNU Affero General Public License, version 3 or later (AGPL-3.0-or-later)**.
The full licence text is in [`LICENSE`](LICENSE).

BoltPDF links the AGPL-licensed [PyMuPDF](https://pymupdf.readthedocs.io/)
and the GPL-3.0-licensed [PyQt6](https://www.riverbankcomputing.com/software/pyqt/).
Because of these copyleft components the **combined work is conveyed under the
AGPL-3.0**. You may use, study, share and modify it at no cost, provided you
pass on the same freedoms — including making complete corresponding source
available to anyone you give a binary to.

Licences for every bundled third-party component are reproduced verbatim in
[`THIRD_PARTY_LICENSES.txt`](THIRD_PARTY_LICENSES.txt).

## Complete corresponding source (AGPL §6)

This repository **is** the complete corresponding source for every released
binary. Each binary on the Releases page is built solely from the matching
tagged commit here. There are no hidden build steps.

## Building from source

Requires Windows x64, Python 3.x, and (optionally)
[Inno Setup 6](https://jrsoftware.org/isinfo.php) to produce the installer.

```bat
pip install -r requirements.txt
build.bat
```

`build.bat` runs PyInstaller against `BoltPDF.spec` to produce the onedir
bundle in `dist\BoltPDF\`, then compiles `BoltPDF.iss` into
`dist\BoltPDFSetup.exe`. If Inno Setup is absent it falls back to a plain zip.

## Third-party components

| Component | Licence |
|---|---|
| pypdfium2 | BSD-3-Clause / Apache-2.0 |
| PyQt6 / PyQt6-WebEngine | GPL-3.0-only |
| Qt 6 (via PyQt6) | LGPL-3.0 |
| PyMuPDF (fitz) | AGPL-3.0 |
| Pillow | MIT-CMU (HPND) |
| pypdf | BSD-3-Clause |
| python-docx | MIT |
| lxml | BSD-3-Clause |
| Python | PSF-2.0 |

OCR uses the Windows built-in `Windows.Media.Ocr` API; no OCR engine is
redistributed. Packaging uses PyInstaller (GPL + bootloader exception),
UPX (GPL + special exception) and Inno Setup (permissive) — none of which
impose additional terms on this work.
