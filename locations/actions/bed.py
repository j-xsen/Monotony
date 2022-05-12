from locations.actions.action import Action


class WakeUp(Action):
    def __init__(self, location):
        Action.__init__(self, "art/activities/wake_up.png", location)

    def command(self):
        # change stage
        self.location.set_stage(1)
