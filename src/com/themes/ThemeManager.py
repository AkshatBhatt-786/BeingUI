import os
import sys
import yaml
from types import SimpleNamespace
from rich import print
from icecream import ic

ic.configureOutput(prefix="[System.BeingUI]: ")


class ThemeManager:

    def __init__(self, **kwargs):
        self._palette = kwargs.get("palette", "butterscotch")
        ic("Initialising [ThemeManager]")
        self._instantiation = {
            "init_palette": False,
            "init_theme": False
        }
        self.colors = self._init_palette()


    def _init_palette(self):

        def dict_to_namespace(d):
            if isinstance(d, dict):
                return SimpleNamespace(**{
                    k: dict_to_namespace(v) for k, v in d.items()
                })
            return d

        try:
            ic(f"Loading palette configurations for {self._palette}")
            path = self.getPath(f"colors\\{self._palette}.yaml")
            if not path:
                ic("Palette configurations not Found!")
                ic(f"Path: {path}")
                return
            with open(path, "r") as pt_file:
                data = yaml.safe_load(pt_file)
                colors = dict_to_namespace(data["Colors"])
                ic(f"Loaded palette: {path}")
                self._instantiation["init_palette"] = True
                return colors
        except Exception as e:
            ic(e)

    @staticmethod
    def getPath(filename: str):
        try:
            base = sys._MEIPASS
        except AttributeError as e:
            base = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(base, filename)
        if os.path.exists(path):
            return path
        return None
