from WGF.nodes import Node, TextNode
from WGF import shared, Point, game
import logging

log = logging.getLogger(__name__)

hud = Node("player_hud")

score = TextNode(
    name="score",
    text="Score: 0",
    font=shared.font,
    antialiasing=False,
    pos=(Point(60, 10)),
)
# score.last_len = len(score.text)
kill_counter = TextNode(
    name="kill_counter",
    text="Kills: 0",
    font=shared.font,
    antialiasing=False,
    pos=(Point(60, 30)),
)
# kill_counter.last_len = len(kill_counter.text)

hud.add_child(score)
hud.add_child(kill_counter)

# #TODO: add some optional "align" argument that switches align of node from
# center.x, center.y to top left or whatever, so this whole len/reposition garbage
# could be easily removed
# def reposition(node, new_len:int):
#     if node.last_len != new_len:
#         diff = new_len - node.last_len
#         node.pos = Point((node.pos.x + diff*5), node.pos.y)
#         node.last_len = new_len


@hud.updatemethod
def update():
    hud["score"].text = f"Score: {shared.score}"
    # reposition(hud["score"], len(hud["score"].text))
    hud["kill_counter"].text = f"Kills: {shared.kill_counter}"
    # reposition(hud["kill_counter"], len(hud["kill_counter"].text))
