from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import DGG
from direct.gui.DirectWaitBar import DirectWaitBar
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ConfigVariableString

from objects.notifier import Notifier


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


class Clock(Notifier, DirectObject):
    def __init__(self):
        """
        Clock object that holds:
        - Task ("RunClock") that progresses hours
            = Deteriorates player
        - bar: A clock widget showing the progress between hours
        - toggle: The pause/play button

        Variables for time settings are in config/Config.prc
        - starting-time 600
        - secs-per-hour 5
        - hours-in-day 24
        """
        Notifier.__init__(self, "clock")

        # the clock bar
        self.bar = DirectWaitBar(text="", value=0, pos=(0, 0, .1), scale=(1, 1, 0.75), sortOrder=0)
        self.bar['barColor'] = (1, 1, 1, 1)
        self.bar['frameColor'] = (.075, .075, .075, 1)
        self.bar['frameSize'] = (-1.28, 1.28, -.050, .025)

        # the time
        self.seconds_per_hour = int(ConfigVariableString('secs-per-hour', '10').getValue())
        self.hours_in_day = int(ConfigVariableString('hours-in-day', '24').getValue())
        self.time = int(ConfigVariableString('starting-time', '600').getValue())

        self.click_sounds = [base.loader.loadSfx("art/sounds/resume.ogg"),
                             base.loader.loadSfx("art/sounds/pause.ogg")]
        for sound in self.click_sounds:
            sound.setVolume(0.35)

        self.egg = loader.loadModel("art/clock.egg")
        self.toggle = DirectButton(geom=self.egg.find("**/pause"),
                                   relief=None,
                                   scale=0.1,
                                   pos=(0.38, 0, -.04),
                                   command=self.toggle_clock,
                                   clickSound=self.click_sounds[0])

        self.paused = False
        self.double_pause = False
        self.offset_time = 0

        # start task
        self.start_clock()

        self.accept("clock_disable_pausing", self.disable_pausing)
        self.accept("clock_enable_pausing", self.enable_pausing)
        self.accept("clock_pause", self.pause_clock)
        self.accept("clock_toggle", self.toggle_clock)
        self.accept("clock_resume", self.resume_clock)
        self.accept("clock_set_speed", self.set_speed)

    def set_speed(self, args):
        self.notify.debug(f"Settings seconds per hour to {self.seconds_per_hour}/{args}")
        self.seconds_per_hour /= float(args)
        self.notify.debug(f"new seconds per hour: {self.seconds_per_hour}")

    def disable_pausing(self):
        tint = .4
        self.toggle["state"] = DGG.DISABLED
        self.toggle.setColor(tint, tint, tint, 1)

    def enable_pausing(self):
        self.toggle["state"] = DGG.NORMAL
        self.toggle.setColor(1, 1, 1, 1)

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
        messenger.send(self.time)
        if self.time >= self.hours_in_day * 100:
            self.time -= self.hours_in_day * 100
            # TODO do day move
            self.notify.debug("[progress_hour] End of day")
        messenger.send("deteriorate")

    def toggle_clock(self):
        if not self.paused:
            self.notify.debug("[toggle_clock] Pausing")
            self.toggle["clickSound"] = self.click_sounds[1]
            messenger.send("disable_actions")
            self.offset_time = (self.bar['value'] / 100) * self.seconds_per_hour
            self.toggle.setGeom(self.egg.find("**/play"))
        else:
            self.notify.debug("[toggle_clock] Unpausing")
            self.toggle["clickSound"] = self.click_sounds[0]
            messenger.send("enable_actions")
            self.toggle.setGeom(self.egg.find("**/pause"))
        self.paused = not self.paused
        self.double_pause = False

    def resume_clock(self):
        """
        Resumes clock if currently disabled
        """
        if self.double_pause:
            self.double_pause = False
        else:
            if self.paused:
                self.toggle_clock()

    def pause_clock(self):
        if not self.paused:
            self.toggle_clock()
        else:
            self.double_pause = True

    def destroy(self):
        self.ignore_all()
