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

from WGF.nodes import Button, TextNode, Align
from WGF import shared, Point, RGB
from pygame import Surface
import logging

log = logging.getLogger(__name__)


def make_button(
    name: str,
    text: str,
    pos: Point,
    clickmethod: callable = None,
    active: bool = True,
) -> Button:
    return Button(
        name=name,
        text=text,
        font=shared.font,
        antialiasing=False,
        color=RGB(0, 0, 0) if active else RGB.from_hex("222034"),
        clickmethod=clickmethod,
        pos=pos,
    )


def make_text(
    name: str, text: str, pos: Point, align: Align = Align.center, frame=None
) -> TextNode:
    return TextNode(
        name=name,
        text=text,
        font=shared.font,
        antialiasing=False,
        align=align,
        pos=pos,
        frame=frame,
    )
