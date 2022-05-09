from direct.gui.DirectGuiGlobals import SUNKEN, RAISED, GROOVE, RIDGE
from direct.gui.DirectWaitBar import DirectWaitBar
from direct.showbase.ShowBase import ShowBase
from objects.selfportrait import SelfPortrait
from objects.console import Console


class Monotony(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.setBackgroundColor(0, 0, 0)
        self.self_portrait = SelfPortrait()
        self.console = None
        self.accept("`", self.pressed_tilda)

        self.bar = DirectWaitBar(text="", value=50, pos=(0, 0, .1))
        self.bar['barColor'] = (1, 1, 1, 1)
        self.bar['frameColor'] = (0, 0, 0, 1)
        self.bar['frameSize'] = (-1.28, 1.28, -.070, .020)

    def pressed_tilda(self):
        if self.console is None:
            self.console = Console(self)
        else:
            self.console.destroy()
            self.console = None




app = Monotony()
app.run()