from WGF import game, RGB, Point, base, shared, tree, clock
from WGF.nodes import Scene, TextNode
from Game import entities
from pygame import sprite, transform, Surface
import logging

log = logging.getLogger(__name__)

# Scene blueprint
bg = Surface(game.screen.get_size()).convert()
bg.fill(RGB(255, 255, 255))

sc = Scene(name="intro", background=bg)


@sc.initmethod
def init():
    gr = game.screen.get_rect()
    sc.text = TextNode(
        name="logo",
        text="Hello, World!",
        font=shared.font,
        antialiasing=False,
        pos=Point(gr.centerx, gr.centery),
    )
    sc.add_child(sc.text, show=False)


@sc.showmethod
def show():
    sc.text.show()

    # Hiding game's mouse
    game.mouse.set_visible(False)

    # Scheduling logo scene to auto skip to next one in 3 seconds
    sc.time = 3000


def switch():
    # #TODO: idk how to re-implement switch functionality properly
    log.debug("Switching to menu")
    sc.hide()
    tree["main_menu"].show()


@sc.updatemethod
def updater():
    for event in game.event_handler.events:
        if event.type == base.pgl.MOUSEBUTTONDOWN:
            switch()
            return

    sc.time -= clock.get_time()
    if sc.time > 0:
        return

    switch()
