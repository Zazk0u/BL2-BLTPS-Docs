import unrealsdk

from pathlib import Path

from mods_base import build_mod, SETTINGS_DIR, get_pc

from mods_base.options import BaseOption, SliderOption


__version__: str
__version_info__: tuple[int, ...]


def set_fov(option:BaseOption, value:float):
    for d in unrealsdk.find_all("PlayerClassDefinition"):
        d.FOV = value
    get_pc().SetFOV(value)


fov_setting = SliderOption("FOV", 80, 0, 999, 1, True, on_change=set_fov)


build_mod(
    options=[fov_setting],
    settings_file=Path(f"{SETTINGS_DIR}/bl1_fov_controller.json")
)