from WGF.nodes import Scene, Button, Node, VisualNode
from WGF import Point, game, tree, RGB, base, task_mgr, shared
from pygame import Surface
from Game.entities import MousePointer
from Game.ui import make_button, make_text
import logging

log = logging.getLogger(__name__)

bg = Surface(game.screen.get_size()).convert()
bg.fill(RGB.from_hex("cbdbfc"))
gr = game.screen.get_rect()

mm_wrapper = Scene(name="menu_wrapper", background=bg)

main_menu = Node(name="main_menu")


def switch(name: str):
    for menu in mm_wrapper.menus:
        menu.hide()
    mm_wrapper[name].show()


mm_wrapper.switch = switch


@main_menu.initmethod
def init_mm():
    play_button = make_button(
        name="play_button",
        text="Play",
        pos=Point(gr.centerx, gr.centery),
    )

    @play_button.clickmethod
    def play():
        log.debug("Selecting game mode")
        mm_wrapper.switch("mode_selection")

    options_button = make_button(
        name="options_button",
        text="Options",
        pos=Point(gr.centerx, gr.centery + 30),
        active=False,
    )

    score_button = make_button(
        name="score_button",
        text="High Scores",
        pos=Point(gr.centerx, gr.centery + 60),
        active=False,
    )

    exit_button = make_button(
        name="exit_button",
        text="Exit",
        pos=Point(gr.centerx, gr.centery + 90),
    )

    @exit_button.clickmethod
    def exit():
        game.active = False

    for button in (play_button, options_button, score_button, exit_button):
        main_menu.add_child(button)

    @main_menu.showmethod
    def show_mm():
        mm_wrapper.buttons = tuple(x for x in main_menu.children if type(x) is Button)


mode_selection = Node(name="mode_selection")


@mode_selection.initmethod
def init_mm():
    ms_title = make_text(
        name="ms_title",
        text="Select Gamemode",
        pos=Point(gr.centerx, gr.centery - 70),
    )

    # #Not implemented yet #TODO
    ta_button = make_button(
        name="ta_button",
        text="Time Attack",
        pos=Point(gr.centerx, gr.centery),
        active=False,
    )

    # #Not implemented yet #TODO
    surv_button = make_button(
        name="surv_button",
        text="Survival",
        pos=Point(gr.centerx, gr.centery + 30),
        active=False,
    )

    en_button = make_button(
        name="en_button",
        text="Endless",
        pos=Point(gr.centerx, gr.centery + 60),
    )

    @en_button.clickmethod
    def play():
        log.debug("Switching to level")
        tree["level"].init()
        tree["menu_wrapper"].hide()
        tree["level"].show()

    back_button = make_button(
        name="back_button",
        text="Back to Menu",
        pos=Point(gr.centerx, gr.centery + 130),
    )

    @back_button.clickmethod
    def back():
        log.debug("Switching to menu")
        mm_wrapper.switch("main_menu")

    for item in (ms_title, ta_button, surv_button, en_button, back_button):
        mode_selection.add_child(item)

    @mode_selection.showmethod
    def show_ms():
        mm_wrapper.buttons = tuple(
            x for x in mode_selection.children if type(x) is Button
        )


pause_menu = Node(name="pause_menu")


@pause_menu.initmethod
def init_pause():
    pause_title = make_text(
        name="pause_msg",
        text="Game Paused",
        pos=Point(gr.centerx, gr.centery - 70),
    )

    def continue_game():
        tree["menu_wrapper"].hide()
        shared.game_paused = False
        tree["level"].show()

    continue_button = make_button(
        name="continue_button",
        text="Continue",
        pos=Point(gr.centerx, gr.centery),
        clickmethod=continue_game,
    )

    giveup_button = make_button(
        name="giveup_button",
        text="Give Up",
        pos=Point(gr.centerx, gr.centery + 30),
    )

    @giveup_button.clickmethod
    def giveup():
        tree["menu_wrapper"].switch("gameover_menu")

    for item in (pause_title, continue_button, giveup_button):
        pause_menu.add_child(item)

    @pause_menu.showmethod
    def show_pause():
        mm_wrapper.buttons = tuple(x for x in pause_menu.children if type(x) is Button)

    @pause_menu.updatemethod
    def update_pause():
        for event in game.event_handler.events:
            if event.type == base.pgl.KEYDOWN and event.key == base.pgl.K_p:
                continue_game()


gameover_menu = Node(name="gameover_menu")


@gameover_menu.initmethod
def configure_gameover():
    go_title = make_text(
        name="go_title",
        text="Game Over",
        pos=Point(gr.centerx, gr.centery - 70),
    )

    restart_button = make_button(
        name="restart_button",
        text="Restart",
        pos=Point(gr.centerx, gr.centery),
        active=False,
    )

    lb_button = make_button(
        name="lb_button",
        text="High Scores",
        pos=Point(gr.centerx, gr.centery + 30),
        active=False,
    )

    exit_button = make_button(
        name="exit_button",
        text="Back to Menu",
        pos=Point(gr.centerx, gr.centery + 60),
    )

    @exit_button.clickmethod
    def exit_level():
        log.debug("Switching to main menu")
        tree["level"].stop()
        tree["menu_wrapper"].switch("main_menu")

    for item in (go_title, restart_button, lb_button, exit_button):
        gameover_menu.add_child(item)

    @gameover_menu.showmethod
    def show_gameover():
        mm_wrapper.buttons = tuple(
            x for x in gameover_menu.children if type(x) is Button
        )


@mm_wrapper.showmethod
def show():
    # Doing things like that, coz otherwise we could accidently exit game right
    # away, on clicking (during logo) on the same place as exit button
    @mm_wrapper.updatemethod
    @task_mgr.do_later(ms=300)
    def update():
        for event in game.event_handler.events:
            if event.type == base.pgl.MOUSEBUTTONDOWN and event.button == 1:
                mm_wrapper["gun"].attack(mm_wrapper.buttons)
            elif event.type == base.pgl.MOUSEBUTTONUP and event.button == 1:
                mm_wrapper["gun"].pullback()


author_txt = make_text(
    name="author_txt",
    text="© moonburnt, 2021",
    pos=Point(gr.centerx, gr.bottom - 50),
)

game_logo = VisualNode(
    name="game_logo",
    surface=game.assets.images["game_logo"],
    pos=Point(gr.centerx, gr.top + 150),
)


def add_submenus(current: str, menus: tuple):
    for menu in menus:
        if menu.name == current:
            mm_wrapper.add_child(menu)
        else:
            mm_wrapper.add_child(menu, show=False)

    mm_wrapper.menus = menus


@mm_wrapper.initmethod
def init_mm_wrapper():
    mm_wrapper.add_child(game_logo)
    add_submenus(
        current="main_menu",
        menus=(main_menu, mode_selection, pause_menu, gameover_menu),
    )
    mm_wrapper.add_child(author_txt)
    mm_wrapper.add_child(MousePointer())
