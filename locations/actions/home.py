from locations.actions.action import Action
from codes.selfportraitstates import *


class WakeUp(Action):
    def __init__(self, location):
        Action.__init__(self, "**/wake_up", location)

    def command(self):
        # change stage
        self.location.set_stage(1)
        # update portrait
        self.location.self_portrait.update_state(PERSON)


class Eat(Action):
    def __init__(self, location):
        Action.__init__(self, "**/eat", location)

    def command(self):
        print("EAT")
