from direct.gui.DirectWaitBar import DirectWaitBar
from direct.task.TaskManagerGlobal import taskMgr

from objects.notifier import Notifier
from direct.task import Task


class Clock(Notifier):
    """
    Every x seconds, a clock cycle is finished
    A clock cycle symbolizes an hour
    """
    def __init__(self):
        Notifier.__init__(self, "clock")

        # the clock
        self.action_bar = DirectWaitBar(text="", value=50, pos=(0, 0, .1))
        self.action_bar['barColor'] = (1, 1, 1, 1)
        self.action_bar['frameColor'] = (0, 0, 0, 1)
        self.action_bar['frameSize'] = (-1.28, 1.28, -.050, .025)

        # the time
        self.seconds_per_hour = 3.0
        self.time = 0 # goes up in 100s

        # start task
        self.start_clock()

    def run_clock(self, task):
        self.action_bar['value'] = (task.time % self.seconds_per_hour) / self.seconds_per_hour * 100
        if (task.time % self.seconds_per_hour) < self.seconds_per_hour:
            return Task.cont
        # its been an hour
        self.action_bar['value'] = 0
        # run again
        Task.again

    def start_clock(self):
        self.notify.debug("[start_clock] Starting the clock!")
        taskMgr.add(self.run_clock, "RunClock")

    def stop_clock(self):
        self.notify.debug("[stop_clock] Stopping the clock!")
        taskMgr.remove("RunClock")

    def progress_hour(self):
        self.time += 100
        if self.time >= 2400:
            self.time -= 2400
            # TODO do hour move
            self.notify.debug("[progres_hour] End of hour")