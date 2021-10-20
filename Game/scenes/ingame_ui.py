from WGF.nodes import Node, Align, VisualNode, Group
from WGF import shared, Point, game
from Game.ui import make_text
import logging

log = logging.getLogger(__name__)

hud = Node("player_hud")

score = make_text(
    name="score",
    text="SCORE: 0",
    pos=Point(5, 0),
    align=Align.topleft,
)

kill_counter = make_text(
    name="kill_counter",
    text="KILLS: 0",
    pos=Point(5, 20),
    align=Align.topleft,
)

bullets = Group(name="bullets")
# max bullet amount is 7 there
pos_x, pos_y = game.screen.get_size()
pos_y -= 50
pos_x -= 10
for i in range(0, 7):
    bullet = VisualNode(
        name="bullet",
        surface=game.assets.images["bullet"],
        pos=Point(pos_x, pos_y),
        align=Align.topright,
    )
    bullets.add_child(bullet)
    pos_x -= 25

hud.add_child(score)
hud.add_child(kill_counter)
hud.add_child(bullets)


@hud.updatemethod
def update():
    hud["score"].text = f"SCORE: {shared.score}"
    hud["kill_counter"].text = f"KILLS: {shared.kill_counter}"
