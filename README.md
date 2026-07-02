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
- `assets/libresprite/`: production source-art workspace for hand-drawn LibreSprite files
- `assets/love_sprites/`: primary LÖVE2D runtime atlas, with 257 individual PNG sprite sheets
- `assets/love_sprites/manifest.lua`: generated Lua manifest consumed by the game
- `tools/export_libresprite_sprites.ps1`: exports LibreSprite `.ase` / `.aseprite` source files into runtime PNG sheets
- `tools/libresprite_manifest_check.py`: reports which manifest sheets still need LibreSprite source art
- `tools/build_love_sprites.py`: regenerates placeholder/runtime LÖVE2D sprite sheets

The old `index.html` browser version remains in the repo only as a static deployment artifact. The LÖVE2D version is the primary game.

## Art

Production-quality art should be hand-drawn in LibreSprite. The generated PNG sheets in `assets/love_sprites/` are runtime exports and placeholders until a matching `.ase` or `.aseprite` source file exists in `assets/libresprite/`.

LibreSprite source filenames must match runtime PNG filenames:

```text
assets/libresprite/characters/character_train_dog_move.aseprite
assets/love_sprites/character_train_dog_move.png
```

See `assets/libresprite/ART_DIRECTION.md` for the pixel-art quality bar.

Export hand-drawn LibreSprite sources into runtime sheets with:

```powershell
$env:LIBRESPRITE_EXE = "C:\path\to\libresprite.exe"
.\tools\export_libresprite_sprites.ps1
```

Check source-art coverage with:

```powershell
python tools/libresprite_manifest_check.py
```

## Sprite Sheets

Legacy browser sprite sheets live in `assets/spritesheets/`.

Generate them with:

```powershell
python tools/build_spritesheets.py
```

The generated `assets/spritesheets/manifest.json` lists every sheet, frame size, action row, frame rectangle, and frame duration. It covers TrainDog actions, every passenger action, collectibles, hazards/enemies, destination portals, terrain/prop tiles, route destination icons, environment/parallax shifts, rail movement, smoke, meter icons, and heart gain/loss states.

See `assets/spritesheets/SPRITE_COVERAGE.md` for the complete coverage map.

Generate placeholder LÖVE2D sheets with:

```powershell
python tools/build_love_sprites.py
```

The LÖVE2D atlas intentionally uses many individual sheets instead of a few combined panels: every TrainDog action, passenger action, collectible state, hazard state, portal state, environment motion state, route icon state, HUD heart/meter state, terrain variant, and FX state has its own PNG sheet.
