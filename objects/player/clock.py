from direct.gui.DirectButton import DirectButton
from direct.gui.DirectWaitBar import DirectWaitBar
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ConfigVariableString, LVecBase4f
from objects.notifier import Notifier
from direct.task import Task


class Day:
    days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    def __init__(self):
        self.index = 1  # Start monday

    def set(self, index):
        self.index = index
        return self.index

    def forward(self):
        self.index += 1
        if self.index >= len(self.days):
            self.index = 0
        return self.index


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
        self.bar = DirectWaitBar(text="", value=0, pos=(0, 0, .1), scale=(1, 1, 0.75), sortOrder=0)
        self.bar['barColor'] = (1, 1, 1, 1)
        self.bar['frameColor'] = (.075, .075, .075, 1)
        self.bar['frameSize'] = (-1.28, 1.28, -.050, .025)

        # the time
        self.seconds_per_hour = int(ConfigVariableString('secs-per-hour', '10').getValue())
        self.hours_in_day = int(ConfigVariableString('hours-in-day', '24').getValue())
        self.time = int(ConfigVariableString('starting-time', '600').getValue())

        self.egg = loader.loadModel("art/clock.egg")
        self.toggle = DirectButton(geom=(self.egg.find("**/pause")),
                                   relief=None,
                                   scale=0.1,
                                   pos=(0.38, 0, -.04),
                                   command=self.toggle_clock)

        self.paused = False
        self.offset_time = 0

        # start task
        self.start_clock()

    def run_clock(self, task):
        if not self.paused:
            self.bar['value'] = (task.time + self.offset_time) / self.seconds_per_hour * 100
            if task.time + self.offset_time < self.seconds_per_hour:
                return Task.cont
            self.offset_time = 0
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

    def toggle_clock(self):
        if not self.paused:
            self.notify.debug("[toggle_clock] Pausing")
            self.player.disable_actions()
            self.offset_time = (self.bar['value'] / 100) * self.seconds_per_hour
            self.toggle.setGeom(self.egg.find("**/play"))
        else:
            self.notify.debug("[toggle_clock] Unpausing")
            self.player.enable_actions()
            self.toggle.setGeom(self.egg.find("**/pause"))
        self.paused = not self.paused

    def resume_clock(self):
        """
        Resumes clock if currently disabled
        """
        if self.paused:
            self.toggle_clock()
