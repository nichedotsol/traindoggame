from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "libresprite"
LOVE = ROOT / "assets" / "love_sprites"
MANIFEST = LOVE / "manifest.lua"


def manifest_keys() -> list[str]:
    text = MANIFEST.read_text(encoding="utf-8")
    return re.findall(r'\["([^"]+)"\]\s*=', text)


def main() -> None:
    keys = manifest_keys()
    sources = {path.stem for path in SOURCE.rglob("*") if path.suffix.lower() in {".ase", ".aseprite"}}
    missing_sources = [key for key in keys if key not in sources]
    missing_pngs = [key for key in keys if not (LOVE / f"{key}.png").exists()]

    print(f"manifest sheets: {len(keys)}")
    print(f"libresprite sources: {len(sources)}")
    print(f"missing libresprite sources: {len(missing_sources)}")
    print(f"missing runtime pngs: {len(missing_pngs)}")
    if missing_sources:
        print("\nfirst missing sources:")
        for key in missing_sources[:40]:
            print(f"  {key}.aseprite")
    if missing_pngs:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
