from objects.selfportrait import SelfPortrait
from objects.console import Console
from direct.showbase.ShowBase import ShowBase


class LevelHolder(ShowBase):
    def __init__(self):
        self.self_portrait = SelfPortrait()

