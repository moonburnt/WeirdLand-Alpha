from WGF.nodes import Scene, Button, Node, TextNode
from WGF import shared, Point, game, tree, RGB, base, task_mgr
from pygame import Surface
from Game.entities import MousePointer
import logging

log = logging.getLogger(__name__)

bg = Surface(game.screen.get_size()).convert()
bg.fill(RGB.from_hex("cbdbfc"))
gr = game.screen.get_rect()


def make_button(name: str, text: str, pos: Point, active: bool = True) -> Button:
    return Button(
        name=name,
        text=text,
        font=shared.font,
        antialiasing=False,
        color=RGB(0, 0, 0) if active else RGB.from_hex("222034"),
        pos=pos,
    )


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
    ms_title = TextNode(
        name="ms_title",
        text="Select Gamemode",
        font=shared.font,
        antialiasing=False,
        pos=Point(gr.centerx, gr.centery - 100),
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
        pos=Point(gr.centerx, gr.centery + 160),
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


mm_wrapper.add_child(main_menu)
mm_wrapper.add_child(mode_selection, show=False)
mm_wrapper.add_child(MousePointer())
