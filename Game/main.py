from WGF import GameWindow, base, RGB, AssetsLoader
from os.path import join
import logging

log = logging.getLogger(__name__)


def make_game() -> GameWindow:
    """Factory to create custom GameWindow"""
    mygame = GameWindow("Test")
    assets_directory = join(".", "Assets")
    mygame.assets = AssetsLoader(
        assets_directory=assets_directory,
        fonts_directory=join(assets_directory, "Fonts"),
        images_directory=join(assets_directory, "Sprites"),
        sounds_directory=join(assets_directory, "Sounds"),
        font_extensions=[".ttf"],
        image_extensions=[".png"],
        sound_extensions=[".wav"],
    )
    mygame.settings["vsync"] = True
    mygame.init()

    mygame.assets.load_all()

    from WGF import shared

    # Specifying font as shared variable, since it should be used in all scenes
    shared.font = mygame.assets.load_font("./Assets/Fonts/romulus.ttf", 36)

    from pygame import draw, Surface

    mg = mygame.tree

    @mg.initmethod
    def init():
        mg.show_fps = True
        mg.fps_bg = None

    # Modifying tree's updatemethod to implement pause support
    @mg.updatemethod
    def update():
        for event in mygame.event_handler.events:
            if event.type == base.pgl.KEYDOWN:
                if event.key == base.pgl.K_p:
                    if mg._current_child:
                        if mg._current_child.playing:
                            mg._current_child.pause()
                        else:
                            mg._current_child.play()

    # Postupdate methods run within update cycle, but after child's tasks
    # This makes it possible to draw things that should appear on top of everything
    # via these - say, fps counters
    @mg.postupdatemethod
    def postupdate():
        # #TODO: this could be reworked into task
        if mg.show_fps:
            fps = mygame.clock.get_fps()
            text = shared.font.render(f"FPS: {fps:2.0f}", False, (10, 10, 10))
            textpos = text.get_rect()

            if not mg.fps_bg or mg.fps_bg.get_rect() < textpos:
                mg.fps_bg = Surface((textpos.w, textpos.h))

            fps_pos = mg.fps_bg.get_rect()
            fps_pos.topright = mygame.screen.get_rect().topright
            mg.fps_bg.fill(RGB(255, 255, 255))
            mg.fps_bg.blit(text, textpos)

            mygame.screen.blit(mg.fps_bg, fps_pos)

    from Game.scenes import logo, intro

    mg.add(logo.sc, default=True)
    mg.add(intro.sc)

    return mygame
