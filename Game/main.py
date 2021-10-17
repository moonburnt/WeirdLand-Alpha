from WGF import GameWindow, AssetsLoader
from os.path import join
import logging

log = logging.getLogger(__name__)

SETTINGS_PATH = join(".", "settings.toml")


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

    from WGF import shared

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

    from Game.scenes import logo, level, menus, meta

    meta.pause_wrapper.add_child(level.sc)
    mygame.tree.add_child(logo.sc)
    mygame.tree.add_child(menus.mm_wrapper, show=False)
    mygame.tree.add_child(meta.pause_wrapper, show=False)
    mygame.tree.add_child(meta.fps_counter, show=mygame.settings["show_fps"])

    return mygame
