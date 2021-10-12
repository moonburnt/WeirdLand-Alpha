from WGF.nodes import Node, TextNode, Align
from WGF import shared, Point, game
import logging

log = logging.getLogger(__name__)

hud = Node("player_hud")

score = TextNode(
    name="score",
    text="SCORE: 0",
    font=shared.font,
    antialiasing=False,
    pos=(Point(5, 0)),
    align=Align.topleft,
)

kill_counter = TextNode(
    name="kill_counter",
    text="KILLS: 0",
    font=shared.font,
    antialiasing=False,
    pos=(Point(5, 20)),
    align=Align.topleft,
)

hud.add_child(score)
hud.add_child(kill_counter)


@hud.updatemethod
def update():
    hud["score"].text = f"SCORE: {shared.score}"
    hud["kill_counter"].text = f"KILLS: {shared.kill_counter}"
