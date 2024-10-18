from direct.gui.DirectWaitBar import DirectWaitBar
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ConfigVariableString
from objects.notifier import Notifier
from direct.task import Task


class Clock(Notifier):
    def __init__(self, player):
        """
        Clock object that holds:
        - Task ("RunClock") that progresses hours
            = Deteriorates player
        - bar: A clock widget showing the progress between hours

        Variables for time settings are in config/Config.prc
        - starting-time 600
        - secs-per-hour 5
        - hours-in-day 24

        @param player: The Player object
        """
        Notifier.__init__(self, "clock")
        self.player = player

        # the clock bar
        self.bar = DirectWaitBar(text="", value=0, pos=(0, 0, .1), scale=(1, 1, 0.75))
        self.bar['barColor'] = (1, 1, 1, 1)
        self.bar['frameColor'] = (0, 0, 0, 1)
        self.bar['frameSize'] = (-1.28, 1.28, -.050, .025)

        # the time
        self.seconds_per_hour = int(ConfigVariableString('secs-per-hour', '10').getValue())
        self.hours_in_day = int(ConfigVariableString('hours-in-day', '24').getValue())
        self.time = int(ConfigVariableString('starting-time', '600').getValue())

        # start task
        self.start_clock()

    def run_clock(self, task):
        self.bar['value'] = task.time / self.seconds_per_hour * 100
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
        self.player.deteriorate()
        if self.time >= self.hours_in_day * 100:
            self.time -= self.hours_in_day * 100
            # TODO do day move
            self.notify.debug("[progress_hour] End of day")
        self.player.stats_widget.update_stats()