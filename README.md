# WeirdLand

## Description:

**WeirdLand** is a WIP arcade shooting game, heavily inspired by Moorhuhn. 
Visually, I've tried to recreate the aestetics of NES/SNES-inspired flash/XBLA 
games (hopefully it was somewhat successfull).

## Project Status:

Early Alpha. For now, there are still plenty of things left to implement, but 
basics are slowly getting there.

## TODO:

- At least 3 game modes: Time Attack (a.k.a "classic moorhuhn"), Survival (where 
you lose health for each creature that escapes alive) and Endless (the only one, 
somewhat implemented right now).
- At least 5 enemy types (2 already implemented, 3 have sprites drawn).
- Random environment events (rare creatures that spawn once in eternity, meteors, 
explosives that can clean whole map, etc).
- Highscores. I mean - that's the whole point, right?
- Achievements. Well... maybe?
- Native game's binary for windows. Maybe also for mac os.

## Building Game Natively:

*For now, its only possible to create native builds for linux*.

- cd into game's directory
- Create virtual environment inside:
`virtualenv .venv`
- Run build.sh:
`chmod +x ./build.sh && ./build.sh`

If everything has went successfully, you will get game's binary in 
**./build/WeirdLand/{name-of-platform}/**

## License:

I think, for this game I will either go for source-available or copyright, coz I 
don't see any benefits from making its messy code available to public - while I'm 
interested, I'd like to implement things the way I see them. And once I will lose 
interest, it's not like someone would pick things up and continue to add new stuff. 
Or at least thats how I see things for now.

Oh, and while I drew all the sprites, fonts and sounds are creative commons, thus 
by time this game makes it to full release, I'd need to mention their licenses 
and autors somewhere. #TODO
