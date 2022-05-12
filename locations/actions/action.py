from direct.gui.DirectButton import DirectButton
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import DGG


class Action:
    def __init__(self, image_dir, location):
        self.maps = loader.loadModel('art/activities/activities.egg')
        self.location = location
        self.image_dir = image_dir
        self.button = None

    def create_button(self):
        self.button = DirectButton(scale=(0.6, 1, 0.3), relief=None, command=self.command,
                                   geom=(self.maps.find(self.image_dir)))

    def destroy_button(self):
        self.button.destroy()

    def command(self):
        print("NO command WRITTEN")
