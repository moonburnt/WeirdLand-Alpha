from WGF.nodes import VisualNode, Group, Scene, Node, Button
from WGF import Point, game, RGB, Size, tree, base, camera, shared
from WGF.tasks import TaskManager
from Game.entities import enemies, Grass, Mountains, Gun, MousePointer
from pygame import Surface, key
from random import choice, randint
from enum import Enum
from math import ceil
from Game.scenes import ingame_ui
from Game import ui
import logging

log = logging.getLogger(__name__)

# It cant be the same as entity Direction, coz its values are inverted
class CameraDirection(Enum):
    left: int = 1
    right: int = -1
    stop: int = 0


# Level wrapper, to which both scene layout and pause menu will be attached
# level = Node(name="level")

shared.bg_size = Size(2560, 720)
bg = Surface(shared.bg_size).convert()
bg.fill(RGB.from_hex("cbdbfc"))

screen_size = game.screen.get_rect()
screen_bottom = screen_size.bottom

sc = Scene(name="level", background=bg)
# Initializing per-scene task manager, to avoid issues with spawning things
# while game is paused
sc.mgr = TaskManager()


@sc.initmethod
def init():
    # This will be used to calculate maximum allowed camera offset to right
    sc.screen_diff = shared.bg_size.width - game.screen.get_rect().width

    # Setting up environment
    lbg = Surface((game.screen.get_size()[0], 300)).convert()
    lbg.fill(RGB.from_hex("5b6ee1"))
    lower_background = VisualNode(
        name="lower_background",
        surface=lbg,
        pos=Point(game.screen.get_size()[0] / 2, game.screen.get_size()[1]),
    )

    front_grass = make_horizontal_filler(
        name="front_grass",
        entity=Grass,
        entity_x=(64 * 4),  # size*scale
        y=screen_bottom - 150,
    )

    back_grass = make_horizontal_filler(
        name="back_grass",
        entity=Grass,
        entity_x=(64 * 4),
        y=screen_bottom - 250,
        entity_kwargs={"bg": True},
    )

    mountains = make_horizontal_filler(
        name="mountains",
        entity=Mountains,
        entity_x=(256 * 4),
        y=(screen_bottom - 450),
    )

    msg = ui.make_text(
        name="encourage_msg",
        text="Shoot Em All!",
        pos=Point(game.screen.get_size()[0] / 2, game.screen.get_size()[1] / 2),
    )

    sc.add_child(mountains)
    sc.add_child(back_grass)
    sc.add_child(lower_background)
    sc.add_child(Group(name="enemies"))
    sc.add_child(front_grass)
    sc.add_child(msg)
    sc.add_child(Gun())

    # Sharing vars that will be accessed from entity module
    shared.score = 0
    shared.kill_counter = 0

    sc.add_child(ingame_ui.hud)

    sc.enemy_counter = 0
    sc.enemy_storage = []

    sc.bullets_amount = 7
    for _, bullet in sc["player_hud"]["bullets"]:
        bullet.show()

    sc.reloading = False
    sc.first_run = True
    shared.pause_button_pressed = False


@sc.mgr.timed_task("spawn_enemies", 1000)
def spawn():
    # log.debug("Attempting to spawn enemies")
    if sc.enemy_counter <= 10:
        pos = Point(
            # This should solve the issue with enemies spawning outside of screen
            randint(0, shared.bg_size.width - 150),
            # #TODO: I should probably make height's offset dynamic, based on
            # window's height - to provide same results with different resolutions
            screen_bottom - 220,
        )
        enemy_type = choice(list(enemies))
        log.debug(f"Spawning {enemy_type} at {pos}")
        enemy = enemies[enemy_type](pos=pos)
        sc["enemies"].add_child(enemy)
        sc.enemy_counter += 1


def make_horizontal_filler(
    name: str, entity: VisualNode, entity_x: int, y: int, entity_kwargs: dict = {}
) -> Group:
    # its +1 now, since center of node has been moved from top left to center
    amount = ceil(shared.bg_size.width / entity_x) + 1

    items = Group(name=name)
    for pos in range(0, amount):
        x = entity_x * pos
        items.add_child(entity(Point(x, y), **entity_kwargs))

    return items


@sc.mgr.do_later(ms=1000)
def hide_msg():
    sc["encourage_msg"].hide()


# This has to be done with small pause, to make engine process it and avoid endless
# loop between pause menu and level
@sc.mgr.do_later(ms=10)
def unpress_pause():
    if shared.pause_button_pressed:
        shared.pause_button_pressed = False


@sc.showmethod
def show():
    camera.pos.x = -game.screen.get_rect().width / 2
    spawn()
    unpress_pause()
    if sc.first_run:
        sc["encourage_msg"].show()
        hide_msg()
        sc.first_run = False


def move_cam(direction: CameraDirection):
    dt = game.clock.get_time()
    spd = game.settings["camera_speed"]
    new_x = camera.pos.x + direction.value * spd * dt
    if -sc.screen_diff <= new_x <= 0:
        camera.pos.x = new_x


def remove_dead():
    for k, v in tuple(sc["enemies"]):
        if v.remove:
            del sc["enemies"][k]
    sc.enemy_storage = [i for i in sc["enemies"].children if i.alive]
    sc.enemy_counter = len(sc.enemy_storage)


@sc.mgr.do_later(1000)
def do_reload():
    for _, bullet in sc["player_hud"]["bullets"]:
        bullet.show()
    sc.bullets_amount = 7
    sc.reloading = False


def reload():
    log.debug("Reloading a gun")
    sc.reloading = True
    game.assets.sounds["reload"].play()
    do_reload()


def attack():
    if sc.reloading:
        # game.assets.sounds["busy"].play()
        return

    if sc.bullets_amount > 0:
        sc.bullets_amount -= 1
        sc["player_hud"]["bullets"][f"bullets_{sc.bullets_amount}"].hide()
        sc["gun"].attack(sc.enemy_storage)
    else:
        reload()


@sc.updatemethod
def updater():
    for event in game.event_handler.events:
        # excessive press check is there to avoid looping between pause menu and
        # game while P is held
        # #TODO: maybe move this check to pause menu, since it should only be in
        # one place, and level's updater is already loaded with stuff to do?
        if (
            not shared.pause_button_pressed
            and event.type == base.pgl.KEYDOWN
            and event.key == base.pgl.K_p
        ):
            tree["menu_wrapper"].switch("pause_menu")
            sc.hide()
            shared.game_paused = True
            shared.pause_button_pressed = True
            tree["menu_wrapper"].show()
        elif event.type == base.pgl.KEYUP and event.key == base.pgl.K_p:
            shared.pause_button_pressed = False

        if (
            not sc.reloading
            and event.type == base.pgl.KEYDOWN
            and event.key == base.pgl.K_r
        ):
            reload()

        if event.type == base.pgl.MOUSEBUTTONDOWN and event.button == 1:
            attack()
        elif event.type == base.pgl.MOUSEBUTTONUP and event.button == 1:
            sc["gun"].pullback()

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

    remove_dead()
