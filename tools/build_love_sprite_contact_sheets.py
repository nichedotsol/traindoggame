from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SPRITES = ROOT / "assets" / "love_sprites"
OUT = SPRITES / "contact_sheets"


def parse_manifest() -> list[tuple[str, str]]:
    items = []
    for line in (SPRITES / "manifest.lua").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("[") and "] = {" in line:
            key = line.split("]")[0].strip("[]").strip('"')
            items.append((key, f"{key}.png"))
    return items


def fit(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / img.width, max_h / img.height, 1)
    return img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.Resampling.NEAREST)


def write_page(page: int, items: list[tuple[str, str]]) -> Path:
    cols = 4
    cell_w, cell_h = 330, 220
    rows = math.ceil(len(items) / cols)
    image = Image.new("RGB", (cols * cell_w, rows * cell_h), "#151221")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for index, (key, filename) in enumerate(items):
        x = (index % cols) * cell_w
        y = (index // cols) * cell_h
        draw.rectangle((x + 7, y + 7, x + cell_w - 7, y + cell_h - 7), fill="#251c31", outline="#8b7b92", width=2)
        draw.text((x + 13, y + 13), key[:48], fill="#f7b941", font=font)
        sprite = Image.open(SPRITES / filename).convert("RGBA")
        preview = fit(sprite, cell_w - 30, cell_h - 48)
        checker = Image.new("RGB", preview.size, "#2d2437")
        cd = ImageDraw.Draw(checker)
        for cy in range(0, preview.height, 8):
            for cx in range(0, preview.width, 8):
                if (cx // 8 + cy // 8) % 2 == 0:
                    cd.rectangle((cx, cy, cx + 7, cy + 7), fill="#3a3047")
        px = x + (cell_w - preview.width) // 2
        py = y + 36 + (cell_h - 48 - preview.height) // 2
        image.paste(checker, (px, py))
        image.paste(preview, (px, py), preview)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"love_sprites_page_{page:02d}.png"
    image.save(path)
    return path


def main() -> None:
    items = parse_manifest()
    per_page = 32
    written = []
    for page, start in enumerate(range(0, len(items), per_page), 1):
        written.append(write_page(page, items[start : start + per_page]))
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
