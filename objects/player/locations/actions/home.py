from objects.player.locations.actions.action import Action
from objects.player.selfportrait import PERSON


class WakeUp(Action):
    def __init__(self, player):
        Action.__init__(self, "**/wake_up", player)

    def command(self):
        # change stage
        self.player.location_object.set_stage(1)
        # update portrait
        self.player.self_portrait.update_state(PERSON)
        # change player variable for deteriorate
        self.player.in_bed = False


class Eat(Action):
    def __init__(self, player):
        Action.__init__(self, "**/eat", player)

    def command(self):
        self.player.feed()
