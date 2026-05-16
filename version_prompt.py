"""Pre-build version prompt for BoltPDF.

Shows a small GUI dialog that displays the current version and lets
the builder type a new one.  If confirmed, it updates:

    1.  pdf_reader.py   →  __version__ = "X.Y.Z"
    2.  BoltPDF.iss     →  #define MyAppVersion   "X.Y.Z"
    3.  version.json    →  "version": "X.Y.Z"

Exit codes:
    0  — version updated (or kept the same)
    1  — user cancelled the dialog  →  build should abort
"""

import json
import os
import re
import sys
import tkinter as tk
from tkinter import messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PY_FILE = os.path.join(SCRIPT_DIR, "pdf_reader.py")
ISS_FILE = os.path.join(SCRIPT_DIR, "BoltPDF.iss")
JSON_FILE = os.path.join(SCRIPT_DIR, "version.json")


def read_current_version() -> str:
    """Pull the current version from pdf_reader.py."""
    with open(PY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r'^__version__\s*=\s*["\']([^"\']+)["\']', line)
            if m:
                return m.group(1)
    return "0.0.0"


def update_py(version: str):
    with open(PY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r'^(__version__\s*=\s*["\'])[^"\']+(["\'])',
        rf'\g<1>{version}\2',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    with open(PY_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def update_iss(version: str):
    with open(ISS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r'(#define\s+MyAppVersion\s+")[^"]+(")',
        rf"\g<1>{version}\2",
        content,
        count=1,
    )
    with open(ISS_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def update_json(version: str):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["version"] = version
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        f.write("\n")


def main():
    current = read_current_version()

    # --- Build the dialog ---------------------------------------------------
    root = tk.Tk()
    root.title("BoltPDF — Set Build Version")
    root.resizable(False, False)

    # Centre on screen
    win_w, win_h = 370, 200
    sx = root.winfo_screenwidth() // 2 - win_w // 2
    sy = root.winfo_screenheight() // 2 - win_h // 2
    root.geometry(f"{win_w}x{win_h}+{sx}+{sy}")

    result = {"cancelled": True, "version": ""}

    tk.Label(root, text="BoltPDF Build", font=("Segoe UI", 14, "bold")).pack(
        pady=(16, 4)
    )
    tk.Label(root, text=f"Current version:  {current}", font=("Segoe UI", 10)).pack()

    frame = tk.Frame(root)
    frame.pack(pady=10)
    tk.Label(frame, text="New version:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
    entry = tk.Entry(frame, width=16, font=("Segoe UI", 11))
    entry.insert(0, current)
    entry.select_range(0, tk.END)
    entry.pack(side=tk.LEFT, padx=6)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    def on_build():
        # Grab value BEFORE destroying the window
        result["version"] = entry.get().strip()
        result["cancelled"] = False
        root.destroy()

    def on_cancel():
        root.destroy()

    tk.Button(
        btn_frame, text="Build", width=10, font=("Segoe UI", 10), command=on_build
    ).pack(side=tk.LEFT, padx=6)
    tk.Button(
        btn_frame, text="Cancel", width=10, font=("Segoe UI", 10), command=on_cancel
    ).pack(side=tk.LEFT, padx=6)

    entry.focus_set()
    entry.bind("<Return>", lambda e: on_build())
    root.protocol("WM_DELETE_WINDOW", on_cancel)

    root.mainloop()

    if result["cancelled"]:
        print("Build cancelled by user.")
        sys.exit(1)

    new_version = result["version"]
    if not new_version:
        print("No version entered — build cancelled.")
        sys.exit(1)

    # Validate format (loose: digits and dots)
    if not re.match(r"^\d+(\.\d+)*$", new_version):
        print(f"Invalid version format: {new_version}")
        sys.exit(1)

    # --- Apply updates ------------------------------------------------------
    print(f"Version: {current} -> {new_version}")

    if new_version != current:
        update_py(new_version)
        print(f"  Updated {os.path.basename(PY_FILE)}")

        update_iss(new_version)
        print(f"  Updated {os.path.basename(ISS_FILE)}")

        update_json(new_version)
        print(f"  Updated {os.path.basename(JSON_FILE)}")
    else:
        print("  Version unchanged — no files modified.")

    sys.exit(0)


if __name__ == "__main__":
    main()
