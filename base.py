from objects.clock import Clock
from direct.showbase.ShowBase import ShowBase
from objects.selfportrait import SelfPortrait
from objects.console import Console
from panda3d.core import loadPrcFile

loadPrcFile("config/Config.prc")


class Monotony(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.setBackgroundColor(0, 0, 0)
        self.self_portrait = SelfPortrait()
        self.console = None
        self.accept("`", self.pressed_tilda)

        self.clock = Clock()

    def pressed_tilda(self):
        if self.console is None:
            self.console = Console(self)
        else:
            self.console.destroy()
            self.console = None




app = Monotony()
app.run()