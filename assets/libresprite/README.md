# TrainDog LibreSprite Source Art

This folder is the master art workspace for TrainDog.

The PNG files in `assets/love_sprites/` are runtime exports. They are not the
master artwork once a LibreSprite source exists for a sheet.

LibreSprite source files should use `.ase` or `.aseprite`; LibreSprite supports
the Aseprite-era file format.

## Required Standard

Every production sprite sheet should be drawn in LibreSprite with:

- one source file per subject/action sheet
- four animation frames arranged horizontally
- the same frame dimensions declared in `assets/love_sprites/manifest.lua`
- nearest-neighbor pixel art only
- visible dark outlines, clustered shading, and material-specific highlight ramps
- no AI-smoothed, scaled, blurred, or antialiased source pixels

## Folder Layout

```text
assets/libresprite/
  characters/
  collectibles/
  environments/
  fx/
  hazards/
  hud/
  portals/
  route_icons/
  terrain/
```

## Export Rule

Use `tools/export_libresprite_sprites.ps1` to export `.ase` and `.aseprite`
files into `assets/love_sprites/`.

The source filename must match the runtime PNG filename:

```text
assets/libresprite/characters/character_train_dog_move.aseprite
assets/love_sprites/character_train_dog_move.png
```

Until a matching LibreSprite source file exists, the PNG is still a placeholder.
