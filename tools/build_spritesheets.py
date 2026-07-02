from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "spritesheets"

INK = "#111018"
CREAM = "#fff3cf"
GOLD = "#f7b941"
DOG = "#e0a14a"
DOG_LIGHT = "#f1bd62"
DOG_DARK = "#b77036"
PINK = "#f386a4"
STEEL = "#25232b"
STEEL_LIGHT = "#555861"


def rgba(color: str) -> tuple[int, int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4)) + (255,)


def px(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, color: str) -> None:
    draw.rectangle((round(x), round(y), round(x + w - 1), round(y + h - 1)), fill=rgba(color))


def frame(width: int, height: int, drawer: Callable[[ImageDraw.ImageDraw, int], None], index: int) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    drawer(ImageDraw.Draw(img), index)
    return img


def save_sheet(
    name: str,
    frame_width: int,
    frame_height: int,
    actions: list[str],
    drawer: Callable[[ImageDraw.ImageDraw, str, int], None],
    frames_per_action: int = 4,
) -> dict:
    sheet = Image.new("RGBA", (frame_width * frames_per_action, frame_height * len(actions)), (0, 0, 0, 0))
    action_meta = {}
    for row, action in enumerate(actions):
        action_meta[action] = []
        for col in range(frames_per_action):
            tile = frame(frame_width, frame_height, lambda d, i, a=action: drawer(d, a, i), col)
            sheet.alpha_composite(tile, (col * frame_width, row * frame_height))
            action_meta[action].append(
                {
                    "x": col * frame_width,
                    "y": row * frame_height,
                    "w": frame_width,
                    "h": frame_height,
                    "durationMs": 120,
                }
            )
    path = OUT / f"{name}.png"
    sheet.save(path)
    return {
        "file": f"assets/spritesheets/{name}.png",
        "frameSize": {"w": frame_width, "h": frame_height},
        "actions": action_meta,
    }


def dog_head(draw: ImageDraw.ImageDraw, x: int, y: int, tongue: bool = True, blink: bool = False) -> None:
    px(draw, x + 5, y + 2, 24, 23, INK)
    px(draw, x + 7, y + 4, 19, 19, DOG)
    px(draw, x + 4, y + 7, 6, 13, DOG_DARK)
    px(draw, x + 24, y + 8, 5, 11, DOG_DARK)
    px(draw, x + 12, y + 3, 10, 5, DOG_LIGHT)
    if blink:
        px(draw, x + 15, y + 14, 6, 2, INK)
    else:
        px(draw, x + 16, y + 13, 4, 3, INK)
    px(draw, x + 25, y + 14, 7, 6, INK)
    px(draw, x + 18, y + 20, 10, 2, INK)
    if tongue:
        px(draw, x + 22, y + 22, 7, 10, PINK)
        px(draw, x + 25, y + 23, 2, 5, "#ffc0cc")
        px(draw, x + 22, y + 31, 6, 2, INK)


def train_body(draw: ImageDraw.ImageDraw, wheel_shift: int = 0, tilt: int = 0, flare: bool = False) -> None:
    px(draw, 4, 22 + tilt, 44, 19, INK)
    px(draw, 8, 15 + tilt, 26, 13, INK)
    px(draw, 10, 17 + tilt, 22, 9, STEEL)
    px(draw, 6, 24 + tilt, 39, 14, "#24232a")
    px(draw, 14, 10 + tilt, 10, 7, INK)
    px(draw, 16, 8 + tilt, 12, 3, "#30303a")
    px(draw, 37, 8 + tilt, 9, 13, INK)
    px(draw, 39, 5 + tilt, 11, 4, "#30303a")
    px(draw, 43, 20 + tilt, 9, 3, "#bd6841")
    px(draw, 2, 35 + tilt, 54, 5, INK)
    for i in range(4):
        x = 9 + i * 11
        px(draw, x, 40 + tilt, 8, 8, INK)
        px(draw, x + 2 + wheel_shift, 42 + tilt, 4, 4, STEEL_LIGHT)
    px(draw, 5, 22 + tilt, 4, 14, "#4b2930")
    px(draw, 10, 25 + tilt, 3, 8, "#6ea5b3")
    if flare:
        px(draw, 38, 43 + tilt, 9, 3, "#f7b941")
        px(draw, 46, 43 + tilt, 8, 3, "#ff6e38")


