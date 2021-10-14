from WGF.nodes import Scene, Button, Node, VisualNode
from WGF import Point, game, tree, RGB, base, task_mgr
from pygame import Surface
from Game.entities import MousePointer, rescale
from Game.ui import make_button, make_text
import logging

log = logging.getLogger(__name__)

bg = Surface(game.screen.get_size()).convert()
bg.fill(RGB.from_hex("cbdbfc"))
gr = game.screen.get_rect()

mm_wrapper = Scene(name="menu_wrapper", background=bg)

main_menu = Node(name="main_menu")


@main_menu.initmethod
def init_mm():
    play_button = make_button(
        name="play_button",
        text="Play",
        pos=Point(gr.centerx, gr.centery),
    )

    @play_button.clickmethod
    def play():
        log.debug("Switching to level")
        main_menu.hide()
        tree["menu_wrapper"]["mode_selection"].show()

    exit_button = make_button(
        name="exit_button",
        text="Exit",
        pos=Point(gr.centerx, gr.centery + 30),
    )

    @exit_button.clickmethod
    def exit():
        game.active = False

    main_menu.add_child(play_button)
    main_menu.add_child(exit_button)

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
        # Resetting and hiding mein menu
        mode_selection.hide()
        tree["menu_wrapper"]["main_menu"].show()
        tree["menu_wrapper"].hide()
        # Now we should proceed to game without issues
        tree["pause_screen"].show()

    back_button = make_button(
        name="back_button",
        text="Back to Menu",
        pos=Point(gr.centerx, gr.centery + 130),
    )

    @back_button.clickmethod
    def back():
        log.debug("Switching to menu")
        mode_selection.hide()
        tree["menu_wrapper"]["main_menu"].show()

    mode_selection.add_child(ms_title)
    mode_selection.add_child(ta_button)
    mode_selection.add_child(surv_button)
    mode_selection.add_child(en_button)
    mode_selection.add_child(back_button)

    @mode_selection.showmethod
    def show_ms():
        mm_wrapper.buttons = tuple(
            x for x in mode_selection.children if type(x) is Button
        )


author_txt = make_text(
    name="author_txt",
    text="© moonburnt, 2021",
    pos=Point(gr.centerx, gr.bottom - 50),
)

logo = game.assets.images["game_logo"]
logo = rescale(logo, 4)
game_logo = VisualNode(
    name="game_logo",
    surface=logo,
    pos=Point(gr.centerx, gr.top + 150),
)


@mm_wrapper.showmethod
def show():
    # Doing things like that, coz otherwise we could accidently exit game right
    # away, on clicking (during logo) on the same place as exit button
    @mm_wrapper.updatemethod
    @task_mgr.do_later(ms=300)
    def update():
        for event in game.event_handler.events:
            if event.type == base.pgl.MOUSEBUTTONDOWN:
                mm_wrapper["gun"].attack(mm_wrapper.buttons)
            elif event.type == base.pgl.MOUSEBUTTONUP:
                mm_wrapper["gun"].pullback()


mm_wrapper.add_child(game_logo)
mm_wrapper.add_child(main_menu)
mm_wrapper.add_child(mode_selection, show=False)
mm_wrapper.add_child(author_txt)
mm_wrapper.add_child(MousePointer())
