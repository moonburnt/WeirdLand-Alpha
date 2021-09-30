from WGF import Scene, game, RGB, base, shared, Size, Point
from WGF.tasks import TaskManager
from Game import entities
from pygame import sprite, transform, Surface, key
from random import randint, choice
from enum import Enum
from math import ceil
import logging

log = logging.getLogger(__name__)

# It cant be the same as entity Direction, coz its values are inverted
class CameraDirection(Enum):
    left: int = 1
    right: int = -1
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

    # setup_bg()
    sc.bg_size = Size(2560, 720)
    sc.background = Surface(sc.bg_size).convert()
    # This will be used to calculate maximum allowed camera offset to right
    sc.screen_diff = sc.bg_size.width - game.screen.get_rect().width
    sc.background.fill(RGB.from_hex("cbdbfc"))
    sc.bg_pos = sc.background.get_rect()
    sc.bg_pos.center = game.screen.get_rect().center

    sc.enemy_storage = []
    sc.enemy_counter = 0

    sc.camera_direction = CameraDirection.stop

    # Sharing vars that will be accessed from entity module
    shared.camera_offset = Point(0, 0)
    shared.score = 0
    shared.bg_size = sc.bg_size

    spawn()


def remove_dead():
    sc.enemy_storage = [e for e in sc.enemy_storage if e.alive]
    sc.enemy_counter = len(sc.enemy_storage)


def update_enemies():
    remove_dead()
    sc.enemies = sprite.RenderPlain(sc.enemy_storage)


def fill_bg_horizontally(
    entity, entity_x: int, y: int, entity_kwargs: dict = {}
) -> sprite.RenderPlain:
    amount = ceil(sc.bg_size.width / entity_x)

    items = []
    for pos in range(0, amount):
        x = entity_x * pos
        items.append(entity(Point(x, y), **entity_kwargs))

    return sprite.RenderPlain(items)


def set_environment():
    sc.grass = fill_bg_horizontally(
        entity=entities.Grass,
        entity_x=(64 * 4),  # size*scale
        y=(sc.bg_pos.bottom - 200),
    )

    sc.bg_grass = fill_bg_horizontally(
        entity=entities.Grass,
        entity_x=(64 * 4),
        y=(sc.bg_pos.bottom - 300),
        entity_kwargs={"bg": True},
    )

    sc.mountains = fill_bg_horizontally(
        entity=entities.Mountains,
        entity_x=(256 * 4),
        y=(sc.bg_pos.bottom - 600),
    )


@sc.showmethod
def show():
    set_environment()
    # Setting camera to appear at center of screen on start
    shared.camera_offset.x = -game.screen.get_rect().width / 2


def update_score():
    text = shared.font.render(f" Score: {shared.score}", False, (10, 10, 10))
    textpos = text.get_rect()
    textpos.topleft = game.screen.get_rect().topleft
    game.screen.blit(text, textpos)


def move_cam(direction: CameraDirection):
    dt = game.clock.get_time()
    spd = game.settings["camera_speed"]
    new_x = shared.camera_offset.x + direction.value * spd * dt
    if -sc.screen_diff <= new_x <= 0:
        shared.camera_offset.x = new_x


@sc.updatemethod
def updater():
    for event in game.event_handler.events:
        if event.type == base.pgl.MOUSEBUTTONDOWN:
            sc.weapon.attack(sc.enemy_storage)
        elif event.type == base.pgl.MOUSEBUTTONUP:
            sc.weapon.pullback()

    # Camera controls shenanigans
    right = False
    left = False

    if key.get_pressed()[base.pgl.K_d]:
        right = True
    if key.get_pressed()[base.pgl.K_a]:
        left = True

    if right and not left:
        move_cam(CameraDirection.right)
    elif left and not right:
        move_cam(CameraDirection.left)

    sc.mgr.update()
    update_enemies()

    # Update sprites position
    sc.mountains.update()
    sc.enemies.update()
    sc.pointer.update()
    sc.bg_grass.update()
    sc.grass.update()
    # Wipe out whats already visible with background
    game.screen.blit(sc.background, shared.camera_offset)
    # Draw updated sprites on top
    sc.mountains.draw(game.screen)
    sc.bg_grass.draw(game.screen)
    sc.enemies.draw(game.screen)
    sc.grass.draw(game.screen)
    sc.pointer.draw(game.screen)
    update_score()
