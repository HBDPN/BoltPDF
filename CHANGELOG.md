# Changelog

All notable changes to BoltPDF are documented here.

## v1.0.3

The first full public release. BoltPDF is now a fast PDF **reader *and*
editor** for Windows — and it's free and open-source under the
**GNU AGPL-3.0**.

### Highlights

- A complete editing & annotation toolset (beta) on top of the fast reader
- New reading modes including **two-page spread**, a page-thumbnail
  sidebar, bookmarks and reading tints
- Unlimited **undo / redo**; edits export as **real PDF annotations**
- Crash-safe: opens clean, and offers to recover unsaved edits after an
  unexpected close
- Now **open-source** under the GNU AGPL-3.0 licence

### Reading

- Multi-core PDFium rendering; tabbed, drag-and-drop multi-document
- Built-in Windows OCR — makes scanned pages selectable and searchable
- Reading modes: continuous scroll, single page, and **two-page spread**
- Lazy page-thumbnail sidebar
- Recent-files list and per-document bookmarks
- Night / sepia / warm / dim reading tints
- Full-text search (including OCR'd text)
- Detect and export embedded images as JPEG
- Opens with no document by default; only re-opens a PDF if it had
  unsaved work when the app last closed unexpectedly

### Editing & annotation (Beta)

- Add, move and edit text and images; in-place text editing matches the
  original font style
- Shapes — rectangle, circle, line, arrow — with dashed/dotted styles,
  fill colour and opacity, double-ended arrows, and Shift-to-constrain
- Highlighter and sticky notes (listed in the Notes panel; click a note
  to jump to its page)
- Redaction and whiteout
- Stamps: a saved custom-stamp library, date/time stamp, and
  Bates / page numbering across the document
- Unlimited multi-step **undo / redo** (Ctrl+Z / Ctrl+Y)
- Properties inspector for exact position, size, colour, stroke and
  opacity of the selected object
- Multi-select tool: rubber-band select, group / ungroup, align,
  distribute, and bulk move / delete
- Snapping with live alignment guides
- Copy / paste / duplicate objects — including across pages
- Edits save as **standard PDF annotations** that other readers
  (Acrobat, etc.) can open and edit
- Export pages to images or Word; combine / rebuild PDFs

### Fixes & changes

- Notes panel: clicking a note jumps to its page, and a note moved to
  another page now updates its jump target
- Added an **Add Note** button to the Notes panel
- Exiting Edit mode now offers **Keep / Discard** — you can keep your
  changes without saving until the file is closed
- Removed the old "Generate Preview" feature (the Pages thumbnail
  sidebar replaces it)
- Fixed the page jumping back to the last wheel position when switching
  from scrollbar to mouse-wheel in single-page mode
- Fixed several two-page-spread edge cases (fit-to-page centring,
  switching layout, and the post-reload recovery prompt)

### Licensing

BoltPDF is now released under the **GNU Affero General Public License
v3.0**. Because it links PyMuPDF (AGPL) and PyQt6 (GPL), the combined
work is conveyed under the AGPL-3.0. Complete corresponding source is
available in this repository; bundled component licences are listed in
`THIRD_PARTY_LICENSES.txt`.

### Requirements

Windows 10 or 11 (64-bit). Free, no sign-up, no telemetry — the only
network use is an optional check to GitHub for updates.

> **Note:** the editing tools are in active beta. They work well on most
> documents but may need care on unusual layouts or embedded fonts.
> Feedback is welcome.
