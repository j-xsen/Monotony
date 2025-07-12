from direct.gui.DirectFrame import DirectFrame
from direct.showbase.DirectObject import DirectObject

from objects.notifier import Notifier
from objects.ui.UIConstants import UIConstants


class Panel(Notifier, DirectObject):
    def __init__(self, name: str, frame_size: tuple = (-1, 1, -1, 1), pos: tuple = (0, 0, 0), sort: int = 0):
        """
        :param name: Name to give to Notifier
        :type name: str
        :param frame_size: Size of the background box
        :type frame_size: tuple
        :param pos: Position of the panel
        :type pos: tuple
        :param sort: Sort order of the panel
        :type sort: int
        """
        Notifier.__init__(self, name)

        # create background box
        self.background = None
        self.frame_size = frame_size
        self.pos = pos
        self.sort = sort
        self.create_background()

    def create_background(self):
        self.background = DirectFrame(frameColor=UIConstants.COLOR_ENABLE,
                                      frameTexture='art/drawn_square.png',
                                      frameSize=self.frame_size,
                                      pos=self.pos, sortOrder=self.sort)

    def destroy(self):
        self.background.destroy()
        self.background = None
