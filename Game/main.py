from WGF import GameWindow, AssetsLoader, shared
from os.path import join
import logging

log = logging.getLogger(__name__)

SETTINGS_PATH = join(".", "settings.toml")
LEADERBOARD_PATH = join(".", "leaderboard.json")


def load_leaderboard():
    if getattr(shared, "leaderboard", None) is None:
        from Game.leaderboard import Leaderboard

        try:
            lb = Leaderboard.from_file(LEADERBOARD_PATH)
        except Exception as e:
            log.warning(f"Unable to load leaderboard: {e}")
            # Creating default lb, in case our own doesnt exist
            lb = Leaderboard(
                {
                    "endless": [
                        {"name": "xXx_Gamer_xXx", "score": 500, "kills": 69},
                        {"name": "amogus", "score": 300, "kills": 50},
                        {"name": "Gabriel", "score": 100, "kills": 20},
                        {"name": "Default", "score": 50, "kills": 10},
                        {"name": "Karen", "score": 10, "kills": 1},
                    ]
                },
                path=LEADERBOARD_PATH,
            )
            lb.to_file()

        shared.leaderboard = lb
    return shared.leaderboard


def make_game() -> GameWindow:
    """Factory to create custom GameWindow"""
    mygame = GameWindow("WeirdLand")
    assets_directory = join(".", "Assets")
    img_directory = join(assets_directory, join("Sprites"))

    mygame.assets = AssetsLoader(
        assets_directory=assets_directory,
        fonts_directory=join(assets_directory, "Fonts"),
        sounds_directory=join(assets_directory, "Sounds"),
        font_extensions=[".ttf"],
        image_extensions=[".png"],
        sound_extensions=[".wav"],
    )
    # Overriding some built-in defaults and adding new
    mygame.settings.set_default("vsync", True)
    mygame.settings.set_default("show_fps", False)
    mygame.settings.set_default("camera_speed", 0.8)
    mygame.settings.set_default(
        "window_modes",
        {
            "double_buffer": True,
            "hardware_acceleration": True,
        },
    )
    mygame.icon_path = join(".", "icon.png")
    mygame.settings.from_toml(SETTINGS_PATH)
    mygame.init()

    mygame.assets.load_all()

    mygame.assets.spritesheets = {}

    # from WGF import shared

    load_leaderboard()

    # This is kinda janky, but also kinda not?
    shared.sprite_scale = 4
    mygame.assets.load_images(
        path=join(img_directory, "4x"),
        scale=shared.sprite_scale,
    )

    shared.extra_scale = 2
    mygame.assets.load_images(
        path=join(img_directory, "2x"),
        scale=shared.extra_scale,
    )

    # Specifying font as shared variable, since it should be used in all scenes
    shared.font = mygame.assets.load_font("./Assets/Fonts/romulus.ttf", 36)

    shared.game_paused = False

    from WGF.nodes import Align
    from WGF import Point
    from Game.ui import make_text

    fps_counter = make_text(
        name="fps_counter",
        text="",
        pos=Point(mygame.screen.get_rect().width, 0),
        align=Align.topright,
    )

    @fps_counter.updatemethod
    def update_fps():
        if not shared.game_paused:
            fps_counter.text = f"FPS: {mygame.clock.get_fps():2.0f}"

    from Game.scenes import logo, level, menus

    mygame.tree.add_child(logo.sc)
    mygame.tree.add_child(menus.mm_wrapper, show=False)
    mygame.tree.add_child(level.sc, show=False)
    mygame.tree.add_child(fps_counter, show=mygame.settings["show_fps"])

    return mygame
