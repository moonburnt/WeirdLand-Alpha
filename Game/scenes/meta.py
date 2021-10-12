from pygame import draw, Surface
from WGF import game, Size, RGB, Point, shared, base
from WGF.nodes import Node, TextNode, Align
import logging

log = logging.getLogger(__name__)

__all__ = [
    "pause_wrapper",
    "pause_msg",
    "fps_counter",
]

# #TODO: this could be turned into reusable decorator, I think
pause_wrapper = Node(name="pause_screen")
pause_wrapper.game_paused = False


@pause_wrapper.updatemethod
def update():
    for event in game.event_handler.events:
        if event.type == base.pgl.KEYDOWN:
            if event.key == base.pgl.K_p:
                # pause_wrapper.toggle_pause()
                if pause_wrapper.game_paused:
                    for child in pause_wrapper.children:
                        child.play()
                    pause_wrapper.game_paused = False
                    pause_msg.hide()
                else:
                    # if not pause_wrapper.game_paused:
                    for child in pause_wrapper.children:
                        child.pause()
                    pause_wrapper.game_paused = True
                    pause_msg.show()


gr = game.screen.get_rect()
frame = Surface(Size(108, 32)).convert()
frame.fill(RGB.from_hex("3f3f74"))
pause_msg = TextNode(
    name="pause_msg",
    text="PAUSED",
    font=shared.font,
    antialiasing=False,
    pos=Point(gr.centerx, gr.centery),
    frame=frame,
)
pause_wrapper.add_child(pause_msg, show=False)

fps_counter = TextNode(
    name="fps_counter",
    text="",
    font=shared.font,
    antialiasing=False,
    pos=Point(gr.width, 0),
    align=Align.topright,
)


@fps_counter.updatemethod
def update_fps():
    if not pause_wrapper.game_paused:
        fps_counter.text = f"FPS: {game.clock.get_fps():2.0f}"
