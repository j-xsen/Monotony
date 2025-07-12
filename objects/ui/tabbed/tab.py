from direct.gui.DirectFrame import DirectFrame
from direct.showbase.DirectObject import DirectObject

size = .45


class Tab(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.frame = DirectFrame(frameColor=(1, 0, 0, 0),
                                 frameSize=(size - .2, -size * 2.75, size - .245, -size - .1),
                                 pos=(0, 0, -.37))

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
