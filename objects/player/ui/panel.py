from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

from objects.notifier import Notifier


class Panel(Notifier):
    def __init__(self, name):
        """
        UI Widget that has a box
        """
        Notifier.__init__(self, name)

        # create background box
        self.background = OnscreenImage(image='art/action_bar.png')
        self.background.setTransparency(TransparencyAttrib.MAlpha)
