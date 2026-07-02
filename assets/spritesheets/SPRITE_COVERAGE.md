# Sprite Sheet Coverage

This directory contains the older browser-runtime sprite sheets plus `manifest.json`.

The primary LÖVE2D revamp uses `assets/love_sprites/`, which contains 257 individual PNG sprite sheets and its own `manifest.lua`.

## Browser Runtime Sheets

- `train_dog.png`: idle, move, jump, land, duck, hurt, cheer, board
- `passenger_*.png`: idle, walk, wave, board, cheer for conductor, fox, rabbit, cat, bear, frog, sheep, and astronaut passengers
- `collectible_*.png`: idle, spin, sparkle, collect
- `hazard_*.png`: idle, warning, active, broken
- `portal_*.png`: closed, idle, open, activate
- `environment_*.png`: cloud drift, parallax far, parallax mid, parallax near, rail scroll, full scroll, arrival flash, danger shake
- `ui_hearts.png`: full, empty, pulse, gain, lose
- `ui_meters.png`: whistle, bone, coin, space button, route marker
- `fx_smoke.png`: puff, burst, fade
- `terrain_tiles.png`: terrain and prop variants
- `destination_*.png`: idle, selected, complete

No demo-crop sheets are part of the current atlas.
