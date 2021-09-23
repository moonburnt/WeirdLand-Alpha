from WGF import Scene, game, RGB, base, shared, tree, clock
from Game import entities
from pygame import sprite, transform, Surface
import logging

log = logging.getLogger(__name__)

# Scene blueprint
sc = Scene("intro")


@sc.initmethod
def init():
    sc.background = Surface(game.screen.get_size()).convert()
    sc.background.fill(RGB(255, 255, 255))


@sc.showmethod
def show():
    # Setting up text, text's antialias and its position on screen
    text = shared.font.render("Hello, World", False, (10, 10, 10))
    # Getting text's rectangle - local version of node - to drag/resize item
    textpos = text.get_rect()
    # This will set position to be the same as screen's center
    textpos.centerx = sc.background.get_rect().centerx
    textpos.centery = sc.background.get_rect().centery
    sc.background.blit(text, textpos)

    # Hiding game's mouse
    game.mouse.set_visible(False)

    # Wipe out whats already visible with background
    game.screen.blit(sc.background, (0, 0))

    # Scheduling logo scene to auto skip to next one in 3 seconds
    sc.time = 3000


@sc.updatemethod
def updater():
    for event in game.event_handler.events:
        if event.type == base.pgl.MOUSEBUTTONDOWN:
            game.tree.switch("level")
            return

    game.screen.blit(sc.background, (0, 0))

    sc.time -= clock.get_time()
    if sc.time > 0:
        return

    game.tree.switch("level")
