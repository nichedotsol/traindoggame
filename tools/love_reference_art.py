from __future__ import annotations

from typing import Callable

from PIL import ImageDraw

import build_spritesheets as base


INK = "#111018"
INK2 = "#241820"
HI = "#fff0c9"
DOG = "#d7903f"
DOG_MID = "#f0b454"
DOG_HI = "#ffd274"
DOG_DARK = "#9b552f"
PINK = "#f386a4"
PINK_HI = "#ffc0cc"
STEEL = "#25232b"
STEEL2 = "#3b3a42"
STEEL3 = "#5a5c66"
GOLD = "#f7b941"
GOLD_HI = "#ffe483"
WOOD = "#6b4b34"
WOOD_DARK = "#3b2630"
STONE = "#777b95"
STONE_DARK = "#3c4050"


def px(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, color: str) -> None:
    base.px(draw, x, y, w, h, color)


def poly(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], color: str) -> None:
    draw.polygon(points, fill=base.rgba(color))


def line(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], color: str, width: int = 1) -> None:
    draw.line(xy, fill=base.rgba(color), width=width)


def sparkle(draw: ImageDraw.ImageDraw, x: int, y: int, color: str = HI) -> None:
    px(draw, x + 1, y, 1, 5, color)
    px(draw, x, y + 2, 3, 1, color)


def dog_head(draw: ImageDraw.ImageDraw, x: int, y: int, action: str, i: int) -> None:
    blink = action == "hurt" and i % 2 == 0
    tongue = action not in {"duck", "hurt"} or i % 2 == 1

    px(draw, x + 8, y + 5, 34, 29, INK)
    px(draw, x + 5, y + 11, 13, 25, INK)
    px(draw, x + 35, y + 10, 9, 23, INK)
    px(draw, x + 11, y + 7, 28, 24, DOG)
    px(draw, x + 11, y + 8, 18, 9, DOG_MID)
    px(draw, x + 17, y + 6, 13, 5, DOG_HI)
    px(draw, x + 6, y + 13, 10, 22, DOG_DARK)
    px(draw, x + 35, y + 12, 6, 20, DOG_DARK)
    px(draw, x + 38, y + 18, 10, 10, INK)
    px(draw, x + 40, y + 20, 7, 6, "#2b202a")
    px(draw, x + 28, y + 28, 11, 3, INK)
    px(draw, x + 24, y + 31, 10, 3, "#2b202a")
    if blink:
        px(draw, x + 24, y + 18, 7, 2, INK)
    else:
        px(draw, x + 25, y + 17, 4, 4, INK)
        px(draw, x + 26, y + 17, 1, 1, HI)
    if tongue:
        wag = i % 2
        px(draw, x + 34, y + 31, 9, 17 + wag, INK)
        px(draw, x + 35, y + 31, 7, 15 + wag, PINK)
        px(draw, x + 38, y + 33, 2, 8, PINK_HI)
        px(draw, x + 35, y + 46 + wag, 6, 2, INK)


def train_engine(draw: ImageDraw.ImageDraw, y: int, wheel: int, action: str, i: int) -> None:
    px(draw, 3, y + 24, 57, 6, INK)
    px(draw, 7, y + 13, 42, 19, INK)
    px(draw, 11, y + 5, 28, 14, INK)
    px(draw, 14, y + 7, 23, 10, STEEL2)
    px(draw, 9, y + 16, 38, 13, STEEL)
    px(draw, 12, y + 18, 30, 4, STEEL3)
    px(draw, 8, y + 17, 7, 13, "#4b2930")
    px(draw, 12, y + 19, 2, 8, "#68a6b8")
    px(draw, 40, y + 3, 10, 17, INK)
    px(draw, 42, y, 13, 5, STEEL3)
    px(draw, 17, y, 12, 6, INK)
    px(draw, 19, y - 2, 15, 3, STEEL3)
    px(draw, 47, y + 17, 10, 4, "#bd6841")
    px(draw, 57, y + 20, 7, 9, "#7f392e")
    px(draw, 59, y + 22, 5, 6, "#bf5239")
    for n, x in enumerate((9, 22, 36, 49)):
        px(draw, x, y + 29, 11, 11, INK)
        px(draw, x + 2, y + 31, 7, 7, STEEL3)
        px(draw, x + 4 + (wheel + n) % 2, y + 33, 3, 3, "#a7a9b1")
    px(draw, 5, y + 39, 58, 3, INK)
    if action in {"jump", "cheer"}:
        px(draw, 52, y + 39, 12, 3, GOLD)
        px(draw, 62, y + 39, 9, 3, "#ff6e38")
    for n in range(5):
        sx = 31 - n * 8 - i * 2
        sy = y - 8 - (n % 2) * 3
        px(draw, sx, sy, 8 + n, 5 + n % 2, "#e9eef2")
        px(draw, sx + 2, sy + 1, 5 + n, 3, "#ffffff")


