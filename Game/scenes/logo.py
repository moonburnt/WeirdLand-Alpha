from WGF import Scene, game, RGB, base, shared, tree, clock
from Game import entities
from pygame import sprite, transform, Surface
import logging

log = logging.getLogger(__name__)

# Scene blueprint
sc = Scene("intro")


@sc.initmethod
def init():
    # This will load and overwrite "romulus" font in storage
    # Also rescaling font right away
    # shared.font = game.assets.load_font("./Assets/Fonts/romulus.ttf", 36)
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
    # "blit()" is local equal of "render". It will show provided items on screen
    # However there is a huge and important difference between how these work.
    # blit() is kind of low-level stuff that copy one object's pixels on top of
    # another. To drag object around, you'd do that each frame, which is kinda
    # resource-consuming. So yeah - there are "best practices" to how to use it,
    # which I didnt encounter yet
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
            game.tree.switch("intro")
            return
            # sc.weapon.attack(sc.enemy)
        # elif event.type == base.pgl.MOUSEBUTTONUP:
        #    sc.weapon.pullback()

    sc.time -= clock.get_time()
    if sc.time > 0:
        return

    game.tree.switch("intro")

    # Update sprites position
    # sc.sprites.update()
    # Wipe out whats already visible with background
    # game.screen.blit(sc.background, (0, 0))
    # Draw updated sprites on top
    # sc.sprites.draw(game.screen)
