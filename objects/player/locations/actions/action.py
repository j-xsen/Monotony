from direct.gui.DirectButton import DirectButton


class Action:
    def __init__(self, image_dir, player):
        """
        An action doable in a location
        @param image_dir: Image directory of portrait
        @param player: player object
        """
        self.image_dir = image_dir
        self.button = None
        self.player = player

    def create_button(self):
        """
        Creates a DirectButton
        """
        self.button = DirectButton(scale=(0.6, 1, 0.3), relief=None, command=self.command,
                                   geom=(self.player.action_bar.maps.find(self.image_dir)))

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
