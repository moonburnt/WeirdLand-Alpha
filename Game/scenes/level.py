from WGF import Scene, game, RGB, base, shared, Size, Point
from WGF.tasks import TaskManager
from Game import entities
from pygame import sprite, transform, Surface
from random import randint, choice
from enum import Enum
from math import ceil
import logging

log = logging.getLogger(__name__)


class MoveCamera(Enum):
    left: int = 10
    right: int = -10
    stop: int = 0


sc = Scene("level")
# Initializing per-scene task manager, to avoid issues with spawning things while
# game is paused
sc.mgr = TaskManager()


@sc.mgr.timed_task("spawn_enemies", 1000)
def spawn():
    log.debug("Attempting to spawn enemies")
    if sc.enemy_counter <= 10:
        pos = Point(
            # This should solve the issue with enemies spawning outside of screen
            randint(0, sc.bg_size.width - 150),
            # #TODO: I should probably make height's offset dynamic, based on
            # window's height - to provide same results with different resolutions
            sc.bg_pos.bottom - 220,
        )
        enemy_type = choice(list(entities.enemies))
        log.debug(f"Spawning {enemy_type} at {pos}")
        enemy = entities.enemies[enemy_type](pos=pos)
        sc.enemy_storage.append(enemy)
        sc.enemy_counter += 1


@sc.initmethod
def init():
    sc.weapon = entities.Gun()
    # Group of sprites to render together. Later appears above previous
    sc.pointer = sprite.RenderPlain(sc.weapon)

    sc.bg_size = Size(2560, 720)
    sc.background = Surface(sc.bg_size).convert()
    # This will be used to calculate maximum allowed camera offset to right
    sc.screen_diff = sc.bg_size.width - game.screen.get_rect().width

    # sc.background.fill(RGB(255, 255, 255))
    sc.background.fill(RGB.from_hex("cbdbfc"))
    sc.bg_pos = sc.background.get_rect()
    sc.bg_pos.center = game.screen.get_rect().center

    sc.enemy_storage = []
    sc.enemy_counter = 0

    sc.camera_direction = MoveCamera.stop

    # Sharing vars that will be accessed from entity module
    shared.camera_offset = Point(0, 0)
    shared.score = 0
    shared.bg_size = sc.bg_size

    spawn()
    move_cam()


def remove_dead():
    sc.enemy_storage = [e for e in sc.enemy_storage if e.alive]
    sc.enemy_counter = len(sc.enemy_storage)


def update_enemies():
    remove_dead()
    # spawn()
    sc.enemies = sprite.RenderPlain(sc.enemy_storage)


def spawn_grass():
    grass_x = 64 * 4  # size*scale
    amount = ceil(sc.bg_size.width / grass_x)
    y = sc.bg_pos.bottom - 200
    bg_y = sc.bg_pos.bottom - 300

    grass = []
    bg_grass = []
    # for y in (sc.bg_pos.bottom - 150, sc.bg_pos.bottom - 120):
    for pos in range(0, amount):
        x = grass_x * pos
        grass.append(entities.Grass(Point(x, y)))
        bg_grass.append(entities.Grass(Point(x, bg_y)))

    sc.grass = sprite.RenderPlain(grass)
    sc.bg_grass = sprite.RenderPlain(bg_grass)


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

    spawn_grass()


def update_score():
    text = shared.font.render(f" Score: {shared.score}", False, (10, 10, 10))
    textpos = text.get_rect()
    textpos.topleft = game.screen.get_rect().topleft
    game.screen.blit(text, textpos)


@sc.mgr.task("move_camera")
def move_cam():
    if sc.camera_direction:
        new_x = shared.camera_offset.x + sc.camera_direction.value
        if -sc.screen_diff <= new_x <= 0:
            shared.camera_offset.x = new_x


@sc.updatemethod
def updater():
    for event in game.event_handler.events:
        if event.type == base.pgl.MOUSEBUTTONDOWN:
            sc.weapon.attack(sc.enemy_storage)
        elif event.type == base.pgl.MOUSEBUTTONUP:
            sc.weapon.pullback()

        if event.type == base.pgl.KEYDOWN:
            if event.key == base.pgl.K_d:
                sc.camera_direction = MoveCamera.right
            elif event.key == base.pgl.K_a:
                sc.camera_direction = MoveCamera.left

        if event.type == base.pgl.KEYUP:
            if event.key == base.pgl.K_d or event.key == base.pgl.K_a:
                sc.camera_direction = MoveCamera.stop

    sc.mgr.update()
    update_enemies()

    # Update sprites position
    sc.enemies.update()
    sc.pointer.update()
    sc.bg_grass.update()
    sc.grass.update()
    # Wipe out whats already visible with background
    game.screen.blit(sc.background, shared.camera_offset)
    # Draw updated sprites on top
    sc.bg_grass.draw(game.screen)
    sc.enemies.draw(game.screen)
    sc.grass.draw(game.screen)
    sc.pointer.draw(game.screen)
    update_score()
