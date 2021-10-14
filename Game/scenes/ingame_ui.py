from WGF.nodes import Node, Align
from WGF import shared, Point, game
from Game.ui import make_text
import logging

log = logging.getLogger(__name__)

hud = Node("player_hud")

score = make_text(
    name="score",
    text="SCORE: 0",
    pos=(Point(5, 0)),
    align=Align.topleft,
)

kill_counter = make_text(
    name="kill_counter",
    text="KILLS: 0",
    pos=(Point(5, 20)),
    align=Align.topleft,
)

hud.add_child(score)
hud.add_child(kill_counter)


@hud.updatemethod
def update():
    hud["score"].text = f"SCORE: {shared.score}"
    hud["kill_counter"].text = f"KILLS: {shared.kill_counter}"
