# TrainDog: Moon Line

A tiny pixel-art side-scroller starring TrainDog, a golden retriever steam locomotive. Press Space to choo, jump, collect whistles, greet passengers, dodge destination hazards, and ride through world stops until the final stop on the moon.

## Play

Open `index.html` in a browser.

Controls:

- `Space`: choo / jump
- `Down` or `S`: duck
- `R`: restart

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
