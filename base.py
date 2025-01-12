from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import loadPrcFile

from objects.clock import Clock
from objects.locations.location import LocationHandler
from objects.notifier import Notifier
from objects.ui.tab import TabContainer
from objects.ui.selfportrait import SelfPortrait

loadPrcFile("config/Config.prc")

from direct.showbase.ShowBase import ShowBase
from objects.ui.console.console import Console
from panda3d.core import Multifile, VirtualFileSystem
from objects.player.player import Player


class Monotony(ShowBase, Notifier):

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

        # music
        self.current_song = 0
        self.swap_songs()

        self.setBackgroundColor(0, 0, 0)

        self.console = None

        self.clock = Clock()
        self.detail_rectangle = TabContainer(self.clock)
        self.player = Player(self.clock)
        self.location_holder = LocationHandler()
        self.self_portrait = SelfPortrait()

        # Controls
        self.accept("`", self.pressed_tilda)
        self.accept("escape", self.userExit)
        self.accept("swap_songs", self.swap_songs)

    def swap_songs(self):
        taskMgr.remove("MusicSwap")

        volume = 0.05

        if self.current_song != 1:
            self.notify.debug("Playing song One")
            song_one = self.loader.loadMusic("art/music/song_1.mp3")
            song_one.setVolume(volume)
            song_one.play()
            self.current_song = 1
            taskMgr.doMethodLater(song_one.length()+3, self.swap_songs_event, "MusicSwap")
        elif self.current_song == 1:
            self.notify.debug("playing song Two")
            song_two = self.loader.loadMusic("art/music/song_2.mp3")
            song_two.setVolume(volume)
            song_two.play()
            self.current_song = 2
            taskMgr.doMethodLater(song_two.length()+3, self.swap_songs_event, "MusicSwap")

    def swap_songs_event(self, event):
        self.swap_songs()

    def pressed_tilda(self):
        if self.console is None:
            self.console = Console(self)
        else:
            self.console.destroy()
            self.console = None


app = Monotony()
app.run()
