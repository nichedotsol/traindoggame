# TrainDog: Moon Line

A LÖVE2D pixel-art side-scroller starring TrainDog, a golden retriever steam locomotive. Press Space to choo, jump, collect whistles, greet passengers, dodge destination hazards, and ride through world stops until the final stop on the moon.

## Play

Install [LÖVE2D](https://love2d.org/), then run this repository folder:

```powershell
love .
```

Controls:

- `Space`: choo / jump
- `Down` or `S`: duck
- `R`: restart
- `Escape`: quit

## Project Structure

- `main.lua`: LÖVE2D game loop
- `conf.lua`: LÖVE2D window/app config
- `src/atlas.lua`: sprite sheet loader and animation helper
- `src/world.lua`: destination, passenger, and hazard data
- `assets/love_sprites/`: primary LÖVE2D sprite atlas, with 257 individual PNG sprite sheets
- `assets/love_sprites/manifest.lua`: generated Lua manifest consumed by the game
- `tools/build_love_sprites.py`: regenerates the LÖVE2D sprite atlas

The old `index.html` browser version remains in the repo only as a static deployment artifact. The LÖVE2D version is the primary game.

## Art

The game uses original code-authored pixel sprites and canvas scenery for every destination, obstacle, NPC, collectible, portal, and TrainDog animation frame. The concept reference is saved at `assets/traindog-concept.png`.

## Sprite Sheets

Full transparent PNG sprite sheets live in `assets/spritesheets/`.

Generate them with:

```powershell
python tools/build_spritesheets.py
```

The generated `assets/spritesheets/manifest.json` lists every sheet, frame size, action row, frame rectangle, and frame duration. It covers TrainDog actions, every passenger action, collectibles, hazards/enemies, destination portals, terrain/prop tiles, route destination icons, environment/parallax shifts, rail movement, smoke, meter icons, and heart gain/loss states.

See `assets/spritesheets/SPRITE_COVERAGE.md` for the complete coverage map.

Generate the primary LÖVE2D sheets with:

```powershell
python tools/build_love_sprites.py
```

The LÖVE2D atlas intentionally uses many individual sheets instead of a few combined panels: every TrainDog action, passenger action, collectible state, hazard state, portal state, environment motion state, route icon state, HUD heart/meter state, terrain variant, and FX state has its own PNG sheet.
