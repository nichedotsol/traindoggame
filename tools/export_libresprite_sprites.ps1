param(
  [string]$LibreSpriteExe = $env:LIBRESPRITE_EXE,
  [string]$SourceRoot = "assets\libresprite",
  [string]$OutputRoot = "assets\love_sprites"
)

$ErrorActionPreference = "Stop"

if (-not $LibreSpriteExe) {
  $cmd = Get-Command libresprite -ErrorAction SilentlyContinue
  if ($cmd) {
    $LibreSpriteExe = $cmd.Source
  }
}

if (-not $LibreSpriteExe) {
  $knownLocalInstall = "C:\Users\ball1\Documents\Codex\libresprite-development-windows-x86_64\libresprite.exe"
  if (Test-Path -LiteralPath $knownLocalInstall) {
    $LibreSpriteExe = $knownLocalInstall
  }
}

if (-not $LibreSpriteExe -or -not (Test-Path -LiteralPath $LibreSpriteExe)) {
  throw "LibreSprite executable not found. Set LIBRESPRITE_EXE to the full path of libresprite.exe, then rerun this script."
}

$sourcePath = Resolve-Path -LiteralPath $SourceRoot
$outputPath = Resolve-Path -LiteralPath $OutputRoot
$files = Get-ChildItem -LiteralPath $sourcePath.Path -Recurse -File |
  Where-Object { $_.Extension -in ".ase", ".aseprite" }

if (-not $files) {
  Write-Host "No LibreSprite source files found under $($sourcePath.Path)."
  exit 0
}

foreach ($file in $files) {
  $pngName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name) + ".png"
  $dest = Join-Path $outputPath.Path $pngName
  & $LibreSpriteExe -b $file.FullName --sheet $dest --sheet-type horizontal --merge-duplicates
  if ($LASTEXITCODE -ne 0) {
    throw "LibreSprite export failed for $($file.FullName)"
  }
  Write-Host "Exported $pngName"
}
