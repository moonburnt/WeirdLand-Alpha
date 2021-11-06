from WGF.nodes import VisualNode, Group, Scene, Node, Button, TextNode
from WGF import Point, game, RGB, Size, tree, base, camera, shared
from WGF.tasks import TaskManager, Timer
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
    left = 1
    right = -1
    stop = 0


class GameMode(Enum):
    endless = 0
    time_attack = 1
    survival = 2


class Level(Scene):
    def __init__(self, mode: GameMode, size: Size = Size(2560, 720)):
        shared.bg_size = size
        bg = Surface(shared.bg_size).convert()
        bg.fill(RGB.from_hex("cbdbfc"))
        super().__init__(name="level", background=bg)
        self.mode = mode
        # Initializing per-scene task manager, to avoid issues with spawning things
        # while game is paused
        self.mgr = TaskManager()
        # shared.lvl = self #idk if this makes sense

    def end_level(self):
        shared.leaderboard.add_entry(
            score=shared.score,
            kills=shared.kill_counter,
            # #TODO: add support for customizable player name
            mode=self.mode.name,
        )
        # I should probably restructure this thing #TODO
        try:
            shared.leaderboard.to_file()
        except Exception as e:
            log.warning(f"Unable to save leaderboard: {e}")

        tree["menu_wrapper"].switch("gameover_menu")
        self.stop()
        tree["menu_wrapper"].show()

    def restart(self):
        self.stop()
        self.init()


class Countdown(TextNode):
    def __init__(
        self,
        ms: int,
        timeout_func: callable,
        name: str = "countdown",
        pos=None,
        max_text_len: int = 0,
    ):
        self.time = ms
        self.timer = Timer(self.time)
        self.text_len = max_text_len or len(str(int(ms / 1000)))
        self.timeout_func = timeout_func

        super().__init__(
            name=name,
            text="asda",
            font=shared.font,
            antialiasing=False,
            pos=pos,
        )

    def restart(self):
        self.timer.restart()

    def update(self):
        if self.timer.update():
            self.timeout_func()
            return

        # Yep, this would be tiny bit faster than doing f"{(stuff):.0f}"
        self.text = str(int(self.timer.time_left / 1000)).rjust(self.text_len, "0")
        super().update()


screen_size = game.screen.get_rect()
screen_bottom = screen_size.bottom

sc = Level(mode=GameMode.endless)


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

    if sc.mode is GameMode.time_attack:
        if "lvl_countdown" in sc._children:
            sc["lvl_countdown"].restart()
        else:
            sc["lvl_countdown"] = Countdown(
                ms=30000,
                timeout_func=sc.end_level,
                name="lvl_countdown",
                pos=Point(screen_size.width / 2, 15),
            )
    # This is jank, but will do for now
    else:
        if "lvl_countdown" in sc._children:
            sc._children.pop("lvl_countdown")


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
    unpress_pause()
    if sc.first_run:
        camera.pos.x = -game.screen.get_rect().width / 2
        spawn()
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
