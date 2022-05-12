from direct.gui.DirectButton import DirectButton
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import DGG


class Action:
    def __init__(self, image_dir, location):
        maps = loader.loadModel('art/activities/activities.egg')
        self.location = location
        self.button = DirectButton(scale=(0.6, 1, 0.3), relief=None, command=self.command,
                                   geom=(maps.find('**/wake_up')))

    def command(self):
        print("NO command WRITTEN")
