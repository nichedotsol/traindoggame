from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOVE = ROOT / "assets" / "love_sprites"
SOURCE = ROOT / "assets" / "libresprite"
MANIFEST = LOVE / "manifest.lua"
SCRIPT = ROOT / "tools" / ".generated_libresprite_make_masters.js"
KNOWN_LOCAL_INSTALL = Path(
    r"C:\Users\ball1\Documents\Codex\libresprite-development-windows-x86_64\libresprite.exe"
)

CATEGORY_DIRS = {
    "character": "characters",
    "collectible": "collectibles",
    "environment": "environments",
    "fx": "fx",
    "hazard": "hazards",
    "hud": "hud",
    "portal": "portals",
    "route_icon": "route_icons",
    "terrain": "terrain",
}


def read_manifest() -> list[dict[str, str]]:
    text = MANIFEST.read_text(encoding="utf-8")
    entries = []
    for match in re.finditer(r'\["([^"]+)"\]\s*=\s*\{(.*?)\n\s*\},', text, re.S):
        key, block = match.groups()
        category = re.search(r'category\s*=\s*"([^"]+)"', block)
        file_name = re.search(r'file\s*=\s*"([^"]+)"', block)
        if not category or not file_name:
            continue
        out_dir = SOURCE / CATEGORY_DIRS.get(category.group(1), category.group(1))
        entries.append(
            {
                "key": key,
                "png": (ROOT / file_name.group(1)).as_posix(),
                "ase": (out_dir / f"{key}.ase").as_posix(),
            }
        )
    return entries


def write_script(entries: list[dict[str, str]]) -> None:
    for entry in entries:
        Path(entry["ase"]).parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(entries)
    SCRIPT.write_text(
        "\n".join(
            [
                "var entries = " + payload + ";",
                "for (var i = 0; i < entries.length; i++) {",
                "  var e = entries[i];",
                "  var doc = app.open(e.png);",
                "  if (!doc || !doc.sprite) { throw new Error('Could not open ' + e.png); }",
                "  doc.sprite.saveAs(e.ase, false);",
                "  doc.close();",
                "  console.log('master ' + (i + 1) + '/' + entries.length + ' ' + e.key);",
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def find_libresprite() -> Path:
    env_path = os.environ.get("LIBRESPRITE_EXE")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    path_install = shutil.which("libresprite")
    if path_install:
        return Path(path_install)
    if KNOWN_LOCAL_INSTALL.exists():
        return KNOWN_LOCAL_INSTALL
    raise SystemExit(
        "LibreSprite not found. Set LIBRESPRITE_EXE to the full path of libresprite.exe."
    )


def main() -> None:
    libresprite = find_libresprite()
    entries = read_manifest()
    write_script(entries)
    subprocess.run(
        [str(libresprite), "--batch", "--script", str(SCRIPT)],
        check=True,
        cwd=str(ROOT),
    )
    print(f"Wrote {len(entries)} LibreSprite .ase masters under {SOURCE}")


if __name__ == "__main__":
    main()
