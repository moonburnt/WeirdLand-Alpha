from WGF import GameWindow, base, RGB, Size, AssetsLoader
from os.path import join
import logging

log = logging.getLogger(__name__)


def make_game() -> GameWindow:
    """Factory to create custom GameWindow"""
    mygame = GameWindow("Whatever Shooting Game")
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

    def show_pause_msg():
        text = shared.font.render("PAUSED", False, (10, 10, 10))
        textpos = text.get_rect()
        gr = mygame.screen.get_rect()
        textpos.centerx = gr.centerx
        textpos.centery = gr.centery
        frame = Surface(Size(108, 32)).convert()
        frame.fill(RGB.from_hex("3f3f74"))
        mygame.screen.blit(frame, textpos)
        mygame.screen.blit(text, textpos)

    @mg.initmethod
    def init():
        mg.show_fps = True
        mg.game_paused = False

    # Modifying tree's updatemethod to implement pause support
    @mg.updatemethod
    def update():
        for event in mygame.event_handler.events:
            if event.type == base.pgl.KEYDOWN:
                if event.key == base.pgl.K_p:
                    if mg._current_child:
                        if mg._current_child.playing:
                            mg._current_child.pause()
                            mg.game_paused = True
                        else:
                            mg._current_child.play()
                            mg.game_paused = False

    # Postupdate methods run within update cycle, but after child's tasks
    # This makes it possible to draw things that should appear on top of everything
    # via these - say, fps counters
    @mg.postupdatemethod
    def postupdate():
        if mg.show_fps and not mg.game_paused:
            fps = mygame.clock.get_fps()
            text = shared.font.render(f"FPS: {fps:2.0f}", False, (10, 10, 10))
            textpos = text.get_rect()

            textpos.topright = mygame.screen.get_rect().topright
            mygame.screen.blit(text, textpos)

        if mg.game_paused:
            show_pause_msg()

    from Game.scenes import logo, level

    mg.add(logo.sc, default=True)
    mg.add(level.sc)

    return mygame
