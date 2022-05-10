from objects.notifier import Notifier


class Location(Notifier):
    def __init__(self, action_bar):
        Notifier.__init__(self, "location")
        self.action_bar = action_bar

    def head_to(self):
        self.notify.warning("NO head_to FOR LOCATION")
