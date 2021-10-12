from WGF.nodes import Scene, Button, VisualNode
from WGF import shared, Point, game, tree, RGB, base, task_mgr
from pygame import Surface
from Game.entities import MousePointer
import logging

log = logging.getLogger(__name__)

bg = Surface(game.screen.get_size()).convert()
bg.fill(RGB.from_hex("cbdbfc"))
sc = Scene(name="main_menu", background=bg)

gr = game.screen.get_rect()

play_button = Button(
    name="play_button",
    text="Play",
    font=shared.font,
    antialiasing=False,
    pos=Point(gr.centerx, gr.centery),
)


@play_button.clickmethod
def play():
    log.debug("Switching to level")
    sc.hide()
    tree["pause_screen"].show()


exit_button = Button(
    name="exit_button",
    text="Exit",
    font=shared.font,
    antialiasing=False,
    pos=Point(gr.centerx, gr.centery + 30),
)


@exit_button.clickmethod
def exit():
    game.active = False


sc.add_child(play_button)
sc.add_child(exit_button)
sc.add_child(MousePointer())

buttons = (play_button, exit_button)


@sc.showmethod
def show():
    # Doing things like that, coz otherwise we could accidently exit game right
    # away, on clicking (during logo) on the same place as exit button
    @sc.updatemethod
    @task_mgr.do_later(ms=300)
    def update():
        for event in game.event_handler.events:
            if event.type == base.pgl.MOUSEBUTTONDOWN:
                sc["gun"].attack(buttons)
            elif event.type == base.pgl.MOUSEBUTTONUP:
                sc["gun"].pullback()
