from objects.locations.actions.action import Action
from codes.selfportraitstates import *


class WakeUp(Action):
    def __init__(self, location, _player):
        Action.__init__(self, "**/wake_up", location)

    def command(self):
        # change stage
        self.location.set_stage(1)
        # update portrait
        self.location.self_portrait.update_state(PERSON)
        # change player variable for deteriorate
        self.player.in_bed = False


class Eat(Action):
    def __init__(self, location, _player):
        Action.__init__(self, "**/eat", location)

    def command(self):
        self.player.hunger += 10
