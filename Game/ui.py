from WGF.nodes import Button, TextNode, Align
from WGF import shared, Point, RGB
from pygame import Surface
import logging

log = logging.getLogger(__name__)


def make_button(name: str, text: str, pos: Point, active: bool = True) -> Button:
    return Button(
        name=name,
        text=text,
        font=shared.font,
        antialiasing=False,
        color=RGB(0, 0, 0) if active else RGB.from_hex("222034"),
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
