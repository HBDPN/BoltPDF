# BoltPDF

A lightweight, multi-core PDF reader and editor for Windows. Fast PDFium
rendering, Windows built-in OCR (no external installs), tabs, annotation
and redaction tools.

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
