from locations.actions.action import Action
from codes.selfportraitstates import *


class WakeUp(Action):
    def __init__(self, location, _player):
        Action.__init__(self, "**/wake_up", location, _player)

    def command(self):
        # change stage
        self.location.set_stage(1)
        # update portrait
        self.location.self_portrait.update_state(PERSON)
        self.player.in_bed = False


class Eat(Action):
    def __init__(self, location, _player):
        Action.__init__(self, "**/eat", location, _player)

    def command(self):
        print("EAT")
