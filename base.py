from panda3d.core import loadPrcFile

from objects.clock import Clock
from objects.locations.location import LocationHandler
from objects.ui.detailrectangle import DetailRectangle
from objects.ui.selfportrait import SelfPortrait

loadPrcFile("config/Config.prc")

from direct.showbase.ShowBase import ShowBase
from objects.ui.console.console import Console
from panda3d.core import Multifile, VirtualFileSystem
from objects.player.player import Player


class Monotony(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Open Multfile
        self.vfs = VirtualFileSystem.getGlobalPtr()
        self.multifile = Multifile()
        self.multifile.openReadWrite("art.mf")

        if self.vfs.mount(self.multifile, ".", VirtualFileSystem.MFReadOnly):
            self.notify.debug("mounted art.mf!")
        else:
            self.notify.error("Unable to mount art.mf!")

        self.setBackgroundColor(0, 0, 0)

        self.console = None

        self.clock = Clock()
        self.detail_rectangle = DetailRectangle(self.clock)
        self.player = Player(self.clock)
        self.location_holder = LocationHandler()
        self.self_portrait = SelfPortrait()

        # Controls
        self.accept("`", self.pressed_tilda)
        self.accept("escape", self.userExit)

    def pressed_tilda(self):
        if self.console is None:
            self.console = Console(self)
        else:
            self.console.destroy()
            self.console = None


app = Monotony()
app.run()
