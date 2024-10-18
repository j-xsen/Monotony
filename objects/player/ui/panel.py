from direct.gui.DirectFrame import DirectFrame

from objects.notifier import Notifier


class Panel(Notifier):
    def __init__(self, name):
        """
        UI Widget that has a box
        """
        Notifier.__init__(self, name)

        # create background box
        self.background = DirectFrame(frameColor=(1, 1, 1, 1),
                                      frameTexture='art/activities/drawn_square.png',
                                      frameSize=(5, 0, 10, 0),
                                      pos=(1, 0, 1))
