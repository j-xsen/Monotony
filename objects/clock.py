from direct.gui.DirectWaitBar import DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ConfigVariableString

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
        self.action_bar = DirectWaitBar(text="", value=50, pos=(0, 0, .1), scale=(1, 1, 0.75))
        self.action_bar['barColor'] = (1, 1, 1, 1)
        self.action_bar['frameColor'] = (0, 0, 0, 1)
        self.action_bar['frameSize'] = (-1.28, 1.28, -.050, .025)

        # the time
        self.seconds_per_hour = 5.0
        self.hours_in_day = 24
        self.time = ConfigVariableString('starting-time', '600')  # starting time, goes up in 100s

        # start task
        self.start_clock()

    def run_clock(self, task):
        self.action_bar['value'] = task.time / self.seconds_per_hour * 100

        if task.time < self.seconds_per_hour:
            return Task.cont
        self.progress_hour()
        return Task.again

    def start_clock(self):
        self.notify.debug("[start_clock] Starting the clock!")
        taskMgr.add(self.run_clock, "RunClock")

    def stop_clock(self):
        self.notify.debug("[stop_clock] Stopping the clock!")
        taskMgr.remove("RunClock")

    def progress_hour(self):
        self.time += 100
        if self.time >= self.hours_in_day * 100:
            self.time -= self.hours_in_day * 100
            # TODO do day move
            self.notify.debug("[progress_hour] End of day")