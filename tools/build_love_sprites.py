from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "love_sprites"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_spritesheets as base  # noqa: E402
import love_reference_art as art  # noqa: E402


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", value).strip("_")


def save_action_sheet(name: str, frame_width: int, frame_height: int, action: str, drawer, frames: int = 4) -> dict:
    sheet = Image.new("RGBA", (frame_width * frames, frame_height), (0, 0, 0, 0))
    for index in range(frames):
        tile = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(tile)
        drawer(draw, action, index)
        sheet.alpha_composite(tile, (index * frame_width, 0))
    path = OUT / f"{name}.png"
    sheet.save(path)
    return {
        "file": f"assets/love_sprites/{name}.png",
        "frameWidth": frame_width,
        "frameHeight": frame_height,
        "frames": frames,
        "duration": 0.12,
    }


def lua_quote(value: str) -> str:
    return json.dumps(value)


def write_lua_manifest(manifest: dict) -> None:
    lines = ["return {", "  sheets = {"]
    for key in sorted(manifest):
        item = manifest[key]
        lines.append(f"    [{lua_quote(key)}] = {{")
        lines.append(f"      file = {lua_quote(item['file'])},")
        lines.append(f"      frameWidth = {item['frameWidth']},")
        lines.append(f"      frameHeight = {item['frameHeight']},")
        lines.append(f"      frames = {item['frames']},")
        lines.append(f"      duration = {item['duration']},")
        lines.append(f"      category = {lua_quote(item['category'])},")
        lines.append(f"      action = {lua_quote(item['action'])},")
        lines.append(f"      subject = {lua_quote(item['subject'])},")
        lines.append("    },")
    lines.append("  }")
    lines.append("}")
    (OUT / "manifest.lua").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict] = {}

    def add(category: str, subject: str, action: str, fw: int, fh: int, drawer, frames: int = 4) -> None:
        key = f"{slug(category)}_{slug(subject)}_{slug(action)}"
        data = save_action_sheet(key, fw, fh, action, drawer, frames)
        data.update({"category": category, "subject": subject, "action": action})
        manifest[key] = data

    for action in ["idle", "move", "jump", "land", "duck", "hurt", "cheer", "board"]:
        add("character", "train_dog", action, 92, 58, art.draw_train)

    for passenger in base.PASSENGERS:
        for action in ["idle", "walk", "wave", "board", "cheer"]:
            add("character", passenger, action, 44, 50, art.draw_passenger(passenger))

    for collectible in ["gold_whistle", "silver_bone", "rainbow_ticket", "star_coin"]:
        for action in ["idle", "spin", "sparkle", "collect"]:
            add("collectible", collectible, action, 30, 28, art.draw_collectible(collectible))

    for hazard in [
        "spiked_ball",
        "boulder",
        "cactus",
        "crow",
        "pine_rock",
        "snow_boulder",
        "lantern",
        "wave_crate",
        "ice_spike",
        "meteor",
        "crater",
    ]:
        for action in ["idle", "warning", "active", "broken"]:
            add("hazard", hazard, action, 40, 40, art.draw_hazard(hazard))

    for destination, color in base.PORTALS.items():
        for action in ["closed", "idle", "open", "activate"]:
            add("portal", destination, action, 56, 70, art.draw_portal(destination))

    for destination in base.DESTINATIONS:
        for action in [
            "cloud_drift",
            "parallax_far",
            "parallax_mid",
            "parallax_near",
            "rail_scroll",
            "full_scroll",
            "arrival_flash",
            "danger_shake",
        ]:
            add("environment", destination, action, 320, 180, art.draw_environment(destination))

    for destination in base.PORTALS:
        for action in ["idle", "selected", "complete"]:
            add("route_icon", destination, action, 48, 32, art.draw_destination_icon(destination))

    for action in [
        "grass",
        "stone",
        "bush",
        "rail",
        "wood",
        "water",
        "sand",
        "ice",
        "flower",
        "mushroom",
        "rock",
        "crate",
        "barrel",
        "sign",
        "lamp",
        "cloud",
    ]:
        add("terrain", action, "variant", 32, 32, lambda draw, _action, index, tile=action: art.draw_tile(draw, tile, index))

    for action in ["puff", "burst", "fade"]:
        add("fx", "smoke", action, 64, 40, art.draw_smoke)

    for action in ["full", "empty", "pulse", "gain", "lose"]:
        add("hud", "heart", action, 32, 32, art.draw_heart)

    for action in ["whistle", "bone", "coin", "space_button", "route_marker"]:
        add("hud", "meter", action, 64, 24, art.draw_meter)

    write_lua_manifest(manifest)
    print(f"Wrote {len(manifest)} LÖVE2D sprite sheets to {OUT}")


if __name__ == "__main__":
    main()
