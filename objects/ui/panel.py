from direct.gui.DirectFrame import DirectFrame

from objects.notifier import Notifier


class Panel(Notifier):
    def __init__(self, name, frame_size=(-1, 1, -1, 1), pos=(0, 0, 0), sort=0):
        """
        UI Widget that has a box
        """
        Notifier.__init__(self, name)

        # create background box
        self.background = None
        self.frame_size = frame_size
        self.pos = pos
        self.sort = sort
        self.create_background()

    def create_background(self):
        self.background = DirectFrame(frameColor=(1, 1, 1, 1),
                                      frameTexture='art/drawn_square.png',
                                      frameSize=self.frame_size,
                                      pos=self.pos, sortOrder=self.sort)

    def destroy(self):
        self.background.destroy()
        self.background = None
