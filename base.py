from panda3d.core import loadPrcFile

loadPrcFile("config/Config.prc")

from direct.showbase.ShowBase import ShowBase
from objects.ui.console.console import Console
from panda3d.core import Multifile, VirtualFileSystem
from objects.player.player import Player


class Monotony(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.vfs = VirtualFileSystem.getGlobalPtr()
        self.multifile = Multifile()
        self.multifile.openReadWrite("art.mf")

        if self.vfs.mount(self.multifile, ".", VirtualFileSystem.MFReadOnly):
            self.notify.debug("mounted art.mf!")
        else:
            self.notify.error("Unable to mount art.mf!")

        self.setBackgroundColor(0, 0, 0)
        self.console = None
        self.accept("`", self.pressed_tilda)

        self.player = Player()

    def pressed_tilda(self):
        if self.console is None:
            self.console = Console(self)
        else:
            self.console.destroy()
            self.console = None


app = Monotony()
app.run()