def draw_train(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    offsets = {
        "idle": (0, 0, False, True),
        "move": (i % 3, 0 if i % 2 else -1, False, True),
        "jump": (1, -5 + min(i, 2), True, True),
        "land": (0, 4 - i, False, True),
        "duck": (i % 2, 5, False, False),
        "hurt": (0, 1, False, False),
        "cheer": (i % 2, -1, True, True),
        "board": (i % 2, 0, False, True),
    }
    wheel, tilt, flare, tongue = offsets[action]
    train_body(draw, wheel, tilt, flare)
    dog_head(draw, 49, 10 + tilt, tongue=tongue, blink=action == "hurt" and i % 2 == 0)
    if action != "duck":
        px(draw, 36, 2 + tilt, 7 + i % 2, 4, "#d9d9df")
        px(draw, 26, 0 + tilt - i % 2, 8, 5, "#e9eef2")
        px(draw, 16, 2 + tilt, 7, 4, "#e9eef2")
    if action == "cheer":
        px(draw, 75, 1 + i % 2, 7, 7, GOLD)
        px(draw, 82, 4 + i % 2, 6, 3, GOLD)


def person_base(draw: ImageDraw.ImageDraw, x: int, y: int, coat: str, hat: str, skin: str = "#d59a66") -> None:
    px(draw, x + 4, y + 5, 14, 14, skin)
    px(draw, x + 6, y + 10, 2, 2, INK)
    px(draw, x + 14, y + 10, 2, 2, INK)
    px(draw, x + 9, y + 16, 6, 2, INK)
    px(draw, x + 2, y + 20, 18, 17, coat)
    px(draw, x + 1, y + 37, 7, 6, INK)
    px(draw, x + 14, y + 37, 7, 6, INK)
    px(draw, x + 1, y + 1, 20, 6, INK)
    px(draw, x + 4, y - 1, 14, 6, hat)


PASSENGERS = {
    "conductor": ("#3157a8", "#1b285b", "#d59a66"),
    "fox_passenger": ("#4da85e", "#d87432", "#d87432"),
    "rabbit_passenger": ("#f2a5c7", "#f4f5ff", "#f4f5ff"),
    "cool_cat": ("#c7943d", "#29263a", "#7b6b62"),
    "bear_tourist": ("#bf6b36", "#9b2f29", "#a16b43"),
    "frog_friend": ("#63b957", "#28613d", "#63b957"),
    "sheep_hiker": ("#9a9daf", "#f4f5ff", "#d59a66"),
    "astronaut": ("#f4f5ff", "#f4f5ff", "#d59a66"),
}


def draw_passenger(kind: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        y = 3 + (1 if action == "walk" and i % 2 else 0)
        coat, hat, skin = PASSENGERS[kind]
        if kind == "rabbit_passenger":
            px(draw, 14, y - 1, 5, 10, INK)
            px(draw, 23, y - 1, 5, 10, INK)
            px(draw, 15, y, 3, 9, "#f4f5ff")
            px(draw, 24, y, 3, 9, "#f4f5ff")
        if kind == "frog_friend":
            px(draw, 11, y + 3, 22, 18, INK)
            px(draw, 13, y + 5, 18, 16, skin)
            px(draw, 12, y + 4, 5, 5, skin)
            px(draw, 26, y + 4, 5, 5, skin)
            px(draw, 15, y + 10, 3, 3, INK)
            px(draw, 25, y + 10, 3, 3, INK)
            px(draw, 12, y + 23, 20, 17, coat)
        elif kind == "astronaut":
            px(draw, 10, y + 2, 24, 24, INK)
            px(draw, 12, y + 4, 20, 20, "#f4f5ff")
            px(draw, 15, y + 9, 14, 8, "#76d7ff")
            px(draw, 11, y + 27, 22, 16, "#f4f5ff")
            px(draw, 18, y + 31, 8, 5, "#ff6e7d")
        else:
            person_base(draw, 10, y + 2, coat, hat, skin)
        if action == "wave":
            px(draw, 31, y + 17 - i % 2 * 5, 9, 4, INK)
            px(draw, 34, y + 15 - i % 2 * 5, 5, 4, skin)
        if action == "board":
            px(draw, 0 + i * 2, y + 32, 12, 8, "#6b4b34")
            px(draw, 2 + i * 2, y + 29, 8, 5, GOLD)
        if action == "cheer":
            px(draw, 2, y + 6, 8, 8, GOLD)
            px(draw, 32, y + 8, 7, 7, "#ff8bad")

    return drawer


def draw_collectible(kind: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    colors = {
        "gold_whistle": (GOLD, "#ff8b26"),
        "silver_bone": ("#dbe8f2", "#85a6b5"),
        "rainbow_ticket": ("#ff6e7d", "#58d9e6"),
        "star_coin": ("#ffe483", "#f7b941"),
    }

    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        lift = 2 if action == "sparkle" and i % 2 else 0
        spin = 2 + i % 3
        a, b = colors[kind]
        if kind == "gold_whistle":
            px(draw, 5, 8 - lift, 15 + spin, 8, INK)
            px(draw, 6, 6 - lift, 13 + spin, 8, a)
            px(draw, 16 + spin, 9 - lift, 5, 4, a)
            px(draw, 8, 8 - lift, 4, 3, CREAM)
        if kind == "silver_bone":
            px(draw, 5, 9 - lift, 19, 7, INK)
            px(draw, 6, 10 - lift, 17, 5, a)
            px(draw, 3, 7 - lift, 7, 7, a)
            px(draw, 20, 7 - lift, 7, 7, a)
            px(draw, 11, 14 - lift, 8, 2, b)
        if kind == "rainbow_ticket":
            palette = ["#ff4d6d", "#f7b941", "#63d86b", "#58d9e6"]
            px(draw, 5, 5 - lift, 19, 15, INK)
            for row, color in enumerate(palette):
                px(draw, 7 + i % 2, 7 + row * 3 - lift, 15, 3, color)
        if kind == "star_coin":
            points = [(15, 3), (18, 11), (26, 11), (20, 16), (22, 24), (15, 19), (8, 24), (10, 16), (4, 11), (12, 11)]
            draw.polygon(points, fill=rgba(INK))
            inner = [(15, 6), (17, 12), (23, 12), (18, 16), (20, 21), (15, 18), (10, 21), (12, 16), (7, 12), (13, 12)]
            draw.polygon(inner, fill=rgba(a if i % 2 == 0 else b))

    return drawer


def draw_hazard(kind: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        hot = action == "active" or (action == "warning" and i % 2)
        if kind in {"pine_rock", "boulder", "snow_boulder"}:
            base = "#7b807d" if kind != "snow_boulder" else "#dfeeff"
            px(draw, 8, 20, 25, 13, INK)
            px(draw, 10 + i % 2, 17, 20, 13, base)
            px(draw, 14, 14, 12, 5, "#aeb5ae" if kind != "snow_boulder" else "#ffffff")
            if hot:
                px(draw, 12, 29, 18, 3, "#ff6e7d")
        if kind == "spiked_ball":
            px(draw, 18, 6, 4, 28, INK)
            px(draw, 8, 14, 24, 18, INK)
            px(draw, 11, 16, 18, 14, "#555861")
            for x, y in [(20, 7), (31, 21), (20, 35), (7, 21)]:
                px(draw, x - 2, y - 2, 5, 5, "#dbe8f2")
        if kind == "cactus":
            px(draw, 17, 8, 10, 28, INK)
            px(draw, 19, 6, 6, 28, "#2f9d50")
            px(draw, 9, 18, 10, 6, INK)
            px(draw, 9, 16, 7, 6, "#2f9d50")
            px(draw, 28, 20, 6, 6, "#2f9d50")
        if kind == "crow":
            px(draw, 7 + i % 2, 18, 24, 9, INK)
            px(draw, 12, 13 - i % 3, 10, 8, "#20202a")
            px(draw, 29, 18, 7, 4, "#f7b941")
            px(draw, 3, 15 + i % 3, 12, 5, "#20202a")
        if kind == "lantern":
            px(draw, 17, 5, 5, 28, INK)
            px(draw, 10, 15, 19, 18, INK)
            px(draw, 12, 17, 15, 13, "#f05467")
            px(draw, 15, 19, 8, 8, "#ffd45f" if hot else "#8b5a37")
        if kind == "wave_crate":
            px(draw, 7, 22, 25, 13, INK)
            px(draw, 9, 19, 21, 13, "#8b5a37")
            px(draw, 4, 13 - i % 2, 30, 8, INK)
            px(draw, 6, 11 - i % 2, 26, 8, "#58d9e6")
        if kind == "ice_spike":
            px(draw, 8, 33, 25, 4, INK)
            px(draw, 12, 10 - i % 2, 7, 23, "#eafcff")
            px(draw, 20, 4, 9, 29, "#a7ebff")
            px(draw, 27, 17, 5, 16, "#eafcff")
        if kind == "meteor":
            px(draw, 14 - i, 11 + i % 2, 18, 18, INK)
            px(draw, 16 - i, 9, 15, 17, "#99614d")
            px(draw, 8 - i * 2, 4, 13, 6, "#ff6e38")
            px(draw, 3 - i * 2, 8, 13, 5, "#ffd45f")
        if kind == "crater":
            px(draw, 5, 24, 30, 11, INK)
            px(draw, 8, 21, 24, 11, "#777b95")
            px(draw, 12, 24, 15, 5, "#484b5d")

    return drawer


PORTALS = {
    "forest": "#46e96f",
    "mountains": "#45a7ff",
    "city": "#b65cff",
    "desert": "#ff8b26",
    "ocean": "#25e4db",
    "arctic": "#64f7ff",
    "space": "#906cff",
    "moon": "#f4f5ff",
}


def draw_portal(color: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        glow = color if action != "closed" else "#312333"
        px(draw, 5, 13, 46, 52, INK)
        px(draw, 8, 16, 40, 48, "#6b5d5b")
        px(draw, 12, 20, 32, 41, "#312333")
        px(draw, 16, 24, 24, 34, glow)
        px(draw, 19 + i % 2, 27, 18 - i % 2 * 2, 28, "#141229")
        if action in {"open", "activate"}:
            px(draw, 22, 30, 12 + i, 22, glow)
        px(draw, 14, 10, 28, 8, "#48414b")
        px(draw, 19, 5, 18, 7, "#777b95")
        px(draw, 2, 61, 52, 6, INK)
        px(draw, 0, 52, 8, 10, GOLD)
        px(draw, 48, 52, 8, 10, GOLD)
        if action == "activate":
            px(draw, 4, 4 + i, 6, 6, glow)
            px(draw, 45, 8, 5, 5, glow)

    return drawer


def draw_tile(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    colors = {
        "grass": ("#5f923f", "#2f704c"),
        "stone": ("#777b95", "#484b5d"),
        "bush": ("#3e765d", "#27533f"),
        "rail": ("#6b4b34", "#2b202a"),
        "wood": ("#8b5a37", "#4d322f"),
        "water": ("#58d9e6", "#228f9c"),
        "sand": ("#e7b15b", "#9d5830"),
        "ice": ("#d8f7ff", "#8eb6c4"),
        "flower": ("#63d86b", "#ff8bad"),
        "mushroom": ("#f4f5ff", "#e0524d"),
        "rock": ("#7b807d", "#484b5d"),
        "crate": ("#8b5a37", "#d19b57"),
        "barrel": ("#8b5a37", "#4d322f"),
        "sign": ("#6b4b34", GOLD),
        "lamp": ("#312333", "#ffd45f"),
        "cloud": ("#f4f5ff", "#dbe8f2"),
    }
    a, b = colors[action]
    px(draw, 2, 22, 28, 8, INK)
    px(draw, 3, 16, 26, 12, a)
    px(draw, 3, 24, 26, 5, b)
    if action in {"rail", "wood"}:
        px(draw, 1, 12, 30, 5, a)
        px(draw, 7, 10, 5, 18, INK)
        px(draw, 21, 10, 5, 18, INK)
    if action in {"flower", "mushroom", "lamp"}:
        px(draw, 14, 7 + i % 2, 5, 15, b)
        px(draw, 10, 5 + i % 2, 13, 7, a if action == "lamp" else b)
    if action == "cloud":
        px(draw, 2, 14, 28, 10, a)
        px(draw, 9, 8, 14, 11, a)


def draw_destination_icon(name: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        bg = "#312333" if action == "idle" else "#4a3b5b"
        px(draw, 1, 1, 46, 30, INK)
        px(draw, 3, 3, 42, 26, bg)
        if name == "forest":
            px(draw, 8, 20, 28, 5, "#5f923f")
            for x in (10, 21, 31):
                px(draw, x, 12, 5, 12, "#6b4b34")
                px(draw, x - 5, 10, 15, 8, "#2f704c")
                px(draw, x - 3, 5, 11, 8, "#3e765d")
        if name == "mountains":
            px(draw, 7, 22, 34, 5, "#8eb6c4")
            px(draw, 10, 10, 15, 15, "#d8f7ff")
            px(draw, 22, 7, 18, 18, "#8cadc8")
        if name == "city":
            for x in (9, 17, 27, 35):
                px(draw, x, 9 + x % 3, 7, 17 - x % 3, "#6357be")
                px(draw, x + 2, 14, 2, 2, GOLD)
        if name == "desert":
            px(draw, 7, 20, 34, 7, "#e7b15b")
            px(draw, 18, 8, 9, 17, "#2f9d50")
            px(draw, 9, 16, 6, 4, "#2f9d50")
        if name == "ocean":
            px(draw, 6, 20, 35, 7, "#228f9c")
            px(draw, 19, 8, 8, 18, "#f4f5ff")
            px(draw, 17, 6, 12, 5, "#e0524d")
        if name == "arctic":
            px(draw, 6, 20, 35, 7, "#d8f7ff")
            px(draw, 13, 8, 11, 18, "#a7ebff")
            px(draw, 25, 12, 9, 14, "#eafcff")
        if name == "space":
            px(draw, 20, 5, 7, 17, "#f4f5ff")
            px(draw, 15, 18, 17, 8, "#ff6e38")
            px(draw, 12, 25, 22, 4, "#ffd45f")
        if name == "moon":
            px(draw, 15, 7, 18, 18, "#d7d8e1")
            px(draw, 18, 12, 4, 4, "#777b95")
            px(draw, 26, 16, 3, 3, "#777b95")

    return drawer


DESTINATIONS = {
    "forest": {
        "sky": ("#67b9f0", "#bfeeff"),
        "far": "#90cae8",
        "mid": "#3e765d",
        "near": "#27533f",
        "ground": "#5f923f",
        "dirt": "#5b3a25",
        "rail": "#41313b",
        "landmark": "pines",
    },
    "mountains": {
        "sky": ("#75c9ff", "#ecfbff"),
        "far": "#d7eef6",
        "mid": "#6d92b3",
        "near": "#314c67",
        "ground": "#d8f3fa",
        "dirt": "#7b786f",
        "rail": "#363945",
        "landmark": "mountains",
    },
    "city": {
        "sky": ("#6357be", "#f08aa8"),
        "far": "#ffc477",
        "mid": "#372f76",
        "near": "#1e1941",
        "ground": "#4e4364",
        "dirt": "#2b263d",
        "rail": "#171722",
        "landmark": "city",
    },
    "desert": {
        "sky": ("#f4a85e", "#ffe7a5"),
        "far": "#f7cf78",
        "mid": "#c67939",
        "near": "#9d5830",
        "ground": "#e7b15b",
        "dirt": "#8d5732",
        "rail": "#4d322f",
        "landmark": "dunes",
    },
    "ocean": {
        "sky": ("#48b7d9", "#d7fff7"),
        "far": "#76e0de",
        "mid": "#228f9c",
        "near": "#156373",
        "ground": "#d9ba71",
        "dirt": "#6c563e",
        "rail": "#33404b",
        "landmark": "lighthouse",
    },
    "arctic": {
        "sky": ("#11274e", "#75d8ff"),
        "far": "#b8fff4",
        "mid": "#59a5c8",
        "near": "#1f5f82",
        "ground": "#d8f7ff",
        "dirt": "#8eb6c4",
        "rail": "#3a4d60",
        "landmark": "aurora",
    },
    "space": {
        "sky": ("#07071b", "#15124c"),
        "far": "#45427d",
        "mid": "#22235b",
        "near": "#121333",
        "ground": "#32324f",
        "dirt": "#17172c",
        "rail": "#54516e",
        "landmark": "stars",
    },
    "moon": {
        "sky": ("#050511", "#1b1d35"),
        "far": "#777b95",
        "mid": "#555a70",
        "near": "#33384d",
        "ground": "#b9bbc7",
        "dirt": "#626676",
        "rail": "#494c5b",
        "landmark": "earth",
    },
}


def draw_environment_scene(destination: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    data = DESTINATIONS[destination]

    def sky_fill(draw: ImageDraw.ImageDraw) -> None:
        top, bottom = data["sky"]
        top_rgb = rgba(top)
        bottom_rgb = rgba(bottom)
        for y in range(180):
            t = y / 179
            color = tuple(round(top_rgb[c] * (1 - t) + bottom_rgb[c] * t) for c in range(3)) + (255,)
            draw.line((0, y, 319, y), fill=color)

    def clouds(draw: ImageDraw.ImageDraw, offset: int) -> None:
        for n in range(5):
            x = (n * 88 - offset) % 410 - 60
            y = 18 + (n % 3) * 14
            px(draw, x + 5, y + 8, 34, 7, "#f4f5ff")
            px(draw, x + 18, y + 3, 26, 12, "#f4f5ff")
            px(draw, x + 37, y + 9, 23, 6, "#f4f5ff")

    def stars(draw: ImageDraw.ImageDraw, offset: int) -> None:
        for n in range(56):
            x = (n * 47 - offset) % 360
            y = 7 + (n * 31) % 82
            size = 2 if n % 5 == 0 else 1
            px(draw, x, y, size, size, "#f4f5ff")

    def landmark(draw: ImageDraw.ImageDraw, offset: int, layer_action: str) -> None:
        landmark_name = data["landmark"]
        if layer_action == "parallax_far":
            color = data["far"]
            speed = offset // 2
        elif layer_action == "parallax_mid":
            color = data["mid"]
            speed = offset
        else:
            color = data["near"]
            speed = offset * 2

        if landmark_name == "pines":
            for n in range(12):
                x = (n * 42 - speed) % 410 - 45
                h = 30 + (n % 3) * 10
                px(draw, x + 15, 88 - h // 2, 6, h, "#513a26")
                px(draw, x + 2, 74 - h // 2, 32, 14, color)
                px(draw, x + 6, 62 - h // 2, 24, 14, data["near"])
        elif landmark_name == "mountains":
            for n in range(6):
                x = (n * 74 - speed) % 470 - 80
                px(draw, x + 10, 94, 58, 28, color)
                px(draw, x + 28, 60, 22, 36, "#eafcff")
                px(draw, x + 36, 76, 30, 24, "#8cadc8")
        elif landmark_name == "city":
            for n in range(14):
                x = (n * 28 - speed) % 390 - 35
                h = 25 + (n % 5) * 8
                px(draw, x, 113 - h, 20, h, color)
                px(draw, x + 5, 101 - h, 4, 4, GOLD)
                px(draw, x + 13, 111 - h, 4, 4, GOLD)
        elif landmark_name == "dunes":
            for n in range(5):
                x = (n * 92 - speed) % 500 - 90
                px(draw, x, 96, 88, 25, data["far"])
                px(draw, x + 35, 80, 75, 41, color)
        elif landmark_name == "lighthouse":
            x = 218 - speed % 40
            px(draw, x, 53, 20, 66, INK)
            px(draw, x + 4, 57, 12, 58, "#f4f5ff")
            px(draw, x + 4, 72, 12, 8, "#e0524d")
            px(draw, x + 1, 46, 18, 9, "#e0524d")
            px(draw, x - 18, 54, 56, 5, "#ffe483")
        elif landmark_name == "aurora":
            for x, y, c in [(40, 20, "#63e6a8"), (62, 14, "#78d3ff"), (82, 22, "#9cffd9"), (210, 12, "#63e6a8")]:
                px(draw, x + speed % 12, y, 18, 68, c)
        elif landmark_name == "stars":
            px(draw, 220 - speed % 80, 38, 15, 26, INK)
            px(draw, 224 - speed % 80, 20, 7, 18, "#f4f5ff")
            px(draw, 218 - speed % 80, 48, 27, 13, "#ff6e38")
            px(draw, 224 - speed % 80, 61, 10, 16, "#ffd45f")
        elif landmark_name == "earth":
            px(draw, 220 - speed % 30, 22, 38, 38, INK)
            px(draw, 223 - speed % 30, 25, 32, 32, "#5eb9ff")
            px(draw, 228 - speed % 30, 32, 10, 7, "#64d56f")
            px(draw, 241 - speed % 30, 42, 11, 7, "#64d56f")

    def ground(draw: ImageDraw.ImageDraw, offset: int) -> None:
        px(draw, 0, 148, 320, 32, data["dirt"])
        px(draw, 0, 140, 320, 13, INK)
        px(draw, 0, 135, 320, 14, data["ground"])
        for x in range(-40 - offset % 32, 360, 32):
            px(draw, x, 141, 20, 4, "#9f7b4d")
            px(draw, x + 22, 141, 16, 4, "#9f7b4d")
            px(draw, x + 2, 148, 5, 17, INK)
            px(draw, x + 3, 148, 3, 15, "#6b4b34")
        px(draw, 0, 143, 320, 3, data["rail"])
        px(draw, 0, 152, 320, 3, data["rail"])
        for x in range(-20 - offset % 18, 340, 18):
            px(draw, x, 142, 5, 14, "#2b202a")

    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        sky_fill(draw)
        offset = i * 16
        if destination in {"space", "moon"}:
            stars(draw, offset)
        else:
            clouds(draw, offset if action == "cloud_drift" else 0)
        if action in {"parallax_far", "parallax_mid", "parallax_near"}:
            landmark(draw, offset, action)
        else:
            landmark(draw, offset // 2, "parallax_far")
            landmark(draw, offset, "parallax_mid")
            landmark(draw, offset * 2, "parallax_near")
        ground(draw, offset if action in {"rail_scroll", "full_scroll"} else 0)
        if action == "arrival_flash":
            px(draw, 0, 0, 320, 180, "#ffffff")
            draw.rectangle((0, 0, 319, 179), outline=rgba(PORTALS.get(destination, "#ffffff")), width=5)
        if action == "danger_shake":
            px(draw, 0, 0, 320, 180, "#ff6e7d")

    return drawer


def draw_smoke(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    drift = i * 3
    color = "#e9eef2" if action != "fade" else "#aeb5ae"
    px(draw, 26 - drift, 18 - i, 9 + i, 6 + i, color)
    px(draw, 16 - drift, 12 - i, 12 + i, 8 + i, color)
    px(draw, 5 - drift, 18, 10, 6, "#c6d3dc")
    if action == "burst":
        px(draw, 38 - drift, 11, 13, 10, "#f4f5ff")


def draw_ui_heart(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    filled = action not in {"empty", "lose_3"}
    color = "#ff4d6d" if filled else "#4c4057"
    if action == "gain":
        color = "#ff8bad" if i % 2 else "#ff4d6d"
    if action == "lose":
        color = "#4c4057" if i > 1 else "#ff4d6d"
    px(draw, 7, 9 - (1 if action == "pulse" and i % 2 else 0), 8, 8, INK)
    px(draw, 17, 9 - (1 if action == "pulse" and i % 2 else 0), 8, 8, INK)
    px(draw, 5, 13, 22, 10, INK)
    px(draw, 9, 11, 6, 6, color)
    px(draw, 17, 11, 6, 6, color)
    px(draw, 7, 15, 18, 7, color)
    px(draw, 11, 22, 10, 5, color)


def draw_ui_meter(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    px(draw, 1, 1, 62, 22, INK)
    px(draw, 3, 3, 58, 18, "#251c31")
    if action == "whistle":
        draw_collectible("gold_whistle")(draw, "spin", i)
        px(draw, 32, 8, 18, 7, GOLD)
    elif action == "bone":
        draw_collectible("silver_bone")(draw, "spin", i)
        px(draw, 32, 8, 18, 7, "#dbe8f2")
    elif action == "coin":
        px(draw, 7 + i % 2, 5, 16, 16, GOLD)
        px(draw, 31, 8, 20, 7, GOLD)
    elif action == "space_button":
        y = 5 + (2 if i % 2 else 0)
        px(draw, 10, y, 44, 14, GOLD)
        px(draw, 14, y + 5, 36, 4, INK)
    elif action == "route_marker":
        px(draw, 25, 4, 14, 14, GOLD if i % 2 else "#4c4057")
        px(draw, 5, 16, 54, 3, "#9f7b4d")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "traindog-spritesheet-manifest/v1",
        "pixelScale": 1,
        "sheets": {},
    }

    manifest["sheets"]["train_dog"] = save_sheet(
        "train_dog",
        92,
        58,
        ["idle", "move", "jump", "land", "duck", "hurt", "cheer", "board"],
        draw_train,
    )

    for passenger in PASSENGERS:
        manifest["sheets"][f"passenger_{passenger}"] = save_sheet(
            f"passenger_{passenger}",
            44,
            50,
            ["idle", "walk", "wave", "board", "cheer"],
            draw_passenger(passenger),
        )

    for collectible in ["gold_whistle", "silver_bone", "rainbow_ticket", "star_coin"]:
        manifest["sheets"][f"collectible_{collectible}"] = save_sheet(
            f"collectible_{collectible}",
            30,
            28,
            ["idle", "spin", "sparkle", "collect"],
            draw_collectible(collectible),
        )

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
        manifest["sheets"][f"hazard_{hazard}"] = save_sheet(
            f"hazard_{hazard}",
            40,
            40,
            ["idle", "warning", "active", "broken"],
            draw_hazard(hazard),
        )

    for destination, color in PORTALS.items():
        manifest["sheets"][f"portal_{destination}"] = save_sheet(
            f"portal_{destination}",
            56,
            70,
            ["closed", "idle", "open", "activate"],
            draw_portal(color),
        )

    tile_actions = [
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
    ]
    manifest["sheets"]["terrain_tiles"] = save_sheet("terrain_tiles", 32, 32, tile_actions, draw_tile)

    for destination in PORTALS:
        manifest["sheets"][f"destination_{destination}"] = save_sheet(
            f"destination_{destination}",
            48,
            32,
            ["idle", "selected", "complete"],
            draw_destination_icon(destination),
        )

    for destination in DESTINATIONS:
        manifest["sheets"][f"environment_{destination}"] = save_sheet(
            f"environment_{destination}",
            320,
            180,
            ["cloud_drift", "parallax_far", "parallax_mid", "parallax_near", "rail_scroll", "full_scroll", "arrival_flash", "danger_shake"],
            draw_environment_scene(destination),
            frames_per_action=4,
        )

    manifest["sheets"]["fx_smoke"] = save_sheet("fx_smoke", 64, 40, ["puff", "burst", "fade"], draw_smoke)
    manifest["sheets"]["ui_hearts"] = save_sheet("ui_hearts", 32, 32, ["full", "empty", "pulse", "gain", "lose"], draw_ui_heart)
    manifest["sheets"]["ui_meters"] = save_sheet(
        "ui_meters",
        64,
        24,
        ["whistle", "bone", "coin", "space_button", "route_marker"],
        draw_ui_meter,
    )

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(manifest['sheets'])} sprite sheets to {OUT}")


if __name__ == "__main__":
    main()
