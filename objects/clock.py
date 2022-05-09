from direct.gui.DirectWaitBar import DirectWaitBar
from objects.notifier import Notifier


class Clock(Notifier):
    def __init__(self):
        Notifier.__init__(self, "clock")
        self.notify.debug("[__init__] Creating the clock...")
        # the clock
        self.action_bar = DirectWaitBar(text="", value=50, pos=(0, 0, .1))
        self.action_bar['barColor'] = (1, 1, 1, 1)
        self.action_bar['frameColor'] = (0, 0, 0, 1)
        self.action_bar['frameSize'] = (-1.28, 1.28, -.070, .020)

    def start_clock(self):
        self.notify.debug("[start_clock] Starting the clock!")

    def stop_clock(self):
        self.notify.debug("[stop_clock] Stopping the clock!")