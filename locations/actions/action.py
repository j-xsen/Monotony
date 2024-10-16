from direct.gui.DirectButton import DirectButton
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import DGG


class Action:
    def __init__(self, image_dir, location):
        """
        An action doable in a location
        @param image_dir: Image directory of portrait
        @param location: Location
        """
        self.maps = loader.loadModel('art/activities/activities.egg')
        self.location = location
        self.image_dir = image_dir
        self.button = None
        self.player = self.location.player

    def create_button(self):
        """
        Creates a DirectButton
        """
        self.button = DirectButton(scale=(0.6, 1, 0.3), relief=None, command=self.command,
                                   geom=(self.maps.find(self.image_dir)))

    def destroy_button(self):
        """
        Destroys the DirectButton self.button
        """
        self.button.destroy()

    def command(self):
        """
        OVERWRITE! Function ran when DirectButton pressed
        """
        pass
