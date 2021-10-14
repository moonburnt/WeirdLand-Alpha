from WGF import game, RGB, Point, base, shared, tree, clock
from WGF.nodes import Scene, TextNode, VisualNode
from Game.entities import rescale
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

    img = game.assets.images["trashhead"]
    img = rescale(img, 4)

    icon = VisualNode(
        name="icon",
        surface=img,
        pos=Point(gr.centerx - 400, gr.centery),
    )

    logo = TextNode(
        name="logo",
        text="This game has been made with pygame+WGF",
        font=shared.font,
        antialiasing=False,
        pos=Point(gr.centerx, gr.centery),
    )
    sc["icon"] = icon
    sc["logo"] = logo


@sc.showmethod
def show():
    # Hiding game's mouse
    game.mouse.set_visible(False)

    # Scheduling logo scene to auto skip to next one in 3 seconds
    sc.time = 3000


def switch():
    # #TODO: idk how to re-implement switch functionality properly
    log.debug("Switching to menu")
    sc.hide()
    tree["menu_wrapper"].show()


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
