# WeirdLand

[![Build](https://github.com/moonburnt/WeirdLand/actions/workflows/build.yml/badge.svg)](https://github.com/moonburnt/WeirdLand/actions/workflows/build.yml)

## Description:

**WeirdLand** is a WIP arcade shooting game, heavily inspired by Moorhuhn.
Visually, I've tried to recreate the aestetics of NES/SNES-inspired flash/XBLA
games (hopefully it was somewhat successfull).

## Project Status:

Demo. For now, there are still plenty of things left to implement, but basics are
kind of there.

## Gameplay Preview:

[Gameplay Video](https://user-images.githubusercontent.com/52989889/153038045-c25038f2-1993-4e57-9014-8efdfa268f62.mp4)

## TODO:

- At least 5 enemy types (3 already implemented).
- Random environment events (rare creatures that spawn once in eternity, meteors,
explosives that can clean whole map, etc).
- Achievements. Well... maybe?

## Building Game Natively:

*For now, its only possible to create native builds for linux*.

- cd into game's directory
- Create virtual environment inside:
`virtualenv .venv && source .venv/bin/activate`
- Run build.sh:
`chmod +x ./build.sh && ./build.sh`

If everything has went successfully, you will get game's binary in
**./build/WeirdLand/{name-of-platform}/**

## License:

[GPLv3](LICENSE)

For licenses of media used in this game - check [Assets/license.txt](/Assets/license.txt)
