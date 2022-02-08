# WeirdLand

## Description:

**WeirdLand** is a WIP arcade shooting game, heavily inspired by Moorhuhn. 
Visually, I've tried to recreate the aestetics of NES/SNES-inspired flash/XBLA 
games (hopefully it was somewhat successfull).

## Project Status:

Demo. For now, there are still plenty of things left to implement, but basics are 
kind of there.

## TODO:

- At least 5 enemy types (3 already implemented).
- Random environment events (rare creatures that spawn once in eternity, meteors, 
explosives that can clean whole map, etc).
- Achievements. Well... maybe?
- Native game's binary for windows. Maybe also for mac os.

## Building Game Natively:

*For now, its only possible to create native builds for linux*.

- cd into game's directory
- Create virtual environment inside:
`virtualenv .venv && source .venv/bin/activate`
- Install game's requirements and dev requirements:
`pip install -r requirements.txt && pip install -r dev-requirements.txt`
- Run build.sh:
`chmod +x ./build.sh && ./build.sh`

If everything has went successfully, you will get game's binary in 
**./build/WeirdLand/{name-of-platform}/**

## License:

TODO.

For licenses of media used in this game - check [Assets/license.txt](/Assets/license.txt)
