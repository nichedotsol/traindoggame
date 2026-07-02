# TrainDog Pixel Art Direction

The target is the supplied demo image: dense, readable, cheerful arcade pixel
art with strong silhouettes and high material detail.

## Quality Bar

- Characters need large readable heads, expressive poses, and clear action
  changes between frames.
- TrainDog needs believable locomotive mass, wheel motion, smoke, dog-face
  expression, tongue motion, body bounce, and frame-specific recoil.
- Environments need layered parallax: sky, clouds/stars, far landmarks, mid
  silhouettes, near props, rails, ground texture, and destination-specific
  accents.
- HUD elements need jewel-like highlights, dark outlines, and animated state
  changes for gain/loss/pulse.
- Portals need stonework, lamps, flags, animated inner glow, rim light, and
  destination-specific color identity.
- Collectibles need spin/sparkle/collect frames that actually change their
  shape, lighting, or pose.

## Palette Rules

- Use near-black outlines: `#111018`, `#241820`, `#2b202a`.
- Use warm gold highlights for UI and collectibles: `#f7b941`, `#ffe483`.
- Use three to six shades per important material.
- Avoid flat single-color fills except for tiny interior pixels.
- Keep sky and environment colors bright, but keep sprite outlines dark.

## Animation Rules

- Four frames per sheet minimum.
- Each frame must have a visible motion purpose.
- Do not create "same sprite shifted by one pixel" as the only animation.
- Idle frames should breathe, blink, wag, shimmer, or pulse.
- Movement frames should change legs/wheels/smoke/pose, not just position.

## Sheet Priority

1. `character_train_dog_*`
2. `hud_heart_*`, `hud_meter_*`
3. `collectible_*`
4. `portal_*`
5. `environment_forest_*`
6. all passenger characters
7. remaining environments
8. hazards, terrain, FX, route icons
