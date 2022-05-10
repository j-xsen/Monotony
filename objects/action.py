from direct.gui.DirectButton import DirectButton


class Action(DirectButton):
    def __init__(self, image_dir):
        DirectButton.__init__(self)
        self.setImage(image_dir)