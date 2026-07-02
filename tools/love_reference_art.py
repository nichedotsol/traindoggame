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


PASSENGER_STYLE = {
    "conductor": ("#3157a8", "#1b285b", "#d59a66", "human"),
    "fox_passenger": ("#4da85e", "#d87432", "#d87432", "fox"),
    "rabbit_passenger": ("#f2a5c7", "#f4f5ff", "#f4f5ff", "rabbit"),
    "cool_cat": ("#c7943d", "#29263a", "#7b6b62", "cat"),
    "bear_tourist": ("#bf6b36", "#9b2f29", "#a16b43", "bear"),
    "frog_friend": ("#63b957", "#28613d", "#63b957", "frog"),
    "sheep_hiker": ("#9a9daf", "#f4f5ff", "#d59a66", "sheep"),
    "astronaut": ("#f4f5ff", "#f4f5ff", "#d59a66", "astronaut"),
}


def draw_passenger(kind: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    coat, accent, skin, species = PASSENGER_STYLE[kind]

    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        bob = 1 if action in {"walk", "cheer"} and i % 2 else 0
        x, y = 10, 5 + bob
        arm_y = y + 23 - (5 if action in {"wave", "cheer"} and i % 2 else 0)

        if species == "rabbit":
            px(draw, x + 4, y - 4, 5, 14, INK)
            px(draw, x + 15, y - 4, 5, 14, INK)
            px(draw, x + 5, y - 3, 3, 12, accent)
            px(draw, x + 16, y - 3, 3, 12, accent)
        elif species == "fox":
            poly(draw, [(x + 3, y + 8), (x + 7, y), (x + 11, y + 9)], INK)
            poly(draw, [(x + 17, y + 9), (x + 22, y), (x + 24, y + 11)], INK)
            poly(draw, [(x + 5, y + 7), (x + 8, y + 3), (x + 10, y + 9)], skin)
            poly(draw, [(x + 18, y + 8), (x + 21, y + 3), (x + 22, y + 10)], skin)
        elif species == "cat":
            poly(draw, [(x + 4, y + 8), (x + 7, y + 2), (x + 10, y + 8)], INK)
            poly(draw, [(x + 15, y + 8), (x + 18, y + 2), (x + 21, y + 8)], INK)
        elif species == "frog":
            px(draw, x + 2, y + 4, 8, 8, INK)
            px(draw, x + 17, y + 4, 8, 8, INK)
            px(draw, x + 4, y + 5, 5, 5, skin)
            px(draw, x + 18, y + 5, 5, 5, skin)
        elif species == "astronaut":
            px(draw, x + 1, y + 1, 25, 25, INK)
            px(draw, x + 3, y + 3, 21, 21, "#f4f5ff")
            px(draw, x + 6, y + 8, 15, 8, "#76d7ff")
            px(draw, x + 8, y + 9, 10, 2, "#d7fff7")
        elif species == "sheep":
            for sx, sy in [(1, 6), (6, 2), (13, 2), (19, 6), (4, 12), (16, 12)]:
                px(draw, x + sx, y + sy, 7, 7, "#f4f5ff")

        if species != "astronaut":
            px(draw, x + 4, y + 7, 20, 17, INK)
            px(draw, x + 6, y + 8, 16, 14, skin)
            px(draw, x + 8, y + 12, 3, 3, INK)
            px(draw, x + 17, y + 12, 3, 3, INK)
            px(draw, x + 11, y + 18, 7, 2, INK)
            px(draw, x + 8, y + 9, 9, 3, "#ffd6a1" if species == "human" else "#ffffff")
        if species == "conductor" or species == "bear":
            px(draw, x + 3, y + 3, 22, 5, INK)
            px(draw, x + 6, y, 15, 6, accent)
        if species == "bear":
            px(draw, x + 3, y + 5, 6, 6, skin)
            px(draw, x + 19, y + 5, 6, 6, skin)

        px(draw, x + 3, y + 25, 22, 17, INK)
        px(draw, x + 6, y + 26, 16, 15, coat)
        px(draw, x + 8, y + 27, 10, 3, "#ffffff" if species == "astronaut" else "#ffc46b")
        leg = 2 if action == "walk" and i % 2 else 0
        px(draw, x + 5, y + 41, 7, 5 + leg, INK)
        px(draw, x + 17, y + 41, 7, 5 - min(leg, 2), INK)
        px(draw, x - 1, arm_y, 8, 4, INK)
        px(draw, x + 22, arm_y + (3 if action != "wave" else 0), 9, 4, INK)
        px(draw, x + 1, arm_y, 5, 3, skin)
        px(draw, x + 25, arm_y + (3 if action != "wave" else 0), 5, 3, skin)
        if action == "board":
            px(draw, x - 5 + i, y + 34, 11, 8, WOOD_DARK)
            px(draw, x - 3 + i, y + 31, 7, 5, GOLD)
        if action == "cheer":
            sparkle(draw, 3, 8 + i % 2, GOLD_HI)
            sparkle(draw, 36, 10, "#ff8bad")

    return drawer


def draw_hazard(kind: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        hot = action == "active" or (action == "warning" and i % 2 == 0)
        shade = "#ff4d6d" if hot else "#ffffff"
        broken = action == "broken"
        if kind in {"boulder", "pine_rock", "snow_boulder"}:
            c1 = "#dfeeff" if kind == "snow_boulder" else "#7b807d"
            c2 = "#ffffff" if kind == "snow_boulder" else "#aeb5ae"
            poly(draw, [(7, 31), (10, 19), (18, 13), (29, 16), (35, 26), (31, 35), (12, 35)], INK)
            poly(draw, [(10, 30), (13, 21), (19, 16), (28, 18), (32, 26), (29, 32), (13, 32)], c1)
            px(draw, 16, 18, 9, 4, c2)
            px(draw, 23, 26, 6, 3, "#555861")
            if kind == "pine_rock":
                poly(draw, [(20, 7), (9, 21), (31, 21)], "#2f704c")
                px(draw, 18, 18, 5, 11, "#513a26")
            if broken:
                px(draw, 13, 27, 7, 3, INK)
                px(draw, 25, 22, 4, 7, INK)
        elif kind == "spiked_ball":
            px(draw, 19, 3, 3, 32, INK)
            for x, y in [(20, 8), (32, 20), (20, 33), (8, 20)]:
                poly(draw, [(x, y - 4), (x + 4, y), (x, y + 4), (x - 4, y)], shade)
            px(draw, 8, 11, 24, 24, INK)
            px(draw, 11, 14, 18, 18, "#555861")
            px(draw, 14, 16, 7, 4, "#aeb5ae")
        elif kind == "cactus":
            px(draw, 16, 7, 11, 30, INK)
            px(draw, 18, 6, 7, 29, "#2f9d50")
            px(draw, 20, 8, 2, 22, "#63d86b")
            px(draw, 8, 18, 12, 7, INK)
            px(draw, 9, 16, 8, 7, "#2f9d50")
            px(draw, 26, 21, 8, 7, INK)
            px(draw, 26, 19, 6, 7, "#2f9d50")
            if hot:
                px(draw, 14, 8, 3, 3, "#ff8bad")
        elif kind == "crow":
            wing = -3 if i % 2 else 2
            px(draw, 10, 16, 20, 12, INK)
            px(draw, 14, 13, 10, 8, "#20202a")
            poly(draw, [(27, 18), (37, 21), (27, 24)], GOLD)
            poly(draw, [(13, 20), (1, 14 + wing), (12, 25)], "#20202a")
            poly(draw, [(21, 20), (34, 14 - wing), (25, 27)], "#20202a")
            px(draw, 22, 16, 2, 2, "#ffffff")
        elif kind == "lantern":
            px(draw, 18, 3, 4, 30, INK)
            px(draw, 10, 14, 20, 20, INK)
            px(draw, 12, 16, 16, 16, "#7a293b")
            px(draw, 15, 18, 10, 10, "#ffd45f" if hot else "#8b5a37")
            px(draw, 16, 19, 4, 4, HI if hot else "#b17642")
        elif kind == "wave_crate":
            px(draw, 7, 22, 26, 13, INK)
            px(draw, 9, 20, 22, 12, WOOD)
            px(draw, 11, 22, 18, 3, "#c9844a")
            px(draw, 3, 12 - i % 2, 34, 10, INK)
            px(draw, 5, 10 - i % 2, 30, 9, "#58d9e6")
            px(draw, 8, 12 - i % 2, 8, 2, "#d7fff7")
        elif kind == "ice_spike":
            px(draw, 7, 34, 27, 4, INK)
            poly(draw, [(11, 34), (17, 9 - i % 2), (23, 34)], "#eafcff")
            poly(draw, [(18, 34), (27, 3), (34, 34)], "#a7ebff")
            px(draw, 23, 11, 3, 17, "#ffffff")
        elif kind == "meteor":
            poly(draw, [(14 - i, 9), (4 - i * 2, 15), (16 - i, 19)], "#ff6e38")
            poly(draw, [(10 - i, 14), (0 - i * 2, 21), (16 - i, 24)], "#ffd45f")
            px(draw, 15, 12 + i % 2, 18, 18, INK)
            px(draw, 17, 10, 15, 17, "#99614d")
            px(draw, 20, 13, 6, 4, "#c18462")
        elif kind == "crater":
            px(draw, 5, 24, 31, 11, INK)
            px(draw, 8, 21, 25, 11, "#777b95")
            px(draw, 12, 24, 16, 5, "#33384d")
            px(draw, 18, 22, 5, 2, "#b9bbc7")
        if action == "warning":
            px(draw, 3, 3, 4, 10, "#ff4d6d")
            px(draw, 3, 16, 4, 4, "#ff4d6d")
    return drawer


def draw_tile(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    palettes = {
        "grass": ("#5f923f", "#82b64d", "#2f704c"),
        "stone": ("#777b95", "#b9bbc7", "#484b5d"),
        "bush": ("#3e765d", "#6ea876", "#27533f"),
        "rail": (WOOD, GOLD, WOOD_DARK),
        "wood": (WOOD, "#c9844a", WOOD_DARK),
        "water": ("#228f9c", "#58d9e6", "#156373"),
        "sand": ("#e7b15b", "#ffe19a", "#9d5830"),
        "ice": ("#a7ebff", "#ffffff", "#8eb6c4"),
        "flower": ("#63d86b", "#ff8bad", "#2f704c"),
        "mushroom": ("#f4f5ff", "#e0524d", "#8b2b33"),
        "rock": ("#7b807d", "#aeb5ae", "#484b5d"),
        "crate": (WOOD, "#c9844a", WOOD_DARK),
        "barrel": (WOOD, "#d19b57", WOOD_DARK),
        "sign": (WOOD, GOLD, WOOD_DARK),
        "lamp": ("#312333", "#ffd45f", "#8b5a37"),
        "cloud": ("#f4f5ff", "#ffffff", "#dbe8f2"),
    }
    a, b, c = palettes[action]
    px(draw, 2, 24, 28, 6, INK)
    px(draw, 3, 17, 26, 11, a)
    px(draw, 3, 24, 26, 4, c)
    if action in {"grass", "bush"}:
        for x in range(4, 29, 5):
            px(draw, x, 12 + (x + i) % 3, 3, 8, b)
    elif action == "rail":
        px(draw, 0, 11, 32, 4, INK)
        px(draw, 1, 12, 30, 2, GOLD)
        for x in (6, 21):
            px(draw, x, 8, 5, 20, WOOD_DARK)
            px(draw, x + 1, 9, 3, 17, WOOD)
    elif action in {"wood", "crate"}:
        for x in (8, 18):
            px(draw, x, 14, 3, 14, c)
        line(draw, (5, 18, 25, 27), b, 2)
    elif action == "barrel":
        px(draw, 8, 9, 17, 20, INK)
        px(draw, 10, 10, 13, 18, a)
        px(draw, 8, 14, 17, 3, c)
        px(draw, 8, 23, 17, 3, c)
    elif action == "water":
        for x in range(2, 30, 8):
            px(draw, x + i % 3, 13, 6, 2, b)
    elif action == "sand":
        for x, y in [(6, 14), (17, 18), (25, 13)]:
            px(draw, x, y + i % 2, 4, 2, b)
    elif action == "ice":
        poly(draw, [(6, 27), (14, 8), (22, 27)], b)
        poly(draw, [(17, 27), (25, 12), (30, 27)], a)
    elif action == "flower":
        px(draw, 15, 8, 3, 15, c)
        for dx, dy in [(12, 7), (18, 7), (14, 4), (16, 11)]:
            px(draw, dx, dy + i % 2, 5, 5, b)
        px(draw, 16, 8, 2, 2, GOLD)
    elif action == "mushroom":
        px(draw, 14, 14, 5, 13, a)
        px(draw, 9, 8, 15, 9, b)
        px(draw, 12, 10, 3, 3, HI)
    elif action == "rock":
        poly(draw, [(6, 26), (10, 15), (20, 11), (28, 22), (25, 28), (9, 29)], INK)
        poly(draw, [(9, 25), (12, 17), (20, 14), (25, 22), (22, 26), (11, 27)], a)
        px(draw, 14, 16, 7, 3, b)
    elif action == "sign":
        px(draw, 15, 15, 4, 14, c)
        px(draw, 6, 8, 22, 10, INK)
        px(draw, 8, 9, 18, 8, a)
        px(draw, 10, 12, 10, 2, b)
    elif action == "lamp":
        px(draw, 15, 7, 4, 22, a)
        px(draw, 10, 9, 14, 12, INK)
        px(draw, 12, 11, 10, 8, b if i % 2 else c)
    elif action == "cloud":
        px(draw, 2, 15, 28, 9, c)
        px(draw, 7, 10, 13, 11, a)
        px(draw, 17, 12, 10, 9, b)


def draw_smoke(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    drift = i * 6
    colors = ("#ffffff", "#e9eef2", "#c6d3dc") if action != "fade" else ("#c6d3dc", "#9eaab2", "#777b95")
    for n in range(4):
        x = 42 - drift - n * 10
        y = 19 - i - (n % 2) * 5
        px(draw, x, y, 9 + n * 2, 6 + n, colors[min(n, 2)])
        px(draw, x + 2, y + 1, 5 + n, 2, colors[0])
    if action == "burst":
        sparkle(draw, 48 - drift, 8, HI)
        sparkle(draw, 30 - drift, 5, "#ffffff")


def draw_meter(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
    px(draw, 1, 1, 62, 22, INK)
    px(draw, 3, 3, 58, 18, "#251c31")
    px(draw, 4, 4, 56, 2, "#4c4057")
    if action == "whistle":
        draw_collectible("gold_whistle")(draw, "spin", i)
        px(draw, 34, 8, 18, 6, GOLD)
        px(draw, 37, 9, 12, 2, GOLD_HI)
    elif action == "bone":
        draw_collectible("silver_bone")(draw, "spin", i)
        px(draw, 34, 8, 18, 6, "#dbe8f2")
        px(draw, 38, 9, 10, 2, "#ffffff")
    elif action == "coin":
        px(draw, 7 + i % 2, 5, 16, 16, INK)
        px(draw, 9 + i % 2, 7, 12, 12, GOLD)
        px(draw, 12 + i % 2, 8, 5, 2, GOLD_HI)
        px(draw, 31, 8, 21, 7, GOLD)
    elif action == "space_button":
        y = 5 + (2 if i % 2 else 0)
        px(draw, 9, y, 46, 15, INK)
        px(draw, 12, y + 2, 40, 10, GOLD)
        px(draw, 16, y + 6, 31, 3, INK)
    elif action == "route_marker":
        px(draw, 6, 16, 52, 3, "#9f7b4d")
        for n in range(4):
            px(draw, 10 + n * 12, 12, 5, 5, GOLD if (n + i) % 2 == 0 else "#4c4057")


ENV = {
    "forest": {"sky": ("#55b5f0", "#bfeeff"), "far": "#92c7df", "mid": "#3e765d", "near": "#27533f", "ground": "#5f923f", "dirt": "#5b3a25", "kind": "pines"},
    "mountains": {"sky": ("#75c9ff", "#ecfbff"), "far": "#d7eef6", "mid": "#6d92b3", "near": "#314c67", "ground": "#d8f3fa", "dirt": "#7b786f", "kind": "mountains"},
    "city": {"sky": ("#6357be", "#f08aa8"), "far": "#ffc477", "mid": "#372f76", "near": "#1e1941", "ground": "#4e4364", "dirt": "#2b263d", "kind": "city"},
    "desert": {"sky": ("#f4a85e", "#ffe7a5"), "far": "#f7cf78", "mid": "#c67939", "near": "#9d5830", "ground": "#e7b15b", "dirt": "#8d5732", "kind": "dunes"},
    "ocean": {"sky": ("#48b7d9", "#d7fff7"), "far": "#76e0de", "mid": "#228f9c", "near": "#156373", "ground": "#d9ba71", "dirt": "#6c563e", "kind": "lighthouse"},
    "arctic": {"sky": ("#11274e", "#75d8ff"), "far": "#b8fff4", "mid": "#59a5c8", "near": "#1f5f82", "ground": "#d8f7ff", "dirt": "#8eb6c4", "kind": "aurora"},
    "space": {"sky": ("#07071b", "#15124c"), "far": "#45427d", "mid": "#22235b", "near": "#121333", "ground": "#32324f", "dirt": "#17172c", "kind": "space"},
    "moon": {"sky": ("#050511", "#1b1d35"), "far": "#777b95", "mid": "#555a70", "near": "#33384d", "ground": "#b9bbc7", "dirt": "#626676", "kind": "earth"},
}


def gradient(draw: ImageDraw.ImageDraw, top: str, bottom: str) -> None:
    tr, tg, tb, _ = base.rgba(top)
    br, bg, bb, _ = base.rgba(bottom)
    for y in range(180):
        t = y / 179
        draw.line((0, y, 319, y), fill=(round(tr * (1 - t) + br * t), round(tg * (1 - t) + bg * t), round(tb * (1 - t) + bb * t), 255))


def clouds(draw: ImageDraw.ImageDraw, offset: int, night: bool = False) -> None:
    if night:
        for n in range(70):
            x = (n * 41 - offset) % 340
            y = 8 + (n * 23) % 80
            px(draw, x, y, 2 if n % 9 == 0 else 1, 1, "#ffffff")
        return
    for n in range(6):
        x = (n * 72 - offset) % 390 - 55
        y = 18 + (n % 3) * 11
        px(draw, x + 4, y + 9, 42, 7, "#e6f7ff")
        px(draw, x + 16, y + 2, 27, 15, "#ffffff")
        px(draw, x + 38, y + 8, 27, 8, "#f4f5ff")


def landmark(draw: ImageDraw.ImageDraw, data: dict[str, str], offset: int, layer: str) -> None:
    kind = data["kind"]
    color = data[layer]
    speed = {"far": 1, "mid": 2, "near": 3}[layer]
    off = offset * speed
    if kind == "pines":
        for n in range(11):
            x = (n * 38 - off) % 390 - 45
            h = 34 + (n % 4) * 9
            px(draw, x + 14, 126 - h // 2, 7, h, "#513a26")
            poly(draw, [(x + 17, 126 - h), (x, 126 - h + 25), (x + 34, 126 - h + 25)], color)
            poly(draw, [(x + 17, 138 - h), (x + 2, 164 - h), (x + 32, 164 - h)], data["near"])
    elif kind == "mountains":
        for n in range(5):
            x = (n * 80 - off) % 470 - 80
            poly(draw, [(x, 120), (x + 40, 55 + n % 2 * 9), (x + 85, 120)], color)
            poly(draw, [(x + 40, 55 + n % 2 * 9), (x + 53, 84), (x + 30, 78)], "#ffffff")
    elif kind == "city":
        for n in range(16):
            x = (n * 25 - off) % 390 - 30
            h = 23 + (n % 5) * 8
            px(draw, x, 123 - h, 18, h, color)
            px(draw, x + 4, 104 - h, 3, 3, GOLD)
            px(draw, x + 11, 113 - h, 3, 3, "#ff8bad")
    elif kind == "dunes":
        for n in range(6):
            x = (n * 82 - off) % 460 - 80
            poly(draw, [(x, 121), (x + 50, 82), (x + 110, 121)], color)
            line(draw, (x + 34, 99, x + 85, 120), "#ffe19a", 2)
    elif kind == "lighthouse":
        x = 218 - off % 70
        px(draw, 0, 108, 320, 22, data["mid"])
        px(draw, x, 50, 22, 76, INK)
        px(draw, x + 4, 55, 14, 68, "#f4f5ff")
        px(draw, x + 4, 72, 14, 8, "#e0524d")
        px(draw, x + 1, 45, 20, 9, "#e0524d")
        px(draw, x - 22, 54, 62, 4, "#ffe483")
    elif kind == "aurora":
        for x, c in [(32, "#63e6a8"), (70, "#78d3ff"), (112, "#9cffd9"), (222, "#63e6a8")]:
            px(draw, x + off % 18, 16, 15, 78, c)
            px(draw, x + 5 + off % 18, 16, 5, 78, "#ffffff")
    elif kind == "space":
        for n in range(5):
            x = (n * 82 - off) % 420 - 40
            px(draw, x + 18, 20, 7, 22, "#f4f5ff")
            px(draw, x + 13, 39, 18, 8, "#ff6e38")
            px(draw, x + 17, 47, 10, 14, "#ffd45f")
            px(draw, x, 65, 18, 18, "#45427d")
    elif kind == "earth":
        x = 226 - off % 35
        px(draw, x, 20, 39, 39, INK)
        px(draw, x + 3, 23, 33, 33, "#5eb9ff")
        px(draw, x + 8, 30, 10, 7, "#64d56f")
        px(draw, x + 22, 41, 11, 7, "#64d56f")


def draw_ground(draw: ImageDraw.ImageDraw, data: dict[str, str], offset: int) -> None:
    px(draw, 0, 146, 320, 34, data["dirt"])
    px(draw, 0, 136, 320, 12, INK)
    px(draw, 0, 132, 320, 13, data["ground"])
    for x in range(-24 - offset % 32, 350, 32):
        px(draw, x, 133, 18, 5, "#ffffff" if data["kind"] in {"mountains", "arctic", "moon"} else "#82b64d")
        px(draw, x + 3, 151, 9, 4, "#8b5a37")
        px(draw, x + 18, 161, 8, 4, "#3b2630")
    px(draw, 0, 142, 320, 3, "#1d1b22")
    px(draw, 0, 151, 320, 3, "#1d1b22")
    for x in range(-18 - offset % 20, 340, 20):
        px(draw, x, 140, 5, 16, WOOD_DARK)
        px(draw, x + 1, 141, 3, 14, WOOD)


def draw_environment(destination: str) -> Callable[[ImageDraw.ImageDraw, str, int], None]:
    data = ENV[destination]

    def drawer(draw: ImageDraw.ImageDraw, action: str, i: int) -> None:
        offset = i * 16
        gradient(draw, data["sky"][0], data["sky"][1])
        clouds(draw, offset if action == "cloud_drift" else 0, destination in {"space", "moon", "arctic"})
        if action in {"parallax_far", "parallax_mid", "parallax_near"}:
            landmark(draw, data, offset, action.split("_")[-1])
        else:
            landmark(draw, data, offset // 2, "far")
            landmark(draw, data, offset, "mid")
            landmark(draw, data, offset * 2, "near")
        draw_ground(draw, data, offset if action in {"rail_scroll", "full_scroll"} else 0)
        if action == "arrival_flash":
            draw.rectangle((0, 0, 319, 179), outline=base.rgba(PORTAL_COLORS.get(destination, ("#ffffff",))[0]), width=5)
        if action == "danger_shake":
            draw.rectangle((0, 0, 319, 179), outline=base.rgba("#ff4d6d"), width=4)

    return drawer
