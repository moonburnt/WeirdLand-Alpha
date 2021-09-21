from WGF import Scene, game, RGB, base, shared
from WGF.tasks import TaskManager
from Game import entities
from pygame import sprite, transform, Surface
from random import randint
import logging

log = logging.getLogger(__name__)

sc = Scene("level")
# Initializing per-scene task manager, to avoid issues with spawning things while
# game is paused
sc.mgr = TaskManager()


@sc.mgr.timed_task("spawn_enemies", 1000)
def spawn():
    log.debug("Attempting to spawn enemies")
    if sc.enemy_counter <= 10:
        x = game.screen.get_size()[0] - 100

        enemy = entities.Enemy(
            pos=(randint(100, x), 450),
        )
        sc.enemy_storage.append(enemy)
        sc.enemy_counter += 1


@sc.initmethod
def init():
    sc.weapon = entities.Gun()
    # Group of sprites to render together. Later appears above previous
    sc.pointer = sprite.RenderPlain(sc.weapon)
    sc.background = Surface(game.screen.get_size()).convert()
    sc.background.fill(RGB(255, 255, 255))

    sc.enemy_storage = []
    sc.enemy_counter = 0

    # Score is shared property, coz we update it from entity's methods
    shared.score = 0

    spawn()


def remove_dead():
    sc.enemy_storage = [e for e in sc.enemy_storage if e.alive]
    sc.enemy_counter = len(sc.enemy_storage)


def update_enemies():
    remove_dead()
    # spawn()
    sc.enemies = sprite.RenderPlain(sc.enemy_storage)


@sc.showmethod
def show():
    # Setting up text, text's antialias and its position on screen
    text = shared.font.render("Shoot Em All!", False, (10, 10, 10))
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


def update_score():
    text = shared.font.render(f" Score: {shared.score}", False, (10, 10, 10))
    textpos = text.get_rect()
    textpos.topleft = game.screen.get_rect().topleft
    game.screen.blit(text, textpos)


@sc.updatemethod
def updater():
    sc.mgr.update()
    update_enemies()

    for event in game.event_handler.events:
        if event.type == base.pgl.MOUSEBUTTONDOWN:
            sc.weapon.attack(sc.enemy_storage)
        elif event.type == base.pgl.MOUSEBUTTONUP:
            sc.weapon.pullback()

    # Update sprites position
    sc.enemies.update()
    sc.pointer.update()
    # Wipe out whats already visible with background
    game.screen.blit(sc.background, (0, 0))
    # Draw updated sprites on top
    sc.enemies.draw(game.screen)
    sc.pointer.draw(game.screen)
    update_score()
