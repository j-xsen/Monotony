from direct.gui import DirectButton

from objects.clock import Clock
from direct.showbase.ShowBase import ShowBase
from objects.selfportrait import SelfPortrait
from objects.console import Console
from panda3d.core import loadPrcFile, Multifile, VirtualFileSystem, TransparencyAttrib
from objects.player import Player
from objects.statswidget import StatsWidget
from objects.action_bar import ActionBar

loadPrcFile("config/Config.prc")


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
        self.self_portrait = SelfPortrait()
        self.console = None
        self.accept("`", self.pressed_tilda)

        self.action_bar = ActionBar()
        self.clock = Clock()
        self.player = Player(self, self.clock)
        self.clock.add_player(self.player)

        self.stats_widget = StatsWidget(self.player, self.clock)

    def test(self):
        print("YUP")

    def pressed_tilda(self):
        if self.console is None:
            self.console = Console(self)
        else:
            self.console.destroy()
            self.console = None




app = Monotony()
app.run()