def draw_train(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    bounce = {
        "idle": 0,
        "move": -1 if i % 2 == 0 else 0,
        "jump": -7 + i,
        "land": 4 - i,
        "duck": 5,
        "hurt": 1,
        "cheer": -2 if i % 2 else -1,
        "board": 0,
    }[action]
    wheel = i % 3
    train_engine(draw, 15 + bounce, wheel, action, i)
    dog_head(draw, 47, 4 + bounce + (5 if action == "duck" else 0), action, i)
    if action == "cheer":
        sparkle(draw, 81, 5 + i % 2, GOLD_HI)
        px(draw, 76, 10, 8, 6, GOLD)
    if action == "hurt":
        px(draw, 75, 6, 3, 12, "#ff4d6d")
        px(draw, 82, 7, 3, 10, "#ff4d6d")


def draw_heart(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    lift = 1 if action in {"pulse", "gain"} and i % 2 else 0
    color = "#ff4d6d"
    shade = "#b72c4c"
    if action == "empty":
        color, shade = "#4c4057", "#2b2038"
    if action == "lose" and i > 1:
        color, shade = "#4c4057", "#2b2038"
    if action == "gain":
        color = "#ff8bad" if i % 2 else "#ff4d6d"
    px(draw, 7, 8 - lift, 8, 8, INK)
    px(draw, 17, 8 - lift, 8, 8, INK)
    px(draw, 5, 12 - lift, 22, 11, INK)
    px(draw, 9, 10 - lift, 6, 6, color)
    px(draw, 17, 10 - lift, 6, 6, color)
    px(draw, 7, 14 - lift, 18, 7, color)
    px(draw, 10, 21 - lift, 12, 4, color)
    px(draw, 13, 25 - lift, 6, 3, shade)
    px(draw, 10, 12 - lift, 4, 2, "#ffc0cc" if action != "empty" else "#6c6176")
    if action in {"gain", "pulse"}:
        sparkle(draw, 24, 4, HI)


def draw_collectible(kind: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        lift = 2 if action in {"sparkle", "collect"} and i % 2 else 0
        if kind == "gold_whistle":
            px(draw, 4, 10 - lift, 21, 9, INK)
            px(draw, 6, 8 - lift, 16, 9, GOLD)
            px(draw, 8, 7 - lift, 10, 3, GOLD_HI)
            px(draw, 19, 11 - lift, 6, 4, "#d57a22")
            px(draw, 8, 11 - lift, 5, 3, HI)
        elif kind == "silver_bone":
            px(draw, 4, 10 - lift, 22, 7, INK)
            px(draw, 7, 11 - lift, 16, 5, "#dbe8f2")
            for x in (3, 21):
                px(draw, x, 7 - lift, 7, 7, INK)
                px(draw, x + 1, 8 - lift, 5, 5, "#edf8ff")
                px(draw, x, 14 - lift, 7, 6, INK)
                px(draw, x + 1, 14 - lift, 5, 4, "#c1d7e4")
            px(draw, 12, 15 - lift, 9, 2, "#85a6b5")
        elif kind == "rainbow_ticket":
            px(draw, 5, 4 - lift, 21, 18, INK)
            palette = ["#ff4d6d", "#f7b941", "#63d86b", "#58d9e6", "#906cff"]
            for row, color in enumerate(palette):
                px(draw, 7 + i % 2, 6 + row * 3 - lift, 17, 3, color)
            px(draw, 9, 7 - lift, 6, 2, HI)
        elif kind == "star_coin":
            outer = [(15, 3 - lift), (19, 11 - lift), (27, 11 - lift), (21, 16 - lift), (23, 24 - lift), (15, 19 - lift), (7, 24 - lift), (9, 16 - lift), (3, 11 - lift), (11, 11 - lift)]
            inner = [(15, 6 - lift), (18, 12 - lift), (24, 12 - lift), (19, 16 - lift), (20, 21 - lift), (15, 18 - lift), (10, 21 - lift), (11, 16 - lift), (6, 12 - lift), (12, 12 - lift)]
            poly(draw, outer, INK)
            poly(draw, inner, GOLD_HI if i % 2 else GOLD)
            px(draw, 12, 10 - lift, 3, 3, HI)
        if action in {"sparkle", "collect"}:
            sparkle(draw, 24 - i, 3 + i % 2, HI)
            sparkle(draw, 3 + i, 21 - i % 2, GOLD_HI)
    return drawer


PORTAL_COLORS = {
    "forest": ("#46e96f", "#0b5a39"),
    "mountains": ("#45a7ff", "#103c73"),
    "city": ("#b65cff", "#472268"),
    "desert": ("#ff8b26", "#7d301c"),
    "ocean": ("#25e4db", "#0b5f72"),
    "arctic": ("#64f7ff", "#24667f"),
    "space": ("#906cff", "#261064"),
    "moon": ("#f4f5ff", "#555a70"),
}


def draw_portal(destination: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    glow, dark = PORTAL_COLORS[destination]

    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        active = action != "closed"
        px(draw, 5, 16, 46, 47, INK)
        px(draw, 8, 13, 40, 53, STONE_DARK)
        for n in range(5):
            px(draw, 10 + n * 7, 15 + (n % 2) * 2, 6, 8, STONE)
        px(draw, 13, 21, 30, 39, INK)
        if active:
            px(draw, 16, 24, 24, 33, glow)
            px(draw, 19 + i % 2, 27, 18 - i % 2, 27, dark)
            px(draw, 23, 30 + i % 3, 10 + i, 20, glow)
        else:
            px(draw, 16, 24, 24, 33, "#312333")
            px(draw, 20, 28, 16, 25, "#171422")
        px(draw, 14, 9, 28, 8, INK)
        px(draw, 17, 6, 22, 8, STONE)
        px(draw, 2, 62, 52, 6, INK)
        for x in (1, 48):
            px(draw, x, 49, 7, 13, INK)
            px(draw, x + 1, 50, 5, 10, GOLD if active else "#59432b")
            px(draw, x + 2, 51, 2, 4, GOLD_HI if active else "#71543a")
        if action == "activate":
            for x, y in ((4, 8), (48, 11), (44, 28), (9, 34)):
                sparkle(draw, x + i % 2, y, glow)
    return drawer


def draw_forest_environment(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    for y in range(180):
        t = y / 179
        r = round(85 * (1 - t) + 191 * t)
        g = round(181 * (1 - t) + 238 * t)
        b = round(240 * (1 - t) + 255 * t)
        draw.line((0, y, 319, y), fill=(r, g, b, 255))
    offset = i * 16
    for n in range(6):
        x = (n * 72 - offset // 3) % 390 - 55
        y = 20 + (n % 3) * 9
        px(draw, x + 4, y + 9, 42, 7, "#f4f5ff")
        px(draw, x + 16, y + 2, 27, 15, "#ffffff")
        px(draw, x + 38, y + 8, 27, 8, "#e6f7ff")
    for n in range(5):
        x = (n * 78 - offset // 2) % 430 - 70
        poly(draw, [(x + 8, 106), (x + 39, 55), (x + 72, 106)], "#92c7df")
        poly(draw, [(x + 39, 55), (x + 51, 83), (x + 31, 78)], "#f4f5ff")
        poly(draw, [(x + 28, 106), (x + 66, 70), (x + 102, 106)], "#5b8daa")
        poly(draw, [(x + 66, 70), (x + 78, 89), (x + 57, 85)], "#eafcff")
    for layer, color, speed, base_y in ((0, "#3e765d", 1, 124), (1, "#27533f", 2, 136)):
        for n in range(13):
            x = (n * 34 - offset * speed) % 390 - 45
            h = 34 + (n % 4) * 9 + layer * 5
            px(draw, x + 14, base_y - h // 2, 7, h, "#513a26")
            poly(draw, [(x + 17, base_y - h), (x, base_y - h + 25), (x + 34, base_y - h + 25)], color)
            poly(draw, [(x + 17, base_y - h + 12), (x + 2, base_y - h + 38), (x + 32, base_y - h + 38)], "#1f503a" if layer else "#4b8b65")
            px(draw, x + 20, base_y - h + 20, 4, 8, "#6ea876")
    px(draw, 0, 146, 320, 34, "#5b3a25")
    px(draw, 0, 136, 320, 12, INK)
    px(draw, 0, 132, 320, 13, "#5f923f")
    for x in range(-24 - offset % 32, 350, 32):
        px(draw, x, 133, 18, 5, "#82b64d")
        px(draw, x + 16, 136, 12, 4, "#2f704c")
        px(draw, x + 3, 151, 9, 4, "#8b5a37")
        px(draw, x + 18, 161, 8, 4, "#3b2630")
    px(draw, 0, 142, 320, 3, "#1d1b22")
    px(draw, 0, 151, 320, 3, "#1d1b22")
    for x in range(-18 - offset % 20, 340, 20):
        px(draw, x, 140, 5, 16, WOOD_DARK)
        px(draw, x + 1, 141, 3, 14, WOOD)
    if action == "arrival_flash":
        draw.rectangle((0, 0, 319, 179), outline=base.rgba("#46e96f"), width=5)
    if action == "danger_shake":
        draw.rectangle((0, 0, 319, 179), outline=base.rgba("#ff4d6d"), width=4)


def draw_environment(destination: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    if destination == "forest":
        return draw_forest_environment
    return base.draw_environment_scene(destination)


def draw_destination_icon(name: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    base_icon = base.draw_destination_icon(name)

    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        base_icon(draw, action, i)
        if action == "selected":
            draw.rectangle((1, 1, 46, 30), outline=base.rgba(GOLD_HI), width=2)
        if action == "complete":
            sparkle(draw, 39, 4, GOLD_HI)
    return drawer
