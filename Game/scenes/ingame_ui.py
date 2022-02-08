## WeirdLand - an arcade shooting game.
## Copyright (c) 2021 moonburnt
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt

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
